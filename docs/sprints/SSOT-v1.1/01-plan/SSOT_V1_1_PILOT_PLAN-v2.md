---
id: "SPRINT-SSOT-v1_1-PILOT"
id_root: "SPRINT-SSOT-v1_1-PILOT"
version: "2.0"
type: "SPRINT_DOC"
status: "Active"
title: "Plan de Sprint Pilote SSOT v1.1"
date: "2025-11-06"
scope: "organizational"
pattern: "plan"
decision_type: "execution_plan"
created_at: "2025-11-06T19:15:00Z"
authors:
  - id: "cline"
    role: "author"
roles:
  - name: "Author"
    actor: "Cline"
links:
  supersedes:
    - "docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PILOT_PLAN.md"
  relates_to:
    - "RFC-0004"

previous_hash: "sha256:4635b67272f12f993a22aef7b513afc3d11dcee6776d2cf4ddc7bd14340e4c25"
self_hash: sha256:672151768f0a7a93dab1268f9acd1472844df0e0d1450cc05f87e1b0e83e2343
---

# Plan de Sprint Pilote SSOT v1.1

**ID**: SPRINT-SSOT-v1.1  
**Date**: 2025-11-05  
**Statut**: En cours  
**Responsable**: Greg Catteau

---

## 🎯 Contexte

### Héritage SSOT v1.0

Le sprint SSOT v1.0 a posé les fondations du système documentaire Relinium :
- Schéma v1.0 avec frontmatter structuré (id, type, status, date)
- Scripts de validation (validate_frontmatter.py)
- Registre centralisé (registry.yaml)
- Pipeline CI/CD de validation
- Audit cryptographique (hashes SHA256)

### Évolution vers v1.1

Le **RFC-004-alignment-protocol.md** et les schémas v1.1 introduisent :
- **Succession certifiée** : `previous_hash`, `id_root`, liens `supersedes`
- **Gouvernance renforcée** : `roles`, `decision_type`, `stakeholders`
- **Classification** : `scope` (technical/organizational/ethical), `pattern` (decision/reflection/observation/experiment)
- **Relations enrichies** : `impacts`, `dependencies`, `compliance`

### Objectif du Sprint Pilote

Démontrer la faisabilité d'une migration **strictement non-destructive** en :
1. Ne modifiant AUCUN document existant
2. Créant uniquement des successeurs v1.1
3. Maintenant la traçabilité cryptographique complète
4. Validant le protocole sur un périmètre restreint

---

## 📂 Périmètre

### Répertoire Cible

```
docs/03-architecture/
├── decisions/
│   └── ADR-0001-repo-driven-by-docs-first.md
├── rfcs/
│   ├── RFC-001-choix-stack-initiale.md
│   └── RFC-002-backend-et-composants-scoring-matrix.md
└── observations/
    └── OBS-0003-calibration-et-SLOs.md (optionnel)
```

### Documents Pilotes

Les documents sélectionnés sont fondamentaux pour le projet :

1. **ADR-0001** : Décision architecturale racine (docs-first)
2. **RFC-001** : Choix de stack technique initial
3. **RFC-002** : Architecture backend et composants

Ces 3 documents forment un échantillon représentatif des patterns documentaires.

### Remarque Importante

⚠️ Le script `migrate_to_v1_1.py` utilise un pattern de nommage strict (`ADR-\d{4}\.md`) qui ne correspond pas aux conventions actuelles (`ADR-0001-titre.md`).

**Décision** : Pour ce sprint pilote, la migration sera effectuée **manuellement** pour :
- Respecter les contraintes de nommage existantes
- Démontrer le concept de succession certifiée
- Valider les schémas v1.1 sans modifier l'outillage existant

---

## 🎯 Objectifs Détaillés

### Objectif 1 : Tester le Pipeline de Migration

- ✅ Exécuter le script en mode dry-run
- ✅ Documenter les résultats et limitations
- ✅ Identifier les ajustements nécessaires

### Objectif 2 : Vérifier la Cohérence des Successeurs v1.1

- Créer 2-3 documents successeurs conformes au schéma v1.1
- Valider que tous les champs requis sont présents
- Vérifier les liens de succession (previous_hash, id_root, supersedes)
- Confirmer la conformité avec RFC-004

### Objectif 3 : Valider le Comportement Non-Destructif

- Calculer les hashs des documents originaux **avant** toute action
- Effectuer la migration (création des successeurs)
- Re-calculer les hashs des documents originaux **après**
- **Prouver** qu'aucun document original n'a été modifié

---

## 📋 Étapes d'Exécution

### Phase 1 : Préparation (Dry-Run)

**Livrable** : `MIGRATION_DRY_RUN_REPORT.md`

1. Exécuter le script en mode dry-run :
   ```bash
   python scripts/migrate_to_v1_1.py --dry-run --target docs/03-architecture
   ```

2. Documenter les résultats :
   - Nombre de documents analysés
   - Documents candidats identifiés
   - Frontmatters v1.1 proposés (extraits)
   - Hashs calculés

3. Vérifier qu'AUCUNE écriture disque n'a eu lieu

**Critère de succès** : Rapport dry-run généré et validé

---

### Phase 2 : Exécution Partielle (Succession Effective)

**Livrable** : `MIGRATION_EXECUTION_REPORT.md`

#### Étape 2.1 : Capture des Hashs Originaux

Avant toute modification, capturer les hashs SHA256 :

```bash
sha256sum docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md
sha256sum docs/03-architecture/rfcs/RFC-001-choix-stack-initiale.md  
sha256sum docs/03-architecture/rfcs/RFC-002-backend-et-composants-scoring-matrix.md
```

