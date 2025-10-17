import itertools

def generer_variantes_casse(mot):
    """Génère toutes les variantes de casse pour un mot donné."""
    if not mot:
        return {""}
    # Crée toutes les combinaisons possibles de (char.lower(), char.upper())
    # Par exemple pour "nom": [('n', 'N'), ('o', 'O'), ('m', 'M')]
    # itertools.product va ensuite créer tous les chemins possibles : ('n','o','m'), ('n','o','M'), etc.
    variants = set()
    for combo in itertools.product(*zip(mot.lower(), mot.upper())):
        variants.add("".join(combo))
    return list(variants)

# Exemple d'utilisation
# print(generer_variantes_casse("Nom"))
# Output: ['nom', 'Nom', 'nOm', 'noM', 'NOm', 'nOM', 'NoM', 'NOM']