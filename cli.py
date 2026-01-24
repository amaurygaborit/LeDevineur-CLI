import argparse
import sys
import time

def configurer_arguments():
    """
    Gère toute la configuration de argparse.
    Retourne l'objet args contenant les paramètres choisis par l'utilisateur.
    """
    parser = argparse.ArgumentParser(
        description="Générateur de dictionnaire de mots de passe contextuel."
    )

    # --- Fichiers ---
    group_files = parser.add_argument_group('Fichiers')
    group_files.add_argument("-s", "--source", default="infos.json",
                             help="Chemin du fichier source JSON (Défaut: infos.json)")
    group_files.add_argument("-o", "--output", default="dictionnaire.txt",
                             help="Chemin du fichier de sortie (Défaut: dictionnaire.txt)")
    group_files.add_argument("-p", "--patterns", default="patterns.txt",
                             help="Chemin du fichier de structures (Défaut: patterns.txt)")
    group_files.add_argument("-f", "--format", choices=['txt'], default='txt',
                             help="Format du fichier de sortie (Défaut: txt)")

    # --- Contrôle ---
    group_ctrl = parser.add_argument_group('Contrôle')
    group_ctrl.add_argument("-v", "--verbose", action="store_true",
                            help="Mode verbeux : Affiche la progression en temps réel")

    # Simulation
    group_ctrl.add_argument("-S","--simulation", action="store_true",
                            help="Affiche le nombre total de mdp sans créer le fichier.")

    # --- Génération ---
    group_gen = parser.add_argument_group('Paramètres de Génération')
    group_gen.add_argument("--niveau-leet", type=int, choices=[1, 2], default=1,
                           help="Niveau de Leet Speak (1=Basique, 2=Avancé). Défaut: 1")
    group_gen.add_argument("--max-leet", type=int, default=3,
                           help="Max substitutions de caractères par mot. Défaut: 3")
    group_gen.add_argument("--max-casse", type=int, default=3,
                           help="Max variations majuscules aléatoires. Défaut: 3")

    return parser.parse_args()

def calculer_total_combinaisons(structures, pool_donnees, nb_separateurs):
    """
    Calcule mathématiquement le nombre de mots de passe qui seront générés.
    """
    total = 0
    for structure in structures:
        if not all(key in pool_donnees for key in structure):
            continue

        nb_combinaisons_pattern = 1
        for key in structure:
            nb_combinaisons_pattern *= len(pool_donnees[key])

        total += (nb_combinaisons_pattern * nb_separateurs)

    return total


def afficher_resume(args, total, nb_patterns):
    """
    Affiche le bloc d'informations (utilisé pour Simulation ET Verbose).
    """
    total_str = f"{total:_}".replace("_", " ")

    print(f"[*] Configuration : Leet={args.niveau_leet}, MaxCasse={args.max_casse}")
    print(f"[*] Patterns chargés : {nb_patterns}")
    print(f"[*] Mots de passe à générer : {total_str}")
    print(f"[*] Fichier de sortie : {args.output}")
    print("------------------------------------------------")


def afficher_barre_progression(actuel, total, start_time, taille_barre=30, unite="mdp"):
    """
    Affiche la barre de chargement avec vitesse et temps restant.
    [NOUVEAU] Le paramètre 'unite' permet de changer l'affichage (ex: 'fichiers' au lieu de 'mdp')
    """
    if total == 0: return

    pourcentage = (actuel / total) * 100
    rempli = int(taille_barre * actuel // total)
    barre = '█' * rempli + '-' * (taille_barre - rempli)

    elapsed = time.time() - start_time
    infos_sup = ""

    if elapsed > 0 and actuel > 0:
        vitesse = actuel / elapsed
        if vitesse > 0:
            restant = (total - actuel) / vitesse
            m, s = divmod(int(restant), 60)
            temps_str = f"{m}m {s}s"
        else:
            temps_str = "?"

        # On formate aussi la vitesse 
        vitesse_str = f"{int(vitesse):_}".replace("_", " ")
        infos_sup = f"[{vitesse_str} {unite}/s | Reste: {temps_str}]"

    # On formate le compteur actuel et total (ex: 1 500 / 3 000)
    actuel_str = f"{actuel:_}".replace("_", " ")
    total_str = f"{total:_}".replace("_", " ")

    sys.stdout.write(f"\r[{barre}] {pourcentage:.1f}% ({actuel_str}/{total_str}) {infos_sup}")
    sys.stdout.flush()