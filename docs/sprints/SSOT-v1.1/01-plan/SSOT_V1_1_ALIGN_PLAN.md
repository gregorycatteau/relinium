---
id: "PLAN-ALIGN-SSOT-V1_1-0001"
id_root: "PLAN-ALIGN-SSOT-V1_1-0001"
version: "1.1"
type: "sprint_plan"
pattern: "plan"
scope: "organizational"
decision_type: "plan"
status: "Active"
created_at: "2025-11-06T19:18:00+01:00"
updated_at: "2025-11-06T19:18:00+01:00"
authors:
  - name: "Cline"
    role: "AI Assistant"
participants:
  - name: "Human"
    role: "Validator"
workstream: "SSOT"
phase: "alignment"
priority: "critical"
tags:
  - "ssot"
  - "v1.1"
  - "alignment"
  - "succession"
  - "rfc-004"
  - "s9-align"
links:
  relates_to:
    - "EXPLORE-SSOT-V1_1-100PCT-0001"
    - "VAL-PROOF-SSOT-V1_1-0001"
    - "VAL-STRICT-SSOT-V1_1-0001"
  implements:
    - "RFC-004"
changelog:
  - version: "1.0.0"
    date: "2025-11-06T19:18:00+01:00"
    author: "Cline"
    changes: "Création initiale du plan S9-ALIGN"
self_hash: sha256:7aa808917facb9f667d014c8aaffed69746b37d18fedf8e502cc5882ec2ed6cf
---

# Sprint S9-ALIGN — Plan de mise en conformité du SSOT v1.1

## 🎯 Objectif

Remettre le SSOT v1.1 en **conformité complète** avec le pipeline strict S8, en respectant **strictement** le protocole de succession (RFC-004) :

> 🔴 **Aucun fichier existant n'est modifié**  
> 🟢 **Tout document impacté est superseded par un nouveau fichier successeur**

À la fin de S9-ALIGN, le pipeline S8-STRICT (triple-check hash/registry/schema en `--strict --ci`) doit passer **intégralement au vert** sur le périmètre visé.

## 📊 Contexte — Verdict S8-STRICT

L'exécution complète du triple-check strict révèle les écarts suivants :

### 1️⃣ ssot_hash_check.py --ci --strict

**Résultat :** ❌ Code de sortie 2 (erreurs critiques)

**Catégories d'écarts :**

- **SELF_HASH-DIVERGENCE** (7 fichiers) :
  - `docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_PROOF_EVIDENCE.md`
  - `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_STRICT_PLAN.md`
  - `reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT.md`
  - `reports/analysis/SSOT_V1_1_100PCT_EXPLORATION.md`
  - `reports/validation/SSOT_V1_1_VALIDATION_CODEX.md`
  - `reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE.md`
  - `reports/validation/SSOT_V1_1_MIRROR_CODEX.md`

- **HASH-PLACEHOLDER** (2 fichiers) :
  - `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PILOT_PLAN.md` : `sha256:(to_be_calculated)`
  - `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS.yaml` : `sha256:(to_be_calculated)`

- **HASH-DIVERGENCE** (1 fichier) :
  - `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml`

### 2️⃣ ssot_registry_check.py --ci --strict

**Résultat :** ❌ Code de sortie 2 (erreurs critiques)

**Catégories d'écarts :**

- **REG-HASH-PLACEHOLDER** :
  - `ADR-0001-v2` : `sha256:(to_be_calculated)`
  - `RFC-0001-v2` : `sha256:(to_be_calculated)`

- **REG-ID** invalide :
  - `RFC-001` déclaré avec `id_root=RFC-0001` (incohérence)

- **REG-COVERAGE** — 47 fichiers normatifs non couverts :
  - `RFC-004-alignment-protocol.md`
  - `OBS-CONFORMITY-0001`, `OBS-GOVERNANCE-0001`, `OBS-SCHEMA-0001`, `OBS-SSOT-EXPLORATION`
  - Tous les fichiers `SSOT_GOVERNANCE_*`, `SSOT_METADATA_*`, `SSOT_SCENARIOS_*`
  - Tous les sprints SSOT-v1.0 (README, plans, evidence, validation)
  - Tous les sprints SSOT-v1.1 récents (PILOT_PLAN, PROOF_*, STRICT_*, SNAPSHOT)
  - Tous les reports (`reports/analysis/*`, `reports/audits/*`, `reports/validation/*`)

- **PEND-STATUS-MISSING** et **PEND-HASH-MISSING** :
  - `OBS-0001`, `OBS-0002`, `OBS-0003` dans `pending_migration`

### 3️⃣ ssot_schema_check.py --ci --strict

**Résultat :** ❌ Code de sortie 2 (erreurs critiques)

**Catégories d'écarts :**

