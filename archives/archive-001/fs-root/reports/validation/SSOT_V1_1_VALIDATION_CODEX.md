---
id: "VAL-SSOT-V1_1-0001"
id_root: "VAL-SSOT-V1_1-0001"
version: "1.0"
type: "validation"
status: "Active"
title: "Validation indépendante Codex – SSOT v1.1 (Migration + S6-A + Snapshot)"
scope: "organizational"
pattern: "validation"
decision_type: "assessment"
created_at: "2025-11-06T08:59:25Z"
authors:
  - id: "codex"
    role: "auditor"
roles:
  - name: "Auditor"
    actor: "Codex"
links:
  relates_to:
    - "ADR-0001"
    - "RFC-0001"
    - "RFC-0004"
    - "OBS-0001"
    - "OBS-0002"
    - "OBS-0003"
  evidence:
    - "SPRINT_DOC-0043"
    - "SPRINT_DOC-0048"
    - "SPRINT_DOC-0050"
self_hash: sha256:656b65fb69a009bcc565ec897b8de3e9cd39edb547b00502f7d9342964dcc6e2
---

## 1️⃣ Contexte & périmètre
- Validation exécutée le 2025-11-06T08:59:25Z (UTC).
- Commit contrôlé : `1073f0c8d2e8e2d70f1b053b72d8db2faa811214`.
- Rapports analysés :
  - `docs/sprints/SSOT-v1.1/02-evidence/MIGRATION_EXECUTION_REPORT.md`
  - `reports/audits/SSOT_V1_1_REGISTRY_AUDIT.md`
  - `docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_SNAPSHOT_20251106_0846.md`
- Périmètre matériel : `docs/03-architecture/**`, `docs/_registry/registry_v1.1.yaml`, `docs/sprints/SSOT-v1.1/02-evidence/*`, `docs/sprints/SSOT-v1.1/03-validation/*`, `reports/audits/*`.
- Méthode : lecture seule, recalcul SHA256 de 18 artefacts, confrontation point par point des affirmations de Cline avec l’état réel du dépôt.

## 2️⃣ Concordances Cline ↔ Réalité

| # | Déclaration Cline | Référence Cline | Constat Codex |
|---|-------------------|-----------------|---------------|
| 1 | 2 documents migrés via succession certifiée (ADR-0001, RFC-001) | `docs/sprints/SSOT-v1.1/02-evidence/MIGRATION_EXECUTION_REPORT.md:16-90` | Successeurs présents avec `id_root` et `previous_hash` corrects (`docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first-v2.md:2-15`, `docs/03-architecture/rfcs/RFC-001-choix-stack-initiale-v2.md:2-15`). |
| 2 | Aucune modification des originaux (hashs identiques) | `docs/sprints/SSOT-v1.1/02-evidence/MIGRATION_EXECUTION_REPORT.md:95-119` | SHA256 recalculés pour ADR-0001, RFC-001 et RFC-002 = `3c8d…`, `2244…`, `7758…`, identiques aux valeurs consignées (`docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml:12-45`). |
| 3 | Registre v1.1 créé avec les 2 lignées pilotes | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS.yaml:37-48` | `docs/_registry/registry_v1.1.yaml:10-65` expose bien les lignées ADR-0001 et RFC-0001, incluant `previous_hash` et statuts. |
| 4 | Taux de conformité v1.1 = 22,2 % (2/9 documents) | `reports/audits/SSOT_V1_1_REGISTRY_AUDIT.md:20-28` | Inventaire réel = 9 docs (7 v1.0 + 2 v1.1). Calcul = 2/9 = 22,2 %. |
| 5 | Successeurs comportent tous les champs obligatoires v1.1 | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS.yaml:69-105` | Frontmatters v2 incluent `id_root`, `previous_hash`, `scope`, `pattern`, `roles` (cf. fichiers v2). |

## 3️⃣ Divergences Cline ↔ Réalité

