# CICD

CI et CD sont des pratiques d’automatisation qui évitent l’« enfer des intégrations » et les déploiements manuels fragiles, en rendant les changements de code fréquents, testés et déployables en continu.

## 1. Qu’est-ce que la CI ?

- ### Définition :
la Continuous Integration, c’est le fait de merger souvent du code (plusieurs fois par jour) sur une branche partagée, avec une pipeline automatique qui build et exécute les tests à chaque push/PR.

- ### Problèmes résolus :
gros conflits de merge en fin de sprint, bugs découverts très tard, régressions après intégration d’un gros lot de code, tests manuels chronophages.

- ### Principes clés :
petits commits fréquents, dépôt central unique, build/tests automatisés, feedback rapide, règle « build rouge = on arrête tout et on répare ».

- ### Exemples d’outils de CI :
GitHub Actions, GitLab CI, Jenkins.

## 1. Qu’est-ce que le CD ?

- ### Définition générale :
le CD automatise ce qui se passe après la CI : packaging, déploiement sur les environnements (recette, staging, prod), migrations, etc.

## Continuous Delivery vs Continuous Deployment :

- ### Continuous Delivery :
tout est automatisé jusqu’à un artefact prêt à être déployé ; la mise en prod nécessite encore un « OK » humain (bouton ou approval).

- ### Continuous Deployment :
si la pipeline est verte, la mise en prod est déclenchée automatiquement, sans validation manuelle.

- ### Bénéfices :
déploiements fréquents et reproductibles, moins de stress en release, feedback utilisateur plus rapide, petits changements donc moins risqués individuellement.

- ### Risques :
pousser plus vite des bugs en prod si la qualité des tests est faible, erreurs de configuration d’infra, incidents plus fréquents si la supervision et le rollback ne sont pas maîtrisés.

## 3. Pourquoi CI/CD est important ?

- ### Impact sur la qualité du code :
impose des tests automatiques, linters, vérifs de style/sécurité à chaque changement, ce qui réduit les régressions et uniformise le niveau de qualité.

- ### Impact sur la vitesse de développement :
moins de tâches manuelles (tests à la main, packaging, déploiements), boucle de feedback plus courte, ce qui permet d’itérer plus vite et de livrer plus souvent.

- ### Impact sur la collaboration :
tout le monde passe par la même pipeline, l’état du projet est visible (build vert/rouge), cela réduit les « chez moi ça marche » et facilite le travail en équipe sur une même base de code.

### ================================================================================================================

# UV

## 1. Qu’est-ce que uv ?

- uv est le gestionnaire de paquets Python le plus rapide, il installe et gère les versions de Python, crée des environnements virtuels, gère les dépendances, exécute des scripts et fournit aussi une interface compatible pip (uv pip).
- Contrairement à pip (qui ne gère ni projet ni lockfile standard) et à Poetry/pipenv (plus lents, centrés sur un seul use‑case), uv vise à être un outil unifié « tout‑en‑un » (package manager + project manager + gestion de Python) avec des performances très élevées.

### Avantages principaux :
- Très rapide (écrit en Rust, cache agressif, binaire autonome).
- Gestion unifiée de l’environnement : création de projets, venv, installation de Python, dépendances, scripts, lockfile unique (uv.lock).
- Compatible avec l’écosystème existant (pyproject.toml, interface pip‑like, outils classiques comme pytest, Ruff, etc.).

## 2. uv et pyproject.toml

- uv considère le projet comme défini par un pyproject.toml standard, que tu peux créer avec uv init ou uv init --bare.
- La section [project] contient le nom, la version, requires-python et la liste dependencies, et [project.optional-dependencies] sert pour les deps de dev ou extras (par ex. dev = ["pytest", "ruff"]).
- Quand tu fais uv add ou uv add --dev, uv met à jour pyproject.toml, résout les versions et écrit un lockfile (uv.lock) pour figer l’ensemble, puis installe les paquets dans l’environnement du projet.
- Le build backend est déclaré dans [build-system] du pyproject.toml (ex. hatchling, setuptools), et uv respecte ce choix comme n’importe quel outil conforme PEP 517 : il ne remplace pas le backend, il l’utilise pour builder le paquet.