- **FM-ABSENT** (front matter absent) : ~26 fichiers dont :
  - Tous les fichiers observatory anciens (`OBS-SSOT-EXPLORATION`, `SSOT_GOVERNANCE_*`, etc.)
  - Tous les sprints SSOT-v1.0
  - Plusieurs fichiers SSOT-v1.1 (`PILOT_PLAN`, `README`, etc.)
  - `reports/audits/SSOT_V1_1_REGISTRY_AUDIT.md`

- **SCHEMA** (validation schéma v1.1 échouée) : ~27 fichiers dont :
  - Fichiers ADR, RFC, OBS avec front matter incomplet
  - Fichiers sprints SSOT-v1.1 (`PROOF_PLAN`, `PROOF_EVIDENCE`, etc.)
  - Reports avec front matter incomplet

**Synthèse globale :**
- ~60 fichiers présentent au moins une non-conformité critique
- ~10 fichiers nécessitent des corrections multiples (self_hash + schema + registry)
- 2 placeholders explicites à éliminer
- 1 registre v1.1 incomplet à enrichir par succession

## 🧬 Objectifs S9-ALIGN

1. **Corriger tous les self_hash divergents** par succession (7 fichiers)
2. **Éliminer tous les placeholders** par calcul réel (2 fichiers manifests + registry)
3. **Enrichir le registre v1.1** par succession pour couvrir :
   - RFC-004
   - OBS-CONFORMITY-0001, OBS-GOVERNANCE-0001, OBS-SCHEMA-0001, OBS-SSOT-EXPLORATION
   - Tous les reports (analysis, audits, validation)
   - Tous les sprints SSOT-v1.0 et SSOT-v1.1 manquants
4. **Compléter les front matter** par succession (schema v1.1) pour les fichiers SCHEMA
5. **Corriger les manifests** HASHES, PROGRESS, MANIFEST par succession
6. **Validation finale** : pipeline strict au vert (exit code 0) sur le périmètre traité

## 🔐 Principe fondamental : Succession RFC-004

**Règle d'or :** Aucun fichier existant du SSOT n'est modifié in-place.

### Mécanisme de succession

Pour tout fichier `X.md` ou `X.yaml` nécessitant une correction :

1. **Ne pas** modifier `X.md` / `X.yaml`
2. **Créer** un successeur `X-v2.md` / `X_v2.yaml` avec :
   - Contenu corrigé (self_hash fixé, placeholders remplacés, front matter complété)
   - Champ `previous_hash` = SHA256 de `X.md` / `X.yaml` (version précédente)
   - Champ `id_root` identique à la première version de la lignée
   - Lien `links.supersedes` vers l'ID du prédécesseur (si applicable)
3. **Recalculer** le `self_hash` du successeur (algorithme RFC-004)
4. **Mettre à jour** le registre v1.1 par succession :
   - Marquer `X.md` comme `Superseded`
   - Ajouter `X-v2.md` avec statut `Active`
   - Renseigner les hashs réels

### Convention de nommage des successeurs

| Type | Original | Successeur |
|------|----------|-----------|
| Markdown report | `SSOT_V1_1_TRUTHKEEPER_REPORT.md` | `SSOT_V1_1_TRUTHKEEPER_REPORT-v2.md` |
| Markdown sprint | `SSOT_V1_1_STRICT_PLAN.md` | `SSOT_V1_1_STRICT_PLAN-v2.md` |
| YAML manifest | `SSOT_V1_1_HASHES.yaml` | `SSOT_V1_1_HASHES_v2.yaml` |
| YAML progress | `SSOT_V1_1_PROGRESS.yaml` | `SSOT_V1_1_PROGRESS_v2.yaml` |
| Registry | `registry_v1.1.yaml` | `registry_v1.1_v2.yaml` |

## 📋 Catégories de corrections

### Catégorie A : Self-hash divergents (7 fichiers)

**Fichiers concernés :**
1. `docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_PROOF_EVIDENCE.md`
2. `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_STRICT_PLAN.md`
3. `reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT.md`
4. `reports/analysis/SSOT_V1_1_100PCT_EXPLORATION.md`
5. `reports/validation/SSOT_V1_1_VALIDATION_CODEX.md`
6. `reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE.md`
7. `reports/validation/SSOT_V1_1_MIRROR_CODEX.md`

**Action :**
- Pour chaque fichier : créer un successeur `-v2.md`
- Copier le contenu complet
- Recalculer le `self_hash` (algorithme RFC-004)
- Ajouter `previous_hash` = SHA256 de la version originale
- Préserver `id_root` identique

**Livrables :**
- 7 nouveaux fichiers `*-v2.md`
- Mise à jour du registre v1.1 (via successeur)

### Catégorie B : Placeholders explicites (2 fichiers)

