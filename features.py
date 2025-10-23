import pywhatkit
import re
import webbrowser
from googletrans import Translator
import wikipedia
import feedparser
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from voice import parle, ecoute  # AJOUTÉ : import de ecoute pour éviter l'erreur

# Configurer Wikipedia en français
wikipedia.set_lang("fr")

translator = Translator()

def envoyer_mail(destinataire, sujet, corps):
    expediteur = "kiri22519@gmail.com"
    mot_de_passe = "mmknoxmafvwctxwp"
    message = MIMEMultipart()
    message['From'] = expediteur
    message['To'] = destinataire
    message['Subject'] = sujet
    message.attach(MIMEText(corps, 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as serveur:
            serveur.starttls()
            serveur.login(expediteur, mot_de_passe)
            serveur.send_message(message)
            parle("Le mail a été envoyé.")
    except Exception as e:
        print("Erreur d'envoi :", e)
        parle("Erreur pendant l'envoi du mail.")

def lire_actualites():
    flux = feedparser.parse("https://www.francetvinfo.fr/titres.rss")
    titres = [entry.title for entry in flux.entries[:5]]
    if not titres:
        parle("Désolé, je n'ai trouvé aucune actualité.")
    else:
        for titre in titres:
            parle(titre)

def meteo_ville(ville):
    try:
        url = f"https://wttr.in/{ville}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "❌ Impossible de récupérer la météo."
    except Exception as e:
        return f"❌ Erreur : {e}"

def definir_mot(mot):
    try:
        resultat = wikipedia.summary(mot, sentences=2)
        print(f"Définition : {resultat}")
        parle(f"Voici la définition de {mot} : {resultat}")
    except wikipedia.exceptions.DisambiguationError as e:
        parle(f"Le mot {mot} est ambigu. Peux-tu être plus précis ?")
    except wikipedia.exceptions.PageError:
        parle(f"Je n'ai pas trouvé de définition pour {mot}.")
    except Exception as e:
        parle("Erreur lors de la recherche de la définition.")

def traduire():
    parle("Que veux-tu traduire ?")
    phrase = ecoute()
    if phrase:
        parle("Vers quelle langue ? (anglais, espagnol, portugais)")
        langue = ecoute()
        codes = {"anglais": "en", "espagnol": "es", "portugais": "pt"}
        dest = codes.get(langue)
        if not dest:
            parle("Langue non reconnue.")
            return
        trad = translator.translate(phrase, src="fr", dest=dest)
        parle(f"Traduction en {langue} : {trad.text}")
    else:
        parle("Je n'ai pas compris la phrase à traduire.")

def recherche_google():
    parle("Que veux-tu chercher sur Google ?")
    requete = ecoute()
    if requete:
        url = f"https://www.google.com/search?q={requete}"
        webbrowser.open(url)
        parle(f"Voici les résultats de ta recherche pour {requete}.")

def jouer_chanson():
    parle("Cette fonctionnalité de lecture de musique a été désactivée car Spotify n'est pas configuré.")