## 3. Utiliser uv dans GitHub Actions

- L’installation recommandée en CI passe par l’action officielle astral-sh/setup-uv, qui installe uv dans le job et le met dans le PATH.
- Pour le cache des dépendances, cette action (ou celle du Marketplace « Setup uv and Handle Its Cache ») utilise typiquement uv.lock ou pyproject.toml comme clé, afin de réutiliser le cache tant que les deps ne changent pas.

### Le workflow typique est :
- installer uv avec l’action,
- exécuter uv sync ou équivalent pour installer les dépendances à partir de pyproject.toml/uv.lock,
- lancer ensuite les commandes de CI classiques (uv run pytest, uv run ruff, etc.), uv se chargeant d’utiliser l’environnement du projet.

### ================================================================================================================

# Semantic Release

## 1. Versionnage sémantique (SemVer)
Le versionnage sémantique (SemVer) est une convention de numérotation de versions du type MAJOR.MINOR.PATCH, où chaque nombre a une signification claire liée aux changements du code.​

### Format MAJOR.MINOR.PATCH

- MAJOR : changements incompatibles (breaking changes).
- MINOR : nouvelles fonctionnalités rétro‑compatibles.
- PATCH : corrections de bugs sans modification de l’API.

### Quand bumper chaque niveau ?

- Bump MAJOR : tu casses une API publique, supprimes/changes un comportement sur lequel des utilisateurs peuvent dépendre.
- Bump MINOR : tu ajoutes une fonctionnalité ou une extension d’API, sans casser l’existant.
- Bump PATCH : tu corriges un bug, améliores les perfs ou ajustes un détail interne, sans nouvelle feature visible.

## 2. Conventional Commits

- Format des messages : Conventional Commits impose un format du style :

    type(scope)?: description (ex. feat(api): add user endpoint).

- Types de commits courants

    - feat : ajout d’une nouvelle fonctionnalité visible (nouvelle API, nouvel écran, nouveau comportement).
    - fix : correction de bug (fonctionnalité existante réparée, comportement incorrect corrigé).
    - docs : changements de documentation uniquement (README, doc utilisateur, doc technique).
    - style : changements de style de code sans impact sur le comportement (indentation, espaces, formatage).
    - refactor : refactorisation interne du code, même comportement externe mais structure/modularisation modifiée.
    - test : ajout ou modification de tests (unitaires, d’intégration, etc.) sans changer le code applicatif.
    - chore : tâches de maintenance ou de support (maj de dépendances, config CI, scripts, outils) sans impact fonctionnel direct.
    - Le suffixe ! ou la mention BREAKING CHANGE: dans le body signale une rupture de compatibilité.
      - Suffixe ! (ex. feat!: ... ou feat(api)!: ...) : indique que ce commit introduit un breaking change (rupture de compatibilité).
      - Footer BREAKING CHANGE: dans le body du commit : même signification, il décrit en texte la rupture de compatibilité et ce que les utilisateurs doivent adapter.
        - Exemple : <br>
            feat(api): change la signature de get_user<br>
            Ici tu mets la description détaillée du changement.<br>
            BREAKING CHANGE: explique précisément ce qui casse et quoi modifier.<br>

- Impact sur le versionnage : Dans beaucoup d’outils, ces types pilotent SemVer :

    - fix → bump PATCH.
    - feat → bump MINOR.
    - Commit marqué breaking (! ou BREAKING CHANGE) → bump MAJOR.

## 3. python-semantic-release

- Configuration dans pyproject.toml :
    - python-semantic-release lit la config dans [tool.semantic_release] (version source, branche de release, type de versioning, options de changelog, etc.).
    - On définit par exemple où se trouve la version (fichier, tag), si on utilise Conventional Commits, et comment publier (GitHub, PyPI…).

- Génération du CHANGELOG
  - L’outil lit l’historique des commits depuis la dernière version, classe les messages par type (feat, fix, …) et génère/met à jour un CHANGELOG.md structuré automatiquement.

- Création des releases GitHub : Lorsqu’il est lancé (souvent via GitHub Actions), python-semantic-release :
    - Calcule la nouvelle version en fonction des commits (SemVer + Conventional Commits).
    - Crée un tag Git correspondant.
    - Publie une release GitHub avec ce tag et le texte de release basé sur le changelog généré.
