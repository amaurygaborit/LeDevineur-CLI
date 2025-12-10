import data_loader
import enrich_data
import generate_variants
import generate_patterns
import itertools

# --- CONFIGURATION ---
CONFIG = {
    # Quels séparateurs tester entre les blocs ?
    "SEPARATEURS": ["", ".", "-", "_", "@"], 
    
    # Configuration des variantes
    "NIVEAU_LEET": 1,
    "MAX_SUBS_LEET": 2,
    "MAX_CASSE_BRUTEFORCE": 8
}

def construire_groupes_de_donnees(infos_enrichies, infos_brutes_keys):
    """
    Associe chaque clé enrichie à sa clé parente brute.
    Ex: Si la clé brute est 'DateNaissance', on veut associer :
        - La valeur brute '25/08/1992'
        - '1992' (NaissanceAnnee)
        - '92' (NaissanceAnneeCourt)
        - '25' (NaissanceJour)
    """
    groupes = {}

    # 1. On initialise les groupes avec les clés brutes du JSON
    for key in infos_brutes_keys:
        groupes[key] = set()

    # 2. On parcourt les infos enrichies pour les ranger
    for key_enrichie, valeur in infos_enrichies.items():
        # On essaie de trouver à quelle clé brute cela appartient
        # Ex: 'NaissanceAnnee' appartient à 'DateNaissance'
        # Ex: 'Prenom' appartient à 'Prenom'
        
        parent_trouve = None
        
        # Cas simple : c'est une clé brute directe (ex: 'Prenom')
        if key_enrichie in groupes:
            parent_trouve = key_enrichie
            
        # Cas dérivé : c'est une sous-clé (ex: 'NaissanceAnnee' vient de 'DateNaissance')
        else:
            # On cherche quel préfixe correspond
            # Astuce : enrich_data enlève 'Date' du nom. 
            # Donc 'DateNaissance' devient prefixe 'Naissance'
            for key_brute in groupes.keys():
                prefixe_attendu = key_brute.replace("Date", "")
                if key_enrichie.startswith(prefixe_attendu):
                    parent_trouve = key_brute
                    break
        
        # Si on a trouvé le parent, on génère les variantes et on ajoute
        if parent_trouve:
            variantes = generate_variants.generer_toutes_variantes(
                valeur, 
                niveau_leet=CONFIG["NIVEAU_LEET"], 
                max_subs_leet=CONFIG["MAX_SUBS_LEET"],
                max_bruteforce=CONFIG["MAX_CASSE_BRUTEFORCE"]
            )
            groupes[parent_trouve].update(variantes)

    # Conversion en listes pour itertools
    return {k: list(v) for k, v in groupes.items() if v}

def main():
    print("--- 1. Chargement ---")
    infos_brutes = data_loader.charger_infos_json("infos.json")
    if not infos_brutes: return

    print("--- 2. Enrichissement ---")
    infos_enrichies = enrich_data.enrichir_donnees(infos_brutes)
    
    print("--- 3. Groupement et Variantes ---")
    # C'est l'étape cruciale : on regroupe tout ce qui concerne "DateNaissance" ensemble
    # Dictionnaire : {'DateNaissance': ['1992', '92', 'nov', '25081992'...], 'Prenom': ['Pierre', 'P1erre']...}
    pool_donnees = construire_groupes_de_donnees(infos_enrichies, infos_brutes.keys())
    
    print("--- 4. Chargement des Structures ---")
    structures = generate_patterns.charger_structures_patterns("patterns.txt")
    print(f"   > {len(structures)} structures chargées.")

    print("--- 5. Génération Finale ---")
    mots_de_passe_finaux = set()
    separateurs = CONFIG["SEPARATEURS"]

    for structure in structures:
        # structure ressemble à ['Prenom', 'DateNaissance']
        
        # Vérification : est-ce qu'on a des données pour chaque élément demandé ?
        if all(element in pool_donnees for element in structure):
            
            # On récupère les listes de variantes pour chaque bloc
            # ex: listes_blocs = [ ['Pierre', 'pierre'], ['1992', '92', 'nov'] ]
            listes_blocs = [pool_donnees[element] for element in structure]
            
            # Produit cartésien des contenus (Pierre + 1992, Pierre + 92...)
            for combinaison in itertools.product(*listes_blocs):
                
                # Pour chaque combinaison de mots, on teste tous les séparateurs
                # On applique le MEME séparateur partout (souvent le cas) 
                # ou on pourrait faire plus complexe, mais restons simple :
                for sep in separateurs:
                    mdp = sep.join(combinaison)
                    mots_de_passe_finaux.add(mdp)

    # Écriture
    fichier_sortie = "dictionnaire.txt"
    with open(fichier_sortie, "w", encoding="utf-8") as f:
        for mdp in sorted(list(mots_de_passe_finaux)):
            f.write(mdp + "\n")

    print(f"[SUCCÈS] {len(mots_de_passe_finaux)} mots de passe générés dans {fichier_sortie}")

if __name__ == "__main__":
    main()