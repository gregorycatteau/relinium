# Sprint Pilote SSOT v1.1 – Migration Documentaire Non-Destructive

## 🎯 Objectif

Démonstration pilote de la migration vers le schéma documentaire v1.1 en appliquant strictement le principe de **succession certifiée** : aucun document existant ne sera modifié, seuls de nouveaux documents successeurs seront créés.

## 📋 Principe Directeur

> **"La migration n'est pas une purge, c'est un acte de filiation :  
> chaque nouveau document atteste de ceux qui l'ont précédé."**

## 📂 Structure du Sprint

```
SSOT-v1.1/
├── README.md                    # Ce fichier
├── 01-plan/
│   └── SSOT_V1_1_PILOT_PLAN.md # Plan détaillé du sprint
├── 02-evidence/
│   ├── MIGRATION_DRY_RUN_REPORT.md
│   └── MIGRATION_EXECUTION_REPORT.md
└── 03-validation/
    ├── SSOT_V1_1_PROGRESS.yaml
    └── SSOT_V1_1_HASHES.yaml
```

## 🔗 Références

- **RFC-004**: [Protocole d'Alignement](../../03-architecture/rfcs/RFC-004-alignment-protocol.md)
- **Schéma v1.1 YAML**: [document_schema_v1.1.yaml](../../01-genesis/document_schema_v1.1.yaml)
- **Schéma v1.1 JSON**: [document_schema_v1.1.json](../../01-genesis/document_schema_v1.1.json)
- **Script de migration**: [migrate_to_v1_1.py](../../../scripts/migrate_to_v1_1.py)

## ⚖️ Contraintes Absolues

1. ✅ **Non-destructif** : Aucun fichier existant ne sera modifié
2. ✅ **Traçabilité** : Chaque création documentée avec hash
3. ✅ **Réversibilité** : Possibilité logique de revenir en arrière
4. ✅ **Succession** : Liens explicites previous_hash/id_root

## 📊 Statut

**Date de démarrage** : 2025-11-05  
**Phase** : En cours  
**Périmètre** : docs/03-architecture (pilote)
