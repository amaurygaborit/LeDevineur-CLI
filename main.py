import time
import itertools
import os
import shutil

import data_loader
import generate_variants
import generate_patterns
import cli

# --- CONFIGURATION ---
NUM_PARTITIONS = 64
TEMP_DIR = "temp_mdp"
BUFFER_SIZE = 1024 * 1024 * 64  # 64 Mo Buffer pour I/O disque

def nettoyer_dossier_temp():
    """Reset de l'environnement de travail temporaire."""
    if os.path.exists(TEMP_DIR):
        try:
            shutil.rmtree(TEMP_DIR)
        except OSError:
            pass
    os.makedirs(TEMP_DIR, exist_ok=True)

def main():
    # 1. SETUP
    args = cli.configurer_arguments()
    config = {
        "SEPARATEURS_PATTERN": ["", ".", "-", "_"],
        "SEPARATEURS_DATE": ["", "-"],
        "NIVEAU_LEET": args.niveau_leet,
        "MAX_LEET": args.max_leet,
        "MAX_CASSE": args.max_casse
    }

    if args.verbose:
        print(f"[*] Chargement configuration. Source: {args.source}")

    # 2. DATA LOADING
    infos_brutes = data_loader.charger_infos_json(args.source)
    structures = generate_patterns.charger_structures_patterns(args.patterns)

    if not infos_brutes or not structures:
        print("[!] Echec chargement données.")
        return

    # 3. PRE-GENERATION (Pool de variantes en mémoire)
    pool_donnees = {}
    for cle, valeur in infos_brutes.items():
        pool_donnees[cle] = generate_variants.generer_toutes_variantes(valeur, config)

    # 4. ESTIMATION
    separateurs = config["SEPARATEURS_PATTERN"]
    total_theorique = cli.calculer_total_combinaisons(structures, pool_donnees, len(separateurs))

    if args.simulation:
        cli.afficher_resume(args, total_theorique, len(structures))
        return

    if args.verbose:
        cli.afficher_resume(args, total_theorique, len(structures))

    # --- PHASE 1 : SHARDING (Distribution) ---
    start_time = time.time()
    compteur_genere = 0
    nettoyer_dossier_temp()

    handles = []
    try:
        # Ouverture des fichiers partitions en mode Write
        for i in range(NUM_PARTITIONS):
            f = open(os.path.join(TEMP_DIR, f"part_{i}.txt"), "w", encoding="utf-8", buffering=BUFFER_SIZE)
            handles.append(f)
    except OSError as e:
        print(f"[ERREUR] Init partitions: {e}")
        return

    if args.verbose:
        print(f"[*] Phase 1 : Génération et Sharding...")
        cli.afficher_barre_progression(0, total_theorique, start_time)

    try:
        for structure in structures:
            if not all(key in pool_donnees for key in structure):
                continue
            
            # Produit cartésien des variantes
            listes_blocs = [pool_donnees[key] for key in structure]
            for combinaison in itertools.product(*listes_blocs):
                for sep in separateurs:
                    mdp = sep.join(combinaison)
                    compteur_genere += 1
                    
                    # Routing déterministe par hash : garantit le regroupement des doublons
                    bucket_id = hash(mdp) % NUM_PARTITIONS
                    handles[bucket_id].write(mdp + "\n")

                    if args.verbose and compteur_genere % 50000 == 0:
                        cli.afficher_barre_progression(compteur_genere, total_theorique, start_time)

    except KeyboardInterrupt:
        print("\n[!] Interruption utilisateur.")
        for h in handles: h.close()
        shutil.rmtree(TEMP_DIR)
        return
    finally:
        for h in handles: h.close()

    if args.verbose:
        cli.afficher_barre_progression(total_theorique, total_theorique, start_time)
        print(f"\n[*] Phase 2 : Fusion et Déduplication...")

    # --- PHASE 2 : MERGE & DEDUPE ---
    compteur_unique = 0
    start_time_phase2 = time.time()
    
    try:
        with open(args.output, "w", encoding="utf-8", buffering=BUFFER_SIZE) as f_out:
            for i in range(NUM_PARTITIONS):
                part_path = os.path.join(TEMP_DIR, f"part_{i}.txt")
                
                try:
                    # Skip fichiers vides pour gagner du temps
                    if os.path.getsize(part_path) == 0:
                        if args.verbose:
                            cli.afficher_barre_progression(i + 1, NUM_PARTITIONS, start_time_phase2, unite="files")
                        continue
                except OSError:
                    continue
                
                # Chargement partition -> Set (Dedupe auto) -> Write Bulk
                with open(part_path, "r", encoding="utf-8") as f_in:
                    lignes_uniques = set(f_in)
                
                f_out.writelines(lignes_uniques)
                compteur_unique += len(lignes_uniques)
                
                del lignes_uniques

                if args.verbose:
                    cli.afficher_barre_progression(i + 1, NUM_PARTITIONS, start_time_phase2, unite="files")

    except IOError as e:
        print(f"[ERREUR] I/O Final : {e}")
    finally:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)

    # --- FINAL REPORT ---
    elapsed = time.time() - start_time
    if args.verbose:
        print(f"\n\n--- TERMINÉ ({elapsed:.2f}s) ---")
        print(f"Brut     : {compteur_genere:_}".replace("_", " "))
        print(f"Uniques  : {compteur_unique:_}".replace("_", " "))
        print(f"Doublons : {(compteur_genere - compteur_unique):_}".replace("_", " "))
    else:
        print(f"Terminé : {compteur_unique} mdp générés.")

if __name__ == "__main__":
    main()