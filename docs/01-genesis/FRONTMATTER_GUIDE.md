# Guide du Frontmatter Relinium

**Version** : 1.0.0  
**Date** : 2025-01-05  
**Statut** : Stable  

---

## 📚 Table des matières

1. [Introduction](#introduction)
2. [Qu'est-ce que le frontmatter ?](#quest-ce-que-le-frontmatter)
3. [Champs obligatoires](#champs-obligatoires)
4. [Champs recommandés](#champs-recommandés)
5. [Champs optionnels](#champs-optionnels)
6. [Exemples par type de document](#exemples-par-type-de-document)
7. [Statuts et cycles de vie](#statuts-et-cycles-de-vie)
8. [Bonnes pratiques](#bonnes-pratiques)
9. [Validation](#validation)
10. [FAQ](#faq)

---

## Introduction

Ce guide explique comment utiliser les métadonnées frontmatter dans les documents Relinium. Le frontmatter est le système de métadonnées qui permet de :

- **Tracer** l'historique et l'évolution des documents
- **Organiser** et classifier la documentation
- **Valider** automatiquement la cohérence du projet
- **Générer** le registre documentaire central

Le frontmatter suit la philosophie **"Minimal Viable Metadata"** : assez de structure pour garantir la qualité, assez de flexibilité pour rester pratique.

---

## Qu'est-ce que le frontmatter ?

Le frontmatter est un bloc de métadonnées au format YAML placé **au début** de chaque document Markdown. Il est délimité par des triples tirets (`---`).

### Structure de base

```markdown
---
id: "ADR-0001"
type: "ADR"
status: "Accepté"
date: "2025-01-03"
---

# Titre du document

Contenu du document...
```

### Règles structurelles

1. Le frontmatter doit être **en début de fichier** (première ligne)
2. Délimité par `---` au début ET à la fin
3. Contenu au format **YAML valide**
4. Encodage **UTF-8**
5. Contient au minimum les **4 champs obligatoires**

---

## Champs obligatoires

Ces 4 champs DOIVENT être présents dans tous les documents :

### `id` (Identifiant unique)

**Format** : `TYPE-NNNN`

- `TYPE` : Type de document (ADR, RFC, OBS, POC, SPRINT_DOC)
- `NNNN` : Numéro séquentiel sur 4 chiffres avec padding zéros

**Exemples** :
```yaml
id: "ADR-0001"    # Premier ADR
id: "RFC-002"     # Deuxième RFC (padding flexible)
id: "OBS-0003"    # Troisième observation
id: "POC-0042"    # 42ème POC
id: "SPRINT_DOC-0001"  # Premier document de sprint
```

**Règles** :
- ✅ Unique dans tout le projet
- ✅ Séquentiel par type de document
- ❌ Pas de réutilisation après suppression
- ❌ Pas d'espace ni caractères spéciaux

---

### `type` (Type de document)

**Valeurs possibles** : `ADR` | `RFC` | `OBS` | `POC` | `SPRINT_DOC`

| Type | Signification | Usage |
|------|---------------|-------|
| **ADR** | Architecture Decision Record | Décisions d'architecture validées |
| **RFC** | Request For Comments | Propositions ouvertes à discussion |
| **OBS** | Observation | Observations factuelles sans jugement |
| **POC** | Proof of Concept | Résultats de prototypes techniques |
| **SPRINT_DOC** | Document de Sprint | Planification et suivi de sprints |

**Exemples** :
```yaml
type: "ADR"         # Décision d'architecture
type: "RFC"         # Proposition technique
type: "OBS"         # Observation factuelle
type: "POC"         # Résultat de prototype
type: "SPRINT_DOC"  # Document de sprint
```

**Règle** : Le type doit correspondre au préfixe de l'ID
```yaml
# ✅ Cohérent
id: "ADR-0001"
type: "ADR"

# ❌ Incohérent
id: "RFC-001"
type: "ADR"
```

---

### `status` (Statut du document)

**Type** : Chaîne de caractères

Le statut indique où en est le document dans son cycle de vie. Les valeurs possibles **dépendent du type** de document.

**Exemples** :
```yaml
# Pour un ADR
status: "Accepté"

# Pour une RFC
status: "En discussion"

# Pour une OBS
status: "Ouvert"

# Pour un POC
status: "Complete"

# Pour un SPRINT_DOC
status: "En cours"
```

Voir la section [Statuts et cycles de vie](#statuts-et-cycles-de-vie) pour la liste complète.

---

### `date` (Date)

**Format** : ISO 8601 (`YYYY-MM-DD`)

Date de création ou de dernière modification majeure du document.

**Exemples** :
```yaml
date: "2025-01-05"   # 5 janvier 2025
date: "2025-11-03"   # 3 novembre 2025
date: "2024-12-25"   # 25 décembre 2024
```

**Règles** :
- ✅ Format strict YYYY-MM-DD
- ✅ Date valide dans le passé ou présent
- ❌ Pas de date dans le futur
- ❌ Pas d'autre format (DD/MM/YYYY interdit)

---

## Champs recommandés

Ces champs ne sont pas obligatoires mais **fortement recommandés** :

### `author` (Auteur)

**Type** : Chaîne de caractères

Identifie l'auteur principal ou l'équipe responsable du document.

**Exemples** :
```yaml
author: "Équipe Relinium Genesis"   # Nom d'équipe
author: "Alice Dupont"              # Nom de personne
author: "Équipe Backend"            # Équipe spécifique
author: "@alice"                    # Handle/pseudo
```

**Bonne pratique** : Utilisez une convention cohérente dans tout le projet.

---

### `version` (Version)

**Format** : SemVer simplifié (`MAJOR.MINOR` ou `MAJOR.MINOR.PATCH`)

Version du document selon le principe de versionnage sémantique.

**Exemples** :
```yaml
version: "1.0"      # Version stable initiale
version: "1.2"      # Ajout de contenu significatif
version: "2.0"      # Changement structurel majeur
version: "1.2.3"    # Correction mineure (optionnel)
```

**Guide d'incrémentation** :
- **MAJOR** (1.x → 2.x) : Changements structurels, réorganisation majeure
- **MINOR** (x.1 → x.2) : Ajouts de sections, modifications significatives
- **PATCH** (x.x.1 → x.x.2) : Corrections typos, clarifications mineures

---

## Champs optionnels

### `tags` (Tags)

**Type** : Tableau de chaînes

Tags thématiques pour faciliter la classification et la recherche.

**Exemples** :
```yaml
tags: ["governance", "methodology"]
tags: ["security", "authentication", "backend"]
tags: ["frontend", "nuxt", "vue", "ux"]
tags: []  # Aucun tag (valide)
```

**Bonnes pratiques** :
- ✅ Utiliser 2 à 5 tags par document
- ✅ Privilégier des tags courts et descriptifs
- ✅ Utiliser kebab-case pour tags composés : `docs-first`, `tech-stack`
- ❌ Éviter la prolifération de tags similaires

**Tags courants dans Relinium** :
- Domaines : `governance`, `security`, `architecture`, `infrastructure`
- Technologies : `backend`, `frontend`, `database`, `auth`
- Phases : `exploration`, `planning`, `implementation`, `review`

---

### `links` (Liens inter-documents)

**Type** : Objet avec propriétés

Structure de liens pour tracer les dépendances entre documents.

**Structure** :
```yaml
links:
  cites: []          # Documents cités par celui-ci
  cited_by: []       # Documents qui citent celui-ci
  supersedes: []     # Documents remplacés par celui-ci
  superseded_by: []  # Document qui remplace celui-ci
```

#### `cites` (Citations)

Documents référencés par le document actuel.

**Exemples** :
```yaml
links:
  cites: ["ADR-0001"]                    # Cite un ADR
  cites: ["ADR-0001", "RFC-002"]        # Cite plusieurs docs
  cites: ["ADR-0001", "OBS-0003", "RFC-005"]  # Citations mixtes
```

#### `cited_by` (Cité par)

Documents qui citent le document actuel. Généralement **généré automatiquement** par le Registry.

**Exemple** :
```yaml
links:
  cited_by: ["RFC-003", "ADR-0005", "OBS-0007"]
```

#### `supersedes` (Remplace)

Documents que le document actuel remplace ou rend obsolètes.

**Exemple** :
```yaml
# Dans ADR-0010
links:
  supersedes: ["ADR-0001"]  # ADR-0010 remplace ADR-0001
```

**Usage** : Utilisé quand une nouvelle décision annule une ancienne.

#### `superseded_by` (Remplacé par)

Document qui remplace le document actuel.

**Exemple** :
```yaml
# Dans ADR-0001 (ancien)
status: "Supersédé"
links:
  superseded_by: ["ADR-0010"]  # Remplacé par ADR-0010
```

**Note** : Quand un document est supersédé, son statut doit passer à "Supersédé".

---

## Exemples par type de document

### ADR (Architecture Decision Record)

#### ADR Accepté

```markdown
---
id: "ADR-0001"
type: "ADR"
status: "Accepté"
date: "2025-01-03"
author: "Équipe Relinium Genesis"
version: "1.0"
tags: ["governance", "methodology", "docs-first"]
links:
  cited_by: ["RFC-001", "RFC-002"]
---

# ADR-0001 – Repo Driven by Docs-First

Contenu du document...
```

#### ADR en Discussion

```markdown
---
id: "ADR-0002"
type: "ADR"
status: "En discussion"
date: "2025-01-04"
author: "Équipe Backend"
version: "0.9"
tags: ["backend", "framework", "django"]
links:
  cites: ["RFC-001", "OBS-0001"]
---

# ADR-0002 – Choix de Django comme framework backend

Contenu du document...
```

#### ADR Supersédé

```markdown
---
id: "ADR-0001"
type: "ADR"
status: "Supersédé"
date: "2025-01-03"
author: "Équipe Relinium Genesis"
version: "1.0"
tags: ["governance", "methodology"]
links:
  superseded_by: ["ADR-0015"]
  cited_by: ["RFC-001", "RFC-002"]
---

# ADR-0001 – Ancienne approche (Supersédé)

Ce document a été remplacé par ADR-0015.
```

---

### RFC (Request For Comments)

#### RFC en Discussion

```markdown
---
id: "RFC-001"
type: "RFC"
status: "En discussion"
date: "2025-01-03"
author: "Équipe Relinium Genesis"
version: "1.0"
tags: ["architecture", "stack", "backend", "frontend"]
links:
  cites: ["ADR-0001"]
---

# RFC-001 – Choix de stack initiale

Contenu de la proposition...
```

#### RFC Acceptée

```markdown
---
id: "RFC-002"
type: "RFC"
status: "Accepté"
date: "2025-01-05"
author: "Équipe Architecture"
version: "2.0"
tags: ["backend", "scoring", "matrix"]
links:
  cites: ["OBS-0001", "OBS-0002"]
---

# RFC-002 – Matrice de scoring backend

Cette RFC a été acceptée et a généré ADR-0003.
```

---

### OBS (Observation)

#### Observation Ouverte

```markdown
---
id: "OBS-0001"
type: "OBS"
status: "Ouvert"
date: "2025-01-03"
author: "Équipe Relinium Genesis"
version: "1.0"
tags: ["backend", "composants", "inventaire"]
links:
  cited_by: ["RFC-002"]
---

# OBS-0001 – Inventaire des composants backend

Phase d'observation en cours...
```

#### Observation Synthétisée

```markdown
---
id: "OBS-0002"
type: "OBS"
status: "Synthétisé"
date: "2025-01-04"
author: "Équipe Testing"
version: "1.1"
tags: ["testing", "benchmarks", "results"]
---

# OBS-0002 – Résultats des tests initiaux

Synthèse des observations collectées...
```

---

### POC (Proof of Concept)

#### POC Complété

```markdown
---
id: "POC-0001"
type: "POC"
status: "Complete"
date: "2025-01-04"
author: "Dev Team"
version: "1.0"
tags: ["auth", "keycloak", "security"]
---

# POC-0001 – Authentification avec Keycloak

Résultats du prototype...
```

#### POC Échoué

```markdown
---
id: "POC-0005"
type: "POC"
status: "Failed"
date: "2025-01-06"
author: "Lab Team"
version: "1.0"
tags: ["storage", "couchdb", "sync"]
---

# POC-0005 – Synchronisation CouchDB

Analyse de l'échec et leçons apprises...
```

---

### SPRINT_DOC (Document de Sprint)

#### Sprint en Cours

```markdown
---
id: "SPRINT_DOC-0001"
type: "SPRINT_DOC"
status: "En cours"
date: "2025-01-05"
author: "Équipe Relinium Genesis"
version: "1.0"
tags: ["ssot", "metadata", "sprint"]
---

# Sprint SSOT v1.0

Plan et suivi du sprint...
```

---

## Statuts et cycles de vie

### ADR (Architecture Decision Record)

**Statuts** : `Proposition` → `En discussion` → `Accepté` | `Rejeté` → `Supersédé`

| Statut | Emoji | Description |
|--------|-------|-------------|
| **Proposition** | 📝 | ADR soumis, en attente de discussion |
| **En discussion** | 💬 | ADR en cours de revue et débat |
| **Accepté** | ✅ | ADR validé et appliqué |
| **Rejeté** | ❌ | ADR refusé avec justification |
| **Supersédé** | 🔄 | ADR remplacé par un nouveau |

**Transitions logiques** :
```
Proposition
    ↓
En discussion
    ↓
Accepté ou Rejeté
    ↓
[Supersédé] (optionnel, seulement pour Accepté)
```

---

### RFC (Request For Comments)

**Statuts** : `Ébauche` → `En discussion` → `Mature` → `Accepté` | `Abandonné`

| Statut | Emoji | Description |
|--------|-------|-------------|
| **Ébauche** | ✏️ | RFC en cours de rédaction |
| **En discussion** | 💬 | RFC ouverte aux commentaires |
| **Mature** | 📊 | RFC complète, prête pour décision |
| **Accepté** | ✅ | RFC validée, génère un ADR |
| **Abandonné** | 🗑️ | RFC abandonnée avec raison |

---

### OBS (Observation)

**Statuts** : `Ouvert` → `En observation` → `Synthétisé` → `Archivé`

| Statut | Emoji | Description |
|--------|-------|-------------|
| **Ouvert** | 🔍 | Observation initiale, collecte de données |
| **En observation** | 👁️ | Observation active, analyse en cours |
| **Synthétisé** | 📋 | Observation complète avec conclusions |
| **Archivé** | 📦 | Observation close, référence historique |

---

### POC (Proof of Concept)

**Statuts** : `Planned` → `In Progress` → `Complete` | `Failed`

| Statut | Emoji | Description |
|--------|-------|-------------|
| **Planned** | 📋 | POC planifié, non démarré |
| **In Progress** | 🔨 | POC en cours d'implémentation |
| **Complete** | ✅ | POC terminé avec résultats |
| **Failed** | ❌ | POC échoué avec analyse |

---

### SPRINT_DOC (Document de Sprint)

**Statuts** : `Planifié` → `En cours` → `Terminé` → `Certifié`

| Statut | Emoji | Description |
|--------|-------|-------------|
| **Planifié** | 📋 | Sprint planifié, non démarré |
| **En cours** | 🏃 | Sprint actif, en exécution |
| **Terminé** | ✓ | Sprint complété, en attente validation |
| **Certifié** | 🏆 | Sprint validé et certifié |

---

## Bonnes pratiques

### 1. Cohérence et conventions

✅ **À faire** :
- Utiliser le même format de date partout (ISO 8601)
- Adopter une convention pour les auteurs (équipe vs personne)
- Maintenir une liste de tags cohérente
- Suivre les cycles de vie définis

❌ **À éviter** :
- Mélanger différents formats de dates
- Créer des tags trop similaires (`backend` vs `back-end` vs `Backend`)
- Sauter des statuts dans le cycle de vie

---

### 2. Liens inter-documents

✅ **À faire** :
- Toujours citer les documents qui influencent vos décisions
- Mettre à jour les liens quand un document est supersédé
- Vérifier que les IDs référencés existent

❌ **À éviter** :
- Créer des références circulaires (A supersedes B, B supersedes A)
- Référencer des documents qui n'existent pas

---

### 3. Versioning

✅ **À faire** :
- Commencer à `0.9` pour les ébauches
- Passer à `1.0` quand le document est stable
- Incrémenter `MAJOR` pour restructuration
- Incrémenter `MINOR` pour ajouts significatifs

❌ **À éviter** :
- Sauter des versions (1.0 → 3.0 sans raison)
- Utiliser des versions non-numériques

---

### 4. Tags

✅ **À faire** :
- 2-5 tags par document (sweet spot)
- Tags génériques + tags spécifiques
- Kebab-case pour cohérence

❌ **À éviter** :
- Trop de tags (> 7) = bruit
- Tags trop génériques seuls (`doc`, `file`)
- Duplication de tags dans différentes casses

---

## Validation

### Validation manuelle

Vérifiez que :
1. ✅ Les 4 champs obligatoires sont présents
2. ✅ Le format YAML est valide
3. ✅ L'ID correspond au type
4. ✅ Le statut est valide pour le type
5. ✅ La date est au format ISO 8601
6. ✅ Les IDs référencés existent

### Validation automatique

Le projet Relinium utilise un script de validation qui vérifie automatiquement :

```bash
# Validation locale
python scripts/validate_frontmatter.py

# Validation en CI
# Exécutée automatiquement à chaque commit
```

Le validateur vérifie :
- Structure YAML correcte
- Présence des champs obligatoires
- Cohérence des types et formats
- Validité des liens inter-documents
- Respect des patterns (dates, IDs, versions)

---

## FAQ

### Puis-je ajouter des champs personnalisés ?

Non, le schéma est **fermé** (`additionalProperties: false`). Seuls les champs définis sont autorisés. Cela garantit la cohérence et la validabilité automatique.

Si vous avez besoin d'un nouveau champ, proposez-le via une RFC.

---

### Que faire si je me trompe d'ID ?

Les IDs sont **permanents**. Si vous vous trompez :
1. Ne changez PAS l'ID (cela casse les références)
2. Créez un nouveau document avec le bon ID
3. Utilisez `supersedes` pour lier l'ancien au nouveau
4. Marquez l'ancien comme "Supersédé"

---

### Comment numéroter un nouveau document ?

Prenez le **dernier numéro utilisé** pour ce type + 1.

Exemple :
```bash
# Vérifier les ADR existants
ls docs/03-architecture/decisions/
# → ADR-0001, ADR-0002, ADR-0003

# Nouveau ADR
id: "ADR-0004"
```

---

### Dois-je mettre à jour `cited_by` manuellement ?

**Non**, le champ `cited_by` est généralement **généré automatiquement** par le Registry (S4). Vous pouvez le maintenir manuellement si vous le souhaitez, mais il sera écrasé lors de la génération du registre.

Concentrez-vous sur `cites` qui indique les documents que vous référencez.

---

### Quand mettre à jour la date ?

Mettez à jour `date` lors de **modifications majeures** :
- Changement de statut
- Ajout de sections importantes
- Restructuration du contenu

Ne la mettez PAS à jour pour :
- Corrections de typos
- Reformatages mineurs
- Ajouts de précisions mineures

---

### Peut-on avoir plusieurs auteurs ?

Le champ `author` est une chaîne. Pour plusieurs auteurs :

```yaml
# Option 1 : Liste séparée par virgule
author: "Alice Dupont, Bob Martin"

# Option 2 : Nom d'équipe
author: "Équipe Backend"

# Option 3 : Auteur principal + contributeurs dans le corps
author: "Alice Dupont"
# Et dans le document : "Contributeurs: Bob, Charlie"
```

---

### Que faire en cas d'erreur de validation ?

Le validateur vous indiquera l'erreur précise :

```
ERROR in docs/03-architecture/decisions/ADR-0001.md:
  - Missing required field: 'date'
  - Invalid status 'WIP' for type 'ADR'
  - ID format mismatch: 'ADR-001' should be 'ADR-0001'
```

Corrigez les erreurs signalées et relancez la validation.

---

## Références

- **Schéma YAML** : [`document_schema_v1.yaml`](./document_schema_v1.yaml)
- **JSON Schema** : [`document_schema_v1.json`](./document_schema_v1.json)
- **Script de validation** : `scripts/validate_frontmatter.py` (S3)
- **Registre documentaire** : `docs/_registry/registry.yaml` (S4)

---

## Changelog

### Version 1.0.0 (2025-01-05)

- Version initiale du guide
- Documentation complète des 4 champs obligatoires
- Exemples pour les 5 types de documents
- Bonnes pratiques et FAQ

---

> _"Les métadonnées ne sont pas du bruit, elles sont la carte du territoire."_  
> — Relinium Genesis
