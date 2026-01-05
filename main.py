import time
import itertools

import data_loader
import generate_variants
import generate_patterns
import cli

def main():
    # --- 1. CONFIGURATION ---
    args = cli.configurer_arguments()
    config = {
        "SEPARATEURS_PATTERN": ["", ".", "-", "_"],
        "SEPARATEURS_DATE": ["", "-"],
        "NIVEAU_LEET": args.niveau_leet,
        "MAX_LEET": args.max_leet,
        "MAX_CASSE": args.max_casse
    }

    if args.verbose:
        print(f"[*] Configuration chargée. Source: {args.source}")

    # --- 2. CHARGEMENT ---
    infos_brutes = data_loader.charger_infos_json(args.source)
    structures = generate_patterns.charger_structures_patterns(args.patterns)

    if not infos_brutes or not structures:
        print("[!] Erreur chargement fichiers.")
        return

    # --- 3. GÉNÉRATION POOL ---
    if args.verbose: print("--- Génération des variantes ---")
    pool_donnees = {}
    for cle, valeur in infos_brutes.items():
        pool_donnees[cle] = generate_variants.generer_toutes_variantes(valeur, config)

    # --- 4. CALCUL PRÉVISIONNEL ---
    separateurs = config["SEPARATEURS_PATTERN"]
    total_a_generer = cli.calculer_total_combinaisons(structures, pool_donnees, len(separateurs))

    # --- 5. AFFICHAGE DU RÉSUMÉ ---
    # On affiche le résumé si on est en Simulation OU en Verbose
    if args.simulation or args.verbose:
        print("--- RÉSUMÉ AVANT GÉNÉRATION ---")
        cli.afficher_resume(args, total_a_generer, len(structures))

    # SI SIMULATION : ON S'ARRÊTE LÀ
    if args.simulation:
        return

    # --- 6. EXÉCUTION RÉELLE ---
    if args.verbose:
        # On initialise la barre vide
        cli.afficher_barre_progression(0, total_a_generer, time.time())
    # --- 5. ÉCRITURE ---
    compteur_total = 0
    start_time = time.time()

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            for structure in structures:
                if not all(key in pool_donnees for key in structure):
                    continue

                listes_blocs = [pool_donnees[key] for key in structure]

                # Boucle de génération
                for combinaison in itertools.product(*listes_blocs):
                    for sep in separateurs:
                        mdp = sep.join(combinaison)
                        f.write(mdp + "\n")
                        compteur_total += 1

                        # Mise à jour barre de progression
                        if args.verbose and compteur_total % 5000 == 0:
                            cli.afficher_barre_progression(compteur_total, total_a_generer, start_time)

    except IOError as e:
        print(f"\n[ERREUR] Ecriture : {e}")
        return

# Affichage final
    if args.verbose:
        cli.afficher_barre_progression(total_a_generer, total_a_generer, start_time)
        elapsed = time.time() - start_time
        print(f"\n\n--- TERMINÉ en {elapsed:.2f}s ---")
    else:
        # Formatage du nombre final avec espaces
        total_str = f"{compteur_total:_}".replace("_", " ")
        print(f"Terminé : {total_str} mdp générés.")


if __name__ == "__main__":
    main()