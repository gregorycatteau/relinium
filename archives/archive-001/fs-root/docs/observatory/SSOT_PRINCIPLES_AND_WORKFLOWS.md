---
id: OBS-0104
type: OBS
status: Synthétisé
date: '2025-11-08'
author: Équipe Relinium Genesis
version: '1.0'
tags:
- ssot
- principes
- workflows
- registry
- validation
links:
  cites:
  - ADR-0001
  - OBS-0100
  - OBS-0101
  - OBS-0102
  - OBS-0103
id_root: OBS-0104
scope: organizational
pattern: observation
self_hash: sha256:2cb009982051c5b4654ee937287131135fe31647ed7e1db9ec23ebb3f3143faf
---

# SSOT_PRINCIPLES_AND_WORKFLOWS — Principes et Workflows du SSOT Relinium

- Statut: ✅ Synthèse validable
- Portée: Description des principes, des composants et des workflows opérationnels du SSOT (phase Genesis → Croissance)
- Références: ADR-0001 (Docs-first), OBS-0100 (Exploration SSOT), OBS-0101 (Métadonnées), OBS-0102 (Gouvernance), OBS-0103 (Scénarios)

---

## 1. Principes Directeurs du SSOT Relinium

1) Source unique de vérité pilotée par la documentation  
- La documentation structure la vérité de projet (Docs-first, ADR-0001).  
- Le code et les scripts dérivent de la matière documentaire.

2) Traçabilité, Transparence, Auditabilité  
- Chaque changement est explicite, daté, attribué, justifié.  
- L'historique est consultable et vérifiable (Git + rapports).

3) Inviolabilité pragmatique  
- Inviolabilité = impossibilité d’effacer l’intention et la trace, pas blocage de l’édition.  
- Les contenus terminaux (ADR acceptés) sont figés, les vivants (OBS, RFC en discussion) évoluent.

4) Lisibilité humaine d’abord  
- Markdown + frontmatter YAML minimal (id, type, status, date).  
- Les enrichissements (graphes, index, signatures) restent annexes et régénérables.

5) Automatisation mesurée  
- Validation automatique (frontmatter/schema), génération d’index (registry) et contrôles d’intégrité.  
- Le registre est un index, pas la vérité elle-même (Git-as-Truth + Lightweight Registry).

---

## 2. Composants Clés du SSOT

- Frontmatter YAML (S1)  
  - Schéma canonique: `docs/01-genesis/document_schema_v1.json`.  
  - Champs obligatoires: id, type, status, date.  
  - Objectif: métadonnées minimales, extractibles et validables.

- Validateur de frontmatter (S3)  
  - Script: `scripts/validate_frontmatter.py`.  
  - Rôle: contrôle du schéma, cohérence de base, rapports CI.

- Registre documentaire (S4)  
  - Script: `scripts/generate_registry.py` → produit `docs/_registry/registry.yaml`.  
  - Contenu: inventaire, métadonnées essentielles, hashes fichier, graph simplifié des liens.  
  - Statut: index régénérable (ne remplace pas Git).

- Contrôles SSOT v1.1 (triple-check)  
  - Script: `scripts/ssot_registry_check.py` (cible v1.1), couverture et cohérence avancées.  
  - Compléments: `scripts/ssot_schema_check.py`, `scripts/ssot_hash_check.py`, `scripts/audit_verify_hashes.py`.

- CI et gouvernance  
  - GitHub Actions (frontmatter CI), commits signés recommandés (GOVERNANCE.md).  
  - Règles de contribution (CONTRIBUTING.md), responsabilités (CODEOWNERS).

---

## 3. Workflows Opérationnels

### 3.1. Rédaction / Évolution d’un document

- Entrées: besoin, observation, proposition.  
- Étapes:  
  1) Créer/éditer un document Markdown avec frontmatter minimal conforme.  
  2) Lier les documents cités (`links.cites`).  
  3) Choisir le statut cohérent avec le type (schéma v1).  
  4) Commit (idéalement signé).

- Sorties: document traçable, prêt pour validation automatique.

