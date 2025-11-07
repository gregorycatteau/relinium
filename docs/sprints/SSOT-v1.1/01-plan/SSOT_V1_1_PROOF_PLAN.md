---
id: "SPRINT_DOC-0008"
type: "sprint_plan"
status: "En cours"
date: "2025-11-06"
author: "Équipe Relinium Genesis"
version: "1.0"

scope: "organizational"
pattern: "plan"

links:
  cites:
    - "reports/analysis/SSOT_V1_1_100PCT_EXPLORATION.md"
    - "reports/analysis/SSOT_V1_1_100PCT_PLAN.yaml"
    - "reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT.md"
    - "reports/analysis/SSOT_V1_1_TRUTHKEEPER_SCORECARD.yaml"
    - "reports/validation/SSOT_V1_1_VALIDATION_CODEX.md"
    - "reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE.md"
    - "docs/_registry/registry_v1.1.yaml"
    - "docs/01-genesis/document_schema_v1.1.yaml"

self_hash: sha256:98544b18c5ae2675d3a94baaa6d11e112f5f00f9ccd0993a8283d7d4ebdde6b7
---

# S8-PROOF — Plan de Sprint: Implémentation du pipeline de preuve SSOT (Phase 1)

## 🎯 Objet du sprint

Mettre en place l’infrastructure de preuve “triple-check” permettant:
- vérification des `self_hash` et des hash manifests,
- vérification de couverture et cohérence du registre v1.1,
- vérification de conformité documentaire v1.1 (sous-ensemble ciblé),
afin de rendre le SSOT vérifiable par la machine et reproductible par tout audit externe, sans modifier le contenu métier ni corriger les écarts existants.

Contexte: Truth Index ≈ 0.60 (cf. S7-EXPLORE). S8-PROOF prépare les instruments de mesure pour améliorer ce score dans les sprints suivants.

Références:
- Plan S7-EXPLORE: `reports/analysis/SSOT_V1_1_100PCT_EXPLORATION.md`, `reports/analysis/SSOT_V1_1_100PCT_PLAN.yaml`
- Méta-analyse TruthKeeper: `reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT.md`, `reports/analysis/SSOT_V1_1_TRUTHKEEPER_SCORECARD.yaml`
- Validation et auto-critique: `reports/validation/SSOT_V1_1_VALIDATION_CODEX.md`, `reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE.md`, `reports/validation/SSOT_V1_1_MIRROR_CODEX.md`
- SSOT v1.1 / Registre / Schéma: `docs/_registry/registry_v1.1.yaml`, `docs/01-genesis/document_schema_v1.1.yaml`

---

## 🧪 Triple-check: Règles vérifiées (sans correction)

1) Hash/self_hash
- Calcul et comparaison SHA256 des fichiers référencés dans `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml`
- Vérification `self_hash` dans les Markdown (exclusion de la ligne `self_hash:` dans le front matter)
- Aucune écriture disque par défaut (dry-run implicite)

2) Registre v1.1
- Couverture: tout fichier normatif scanné doit être présent dans `lineages[].versions[].file_path` ou dans `pending_migration`
- Cohérence basique: `id_root`, `id`, `file_path` existant, format `previous_hash` si présent

3) Schéma documentaire v1.1 (ciblé)
- Champs requis: `id`, `type`, `status`, `date`
- Cohérence `id`/`type`, statut autorisé par type (mappé depuis le schéma)
- Règle succession: `links.supersedes` => `previous_hash` requis (`sha256:...`)
- Conflit interdit: `author` et `roles.author` simultanés
- Ciblage initial: `docs/03-architecture/{decisions,rfcs,observations}`

Limites: S8 ne corrige pas encore les écarts détectés; il les signale.

---

## 🧰 Scripts et workflows à créer

Scripts (lecture seule par défaut, sortie non nulle si anomalies):
- scripts/ssot_hash_check.py
  - Vérifie `self_hash` et manifeste `SSOT_V1_1_HASHES.yaml`
  - Flags: `--ci`, `--print-self-hash FILE`, `--write-self-hash FILE` (local uniquement)
- scripts/ssot_registry_check.py
  - Vérifie couverture et cohérence minimale du registre v1.1
  - Flags: `--ci`, `--registry-file`, `--scan-roots`
- scripts/ssot_schema_check.py
  - Vérifie conformité front matter v1.1 (ciblage 03-architecture)
  - Flags: `--ci`, `--schema`, `--targets`

Workflow CI:
- .github/workflows/ssot-proof.yml
  - Triggers: push, pull_request
  - Jobs: exécution des 3 scripts en `--ci`
  - Échec du job si code de sortie non nul

---

## 🧭 Stratégie d’exécution — Dry-run d’abord

- Par défaut tous les scripts sont non destructifs et n’écrivent rien (lecture seule).
- En local, l’auditeur peut utiliser les utilitaires “print” et “write” des `self_hash` pour calculer/insérer un hash, mais jamais en CI.
- Le workflow CI n’active aucun mode écriture.

---

## 🗂️ Périmètre initial

- Hash/self_hash: `docs/**` et `reports/**` pour la détection `self_hash`
- Manifeste v1.1: `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml`
- Registre v1.1: `docs/_registry/registry_v1.1.yaml`
- Schéma v1.1 ciblé: `docs/03-architecture/decisions`, `docs/03-architecture/rfcs`, `docs/03-architecture/observations`
  - Les documents de sprint (`docs/sprints/**`) ne sont pas inclus dans le contrôle de schéma à ce stade

---

## 📌 Livrables du sprint

- Plan: docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PROOF_PLAN.md (présent)
- CI: .github/workflows/ssot-proof.yml (présent)
- Scripts: scripts/ssot_hash_check.py, scripts/ssot_registry_check.py, scripts/ssot_schema_check.py (présents)
- Evidence: docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_PROOF_EVIDENCE.md
- Validation: docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROOF_VALIDATION.md

Tous les nouveaux Markdown incluent un `self_hash` (calculé par utilitaire local) et respectent la front matter v1.1.

---

## 🧪 Reproductibilité (auditeur externe)

Pré-requis:
- Python 3.11+
- `pip install pyyaml`

Commande d’audit local:
```bash
python scripts/ssot_hash_check.py --ci \
  && python scripts/ssot_registry_check.py --ci \
  && python scripts/ssot_schema_check.py --ci
```

Interprétation:
- Code de sortie 0 => checks OK sur le périmètre
- Code non nul => divergences détectées (voir logs)
- Aucune écriture effectuée sans drapeau explicite (non utilisé en CI)

---

## 🧱 Contraintes

- Ne pas modifier de documents normatifs historisés (ADR/RFC/OBS existants)
- Ne pas modifier de snapshots certifiés
- Créer uniquement des scripts, workflows et rapports nouveaux
- Respecter la nomenclature S8-PROOF

---

## ✅ DoD (Definition of Done)

- [ ] Scripts présents, en lecture seule, avec codes de sortie corrects
- [ ] Workflow CI présent, déclenché sur push/PR, fail en cas d’anomalies
- [ ] Evidence S8-PROOF avec exemples de sortie (OK/KO)
- [ ] Validation S8-PROOF avec récapitulatif d’exécution locale (ou simulée)
- [ ] Tous les nouveaux Markdown avec front matter v1.1 + self_hash
