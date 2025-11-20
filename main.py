import data_loader
import enrich_data
import generate_variants
import generate_patterns
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
    
    # ÉTAPE 3 : Générer toutes les variantes pour chaque information
    infos_variantes = {}
    for cle, valeur in infos_enrichies.items():
        variantes_temp = set()
        
        # Important : s'assurer que la valeur est une string (car enrich_data peut renvoyer des ints convertis)
        valeur_str = str(valeur)

        # A. Ajout des variantes de casse classiques
        variantes_temp.update(generate_variants.generate_case_variants(valeur_str))

        # B. Leet speak
        variantes_temp.update(generate_variants.generate_leet_variants(valeur_str))

        # C. Gestion des dates/chiffres
        if not valeur_str.isalpha():
            variantes_temp.add(valeur_str)

        infos_variantes[cle] = list(variantes_temp)

    # ÉTAPE 4 : Définir les patterns
    patterns = generate_patterns.generer_patterns_basiques()

    # ÉTAPE 5 : Génération des mots de passe (Moteur de combinaison)
    mots_de_passe_probables = set()

    for pattern in patterns:
        # Récupération des clés du pattern
        cles_necessaires = [fn for _, fn, _, _ in formatter.parse(pattern) if fn is not None]
        
        # Vérification que toutes les clés existent dans nos données enrichies
        # Si une clé manque (ex: pas de Surnom dans le JSON), on ignore ce pattern
        if all(key in infos_variantes for key in cles_necessaires):
            listes_de_variantes = [infos_variantes[key] for key in cles_necessaires]
            
            # Produit cartésien
            for combinaison in generate_variants.itertools.product(*listes_de_variantes):
                valeurs_a_formater = dict(zip(cles_necessaires, combinaison))
                try:
                    mot_de_passe = pattern.format(**valeurs_a_formater)
                    mots_de_passe_probables.add(mot_de_passe)
                except KeyError:
                    pass # Sécurité

    # ÉTAPE 6 : Écriture fichier
    with open("dictionnaire.txt", "w") as f:
        for mdp in sorted(list(mots_de_passe_probables)):
            f.write(mdp + "\n")

    print(f"Succès : {len(mots_de_passe_probables)} mots de passe générés dans dictionnaire.txt")

if __name__ == "__main__":
    main()