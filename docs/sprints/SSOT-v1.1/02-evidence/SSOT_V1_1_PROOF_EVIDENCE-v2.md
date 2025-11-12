---
id: "SPRINT_DOC-0002-v2"
id_root: "SPRINT_DOC-0002"
type: "SPRINT_DOC"
status: "Terminé"
date: "2025-11-06"
author: "Équipe Relinium Genesis"
version: "2.0"
scope: "organizational"
pattern: "experiment"

links:
  supersedes: "SPRINT_DOC-0002"
  implements:
    - "SPRINT_DOC-0041"
  cites:
    - "SPRINT_DOC-0005"
    - "SPRINT_DOC-0006"
    - "SPRINT_DOC-0007"
previous_hash: "sha256:5aa74d858fd8c4ed106d6c977317b6a278d15ea5a372fd05f20e22bc656b67ca"
self_hash: sha256:703d26f9760da0b5020ea7315cb6a70fce03aaf4d769c62be11734e13869d046
---

# S8-PROOF — Rapport d’évidence

Ce document rassemble les éléments probants de la mise en place du pipeline de preuve (triple-check) en S8-PROOF. Il est conçu pour être lisible par un auditeur externe et reproductible localement.

---

## 1) Scripts livrés

- scripts/ssot_hash_check.py
  - Vérifie les self_hash dans les Markdown (exclusion de la ligne self_hash dans le front matter)
  - Vérifie la cohérence du manifeste v1.1 `docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml`
  - Lecture seule par défaut. Options utilitaires locales:
    - `--print-self-hash FILE`
    - `--write-self-hash FILE` (non utilisé en CI)

- scripts/ssot_registry_check.py
  - Vérifie la couverture et la cohérence basique du registre `docs/_registry/registry_v1.1.yaml`
  - Couvre id_root/id/file_path/previous_hash(+format), et existence des fichiers
  - Vérifie que tout fichier normatif scanné est présent dans le registre ou dans `pending_migration`

- scripts/ssot_schema_check.py
  - Vérifie la conformité minimale du front matter v1.1 pour un sous-ensemble ciblé:
    - `docs/03-architecture/decisions`, `docs/03-architecture/rfcs`, `docs/03-architecture/observations`
  - Controles: id/type/status/date, cohérence id/type, statut autorisé par type, previous_hash requis si links.supersedes, conflit author vs roles.author

---

## 2) Exécution locale — Exemples de sorties

Exemple (succès global, code de retour 0):

```bash
$ python scripts/ssot_hash_check.py --ci
✅ [HASH-OK] /path/to/docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md
⏭️  [SKIP] /path/to/docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PILOT_PLAN.md hash='sha256:(to_be_calculated)'
…

$ python scripts/ssot_registry_check.py --ci
✅ [REG-COVERAGE] Couverture registre OK sur les répertoires scannés

$ python scripts/ssot_schema_check.py --ci
✅ [SCHEMA-OK] /path/to/docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first-v2.md
—--------------------------------------------------------------------
Récapitulatif: ok=NN, errors=0
```

Exemple (détection d’écarts, code de retour non nul):

```bash
$ python scripts/ssot_hash_check.py --ci
❌ [SELF_HASH-DIVERGENCE] docs/03-architecture/rfcs/RFC-001-choix-stack-initiale.md
    déclaré: sha256:aaaaaaaa...
    calculé: sha256:bbbbbbbb...

$ python scripts/ssot_registry_check.py --ci
❌ [REG-PATH-MISSING] Fichier inexistant: /repo/docs/03-architecture/observations/OBS-0003-calibration-et-SLOs.md

$ python scripts/ssot_schema_check.py --ci
❌ [SCHEMA] docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first-v2.md
    - previous_hash_requis_ou_invalide_si_supersedes
```

Remarque: S8-PROOF ne corrige pas ces écarts; il les signale pour traitement dans des sprints ultérieurs.

### Sortie réelle (exécution locale S8-PROOF)

Les commandes exécutées localement ont produit la sortie suivante, confirmant que le pipeline détecte correctement les divergences actuelles (attendu en S8, car ce sprint installe l'infrastructure de preuve sans corriger le contenu):

```
❌ [SELF_HASH-DIVERGENCE] /home/striker/Documents/developpement_web/relinium/reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT.md
❌ [SELF_HASH-DIVERGENCE] /home/striker/Documents/developpement_web/relinium/reports/analysis/SSOT_V1_1_100PCT_EXPLORATION.md
❌ [SELF_HASH-DIVERGENCE] /home/striker/Documents/developpement_web/relinium/reports/validation/SSOT_V1_1_VALIDATION_CODEX.md
❌ [SELF_HASH-DIVERGENCE] /home/striker/Documents/developpement_web/relinium/reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE.md
❌ [SELF_HASH-DIVERGENCE] /home/striker/Documents/developpement_web/relinium/reports/validation/SSOT_V1_1_MIRROR_CODEX.md
❌ [HASH-DIVERGENCE] /home/striker/Documents/developpement_web/relinium/docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml
```

Interprétation:
- Les divergences self_hash indiquent un hash déclaré différent du hash recalculé (avec exclusion de la ligne self_hash).
- La divergence de hash manifeste indique que la valeur attendue dans le manifeste ne correspond pas au hash actuel du fichier référencé.

---

## 3) Workflow CI — Résumé

Fichier: `.github/workflows/ssot-proof.yml`

- Déclencheurs: `push`, `pull_request` (toutes branches)
- Jobs:
  - Python 3.11 + PyYAML
  - `python scripts/ssot_hash_check.py --ci`
  - `python scripts/ssot_registry_check.py --ci`
  - `python scripts/ssot_schema_check.py --ci`
- Si un script retourne un code non nul → le job échoue → CI bloque

---

## 4) Reproductibilité — Guide auditeur externe

Pré-requis:
- Python 3.11+
- Dépendances: `pip install pyyaml`

Commandes:

```bash
python scripts/ssot_hash_check.py --ci \
  && python scripts/ssot_registry_check.py --ci \
  && python scripts/ssot_schema_check.py --ci
```

Interprétation:
- Code 0: invariants respectés sur le périmètre
- Code non nul: écarts détectés; consulter les logs pour la typologie et le fichier

---

## 5) Limites connues

- self_hash: l’absence de self_hash est loggée en avertissement (non bloquant à ce stade)
- registre: la couverture est limitée aux répertoires scannés par défaut (03-architecture/*)
- schéma: la validation cible uniquement les documents normatifs (les documents de sprint ne sont pas visés dans S8)
- pipeline orienté lecture seule: aucune écriture FS en CI

---

## 6) Traçabilité

- Plan S8-PROOF: `docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PROOF_PLAN.md`
- Workflow CI: `.github/workflows/ssot-proof.yml`
- Registre v1.1: `docs/_registry/registry_v1.1.yaml`
- Schéma v1.1: `docs/01-genesis/document_schema_v1.1.yaml`
