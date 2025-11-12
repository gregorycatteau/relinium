---
id: "SPRINT_DOC-1011"
id_root: "SPRINT_DOC-1011"
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
self_hash: sha256:13f225999574077c120c23ddaee7761a2e811d21c3e0dc246e66bd0e37324532
---

# S2 — FRONTMATTER INJECTION PILOTE

- **id** : `S2-FRONTMATTER-INJECTION`
- **type** : `SUBSPRINT_DOC`
- **sprint_parent** : `SPRINT-SSOT-V1.0`
- **version** : `1.0.0`
- **status** : `📋 Planifié`
- **created_at** : `2025-01-04T17:23:00Z`
- **effort** : 🟡 Moyen (1 jour)
- **order** : 2/5
- **depends_on** : `S1-FRONTMATTER-SCHEMA`

---

## 🎯 INTENTION

**Valider l'applicabilité du schéma frontmatter sur un échantillon représentatif de documents sans dégrader la lisibilité.**

### Objectifs

1. Ajouter frontmatter YAML aux 6 documents pilotes
2. Préserver 100% de la lisibilité
3. Garantir cohérence avec schéma v1.0
4. Documenter le workflow d'ajout

---

## 📦 DOCUMENTS PILOTES

### Liste des 6 documents

| # | Document | Type | Statut actuel | Complexité |
|---|----------|------|---------------|------------|
| 1 | `docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md` | ADR | Accepté | 🟢 Simple |
| 2 | `docs/03-architecture/rfcs/RFC-001-choix-stack-initiale.md` | RFC | En discussion | 🟡 Moyen |
| 3 | `docs/03-architecture/rfcs/RFC-002-backend-et-composants-scoring-matrix.md` | RFC | En discussion | 🟡 Moyen |
| 4 | `docs/03-architecture/observations/OBS-0001-backend-composants-inventaire.md` | OBS | Synthétisé | 🟢 Simple |
| 5 | `docs/03-architecture/observations/OBS-0002-tests-initiaux.md` | OBS | Ouvert | 🟢 Simple |
| 6 | `docs/03-architecture/observations/OBS-0003-calibration-et-SLOs.md` | OBS | Ouvert | 🟢 Simple |

---

## 📋 MÉTHODOLOGIE

### Processus d'injection

**Pour chaque document** :

1. **Lecture** : Extraire métadonnées actuelles (en-tête manuel)
2. **Conversion** : Transformer en frontmatter YAML conforme schéma
3. **Injection** : Ajouter frontmatter en tête de fichier
4. **Vérification** : Parser YAML, valider schéma, vérifier lisibilité
5. **Commit** : Message descriptif, signé si possible

### Template d'injection

```yaml
---
id: "ADR-0001"
type: "ADR"
status: "Accepté"
date: "2025-01-03"
author: "Équipe Relinium Genesis"
version: "1.0"
tags: ["governance", "methodology", "founding"]
links:
  cites: []
  cited_by: ["RFC-001"]
  supersedes: []
---

# ADR-0001 — Repo driven by docs-first

[Contenu inchangé du document...]
```

---

## ✅ DEFINITION OF DONE

1. ✓ **6 documents modifiés avec frontmatter valide**
2. ✓ **Parsing YAML réussi pour tous**
3. ✓ **Validation schéma passée pour tous**
4. ✓ **Lisibilité préservée** (revue humaine)
5. ✓ **Liens bidirectionnels corrects** (cites ↔ cited_by cohérents)
6. ✓ **Commits Git propres** (1 commit par document ou 1 commit groupé)

---

## 🔍 ÉLÉMENTS DE PREUVE

1. **Hashes SHA256** des 6 fichiers modifiés
2. **Logs de validation YAML** (tous PASS)
3. **Diff Git** montrant les changements
4. **Screenshot** ou capture lisibilité préservée
5. **Rapport d'injection** : `02-evidence/S2_injection_report.md`

---

## ⚠️ RISQUES

| Risque | Mitigation |
|--------|------------|
| Corruption fichier | Backup avant modification |
| Frontmatter trop verbeux | Utiliser champs obligatoires uniquement si doute |
| Désync contenu | Parser après chaque injection |

---

## 📅 TIMELINE

**Durée** : 1 jour (8h)

- Préparation : 1h
- Injection doc 1-3 : 3h
- Injection doc 4-6 : 2h
- Validation & tests : 1.5h
- Documentation : 0.5h

---

**Fin du sous-sprint S2**
