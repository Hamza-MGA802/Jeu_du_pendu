"""
module_lecture_mots.py
----------------------
Module utilitaire pour le jeu du pendu (MGA802).
Fournit les fonctions de chargement et de sélection de mots.
"""

import random
import os


def charger_mots(chemin_fichier: str) -> list[str]:
    """
    Charge la liste de mots depuis un fichier texte (un mot par ligne).

    Args:
        chemin_fichier: Chemin vers le fichier .txt contenant les mots.

    Returns:
        Liste de mots (chaînes de caractères).

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
    """
    with open(chemin_fichier, encoding="utf-8") as f:
        mots = [ligne.strip() for ligne in f if ligne.strip()]
    return mots


def obtenir_chemin_fichier(chemin_utilisateur: str = "") -> str:
    """
    Retourne le chemin du fichier de mots à utiliser.

    Si l'utilisateur fournit un chemin valide, il est utilisé.
    Sinon, le fichier par défaut 'mots_pendu.txt' (même répertoire
    que ce module) est sélectionné.

    Args:
        chemin_utilisateur: Chemin fourni par l'utilisateur (peut être vide).

    Returns:
        Chemin vers le fichier de mots à utiliser.
    """
    if chemin_utilisateur and os.path.isfile(chemin_utilisateur):
        return chemin_utilisateur

    chemin_defaut = os.path.join(os.path.dirname(__file__), "mots_pendu.txt")
    return chemin_defaut


def choisir_mot(mots: list[str]) -> str:
    """
    Sélectionne un mot aléatoire dans la liste fournie.

    Args:
        mots: Liste de mots disponibles.

    Returns:
        Un mot choisi aléatoirement.
    """
    return random.choice(mots)
