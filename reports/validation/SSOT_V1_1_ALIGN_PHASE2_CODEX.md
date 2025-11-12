---
id: "VAL-ALIGN-PHASE2-SSOT-V1_1-0001"
id_root: "VAL-ALIGN-PHASE2-SSOT-V1_1-0001"
version: "1.0"
type: "validation"
status: "Active"
title: "Validation Codex — SSOT v1.1 Align Phase 2-bis (registry v4)"
scope: "organizational"
pattern: "validation"
decision_type: "assessment"
created_at: "2025-11-07T12:44:21Z"
authors:
  - id: "codex"
    role: "auditor"
roles:
  - name: "Auditor"
    actor: "Codex"
links:
  relates_to:
    - "REGISTRY-SSOT-V1_1-0004"
    - "RFC-004"
    - "reports/analysis/SSOT_V1_1_100PCT_PLAN.yaml"
  evidence:
    - "docs/_registry/registry_v1.1_v4.yaml"
    - "docs/_registry/registry_v1.1_v3.yaml"
    - "SPRINT_DOC-0054"
    - "reports/analysis/SSOT_V1_1_100PCT_PLAN.yaml"
    - "reports/validation/SSOT_V1_1_VALIDATION_CODEX.md"
self_hash: sha256:d4fb2df16891c7e1722c8ce7b97e08d858f613da1bc2b37edb82ac578745ea87
---

## 1️⃣ Contexte & méthode
- Audit exécuté le 2025-11-07T12:44:21Z sur le commit `1073f0c8d2e8e2d70f1b053b72d8db2faa811214`.
- Entrées mandatées : registre v3/v4, plan 100 % couverture, rapport Align Phase 2 et historique Codex.
- Commandes : `sha256sum`, scripts Python de comparaison, puis `python scripts/ssot_registry_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v4.yaml` (retour 0).

## 2️⃣ Succession cryptographique
- `previous_hash` du registre v4 (`sha256:3d2fb6…`) égale au SHA256 recalculé de `registry_v1.1_v3.yaml`, ce qui verrouille la chaîne v3→v4 (`docs/_registry/registry_v1.1_v4.yaml:709`, `docs/_registry/registry_v1.1_v3.yaml` hash).
- Suppression temporaire de la ligne `self_hash:` puis recalcul donne `sha256:630eac…`, identique à la valeur publiée (`docs/_registry/registry_v1.1_v4.yaml:710`).
- Diff structurelle entre v3 et v4 : les 12 lignées historiques sont reproduites à l’octet près (comparaison YAML profonde, aucune divergence détectée).

## 3️⃣ Promotion des pending & artefacts Phase 2
- `pending_migration` listait 52 artefacts en v3 (`docs/_registry/registry_v1.1_v3.yaml:320`), la structure est vide en v4 (`docs/_registry/registry_v1.1_v4.yaml:708`).
- 46 entrées pending se retrouvent dans de nouvelles lignées actives (`id_root` inédits) tandis que 6 correspondaient déjà à des lignées existantes (ex : SPRINT_DOC-0005/0006). Les scripts de rapprochement hash↔fichier n’ont relevé aucun reste orphelin.
- Trois artefacts spécifiques à la phase 2-bis (plan, evidence, validation) sont promus comme lignées SPRINT_DOC-0052 à 0054, toutes en `status: Active`, `version: '1.0'`, sans `previous_hash` et avec hash final (`docs/_registry/registry_v1.1_v4.yaml:684-706`).
- Compte final : 61 lignées (12 historiques + 49 nouvelles). Les 46 promotions attendues correspondent exactement aux entrées pending identifiées dans `SSOT_V1_1_ALIGN_PHASE2_VALIDATION.md:19-52`; l’écart de +3 provient des artefacts Phase 2 ajoutés hors backlog.

## 4️⃣ Métadonnées & schéma v1.1
- Le front matter du registre expose bien `id/id_root/version/type/status/pattern/scope/decision_type/previous_hash/self_hash` et leurs rôles/auteurs (`docs/_registry/registry_v1.1_v4.yaml:1-29`).
- Chaque nouvelle lignée possède un `id_root` unique (61 racines sans collision), une unique version `v1.0`/`1.0.0`, `status: Active`, aucun `previous_hash` et un SHA256 réel (analyse automatique sur 49 nouvelles entrées).
- Les lacunes signalées par le plan 100 % couverture (RFC-004 + OBS-0001/0002/0003 absents du registre) sont désormais comblées (`reports/analysis/SSOT_V1_1_100PCT_PLAN.yaml:24-42` vs `docs/_registry/registry_v1.1_v4.yaml:316-355`).

## 5️⃣ CI strict & garde-fous
- `python scripts/ssot_registry_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v4.yaml` retourne 0, validant schéma, unicité, hashs et champs obligatoires (`scripts/ssot_registry_check.py` logique CI).
- Aucun placeholder `sha256:(to_be_calculated)` ni statut invalide trouvés (`docs/_registry/registry_v1.1_v4.yaml` inspection exhaustive).

## 6️⃣ Scores & verdict

| Axe | Score | Éléments clés |
|-----|-------|---------------|
| succession_integrity | **1.00** | SHA256 v3 → `previous_hash` v4 concordants + `self_hash` revérifié. |
| registry_completeness | **1.00** | 52/52 pending migrés, 3 artefacts Phase 2 ajoutés, `pending_migration` vide. |
| metadata_conformity | **1.00** | Front matter v1.1 complet, 49 nouvelles lignées avec métadonnées conformes. |
| ci_gate_result | **1.00** | `ssot_registry_check --ci --strict` vert, aucune alerte bloquante. |

**Verdict : certified.** La succession cryptographique est cohérente, toutes les lignées pending sont actives avec hash final et le garde-fou CI strict passe en mode `--strict`.
