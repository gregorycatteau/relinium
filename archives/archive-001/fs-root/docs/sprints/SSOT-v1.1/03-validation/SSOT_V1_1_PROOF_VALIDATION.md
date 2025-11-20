---
id: "SPRINT_DOC-0046"
id_root: "SPRINT_DOC-0046"
type: "SPRINT_DOC"
status: "Certifié"
date: "2025-11-06"
author: "Équipe Relinium Genesis"
version: "1.0"
scope: "organizational"
pattern: "rule"
links:
  cites:
    - "SPRINT_DOC-0041"
    - "SPRINT_DOC-0002-v3"
    - "SPRINT_DOC-0005-v3"
    - "SPRINT_DOC-0006-v3"
    - "SPRINT_DOC-0007-v3"
    - "SPRINT_DOC-0060-v5"
self_hash: sha256:fad17917a7e65c866e7851a5e8bdaa21751f7af21f6f34dd997f320fdbf358f9
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
