---
id: "SPRINT_DOC-0052"
id_root: "SPRINT_DOC-0052"
type: "SPRINT_DOC"
status: "Planifié"
date: "2025-11-07"
author: "Cline"
version: "1.0"
scope: "organizational"
pattern: "rule"
title: "SSOT v1.1 — Align Phase 2 Plan"
tags:
  - "ssot"
  - "v1.1"
  - "alignment"
links:
  implements:
    - "SPRINT_DOC-0040"
  cites:
    - "SPRINT_DOC-0042"
    - "SPRINT_DOC-0043"
    - "SPRINT_DOC-0050"
    - "SPRINT_DOC-0053"
self_hash: sha256:dcbad26dbbc8ac7dfb9525324e2696ff85b81c86c1787dd9bff5c74ea8ed436f
---

# Sprint S9-ALIGN — Phase 2 : Exploration & planification du registre complet (read-only)

## 🎯 Objectif

Cartographier exhaustivement l’écart entre l’état actuel du registre v1.1_v3 et l’ensemble des documents normatifs du SSOT (docs/ + reports/) puis définir la stratégie de mise en conformité par succession (RFC-004), sans modifier aucun fichier existant. La mise en œuvre (création de `registry_v1.1_v4.yaml` et des successeurs) aura lieu en Phase 2-bis.

## 🔎 Contexte (S8-STRICT, S9-ALIGN P1)

- S8-STRICT (triple-check strict) opérationnel: hash / registry / schema.
- Phase 1 (S9-ALIGN P1) livrée: `registry_v1.1_v3.yaml` intégrant une large couverture via `pending_migration` pour assurer REG-COVERAGE strict sur le périmètre scanné.
- Les lignées fondatrices (ADR-0001, RFC-0001) et les familles SPRINT_DOC (0001..0010) sont structurées avec statuts et previous_hash.
- Les éléments restants (RFC-004, OBS-0001..0003, observatory, reports, sprints SSOT-v1.0) sont référencés dans `pending_migration`.

Référence exécution (local):
- `python scripts/ssot_registry_check.py --strict --registry-file docs/_registry/registry_v1.1_v3.yaml --scan-roots docs/03-architecture docs/observatory docs/sprints/SSOT-v1.1 reports/analysis reports/validation`
- Résultat: warnings=0, errors=0 (REG-COVERAGE OK sur le périmètre scanné)

## 🗺️ Carte des écarts REG-COVERAGE (vue Phase 2)

- Couverture stricte: ✅ aucune absence (uncovered=0) sur les racines scannées.
- Couverture “pending-only” (à promouvoir en lignées): ≈ 50–55 éléments, dont:
  - RFC-004 (alignment protocol)
  - OBS-0001, OBS-0002, OBS-0003
  - Observatoire: OBS-CONFORMITY-0001, OBS-GOVERNANCE-0001, OBS-SCHEMA-0001, OBS-SSOT-EXPLORATION, et documents SSOT_* (foundations/metadata/scenarios)
  - Reports: analysis (TRUTHKEEPER, 100PCT_EXPLORATION), validation (VALIDATION_CODEX, SELFCRITIQUE_CLINE, MIRROR), audits
  - Sprints SSOT-v1.0 (context/evidence/validation) et certains artefacts SSOT-v1.1

### Classification proposée des écarts
- REG-MISSING-LINEAGE: documents présents uniquement en `pending_migration` (aucune lignée créée).
- REG-MISSING-VERSION: lignée attendue mais première version non matérialisée (au moins v1 Active).
- REG-MISSING-META: normalisation à faire lors du passage en lignée (hash réels, status cohérent, id_root, previous_hash si succession).

## 🔄 Stratégie de succession pour `registry_v1.1_v4.yaml` (Phase 2-bis)

- Point de départ:
  - `previous_hash` de v4 = SHA256 de `docs/_registry/registry_v1.1_v3.yaml`.
- Enrichissement de lignées (exemples cibles):
  - RFC-004 → lignée `RFC-0004`, version v1 (Active), file_path: `docs/03-architecture/rfcs/RFC-004-alignment-protocol.md`.
  - OBS-0001..0003 → lignées `OBS-0001..0003`, version v1 (Active), file_path correspondants.
  - Reports critiques (TRUTHKEEPER, 100PCT_EXPLORATION, VALIDATION_CODEX, SELFCRITIQUE_CLINE, MIRROR, AUDIT) → v1 (Active).
  - Sprints SSOT-v1.1 → harmonisation des familles SPRINT_DOC (v2/v3 existantes), statuts cohérents.
  - Observatoire et sprints SSOT-v1.0 → lignée v1 en statut Deprecated/Archived (sans réécriture du contenu).
- Règles d’or (RFC-004):
  - Immutabilité: aucun fichier existant n’est modifié; toute correction se fait via un successeur.
  - Hashs réels (sha256:...) systématiques; `previous_hash` requis pour chaque succession.
  - Statuts en accord avec le type (cf. document_schema_v1.1).

## 📌 Priorités de traitement Phase 2-bis

1) Cœur normatif: RFC-004, OBS-0001..0003 (création des lignées v1 Active).
2) Reports S9-ALIGN: TRUTHKEEPER, 100PCT_EXPLORATION, VALIDATION_CODEX, SELFCRITIQUE_CLINE, MIRROR, AUDIT (création des lignées v1 Active).
3) Sprints SSOT-v1.1: plans/evidence/validation (aligner les versions v2/v3 et statuts).
4) Observatoire et sprints SSOT-v1.0: création de lignées v1 en Deprecated/Archived.

## 🛠️ Plan de travail (Phase 2-bis — exécution)

- E1: Ajout des lignées RFC-0004 et OBS-0001..0003 (v1 Active).
- E2: Ajout des lignées pour tous les reports SSOT-v1.1 (v1 Active).
- E3: Ajout/alignement des lignées pour les sprints SSOT-v1.1 (v2/v3 consolidées, statuts cohérents).
- E4: Normalisation globale (status, hash réels, previous_hash), vérification stricte.

## ✅ Definition of Done — Phase 2 (planification)

- Tous les écarts “pending-only” identifiés et classés (REG-MISSING-LINEAGE / VERSION / META).
- Les documents cibles ont une lignée prévue (id_root & statut souhaité).
- La stratégie de succession vers `registry_v1.1_v4.yaml` est décrite, ordonnancée et prête à exécution.

## 📚 Références

- Registre courant: `docs/_registry/registry_v1.1_v3.yaml`
- Plans / rapports:
  - `reports/analysis/SSOT_V1_1_100PCT_PLAN.yaml`
  - `reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT*.md`
  - `reports/validation/SSOT_V1_1_ALIGN_PHASE1_CODEX.md`
- Schéma: `docs/01-genesis/document_schema_v1.1.yaml`
- Protocole: `docs/03-architecture/rfcs/RFC-004-alignment-protocol.md`
