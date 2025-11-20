---
id: OBS-0102
type: OBS
status: Synthétisé
date: '2025-11-08'
author: Équipe Relinium Genesis
version: '1.0'
tags:
- ssot
- governance
- policy
- signatures
links:
  cites:
  - OBS-0100
  - OBS-0101
  - ADR-0001
id_root: OBS-0102
scope: organizational
pattern: observation
self_hash: sha256:2bc32f54240075b26f3162a9902767336360a294a540cd35da8fa9ea89bb06fc
---

# SSOT_GOVERNANCE_FOUNDATIONS — Fondations de la gouvernance documentaire

- **Statut** : 🔍 Modélisation conceptuelle
- **Date** : 2025-01-04
- **Auteur** : Agent d'exploration documentaire
- **Version** : 1.0
- **Source** : OBS-SSOT-EXPLORATION.md + DNA-v0.1.yaml + SSOT_SCENARIOS_EXPLORATION.md

---

## 🎯 Objectif

Ce document définit ce que signifie **"inviolabilité"** dans un contexte documentaire vivant, et propose un canevas conceptuel pour une future politique de signature et de registre documentaire.

**Principe directeur** : La gouvernance documentaire doit permettre la traçabilité absolue tout en préservant la flexibilité nécessaire à l'évolution du projet.

---

## 1️⃣ INVIOLABILITÉ DANS UN CONTEXTE VIVANT

### 1.1 Définition de l'inviolabilité documentaire

**Inviolabilité ≠ Immutabilité absolue**

L'inviolabilité documentaire dans Relinium signifie :
- **Traçabilité totale** : Toute modification est enregistrée et justifiée
- **Intentionnalité préservée** : L'intention originelle reste accessible
- **Audit possible** : L'historique est reconstructible et vérifiable
- **Révocabilité documentée** : Les changements sont explicites, pas secrets

