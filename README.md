# Import Japon

Site statique : éditions de jeux importées d'Asie, langues incluses et compatibilité avec les consoles européennes.

- `site/` : pages publiées telles quelles par GitHub Pages (exportées depuis le générateur).
- `donnees/generateur-fiches.html` : outil d'édition et de validation des fiches (à ouvrir dans Chrome).
- `donnees/import-japon-52-fiches.json` : sauvegarde des 52 fiches, à importer dans le générateur.
- `donnees/catalogue-v4.json` : ancien catalogue (liste de liens), conservé pour référence.
- `.github/workflows/publish.yml` : publie `site/` à chaque modification de ce dossier, sans régénération.

Le site est en `noindex` tant que l'option n'est pas décochée dans les Réglages du générateur.
