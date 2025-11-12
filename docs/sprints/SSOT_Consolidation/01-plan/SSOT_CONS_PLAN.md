---
id: "SPRINT_DOC-0200"
id_root: "SPRINT_DOC-0200"
version: "1.0.0"
type: "SPRINT_DOC"
status: "Planifié"
date: "2025-11-10"
author: "Codex"
scope: "organizational"
pattern: "rule"
workstream: "SSOT"
phase: "consolidation"
priority: "critical"
tags:
  - "ssot"
  - "consolidation"
  - "automation"
  - "observatory"
links:
  cites:
    - "OBS-0007"
    - "OBS-0005"
    - "OBS-0006"
    - "OBS-0004"
  implements:
    - "RFC-004"
changelog:
  - version: "1.0.0"
    date: "2025-11-10"
    author: "Codex"
    changes: "Plan directeur SSOT Consolidation"
self_hash: sha256:0e6d71bdaec46948e4df37102ac4a86eac59e2cdd3e06aa9c1cae8f34b7a125e
---

# Programme SSOT Consolidation — Plan Directeur

## 1. Mandat & KPIs dérivés d’OBS-0007

| Périmètre OBS-0007 | KPI cible | Mesure associée |
|--------------------|-----------|-----------------|
| Faux positifs CI (désynchronisation schéma) | < 5 % avant fin Semaine 1 | `scripts/validate_frontmatter.py --ci` |
| Couverture registre | 100 % avant fin Mois 1 | `scripts/ssot_registry_check.py --ci --strict` |
| Conformité documentaire | > 95 % avant fin Mois 1 | `scripts/ssot_schema_check.py --strict --targets docs/` |
| Commits signés + logs scellés | 100 % avant fin Mois 2 | `git log --show-signature`, manifestes logs |
| Temps CI stable | < 5 min corpus actuel, < 12 min à 5k docs | Pipeline GitHub Actions |
| UX contributeurs | -70 % MTTR support contenu | Guide incident + dashboard |

Ces objectifs gouvernent l’ordre des sprints ci-dessous. Chaque lot suit la même triade que SSOT-v1.1 (plan → evidence → validation) afin de produire des artefacts vérifiables.

## 2. Orchestration des sprints

| Sprint | Fenêtre | Cible OBS-0007 | Livrables planifiés |
|--------|---------|----------------|---------------------|
| C0 — Quick Sync | Semaine 1 | Bloquants P0 | Patch validateur, promotion registre v6, audit dette complet |
| C1 — Documentary Surge | Semaines 2-4 | Dette documentaire | Sprints de migration par familles + manifestes hash |
| C2 — Registry Automata | Semaines 5-6 | Registre / CI | Jobs auto-refresh + checks stricts signés |
| C3 — Trust Hardening | Semaines 6-8 | Sécurité P1 | Politique GPG, scellement logs, stockage artefacts |
| C4 — DX Shields | Semaines 8-10 | Inefficiences contributrices | Pre-commit, guide erreurs, playbooks |
| C5 — UX & Scale | Mois 3-4 | Phase Innovation courte | Dashboard monitoring, cache CI, parallélisation |
| C6 — Vision Carryover | Mois 4-6 | Phase Vision | Agent UI/API, citations intelligentes, préparation event sourcing |

Les sections suivantes détaillent chaque sprint.

### Sprint C0 — Quick Sync (Semaine 1)

- **Objectif** : Restaurer un pipeline CI exécutable pour pouvoir mesurer la dette réelle.
- **Backlog prioritaire** :
  1. Mise à jour `scripts/validate_frontmatter.py` vers le schéma v1.1.
  2. Promotion de `docs/_registry/registry_v1.1_v6.yaml` comme registre actif et purge des placeholders.
  3. Génération d’un rapport `reports/analysis/SSOT_CONS_DEBT_AUDIT.md` via `ssot_schema_check.py --strict`.
- **Livrables** : patch validateur, registre aligné, rapport d’audit (dossier `02-evidence/`).
- **Validation** : `python3 scripts/validate_frontmatter.py --ci` retourne 0, `ssot_registry_check.py --ci --strict` retourne 0.
- **Pourquoi maintenant** : condition d’entrée pour tout sprint ultérieur (pas de mesure → pas de pilotage).

### Sprint C1 — Documentary Surge (Semaines 2 à 4)

- **Objectif** : Réduire la dette documentaire de 84 % à < 5 %.
- **Stratégie** : Découper par familles (Observatory, sprints v1.0, sprints v1.1, reports) et appliquer succession RFC-004.
- **Backlog** :
  - Injections frontmatter + `previous_hash` pour les sprints SSOT-v1.0 (création de successeurs `-v2`).
  - Normalisation des IDs Observatory (`OBS-000X`) et rattachement aux analyses sources (OBS-0004→7).
  - Alignement des types (`sprint_plan`, `observation`, `decision_record`, etc.) selon `document_schema_v1.1`.
- **Livrables** : Série de plans/README successeurs, manifestes hash dans `03-validation/`.
- **Validation** : `ssot_schema_check.py --strict --targets docs/` passe vert sur le périmètre migré, `SSOT_CONS_PROGRESS.yaml` mis à jour.
- **Dépendances** : Sprint C0 finalisé.

