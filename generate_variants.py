import itertools
from datetime import datetime

# --- 1. CONFIGURATION & DONNÉES ---

def get_leet_map(niveau):
    """
    Construit le dictionnaire de substitution en fusionnant les niveaux.
    Si on choisit niveau 2, on obtient : (Lettres Niv 1) + (Lettres Niv 2).
    """
    # Définition statique des caractères par niveau
    donnees_par_niveau = {
        # Niveau 1
        1: {
            'a': ['4'], 'e': ['3'], 'i': ['1'], 'o': ['0'],
            's': ['5'], 'b': ['8'], 'g': ['6'], 'z': ['2']
        },
        # Niveau 2
        2: {
            'a': ['@'], 's': ['$'], 'i': ['!'],
            't': ['7'], 'l': ['1'], 'g': ['9']
        },
        # Niveau 3
        3: {
            'a': ['^'], 'i': ['|'], 's': ['z'],
            'k': ['|<'], 'h': ['#'], 'v': ['\\/'], 'w': ['\\/\\/'],
            'c': ['('], 'd': ['|)']
        }
    }

    # On part de la base (Niveau 1)
    final_map = donnees_par_niveau[1].copy()

    # On boucle du niveau 2 jusqu'au niveau choisi pour accumuler les variantes
    for n in range(2, niveau + 1):
        if n in donnees_par_niveau:
            for char, variantes in donnees_par_niveau[n].items():
                if char in final_map:
                    # Si la lettre existe déjà (ex: 'a'), on ajoute le nouveau choix
                    final_map[char].extend(variantes)
                else:
                    # Si c'est une nouvelle lettre (ex: 't' au niv 2), on la crée
                    final_map[char] = variantes

    return final_map

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
    formats = ["%d/%m/%Y", "%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d"] 
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

# --- 2. MOTEURS DE GÉNÉRATION (Leet & Casse) ---

def appliquer_leet_speak(mots_base, config):
    """
    Génère des variantes Leet en gérant les CHOIX MULTIPLES.
    Utilise le produit cartésien pour tester toutes les combinaisons.
    """
    niveau = config.get("NIVEAU_LEET", 1)
    max_changes = config.get("MAX_LEET", 2)
    
    if max_changes == 0:
        return set(mots_base)

    leet_map = get_leet_map(niveau)
    resultats = set(mots_base) # On garde les originaux

    for mot in mots_base:
        if not mot: continue
        
        # Identifier les positions modifiables
        indices_possibles = [
            (i, c) for i, c in enumerate(mot.lower()) 
            if c in leet_map
        ]
        
        if not indices_possibles:
            continue

        limit = min(len(indices_possibles), max_changes)
        
        # Génération combinatoire
        for r in range(1, limit + 1):
            for combo_indices in itertools.combinations(indices_possibles, r):
                
                # Récupération des choix possibles pour chaque position
                # choices_per_pos = [['4', '@'], ['3'], ...]
                choices_per_pos = [leet_map[char_origin] for _, char_origin in combo_indices]
                
                # Produit cartésien des choix
                for substitution_combo in itertools.product(*choices_per_pos):
                    mot_liste = list(mot)
                    
                    # Application des substitutions
                    for i, (index_mot, _) in enumerate(combo_indices):
                        mot_liste[index_mot] = substitution_combo[i]
                    
                    resultats.add("".join(mot_liste))
                
    return resultats

def appliquer_casse_controllee(mots_base, config):
    """
    Génère des variantes de casse en respectant MAX_CASSE.
    """
    max_casse = config.get("MAX_CASSE", 3)
    resultats = set()

    for mot in mots_base:
        if not mot: continue
        
        # Bases
        resultats.add(mot)
        resultats.add(mot.lower())
        resultats.add(mot.upper())
        resultats.add(mot.title())

        if max_casse == 0:
            continue

        mot_lower = mot.lower()
        indices = list(range(len(mot_lower)))
        limit = min(len(mot_lower), max_casse)
        
        # Variations MiXEd cAsE
        for r in range(1, limit + 1):
            for indices_maj in itertools.combinations(indices, r):
                temp_list = list(mot_lower)
                for i in indices_maj:
                    temp_list[i] = temp_list[i].upper()
                resultats.add("".join(temp_list))
                
    return resultats

# --- ORCHESTRATEUR PRINCIPAL ---

def generer_toutes_variantes(valeur, config):
    """Pipeline complet (Structure -> Leet Multi-choix -> Casse)."""
    valeur_str = str(valeur)
    date_obj = parser_date(valeur_str)
    
    bases = set()

    # Bases (Texte ou Date)
    if not date_obj:
        bases.add(valeur_str)
    else:
        separateurs = config.get("SEPARATEURS_DATE", [""])
        j = f"{date_obj.day:02d}"
        a = str(date_obj.year)
        a_court = date_obj.strftime("%y")
        toutes_formes_mois = [f"{date_obj.month:02d}"] + obtenir_mois_texte(date_obj.month)

        bases.add(a)
        bases.add(a_court)

        for m_courant in toutes_formes_mois:
            structures_dates = [
                [j, m_courant, a], [j, m_courant, a_court],
                [a, m_courant, j], [a_court, m_courant, j],
                [j, m_courant], [m_courant, j]
            ]
            for structure in structures_dates:
                for sep in separateurs:
                    bases.add(sep.join(structure))

    # Leet Speak Multi-choix
    variantes_leet = appliquer_leet_speak(bases, config)
    
    # Casse
    resultats_finaux = appliquer_casse_controllee(variantes_leet, config)

    return list(resultats_finaux)