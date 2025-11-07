# S4 — REGISTRY PROTOTYPE

- **id** : `S4-REGISTRY-PROTOTYPE`
- **type** : `SUBSPRINT_DOC`
- **sprint_parent** : `SPRINT-SSOT-V1.0`
- **version** : `1.0.0`
- **status** : `📋 Planifié`
- **created_at** : `2025-01-04T17:25:00Z`
- **effort** : 🟢 Faible (0.5 jour)
- **order** : 4/5
- **depends_on** : `S2-FRONTMATTER-INJECTION`

---

## 🎯 INTENTION

**Créer un prototype de registre central pour démontrer la faisabilité de la Phase 2 (Hybride Frontmatter + Registry).**

---

## 📦 LIVRABLES

1. **Registre YAML** : `docs/_registry/registry.yaml`
   - Index des 6 documents pilotes
   - Métadonnées extraites des frontmatters
   - Relations (graphe documentaire)

2. **Script générateur** : `lab/scripts/generate_registry.py`
   - Parse frontmatters de `docs/`
   - Génère `registry.yaml`
   - Mode : manuel ou automatique (CI)

3. **Documentation** : `docs/_registry/README.md`
   - Rôle du registre
   - Comment le régénérer
   - Structure et format

---

## 📋 MÉTHODOLOGIE

### Structure du registre

```yaml
# docs/_registry/registry.yaml
version: "1.0.0"
generated_at: "2025-01-04T17:00:00Z"
generated_by: "generate_registry.py v1.0"
source: "frontmatter"

statistics:
  total_documents: 6
  by_type:
    ADR: 1
    RFC: 2
    OBS: 3
  by_status:
    Accepté: 1
    "En discussion": 2
    Ouvert: 2
    Synthétisé: 1

documents:
  - id: "ADR-0001"
    path: "docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md"
    type: "ADR"
    title: "Repo driven by docs-first"
    status: "Accepté"
    date: "2025-01-03"
    author: "Équipe Relinium Genesis"
    version: "1.0"
    tags: ["governance", "methodology"]
    links:
      cited_by: ["RFC-001"]
  
  # ... autres documents

relations:
  - from: "RFC-001"
    to: "ADR-0001"
    type: "cites"
    bidirectional: true
```

### Script de génération

```python
#!/usr/bin/env python3
"""Generate registry from frontmatter"""

import yaml
from pathlib import Path
from datetime import datetime

def extract_frontmatter(filepath):
    """Extract YAML frontmatter from Markdown"""
    # Implementation
    pass

def generate_registry(docs_dir, output_file):
    """Generate registry.yaml from all documents"""
    documents = []
    
    # Find all .md files
    for md_file in Path(docs_dir).rglob("*.md"):
        fm = extract_frontmatter(md_file)
        if fm:
            documents.append({
                "id": fm["id"],
                "path": str(md_file),
                "type": fm["type"],
                # ... autres champs
            })
    
    # Generate relations
    relations = build_relations(documents)
    
    # Generate statistics
    stats = compute_statistics(documents)
    
    # Write registry
    registry = {
        "version": "1.0.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "statistics": stats,
        "documents": documents,
        "relations": relations
    }
    
    with open(output_file, 'w') as f:
        yaml.dump(registry, f, default_flow_style=False)

if __name__ == "__main__":
    generate_registry("docs/", "docs/_registry/registry.yaml")
```

---

## ✅ DEFINITION OF DONE

1. ✓ **Registre généré et cohérent**
   - 6 documents indexés
   - Métadonnées complètes
   - Relations correctes

2. ✓ **Script fonctionnel**
   - Génération automatique réussie
   - Pas d'erreurs de parsing
   - Performance < 10 secondes

3. ✓ **Validation croisée**
   - Frontmatter ↔ Registry cohérents
   - Pas de désynchronisation
   - Liens bidirectionnels vérifiés

4. ✓ **Documentation claire**
   - README.md du registre complet
   - Workflow de régénération documenté

---

## 🔍 ÉLÉMENTS DE PREUVE

1. Hash registre : `sha256sum docs/_registry/registry.yaml`
2. Hash script : `sha256sum lab/scripts/generate_registry.py`
3. Rapport cohérence : `02-evidence/S4_registry_coherence.md`
4. Logs génération

---

## 📅 TIMELINE

**Durée** : 0.5 jour (4h)

- Développement script : 2h
- Génération & validation : 1h
- Documentation : 1h

---

**Fin du sous-sprint S4**
