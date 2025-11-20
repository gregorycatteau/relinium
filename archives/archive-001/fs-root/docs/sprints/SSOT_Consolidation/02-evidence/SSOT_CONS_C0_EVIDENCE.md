---
id: "SPRINT_DOC-0202"
id_root: "SPRINT_DOC-0202"
type: "SPRINT_DOC"
status: "Terminé"
date: "2025-11-10"
author: "Codex"
version: "1.0.0"
scope: "organizational"
pattern: "observation"
links:
  cites:
    - "SPRINT_DOC-0200"
    - "OBS-0007"
tags:
  - "ssot"
  - "sprint-c0"
  - "evidence"
self_hash: sha256:15a5927135f323f48e795d5aa560d0cac86a77fdb1dabac489b049c64ab5fdab
---

# SSOT Consolidation — Sprint C0 Evidence

## 1. Quick wins exécutés

| Action | Détail | Statut |
|--------|--------|--------|
| Alignement validateur | `scripts/validate_frontmatter.py` pointe sur `document_schema_v1.1.json` | ✅ appliqué |
| Promotion registre | `docs/_registry/registry_v1.1.yaml` remplacé par `registry_v1.1_v6.yaml` | ✅ appliqué |
| Préparation artefacts C0 | Plan (`SPRINT_DOC-0200`) + README (`SPRINT_DOC-0201`) conformes v1.1 + `self_hash` | ✅ appliqué |

## 2. Commandes exécutées

```bash
python3 scripts/validate_frontmatter.py
python3 scripts/ssot_registry_check.py --ci --strict
python3 scripts/ssot_schema_check.py --strict --targets docs
```

Logs associés : 
- `reports/analysis/validate_frontmatter_C0.log`
- `reports/analysis/registry_check_C0.log`
- `reports/analysis/schema_check_C0.log`

## 3. Synthèse des résultats

| Contrôle | Résultat | Observations |
|----------|----------|--------------|
| Frontmatter (80 fichiers) | ❌ 15 valides / 65 invalides | Erreurs majeures : FM absent (SSOT-v1.0), IDs hors pattern, `links` non conformes. |
| Registre v6 | ❌ 4 divergences hash / 7 omissions | Lignées observatory historiques à recalculer, nouveaux artefacts à inscrire. |
| Schéma strict | ❌ ok=13 / errors=53 / skip=14 | V1.0 hérités + observatory legacy → cible principale du Sprint C1. |

## 4. KPIs suivis

- KPI faux positifs CI : **0 %** (exposition réelle de la dette, condition d’entrée OK).
- KPI couverture registre : **93 %** (à porter à 100 % via C2).
- KPI conformité documentaire : **19 %** (15/80) → plan C1.

## 5. Prochaines étapes recommandées

1. Lancer migrations par lignée (C1) pour injecter frontmatter + IDs normés.
2. Mettre à jour `registry_v1.1.yaml` avec les nouvelles lignées + recalcul des hashs.
3. Préparer scripts pre-commit (C4) pour maintenir la conformité dès création.
