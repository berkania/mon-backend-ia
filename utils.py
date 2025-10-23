import os
import pygame
import time
import globals

# Nettoyage fichiers audio anciens
def nettoyage_audio():
    for f in os.listdir():
        if f.startswith("reponse_") and f.endswith(".mp3"):
            try:
                os.remove(f)
            except Exception:
                pass

# Chargement images
def charger_images():
    dossier = "images"
    fichiers = os.listdir(dossier)
    data = {}
    for fichier in fichiers:
        if fichier.endswith(".png") and fichier.startswith("bouche_"):
            nom = fichier[7:-4]
            base = nom.replace("_fermé", "")
            if base not in data:
                data[base] = [None, None]
            if "_fermé" in nom:
                data[base][0] = pygame.image.load(os.path.join(dossier, fichier)).convert_alpha()
            else:
                data[base][1] = pygame.image.load(os.path.join(dossier, fichier)).convert_alpha()
    return data

def extraire_voyelles(text):
    return [c for c in text.lower() if c in "aeioué"]

def supprimer_fichier_audio(fichier, tentatives=5):
    for _ in range(tentatives):
        try:
            if os.path.exists(fichier):
                os.remove(fichier)
                return
        except PermissionError:
            time.sleep(0.5)

def ajouter_contact(nom, email):
    globals.contacts[nom.lower()] = email

def afficher_formulaire_pygame():
    from voice import parle  # Import ici pour éviter le cercle
    parle("Saisis le nom et l'e-mail de la personne à l'écran.")
    font = pygame.font.SysFont(None, 40)
    input_boxes = [pygame.Rect(250, 200, 300, 40), pygame.Rect(250, 270, 300, 40)]
    user_texts = ["", ""]
    active_box = 0
    done = False

    while not done:
        globals.screen.fill((50, 50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_TAB:
                    active_box = (active_box + 1) % 2
                elif event.key == pygame.K_BACKSPACE:
                    user_texts[active_box] = user_texts[active_box][:-1]
                else:
                    user_texts[active_box] += event.unicode

        for i in range(2):
            pygame.draw.rect(globals.screen, (200, 200, 200), input_boxes[i])
            txt_surface = font.render(user_texts[i], True, (0, 0, 0))
            globals.screen.blit(txt_surface, (input_boxes[i].x + 5, input_boxes[i].y + 5))

        pygame.display.flip()
        globals.clock.tick(30)

    ajouter_contact(user_texts[0], user_texts[1])