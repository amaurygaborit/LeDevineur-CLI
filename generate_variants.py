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


def generate_leet_variants(mot, max_subs=3):
    """
    Génère toutes les variantes leet speak d'un mot en suivant la logique combinatoire.
    Inclut également les variantes de casse pour chaque lettre.
    """
    if not mot:
        return [""]

    # Dictionnaire de substitution (caractères minuscules vers variantes)
    leet_map = {
        'a': ['4', '@', '^'],
        'b': ['8'],
        'c': ['(', '<', '{'],
        'e': ['3', '&', '€'],
        'g': ['9', '6'],
        'h': ['#'],
        'i': ['1', '!', '|'],
        'l': ['1', '|', '!'],
        'o': ['0', '*'],
        's': ['5', '$', 'z'],
        't': ['7', '+'],
        'z': ['2', '%'],
        'x': ['*'],
        'y': ['j', '7']
    }

    # 1. On inclut toujours le mot original
    results = {mot}

    # 2. Identification des positions modifiables (où une variante existe)
    indices_modifiables = [i for i, char in enumerate(mot) if char.lower() in leet_map]

    # Si le mot est court (ex: "Paris"), on peut se permettre plus de substitutions
    # Si le mot est long ("Saintetienne"), on garde la limite stricte de 3
    limit_reelle = min(len(indices_modifiables), max_subs)

    # 3. Boucle sur le nombre de substitutions (de 1 à max_subs)
    # C'est ici que l'optimisation opère : on ne change que 'r' lettres à la fois
    for r in range(1, limit_reelle + 1):

        # On choisit QUELLES positions modifier (ex: positions 0 et 4)
        for indices_choisis in itertools.combinations(indices_modifiables, r):

            # On prépare les variantes UNIQUEMENT pour ces positions
            replacements_lists = []
            for idx in indices_choisis:
                char_original = mot[idx].lower()
                replacements_lists.append(leet_map[char_original])

            # Produit cartésien limité aux positions choisies (très rapide)
            for combo in itertools.product(*replacements_lists):
                mot_liste = list(mot)  # Copie modifiable
                for i, position_a_changer in enumerate(indices_choisis):
                    mot_liste[position_a_changer] = combo[i]

                results.add("".join(mot_liste))

    return list(results)