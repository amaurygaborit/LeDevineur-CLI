<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>LeDevineur-CLI - Documentation</title>
</head>
<body>

    <h1>🔐 LeDevineur-CLI</h1>

    <p>
        <strong>LeDevineur-CLI</strong> est un générateur de dictionnaire de mots de passe <strong>contextuel</strong> et <strong>hautement performant</strong>.
    </p>

    <p>
        Contrairement aux générateurs aléatoires (brute-force), cet outil se base sur <strong>l'ingénierie sociale</strong> : il génère des combinaisons probables à partir d'informations personnelles (nom, date de naissance, passions, enfants...) en y appliquant des transformations intelligentes (Leet Speak, variations de casse, formats de dates).
    </p>

    <blockquote>
        <p>⚡ <strong>Performance :</strong> Doté d'une architecture par partitionnement (sharding), il est capable de générer des millions de mots de passe uniques avec une utilisation minimale de la memoire vive.</p>
    </blockquote>

    <hr>

    <h2>🚀 Fonctionnalités Clés</h2>
    <ul>
        <li><strong>Génération Contextuelle :</strong> Utilise un fichier de configuration <code>infos.json</code> pour cibler la génération.</li>
        <li><strong>Moteur de Patterns :</strong> Combine les informations selon des modèles définis dans <code>patterns.txt</code></li>
        <li><strong>Gestion Avancée des Dates :</strong> Détecte automatiquement les formats de dates et génère toutes les variantes (25081995, 250895, 1995, 95...).</li>
        <li><strong>Transformations Intelligentes :</strong>
            <ul>
                <li><strong>Leet Speak :</strong> 2 niveaux de complexité (Basique <code>e=3</code> / Avancé <code>t=7</code>).</li>
                <li><strong>Casse Contrôlée :</strong> Injection de majuscules aléatoires sans explosion combinatoire.</li>
            </ul>
        </li>
        <li><strong>Mode Simulation :</strong> Permet de prévisualiser le volume de données avant la génération.</li>
    </ul>

    <hr>

    <h2>📦 Installation</h2>

    <h3>Prérequis</h3>
    <p>Python 3.8 ou supérieur. Aucune dépendance externe (utilise uniquement la librairie standard).</p>

    <h3>Mise en place</h3>
    <pre><code>git clone https://github.com/votre-user/LeDevineur-CLI.git
cd LeDevineur-CLI</code></pre>

    <hr>

    <h2>⚙️ Configuration</h2>
    <p>Avant de lancer le programme, configurez vos fichiers cibles.</p>

    <h3>1. Fichier <code>infos.json</code> (Vos données)</h3>
    <p>Remplissez ce fichier avec les informations de la cible.</p>
    <pre><code>{
  "Nom": "Dupont",
  "Prenom": "Pierre",
  "DateNaissance": "25/08/1995",
  "EquipeSport": "OM",
  "AnimalNom": "Rex"
}</code></pre>

    <h3>2. Fichier <code>patterns.txt</code> (Vos règles)</h3>
    <p>Définissez comment combiner les informations. Utilisez les <strong>mêmes clés</strong> que dans le JSON.</p>
    <pre><code># Exemples de patterns
Prenom, Nom
Prenom, DateNaissance
AnimalNom, DeptNaissance</code></pre>

    <hr>

    <h2>💻 Utilisation (CLI)</h2>

    <h3>1. Mode Simulation (Recommandé)</h3>
    <p>Voir combien de mots de passe seraient générés <strong>sans</strong> créer le fichier.</p>
    <pre><code>python main.py --simulation --verbose</code></pre>

    <h3>2. Génération Standard</h3>
    <p>Génère le dictionnaire avec les paramètres par défaut (Leet niveau 1, Max 3 substitutions).</p>
    <pre><code>python main.py --verbose</code></pre>
    <p><em>Le résultat sera enregistré dans <code>dictionnaire.txt</code>.</em></p>

    <h3>3. Génération Avancée</h3>
    <pre><code>python main.py --niveau-leet 2 --max-leet 5 --max-casse 4 -v</code></pre>

    <h3>📖 Tableau des Arguments</h3>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Argument</th>
                <th>Description</th>
                <th>Défaut</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>-h, --help</code></td>
                <td>Affiche l'aide complète.</td>
                <td>-</td>
            </tr>
            <tr>
                <td><code>-s, --source</code></td>
                <td>Chemin du fichier JSON source.</td>
                <td>infos.json</td>
            </tr>
            <tr>
                <td><code>-p, --patterns</code></td>
                <td>Chemin du fichier de structures.</td>
                <td>patterns.txt</td>
            </tr>
            <tr>
                <td><code>-o, --output</code></td>
                <td>Chemin du fichier de sortie.</td>
                <td>dictionnaire.txt</td>
            </tr>
            <tr>
                <td><code>-v, --verbose</code></td>
                <td>Affiche les barres de progression.</td>
                <td>Désactivé</td>
            </tr>
            <tr>
                <td><code>-S, --simulation</code></td>
                <td>Simule le calcul sans écrire.</td>
                <td>Désactivé</td>
            </tr>
            <tr>
                <td><code>--niveau-leet</code></td>
                <td>1 (Simple) ou 2 (Complexe).</td>
                <td>1</td>
            </tr>
            <tr>
                <td><code>--max-leet</code></td>
                <td>Max substitutions par mot.</td>
                <td>3</td>
            </tr>
        </tbody>
    </table>

    <hr>

    <h2>🏗 Architecture Technique</h2>
    <ol>
        <li><strong>Pool de Variantes :</strong> Transformation des données JSON en variantes (Casse + Leet) en mémoire.</li>
        <li><strong>Partitionnement :</strong> Distribution des combinaisons dans 64 fichiers temporaires basés sur leur Hash (évite la saturation RAM).</li>
        <li><strong>Fusion (Merge) :</strong> Relecture, dédoublonnage et fusion finale.</li>
    </ol>

    <hr>

    <h2>👥 Auteurs</h2>
    <p>Projet réalisé dans le cadre du cursus ingénieur 4A (Polytech Dijon).</p>
    <ul>
        <li><strong>Robin RUSSIER</strong></li>
        <li><strong>Amaury GABORIT</strong></li>
    </ul>

    <p><em>Ce projet est destiné uniquement à des fins éducatives et de test d'intrusion autorisé.</em></p>

</body>
</html>