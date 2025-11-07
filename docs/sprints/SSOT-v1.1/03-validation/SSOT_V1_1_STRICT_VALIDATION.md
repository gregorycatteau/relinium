---
id: "SPRINT_DOC-0102"
type: "SPRINT_DOC"
status: "En cours"
date: "2025-11-06"
author: "Cline"
version: "1.0"
id_root: "SPRINT_DOC-0102"
scope: "organizational"
pattern: "observation"
links:
  cites: ["SPRINT_DOC-0100", "SPRINT_DOC-0101"]
tags: ["ssot", "ci", "strict", "validation", "audit"]
self_hash: sha256:e27c5650f67032da96bd26dfa1a586fd61b08510b1c2b591adb15247ef4f2ceb
---

# SSOT v1.1 — S8-STRICT Validation

Tableau de résultats consolidés du triple-check en mode strict.

| Check    | Script                   | Statut | Strict Mode | Commentaire |
|----------|--------------------------|--------|-------------|-------------|
| Hash     | ssot_hash_check.py       | KO     | ✅          | Divergences self_hash sur plusieurs rapports existants + manifeste (snapshots). |
| Registry | ssot_registry_check.py   | KO     | ✅          | Placeholders et champs `pending_migration` incomplets (`hash`/`status`), couverture étendue (observatory/sprints/reports). |
| Schema   | ssot_schema_check.py     | KO     | ✅          | Champs v1.1 additionnels manquants (version/scope/pattern/id_root/roles/decision_type) sur fichiers historiques. |

Les résultats KO sont attendus en S8-STRICT: la CI doit échouer tant que les invariants ne sont pas satisfaits. Les artefacts CI (logs + codes) sont publiés automatiquement pour audit externe.

## Limites restantes

- Documents historiques non migrés vers v1.1: compléter `pending_migration` (ajouter `hash` et `status`) ou intégrer dans `lineages`.
- Mettre à jour les front matters manquants/incomplets (version/scope/pattern/id_root, etc.) pour les documents concernés (hors périmètre: ne pas altérer ADR/RFC/OBS certifiés sans procédure adaptée).
- Remplacer tous les placeholders `sha256:(to_be_calculated)` par des hashs réels avant validation finale.

## Reproductibilité (auditeur externe)

- En local:
  - `python scripts/ssot_hash_check.py --strict --ci`
  - `python scripts/ssot_registry_check.py --strict --ci`
  - `python scripts/ssot_schema_check.py --strict --ci --targets docs/03-architecture/decisions docs/03-architecture/rfcs docs/03-architecture/observations docs/observatory docs/sprints docs/reports`
- En CI: consulter les artefacts `ssot-proof-artifacts` (logs `.log` et codes `.code`).
