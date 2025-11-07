# Prompt Next : Phase 2 - Hybride Frontmatter + Registry

Ce prompt sera utilisé après certification du Sprint v1.0 pour déployer la Phase 2.

---

## 📋 PROMPT POUR CLINE

```
Mission : Déployer la Phase 2 du SSOT - Hybride Frontmatter + Registry

Contexte :
- Sprint SSOT v1.0 certifié (Phase 1 complète)
- 6 documents pilotes ont frontmatter YAML
- Validation CI opérationnelle
- Registry prototype existe

Objectifs Phase 2 :

1. Migration corpus complet
   - Ajouter frontmatter à TOUS les documents docs/
   - Préserver frontmatter minimal (id, type, status, date)
   - Validation continue via CI

2. Registry automatisé
   - Script génération registry depuis frontmatters
   - Enrichissement : checksums, relations, tags
   - Génération automatique en CI

3. Recherche et navigation
   - CLI de recherche par métadonnées
   - Visualisation graphe documentaire (optionnel)
   - Interface web simple (optionnel)

4. Signatures pour ADR critiques
   - Implémenter fichiers .signatures
   - Workflow de signature multi-parties
   - Validation signatures en CI

Livrables :
- Corpus complet avec frontmatters (~110 documents)
- docs/_registry/registry.yaml automatisé
- lab/scripts/search_docs.py (CLI recherche)
- .github/workflows/generate-registry.yml
- docs/07-contrib/signatures-workflow.md

Durée estimée : 2-3 semaines

Basé sur :
- SSOT_METADATA_EXPLORATION.md (Approche E - score 33/44)
- SSOT_V1_CERTIFICATION.md (leçons apprises Phase 1)
- Hypothèse 10.4 : Git-as-Truth + Lightweight Registry
```

---

**Utiliser après certification SSOT v1.0**
