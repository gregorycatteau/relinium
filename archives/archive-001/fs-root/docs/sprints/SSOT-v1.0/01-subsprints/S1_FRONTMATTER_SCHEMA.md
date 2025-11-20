---
id: "SPRINT_DOC-1010"
id_root: "SPRINT_DOC-1010"
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
self_hash: sha256:99c9d1157f0448f8052a7f108289a41369458918fb0ad7b133b44a7236619ab3
---

# S1 — FRONTMATTER SCHEMA

- **id** : `S1-FRONTMATTER-SCHEMA`
- **type** : `SUBSPRINT_DOC`
- **sprint_parent** : `SPRINT-SSOT-V1.0`
- **version** : `1.0.0`
- **status** : `📋 Planifié`
- **created_at** : `2025-01-04T17:22:00Z`
- **effort** : 🟢 Faible (0.5 jour)
- **order** : 1/5

---

## 🎯 INTENTION

### Question à résoudre

**Quel est le schéma minimal et suffisant pour les métadonnées frontmatter qui garantit traçabilité, lisibilité et évolutivité ?**

### Objectifs

1. Définir un schéma YAML minimal (4-5 champs essentiels)
2. Créer un JSON Schema pour validation automatique
3. Documenter le schéma avec exemples
4. Valider le schéma avec l'équipe

---

## 📋 MÉTHODOLOGIE

### Approche

1. **Analyse des besoins** :
   - Extraire les métadonnées actuelles des documents existants
   - Identifier les champs essentiels vs. optionnels
   - S'inspirer des standards (Jekyll, Hugo, Obsidian)

2. **Définition du schéma** :
   - Champs obligatoires (id, type, status, date)
   - Champs optionnels (author, version, tags, links)
   - Types de données et contraintes

3. **Documentation** :
   - Spécification complète du schéma
   - Exemples pour chaque type de document (ADR, RFC, OBS)
   - Guide de contribution

4. **Validation** :
   - JSON Schema pour validation automatique
   - Tests sur exemples
   - Revue avec contributeurs

### Schéma proposé

```yaml
---
# Champs obligatoires (REQUIRED)
id: "ADR-0001"              # Identifiant unique format: TYPE-NNNN
type: "ADR"                 # Type: ADR | RFC | OBS | SPRINT_DOC | POC
status: "Accepté"           # Statut selon type de document
date: "2025-01-03"          # Date création ou dernière maj importante (ISO 8601)

# Champs recommandés (RECOMMENDED)
author: "Équipe Relinium"   # Auteur ou équipe
version: "1.0"              # Version du document (SemVer simplifié)

# Champs optionnels (OPTIONAL)
tags: ["governance", "methodology"]  # Tags pour classification
links:
  cites: []                 # Documents cités
  cited_by: []              # Documents qui citent celui-ci
  supersedes: []            # Documents remplacés
  superseded_by: []         # Document qui remplace celui-ci
---
```

### Contraintes

**Format** :
- YAML valide (parseable par tout parser YAML)
- Délimiteurs `---` obligatoires
- Encodage UTF-8

**Champs obligatoires** :
- `id` : Format `TYPE-NNNN` (ex: ADR-0001, RFC-002, OBS-0003)
- `type` : Valeurs autorisées = ADR | RFC | OBS | SPRINT_DOC | POC
- `status` : Dépend du type (voir statuts par type)
- `date` : Format ISO 8601 (YYYY-MM-DD)

**Statuts par type** :
- **ADR** : "Proposition" | "En discussion" | "Accepté" | "Rejeté" | "Supersédé"
- **RFC** : "Ébauche" | "En discussion" | "Mature" | "Accepté" | "Abandonné"
- **OBS** : "Ouvert" | "En observation" | "Synthétisé" | "Archivé"
- **POC** : "Planned" | "In Progress" | "Complete" | "Failed"
- **SPRINT_DOC** : "Planifié" | "En cours" | "Terminé" | "Certifié"

---

## 📦 LIVRABLES PRÉCIS

### Livrable 1 : Schéma YAML

**Fichier** : `docs/01-genesis/document_schema_v1.yaml`

**Contenu** :
- Spécification complète du schéma
- Documentation inline (commentaires YAML)
- Exemples intégrés

