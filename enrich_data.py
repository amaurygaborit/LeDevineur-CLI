import re
from datetime import datetime

def obtenir_mois_texte(mois_int):
    """Retourne les versions texte d'un mois (français et anglais, court et long)."""
    mois_data = {
        1: ["janvier", "janv", "january", "jan"],
        2: ["fevrier", "fev", "february", "feb"],
        3: ["mars", "mar", "march"],
        4: ["avril", "avr", "april", "apr"],
        5: ["mai", "may"],
        6: ["juin", "jun", "june"],
        7: ["juillet", "juil", "july", "jul"],
        8: ["aout", "aug", "august"],
        9: ["septembre", "sept", "september", "sep"],
        10: ["octobre", "oct", "october"],
        11: ["novembre", "nov", "november"],
        12: ["decembre", "dec", "december"]
    }
    return mois_data.get(int(mois_int), [])

def parser_date(date_str):
    """
    Tente de comprendre une date (DDMMYYYY, DD/MM/YYYY, YYYY-MM-DD)
    et retourne un objet datetime ou None.
    """
    formats = [
        "%d%m%Y",      # 25081992
        "%d/%m/%Y",    # 25/08/1992
        "%d-%m-%Y",    # 25-08-1992
        "%Y-%m-%d",    # 1992-08-25
        "%d.%m.%Y"     # 25.08.1992
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def enrichir_donnees(infos):
    """
    Parcourt le dictionnaire d'infos et génère de nouvelles données 
    à partir des dates trouvées.
    """
    nouvelles_infos = infos.copy()
    
    # On parcourt toutes les clés (ex: DateNaissance, DateMariage, AnimalDate...)
    for cle, valeur in infos.items():
        # On ne traite que les clés contenant "Date" ou qui ressemblent à une année/date
        if "Date" in cle or (len(valeur) >= 4 and any(c.isdigit() for c in valeur)):
            
            date_obj = parser_date(valeur)
            
            if date_obj:
                base_key = cle.replace("Date", "") # Ex: DateNaissance -> Naissance
                
                # 1. Année (ex: 2004)
                nouvelles_infos[f"{base_key}Annee"] = str(date_obj.year)
                
                # 2. Année courte (ex: 04)
                nouvelles_infos[f"{base_key}AnneeCourt"] = date_obj.strftime("%y")
                
                # 3. Mois chiffre (ex: 11)
                nouvelles_infos[f"{base_key}Mois"] = f"{date_obj.month:02d}"
                
                # 4. Jour (ex: 13)
                nouvelles_infos[f"{base_key}Jour"] = f"{date_obj.day:02d}"
                
                # 5. Mois en toutes lettres (ex: novembre, nov)
                # On ajoute une liste de variantes pour le mois, qui sera traitée plus tard
                # Note : pour simplifier ici, on peut choisir d'ajouter juste le nom français
                variantes_mois = obtenir_mois_texte(date_obj.month)
                if variantes_mois:
                    nouvelles_infos[f"{base_key}MoisStr"] = variantes_mois[0] # ex: janvier

    # Autres enrichissements possibles (ex: Département depuis code postal)
    if "CodePostal" in infos and len(infos["CodePostal"]) >= 2:
        nouvelles_infos["Departement"] = infos["CodePostal"][:2]

    return nouvelles_infos