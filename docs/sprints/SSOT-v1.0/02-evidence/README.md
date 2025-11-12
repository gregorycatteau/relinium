---
id: "SPRINT_DOC-1020"
id_root: "SPRINT_DOC-1020"
type: "SPRINT_DOC"
status: "Terminé"

date: "2025-01-05"
author: "Relinium Genesis Team"
version: "1.0.0"
scope: "organizational"
pattern: "experiment"
tags:
  - "ssot"
  - "v1.0"
previous_hash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
self_hash: sha256:446823824f4b130311533e739dfc84305ff26ae3b7a1cb90be6eac63d41a6829
---

# Evidence Directory — Dossier de Preuves

Ce répertoire contiendra les **éléments de preuve** de chaque sous-sprint du SSOT v1.0.

## 📋 Structure attendue

Après exécution du sprint, ce dossier contiendra :

```
02-evidence/
├── README.md                      [Ce fichier]
├── MASTER_CHECKLIST.md            [Checklist globale tous DoD]
├── S1_validation_report.md        [Preuves S1 - Schéma]
├── S2_injection_report.md         [Preuves S2 - Injection]
├── S3_ci_validation_report.md     [Preuves S3 - CI]
├── S4_registry_coherence.md       [Preuves S4 - Registry]
├── S5_audit_trail.md              [Preuves S5 - Audit]
└── HASHES.txt                     [Tous les hashes SHA256]
```

## 🔍 Contenu type d'un rapport de preuve

Chaque `SX_*.md` doit contenir :

1. **Identifiant** : ID du sous-sprint
2. **Timestamp** : Date et heure de génération
3. **Livrables** : Liste des fichiers produits avec hashes
4. **Tests** : Résultats de validation (PASS/FAIL/WARN)
5. **Logs** : Sorties pertinentes (CI, scripts, etc.)
6. **Conclusion** : DoD atteint ou non

## 📊 Format de HASHES.txt

```
# Sprint SSOT v1.0 - Hashes SHA256
# Generated: 2025-01-XX

# Sous-sprint S1
abc123... docs/01-genesis/document_schema_v1.yaml
def456... docs/01-genesis/document_schema_v1.json
ghi789... docs/01-genesis/FRONTMATTER_GUIDE.md

# Sous-sprint S2
jkl012... docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md
mno345... docs/03-architecture/rfcs/RFC-001-choix-stack-initiale.md
# ... (6 documents)

# Sous-sprint S3
pqr678... lab/scripts/validate_frontmatter.py
stu901... .github/workflows/validate-frontmatter.yml

# Sous-sprint S4
vwx234... docs/_registry/registry.yaml
yza567... lab/scripts/generate_registry.py

# Hash global sprint
GLOBAL: [hash de tous les livrables concaténés]
```

---

**Ce dossier sera rempli durant l'exécution du sprint**