### 3.2. Validation de métadonnées (CI locale et distante)

- Commande: `python3 scripts/validate_frontmatter.py`  
  - Vérifie YAML, champs obligatoires, formats et liens de base.  
  - Génère un log d’audit: `docs/sprints/SSOT-v1.0/02-evidence/S3_VALIDATION_LOG.txt`.

- Bonne pratique: corriger les erreurs bloquantes avant merge.

### 3.3. Génération du registre (index)

- Commande: `python3 scripts/generate_registry.py`  
  - Produit `docs/_registry/registry.yaml` (SSOT v1.0).  
  - Calcule les SHA256 des fichiers pour suivi d’intégrité.

- Rôle: index central lisible par humain/machine, régénérable à la demande.

### 3.4. Triple-Check v1.1 (si applicable)

- Commande (lecture seule par défaut):  
  `python3 scripts/ssot_registry_check.py --registry-file docs/_registry/registry_v1.1.yaml`  
- Rôles clés:  
  - Couverture vs. répertoires normatifs.  
  - Cohérence id/id_root, formats de hash, previous_hash.  
  - Présence d’entrées requises (ex: RFC-004, OBS-0001..0003).

### 3.5. Publication / Intégration

- Registre et documents versionnés dans Git (branche de travail).  
- Pull Request avec rapports (validation/log) en pièces justificatives.  
- Merge vers la branche principale après revue.

---

## 4. États et Cycles de Vie (Rappel synthétique)

- ADR: Proposition → En discussion → Accepté/Rejeté → Supersédé (immuable une fois accepté).  
- RFC: Ébauche → En discussion → Mature → Accepté/Abandonné (peut devenir ADR).  
- OBS: Ouvert → En observation → Synthétisé → Archivé (vivant jusqu’à « Archivé »).  
- SPRINT_DOC: Planifié → En cours → Terminé → Certifié.

---

## 5. Gouvernance et Impact

- Décision: les ADR acceptés ancrent la gouvernance technique.  
- Transparence: logs d’audit et registres documentent les évolutions.  
- Reproductibilité: scripts standardisés pour mêmes résultats sur postes différents.  
- Auditabilité: preuves générées (logs/rapports) et vérifications (hashes).  
- Sécurité: recommander commits signés GPG pour ADR et gouvernance.

---

## 6. Recommandations de Développement (Roadmap SSOT)

Court terme (Phase Genesis)  
- Généraliser le frontmatter minimal aux documents normatifs prioritaires.  
- Exécuter `validate_frontmatter.py` en CI et corriger les erreurs majeures.  
- Générer et versionner `docs/_registry/registry.yaml` à chaque itération.

Moyen terme (Phase Croissance)  
- Enrichir le registre (graph des relations, auteurs, tags).  
- Ajouter contrôles de cohérence (scripts v1.1) en lecture/rapport.  
- Visualiser le graphe documentaire (outil interne simple).

Long terme (Maturité)  
- Option “living registry” + event-log append-only (audit forensique).  
- Signatures détachées pour ADR critiques (multi-signatures).  
- Interfaces de recherche/observabilité documentaire.

---

## 7. Contrôles de Conformité à Opérer

- Validation frontmatter (obligatoire).  
- Génération du registre (obligatoire).  
- Contrôles v1.1 (si périmètre concerné): structure/coverage/hash.  
- Journalisation des preuves (log de validation dans `docs/sprints/.../02-evidence/`).  

---

## 8. Conclusion

Le SSOT Relinium, centré sur la documentation validée par schémas et preuves d’exécution (logs, hashes), garantit la traçabilité, l’auditabilité et la transparence. L’architecture cible combine:  
- Frontmatter minimal (lisibilité humaine)  
- Registre régénérable (index machine)  
- Contrôles de cohérence (scripts v1.0/v1.1)  
- Gouvernance claire (ADR/RFC/OBS)

Ce cadre permet de faire évoluer la matière documentaire sans perdre l’intention ni la preuve, et prépare la montée en échelle du projet.
