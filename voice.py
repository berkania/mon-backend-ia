import pygame
import speech_recognition as sr
import time
from gtts import gTTS
import os
import globals
from utils import extraire_voyelles, supprimer_fichier_audio


# Initialisation de la reconnaissance vocale
listener = sr.Recognizer()


print("Liste des microphones disponibles :")
for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Micro {i}: {microphone_name}")


def ecoute():
    """Capture la voix de l'utilisateur et renvoie le texte reconnu."""
    try:
        # Remplace device_index par l'index correct de ton micro, trouvé dans la liste ci-dessus
        with sr.Microphone(device_index=0) as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Parle...")
            # timeout=5 secondes max, phrase_time_limit=10 secondes max
            audio = listener.listen(source, timeout=5, phrase_time_limit=10)
            print("🔎 Reconnaissance...")
            texte = listener.recognize_google(audio, language='fr-FR')
            print("🔊 Tu as dit:", texte)
            return texte.lower()
    except Exception as e:
        print("Erreur de reconnaissance vocale:", e)
        return ""


def parle(text):
    """Fait parler le bot et anime le visage selon les voyelles."""
    print("🤖:", text)
    tts = gTTS(text=text, lang='fr')
    nom_fichier = f"reponse_{int(time.time())}.mp3"
    tts.save(nom_fichier)

    # Lecture avec pygame
    pygame.mixer.music.load(nom_fichier)
    pygame.mixer.music.play()

    # Durée approximative du texte
    duree = len(text) * 0.06
    voyelles = extraire_voyelles(text)
    animer_avec_voyelles(voyelles, duree)

    # Retour à l'expression neutre
    globals.expression_actuelle = globals.expressions["neutre"][0]

    # Nettoyage du fichier audio temporaire
    supprimer_fichier_audio(nom_fichier)


def animer_avec_voyelles(voyelles, duree_totale):
    """Anime les expressions en fonction des voyelles prononcées."""
    if not voyelles:
        voyelles = ["neutre"]

    delai = duree_totale / len(voyelles)

    for v in voyelles:
        frames = globals.expressions.get(f"{v}", globals.expressions["neutre"])

        # Bouche ouverte
        if frames:
            globals.expression_actuelle = frames[1]
        time.sleep(delai / 2.3)

        # Bouche fermée
        if frames:
            globals.expression_actuelle = frames[0]
        time.sleep(delai / 2.3)
