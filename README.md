# Jeu du Pendu - MGA802

Auteur : Hamza Amri-Jouidel
Date : Mai 2026

## Description
Jeu du pendu en Python contre l'ordinateur.
Le mot est tiré aléatoirement depuis un fichier texte.
Les lettres accentuées sont normalisées.Le joueur dispose de 6 chances
pour deviner le mot lettre par lettre

## Structure du projet
jeu_pendu/

jeu_pendu.py #Script principal (point d'entrée)

module_lecture_mots.py # Module utilitaire : chargement et sélection des mots

mots_pendu.txt # Fichier de mots par défaut (fourni sur Moodle)

README.md # Ce fichier

## Fonctionnalités
Sélection aléatoire d’un mot depuis mots_pendu.txt (ou un fichier personnalisé)

Affichage du pendu ASCII mis à jour à chaque erreur

Affichage du mot masqué ( _ _ _ ) avec révélation progressive

Suivi des lettres correctes et incorrectes

Gestion des lettres accentuées : é , è , ê , à , â , û … traitées comme e , a , u …

Détection de la victoire et de la défaite avec message clair

Proposition de rejouer ou de quitter après chaque partie

Bonus : quand il reste 1 chance, un indice est donné (une lettre absente du mot)

## Règles du jeu
Le joueur dispose de 6 erreurs maximum avant la pendaison.

Seules les lettres alphabétiques sont acceptées.

Une lettre déjà jouée ne peut pas être rejouée.

Les accents sont ignorés : taper e trouve aussi les é , è , ê .