---
id: "SPRINT_DOC-1042"
id_root: "SPRINT_DOC-1042"
type: "SPRINT_DOC"
status: "Terminé"

date: "2025-01-05"
author: "Relinium Genesis Team"
version: "1.0.0"
scope: "organizational"
pattern: "observation"
tags:
  - "ssot"
  - "v1.0"
previous_hash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
self_hash: sha256:aa24fce2e0165abf7c829bf36357520bcede4c81b77bb73417c845bbc27613bb
---

# Prompt Next : Migration Complète du Corpus

Ce prompt sera utilisé pour migrer l'ensemble du corpus documentaire après validation de la Phase 2.

---

## 📋 PROMPT POUR CLINE

```
Mission : Migrer l'ensemble du corpus documentaire vers le SSOT complet

Contexte :
- Phase 1 certifiée (Frontmatter sur 6 docs pilotes)
- Phase 2 certifiée (Hybride + Registry)
- Outillage CI opérationnel et testé
- Prêt pour migration à grande échelle

Objectifs :

1. Migration exhaustive
   - Ajouter frontmatter YAML à TOUS les documents docs/
   - Documents gouvernance racine (README, CONTRIBUTING, etc.)
   - Documents lab/ (POC triptyques, manifest)
   - Total estimé : ~110 documents

2. Génération registry complet
   - docs/_registry/registry.yaml avec tous les documents
   - Graphe de relations complet
   - Statistiques détaillées

3. Validation globale
   - CI valide 100% des documents
   - Aucun lien brisé
   - Cohérence frontmatter ↔ registry

4. Documentation contributeurs
   - Guide complet workflow frontmatter
   - Procédures validation
   - FAQ étendue

Phases d'exécution :

Phase A : Gouvernance (8 docs racine)
- README.md, CONTRIBUTING.md, GOVERNANCE.md, etc.
- Frontmatter + validation

Phase B : Architecture (docs/03-architecture/)
- Complétion ADR, RFC, OBS restants
- Vérification liens

Phase C : POCs (lab/pocs/ - 81 docs)
- Triptyques POC/RESULTS/SECURITY
- Métadonnées uniformes

Phase D : Autres domaines
- docs/06-ops/, docs/observatory/, etc.
- Documents divers

Phase E : Validation finale
- Registry global régénéré
- CI passe sur tout
- Certification migration

Livrables :
- ~110 documents avec frontmatter
- Registry complet et validé
- Rapport de migration
- Certification globale

Durée estimée : 1-2 semaines

Critères de succès :
- 100% des documents ont frontmatter valide
- CI passe sans erreur
- Registry cohérent
- Performance CI < 2 minutes
- Aucune régression lisibilité

Risques :
- Volume important (automatisation nécessaire)
- Merge conflicts si contributions parallèles
- Performance CI à surveiller
- Fatigue validation humaine

Mitigation :
- Automatiser l'injection frontmatter
- Batches de 10-20 documents
- Validation par batch
- Pauses entre batches
```

---

**Utiliser après Phase 2 pour migration finale**