​
### ================================================================================================================

# Comparatif d'outils

## Linters Python

Analysent statiquement ton code pour détecter erreurs, mauvaises pratiques et problèmes de style avant exécution (ex. Ruff, Flake8, Pylint).

| Outil  | Catégorie | Avantages                                                                           | Inconvénients                                                                           | Note /10 | Choix ? |
| ------ | --------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | -------- | ------- |
| Ruff   | Linter    | Ultra rapide, couvre de nombreuses règles et remplace plusieurs linters classiques. | Moins configurable finement que Pylint, adoption encore en cours dans certains projets. | 9/10     | ✅       |
| Flake8 | Linter    | Léger, extensible via de nombreux plugins, très connu dans l’écosystème.            | Plus lent et moins complet que Ruff sur les gros projets modernes.                      | 7/10     | ⚪       |
| Pylint | Linter    | Analyse très détaillée, nombreuses règles et forte customisation.                   | Lent, verbeux et génère plus de faux positifs.                                          | 7/10     | ⚪       |

## Formatters Python

Reformattent automatiquement ton code selon un style défini (ex. Black, Ruff format, autopep8), pour avoir un style homogène sans débat de mise en forme.

| Outil       | Catégorie | Avantages                                                          | Inconvénients                                                         | Note /10 | Choix ? |
| ----------- | --------- | ------------------------------------------------------------------ | --------------------------------------------------------------------- | -------- | ------- |
| Ruff format | Formatter | Formatage compatible Black avec les performances de Ruff.          | Moins connu que Black seul, écosystème encore jeune.                  | 9/10     | ✅       |
| Black       | Formatter | Style standard de facto, largement adopté, résultat très cohérent. | Très peu configurable, impose un style unique.                        | 9/10     | ✅       |
| autopep8    | Formatter | Corrige rapidement les violations PEP8 existantes.                 | N’uniformise pas vraiment le style global et laisse des incohérences. | 6/10     | ❌       |

## Type Checkers

Vérifient que les types annotés dans ton code sont cohérents (ex. Mypy, Pyright, Pyre), ce qui aide à attraper des bugs avant l’exécution.

| Outil   | Catégorie    | Avantages                                                                    | Inconvénients                                                         | Note /10 | Choix ? |
| ------- | ------------ | ---------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------- | ------- |
| Mypy    | Type checker | Référence historique du typage statique Python, très documenté.              | Plus lent et parfois plus strict que des alternatives récentes.       | 8/10     | ✅       |
| Pyright | Type checker | Très rapide avec excellente intégration à VS Code et bons messages d’erreur. | Moins présent dans certains exemples ou docs CI orientés Mypy.        | 9/10     | ✅       |
| Pyre    | Type checker | Conçu pour l’analyse typée à grande échelle dans de gros monorepos.          | Installation et configuration plus complexes hors environnement Meta. | 6/10     | ⚪       |

## Frameworks de Tests

Fournissent la structure pour écrire et exécuter des tests automatisés (ex. pytest, unittest), avec assertions, fixtures et rapports.

| Outil    | Catégorie | Avantages                                                           | Inconvénients                                                                | Note /10 | Choix ? |
| -------- | --------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------- | -------- | ------- |
| pytest   | Tests     | Syntaxe concise, fixtures puissantes, énorme écosystème de plugins. | Comportement parfois perçu comme « magique » pour les débutants.             | 9/10     | ✅       |
| unittest | Tests     | Inclus dans la stdlib, stable et bien documenté.                    | Plus verbeux et moins ergonomique que pytest pour de grandes bases de tests. | 7/10     | ⚪       |

## Security Scanners

Scannent ton code et/ou tes dépendances pour trouver des vulnérabilités connues ou des patterns dangereux (ex. Bandit, Safety, Snyk, Trivy).

