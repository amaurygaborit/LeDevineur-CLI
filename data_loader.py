import json
import os


def charger_infos_json(chemin_fichier="infos.json"):
    """
    Charge les informations personnelles depuis un fichier JSON.
    Retourne un dictionnaire.
    """
    if not os.path.exists(chemin_fichier):
        print(f"ERREUR: Le fichier '{chemin_fichier}' n'existe pas.")
        return {}

    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Nettoyage basique : on enlève les clés purement décoratives si besoin
            # et on s'assure que tout est converti en string pour éviter des erreurs plus tard
            clean_data = {k: str(v) for k, v in data.items() if v and not k.startswith("__")}
            return clean_data

    except json.JSONDecodeError as e:
        print(f"ERREUR: Problème de format dans '{chemin_fichier}' : {e}")
        return {}
    except Exception as e:
        print(f"ERREUR inattendue lors du chargement de '{chemin_fichier}' : {e}")
        return {}