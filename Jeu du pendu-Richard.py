import random
import unicodedata
import os

# Constante : nombre maximum de chances
CHANCES_MAX = 6

# Supprime les accents d'un mot (ex: é → e)
def supprimer_accents(texte):
    return ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')

# Charge les mots depuis un fichier texte (par défaut : mots_pendu.txt ou mots.txt si non trouvé)
def charger_mots(fichier="mots_pendu.txt"):
    try:
        with open(fichier, encoding="utf-8") as f:
            mots = [ligne.strip().lower() for ligne in f if ligne.strip()]
            return mots
    except FileNotFoundError:
        print(f"Fichier {fichier} introuvable. Utilisation du fichier par défaut.")
        return charger_mots("mots.txt")

# Choisit un mot aléatoire et retourne sa version sans accents
def choisir_mot(mots):
    mot = random.choice(mots)
    mot_sans_accents = supprimer_accents(mot)
    return mot, mot_sans_accents

# Affiche le mot deviné avec des "_" pour les lettres non trouvées
def afficher_mot(mot_sans_accents, lettres_trouvees):
    return ' '.join([lettre if lettre in lettres_trouvees else '_' for lettre in mot_sans_accents])

# Donne un indice : retourne une lettre qui NE figure PAS dans le mot
def donner_indice(mot_sans_accents, lettres_proposees):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    lettres_non_presentes = [l for l in alphabet if l not in mot_sans_accents and l not in lettres_proposees]
    return random.choice(lettres_non_presentes) if lettres_non_presentes else None

# Demande à l'utilisateur le chemin vers son propre fichier (ou utilise le fichier par défaut)
def demander_fichier():
    chemin = input("Entrez le chemin de votre fichier de mots (laisser vide pour défaut): ").strip()
    return chemin if chemin else "mots.txt"

    lettres_trouvees = set()       # Lettres correctes déjà devinées
# Fonction principale pour jouer une partie complète du pendu
def jouer_une_partie(mots):
    mot_original, mot_sans_accents = choisir_mot(mots)  # Choix du mot secret
    lettres_proposees = set()      # Lettres déjà proposées (correctes ou non)
    chances = CHANCES_MAX          # Compteur de chances restantes

    print("\n🎮 Bienvenue dans le jeu du Pendu 🎮")

    while chances > 0:
        # Affiche le mot actuel avec les lettres trouvées
        print("\nMot à deviner : ", afficher_mot(mot_sans_accents, lettres_trouvees))
        print(f"Chances restantes : {chances}")

        # Donne un indice s'il ne reste qu'une seule chance
        if chances == 1:
            indice = donner_indice(mot_sans_accents, lettres_proposees)
            if indice:
                print(f"💡 Indice : la lettre '{indice}' ne fait pas partie du mot.")

        # Demande à l'utilisateur de deviner une lettre
        lettre = input("Entrez une lettre : ").lower()
        lettre = supprimer_accents(lettre)  # Supprime les accents

        # Vérifie que l'entrée est une lettre valide
        if not lettre.isalpha() or len(lettre) != 1:
            print("Veuillez entrer une seule lettre valide.")
            continue

        # Vérifie si la lettre a déjà été proposée
        if lettre in lettres_proposees:
            print("Lettre déjà proposée.")
            continue

        lettres_proposees.add(lettre)  # Ajoute la lettre aux lettres déjà jouées

        if lettre in mot_sans_accents:
            lettres_trouvees.add(lettre)  # Bonne lettre !
            print("✅ Bien joué !")
        else:
            chances -= 1  # Mauvaise lettre, on perd une chance
            print("❌ Raté !")

        # Vérifie si toutes les lettres ont été trouvées (victoire)
        if all(l in lettres_trouvees for l in mot_sans_accents):
            print("\n🎉 Bravo ! Vous avez deviné le mot :", mot_original)
            break
    else:
        # Si la boucle se termine sans break, l'utilisateur a perdu
        print(f"\n💀 Vous avez perdu. Le mot était : {mot_original}")

# Boucle principale du jeu (possibilité de rejouer)
def boucle_jeu():
    fichier = demander_fichier()       # Demande le fichier ou prend celui par défaut
    mots = charger_mots(fichier)       # Charge les mots depuis le fichier

    while True:
        jouer_une_partie(mots)         # Lance une partie
        choix = input("\nVoulez-vous rejouer ? (o/n) : ").lower()
        if choix != 'o':
            print("Merci d'avoir joué. À bientôt !")
            break  # Sortie de la boucle si l'utilisateur ne veut pas rejouer

# Point d'entrée du programme
if __name__ == "__main__":
    boucle_jeu()