| Outil  | Catégorie | Avantages                                                                                 | Inconvénients                                                                 | Note /10 | Choix ? |
| ------ | --------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | -------- | ------- |
| Bandit | Sécurité  | Analyse statique dédiée au code Python pour détecter des patterns de vulnérabilité.       | Produit des faux positifs et ne couvre pas les vulnérabilités de dépendances. | 8/10     | ✅       |
| Safety | Sécurité  | Détecte les vulnérabilités connues dans les dépendances via des bases CVE.                | Ne scanne pas le code source ni les conteneurs.                               | 8/10     | ✅       |
| Snyk   | Sécurité  | Plateforme complète pour dépendances, code et conteneurs avec nombreuses intégrations CI. | Fonctionnalités avancées payantes et outil plus lourd pour petits projets.    | 8/10     | ⚪       |
| Trivy  | Sécurité  | Scanner open source rapide pour images, systèmes de fichiers et IaC (Infra as Code).      | Moins spécialisé sur le code Python pur que Bandit ou Safety.                 | 8/10     | ✅       |

### ================================================================================================================

# MkDocs & GitHub Pages

MkDocs permet de transformer des fichiers Markdown en un site statique de documentation, qu'on peut ensuite publier facilement sur GitHub Pages.

- Comment MkDocs génère de la documentation ?

  - MkDocs lit la configuration dans mkdocs.yml et les fichiers Markdown du dossier docs/, puis les transforme en pages HTML statiques avec un thème (ex. Material).​
  - La commande de base est mkdocs build, qui génère le site dans un dossier site/ prêt à être servi par n’importe quel hébergeur statique.​

- Comment déployer sur GitHub Pages ?

  - La manière classique est d’utiliser mkdocs gh-deploy, qui build le site puis pousse automatiquement le contenu sur une branche gh-pages du repo.​
  - Ensuite, dans les paramètres GitHub Pages, on choisit la branche gh-pages comme source, et GitHub sert directement ton site de doc à une URL du type https://user.github.io/repo/.​

- Qu'est-ce que mkdocstrings ?
  - mkdocstrings est un plugin MkDocs qui génère automatiquement la documentation d’API à partir des docstrings de ton code (par ex. fonctions, classes Python).
  - On écrit simplement dans ton Markdown des blocs du style ::: package.module.Class, et mkdocstrings injecte la doc correspondante (signatures, paramètres, types, docstrings formatées) directement dans les pages.​

### ================================================================================================================

# Identifier les problèmes

1. **Le code fonctionne, mais** :
  - Est-il maintenable ?
Sans typage, le code devient difficile à lire, à maintenir, à étendre et à corriger en équipe, surtout en grandissant.​

  - Est-il sécurisé ?
pas sécurisé ! plusieurs secrets sont exposés (clé API ...)

  - Est-il bien documenté ?
Il manque la documentation dans beaucoup de parties du code.

1. **Comment détecter ces problèmes automatiquement ?**
- Quels outils utiliser ?
Ruff, Black, Mypy, pytest et Bandit 

  - Ruff : détecte rapidement erreurs et problèmes de style dans le code Python.
  - Black : formate automatiquement le code selon un style uniforme.
  - Mypy : vérifie la cohérence des types annotés dans le code.
  - pytest : exécute et organise les tests automatisés.
  - Bandit : repère les failles de sécurité dans le code Python.

- À quel moment les exécuter ?
  - En local, avant chaque commit : lancer Ruff, Black, Mypy et Bandit pour garantir qualité, style, types et sécurité avant validation.
  - Dans la CI (à chaque push ou PR) : exécuter les mêmes outils plus les tests pytest pour bloquer les erreurs avant fusion.
  - En CD (déploiement automatisé) : vérifier que la build et les tests passent avant déploiement, souvent via la pipeline CI intégrée au CD.

1. **Comment empêcher ces problèmes à l'avenir ?**
En mettant en place des hooks de pre-commit locaux et pipelines CI/CD automatiques pour lint, tests, typage, et sécurité systématiques avant fusion.

### ================================================================================================================

# Conventional Commits

1. Pourquoi protéger les branches ?
- Pour éviter erreurs, suppressions accidentelles et modifications non contrôlées.

Que se passerait-il sans protection ?
- Risque de bugs, conflits, perte de code, et mauvaise qualité du dépôt.

2. Pourquoi Conventional Commits ?
- Pour standardiser les messages, faciliter la lecture, l’automatisation et le versionnage.

