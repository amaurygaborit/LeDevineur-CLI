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
    total_theorique = cli.calculer_total_combinaisons(structures, pool_donnees, len(separateurs))

    # --- 5. AFFICHAGE DU RÉSUMÉ ---
    if args.simulation or args.verbose:
        print("--- RÉSUMÉ AVANT GÉNÉRATION ---")
        cli.afficher_resume(args, total_theorique, len(structures))

    if args.simulation:
        return

    # --- 6. EXÉCUTION RÉELLE (OPTIMISÉE) ---
    if args.verbose:
        cli.afficher_barre_progression(0, total_theorique, time.time())
    
    compteur_ecrit = 0
    compteur_teste = 0
    start_time = time.time()
    
    # [OPTIMISATION 1] Le Set pour les doublons (Mémoire)
    deja_vus = set()
    
    # [OPTIMISATION 2] Le Buffer pour l'écriture (Vitesse)
    buffer_ecriture = []
    TAILLE_BUFFER = 100000  # On écrit par blocs de 100 000 lignes

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            for structure in structures:
                if not all(key in pool_donnees for key in structure):
                    continue

                listes_blocs = [pool_donnees[key] for key in structure]

                for combinaison in itertools.product(*listes_blocs):
                    for sep in separateurs:
                        mdp = sep.join(combinaison)
                        compteur_teste += 1
                        
                        # LOGIQUE ANTI-DOUBLON
                        if mdp not in deja_vus:
                            deja_vus.add(mdp)
                            
                            # [OPTIMISATION 3] Au lieu d'écrire tout de suite, on met dans le buffer
                            buffer_ecriture.append(mdp)
                            compteur_ecrit += 1

                            # Si le buffer est plein, on le vide dans le fichier d'un coup
                            if len(buffer_ecriture) >= TAILLE_BUFFER:
                                f.write("\n".join(buffer_ecriture) + "\n")
                                buffer_ecriture = []  # On vide le buffer

                        # Mise à jour barre de progression (fréquence réduite pour perf)
                        if args.verbose and compteur_teste % 10000 == 0:
                            cli.afficher_barre_progression(compteur_teste, total_theorique, start_time)
            
            # [OPTIMISATION 4] IMPORTANT : Écrire ce qui reste dans le buffer à la toute fin
            if buffer_ecriture:
                f.write("\n".join(buffer_ecriture) + "\n")

    except IOError as e:
        print(f"\n[ERREUR] Ecriture : {e}")
        return
    except MemoryError:
        print(f"\n[ERREUR FATALE] Trop de RAM utilisée ! Le fichier contient {compteur_ecrit} mdp.")
        return

    # Affichage final
    if args.verbose:
        cli.afficher_barre_progression(total_theorique, total_theorique, start_time)
        elapsed = time.time() - start_time
        print(f"\n\n--- TERMINÉ en {elapsed:.2f}s ---")
        
        doublons = compteur_teste - compteur_ecrit
        print(f"Statistiques :")
        print(f" - Mots de passe uniques écrits : {compteur_ecrit:_}".replace("_", " "))
        print(f" - Doublons évités             : {doublons:_}".replace("_", " "))

    else:
        total_str = f"{compteur_ecrit:_}".replace("_", " ")
        print(f"Terminé : {total_str} mdp générés (Doublons retirés).")


if __name__ == "__main__":
    main()