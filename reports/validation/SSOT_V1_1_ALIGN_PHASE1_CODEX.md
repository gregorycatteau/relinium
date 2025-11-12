---
id: "VAL-ALIGN-PHASE1-SSOT-V1_1-0001"
id_root: "VAL-ALIGN-SSOT-V1_1-0001"
version: "v1"
type: "validation"
status: "Active"
title: "Validation Codex – S9-ALIGN Phase 1 (successeurs critiques)"
scope: "organizational"
pattern: "alignment_validation"
decision_type: "assessment"
created_at: "2025-11-06T21:34:47+00:00"
authors:
  - id: "codex"
    role: "auditor"
roles:
  - name: "Auditor"
    actor: "Codex"
links:
  relates_to:
    - "SPRINT-SSOT-V1_1-S9-ALIGN-PHASE1"
    - "SPRINT-SSOT-V1_1-S8-STRICT"
    - "EXPLORE-SSOT-V1_1-100PCT-0001"
  evidence:
    - "SPRINT_DOC-0040"
    - "SPRINT_DOC-0044"
    - "SPRINT_DOC-0010"
    - "docs/_registry/registry_v1.1.yaml"
    - "docs/_registry/registry_v1.1_v2.yaml"
    - "scripts/ssot_hash_check.py"
    - "scripts/ssot_registry_check.py"
self_hash: sha256:a86ef0133b5672c6d69a262b09688fbbc20ae39247a8702e83a0a0864c44845b
---

## Contexte & périmètre

Phase 1 de S9-ALIGN devait purger les divergences cryptographiques ciblées (catégories A, B, E) sans toucher aux originaux, puis sécuriser le pipeline strict S8 sur ce périmètre. J’ai contrôlé le plan, l’evidence et le rapport de validation annoncés, ainsi que les 11 paires original/successeur et les scripts stricts.

