import random
from voice import parle, ecoute

def jeu_quiz():
    questions = {
        # ... (votre dictionnaire complet)
    }
    q, r = random.choice(list(questions.items()))
    parle(q)
    if ecoute() == r:
        parle("Bonne réponse !")
    else:
        parle(f"Mauvaise réponse. C'était {r}.")

def jeu_calcul():
    a, b = random.randint(1, 10), random.randint(1, 10)
    op = random.choice(['+', '-', '*'])
    exp = f"{a} {op} {b}"
    res = eval(exp)
    parle(f"Calcule : {a} {op} {b}")
    try:
        if int(ecoute()) == res:
            parle("Correct !")
        else:
            parle(f"Faux. C'était {res}.")
    except:
        parle("Je n'ai pas compris.")

def jeu_pendu():
    mots = [
        # ... (votre liste complète)
    ]
    mot = random.choice(mots)
    mot_cache = ["_" for _ in mot]
    essais = 6
    parle("Devine le mot, lettre par lettre. Tu as 6 essais.")
    while essais > 0 and "_" in mot_cache:
        parle("Le mot est : " + " ".join(mot_cache))
        lettre = ecoute()
        if lettre:
            lettre = lettre.strip().lower()
            if len(lettre) > 1:
                mots_dits = lettre.split()
                lettre = mots_dits[-1][0]
        if not lettre or len(lettre) != 1 or not lettre.isalpha():
            parle("Je n'ai pas compris une seule lettre. Réessaie.")
            continue
        if lettre in mot:
            for i, l in enumerate(mot):
                if l == lettre:
                    mot_cache[i] = lettre
            parle(f"Bonne lettre !")
        else:
            essais -= 1
            parle(f"Raté. Il te reste {essais} essais.")
    if "_" not in mot_cache:
        parle(f"Bravo ! Le mot était bien {mot}.")
    else:
        parle(f"Tu as perdu. Le mot était {mot}.")

def jeux():
    while True:
        parle("Quiz, calcul ou pendu ? Dis stop pour quitter.")
        choix = ecoute()
        if "quiz" in choix:
            jeu_quiz()
        elif "calcul" in choix:
            jeu_calcul()
        elif "mot mystère" in choix or "pendu" in choix:
            jeu_pendu()
        elif "stop" in choix:
            parle("Fin du jeu.")
            break
        else:
            parle("Je n'ai pas compris.")