import itertools

def combiner_et_permuter(elements, separateurs=[""]):
    """
    Génère toutes les permutations possibles d'une liste d'éléments
    avec différents séparateurs.
    
    Ex: elements=["{Nom}", "{Prenom}"], separateurs=["", "."]
    -> "{Nom}{Prenom}", "{Prenom}{Nom}", "{Nom}.{Prenom}", "{Prenom}.{Nom}"
    """
    resultats = []
    # On génère les permutations (l'ordre change : A+B, B+A)
    for perm in itertools.permutations(elements):
        # Pour chaque ordre, on teste tous les séparateurs demandés
        for sep in separateurs:
            pattern = sep.join(perm)
            resultats.append(pattern)
    return resultats

def generer_patterns_basiques():
    """Retourne une liste de patterns générée dynamiquement."""
    patterns = []

    # 1. Identité seule (Permutations de Nom et Prénom)
    # Génère : PierreDupont, DupontPierre, Pierre.Dupont, Dupont.Pierre, etc.
    patterns.extend(combiner_et_permuter(
        elements=["{Prenom}", "{Nom}"], 
        separateurs=["", ".", "-", "_"]
    ))
    
    # 2. Identité + Année (Ex: PierreDupont1992, 1992DupontPierre...)
    bases_identite = combiner_et_permuter(["{Prenom}", "{Nom}"], separateurs=["", ".", "-"])
    
    for base in bases_identite:
        # On ajoute l'année à la fin (très courant)
        patterns.append(f"{base}{{AnneeNaissance}}")
        patterns.append(f"{base}{{AnneeNaissanceCourt}}") # Ex: PierreDupont04
        patterns.append(f"{base}{{Departement}}")         # Ex: PierreDupont69
        
        # On ajoute l'année au début (moins courant mais existe)
        patterns.append(f"{{AnneeNaissance}}{base}")

    # 3. Identité + Ville (Ex: PierreLyon, LyonPierre...)
    patterns.extend(combiner_et_permuter(
        elements=["{Prenom}", "{VilleHabitation}"],
        separateurs=[""]
    ))
    patterns.extend(combiner_et_permuter(
        elements=["{Nom}", "{VilleHabitation}"],
        separateurs=[""]
    ))

    # 4. Dates complètes (On permute Jour/Mois/Année)
    # Génère : 13111992, 19921113, 11131992...
    patterns.extend(combiner_et_permuter(
        elements=["{NaissanceJour}", "{NaissanceMois}", "{NaissanceAnnee}"],
        separateurs=["", "/", "-"]
    ))

    # 5. Patterns Spécifiques "Jeunes" (Mélange Prenom + Dept + Année)
    # Ex: Pierre6904, 04Pierre69...
    # On prend 2 éléments parmi 3 pour éviter des patterns trop longs
    elements_jeunes = ["{Prenom}", "{Departement}", "{NaissanceAnneeCourt}"]
    for perm in itertools.permutations(elements_jeunes):
        patterns.append("".join(perm))

    # 6. Ajout des caractères spéciaux basiques sur les bases identité
    # Ex: Pierre.Dupont! , Pierre-Dupont123
    for base in bases_identite:
        patterns.append(f"{base}!")
        patterns.append(f"{base}123")
        patterns.append(f"{base}*")

    # Suppression des doublons éventuels
    return sorted(list(set(patterns)))