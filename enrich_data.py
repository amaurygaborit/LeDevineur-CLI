import re
from datetime import datetime

def obtenir_mois_texte(mois_int):
    """Retourne une liste de variantes textuelles pour un mois donné."""
    mois_data = {
        1: ["janvier", "janv", "jan"],
        2: ["fevrier", "fev", "feb"],
        3: ["mars", "mar"],
        4: ["avril", "avr", "apr"],
        5: ["mai", "may"],
        6: ["juin", "jun"],
        7: ["juillet", "juil", "jul"],
        8: ["aout", "aug"],
        9: ["septembre", "sept", "sep"],
        10: ["octobre", "oct"],
        11: ["novembre", "nov"],
        12: ["decembre", "dec"]
    }
    return mois_data.get(int(mois_int), [])

def parser_date(date_str):
    """
    Essaie de convertir une chaîne en objet datetime.
    Supporte formats collés (25081992) et séparés (25/08/1992).
    """
    formats = [
        "%d%m%Y", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",  # Fr
        "%Y%m%d", "%Y-%m-%d", "%Y/%m/%d",              # ISO
        "%m%d%Y"                                       # US (parfois)
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def enrichir_donnees(infos):
    """
    Transforme les données brutes en composants atomiques.
    Ex: "25/08/1992" devient -> Jour="25", Mois="08", Annee="1992", AnneeCourt="92"
    """
    nouvelles_infos = infos.copy()
    
    for cle, valeur in infos.items():
        # 1. Traitement des Dates
        if "Date" in cle or (len(valeur) >= 6 and any(c.isdigit() for c in valeur)):
            date_obj = parser_date(valeur)
            
            if date_obj:
                # On enlève "Date" du nom pour avoir un préfixe propre (ex: Naissance, Mariage)
                prefixe = cle.replace("Date", "") 
                if prefixe == cle: prefixe = cle + "_" # Sécurité si le mot Date n'y était pas
                
                # Création des composants atomiques
                nouvelles_infos[f"{prefixe}Annee"] = str(date_obj.year)
                nouvelles_infos[f"{prefixe}AnneeCourt"] = date_obj.strftime("%y")
                nouvelles_infos[f"{prefixe}Mois"] = f"{date_obj.month:02d}"
                nouvelles_infos[f"{prefixe}Jour"] = f"{date_obj.day:02d}"
                
                # Variante textuelle du mois (on prend la 1ère version, souvent le nom complet)
                mois_txt = obtenir_mois_texte(date_obj.month)
                if mois_txt:
                    nouvelles_infos[f"{prefixe}MoisStr"] = mois_txt[0]

    # 2. Traitement des lieux (Code Postal -> Département)
    if "CodePostal" in infos and len(infos["CodePostal"]) >= 2:
        nouvelles_infos["Departement"] = infos["CodePostal"][:2]

    return nouvelles_infos