| Catégorie | Fichier original | Successeur détecté |
|-----------|------------------|--------------------|
| A | `docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_PROOF_EVIDENCE.md` | `docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_PROOF_EVIDENCE-v2.md` |
| A | `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_STRICT_PLAN.md` | `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_STRICT_PLAN-v2.md` |
| A | `reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT.md` | `reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT-v2.md` |
| A | `reports/analysis/SSOT_V1_1_100PCT_EXPLORATION.md` | `reports/analysis/SSOT_V1_1_100PCT_EXPLORATION-v2.md` |
| A | `reports/validation/SSOT_V1_1_VALIDATION_CODEX.md` | `reports/validation/SSOT_V1_1_VALIDATION_CODEX-v2.md` |
| A | `reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE.md` | `reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE-v2.md` |
| A | `reports/validation/SSOT_V1_1_MIRROR_CODEX.md` | `reports/validation/SSOT_V1_1_MIRROR_CODEX-v2.md` |
| B | `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PILOT_PLAN.md` | `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PILOT_PLAN-v2.md` |
| B | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS.yaml` | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS-v2.yaml` |
| E | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml` | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES-v2.yaml` |
| E | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml` | `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846-v2.yaml` |

## Vérification des successeurs Markdown (catégorie A + PILOT_PLAN)

| Fichier original | Successeur | previous_hash cohérent | self_hash correct | Placeholders | Statut |
|------------------|------------|------------------------|-------------------|--------------|--------|
| `SSOT_V1_1_PROOF_EVIDENCE.md` | `SSOT_V1_1_PROOF_EVIDENCE-v2.md` | OK | OK | Mentions textuelles « to_be_calculated » | Partiel – front matter v1.1 sans `roles` et `authors[]` |
| `SSOT_V1_1_STRICT_PLAN.md` | `SSOT_V1_1_STRICT_PLAN-v2.md` | OK | OK | Mentions textuelles | Partiel – front matter v1.1 sans `roles` et `authors[]` |
| `SSOT_V1_1_TRUTHKEEPER_REPORT.md` | `SSOT_V1_1_TRUTHKEEPER_REPORT-v2.md` | OK | OK | Aucun | Partiel – `self_hash` déclaré entre guillemets, rejeté par `ssot_hash_check.py --strict` |
| `SSOT_V1_1_100PCT_EXPLORATION.md` | `SSOT_V1_1_100PCT_EXPLORATION-v2.md` | OK | OK | Mentions textuelles | Partiel – `self_hash` entre guillemets, le strict check reste rouge |
| `SSOT_V1_1_VALIDATION_CODEX.md` | `SSOT_V1_1_VALIDATION_CODEX-v2.md` | OK | OK | Mentions textuelles | Partiel – `self_hash` entre guillemets, script strict en erreur |
| `SSOT_V1_1_SELFCRITIQUE_CLINE.md` | `SSOT_V1_1_SELFCRITIQUE_CLINE-v2.md` | OK | OK | Mentions textuelles | Partiel – `self_hash` entre guillemets, script strict en erreur |
| `SSOT_V1_1_MIRROR_CODEX.md` | `SSOT_V1_1_MIRROR_CODEX-v2.md` | OK | OK | Mentions textuelles | Partiel – `self_hash` entre guillemets, script strict en erreur |
| `SSOT_V1_1_PILOT_PLAN.md` | `SSOT_V1_1_PILOT_PLAN-v2.md` | OK | OK | Aucun | Partiel – `self_hash` entre guillemets et contenu resté « sprint pilote » |

Notes :
- Les 8 successeurs existent et tracent correctement `previous_hash`.
- Les recalculs conceptuels (`self_hash` hors ligne) sont justes, mais la présence de guillemets entraîne encore `SELF_HASH-DIVERGENCE` dans `scripts/ssot_hash_check.py` pour six documents.
- `SSOT_V1_1_PROOF_EVIDENCE-v2.md` et `SSOT_V1_1_STRICT_PLAN-v2.md` n’exposent pas les champs `roles`/`authors` attendus par le schéma v1.1.

## Vérification des manifests & PROGRESS (cat. B + E)

- `SSOT_V1_1_PROGRESS-v2.yaml` : `previous_hash` exact mais `self_hash` calculé ≠ déclaré (`sha256:5318349…` vs `sha256:17f996…`). Le contenu reste celui du sprint pilote (2 migrations ADR/RFC) sans refléter les 11 successeurs ALiGN, et rien ne référence les variantes `-v2`.
- `SSOT_V1_1_HASHES-v2.yaml` : `previous_hash` aligné, mais `self_hash` déclaré `sha256:42737f…` ne correspond pas au recalcul (`sha256:814494…`). Les blocs `successor_hashes` et `sprint_artifacts` ne couvrent que ADR-0001 / RFC-0001 et pointent toujours vers les artefacts d’origine (`SSOT_V1_1_PILOT_PLAN.md`, `SSOT_V1_1_PROGRESS.yaml`), laissant les 11 successeurs Phase 1 hors manifeste.
- `SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846-v2.yaml` : même constat (`self_hash` recalculé `sha256:d843dc…`), et le manifest reste une photo du sprint pilote ; aucune ressource Phase 1 n’y apparaît. Les références de registre et de progress pointent vers les fichiers non corrigés.
- Les fichiers v1 historiques (`SSOT_V1_1_HASHES.yaml`, `SSOT_V1_1_PROGRESS.yaml`, `SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml`) contiennent toujours les placeholders `sha256:(to_be_calculated)` invoqués par défaut par le pipeline.

## Vérification du registre v1.1_v2

`docs/_registry/registry_v1.1_v2.yaml` ne publie que deux lignées (ADR-0001, RFC-0001), identiques au sprint pilote. Aucun des 11 successeurs critiques (catégories A, B, E) n’apparaît dans le registre actif, aucune entrée n’est marquée `Superseded`/`Active` pour ces documents, et aucune chaîne `previous_hash` n’a été créée pour eux. Le workflow CI continue d’appeler `ssot_registry_check.py` sur `docs/_registry/registry_v1.1.yaml`, qui conserve des placeholders `sha256:(to_be_calculated)` et des `pending_migration` incomplets.

## Concordance avec les scripts stricts

- `python scripts/ssot_hash_check.py --ci` renvoie toujours des erreurs : `SELF_HASH-DIVERGENCE` sur les nouveaux rapports (guillemets), `HASH-PLACEHOLDER` sur les manifestes d’origine, `HASH-DIVERGENCE` sur `SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml`.
- Même en forçant `--hashes-file docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES-v2.yaml`, les divergences persistent (guillemets, self_hash YAML incohérents, fichiers d’evidence encore non recalculés).
- `python scripts/ssot_registry_check.py --ci --strict` reste en échec (`REG-HASH-PLACEHOLDER`, `REG-ID`, `REG-COVERAGE`, `PEND-STATUS-MISSING`, `REQ`) faute d’un registre v1.1 couvrant les 11 successeurs.
- Aucun log ou artefact ne démontre une exécution strict réussie postérieure aux corrections annoncées.

## Scores par axe (Phase 1)

| Axe | Score | Commentaire |
|-----|-------|-------------|
| hash_alignment_phase1 | 0.2 | Successeurs présents mais 3 YAML ont un `self_hash` invalide et 6 Markdown restent rejetés par `ssot_hash_check.py` à cause des guillemets. |
| registry_alignment_phase1 | 0.0 | Les 11 successeurs n’existent dans aucune lignée active du registre v1.1_v2. |
| succession_fidelity_phase1 | 0.4 | `previous_hash` correct sur tous les fichiers, mais front matter v1.1 partiel et absence de mise à jour registre détruisent la filiation officielle. |
| proof_readiness_phase1 | 0.0 | Les commandes strictes échouent toujours ; le pipeline S8 reste rouge sur les catégories A/B/E. |

## Verdict & recommandations

Phase 1 n’est pas complète : aucun des 11 fichiers n’est réellement « SSOT-compliant » sur la boucle hash/manifeste/registre. Les successeurs existent mais ne sont pas consommés par le pipeline, les manifestes et le registre demeurent centrés sur le sprint pilote, et les scripts stricts continuent de signaler les mêmes catégories d’erreurs. Pour la suite :
- recalculer les `self_hash` (YAML inclus) sans guillemets et automatiser leur écriture ;
- faire pointer `ssot_hash_check.py` et `ssot_registry_check.py` vers les manifests et registres `-v2`, en supprimant les placeholders résiduels ;
- enrichir `registry_v1.1_v2.yaml` avec les 11 lignées, statuts `Superseded/Active`, et chaîner `previous_hash` ;
- revisiter l’evidence/validation align pour refléter l’état réel et planifier les phases 2/3/4 sur une base factuelle.

Tant que ces correctifs ne sont pas appliqués, les « successeurs critiques » restent des témoins incomplets et le pipeline strict S8 ne peut être considéré comme fiable sur ce périmètre.
