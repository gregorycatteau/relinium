# S3 — VALIDATION CI TOOLING

- **id** : `S3-VALIDATION-CI`
- **type** : `SUBSPRINT_DOC`
- **sprint_parent** : `SPRINT-SSOT-V1.0`
- **version** : `1.0.0`
- **status** : `📋 Planifié`
- **created_at** : `2025-01-04T17:24:00Z`
- **effort** : 🟡 Moyen (1-2 jours)
- **order** : 3/5
- **depends_on** : `S1-FRONTMATTER-SCHEMA`, `S2-FRONTMATTER-INJECTION`

---

## 🎯 INTENTION

**Créer l'outillage de validation automatique des frontmatters pour garantir la conformité du corpus documentaire.**

---

## 📦 LIVRABLES

1. **Script Python** : `lab/scripts/validate_frontmatter.py`
   - Parse tous les fichiers `.md` dans `docs/`
   - Extrait et valide frontmatter contre schéma
   - Retourne : PASS / FAIL / WARN avec détails

2. **GitHub Action** : `.github/workflows/validate-frontmatter.yml`
   - Trigger : Push, PR sur `docs/**`
   - Exécute `validate_frontmatter.py`
   - Bloque merge si FAIL

3. **Documentation** : `docs/07-contrib/frontmatter-validation-guide.md`
   - Comment fonctionne la validation
   - Interpréter les erreurs
   - Corriger les problèmes courants

---

## 📋 MÉTHODOLOGIE

### Architecture du script

```python
#!/usr/bin/env python3
"""
Validate frontmatter in Markdown documents.
Checks:
1. Frontmatter exists and is valid YAML
2. Required fields present (id, type, status, date)
3. Field values match schema constraints
4. Links are bidirectional (cited_by ↔ cites)
"""

import yaml
import json
import jsonschema
from pathlib import Path

def validate_document(filepath):
    """Validate frontmatter of a single document"""
    # Extract frontmatter
    # Parse YAML
    # Validate against JSON Schema
    # Check business rules
    return result  # PASS / FAIL / WARN

def validate_corpus(docs_dir):
    """Validate all documents in corpus"""
    # Find all .md files
    # Validate each
    # Check cross-references
    return summary

if __name__ == "__main__":
    result = validate_corpus("docs/")
    print(result)
    exit(0 if result.passed else 1)
```

### Validations implémentées

**Niveau 1 : Structure**
- ✓ Frontmatter existe
- ✓ YAML valide (parseable)
- ✓ Délimiteurs `---` corrects

**Niveau 2 : Schéma**
- ✓ Champs obligatoires présents
- ✓ Types de données corrects
- ✓ Formats respectés (id, date)

**Niveau 3 : Cohérence**
- ✓ Statut valide pour le type
- ✓ Liens bidirectionnels (cites ↔ cited_by)
- ✓ Documents référencés existent

**Niveau 4 : Qualité** (warnings)
- ⚠️ Champs recommandés absents
- ⚠️ Tags vides
- ⚠️ Version non SemVer

---

## ✅ DEFINITION OF DONE

1. ✓ **Script Python fonctionnel**
   - Valide les 6 documents pilotes
   - Détecte incohérences
   - Exit code 0/1 approprié

2. ✓ **GitHub Action opérationnelle**
   - Workflow CI exécuté
   - Logs clairs et actionnables
   - Intégration avec status checks

3. ✓ **Documentation complète**
   - Guide validation créé
   - Exemples d'erreurs et corrections
   - FAQ intégrée

4. ✓ **Tests passent**
   - CI passe sur documents pilotes
   - Détection d'erreurs volontaires fonctionne
   - Performance < 30 secondes

---

## 🔍 ÉLÉMENTS DE PREUVE

1. Hash script : `sha256sum lab/scripts/validate_frontmatter.py`
2. Logs CI : Capture exécution GitHub Action
3. Rapport validation : `02-evidence/S3_ci_validation_report.md`
4. Tests unitaires : Résultats tests sur cas d'erreur

---

## 📅 TIMELINE

**Durée** : 1-2 jours

- Développement script : 4-6h
- GitHub Action : 2h
- Documentation : 2h
- Tests & debug : 2-4h

---

**Fin du sous-sprint S3**
