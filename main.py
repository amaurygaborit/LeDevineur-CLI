import generate_variants
import data_loader
import enrich_data
from string import Formatter

formatter = Formatter()

def main():
    print("--- Début de la génération ---")

    # ÉTAPE 1 : Charger les données brutes
    infos_perso = data_loader.charger_infos_json("infos.json")
    if not infos_perso:
        return

    # ÉTAPE 2 : Enrichir les données (Générer 04 depuis 2004, Nov depuis 11, etc.)
    infos_enrichies = enrich_data.enrichir_donnees(infos_perso)
    
    print(f"Données enrichies : {len(infos_perso)} champs -> {len(infos_enrichies)} champs.")
    
    # 2. Générer toutes les variantes pour chaque information
    infos_variantes = {}
    for cle, valeur in infos_perso.items():
        # Génère les variantes de casse (ex: marie, Marie, MARIE)
        infos_variantes[cle] = generate_variants.generate_case_variants(valeur)
        # Ajoute la version brute si elle contient des chiffres/symboles (ex: dates, tél)
        if not valeur.isalpha():
             infos_variantes[cle].append(valeur)

    # 3. Définir les patterns (pour commencer, en dur dans une liste)
    patterns = [
        "{Nom}{Prenom}{AnneeNaissance}",
        "{Prenom}.{Nom}",
        "{Ville}{CodePostalCourt}!",
        "{Prenom}{Nom}",
        "{Nom}{Prenom}",
        "{Nom}.{Prenom}",
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

        for combinaison in generate_variants.itertools.product(*listes_de_variantes):
            # Créer un dictionnaire pour le formatage
            valeurs_a_formater = dict(zip(cles_necessaires, combinaison))
            mot_de_passe = pattern.format(**valeurs_a_formater)
            mots_de_passe_probables.add(mot_de_passe)

    # 5. Écrire le résultat dans un fichier
    with open("dictionnaire.txt", "w") as f:
        for mdp in list(mots_de_passe_probables):
            f.write(mdp + "\n")

    print(f"{len(mots_de_passe_probables)} mots de passe générés dans dictionnaire.txt")


# Pour la mise en forme des patterns
from string import Formatter

formatter = Formatter()

if __name__ == "__main__":
    main()