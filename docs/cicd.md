# CI/CD et Semantic Release

## Intégration continue (CI)

La CI exécute :
- Ruff (lint + format).
- Mypy (typage).
- Bandit (sécurité).
- Tests unitaires + couverture.

Le workflow se trouve dans `.github/workflows/ci.yml`.

## Semantic Release

Semantic Release gère :
- Le versionnement sémantique (major / minor / patch).
- La génération automatique du CHANGELOG.
- La création des releases GitHub.
- Le taggage automatique des versions.

Configuration : `pyproject.toml` (`[tool.semantic_release]`).

## Documentation

La documentation MkDocs est déployée via `.github/workflows/docs.yml` sur la branche `gh-pages`.
