---
id: "SPRINT_DOC-0100"
id_root: "SPRINT_DOC-0100"
type: "SPRINT_DOC"
status: "En cours"
date: "2025-11-06"
author: "Cline"
version: "2.0"
scope: "organizational"
pattern: "rule"
links:
  supersedes:
    - "docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_STRICT_PLAN.md"
  cites: ["RFC-0001"]
tags: ["ssot", "ci", "strict", "compliance", "audit"]
previous_hash: "sha256:c4ba98862451c4b79799ce3d22a0da78c926eefa6e3abbe9fe454a4b50147133"
self_hash: sha256:eadaea0193f3480c05c50bf1f13d4b00a83304bfe850cd401002e08d3ef888d6
---

# SSOT v1.1 — S8-STRICT Plan (Durcissement du pipeline de preuve)

Objectif: transformer le triple-check S8-PROOF en mécanisme de certification automatique, bloquant en CI, dont les résultats sont auditables objectivement.

- Portée: scripts (hash/registry/schema), workflow `.github/workflows/ssot-proof.yml`, nouveaux rapports S8-STRICT.
- Non-portée: aucune modification des ADR/RFC/OBS/snapshots certifiés.

## Règles rendues obligatoires (strict)

- Hash:
  - self_hash manquant → échec strict
  - self_hash placeholder `sha256:(to_be_calculated)` → échec strict
  - divergence self_hash/manifeste → échec strict
- Registry:
  - Scan étendu: `docs/observatory/**`, `docs/sprints/**`, `reports/**`
  - pending_migration: `hash` et `status` obligatoires
  - présence RFC-004 et OBS-0001..0003 (au minimum référencés ou en pending_migration)
  - cohérence `hash` registre ↔ fichier réel (placeholder interdit en strict)
  - en strict: tout document scanné absent du registre/pending_migration → échec
- Schema:
  - Champs supplémentaires vérifiés: `version`, `scope`, `pattern`, `id_root`, `roles.*`, `decision_type`
  - `--targets` permet d’inclure `docs/sprints/**` et `reports/**`
  - en strict: champ manquant/invalide → échec (code 2)

## Méthode d’activation

1) Dry-run local
- Exécuter les scripts en local sans commit:
  - `python scripts/ssot_hash_check.py --strict`
  - `python scripts/ssot_registry_check.py --strict`
  - `python scripts/ssot_schema_check.py --strict --targets docs/03-architecture/decisions docs/03-architecture/rfcs docs/03-architecture/observations docs/observatory docs/sprints docs/reports`
- Résoudre les erreurs jusqu’à obtenir code 0 (ou 1 si warning toléré hors strict).

2) Activation CI
- Workflow: `.github/workflows/ssot-proof.yml` force `--strict` + `--ci`
- Publication d’artefacts:
  - `artifacts/hash_check.log`, `artifacts/registry_check.log`, `artifacts/schema_check.log`
  - codes: `artifacts/*.code`
- Évaluation stricte finale: si un code > 0 → job échoue (code 2)

## Codes de sortie

- Code 0: OK
- Code 1: écarts mineurs (warnings/skip non strict)
- Code 2: écarts critiques (bloquant CI, strict)

## Traçabilité et audit externe

- Artefacts CI exportés systématiquement (logs + codes)
- Scripts idempotents, lecture seule par défaut
- Reproductibilité:
  - Python 3.11 + PyYAML
  - `python scripts/ssot_*_check.py --ci --strict ...`
  - mêmes options que CI

## Impacts attendus

- CI échoue explicitement si:
  - `self_hash` absent/placeholder/divergent
  - document scanné absent du registre/pending_migration
  - champ critique de schéma manquant/invalide
- Les corrections nécessaires sont visibles dans les artefacts.

## Limites et next

- Les documents historiques non migrés doivent être listés avec `hash` et `status` dans `pending_migration` (sinon échec strict).
- Les SPRINT_DOC nouvellement ajoutés doivent être intégrés au registre (ou pending_migration) pour passer en strict.
- Améliorations futures: vérification d’existence réelle des IDs référencés dans `links.*` (graph consistency).

## Statut "required" sur la branche principale

- Objectif: faire du job “SSOT v1.1 Triple-Check (S8-PROOF) / triple-check” un contrôle obligatoire sur la branche `main`.
- Méthode recommandée (UI GitHub):
  - Settings → Branches → “Branch protection rules” → Edit (ou Add rule) pour `main`
  - Cocher “Require status checks to pass before merging”
  - Ajouter le check: `SSOT v1.1 Triple-Check (S8-PROOF) / triple-check`
  - Enregistrer
- Alternative (CLI): utiliser `gh` pour créer/mettre à jour la rule (selon droits repo). Le nom exact du contexte requis est visible dans l’onglet “Checks” d’un PR: `SSOT v1.1 Triple-Check (S8-PROOF) / triple-check`.
