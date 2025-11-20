import itertools

def generate_case_variants(mot):
    """Génère toutes les variantes de casse pour un mot donné."""
    if not mot:
        return {""}
    # Crée toutes les combinaisons possibles de (char.lower(), char.upper())
    # Par exemple pour "nom": [('n', 'N'), ('o', 'O'), ('m', 'M')]
    # itertools.product va ensuite créer tous les chemins possibles : ('n','o','m'), ('n','o','M'), etc.
    variants = set()
    for combo in itertools.product(*zip(mot.lower(), mot.upper())):
        variants.add("".join(combo))
    return list(variants)

def generate_year_variants(annee):
    """Génère des variantes d'une année (complète, 2 chiffres, etc.)."""
    variantes = [annee]
    if len(annee) == 4:
        variantes.append(annee[2:])  # Deux derniers chiffres
    return variantes


def generate_leet_variants(mot):
    """
    Génère toutes les variantes leet speak d'un mot en suivant la logique combinatoire.
    Inclut également les variantes de casse pour chaque lettre.
    """
    if not mot:
        return [""]

    # Dictionnaire de substitution (caractères minuscules vers variantes)
    leet_map = {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7'],
        'l': ['1'],
        'g': ['9'],
        'b': ['8']
    }

    # Liste qui contiendra les possibilités pour chaque position de caractère
    options_par_position = []

    for char in mot:
        # 1. On part de la base : le caractère en minuscule et en majuscule
        # On utilise un set pour dédoublonner automatiquement (ex: si char est '1', lower et upper sont pareils)
        possibilites = {char, char.lower(), char.upper()}

        # 2. Si une substitution leet existe pour ce caractère (en minuscule), on l'ajoute
        if char.lower() in leet_map:
            possibilites.update(leet_map[char.lower()])

        options_par_position.append(list(possibilites))

    # 3. Génération du produit cartésien (toutes les combinaisons possibles)
    # C'est exactement la même logique que generate_case_variants
    variants = set()
    for combo in itertools.product(*options_par_position):
        variants.add("".join(combo))

    return list(variants)