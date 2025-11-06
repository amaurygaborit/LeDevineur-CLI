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
    """Génère des variantes leet speak d'un mot."""
    leet_map = {
        'a': ['a', '4', '@'],
        'e': ['e', '3'],
        'i': ['i', '1', '!'],
        'o': ['o', '0'],
        's': ['s', '5', '$'],
        't': ['t', '7'],
        'l': ['l', '1'],
        'g': ['g', '9'],
        'b': ['b', '8']
    }
    
    mot_lower = mot.lower()
    variantes = []
    
    # Pour chaque caractère, on prend soit le caractère original, soit ses remplacements leet
    options = []
    for char in mot_lower:
        if char in leet_map:
            options.append(leet_map[char])
        else:
            options.append([char])
    
    # Génère toutes les combinaisons (limité à 100 pour éviter l'explosion combinatoire)
    for combo in itertools.islice(itertools.product(*options), 100):
        variantes.append("".join(combo))
    
    return variantes