**Fichiers concernés :**
1. `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PILOT_PLAN.md`
2. `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS.yaml`

**Action :**
- Créer des successeurs avec les placeholders remplacés par des SHA256 réels
- Pour PILOT_PLAN : recalculer le self_hash du document
- Pour PROGRESS : recalculer les hashs référencés

**Livrables :**
- `SSOT_V1_1_PILOT_PLAN-v2.md` (si front matter)
- `SSOT_V1_1_PROGRESS_v2.yaml`

### Catégorie C : Registre incomplet

**Fichier concerné :**
- `docs/_registry/registry_v1.1.yaml`

**Action :**
- Créer `registry_v1.1_v2.yaml` avec :
  - Toutes les entrées manquantes (RFC-004, OBS, reports, sprints)
  - Correction de l'ID RFC-001 → RFC-0001
  - Ajout des hashs réels pour ADR-0001-v2, RFC-0001-v2
  - Statuts complets pour pending_migration (OBS-0001/2/3)
  - `previous_hash` = SHA256 de `registry_v1.1.yaml`

**Nouvelles lignées à ajouter :**
- RFC-004 (Active)
- OBS-CONFORMITY-0001 (Active)
- OBS-GOVERNANCE-0001 (Active)
- OBS-SCHEMA-0001 (Active)
- OBS-SSOT-EXPLORATION (Deprecated)
- SSOT_GOVERNANCE_FOUNDATIONS (Deprecated)
- SSOT_METADATA_EXPLORATION (Deprecated)
- SSOT_SCENARIOS_EXPLORATION (Deprecated)
- Tous les sprints SSOT-v1.0 (Completed)
- Tous les sprints SSOT-v1.1 récents (Active)
- Tous les reports (Active)

**Livrables :**
- `registry_v1.1_v2.yaml`

### Catégorie D : Front matter incomplets (SCHEMA)

**Fichiers concernés :** ~27 fichiers

**Stratégie :**
- Pour les fichiers avec front matter incomplet : créer des successeurs avec front matter v1.1 complet
- Pour les fichiers sans front matter (FM-ABSENT) anciens (SSOT-v1.0, observatory anciens) : 
  - **Option 1 :** Les marquer comme Deprecated dans le registre sans créer de successeurs
  - **Option 2 :** Créer des successeurs avec front matter minimal si nécessaire pour la conformité

**Décision :** Option 1 pour les fichiers anciens, Option 2 pour les fichiers v1.1 actifs

**Livrables :**
- Successeurs pour les fichiers v1.1 avec SCHEMA (PROOF_PLAN, PROOF_EVIDENCE, etc.)
- Mise à jour du registre pour marquer les anciens comme Deprecated

### Catégorie E : Manifests (HASHES, MANIFEST)

**Fichiers concernés :**
1. `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml` (1 divergence)
2. `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml` (1 divergence)

**Action :**
- Créer des successeurs avec les hashs recalculés
- Ajouter `previous_hash` dans un bloc meta

**Livrables :**
- `SSOT_V1_1_HASHES_v2.yaml`
- `SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846_v2.yaml` (ou v2 selon convention)

## ⚙️ Méthodologie d'exécution

### Phase 1 : Préparation

1. **Identifier** tous les fichiers à corriger (fait via mesure initiale)
2. **Calculer** tous les SHA256 des versions actuelles (pour previous_hash)
3. **Préparer** les successeurs par catégorie

### Phase 2 : Corrections par succession (Catégories A-E)

Pour chaque catégorie (A, B, C, D, E) :

1. **Créer** les successeurs avec :
   - Contenu corrigé
   - `previous_hash` = SHA256 de la version précédente
   - `id_root` préservé
   - `self_hash` recalculé (Markdown)
   
2. **Vérifier** localement avec les scripts :
   ```bash
   python scripts/ssot_hash_check.py --print-self-hash <fichier-v2.md>
   ```

3. **Ne pas** supprimer les fichiers originaux (RFC-004 : immutabilité)

### Phase 3 : Registre v1.1 par succession

1. **Créer** `registry_v1.1_v2.yaml` avec :
   - Toutes les nouvelles lignées (RFC-004, OBS, reports, sprints)
   - Toutes les versions successeurs (v2) avec statut Active
   - Toutes les versions originales avec statut Superseded
   - Correction RFC-001 → RFC-0001
   - Hashs réels partout (élimination placeholders)
   - `previous_hash` = SHA256 de `registry_v1.1.yaml`

### Phase 4 : Validation triple-check strict

Exécuter le pipeline complet :

```bash
python scripts/ssot_hash_check.py --ci --strict
python scripts/ssot_registry_check.py --ci --strict
python scripts/ssot_schema_check.py --ci --strict --targets docs/ reports/
```

