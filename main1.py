import pygame
import threading
import time
import random
import datetime
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
import imaplib
import email

# Imports des modules personnalisés
from utils import nettoyage_audio, charger_images, extraire_voyelles, supprimer_fichier_audio, ajouter_contact, afficher_formulaire_pygame
from voice import ecoute, parle, animer_avec_voyelles
from features import envoyer_mail, lire_actualites, meteo_ville, definir_mot, traduire, recherche_google, jouer_chanson
from games import jeu_quiz, jeu_calcul, jeu_pendu, jeux
from email_utils import lire_email_specifique, repondre_email
import globals

# Configurer Wikipedia en français
wikipedia.set_lang("fr")

# Nettoyage initial des fichiers audio temporaires
nettoyage_audio()

# Initialisation Pygame
pygame.init()
globals.screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("VTuber AYKIA 2D")
globals.clock = pygame.time.Clock()
pygame.mixer.init()

# Chargement des images d'expression
globals.expressions = charger_images()
globals.expression_actuelle = globals.expressions.get("smile", globals.expressions["neutre"])[1]

# Initialisation du traducteur Google Translate
translator = Translator()

def assistant():
    """Thread assistant vocal en écoute des commandes."""
    while True:
        cmd = ecoute()
        if not cmd:
            continue
        elif "bonjour" in cmd:
            parle("Bonjour !")
        elif "joue avec moi" in cmd:
            jeux()
        elif "envoie un mail" in cmd:
            parle("À qui voulez-vous envoyer le mail ?")
            nom = ecoute()
            email_dest = globals.contacts.get(nom.strip().lower())
            if email_dest:
                parle("Quel est le sujet du mail ?")
                sujet = ecoute()
                parle("Quel est le message ?")
                corps = ecoute()
                envoyer_mail(email_dest, sujet, corps)
            else:
                parle("Je ne connais pas cette personne.")
        # Ajoute ici d'autres commandes si besoin
        elif "stop" in cmd:
            parle("Au revoir !")
            break  # Arrête le thread assistant

# Démarrage du thread assistant vocal en arrière-plan
threading.Thread(target=assistant, daemon=True).start()

# Boucle principale Pygame pour affichage du personnage animé
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran avec un fond gris foncé
    globals.screen.fill((50, 50, 50))

    # Afficher l'expression actuelle du personnage au centre de la fenêtre
    if globals.expression_actuelle:
        rect = globals.expression_actuelle.get_rect(center=(400, 300))
        globals.screen.blit(globals.expression_actuelle, rect)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la boucle à 30 images par seconde
    globals.clock.tick(30)

# Quitter proprement Pygame
pygame.quit()
