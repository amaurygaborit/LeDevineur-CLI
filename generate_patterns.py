import os

def charger_structures_patterns(chemin_fichier="patterns.txt"):
    """Parse le fichier de patterns (format CSV simple)."""
    structures = []
    
    if not os.path.exists(chemin_fichier):
        print(f"[ERREUR] Pattern file '{chemin_fichier}' introuvable.")
        return []

    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne or ligne.startswith("#"):
                    continue
                
                # Parsing CSV : "Nom, Prenom" -> ['Nom', 'Prenom']
                structures.append([b.strip() for b in ligne.split(',')])
                
    except Exception as e:
        print(f"[ERREUR] Parsing patterns : {e}")

    return structures