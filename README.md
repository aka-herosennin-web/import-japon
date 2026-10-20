# Import Japon – site Play-Asia automatique

## Fonctionnement

- Catalogue **numérique**, région japonaise (`JP`) uniquement. Le catalogue physique n'est PAS accessible via l'API L402 documentée.
- Recherches configurées dans `build.py`; au plus 30 produits, dédupliqués.
- API Play-Asia interrogée par **GitHub Actions**, pas par les navigateurs des visiteurs.
- Aucun logiciel à installer sur le PC : GitHub exécute Python sur ses serveurs.
- Actualisation quotidienne à 06:15 UTC, puis publication automatique.
- En cas d'échec total de l'API ou sans résultat pertinent, la tâche échoue et **ne remplace pas le site existant**.
- Aucun contenu de jeu inventé, aucune compatibilité présumée. Les visuels ne sont pas réutilisés en attendant permission.
- Pages `noindex` pour les essais, et `rel=sponsored` sur les liens marchands.

## Prévisualisation

`site/index.html` est une **démonstration statique** fournie pour voir le design, avec un seul jeu issu de l'échantillon d'API déjà partagé. Elle n'indique pas le stock/prix actuels.

## Publication sur GitHub Pages (gratuite sur dépôt public)

1. Créer un **dépôt GitHub public** (par ex. `import-japon-test`).
2. Envoyer TOUS les fichiers du dossier, en conservant `.github/workflows/publish.yml`.
3. Dans **Settings > Pages**, choisir **Source : GitHub Actions**.
4. Dans **Actions**, sélectionner `Actualiser et publier le catalogue` puis **Run workflow**.
5. Quand le lancement réussit, ouvrir l'adresse fournie par GitHub Pages (souvent `https://VOTRE-COMPTE.github.io/import-japon-test/`).
6. Chaque jour, GitHub Actions relance la synchronisation. Les planifications GitHub peuvent être retardées/suspendues en cas d'inactivité.

**ATTENTION :** publier rend le code et les données publics sur GitHub Pages. Le site comporte volontairement `noindex` : il est visible avec le lien mais ne vise pas Google avant validation légale, conditions de réutilisation et fiabilité des données. `noindex` **n'est pas une protection de confidentialité**.

## Vérifications avant exploitation publique

- Autorisation contractuelle de l'utilisation des données Play-Asia hors API d'achat/agent.
- Mentions légales complètes et informations de l'éditeur adaptées à son statut.
- Restrictions éventuelles d'affiliation et attribution sur les liens L402.
- Prix, taxes, devises et stocks susceptibles de changer.
- Le catalogue L402 inclut des produits divers : le filtre `JP` n'est pas une preuve de langue ni de compatibilité réelle.

