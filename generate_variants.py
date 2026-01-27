import itertools
from datetime import datetime

# --- 1. HELPERS & DATA ---

def get_leet_map(niveau):
    """Retourne la table de substitution selon le niveau de complexité."""
    map_leet = {'a': '4', 'e': '3', 'i': '1', 'o': '0'}
    
    if niveau >= 2:
        map_leet.update({'s': '5', 't': '7', 'b': '8', 'g': '6', 'l': '1', 'z': '2'})
        
    return map_leet

def obtenir_mois_texte(mois_int):
    """Variantes textuelles (fr/en/abbr) pour un mois donné."""
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
    """Tente de parser la chaîne date selon plusieurs formats standards."""
    formats = ["%d/%m/%Y", "%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d"] 
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

# --- 2. LOGIQUE DE TRANSFORMATION ---

def appliquer_leet_speak(mots_base, config):
    """Génère les variations Leet Speak par combinatoire."""
    niveau = config.get("NIVEAU_LEET", 1)
    max_changes = config.get("MAX_LEET", 2)
    
    if max_changes == 0:
        return set(mots_base)

    leet_map = get_leet_map(niveau)
    resultats = set(mots_base)

    for mot in mots_base:
        if not mot: continue
        
        # Identification des positions substituables
        indices_possibles = [(i, c) for i, c in enumerate(mot.lower()) if c in leet_map]
        if not indices_possibles:
            continue

        limit = min(len(indices_possibles), max_changes)
        
        # Génération des combinaisons de substitutions
        for r in range(1, limit + 1):
            for combo in itertools.combinations(indices_possibles, r):
                mot_liste = list(mot)
                for index, char_original in combo:
                    mot_liste[index] = leet_map[char_original]
                resultats.add("".join(mot_liste))
                
    return resultats

def appliquer_casse_controllee(mots_base, config):
    """Génère les variations de casse (Upper, Lower, Title, Mixed)."""
    max_casse = config.get("MAX_CASSE", 3)
    resultats = set()

    for mot in mots_base:
        if not mot: continue
        
        # Variations standard (coût nul)
        resultats.update({mot, mot.lower(), mot.upper(), mot.title()})

        if max_casse == 0:
            continue

        # Variations Mixed-Case par combinatoire
        mot_lower = mot.lower()
        indices = list(range(len(mot_lower)))
        limit = min(len(mot_lower), max_casse)
        
        for r in range(1, limit + 1):
            for indices_maj in itertools.combinations(indices, r):
                temp = list(mot_lower)
                for i in indices_maj:
                    temp[i] = temp[i].upper()
                resultats.add("".join(temp))
                
    return resultats

# --- 3. ENTRY POINT ---

def generer_toutes_variantes(valeur, config):
    """Pipeline de génération : Parsing -> Formats Dates -> Leet -> Casse."""
    valeur_str = str(valeur)
    date_obj = parser_date(valeur_str)
    
    bases = set()

    # Gestion spécifique des dates ou texte simple
    if not date_obj:
        bases.add(valeur_str)
    else:
        # Génération des formats de date (DDMMYYYY, YYMMDD, etc.)
        separateurs = config.get("SEPARATEURS_DATE", [""])
        j, m, a = f"{date_obj.day:02d}", f"{date_obj.month:02d}", str(date_obj.year)
        a_court = date_obj.strftime("%y")
        mois_textes = [m] + obtenir_mois_texte(date_obj.month)

        bases.update({a, a_court}) # Années seules

        for m_txt in mois_textes:
            formats = [
                [j, m_txt, a], [j, m_txt, a_court],
                [a, m_txt, j], [a_court, m_txt, j],
                [j, m_txt], [m_txt, j]
            ]
            for fmt in formats:
                for sep in separateurs:
                    bases.add(sep.join(fmt))

    # Application des transformations
    variantes_leet = appliquer_leet_speak(bases, config)
    final = appliquer_casse_controllee(variantes_leet, config)

    return list(final)