Enregistrer dans `SSOT_V1_1_HASHES.yaml` (section `original_hashes`).

#### Étape 2.2 : Création Manuelle des Successeurs

Pour chaque document pilote :

1. **Lire** le document original
2. **Calculer** son hash (previous_hash)
3. **Extraire** le frontmatter v1.0
4. **Enrichir** avec les champs v1.1 :
   - `previous_hash` : hash du document original
   - `id_root` : ID sans version (ex: "ADR-0001")
   - `id` : nouvel ID versionné (ex: "ADR-0001-v2")
   - `version` : "2.0" (incrémentation MAJOR)
   - `links.supersedes` : ID du document original
   - `scope` : classification (technical/organizational/ethical)
   - `pattern` : pattern documentaire (decision/reflection/observation)
5. **Créer** le nouveau fichier successeur
6. **Ne jamais toucher** au document original

#### Étape 2.3 : Vérification de Non-Modification

Recalculer les hashs des documents originaux :

```bash
sha256sum docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md
sha256sum docs/03-architecture/rfcs/RFC-001-choix-stack-initiale.md  
sha256sum docs/03-architecture/rfcs/RFC-002-backend-et-composants-scoring-matrix.md
```

**Assertion critique** : Les hashs DOIVENT être identiques à ceux capturés à l'étape 2.1.

---

## 📊 Métriques de Succès

| Métrique | Cible | Mesure |
|----------|-------|--------|
| Documents migrés | ≥ 2 | À compléter |
| Taux de conformité v1.1 | 100% | À compléter |
| Documents originaux modifiés | 0 | À vérifier |
| Hashs cohérents | 100% | À vérifier |

---

## ✅ Definition of Done (DoD)

Le sprint pilote est considéré comme **réussi** si et seulement si :

### ✅ Critère 1 : Dry-Run Documenté

- [ ] `migrate_to_v1_1.py --dry-run` a été exécuté
- [ ] Rapport `MIGRATION_DRY_RUN_REPORT.md` créé et complet
- [ ] Aucune écriture disque effectuée (vérifiable)

### ✅ Critère 2 : Successeurs Créés

- [ ] Au moins 2 documents successeurs v1.1 créés
- [ ] Frontmatters conformes au schéma v1.1.yaml
- [ ] Champs `previous_hash`, `id_root`, `supersedes` présents et corrects

### ✅ Critère 3 : Non-Modification Prouvée

- [ ] Hashs originaux capturés avant migration
- [ ] Hashs originaux recalculés après migration
- [ ] **ÉGALITÉ STRICTE** : `hash_avant == hash_après` pour tous les documents
- [ ] Preuve documentée dans `MIGRATION_EXECUTION_REPORT.md`

### ✅ Critère 4 : Registre v1.1 Cohérent

- [ ] Fichier `registry_v1.1.yaml` créé
- [ ] Au moins une lignée complète (v1.0 → v1.1) documentée
- [ ] Liens de succession corrects et vérifiables

### ✅ Critère 5 : Traçabilité Cryptographique

- [ ] Tous les hashs SHA256 consignés dans `SSOT_V1_1_HASHES.yaml`
- [ ] Cohérence vérifiable entre `previous_hash` et hashs du registre

### ✅ Critère 6 : Validation des Schémas

- [ ] Les nouveaux documents passent la validation du schéma v1.1
- [ ] Pas de régression sur la CI existante
- [ ] Rapport de validation documenté

---

## ⚠️ Contraintes et Limites

### Contraintes Techniques

1. **Ne jamais modifier** un document existant (contenu ou frontmatter)
2. **Ne jamais supprimer** un document existant
3. **Ne jamais renommer** un document existant
4. Toutes les créations doivent être **traçables** dans les rapports

### Limites du Sprint Pilote

1. **Périmètre restreint** : 2-3 documents seulement
2. **Migration manuelle** : script non adapté aux noms de fichiers actuels
3. **Pas de CI automatisée** pour v1.1 (validation manuelle)
4. **Registre v1.1 distinct** : pas de fusion avec registry.yaml v1.0

---

## 🔄 Processus de Validation

### Validation Technique

```bash
# 1. Validation du schéma v1.1
python -c "
import json, jsonschema, yaml
schema = json.load(open('docs/01-genesis/document_schema_v1.1.json'))
doc = yaml.safe_load(open('ADR-0001-repo-driven-by-docs-first-v2.md').read().split('---')[1])
jsonschema.validate(doc, schema)
print('✅ Document conforme v1.1')
"

# 2. Vérification de non-modification
sha256sum ADR-0001-repo-driven-by-docs-first.md  # Comparer avec hash initial
```

### Validation Humaine

- [ ] Revue du frontmatter par un pair
- [ ] Vérification de la cohérence des liens
- [ ] Validation de la lisibilité du contenu

---

## 🎯 Prochaines Étapes

Après validation du sprint pilote :

1. **Ajuster le script** `migrate_to_v1_1.py` pour supporter les noms de fichiers actuels
2. **Automatiser** la validation des schémas v1.1 dans la CI
3. **Étendre** la migration au reste du corpus documentaire
4. **Fusionner** registry.yaml v1.0 et registry_v1.1.yaml

---

## 📝 Notes

- Ce plan est un document vivant, mis à jour au fil du sprint
- Toute décision majeure doit être documentée dans un ADR
- En cas de doute, privilégier la **sécurité** (ne rien exécuter)

---

**Signature** : Greg Catteau  
**Date** : 2025-11-05  
**Version** : 1.0
