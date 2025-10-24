# Fichier principal : password_generator.py

import generer_variantes_casse

def main():
    # 1. Collecter les informations (on verra la ligne de commande plus tard)
    infos_perso = {
        "Nom": "Dupont",
        "Prenom": "Pierre",
        "AnneeNaissance": "1995",
        "Ville": "Paris",
        "CodePostalCourt": "75"
    }

    # 2. Générer toutes les variantes pour chaque information
    infos_variantes = {}
    for cle, valeur in infos_perso.items():
        infos_variantes[cle] = generer_variantes_casse.generer_variantes_casse(valeur)
        # On peut aussi ajouter la valeur brute (ex: 1995) si la casse n'a pas de sens
        if not valeur.isalpha():
            infos_variantes[cle].append(valeur)

    # 3. Définir les patterns (pour commencer, en dur dans une liste)
    patterns = [
        "{Nom}{Prenom}{AnneeNaissance}",
        "{Prenom}.{Nom}",
        "{Ville}{CodePostalCourt}!",
    ]

    # 4. Générer le dictionnaire de mots de passe
    mots_de_passe_probables = set()  # On utilise un set pour éviter les doublons

    for pattern in patterns:
        # Trouver les clés nécessaires pour ce pattern (ex: "Nom", "Prenom", "AnneeNaissance")
        cles_necessaires = [fn for _, fn, _, _ in formatter.parse(pattern) if fn is not None]

        # Créer toutes les combinaisons des variantes pour les clés nécessaires
        # Exemple: pour {Nom}{Prenom}, on combine chaque variante de Nom avec chaque variante de Prenom
        # Si la clé n'est pas trouvée, on utilise une liste contenant une chaîne vide [''] comme valeur par défaut
        listes_de_variantes = [infos_variantes.get(cle, ['']) for cle in cles_necessaires]

        for combinaison in generer_variantes_casse.itertools.product(*listes_de_variantes):
            # Créer un dictionnaire pour le formatage
            valeurs_a_formater = dict(zip(cles_necessaires, combinaison))
            mot_de_passe = pattern.format(**valeurs_a_formater)
            mots_de_passe_probables.add(mot_de_passe)

    # 5. Écrire le résultat dans un fichier
    with open("dictionnaire.txt", "w") as f:
        for mdp in sorted(list(mots_de_passe_probables)):
            f.write(mdp + "\n")

    print(f"{len(mots_de_passe_probables)} mots de passe générés dans dictionnaire.txt")


# Pour la mise en forme des patterns
from string import Formatter

formatter = Formatter()

if __name__ == "__main__":
    main()