"""
jeu_pendu.py
------------
Jeu du Pendu - Mini-projet MGA802
Auteur  : [Hamza Amri-Jouidel]
Date    : Mai 2026

Ce programme permet de jouer au jeu du pendu contre l'ordinateur.
Le mot secret est tiré aléatoirement depuis un fichier texte.
Les lettres accentuées (é, è, ê, à, â, û, etc.) sont normalisées
et traitées comme leur équivalent sans accent.

Utilisation :
    python jeu_pendu.py
    python jeu_pendu.py --fichier mon_fichier.txt
"""

import sys
import unicodedata
from module_lecture_mots import charger_mots, obtenir_chemin_fichier, choisir_mot


# ──────────────────────────────────────────────
#  Constantes
# ──────────────────────────────────────────────

CHANCES_INITIALES = 6

PENDU = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========""",
]


# ──────────────────────────────────────────────
#  Normalisation des lettres accentuées
# ──────────────────────────────────────────────

def normaliser(texte: str) -> str:
    """
    Supprime les accents d'une chaîne de caractères.

    Exemple : 'éléphant' → 'elephant'

    Args:
        texte: Chaîne originale pouvant contenir des accents.

    Returns:
        Chaîne sans accents, en minuscules.
    """
    nfkd = unicodedata.normalize("NFD", texte)
    sans_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sans_accents.lower()


# ──────────────────────────────────────────────
#  Affichage de l'état du jeu
# ──────────────────────────────────────────────

def afficher_etat(
    mot_normalise: str,
    lettres_trouvees: set[str],
    lettres_ratees: set[str],
    chances: int,
) -> None:
    """
    Affiche l'état courant du jeu : pendu, mot masqué, lettres ratées.

    Args:
        mot_normalise : Mot secret sans accents (en minuscules).
        lettres_trouvees: Ensemble des lettres correctement devinées.
        lettres_ratees  : Ensemble des lettres incorrectes proposées.
        chances         : Nombre de chances restantes.
    """
    # Dessin du pendu (index = nb d'erreurs commises)
    nb_erreurs = CHANCES_INITIALES - chances
    print(PENDU[nb_erreurs])

    # Mot avec les lettres trouvées révélées
    affichage_mot = " ".join(
        lettre if lettre in lettres_trouvees else "_"
        for lettre in mot_normalise
    )
    print(f"\n  Mot : {affichage_mot}")
    print(f"  Lettres incorrectes : {', '.join(sorted(lettres_ratees)) or '—'}")
    print(f"  Chances restantes   : {chances}\n")


# ──────────────────────────────────────────────
#  Saisie et validation d'une lettre
# ──────────────────────────────────────────────

def demander_lettre(lettres_deja_jouees: set[str]) -> str:
    """
    Demande à l'utilisateur de saisir une lettre valide et non déjà jouée.

    Args:
        lettres_deja_jouees: Ensemble des lettres déjà proposées.

    Returns:
        Une lettre minuscule sans accent, non encore jouée.
    """
    while True:
        saisie = input("  Entrez une lettre : ").strip()
        saisie_normalisee = normaliser(saisie)

        if len(saisie_normalisee) != 1 or not saisie_normalisee.isalpha():
            print("  ⚠  Veuillez entrer une seule lettre alphabétique.")
            continue

        if saisie_normalisee in lettres_deja_jouees:
            print(f"  ⚠  Vous avez déjà proposé la lettre « {saisie_normalisee} ».")
            continue

        return saisie_normalisee


# ──────────────────────────────────────────────
#  Indice (bonus)
# ──────────────────────────────────────────────

def donner_indice(mot_normalise: str, lettres_trouvees: set[str]) -> str:
    """
    Retourne une lettre du mot qui n'est PAS encore trouvée.

    Appelée uniquement quand il reste 1 chance à l'utilisateur (bonus).

    Args:
        mot_normalise   : Mot secret sans accents.
        lettres_trouvees: Lettres déjà devinées correctement.

    Returns:
        Une lettre indice (absente de lettres_trouvees), ou chaîne vide
        si toutes les lettres sont déjà trouvées.
    """
    lettres_restantes = [l for l in set(mot_normalise) if l not in lettres_trouvees]
    if lettres_restantes:
        import random
        return random.choice(lettres_restantes)
    return ""


# ──────────────────────────────────────────────
#  Vérification victoire / défaite
# ──────────────────────────────────────────────

def verifier_victoire(mot_normalise: str, lettres_trouvees: set[str]) -> bool:
    """
    Vérifie si toutes les lettres du mot ont été trouvées.

    Args:
        mot_normalise   : Mot secret sans accents.
        lettres_trouvees: Lettres correctement devinées.

    Returns:
        True si le joueur a gagné, False sinon.
    """
    return all(lettre in lettres_trouvees for lettre in mot_normalise)


# ──────────────────────────────────────────────
#  Boucle principale d'une partie
# ──────────────────────────────────────────────

def jouer_une_partie(mots: list[str]) -> None:
    """
    Gère le déroulement complet d'une partie du jeu du pendu.

    Args:
        mots: Liste de mots parmi lesquels choisir le mot secret.
    """
    # Sélection et normalisation du mot secret
    mot_original = choisir_mot(mots)
    mot_normalise = normaliser(mot_original)

    chances = CHANCES_INITIALES
    lettres_trouvees: set[str] = set()
    lettres_ratees: set[str] = set()
    indice_donne = False  # Garantit que l'indice n'est donné qu'une seule fois

    print("\n" + "=" * 40)
    print("  🎮  Jeu du Pendu  🎮")
    print("=" * 40)
    print(f"  Le mot à deviner contient {len(mot_normalise)} lettre(s).\n")

    # ── Boucle de jeu ──
    while chances > 0:
        afficher_etat(mot_normalise, lettres_trouvees, lettres_ratees, chances)

        # Bonus : indice quand il reste exactement 1 chance
        if chances == 1 and not indice_donne:
            indice = donner_indice(mot_normalise, lettres_trouvees)
            if indice:
                print(f"  💡 Indice : la lettre « {indice} » ne fait PAS partie du mot !")
                indice_donne = True

        # Saisie de la lettre
        lettre = demander_lettre(lettres_trouvees | lettres_ratees)

        # Traitement
        if lettre in mot_normalise:
            lettres_trouvees.add(lettre)
            print(f"\n  ✅  Bravo ! « {lettre} » est dans le mot.\n")
        else:
            lettres_ratees.add(lettre)
            chances -= 1
            print(f"\n  ❌  Raté ! « {lettre} » n'est pas dans le mot.\n")

        # Vérification victoire
        if verifier_victoire(mot_normalise, lettres_trouvees):
            afficher_etat(mot_normalise, lettres_trouvees, lettres_ratees, chances)
            print("  🎉  Félicitations, vous avez gagné !")
            print(f"  Le mot était : « {mot_original} »\n")
            return

    # Défaite
    afficher_etat(mot_normalise, lettres_trouvees, lettres_ratees, 0)
    print("  💀  Vous avez perdu !")
    print(f"  Le mot était : « {mot_original} »\n")


# ──────────────────────────────────────────────
#  Proposer de rejouer
# ──────────────────────────────────────────────

def demander_rejouer() -> bool:
    """
    Demande à l'utilisateur s'il souhaite jouer une nouvelle partie.

    Returns:
        True si l'utilisateur veut rejouer, False sinon.
    """
    while True:
        choix = input("  Voulez-vous rejouer ? (o/n) : ").strip().lower()
        if choix in ("o", "oui", "y", "yes"):
            return True
        if choix in ("n", "non", "no"):
            return False
        print("  ⚠  Veuillez répondre par « o » (oui) ou « n » (non).")


# ──────────────────────────────────────────────
#  Point d'entrée
# ──────────────────────────────────────────────

def main() -> None:
    """
    Point d'entrée du programme.

    Charge la liste de mots puis lance des parties en boucle jusqu'à
    ce que l'utilisateur décide de quitter.

    Usage :
        python jeu_pendu.py
        python jeu_pendu.py --fichier mon_fichier.txt
    """
    # Récupération du chemin de fichier (optionnel en argument CLI)
    chemin_utilisateur = ""
    if "--fichier" in sys.argv:
        idx = sys.argv.index("--fichier")
        if idx + 1 < len(sys.argv):
            chemin_utilisateur = sys.argv[idx + 1]

    chemin = obtenir_chemin_fichier(chemin_utilisateur)

    # Chargement des mots
    try:
        mots = charger_mots(chemin)
    except FileNotFoundError:
        print(f"  ❌  Fichier introuvable : {chemin}")
        print("  Placez 'mots_pendu.txt' dans le même dossier que le programme.")
        sys.exit(1)

    print(f"  📂  Fichier chargé : {chemin}  ({len(mots)} mots disponibles)")

    # Boucle de parties
    while True:
        jouer_une_partie(mots)
        if not demander_rejouer():
            print("\n  À bientôt ! 👋\n")
            break


if __name__ == "__main__":
    main()
