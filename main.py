import data_loader
import generate_variants
import generate_patterns
import itertools

# --- CONFIGURATION ---
CONFIG = {
    "SEPARATEURS_PATTERN": ["", ".", "-", "_"],
    "SEPARATEURS_DATE": ["", "-"],
    
    "NIVEAU_LEET": 1,  # 1 (a=4) ou 2 (s=5, t=7...)
    "MAX_LEET": 3,     # Max 3 caractères remplacés par mot
    "MAX_CASSE": 3     # Max 3 majuscules "aléatoires" par mot
}

def main():
    print("--- 1. Chargement des données ---")
    infos_brutes = data_loader.charger_infos_json("infos.json")
    if not infos_brutes: return

    print("--- 2. Génération du Pool de Variantes ---")
    # On pré-calcule toutes les variantes pour chaque champ une seule fois
    pool_donnees = {}
    for cle, valeur in infos_brutes.items():
        variantes = generate_variants.generer_toutes_variantes(valeur, CONFIG)
        pool_donnees[cle] = variantes
        
    print(f"   > Variantes prêtes pour {len(pool_donnees)} champs.")

    print("--- 3. Chargement des Patterns ---")
    structures = generate_patterns.charger_structures_patterns("patterns.txt")
    print(f"   > {len(structures)} patterns chargés.")

    print("--- 4. Génération et Écriture en Direct ---")
    fichier_sortie = "dictionnaire.txt"
    separateurs = CONFIG["SEPARATEURS_PATTERN"]
    compteur_total = 0

    # On ouvre le fichier UNE SEULE FOIS en mode écriture ("w") au début
    # Le fichier reste ouvert pendant toute la boucle
    try:
        with open(fichier_sortie, "w", encoding="utf-8") as f:
            
            for structure in structures:
                # structure = ['Prenom', 'DateNaissance'] par exemple
                
                # Vérification : est-ce que toutes les clés du pattern existent dans nos données ?
                if not all(key in pool_donnees for key in structure):
                    # Si une info manque (ex: Pas de nom d'animal), on saute ce pattern
                    continue
                
                # On récupère les listes de variantes pour chaque élément du pattern
                listes_blocs = [pool_donnees[key] for key in structure]
                
                # Produit cartésien (Toutes les combinaisons possibles)
                # Cette boucle génère les combinaisons une par une sans saturer la mémoire
                for combinaison in itertools.product(*listes_blocs):
                    for sep in separateurs:
                        # On assemble le mot de passe
                        mdp = sep.join(combinaison)
                        
                        # ÉCRITURE IMMÉDIATE
                        f.write(mdp + "\n")
                        compteur_total += 1
                        
                        # Petit affichage de progression tous les 100 000 mots de passe
                        if compteur_total % 100000 == 0:
                            print(f"   > {compteur_total} mots de passe générés...")

    except IOError as e:
        print(f"[ERREUR] Impossible d'écrire dans le fichier : {e}")

    print(f"--- TERMINÉ ---")
    print(f"Total généré : {compteur_total} mots de passe dans '{fichier_sortie}'")

if __name__ == "__main__":
    main()