**Critère de succès :** Code de sortie 0 pour les 3 scripts sur le périmètre traité

### Phase 5 : Documentation

1. **Créer** `SSOT_V1_1_ALIGN_EVIDENCE.md` avec :
   - Pour chaque catégorie : liste des fichiers originaux → successeurs
   - Hashs avant/après
   - Confirmation `previous_hash` correct
   - Preuve de correction (self_hash recalculé, placeholders éliminés)

2. **Créer** `SSOT_V1_1_ALIGN_VALIDATION.md` avec :
   - Résultats du triple-check strict (tableaux)
   - Synthèse des corrections par lignée
   - Confirmation conformité pipeline S8-STRICT

## 📊 Périmètre et priorisation

### Périmètre S9-ALIGN (Phase 1)

**Priorité CRITIQUE** (bloquants pipeline) :
1. Catégorie A : Self-hash divergents (7 fichiers)
2. Catégorie B : Placeholders (2 fichiers)
3. Catégorie C : Registre incomplet
4. Catégorie E : Manifests divergents (2 fichiers)

**Priorité HAUTE** (conformité schéma) :
5. Catégorie D : Front matter incomplets SCHEMA pour fichiers v1.1 actifs (~15 fichiers)

**Priorité MOYENNE** (housekeeping) :
6. Catégorie D : Anciens fichiers FM-ABSENT → marquer Deprecated dans registre

### Périmètre exclu de S9-ALIGN

Les fichiers suivants sont **exclus** du périmètre S9-ALIGN car ils ne sont pas critiques :
- Fichiers SSOT-v1.0 sans front matter (seront Deprecated dans registre)
- Fichiers observatory anciens (seront Deprecated dans registre)
- Fichiers techniques non normatifs (README génériques, etc.)

## ✅ Definition of Done (DoD)

Le sprint S9-ALIGN est **terminé** lorsque :

### 1️⃣ Livrables obligatoires présents

- ✅ `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_ALIGN_PLAN.md` (ce fichier)
- ✅ `docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_ALIGN_EVIDENCE.md`
- ✅ `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_ALIGN_VALIDATION.md`

### 2️⃣ Corrections par succession validées

- ✅ 7 successeurs créés pour self-hash divergents (Catégorie A)
- ✅ 2 successeurs créés pour placeholders (Catégorie B)
- ✅ 1 successeur créé pour le registre v1.1 (Catégorie C)
- ✅ 2 successeurs créés pour manifests divergents (Catégorie E)
- ✅ Successeurs créés pour front matter incomplets v1.1 (Catégorie D)

### 3️⃣ Pipeline strict au vert

Exécution réussie (exit code 0) de :

```bash
python scripts/ssot_hash_check.py --ci --strict
python scripts/ssot_registry_check.py --ci --strict
python scripts/ssot_schema_check.py --ci --strict --targets docs/ reports/
```

**Sur le périmètre S9-ALIGN** :
- Aucune SELF_HASH-DIVERGENCE
- Aucun HASH-PLACEHOLDER
- Aucune HASH-DIVERGENCE
- Aucune REG-HASH-PLACEHOLDER
- Aucune REG-COVERAGE pour fichiers prioritaires
- Aucune SCHEMA pour fichiers v1.1 actifs

### 4️⃣ Registre v1.1_v2 complet

- ✅ RFC-004 ajouté (Active)
- ✅ OBS-CONFORMITY-0001, OBS-GOVERNANCE-0001, OBS-SCHEMA-0001 ajoutés (Active)
- ✅ Tous les reports ajoutés (Active)
- ✅ Tous les sprints SSOT-v1.1 récents ajoutés (Active)
- ✅ Anciens fichiers marqués Deprecated
- ✅ Hashs réels partout (placeholders éliminés)
- ✅ `previous_hash` correct

### 5️⃣ Documentation complète

- ✅ Evidence : hashs avant/après pour toutes les corrections
- ✅ Validation : résultats triple-check strict + tableaux
- ✅ Aucun document normatif modifié in-place (respect RFC-004)

## 🎯 Résultat attendu

À la fin de S9-ALIGN, le SSOT v1.1 sera **strictement conforme** au pipeline S8 :

- **Cryptographiquement prouvé** : tous les hashs cohérents
- **Historiquement fidèle** : aucune réécriture, seulement des successions
- **Exhaustivement couvert** : registre v1.1_v2 complet
- **Structurellement valide** : schéma v1.1 respecté

Le SSOT devient non seulement **strictement vérifiable**, mais aussi **historiquement fidèle**.

---

**Rappel philosophique :** S9-ALIGN ne "réécrit" pas le passé, il crée la version alignée qui en dérive, sous contrôle cryptographique. Le SSOT évolue par succession, jamais par mutation.
