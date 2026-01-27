import argparse
import sys
import time

def configurer_arguments():
    """Configuration des arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Générateur de dictionnaire de mots de passe contextuel."
    )

    # I/O
    group_files = parser.add_argument_group('Fichiers')
    group_files.add_argument("-s", "--source", default="infos.json", help="Fichier source JSON")
    group_files.add_argument("-o", "--output", default="dictionnaire.txt", help="Fichier de sortie")
    group_files.add_argument("-p", "--patterns", default="patterns.txt", help="Fichier des patterns")
    group_files.add_argument("-f", "--format", choices=['txt'], default='txt', help="Format de sortie")

    # Options d'exécution
    group_ctrl = parser.add_argument_group('Contrôle')
    group_ctrl.add_argument("-v", "--verbose", action="store_true", help="Afficher la progression")
    group_ctrl.add_argument("-S", "--simulation", action="store_true", help="Simulation (pas d'écriture)")

    # Paramètres de complexité
    group_gen = parser.add_argument_group('Génération')
    group_gen.add_argument("--niveau-leet", type=int, choices=[1, 2], default=1, help="Niveau Leet Speak")
    group_gen.add_argument("--max-leet", type=int, default=3, help="Max substitutions par mot")
    group_gen.add_argument("--max-casse", type=int, default=3, help="Max variations de casse")

    return parser.parse_args()

def calculer_total_combinaisons(structures, pool_donnees, nb_separateurs):
    """Estimation mathématique du nombre total de combinaisons."""
    total = 0
    for structure in structures:
        # Vérifie si toutes les clés du pattern existent dans les données
        if not all(key in pool_donnees for key in structure):
            continue

        nb_combinaisons = 1
        for key in structure:
            nb_combinaisons *= len(pool_donnees[key])

        total += (nb_combinaisons * nb_separateurs)

    return total

def afficher_resume(args, total, nb_patterns):
    """Affiche le récapitulatif de configuration avant lancement."""
    print(f"[*] Config : Leet={args.niveau_leet}, MaxCasse={args.max_casse}")
    print(f"[*] Patterns : {nb_patterns}")
    print(f"[*] Volume estimé : {total:_}".replace("_", " "))
    print(f"[*] Sortie : {args.output}")
    print("-" * 40)

def afficher_barre_progression(actuel, total, start_time, taille_barre=30, unite="mdp"):
    """Barre de progression dynamique avec estimation du temps restant."""
    if total == 0: return

    pourcentage = (actuel / total) * 100
    rempli = int(taille_barre * actuel // total)
    barre = '█' * rempli + '-' * (taille_barre - rempli)

    # Calcul métriques temps
    elapsed = time.time() - start_time
    infos_sup = ""
    
    if elapsed > 0 and actuel > 0:
        vitesse = actuel / elapsed
        if vitesse > 0:
            restant = (total - actuel) / vitesse
            m, s = divmod(int(restant), 60)
            temps_str = f"{m}m {s}s"
            infos_sup = f"[{int(vitesse):_} {unite}/s | Reste: {temps_str}]".replace("_", " ")

    sys.stdout.write(f"\r[{barre}] {pourcentage:.1f}% ({actuel:_}/{total:_}) {infos_sup}".replace("_", " "))
    sys.stdout.flush()