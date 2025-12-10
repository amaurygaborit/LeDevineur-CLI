import os

def charger_structures_patterns(chemin_fichier="patterns.txt"):
    """
    Lit le fichier de patterns et retourne une liste de listes.
    Exemple entrée fichier : "Prenom, Nom"
    Exemple sortie : [['Prenom', 'Nom'], ...]
    """
    structures = []
    
    if not os.path.exists(chemin_fichier):
        print(f"[ERREUR] Le fichier {chemin_fichier} est introuvable.")
        return []

    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                # On ignore les commentaires et lignes vides
                if not ligne or ligne.startswith("#"):
                    continue
                
                # On découpe par la virgule et on nettoie les espaces
                # "Prenom, Nom" -> ['Prenom', 'Nom']
                blocs = [b.strip() for b in ligne.split(',')]
                structures.append(blocs)
                
    except Exception as e:
        print(f"[ERREUR] Lecture patterns : {e}")

    return structures