| Type | Fichier(s) | Description | Impact |
|------|------------|-------------|--------|
| `hash_mismatch` | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml:83-92` | Manifest affirme `sha256:56b14581…` pour `SSOT_V1_1_PROGRESS.yaml` et `sha256:d2e7fdc8…` pour `SSOT_V1_1_HASHES.yaml`, tandis que les recalculs donnent `42a1e5b0…` et `0644fd04…`. | Axe cryptographique : preuves S6-SNAPSHOT obsolètes. |
| `hash_mismatch` | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml:118-122` | Le manifest publie `sha256:3459b1…` pour lui-même alors que le fichier actuel vaut `477ba35f…`. | Axe cryptographique : impossibilité de re-vérifier l’empreinte du manifest. |
| `missing_hash` | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml:66-85` & `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS.yaml:95` | La DoD « Hashs consignés » est marquée ✅, mais les entrées `plan` et `progress_file` restent sur `sha256:(to_be_calculated)`. | Axe cryptographique + gouvernance : preuve incomplète malgré succès déclaré. |
| `missing_in_registry` | `docs/_registry/registry_v1.1.yaml:66-84` | RFC-004 n’apparaît ni dans `lineages` ni dans `pending_migration`, alors qu’elle existe dans `docs/03-architecture/rfcs`. | Axe registre : trajectoire du protocole d’alignement invisible. |
| `id_incoherence` | `docs/03-architecture/rfcs/RFC-001-choix-stack-initiale.md:2` vs `...-v2.md:2` | L’original conserve l’ID `RFC-001` (3 chiffres) tandis que le successeur déclare `id_root: RFC-0001`. Lignée rompue au regard du schéma v1.1. | Axe structurel/documentaire. |
| `partial_metadata` | `docs/_registry/registry_v1.1.yaml:74-84` | OBS-0001/0002/0003 listés en pending_migration sans hash ni statut. | Axe registre : absence de preuve d’intégrité pour 3 racines. |
| `declared_but_absent` | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS.yaml:95-105` | La métrique « Hashs consignés » est annoncée comme achevée alors que plusieurs hashs manquent (voir ci-dessus). | Qualité des rapports : fiabilité DoD remise en cause. |
| `hash_mismatch` | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml:90-94` | Le manifest annonce `sha256:65c009d8…` pour `registry_v1.1.yaml` (bon), mais le même bloc associe `progress_tracker` au mauvais hash (cf. 1er point). | Axe cryptographique (redondance explicite). |

_Total des déclarations vérifiées : 9 · Concordances : 5 · Divergences : 4._

## 4️⃣ Analyse de conformité SSOT v1.1

### Axe structurel — Score 0.40
Deux lignées (ADR-0001, RFC-0001) sont documentées avec succession complète (`previous_hash`, `supersedes`). Les cinq autres racines identifiées (RFC-0002, RFC-0004, OBS-0001/0002/0003) existent physiquement mais ne sont ni migrées ni décrites finement dans le registre. La persistance d’un mix `RFC-001` / `RFC-0001` rompt la continuité nominale attendue par le schéma v1.1.

### Axe cryptographique — Score 0.58
14 artefacts ont été rehashés : 10 concordances (documents sources, successeurs, registre, rapports) et 4 écarts (progress tracker, hash registry, snapshot manifest, champ auto-hash du manifest). Les placeholders `sha256:(to_be_calculated)` contredisent la DoD et empêchent toute vérification automatisée. Les preuves produites le 2025-11-06 ne sont donc plus auto-suffisantes.

### Axe registre — Score 0.35
`registry_v1.1.yaml` ne trace que 2 lignées et laisse `pending_migration` sans hash pour 3 entrées. RFC-004 est totalement absente alors qu’elle fonde le protocole de succession. Les hashs des versions v2 sont encore marqués `to_be_calculated`. Ce registre constitue une base de travail, pas encore un référentiel complet.

### Axe documentaire — Score 0.45
Les successeurs v1.1 respectent bien le schéma (frontmatters complets, rôles, scope/pattern). Les documents v1.0 restent valides au format v1.0 mais n’intègrent pas les champs de lignée. L’incohérence d’ID sur la lignée RFC et l’absence de `id_root`/`previous_hash` pour les autres racines limitent la navigation documentaire.

## 5️⃣ Score global & synthèse

| Axe | Score estimé | Commentaire court |
|-----|--------------|-------------------|
| Structure | 0.40 | 2 lignées certifiées sur ~5 attendues |
| Cryptographie | 0.58 | 10/14 hashs OK, preuves S6 partiellement obsolètes |
| Registre | 0.35 | Couverture incomplète, RFC-004 absente |
| Documentaire | 0.45 | Successeurs conformes, v1.0 encore hybrides |
| Global | **0.46** | Pilote cohérent mais preuves & registre à compléter |

Le SSOT v1.1 dispose bien de ses deux lignées pilotes conformes au RFC-004 : la succession cryptographique ADR/RFC fonctionne et aucune altération des originaux n’a été détectée. En revanche, l’écosystème d’évidence (hash registry, manifest snapshot) n’a pas été maintenu après création, ce qui fragilise la valeur de preuve du sprint. Le registre v1.1 reflète la vision pilote mais ignore encore la majorité des racines actives, dont RFC-004, pourtant normative.

## 6️⃣ Recommandations factuelles
1. Normaliser la lignée RFC : choisir un identifiant racine unique (`RFC-0001`) et aligner les frontmatters + registre.
2. Ajouter RFC-004 et les 3 OBS à `registry_v1.1.yaml` avec hash, statut, scope/pattern au minimum.
3. Recalculer et republier les hashs SHA256 pour `SSOT_V1_1_PROGRESS.yaml`, `SSOT_V1_1_HASHES.yaml`, `SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml` et `SSOT_V1_1_PILOT_PLAN.md`, puis rafraîchir les manifests associés.
4. Compléter les champs `hash` des versions v2 dans le registre (`hash: sha256:e061…` et `sha256:263f…`).
5. Étendre `pending_migration` avec les métadonnées cryptographiques (hash + statut) pour OBS-0001/0002/0003 et toute nouvelle lignée identifiée.
6. Documenter explicitement les divergences dans un prochain rapport sprint pour lever l’ambiguïté sur les DoD déjà cochées.

## 7️⃣ Proposition de patch registre (à exécuter par Cline)
```yaml
lineages:
  - id_root: "RFC-0004"
    title: "Protocole de mise en cohérence documentaire"
    scope: "governance"
    pattern: "reflection"
    versions:
      - id: "RFC-0004"
        status: "Active"
        version: "1.0.0"
        date: "2025-05-11"
        file_path: "docs/03-architecture/rfcs/RFC-004-alignment-protocol.md"
        hash: "sha256:f70651b55c2704ba5976b168f3d9b63ef001138b1f0a9670f95988a902ecd5ca"
```