**Exemple** :
```yaml
# Document Schema v1.0 - Relinium SSOT
# Définit la structure des métadonnées frontmatter

schema_version: "1.0.0"
schema_date: "2025-01-04"

required_fields:
  id:
    type: string
    pattern: "^(ADR|RFC|OBS|POC|SPRINT_DOC)-\\d{4}$"
    description: "Identifiant unique du document"
    examples: ["ADR-0001", "RFC-002", "OBS-0003"]
  
  type:
    type: string
    enum: ["ADR", "RFC", "OBS", "POC", "SPRINT_DOC"]
    description: "Type de document"
  
  status:
    type: string
    description: "Statut du document (dépend du type)"
    # Voir statuts_by_type ci-dessous
  
  date:
    type: string
    format: date
    pattern: "^\\d{4}-\\d{2}-\\d{2}$"
    description: "Date de création ou dernière modification majeure"

recommended_fields:
  author:
    type: string
    description: "Auteur ou équipe responsable"
  
  version:
    type: string
    pattern: "^\\d+\\.\\d+(\\.\\d+)?$"
    description: "Version du document (SemVer simplifié)"
    examples: ["1.0", "1.2", "2.0.1"]

optional_fields:
  tags:
    type: array
    items:
      type: string
    description: "Tags de classification"
  
  links:
    type: object
    properties:
      cites: {type: array, items: {type: string}}
      cited_by: {type: array, items: {type: string}}
      supersedes: {type: array, items: {type: string}}
      superseded_by: {type: array, items: {type: string}}

statuts_by_type:
  ADR: ["Proposition", "En discussion", "Accepté", "Rejeté", "Supersédé"]
  RFC: ["Ébauche", "En discussion", "Mature", "Accepté", "Abandonné"]
  OBS: ["Ouvert", "En observation", "Synthétisé", "Archivé"]
  POC: ["Planned", "In Progress", "Complete", "Failed"]
  SPRINT_DOC: ["Planifié", "En cours", "Terminé", "Certifié"]
```

### Livrable 2 : JSON Schema

**Fichier** : `docs/01-genesis/document_schema_v1.json`

**Contenu** : JSON Schema standard pour validation automatique

### Livrable 3 : Documentation

**Fichier** : `docs/01-genesis/FRONTMATTER_GUIDE.md`

**Sections** :
1. Introduction au frontmatter
2. Champs obligatoires et optionnels
3. Exemples par type de document
4. Bonnes pratiques
5. FAQ

### Livrable 4 : Exemples

**Fichiers** : Exemples dans `FRONTMATTER_GUIDE.md`

Exemples pour :
- ADR (3 exemples : Proposition, Accepté, Supersédé)
- RFC (2 exemples : En discussion, Accepté)
- OBS (2 exemples : Ouvert, Synthétisé)

---

## ✅ DEFINITION OF DONE

Le sous-sprint S1 est **terminé** si et seulement si :

1. ✓ **`document_schema_v1.yaml` existe et est valide**
   - Parseable par PyYAML
   - Tous les champs documentés
   - Exemples intégrés

2. ✓ **`document_schema_v1.json` existe et est valide**
   - JSON Schema standard v7+
   - Validation fonctionnelle (testé)

3. ✓ **`FRONTMATTER_GUIDE.md` existe et est complet**
   - Toutes les sections remplies
   - Au moins 7 exemples fournis
   - Lisible par un non-technique

4. ✓ **Validation par l'équipe**
   - Schéma présenté et approuvé
   - Pas de champs manquants critiques
   - Consensus sur le minimal viable

5. ✓ **Tests réussis**
   - Validation JSON Schema fonctionne
   - Exemples parsent correctement
   - Pas d'ambiguïté détectée

---

## 🔍 ÉLÉMENTS DE PREUVE ATTENDUS

### Preuves techniques

1. **Hash SHA256 des fichiers** :
   ```bash
   sha256sum docs/01-genesis/document_schema_v1.yaml
   sha256sum docs/01-genesis/document_schema_v1.json
   sha256sum docs/01-genesis/FRONTMATTER_GUIDE.md
   ```

2. **Test de validation** :
   ```bash
   # Validation JSON Schema
   python -c "import json, jsonschema; ..."
   # Output: PASS / FAIL
   ```

3. **Test de parsing YAML** :
   ```bash
   python -c "import yaml; yaml.safe_load(open('...'))"
   # Output: No errors
   ```

### Preuves documentaires

1. **Commit Git** :
   - Message : "feat(ssot): add frontmatter schema v1.0"
   - Fichiers modifiés : 3
   - Signé GPG (si activé)

2. **Rapport de validation** :
   - Fichier : `docs/sprints/SSOT-v1.0/02-evidence/S1_validation_report.md`
   - Contenu : Résultats tests, hashes, statut

3. **Checklist DoD** :
   - Fichier : `docs/sprints/SSOT-v1.0/02-evidence/S1_dod_checklist.md`
   - Tous les items cochés

---

## ⚠️ RISQUES IDENTIFIÉS

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Schéma trop rigide | 🟠 Moyen | Privilégier champs optionnels |
| Schéma trop laxiste | 🟡 Faible | Champs obligatoires bien choisis |
| Incompatibilité outils | 🟢 Faible | Standards YAML/JSON Schema |
| Rejet par contributeurs | 🟡 Faible | Validation humaine avant finalisation |

---

## 🔗 DÉPENDANCES

### Entrées requises

- DNA-v0.1.yaml (patterns actuels)
- Documents existants (ADR, RFC, OBS) pour inspiration
- Recommandations SSOT_METADATA_EXPLORATION.md

### Sorties produites

- Schéma v1.0 (YAML + JSON Schema)
- Guide frontmatter
- Base pour S2 (injection)

---

## 📅 TIMELINE

**Durée estimée** : 0.5 jour (4h)

| Étape | Durée | Activité |
|-------|-------|----------|
| Analyse | 1h | Extraction métadonnées existantes |
| Définition | 1.5h | Création schéma YAML + JSON Schema |
| Documentation | 1h | Rédaction guide + exemples |
| Validation | 0.5h | Tests + revue humaine |

---

**Fin du sous-sprint S1**
