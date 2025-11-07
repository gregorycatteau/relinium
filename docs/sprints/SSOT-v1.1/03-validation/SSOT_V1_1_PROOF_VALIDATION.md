---
id: "SPRINT_DOC-0008-VALIDATION"
type: "SPRINT_DOC"
status: "En cours"
date: "2025-11-06"
author: "Équipe Relinium Genesis"
version: "1.0"

scope: "organizational"
pattern: "observation"

links:
  cites:
    - "docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PROOF_PLAN.md"
    - "docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_PROOF_EVIDENCE.md"
    - ".github/workflows/ssot-proof.yml"
    - "scripts/ssot_hash_check.py"
    - "scripts/ssot_registry_check.py"
    - "scripts/ssot_schema_check.py"
    - "docs/_registry/registry_v1.1.yaml"
    - "docs/01-genesis/document_schema_v1.1.yaml"

self_hash: sha256:63c2833fdde98286735f930ce9583f70500ac336d1d461b691da960655474461
---

# S8-PROOF — Rapport de validation (auto)

Ce document trace l’exécution locale des 3 scripts du triple-check (hash/registry/schema) et synthétise leur statut.  
Les scripts sont en lecture seule par défaut; toute écriture est explicitement interdite en CI.

---

## 1) Récapitulatif des objectifs S8

- Implémenter un pipeline de preuve reproductible (triple-check)
- Outiller l’auditeur externe (scripts + workflow CI)
- Ne corriger aucun écart dans ce sprint (détection seule)

---

## 2) Trace d’exécution locale (exemple)

Commandes:

```bash
python scripts/ssot_hash_check.py --ci
python scripts/ssot_registry_check.py --ci
python scripts/ssot_schema_check.py --ci
```

Sorties (exemple illustratif):
```
[hash_check]   ✅ ok=... ⏭️  skip=... ❌ errors=...
[registry]     ✅ coverage OK / ❌ missing: ...
[schema]       ✅ ok=... ❌ errors=...
```

Interprétation:
- Code 0 → OK (aucune divergence bloquante, sur le périmètre)
- Code non nul → KO (divergences signalées)

---

## 3) Tableau synthétique

| Check    | Script                  | Statut | Commentaire |
|----------|-------------------------|--------|-------------|
| Hash     | ssot_hash_check.py      | OK/KO  | Self-hash et manifeste v1.1 |
| Registry | ssot_registry_check.py  | OK/KO  | Couverture + cohérence basique |
| Schema   | ssot_schema_check.py    | OK/KO  | Conformité front matter v1.1 ciblée |

Remarques:
- Les documents de sprint ne sont pas inclus dans le contrôle de schéma S8.
- Les entrées `hash: sha256:(to_be_calculated)` dans le manifeste sont ignorées (skip).

---

## 4) Limites connues

- Les self_hash manquants sont signalés en avertissement (non bloquant).
- La couverture du registre se limite aux répertoires scannés.
- La validation de schéma cible 03-architecture (ADR/RFC/OBS); les sprints ne sont pas visés.
- Aucun correctif automatique n’est appliqué en S8 (détection uniquement).

---

## 5) Reproductibilité

Pré-requis:
- Python 3.11+
- `pip install pyyaml`

Commande d’audit local (équivalente CI):

```bash
python scripts/ssot_hash_check.py --ci \
  && python scripts/ssot_registry_check.py --ci \
  && python scripts/ssot_schema_check.py --ci
```

Code de sortie non nul → investiguer les logs des scripts.