### Sprint C2 — Registry Automata (Semaines 5 à 6)

- **Objectif** : Éliminer toute intervention manuelle pour l’inscription registry.
- **Backlog** :
  - Ajout d’un job CI `refresh_registry_v6.py` exécuté à chaque merge.
  - Signature GPG des commits générés par la CI + attestation du job.
  - Publication automatique du `registry_v1.1.yaml` consolidé dans `docs/_registry/`.
- **Livrables** : Workflow GitHub Actions, script de refresh, manifeste `SSOT_CONS_REGISTRY_VALIDATION.md`.
- **Validation** : `ssot_registry_check.py --ci --strict` appelé depuis CI + rapport attaché dans `02-evidence/`.
- **KPI** : 0 delta manuel détecté sur deux cycles de merge consécutifs.

### Sprint C3 — Trust Hardening (Semaines 6 à 8)

- **Objectif** : Couvrir les défaillances sécurité (GPG + logs scellés).
- **Backlog** :
  - Activation branch protection (commits signés obligatoires) et documentation onboarding GPG.
  - Ajout d’un pipeline de scellement qui attache `sha256` + `commit_sha` aux logs `reports/validation/`.
  - Archivage automatique des artefacts CI dans `reports/validation/ci-runs/DATE/`.
- **Livrables** : `SSOT_CONS_SECURITY_POLICY.md`, scripts de scellement, rapport d’essai.
- **Validation** : `git log --show-signature -5` montre `Good signature`, manifestes logs vérifiés par relecture croisée.

### Sprint C4 — DX Shields (Semaines 8 à 10)

- **Objectif** : Empêcher la réintroduction de dette documentaire et réduire le MTTR contributeurs.
- **Backlog** :
  - Hooks pre-commit (`scripts/pre_commit_ssot.sh`) appelant les validateurs stricts.
  - Guide de résolution d’erreurs CI (`docs/handbook/SSOT_CI_PLAYBOOK.md`).
  - Modèles `issue/PR` intégrant les KPIs (CI logs, hash, registre).
- **Livrables** : Hook versionné, documentation, enregistrement vidéo court (optionnel) dans `02-evidence/`.
- **Validation** : Pas plus de 1 échec CI par semaine dû à la validation frontmatter durant 4 semaines.

### Sprint C5 — UX & Scale (Mois 3 à 4)

- **Objectif** : Réduire le temps d’exécution CI et offrir de la visibilité temps réel.
- **Backlog** :
  - Implémenter cache `mtime + hash` dans les scripts de scan.
  - Paralléliser les scripts via `multiprocessing` (segmentation par dossiers).
  - Déployer un dashboard (Grafana ou simple static) affichant conformité, dettes restantes, temps CI.
- **Livrables** : version 2 des scripts (`ssot_schema_check_v2.py`), `SSOT_CONS_DASHBOARD_SPEC.md`, capture d’écran / JSON du dashboard.
- **Validation** : Temps CI mesurés < 5 min corpus actuel, < 12 min sur dataset projeté (simulation).

### Sprint C6 — Vision Carryover (Mois 4 à 6)

- **Objectif** : Préparer les chantiers innovation de la phase Vision (event sourcing, agent UI, citations).
- **Backlog** :
  - MVP FastAPI pour création assistée (ID auto, suggestions `links.cites`).
  - Service de recommandations de citations (analyse sémantique OBS-0007).
  - Spécification event sourcing + PoC sur un sous-ensemble (par exemple Observatoire).
- **Livrables** : `SSOT_CONS_INNOVATION_ROADMAP.md`, PoC API, graphe des dépendances.
- **Validation** : démonstration interne, KPIs UX (-50 % temps création doc) mesurés sur un panel pilote.

## 3. Gouvernance & Traçabilité

1. **Plan → Evidence → Validation** : chaque sprint crée au minimum un plan détaillé, un rapport d’évidence et une entrée de validation (hashes + manifester) dans ce répertoire.
2. **Registry First** : aucune livraison considérée “done” tant que `registry_v1.1.yaml` n’est pas mis à jour et signé.
3. **Indice de maturité** : `SSOT_CONS_PROGRESS.yaml` (03-validation) suivra l’avancement par KPI et par sprint.
4. **Comités** : revue hebdomadaire S0 (pilotage) + comité mensuel aligné sur RFC-004.

## 4. Risques & Mesures préventives

- **Charge de migration sous-estimée** → Renfort pair-programming (C1) + métriques journalières.
- **Adoption GPG lente** → Paires clé/agent fournies + workshop interne sprint C3.
- **CI rallongée pendant refonte** → Exécuter les scripts optimisés sur un runner dédié avant merge (C5).
- **Innovation dépriorisée** → Sprint C6 conçu comme backlog protégé mais peut être ré-étalé sans bloquer la conformité.

## 5. Suivi attendu

- `SSOT_CONS_STEERING.md` (à créer) contiendra l’historique des revues.
- Chaque sprint clos bénéficie d’un ticket Observatoire lié (ex. `OBS-CONS-00X`) pour maintenir la traçabilité SSOT complète.
