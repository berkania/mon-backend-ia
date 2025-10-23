import imaplib
import email
from voice import parle, ecoute
from features import envoyer_mail
import globals

def lire_email_specifique(nom):
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('kiri22519@gmail.com', 'mmknoxmafvwctxwp')
        mail.select('inbox')
        adresse_recherche = globals.contacts.get(nom.lower(), nom)
        result, data = mail.search(None, f'(FROM "{adresse_recherche}")')
        email_ids = data[0].split()
        if email_ids:
            latest_email_id = email_ids[-1]
            result, msg_data = mail.fetch(latest_email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg['subject']
            body = msg.get_payload(decode=True).decode()  # Simplifié
            parle(f"Voici le mail de {nom}. Sujet : {subject}. Contenu : {body}")
            parle("Voulez-vous lui répondre ? (oui ou non)")
            reponse = ecoute()
            if "oui" in reponse:
                repondre_email(subject)
        else:
            parle(f"Aucun e-mail trouvé de {nom}.")
        mail.logout()
    except Exception as e:
        parle("Erreur lors de la lecture des e-mails.")

def repondre_email(sujet):
    parle("Quel est le contenu de votre réponse ?")
    corps = ecoute()
    parle(f"Vous avez dit : {corps}. Est-ce correct ? (oui ou non)")
    confirmation = ecoute()
    if "oui" in confirmation:
        # Assurez-vous d'avoir l'adresse ; c'est un exemple
        envoyer_mail("adresse@example.com", f"Re: {sujet}", corps)
    else:
        parle("D'accord, je ne vais pas envoyer le mail.")