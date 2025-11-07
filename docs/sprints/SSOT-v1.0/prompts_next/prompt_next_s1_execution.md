# Prompt Next : Exécution S1 - Frontmatter Schema

Ce prompt sera utilisé après validation humaine du plan global pour exécuter le sous-sprint S1.

---

## 📋 PROMPT POUR CLINE

```
Mission : Exécuter le sous-sprint S1 - Frontmatter Schema du sprint SSOT v1.0

Contexte :
- Le plan global SPRINT_GLOBAL_PLAN.md a été validé
- Le sous-sprint S1_FRONTMATTER_SCHEMA.md définit les objectifs
- Tu dois créer le schéma de validation des frontmatters

Livrables à produire :

1. docs/01-genesis/document_schema_v1.yaml
   - Schéma YAML complet avec tous les champs
   - Documentation inline (commentaires)
   - Exemples intégrés

2. docs/01-genesis/document_schema_v1.json
   - JSON Schema standard (draft-07)
   - Validation de structure
   - Types et contraintes

3. docs/01-genesis/FRONTMATTER_GUIDE.md
   - Guide complet frontmatter
   - Exemples pour ADR, RFC, OBS
   - FAQ et bonnes pratiques

4. docs/sprints/SSOT-v1.0/02-evidence/S1_validation_report.md
   - Tests de validation
   - Hashes SHA256 des 3 fichiers
   - Logs de validation

Contraintes :
- Schéma minimal : id, type, status, date (obligatoires)
- Champs recommandés : author, version
- Champs optionnels : tags, links
- Format date : ISO 8601 (YYYY-MM-DD)
- Statuts selon DNA-v0.1.yaml

Validation :
- Parser YAML doit réussir
- JSON Schema doit être valide
- Au moins 7 exemples dans le guide
- Tous les types documentaires couverts

DoD (5 critères) :
1. document_schema_v1.yaml existe et est valide
2. document_schema_v1.json existe et est valide
3. FRONTMATTER_GUIDE.md existe et est complet
4. Validation équipe (à demander explicitement)
5. Tests réussis (parsing + validation)

Après complétion :
- Générer le rapport S1_validation_report.md
- Calculer les hashes SHA256
- Attendre validation humaine avant S2
```

---

**Utiliser ce prompt après validation du plan global**