Avantages pour l'équipe
- Meilleure communication, compréhension claire des changements, moins d’erreurs humaines.

Avantages pour le versionnage automatique
- Permet de générer automatiquement les versions et changelogs fiables et cohérents.

3. Différence entre develop et main ?
- develop sert au développement continu, main est la branche stable prête à être déployée.

Quand merger dans develop ?
- Quand une fonctionnalité ou correction est terminée et validée en local ou feature branch.

Quand merger dans main ?
- Quand la version est testée, stable et prête pour la production ou livraison.

### ================================================================================================================

# CI Pipeline - Tests, Quality & Security

1. Pourquoi plusieurs jobs séparés ?
  - Permet d’exécuter les tâches en parallèle, donc CI plus rapide.
  - Plus simple de cibler précisément la cause d’un échec grâce aux logs spécialisés.

2. Que faire si la CI échoue ?
  - Lire les logs dans l’interface de la CI pour identifier l’erreur précise.
  - Tenter de reproduire l’erreur localement avec les mêmes commandes CI.

3. Faut-il tout corriger d'un coup ?
  - Non, privilégier de petites PRs facilite la compréhension et la validation.
  - Les revues de code sont plus rapides et moins sujettes aux erreurs.

### ================================================================================================================

# Pre-commit Hooks



1. Différence entre pre-commit et CI ?

  - Pre-commit : s'exécute en local avant chaque commit sur les fichiers modifiés.
  - CI : s'exécute sur le serveur après chaque push/PR sur tout le projet.
  - Pourquoi les deux ? Pre-commit détecte vite les erreurs en local ; CI garantit que même ceux qui n'ont pas installé pre-commit respectent les règles.

2. Peut-on bypass pre-commit ?

  - Oui, avec git commit --no-verify ou -n.
  - Mauvaise idée : tu contournes les vérifications et risques de casser la CI.
  - Comment l'empêcher ? Impossible côté Git local, mais la CI bloquera quand même les erreurs.

3. Pre-commit ralentit-il le développement ?

  - Ajoute 5-10 secondes par commit.
  - Mais économise 5-15 minutes d'attente CI + corrections si erreurs détectées après coup.
  - Globalement, ça accélère le workflow.

### ================================================================================================================

# Build & Push Docker Image vers GHCR

1. Pourquoi containeriser ?

- Avantages Docker :

  - Portabilité totale : même environnement partout (dev, test, prod)
  - Isolation complète : pas de conflits entre applications
  - Rapide et léger : démarrage en secondes, moins de ressources qu'une VM

- "Works on my machine" :
  - Docker empaquette l'app + toutes ses dépendances = plus de différence entre ton PC et la prod.
​
2. Multi-stage build : pourquoi ?

- Taille :
  - Sépare build (outils lourds) et exécution (artefact final seul) → images 5-10x plus petites.

- Sécurité :
  - Pas d'outils de build ni de dépendances dev dans l'image finale = moins de surface d'attaque.

3. Tagging strategy

- Pourquoi plusieurs tags ?
  - Référencer la même image différemment selon le besoin (rollback, traçabilité, déploiement).

- latest vs semver vs sha :

  - latest : dernière version, pratique mais dangereux (change sans prévenir)
  - semver (v1.2.3) : versioning clair, parfait pour releases stables
  - sha (abc1234) : immuable, garantit exactement quelle version tourne en prod

### ================================================================================================================

# Semantic Release

1. Quels commits déclenchent un bump de version ?

  - feat: → bump MINOR (1.0.0 → 1.1.0)
  - fix: ou perf: → bump PATCH (1.0.0 → 1.0.1)
  - BREAKING CHANGE: (dans le footer) → bump MAJOR (1.0.0 → 2.0.0)

2. Différence entre main et develop ?

  - main : releases stables (ex: 1.0.0, 2.0.0)
  - develop : releases pre-release/rc (ex: 1.1.0-rc.1, 1.1.0-rc.2)

3. Que contient le CHANGELOG ?

  - Liste automatiquement générée de tous les commits groupés par type (feat, fix, etc.) pour chaque version, avec liens vers les PRs et commits.
​
