---
id: "SPRINT_DOC-0101"
type: "SPRINT_DOC"
status: "En cours"
date: "2025-11-06"
author: "Cline"
version: "1.0"
id_root: "SPRINT_DOC-0101"
scope: "organizational"
pattern: "observation"
links:
  cites: ["SPRINT_DOC-0100"]
tags: ["ssot", "ci", "strict", "evidence", "audit"]
self_hash: sha256:c73f148f023b1252facf326786fd376cb71d3aa3fbde2a27c4721816f99e26f0
---

# SSOT v1.1 — S8-STRICT Evidence

Ce document synthétise les résultats locaux (dry-run) du durcissement du pipeline S8-STRICT.

## Résumé des tests locaux

- Mode strict activé sur les trois scripts (`--strict --ci`).
- Cibles élargies en validation de schéma et registre (observatory/sprints/reports).
- Génération d’artefacts (logs + codes) en CI (voir workflow).

### Exemples de résultats (local)

- Hash check:
  - KO (exemples divergences self_hash sur certains rapports existants)
  - Divergences attendues: correction à faire dans les documents concernés (hors périmètre : pas de modification ADR/RFC/OBS certifiés).
- Registry check:
  - KO (placeholders et champs `pending_migration` incomplets: `hash`/`status` manquants pour certains OBS)
  - Présence des lignées RFC/OBS vérifiée; cohérence des chemins testée.
- Schema check:
  - KO (en mode strict sur cibles élargies: champs additionnels v1.1 manquants sur certains fichiers historiques)

Ces KO sont cohérents avec l’objectif S8-STRICT: faire échouer la CI tant que les invariants ne sont pas respectés.

## Logs et interprétation

- Les logs contiennent:
  - divergences de `self_hash` (ligne déclarée vs recalcul)
  - divergences manifeste vs hash réel du fichier
  - absences dans le registre/pending_migration
  - champs de schéma manquants/incohérents (version, scope, pattern, id_root, roles.*, decision_type)
- Les codes de sortie (0/1/2) permettent une lecture univoque:
  - 0 = OK
  - 1 = écarts mineurs (non strict)
  - 2 = écart critique (strict, bloque la CI)

## Reproductibilité (auditeur externe)

- Python 3.11 + PyYAML
- Exécution locale:
  - `python scripts/ssot_hash_check.py --strict --ci`
  - `python scripts/ssot_registry_check.py --strict --ci`
  - `python scripts/ssot_schema_check.py --strict --ci --targets docs/03-architecture/decisions docs/03-architecture/rfcs docs/03-architecture/observations docs/observatory docs/sprints docs/reports`
- En CI: artefacts publiés automatiquement (`artifacts/*.log`, `artifacts/*.code`)
