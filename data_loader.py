import json
import os

def charger_infos_json(chemin_fichier="infos.json"):
    """Charge et nettoie les données du fichier JSON source."""
    if not os.path.exists(chemin_fichier):
        print(f"ERREUR: Fichier '{chemin_fichier}' introuvable.")
        return {}

    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Conversion en string et suppression des métadonnées
            return {k: str(v) for k, v in data.items() if v and not k.startswith("__")}

    except json.JSONDecodeError as e:
        print(f"ERREUR: JSON invalide dans '{chemin_fichier}' : {e}")
        return {}
    except Exception as e:
        print(f"ERREUR: {e}")
        return {}