# Contribuer à Relinium

Merci de votre intérêt pour Relinium ! Ce document explique comment participer au projet de manière constructive et alignée avec nos valeurs.

## Avant de commencer

### Lecture recommandée

1. **README.md** – Vision globale et objectifs du projet
2. **CODE_OF_CONDUCT.md** – Règles de bienveillance et de respect
3. **docs/03-architecture/decisions/** – Décisions d'architecture (ADR)
4. **docs/03-architecture/rfcs/** – Propositions d'évolution (RFC)

### Principes fondamentaux

Relinium suit une approche **"docs-first"** :
- Toute décision structurante est **documentée avant** d'être implémentée
- Les choix techniques sont traçables via **ADR** (Architecture Decision Records)
- Les évolutions majeures passent par une **RFC** (Request for Comments)

## Process de contribution

### 1. Discuter avant de coder

Avant toute contribution :
- **Créer une issue** pour discuter de l'idée
- **Proposer une RFC** si l'évolution est majeure
- **Vérifier** qu'un travail similaire n'existe pas déjà

### 2. Documenter les décisions

Pour toute décision structurante :
- Rédiger un **ADR** (Architecture Decision Record)
- Expliquer le contexte, les options envisagées, et le choix retenu
- Placer l'ADR dans `docs/03-architecture/decisions/`

Format : `ADR-XXXX-titre-en-kebab-case.md`

### 3. Créer une Pull Request claire

- **1 sujet = 1 PR** (éviter les PR fourre-tout)
- **Titre explicite** et description complète
- **Références** : lier l'issue, la RFC ou l'ADR associée
- **Tests** : vérifier que le code fonctionne
- **Documentation** : mettre à jour les docs si nécessaire

### 4. Qualité et sécurité

- **Commits signés** : `git commit -S -m "message"`
- **Pas de secrets** dans le dépôt (tokens, mots de passe, clés API)
- **Justifier** chaque dépendance ajoutée
- **Code reviews** : accepter les retours constructifs

## Structure des commits

Format recommandé :

```
type(scope): description courte

- Détails supplémentaires
- Impacts et motivations

Refs: #issue-number, ADR-XXXX
```

Types courants :
- `feat` : nouvelle fonctionnalité
- `fix` : correction de bug
- `docs` : modification de documentation
- `refactor` : refactorisation sans changement fonctionnel
- `chore` : tâches techniques (CI, deps, etc.)
- `security` : correctif de sécurité

Exemples :
```
feat(auth): ajout d'authentification 2FA

- Implémentation TOTP
- Tests unitaires couverts
- Documentation utilisateur ajoutée

Refs: #42, ADR-0005
```

```
docs(adr): décision sur choix de base de données

- Analyse comparative PostgreSQL vs MongoDB
- Justification du choix PostgreSQL
- Mitigations des risques identifiés

Refs: RFC-003, ADR-0008
```

## Types de contributions acceptées

### Documentation
- Amélioration de la clarté
- Correction de fautes
- Ajout d'exemples
- Traductions

### Code
- Nouvelles fonctionnalités (avec RFC préalable)
- Corrections de bugs
- Améliorations de performance
- Tests automatisés

### Sécurité
- Signalement de vulnérabilités (via `SECURITY.md`)
- Corrections de failles
- Améliorations du modèle de menaces

### Gouvernance
- Propositions d'amélioration du process
- Retours d'expérience
- Suggestions d'outils

## Revue de code

Toute PR sera revue par au moins un mainteneur.

Critères de validation :
- ✅ Respect du code de conduite
- ✅ Documentation à jour
- ✅ Tests passants (si code)
- ✅ ADR rédigée (si décision structurante)
- ✅ Commits signés
- ✅ Pas de secrets dans le code

## Outils et environnement

### Prérequis
- Git (avec signature GPG configurée)
- Éditeur de texte supportant Markdown
- Selon les contributions : Node.js, Python, Docker, etc.

### Configuration Git recommandée
```bash
git config --global commit.gpgsign true
git config --global tag.gpgSign true
git config --global user.signingkey <votre-clé-GPG>
```

## Routine documentaire automatisée

La création (ou la mise à jour) d'un document normatif doit désormais passer par l’assistant fourni dans `scripts/new_doc_routine.py`. Une cible dédiée facilite l’usage :

```bash
make new-doc \
  ID=SPRINT-0002 \
  TYPE=SPRINT \
  STATUS="En cours" \
  DOC_PATH=docs/sprints/phase1/SPRINT-0002.md \
  VERSION=1.0.0 \
  TAGS="sprint,inventaire,stack" \
  LINKS="OBS-0001,RFC-0002" \
  AUTHOR="Agent Codex"
```

- Utiliser **DOC_PATH** (et non la variable d’environnement `PATH`) pour éviter d’écraser le PATH système.
- Le script peut être invoqué directement (`python scripts/new_doc_routine.py --help`) pour des usages avancés : template de corps, id_root spécifique, previous_hash, etc.
- À chaque exécution, la routine :
  - Regénère le front matter complet et calcule `self_hash` via `scripts/ssot_hash_check.py`.
  - Alimente `docs/_registry/registry_v1.1.yaml` en créant/rafraîchissant l’entrée `id_root`.
  - Lance `python scripts/validate_frontmatter.py` puis `make docs-check` (hash + registre).
  - Commit automatiquement les fichiers si tout est sain (désactivable avec `SKIP_COMMIT=1`).
- **Obligation** : toute modification de contenu (même mineure) doit repasser par la routine pour recalculer `self_hash` et synchroniser le registre avant de pousser une branche.
- Avant tout push/PR, relancer localement `python scripts/validate_frontmatter.py` **et** `make docs-check` pour garantir l’absence de divergences (le hook pré-commit fourni les exécute également).

## Questions fréquentes

### Comment proposer une nouvelle fonctionnalité ?
1. Créer une issue pour discussion
2. Si validée, rédiger une RFC
3. Attendre les retours et ajuster
4. Rédiger l'ADR correspondante
5. Implémenter avec PR

### Puis-je contribuer sans coder ?
Absolument ! Documentation, traductions, revue, design, tests manuels, rapports de bugs, etc. sont tout aussi précieux.

### Comment signaler un bug ?
Créer une issue avec :
- Description claire du problème
- Étapes pour reproduire
- Environnement (OS, version, etc.)
- Comportement attendu vs observé

### Comment suggérer une amélioration ?
Créer une issue de type "enhancement" ou proposer une RFC pour les évolutions majeures.

## Licence

En contribuant, vous acceptez que vos contributions soient publiées sous la même licence que le projet (à définir : MIT ou licence éthique).

## Contact

Pour toute question :
- **Issues GitHub** (privilégié)
- **Email** : contact@pixelprowlersgit add contributing.md.io

---

Merci de contribuer à un numérique plus juste, sobre et humain ! 🌱
