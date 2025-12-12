import itertools
from datetime import datetime

# --- 1. CONFIGURATION & DONNÉES ---

def get_leet_map(niveau):
    """
    Retourne le dictionnaire de substitution selon le niveau.
    """
    # Niveau 1 : Substitutions visuelles évidentes et très courantes
    map_leet = {
        'a': '4',
        'e': '3',
        'i': '1',
        'o': '0'
    }
    
    # Niveau 2 : Substitutions "Gamer" / étendues
    if niveau >= 2:
        map_leet.update({
            's': '5',
            't': '7',
            'b': '8',
            'g': '6',
            'l': '1',
            'z': '2'
        })
        
    return map_leet

def obtenir_mois_texte(mois_int):
    """Retourne une liste de variantes textuelles pour un mois."""
    mois_data = {
        1: ["janvier", "janv", "jan"], 2: ["fevrier", "fev", "feb"],
        3: ["mars", "mar"], 4: ["avril", "avr", "apr"],
        5: ["mai", "may"], 6: ["juin", "jun"],
        7: ["juillet", "juil", "jul"], 8: ["aout", "aug"],
        9: ["septembre", "sept", "sep"], 10: ["octobre", "oct"],
        11: ["novembre", "nov"], 12: ["decembre", "dec"]
    }
    return mois_data.get(int(mois_int), [])

def parser_date(date_str):
    """Essaie de convertir une chaîne en objet datetime."""
    formats = ["%d/%m/%Y", "%Y", "%d-%m-%Y", "%d.%m.%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

# --- 2. MOTEURS DE GÉNÉRATION (Leet & Casse) ---

def appliquer_leet_speak(mots_base, config):
    """
    Génère des variantes Leet en respectant:
    - NIVEAU_LEET : Quels caractères on change.
    - MAX_LEET : Combien de caractères maximum on change dans un seul mot.
    """
    # Récupération config avec valeurs par défaut
    niveau = config.get("NIVEAU_LEET", 1)
    
    # On cherche "MAX_LEET", sinon on regarde "MAX_SUBS_LEET" (compatibilité), sinon 2 par défaut
    max_changes = config.get("MAX_LEET", config.get("MAX_SUBS_LEET", 2))
    
    if max_changes == 0:
        return set(mots_base)

    leet_map = get_leet_map(niveau)
    resultats = set(mots_base) # On garde toujours les originaux

    for mot in mots_base:
        if not mot: continue
        
        # Le Leet s'applique généralement sur des minuscules pour la correspondance
        mot_lower = mot.lower() 
        
        # 1. Identifier les index modifiables (ex: où sont les 'a', les 'e'...)
        indices_possibles = [
            (i, c) for i, c in enumerate(mot_lower) 
            if c in leet_map
        ]
        
        if not indices_possibles:
            continue

        # 2. On limite le nombre de changements à MAX_LEET
        limit = min(len(indices_possibles), max_changes)
        
        # 3. Génération combinatoire : de 1 changement jusqu'à 'limit' changements
        for r in range(1, limit + 1):
            for combo in itertools.combinations(indices_possibles, r):
                # combo est une liste de tuples (index, char_original)
                mot_liste = list(mot) # On repart du mot original (pour garder la casse d'origine si mixte)
                
                for index, char_original in combo:
                    # On remplace par le caractère Leet
                    mot_liste[index] = leet_map[char_original]
                
                resultats.add("".join(mot_liste))
                
    return resultats

def appliquer_casse_controllee(mots_base, config):
    """
    Génère des variantes de casse en respectant MAX_CASSE.
    Évite de générer 2^N variantes pour les mots longs.
    """
    # On cherche "MAX_CASSE", sinon "MAX_CASSE_BRUTEFORCE", sinon 3 par défaut
    max_casse = config.get("MAX_CASSE", config.get("MAX_CASSE_BRUTEFORCE", 3))
    
    resultats = set()

    for mot in mots_base:
        if not mot: continue
        
        # 1. Les bases incontournables (comptent pour 0 "coût" de calcul)
        resultats.add(mot)
        resultats.add(mot.lower())
        resultats.add(mot.upper())
        resultats.add(mot.title())

        if max_casse == 0:
            continue

        # 2. Variations fines (MiXEd cAsE)
        mot_lower = mot.lower()
        indices = list(range(len(mot_lower)))
        
        # On ne va pas changer plus de lettres que le mot n'en contient
        limit = min(len(mot_lower), max_casse)
        
        # On génère des variantes en mettant en majuscule 1 à N lettres
        for r in range(1, limit + 1):
            for indices_maj in itertools.combinations(indices, r):
                temp_list = list(mot_lower)
                for i in indices_maj:
                    temp_list[i] = temp_list[i].upper()
                resultats.add("".join(temp_list))
                
    return resultats

# --- 3. ORCHESTRATEUR PRINCIPAL ---

def generer_toutes_variantes(valeur, config):
    """
    Pipeline : 
    1. Structure (Date vs Texte)
    2. Leet Speak (Injection de chiffres/symboles)
    3. Casse (Variation Maj/Min sur le résultat du Leet)
    """
    valeur_str = str(valeur)
    date_obj = parser_date(valeur_str)
    
    bases = set()

    # ÉTAPE A : Génération des bases
    if not date_obj:
        # C'est du texte simple
        bases.add(valeur_str)
    else:
        # C'est une date -> structures
        separateurs = config.get("SEPARATEURS_DATE", [""])
        j = f"{date_obj.day:02d}"
        a = str(date_obj.year)
        a_court = date_obj.strftime("%y")
        # On mixe le mois chiffre ET les mois textes
        toutes_formes_mois = [f"{date_obj.month:02d}"] + obtenir_mois_texte(date_obj.month)

        for m_courant in toutes_formes_mois:
            structures_dates = [
                [j, m_courant, a],       # 25 08 1995
                [j, m_courant, a_court], # 25 08 95
                [a, m_courant, j],       # 1995 08 25
                [a_court, m_courant, j], # 95 08 25
                [j, m_courant],          # 25 08
                [m_courant, j],          # 08 25
            ]
            for structure in structures_dates:
                for sep in separateurs:
                    bases.add(sep.join(structure))

    # ÉTAPE B : Leet Speak (Contrôlé par NIVEAU_LEET et MAX_LEET)
    # Exemple : "Maison" -> "Ma1son", "M4ison"...
    variantes_leet = appliquer_leet_speak(bases, config)
    
    # ÉTAPE C : Casse (Contrôlé par MAX_CASSE)
    # Exemple : "Ma1son" -> "mA1son", "MA1SON"...
    resultats_finaux = appliquer_casse_controllee(variantes_leet, config)

    return list(resultats_finaux)