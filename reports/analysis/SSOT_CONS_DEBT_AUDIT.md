---
id: "OBS-0008"
id_root: "OBS-0008"
type: "OBS"
status: "Ouvert"
date: "2025-11-10"
author: "Codex"
version: "1.0.0"
scope: "technical"
pattern: "observation"
tags:
  - "ssot"
  - "audit"
  - "sprint-c0"
  - "automation"
links:
  cites:
    - "OBS-0007"
self_hash: sha256:99ae8b08a918763016e91f46505bffa289db91d7fc3a926db54f910f84087b7d
---

# Audit C0 — Dette documentaire & registres SSOT

## 1. Périmètre et commandes exécutées

| Commande | Objectif | Sortie |
|----------|----------|--------|
| `python3 scripts/validate_frontmatter.py` | Vérifier l’usage du schéma v1.1 dans les frontmatters | ❌ Exit 1 |
| `python3 scripts/ssot_registry_check.py --ci --strict` | Contrôler registres/hashs après promotion v6 | ❌ Exit 2 |
| `python3 scripts/ssot_schema_check.py --strict --targets docs` | Cartographier la dette documentaire complète | ❌ Exit 2 |

Logs détaillés : `reports/analysis/validate_frontmatter_C0.log`, `reports/analysis/registry_check_C0.log`, `reports/analysis/schema_check_C0.log`.

## 2. Résultats clés

### 2.1 Validation frontmatter (v1.1)

- 80 fichiers scannés → 15 valides / 65 invalides (81% de dette).
- Principales erreurs : absence de frontmatter (v1.0 héritée), IDs hors pattern, champs `pattern`/`scope` manquants, `links.cites` pointant vers des chemins au lieu d’IDs.
- **Action C0 livrée** : `scripts/validate_frontmatter.py` pointe désormais vers `document_schema_v1.1.json` (Quick Win #1), ce qui expose la dette réelle au lieu des faux positifs v1.0.

### 2.2 Registre SSOT

- Promotion réalisée : `docs/_registry/registry_v1.1.yaml` ← `registry_v1.1_v6.yaml` (Quick Win #2).
- Contrôle strict toujours KO : 4 divergences de hash (observatory historiques) et 7 documents hors couverture (dont OBS-0005/6, OBS-AUTOMATION-0001 et les nouveaux artefacts C0).
- Prochaines étapes (Sprint C2) : automatiser la génération + ajouter les nouvelles lignées (`SPRINT_DOC-0200/0201`, OBS récents, report OBS-0007).

### 2.3 Audit schéma strict (`docs/`)

- 80 fichiers scannés → 13 OK / 53 KO / 14 superseded ignorés.
- Catégories :
  - **Frontmatter absent** : totalité des sprints SSOT-v1.0 + README divers.
  - **IDs/Patterns invalides** : plans SSOT-v1.1 historiques, observatory pré-v1.1.
  - **Champs manquants** : `date`, `status`, `id_root`, `scope`, `pattern`.
- **Action C0 livrée** : les deux nouveaux artefacts SSOT_Consolidation ont reçu un frontmatter v1.1 et un `self_hash` certifié pour éviter d’ajouter de la dette.

## 3. KPIs vs objectifs OBS-0007

| KPI | Baseline mesurée C0 | Cible OBS-0007 | Commentaire |
|-----|---------------------|----------------|-------------|
| Faux positifs CI | 0 % (le validateur reflète désormais la dette réaliste) | < 5 % | L’objectif devient atteignable une fois la dette corrigée (Sprints C1/C4). |
| Couverture registre | 93 % (4 divergences + 7 omissions) | 100 % | La promotion v6 débloque la consolidation, reste la migration des artefacts récents. |
| Conformité documentaire | 19 % (15/80) | > 95 % | Les sprints C1 et C4 adressent la dette par lignée/famille. |

## 4. Points bloquants prioritaires pour C1

1. **Frontmatter manquant (SSOT-v1.0 + evidence)** — nécessite succession `SPRINT_DOC-xxxx-v2` + injection frontmatter automatique.
2. **Observatory historiques** — standardiser IDs (OBS-000X), `pattern`, `scope`, `links`.
3. **Registre partiel** — ajouter les nouvelles lignées et sceller les hashs (C2) avant d’automatiser.

## 5. Livrables C0

- Scripts alignés : `scripts/validate_frontmatter.py` (schéma v1.1) + `docs/_registry/registry_v1.1.yaml` (v6).
- Logs d’exécution centralisés (`reports/analysis/*.log`).
- Artefacts SSOT_Consolidation conformes (plan + README) prêts pour intégration registre.