**Ce n'est PAS** :
- Blocage de toute modification (rigidité mortifère)
- Perfection imposée (erreur est humaine)
- Censure des erreurs (l'erreur a valeur pédagogique)

### 1.2 Quand un document cesse-t-il d'être modifiable ?

#### **Documents figés par nature (ADR acceptés)**

**Règle** : Un ADR accepté devient immuable dans son contenu

**Exceptions autorisées** :
1. **Corrections mineures** (typos, formatage)
   - Sans validation formelle
   - Documentées en commentaire Git
   
2. **Clarifications** (ambiguïtés détectées)
   - Avec validation via RFC si impact significatif
   - Ajout d'une section "Clarifications" datée
   
3. **Supersession** (nouvelle décision remplace l'ancienne)
   - ADR original marqué "Supersédé par ADR-XXXX"
   - Nouvel ADR référence explicitement l'ancien
   - Les deux coexistent dans l'historique

**Contre-exemples (modifications interdites)** :
- Changer la décision prise
- Réécrire les alternatives évaluées
- Modifier les conséquences identifiées
- Supprimer le document

#### **Documents vivants par nature (OBS, RFC en discussion)**

**Règle** : Ces documents peuvent évoluer librement tant qu'ils n'ont pas atteint un état terminal

**Gestion des versions** :
- Incrément de version à chaque modification substantielle
- Section "Historique des modifications" en bas de document
- Possibilité de snapshot si besoin (ex: OBS-XXXX-v2.0 vs v3.0)

**Transition vers l'immutabilité** :
- OBS → "Synthétisé" : Fige les constats, mais synthèse peut encore évoluer
- OBS → "Archivé" : Figé totalement
- RFC → "Accepté" : Se transforme en ADR (donc devient immuable)

#### **Documents de gouvernance (GOVERNANCE.md, SECURITY.md, etc.)**

**Règle** : Modifiables mais avec processus formel

**Processus** :
1. Modification proposée via RFC
2. Discussion communautaire (durée selon impact)
3. Validation formelle (selon GOVERNANCE.md)
4. ADR documente le changement de gouvernance
5. Document racine mis à jour avec référence à l'ADR

**Historique** :
- Git blame pour historique technique
- Section "Historique des révisions" dans le document
- Chaque révision majeure actée par ADR

### 1.3 Quelle est la valeur d'une erreur préservée ?

#### **L'erreur comme artefact pédagogique**

**Principe** : Une erreur documentée est plus précieuse qu'une perfection factice

**Valeurs d'une erreur préservée** :
1. **Apprentissage collectif** : Évite de refaire la même erreur
2. **Transparence** : Montre l'honnêteté du processus
3. **Traçabilité** : Comprendre le cheminement de pensée
4. **Humilité** : Rappelle que l'erreur est humaine et acceptable

**Comment préserver l'erreur ?** :
- Ne jamais supprimer un ADR, même erroné
- Marquer "Supersédé" ou "Erroné" avec explication
- Créer un nouvel ADR qui corrige l'erreur
- Documenter ce qui a été appris

#### **L'erreur vs. la faute**

**Erreur** (acceptable) :
- Décision basée sur informations incomplètes
- Hypothèse invalidée par l'expérience
- Choix technique devenu obsolète
→ **Action** : Documenter, apprendre, corriger

**Faute** (non acceptable) :
- Décision prise sans analyse
- Information connue mais ignorée
- Négligence volontaire
→ **Action** : Post-mortem, processus amélioré, responsabilité assumée

### 1.4 Comment relier intention, action et trace sans rigidité ?

#### **Le triptyque Intention → Action → Trace**

```
INTENTION (Pourquoi)
    ↓
    RFC (Proposition)
    ↓
ACTION (Quoi)
    ↓
    ADR (Décision) + Code (Implémentation)
    ↓
TRACE (Vérifiabilité)
    ↓
    Git History + Signatures + Registre
```

#### **Flexibilité vs. Traçabilité**

**Zones flexibles** :
- OBS peut évoluer librement (vivant par nature)
- RFC peut pivoter pendant discussion
- POC peut itérer sans process lourd

**Zones tracées** :
- Décisions (ADR) sont actées formellement
- Modifications de gouvernance nécessitent RFC
- Changements structurels documentés explicitement

**Éviter la rigidité** :
- Process léger pour petites décisions (ADR court autorisé)
- "Fast track" possible pour urgences sécuritaires
- Rétrospectives régulières pour améliorer le process lui-même

---

## 2️⃣ CANEVAS POUR SIGNATURE ET REGISTRE

### 2.1 Modélisation conceptuelle (non déployée)

#### **Objectif d'un système de signature**

1. **Authentifier l'auteur** : Qui a pris cette décision ?
2. **Dater précisément** : Quand exactement ?
3. **Garantir l'intégrité** : Le document n'a pas été altéré ?
4. **Faciliter l'audit** : Retrouver rapidement l'historique complet

#### **Objectif d'un registre documentaire**

1. **Index central** : Tous les documents référencés
2. **Métadonnées exploitables** : Statut, type, liens, auteur, date
3. **Graph de relations** : ADR ← RFC ← OBS visualisable
4. **Recherche avancée** : Par métadonnées, par contenu, par auteur

### 2.2 Options techniques pour la signature

#### **Option A : Git Commit Signing (déjà utilisé)**

**Avantages** :
- ✅ Déjà en place (GOVERNANCE.md mentionne commits signés)
- ✅ Standard industriel (GPG)
- ✅ Intégré à GitHub
- ✅ Traçabilité native via git log

**Limites** :
- ⚠️ Signe le commit, pas le document spécifiquement
- ⚠️ Complexité pour non-techniciens (gestion clés GPG)
- ⚠️ Pas de signature au niveau contenu (hash du fichier)

**Recommandation** : **Maintenir et renforcer**
- Rendre obligatoire pour tous les mainteneurs
- Documenter la procédure (docs/07-contrib/gpg-setup.md)
- Vérifier les signatures en CI

#### **Option B : Frontmatter avec hash de contenu**

**Principe** : Chaque document inclut son propre hash

```yaml
---
title: "ADR-0001 Repo driven by docs-first"
status: "Accepté"
date: "2025-01-03"
author: "Équipe Relinium Genesis"
version: "1.0"
content_hash: "sha256:7d8e9f..."
signed_by: "greg@relinium.io"
signature: "gpg:BEGIN PGP SIGNATURE..."
---
```

**Avantages** :
- ✅ Hash au niveau document
- ✅ Vérification automatisable (CI peut vérifier hash)
- ✅ Métadonnées structurées (exploitables par scripts)

**Limites** :
- ⚠️ Hash doit être recalculé à chaque modif
- ⚠️ Signature GPG complexe à intégrer dans frontmatter
- ⚠️ Peut alourdir les documents

**Recommandation** : **Envisageable phase future**
- Commencer avec frontmatter sans hash (métadonnées seules)
- Ajouter hash automatiquement via pre-commit hook
- Signature GPG reste au niveau Git

#### **Option C : Registre centralisé avec signatures**

**Principe** : Un registre (YAML ou SQLite) centralise les métadonnées et signatures

```yaml
# docs/_registry/registry.yaml
documents:
  - id: "ADR-0001"
    path: "docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md"
    type: "ADR"
    status: "Accepté"
    author: "Équipe Relinium Genesis"
    date: "2025-01-03"
    version: "1.0"
    content_hash: "sha256:7d8e9f..."
    git_commit: "a1b2c3d..."
    signed_by: "greg@relinium.io"
    links:
      - type: "cited_by"
        target: "RFC-001"
```

**Avantages** :
- ✅ Source unique de vérité pour métadonnées
- ✅ Recherche et navigation facilitées
- ✅ Graph de relations exploitable
- ✅ Audit centralisé

**Limites** :
- ⚠️ Point de défaillance unique (registre corrompu = catastrophe)
- ⚠️ Maintenance : registre doit rester synchronisé avec fichiers
- ⚠️ Complexité : nécessite outillage dédié

**Recommandation** : **À développer progressivement**
- Phase 1 : Registre simple (index uniquement, sans signatures)
- Phase 2 : Ajout métadonnées structurées
- Phase 3 : Ajout hashes et signatures si besoin réel

#### **Option D : Blockchain documentaire (maximaliste)**

**Principe** : Chaque document est un bloc dans une chaîne

**Avantages** :
- ✅ Immutabilité cryptographique absolue
- ✅ Traçabilité totale et vérifiable
- ✅ Décentralisation possible

**Limites** :
- 🔴 Sur-ingénierie extrême pour un projet Genesis
- 🔴 Complexité technique disproportionnée
- 🔴 Performance (chaque lecture = vérification chaîne ?)
- 🔴 Pas de flexibilité (contradiction avec "vivant")

**Recommandation** : **Non pertinent pour Relinium**
- Overkill pour les besoins actuels
- Git + signatures GPG suffisent largement
- Si besoin de blockchain : projet séparé

### 2.3 Architecture proposée pour le registre

#### **Structure recommandée**

```
docs/_registry/
├── registry.yaml           [Index central de tous les documents]
├── graph.json              [Graph des relations entre documents]
├── schemas/                [Schémas de validation]
│   ├── adr-schema.yaml
│   ├── rfc-schema.yaml
│   └── obs-schema.yaml
└── scripts/                [Outils de maintenance]
    ├── validate.sh         [Vérification cohérence]
    ├── gen-graph.py        [Génération du graph]
    └── update-registry.sh  [Mise à jour automatique]
```

#### **Contenu minimal du registre**

```yaml
# docs/_registry/registry.yaml
version: "1.0.0"
last_updated: "2025-01-04T15:00:00Z"
documents:
  - id: "ADR-0001"
    type: "ADR"
    path: "docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md"
    title: "Repo driven by docs-first"
    status: "Accepté"
    author: "Équipe Relinium Genesis"
    date: "2025-01-03"
    version: "1.0"
    git_commit: "1073f0c8"  # Référence au commit Git
    tags: ["governance", "methodology", "founding"]
    links:
      cited_by: ["RFC-001"]
      supersedes: []
  
  - id: "RFC-001"
    type: "RFC"
    path: "docs/03-architecture/rfcs/RFC-001-choix-stack-initiale.md"
    title: "Choix de stack initiale"
    status: "En discussion"
    author: "Équipe Relinium Genesis"
    date: "2025-01-03"
    version: "1.0"
    git_commit: "1073f0c8"
    tags: ["architecture", "stack", "decision"]
    links:
      cites: ["ADR-0001"]
      may_become: ["ADR-0002", "ADR-0003", "ADR-0004"]

```

#### **Validation automatique du registre**

```bash
# docs/_registry/scripts/validate.sh

#!/bin/bash
# Valide la cohérence du registre

# 1. Vérifier que tous les documents listés existent
# 2. Vérifier que tous les liens référencent des documents existants
# 3. Vérifier que les métadonnées correspondent aux frontmatters
# 4. Vérifier qu'aucun document manque dans le registre
# 5. Générer rapport de validation

echo "✅ Registre valide" || echo "❌ Erreurs détectées"
```

#### **Génération automatique du graph**

```python
# docs/_registry/scripts/gen-graph.py

import yaml
import json

def generate_graph(registry_path):
    """Génère un graph JSON des relations entre documents"""
    with open(registry_path) as f:
        registry = yaml.safe_load(f)
    
    graph = {
        "nodes": [],
        "edges": []
    }
    
    for doc in registry["documents"]:
        graph["nodes"].append({
            "id": doc["id"],
            "type": doc["type"],
            "status": doc["status"],
            "title": doc["title"]
        })
        
        for link_type, targets in doc.get("links", {}).items():
            for target in targets:
                graph["edges"].append({
                    "from": doc["id"],
                    "to": target,
                    "type": link_type
                })
    
    return graph
```

### 2.4 Politique de signature (proposition)

#### **Niveaux de signature**

| Niveau | Qui | Quoi | Comment |
|--------|-----|------|---------|
| **L1 - Contributeur** | Tout contributeur | Commits standards | Git commit signing (optionnel) |
| **L2 - Mainteneur** | Mainteneurs validés | ADR, modifs gouvernance | Git commit signing (obligatoire) |
| **L3 - Décision collective** | Consensus équipe | ADR majeurs, RFC critiques | Multi-signatures ou vote documenté |

#### **Process de signature pour ADR**

1. **Rédaction** : Auteur crée l'ADR
2. **Discussion** : RFC si nécessaire
3. **Validation** : Selon GOVERNANCE.md
4. **Signature** : Mainteneur signe le commit d'acceptation
5. **Registre** : ADR ajouté au registre avec référence commit signé

#### **Vérification en CI**

```yaml
# .github/workflows/verify-signatures.yml
name: Verify Signatures

on: [pull_request, push]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Verify commit signatures
        run: |
          # Vérifier que les commits modifiant ADR sont signés
          git log --show-signature
      - name: Validate registry
        run: |
          cd docs/_registry/scripts
          ./validate.sh
```

---

## 3️⃣ FAISABILITÉ ET RECOMMANDATIONS

### 3.1 Évaluation des options

| Mécanisme | Faisabilité | Complexité | Valeur ajoutée | Recommandation |
|-----------|-------------|------------|----------------|----------------|
| **Git commit signing** | ✅ Haute | Faible | Haute | **À maintenir et renforcer** |
| **YAML frontmatter** | ✅ Haute | Moyenne | Moyenne | **À ajouter progressivement** |
| **Registre centralisé** | 🟡 Moyenne | Moyenne | Haute | **À développer phase 2** |
| **Hash de contenu** | 🟡 Moyenne | Moyenne | Moyenne | **Optionnel, phase 3** |
| **Signatures multi-niveaux** | 🟠 Faible | Haute | Faible | **Pas prioritaire** |
| **Blockchain** | 🔴 Très faible | Très haute | Négligeable | **Non pertinent** |

### 3.2 Roadmap de déploiement (phases)

#### **Phase 0 (Actuelle) - Baseline**
- ✅ Git commit signing recommandé (GOVERNANCE.md)
- ✅ Métadonnées en Markdown (en-têtes manuels)
- ✅ Pas de registre central (navigation manuelle)

#### **Phase 1 (Court terme : 1-3 mois) - Fondations**
1. Créer `docs/_registry/registry.yaml` (version minimale)
2. Ajouter frontmatter YAML aux documents existants (ADR/RFC/OBS)
3. Script de validation basique (cohérence registre ↔ fichiers)
4. Documentation procédure GPG (docs/07-contrib/gpg-setup.md)
5. CI vérifie présence de métadonnées

#### **Phase 2 (Moyen terme : 3-6 mois) - Enrichissement**
1. Registre enrichi (tags, liens, graph)
2. Scripts de génération automatique du registre
3. Visualisation du graph documentaire
4. CI vérifie signatures pour ADR
5. Recherche par métadonnées (CLI ou web)

#### **Phase 3 (Long terme : 6-12 mois) - Optimisation**
1. Hash de contenu automatique (si besoin détecté)
2. Interface web pour naviguer le registre
3. Métriques documentaires (taux de remplissage, liens brisés, etc.)
4. Éventuellement signatures multi-niveaux si gouvernance évolue

### 3.3 Garde-fous et principes

#### **Ne jamais sacrifier la lisibilité humaine**
- Les métadonnées doivent rester lisibles (YAML >> XML/JSON verbeux)
- Les documents doivent rester éditables manuellement
- L'outillage automatise mais ne remplace pas l'humain

#### **Éviter la sur-ingénierie**
- Commencer simple (registre YAML manuel)
- Automatiser seulement si besoin récurrent
- Ne pas créer d'outils pour des problèmes hypothétiques

#### **Préserver la flexibilité**
- Le registre est un index, pas une contrainte
- Les métadonnées facilitent, n'emprisonnent pas
- La gouvernance peut évoluer sans réécrire l'outillage

---

## 4️⃣ GESTION DES CAS LIMITES

### 4.1 Que faire en cas de perte d'intégrité ?

#### **Scénario : Document ADR modifié sans trace**

**Détection** :
- CI détecte hash de contenu différent
- ou git log montre commit non signé sur ADR
- ou registre désynchronisé

**Réaction** :
1. Identifier l'origine de la modification (git blame)
2. Évaluer l'intention (erreur ou malveillance ?)
3. Si erreur : Restaurer version précédente + documenter incident
4. Si malveillance : Post-mortem + renforcement sécurité
5. Créer un "ADR de correction" si nécessaire

#### **Scénario : Registre corrompu**

**Prévention** :
- Registre versionné dans Git (historique complet)
- Backups réguliers
- Validation CI avant merge

**Réaction** :
1. Revenir à dernière version valide (git revert)
2. Régénérer depuis les documents sources si nécessaire
3. Analyser la cause de corruption
4. Améliorer les validations

### 4.2 Comment gérer les documents contradictoires ?

#### **ADR contradictoires**

**Principe** : Ne devrait jamais arriver (process de validation)

**Si détecté** :
1. Créer une RFC "Résolution contradiction ADR-X vs ADR-Y"
2. Analyser les deux décisions et leur contexte
3. Proposer une résolution (laquelle prime ? nouvelle décision ?)
4. Créer un ADR de résolution
5. Marquer un des ADR originaux "Supersédé" si besoin

#### **OBS contradictoires**

**Principe** : Acceptable (observations peuvent diverger selon contexte)

**Gestion** :
- Documenter les conditions d'observation (différences environnement, version, etc.)
- Créer une OBS de synthèse si les divergences sont significatives
- Ne pas forcer un consensus artificiel

### 4.3 Évolution des standards de métadonnées

#### **Problème : Frontmatter évolue, anciens documents obsolètes**

**Solution gradualisée** :
1. **Versioning du schéma** : frontmatter v1, v2, etc.
2. **Rétrocompatibilité** : Nouveaux champs optionnels
3. **Migration progressive** : Script de migration disponible, mais pas obligatoire immédiatement
4. **Documentation claire** : Changelog du schéma de métadonnées

**Exemple** :
```yaml
---
schema_version: "2.0"  # Nouveau champ
# ... nouveaux champs ...
---
```

Anciens documents avec `schema_version: "1.0"` restent valides, mais avec métadonnées moins riches.

---

## 5️⃣ PRINCIPES DE GOUVERNANCE DOCUMENTAIRE (SYNTHÈSE)

### 5.1 Les 10 commandements du SSOT Relinium

1. **Traçabilité absolue tu garantiras**
   - Tout changement est documenté
   - L'historique est accessible et vérifiable

2. **L'intention tu préserveras**
   - Pas de réécriture de l'histoire
   - L'ADR original reste intact même si supersédé

3. **L'erreur tu honoreras**
   - Les erreurs sont des apprentissages
   - On ne supprime pas, on documente et on corrige

4. **La flexibilité tu maintiendras**
   - OBS et RFC peuvent évoluer librement
   - La gouvernance elle-même est révisable

5. **La lisibilité humaine tu privilégieras**
   - Markdown > formats binaires
   - Métadonnées simples et claires

6. **L'automatisation tu n'imposeras point**
   - Outillage facilite mais n'emprisonne pas
   - Documents éditables manuellement toujours

7. **La signature tu utiliseras à bon escient**
   - Git commit signing pour ADR et gouvernance
   - Pas de complexité excessive

8. **Le registre tu maintiendras**
   - Index central pour navigation
   - Mais pas point de défaillance unique

9. **La cohérence tu vérifieras**
   - CI valide liens, métadonnées, signatures
   - Rapports réguliers de santé documentaire

10. **L'évolution tu accepteras**
    - La gouvernance peut changer
    - Les outils peuvent être remplacés
    - L'important : intention et traçabilité préservées

### 5.2 Indicateurs de santé documentaire

| Indicateur | Cible | Fréquence de mesure |
|------------|-------|---------------------|
| Taux de documents avec métadonnées complètes | > 95% | Mensuelle |
| Nombre de liens brisés | 0 | Hebdomadaire (CI) |
| Taux d'ADR signés (commits GPG) | 100% | Continue (CI) |
| Cohérence registre ↔ fichiers | 100% | Continue (CI) |
| Temps moyen de navigation | < 2 min | Trimestrielle (enquête) |
| Documents obsolètes non marqués | < 5% | Trimestrielle |

### 5.3 Processus d'amélioration continue

**Rétrospectives documentaires (trimestrielles)** :
1. Métriques de santé documentaire
2. Feedback contributeurs
3. Identification des frictions
4. Propositions d'amélioration (RFC si structurant)

**Audit annuel** :
1. Revue exhaustive du registre
2. Vérification signatures
3. Test de reconstruction historique
4. Mise à jour des processus si nécessaire

---

## 6️⃣ CONCLUSION ET NEXT STEPS

### 6.1 Ce qui est déjà en place

✅ **Gouvernance claire** (GOVERNANCE.md, CONTRIBUTING.md)  
✅ **Process documentaire défini** (ADR, RFC, OBS)  
✅ **Git commit signing recommandé**  
✅ **Structure documentaire robuste**  

### 6.2 Ce qui reste à construire

🔨 **Court terme**
- Registre documentaire minimal (registry.yaml)
- Frontmatter YAML sur documents existants
- Script de validation basique
- Documentation setup GPG

🔨 **Moyen terme**
- Registre enrichi (graph, tags, recherche)
- CI vérifie signatures ADR
- Visualisation du graph documentaire

🔨 **Long terme**
- Hash de contenu (si besoin)
- Interface web de navigation
- Métriques et dashboards

### 6.3 Recommandation finale

**La gouvernance documentaire de Relinium doit rester fidèle à ses principes fondateurs** :
- Transparence radicale
- Traçabilité totale
- Flexibilité préservée
- Accessibilité humaine

**L'outillage proposé (registre + signatures) est un moyen, pas une fin.**  
Il doit servir ces principes, jamais les contraindre.

> _"La vraie inviolabilité n'est pas l'impossibilité de modifier,_  
> _mais l'impossibilité d'oublier pourquoi nous avons décidé."_

---

**Fin des fondations de gouvernance documentaire**
