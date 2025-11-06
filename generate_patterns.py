def generer_patterns_basiques():
    """Retourne une liste de patterns courants de mots de passe."""
    return [
        # Patterns simples
        "{Nom}",
        "{Prenom}",
        "{Ville}",
        
        # Avec année
        "{Nom}{AnneeNaissance}",
        "{Prenom}{AnneeNaissance}",
        "{Nom}{Prenom}{AnneeNaissance}",
        "{Prenom}{Nom}{AnneeNaissance}",
        "{AnneeNaissance}{Nom}",
        "{AnneeNaissance}{Prenom}",
        
        # Avec séparateurs
        "{Prenom}.{Nom}",
        "{Prenom}_{Nom}",
        "{Prenom}-{Nom}",
        "{Nom}.{Prenom}",
        "{Nom}_{Prenom}",
        
        # Avec ville
        "{Prenom}{Ville}",
        "{Nom}{Ville}",
        "{Ville}{AnneeNaissance}",
        "{Prenom}{Ville}{AnneeNaissance}",
        
        # Avec code postal
        "{Prenom}{CodePostal}",
        "{Nom}{CodePostal}",
        "{Ville}{CodePostal}",
        
        # Avec caractères spéciaux courants
        "{Prenom}!",
        "{Nom}!",
        "{Prenom}{AnneeNaissance}!",
        "{Nom}{AnneeNaissance}!",
        "{Prenom}123",
        "{Nom}123",
        "{Prenom}@{AnneeNaissance}",
        
        # Patterns avec date de naissance complète
        "{Prenom}{DateNaissance}",
        "{Nom}{DateNaissance}",
        "{DateNaissance}{Prenom}",
        
        # Patterns avec initiales
        "{Prenom}{Nom[0]}",
        "{Nom[0]}{Prenom}",
    ]