import itertools

def generate_case_variants(mot, max_bruteforce=5):
    """
    Génère les variantes de casse.
    - Mots courts (<= 14 chars) : Brute force intelligent (toutes combinaisons maj/min).
    - Mots longs (> 14 chars) : Variantes classiques uniquement pour la performance.
    """
    if not mot: return set()
    
    # 1. Variantes sémantiques de base (toujours incluses)
    variantes = {mot, mot.lower(), mot.upper(), mot.title(), mot.swapcase()}
    
    # 2. Brute force sur la casse pour les mots raisonnables
    # Limite à 12-14 chars car 2^14 = 16 384 combinaisons, ce qui reste gérable.
    if len(mot) <= max_bruteforce: 
        # Produit cartésien (ex: 'a' -> ['a', 'A'])
        options = [(c.lower(), c.upper()) if c.isalpha() else (c,) for c in mot]
        for combo in itertools.product(*options):
            variantes.add("".join(combo))
            
    return variantes

def generate_leet_variants(mot, niveau=1, max_subs=2):
    """
    Génère le Leet Speak avec contrôle de la complexité.
    
    Args:
        mot (str): Le mot à transformer.
        niveau (int): 1 = substitutions visuelles simples (e->3), 2 = symboles complexes (a->@).
        max_subs (int): Nombre maximum de caractères à changer dans le mot (ex: 2).
    """
    if not mot or mot.isdigit(): 
        return {mot}

    # --- NIVEAU 1 : Substitutions courantes (Chiffres) ---
    leet_map = {
        'a': ['4'], 
        'e': ['3'], 
        'i': ['1'], 
        'o': ['0'], 
        's': ['5'], 
        't': ['7'],
        'b': ['8'],
        'g': ['9', '6'],
        'z': ['2']
    }
    
    # --- NIVEAU 2 : Substitutions complexes (Symboles) ---
    if niveau > 1:
        leet_map['a'].extend(['@', '^'])
        leet_map['e'].extend(['&', '€'])
        leet_map['i'].extend(['!', '|', 'l'])
        leet_map['l'] = ['1', '|', '!']
        leet_map['s'].extend(['$', 'z', 'Z'])
        leet_map['t'].extend(['+'])
        leet_map['o'].extend(['*'])
        leet_map['c'] = ['(', '<', 'k']
        leet_map['k'] = ['c']
        leet_map['x'] = ['*']
        leet_map['y'] = ['j', '7']

    # On ne garde que les lettres présentes dans le mot qui ont une substitution
    indices = [i for i, c in enumerate(mot) if c.lower() in leet_map]
    
    if not indices:
        return {mot}

    variantes = {mot}
    
    # On limite le nombre de substitutions : on ne change pas plus de 'max_subs' lettres
    # Si le mot est très court (ex: "bob"), on peut tout changer. 
    limit_reelle = min(len(indices), max_subs)

    # Boucle de 1 à max_subs changements
    for r in range(1, limit_reelle + 1):
        # On choisit QUELLES positions modifier
        for locs in itertools.combinations(indices, r):
            options_list = []
            for i in locs:
                char_base = mot[i].lower()
                options_list.append(leet_map[char_base])
            
            # On applique les substitutions aux positions choisies
            for replacements in itertools.product(*options_list):
                temp_list = list(mot)
                for idx_tuple, char_remplacement in zip(enumerate(locs), replacements):
                    position_reelle = idx_tuple[1]
                    temp_list[position_reelle] = char_remplacement
                variantes.add("".join(temp_list))
                
    return variantes

def generer_toutes_variantes(valeur, niveau_leet=1, max_subs_leet=2, max_bruteforce=5):
    """
    Fonction Façade : Appelle les sous-fonctions avec les bons paramètres.
    """
    valeur_str = str(valeur)
    resultats = set()

    # 1. Base
    resultats.add(valeur_str)

    # 2. Pas de variantes sur les nombres purs (Années, Dept) pour éviter le bruit
    if valeur_str.isdigit():
        return list(resultats)

    # 3. Casse (Toujours actif)
    resultats.update(generate_case_variants(valeur_str, max_bruteforce))

    # 4. Leet Speak (Configurable)
    # On l'applique sur la version lowercase et Title pour avoir 'p1erre' et 'P1erre'
    bases_pour_leet = {valeur_str.lower(), valeur_str.title()}
    
    for base in bases_pour_leet:
        resultats.update(generate_leet_variants(base, niveau=niveau_leet, max_subs=max_subs_leet))

    return list(resultats)