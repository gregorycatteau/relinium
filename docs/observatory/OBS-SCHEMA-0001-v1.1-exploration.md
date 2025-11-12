---
id: OBS-0112
type: OBS
status: Ouvert
date: '2025-11-05'
author: Greg Catteau
version: 1.0.0
tags:
- schema
- evolution
- governance
- v1.1
links:
  cites:
  - OBS-0111
  - SPRINT_DOC-0001
  - ADR-0001
  - RFC-0002
intent:
  primary_question: Comment faire évoluer le schéma documentaire Relinium pour intégrer
    les patterns de gouvernance identifiés dans v1.0 ?
id_root: OBS-0112
scope: organizational
pattern: observation
self_hash: sha256:257362db64aaafb1a58216452c52e5e8d49cb8f248d64666be5b2fce98da039b
---

# OBS-SCHEMA-0001 – Exploration de l'Évolution du Schéma Documentaire vers v1.1

> *"La grammaire évolue, mais le sens demeure."*

---

## I. Contexte et Intention

### 1.1 Clôture de Genesis et Naissance de l'Observation

Le **5 novembre 2025**, la phase Genesis de Relinium s'est officiellement achevée avec la certification du SSOT v1.0. Cette certification marque un moment charnière : le passage d'un **système documentaire naissant** à un **organisme souverain et traçable**.

**Hash corpus certifié** :
```
61b23d319615f3c20959b5e5a9a2b31a51b72d07e3ef6c8430ab600a95afb24a
```

**Corpus Genesis** :
- 17 fichiers certifiés
- 6 documents architecturaux avec frontmatter
- 1 schéma documentaire v1.0 stable
- Infrastructure de validation CI/CD opérationnelle
- Registre documentaire automatisé

### 1.2 Constat de l'Audit de Gouvernance

L'audit exploratoire `OBS-GOVERNANCE-0001` a révélé des **patterns de gouvernance implicites** qui ont naturellement émergé pendant la phase Genesis. Ces patterns démontrent que le schéma v1.0, bien que fonctionnel et cohérent, présente des **lacunes structurelles** pour supporter une gouvernance collaborative à l'échelle.

**Principales observations de l'audit** :
- ✅ Certification cryptographique exemplaire (5/5)
- ✅ Cycle décisionnel triphasé mature (4/5)
- ⚠️ Autorité organique monoauteur non scalable (2/5)
- ⚠️ Absence de champs pour rôles multiples
- ⚠️ Relations documentaires limitées
- ⚠️ Statuts peu granulaires

### 1.3 Objectifs de l'Exploration

Cette exploration vise à **prototyper l'évolution** du schéma documentaire Relinium de v1.0 vers v1.1, en se basant sur les enseignements empiriques du corpus Genesis.

**Intention principale** :  
Enrichir le schéma documentaire pour intégrer les patterns de gouvernance identifiés, **sans briser la compatibilité** avec les documents existants.

**Objectifs spécifiques** :
1. **Diagnostiquer** : Évaluer les forces et limites du schéma v1.0
2. **Synthétiser** : Extraire les enseignements de la gouvernance observée
3. **Proposer** : Définir les nouveaux champs et relations pour v1.1
4. **Anticiper** : Mesurer les impacts sur la CI/CD, le registre et la migration
5. **Stratégier** : Planifier la transition v1.0 → v1.1
6. **Philosopher** : Formuler les principes directeurs de l'évolution

### 1.4 Philosophie : "La Grammaire Évolue, Mais le Sens Demeure"

Le schéma documentaire Relinium n'est pas une **structure figée**, c'est un **organisme vivant** qui doit évoluer avec la maturité du projet. Mais cette évolution ne doit jamais trahir les principes fondateurs :

- **Simplicité** : Le schéma reste accessible et compréhensible
- **Traçabilité** : Chaque document conserve son historique
- **Souveraineté** : Le système demeure autonome et vérifiable
- **Fidélité** : Les versions antérieures restent valides et lisibles

L'évolution vers v1.1 n'est pas une rupture, c'est un **discernement** : identifier ce qui manque, ajouter ce qui est essentiel, préserver ce qui fonctionne.

---

## II. Diagnostic du Schéma v1.0

### 2.1 Architecture Actuelle

Le schéma v1.0 repose sur une **philosophie minimaliste** exprimée dans son principe fondateur : **"Minimal Viable Metadata"**.

#### 2.1.1 Structure des Champs

| Catégorie | Nombre | Champs |
|-----------|--------|--------|
| **REQUIRED** | 4 | `id`, `type`, `status`, `date` |
| **RECOMMENDED** | 2 | `author`, `version` |
| **OPTIONAL** | 2 | `tags`, `links` |
| **Total** | 8 | Schéma lean et accessible |

#### 2.1.2 Types de Documents

Le schéma v1.0 définit **5 types de documents** :

```yaml
ADR          → Architecture Decision Record
RFC          → Request For Comments
OBS          → Observation
POC          → Proof of Concept
SPRINT_DOC   → Document de Sprint
```

Chaque type possède son propre cycle de vie avec des statuts spécifiques.

### 2.2 Forces du Schéma v1.0

#### Force 1 : Simplicité et Accessibilité (Score : 5/5)

**Observation** :  
Le schéma v1.0 est **remarquablement simple**. Avec seulement 4 champs obligatoires, il impose une charge cognitive minimale aux contributeurs.

**Preuves concrètes** :
- Taux d'adoption : **100%** (6/6 documents pilotes conformes)
- Temps de rédaction frontmatter : ~30 secondes
- Courbe d'apprentissage : ~5 minutes

**Impact positif** :
- Barrière à l'entrée très faible pour nouveaux contributeurs
- Pas de surcharge mentale lors de la documentation
- Facilite l'adoption spontanée du schéma

**Justification du score** : Exemplaire dans sa simplicité, aucune amélioration nécessaire sur cet aspect.

---

#### Force 2 : Validité et Automatisation CI (Score : 5/5)

**Observation** :  
Le schéma v1.0 est **techniquement robuste** et parfaitement validable par des outils automatisés.

**Infrastructure de validation** :
- Script Python : `validate_frontmatter.py` (validation YAML/JSON)
- Workflow CI/CD : `.github/workflows/validate-frontmatter.yml`
- Taux de succès : **100%** (17/17 fichiers certifiés)

**Capacités de validation** :
```python
✅ Présence des champs REQUIRED
✅ Conformité des types de données
✅ Validation des patterns (ID, dates)
✅ Cohérence type/statut
✅ Format YAML syntaxiquement correct
```

**Impact positif** :
- Protection automatique de l'intégrité du SSOT
- Détection précoce des non-conformités
- Garantie de la cohérence structurelle

**Justification du score** : Infrastructure exemplaire, référence pour v1.1.

---

#### Force 3 : Relations Bidirectionnelles (Score : 3/5)

**Observation** :  
Le schéma v1.0 définit des **relations bidirectionnelles** (`cites`/`cited_by`, `supersedes`/`superseded_by`), créant un **graphe de connaissances** traçable.

**Usage observé dans Genesis** :
- `cites` : 8 occurrences
- `cited_by` : 7 occurrences
- `supersedes` : 0 (corpus jeune)
- `superseded_by` : 0

**Exemple concret (RFC-002)** :
```yaml
links:
  cites: ["ADR-0001", "RFC-001"]
  cited_by: ["OBS-0001", "OBS-0002", "OBS-0003"]
```

**Impact positif** :
- Traçabilité des dépendances conceptuelles
- Construction d'un graphe sémantique
- Facilite la navigation intellectuelle

**Limites identifiées** :
- Pas de validation automatique des IDs référencés
- Pas de typologie des relations (toutes sont équivalentes)
- Pas de mécanisme pour marquer un désaccord

**Justification du score** : Pattern structuré et cohérent, mais incomplet. Marge de progression significative.

---

### 2.3 Limites du Schéma v1.0

#### Limite 1 : Rôles Limités à `author` (Score : 1/5)

**Problème identifié** :  
Le schéma v1.0 ne prévoit qu'un seul champ `author` (RECOMMENDED), **sans distinction pour les rôles multiples** nécessaires à une gouvernance collaborative.

**Rôles absents** :
- **Reviewer** : Relecteur technique qui valide la qualité
- **Guardian** : Gardien de cohérence architecturale
- **Approver** : Validateur formel pour les ADR
- **Contributor** : Contributeur secondaire

**Conséquences observées** :
- Impossible de tracer **qui valide** une décision (ADR)
- Impossible de distinguer **auteur original** vs **mainteneur actuel**
- Pas de mécanisme pour les **décisions collégiales**

**Exemple concret** :
```yaml
# ADR-0001 : statut "Accepté"
author: "Greg Catteau"
# ❓ Question : Qui a accepté cette décision ?
# - Greg Catteau lui-même ?
# - Un consensus implicite ?
# - Une équipe de validation ?
```

**Besoin identifié** :  
Champ structuré pour **rôles multiples** avec attributions claires.

**Justification du score (1/5)** : Pattern embryonnaire, inadapté à une gouvernance collaborative.

---

#### Limite 2 : Statuts Peu Granulaires (Score : 2/5)

**Problème identifié** :  
Les statuts définis pour chaque type de document sont **fonctionnels mais peu expressifs**.

**Exemple ADR** :
```yaml
allowed_statuts:
  - "Proposition"
  - "En discussion"
  - "Accepté"
  - "Rejeté"
  - "Supersédé"
```

**Manques détectés** :
- Pas de distinction entre "Accepté définitif" et "Accepté conditionnel"
- Pas de statut "Expérimental" pour les décisions à valider empiriquement
- Pas de traçabilité des **transitions** (quand ? qui ? pourquoi ?)
- Pas de notion de **deadline** ou **expiration**

**Tensions identifiées** :
- "Accepté" vs "Certifié" : sémantique ambiguë (cf. OBS-GOVERNANCE-0001)
- Pas de mécanisme pour marquer une décision **contestée**
- Difficile de tracer un **désaccord explicite**

**Besoin identifié** :  
Enrichissement des statuts avec granularité accrue et traçabilité des transitions.

**Justification du score (2/5)** : Pattern naissant, fonctionnel mais insuffisant.

---

#### Limite 3 : Absence de Champ `scope` (Score : 0/5)

**Problème identifié** :  
Le schéma v1.0 ne permet pas de catégoriser les documents selon leur **domaine d'application**.

**Domaines identifiés empiriquement** :
- **Technique** : Infrastructure, code, architecture
- **Organisationnel** : Processus, méthodologies, gouvernance
- **Éthique** : Valeurs, principes, charte
- **Spirituel** : Philosophie, sens, vision

**Observation dans le corpus** :
- `ADR-0001` : Traite de méthodologie → **Organisationnel + Philosophique**
- `RFC-001` : Traite de stack technique → **Technique**
- `OBS-0003` : Traite de SLOs → **Technique**

**Conséquence** :  
Cette distinction n'est **pas formalisée**, uniquement déductible des tags.

**Impact potentiel** :
- Difficulté à **filtrer** les documents par domaine
- Risque de **mélanger** préoccupations techniques et éthiques
- Impossibilité de définir des **processus de validation différenciés** par scope

**Besoin identifié** :  
Champ `scope` pour classification par domaine d'application.

**Justification du score (0/5)** : Pattern inexistant, besoin critique identifié.

---

#### Limite 4 : Absence de Champ `pattern` (Score : 0/5)

**Problème identifié** :  
Le champ `type` définit le **cycle de vie** (ADR, RFC, OBS), mais pas l'**intent métier** du document.

**Patterns identifiés empiriquement** :
- **Decision** : Document décisionnel (ADR)
- **Reflection** : Document de réflexion (RFC)
- **Observation** : Document factuel (OBS)
- **Experiment** : Document d'expérimentation (POC)
- **Rule** : Document normatif (charte, guide)

**Besoin identifié** :  
Permettre de **rechercher par intent** plutôt que par type formel.

**Exemple d'usage** :
```yaml
# ADR-0001
type: "ADR"          # ← Cycle de vie
pattern: "decision"  # ← Intent métier
```

**Impact potentiel** :
- Facilite l'identification des documents **inspirants** vs **normatifs**
- Permet des requêtes sémantiques ("tous les documents de réflexion")
- Enrichit la sémantique du registre

**Justification du score (0/5)** : Pattern inexistant, opportunité identifiée.

---

#### Limite 5 : Relations Univoques (Score : 2/5)

**Problème identifié** :  
Le schéma v1.0 définit 4 types de relations, mais elles sont **sémantiquement pauvres**.

**Relations actuelles** :
```yaml
cites         → Document A cite Document B
cited_by      → Document B est cité par Document A
supersedes    → Document A remplace Document B
superseded_by → Document B est remplacé par Document A
```

**Manques détectés** :
- Pas de relation `inspired_by` (inspiration sans dépendance)
- Pas de relation `governs` (gouvernance explicite)
- Pas de relation `extends` (extension sans remplacement)
- Pas de relation `refutes` (contestation explicite)

**Conséquence** :  
Toutes les citations sont **équivalentes** sémantiquement, alors qu'en réalité elles expriment des **nuances différentes**.

**Exemple d'ambiguïté** :
```yaml
# RFC-003 cite ADR-0001
links:
  cites: ["ADR-0001"]
# ❓ Question : Cette citation exprime-t-elle :
# - Une dépendance forte ?
# - Une simple inspiration ?
# - Un désaccord avec ADR-0001 ?
```

**Justification du score (2/5)** : Pattern naissant, fonctionnel mais limité.

---

### 2.4 Tableau de Maturité par Champ

| Champ | Présent v1.0 | Score Maturité | Observation |
|-------|--------------|----------------|-------------|
| `id` | ✅ REQUIRED | 5/5 | Exemplaire, aucune amélioration nécessaire |
| `type` | ✅ REQUIRED | 5/5 | Définition claire, 5 types bien distincts |
| `status` | ✅ REQUIRED | 3/5 | Fonctionnel mais peu granulaire |
| `date` | ✅ REQUIRED | 5/5 | Format ISO, validation stricte |
| `author` | ✅ RECOMMENDED | 2/5 | Monoauteur, non scalable |
| `version` | ✅ RECOMMENDED | 4/5 | SemVer simplifié, bien adopté |
| `tags` | ✅ OPTIONAL | 4/5 | Flexible, 100% d'utilisation |
| `links` | ✅ OPTIONAL | 3/5 | Bidirectionnel mais peu typé |
| **`role`** | ❌ Absent | 0/5 | **Besoin critique identifié** |
| **`scope`** | ❌ Absent | 0/5 | **Besoin moyen identifié** |
| **`pattern`** | ❌ Absent | 0/5 | **Opportunité identifiée** |
| **`decision_type`** | ❌ Absent | 0/5 | **Enrichissement statuts** |

**Score moyen actuel** : **3.2/5** (Structuré mais incomplet)

---

## III. Enseignements de la Gouvernance

### 3.1 Synthèse des Patterns Détectés

L'audit `OBS-GOVERNANCE-0001` a identifié **6 patterns majeurs** dans le corpus Genesis.

#### Pattern 1 : Cycle Décisionnel Triphasé (4/5)

**Observation** :  
Un cycle décisionnel **OBS → RFC → ADR** émerge naturellement du corpus.

```
OBS (Observation) → RFC (Proposition) → ADR (Décision)
```

**Graphe de dépendances observé** :
```
ADR-0001 [Accepté]
    ↑ cited_by
    ├─ RFC-001 [En discussion]
    └─ RFC-002 [En discussion]
           ↑ cited_by
           ├─ OBS-0001 [Ouvert]
           ├─ OBS-0002 [Ouvert]
           └─ OBS-0003 [Ouvert]
```

**Enseignement pour v1.1** :  
Ce pattern fonctionne **organiquement**, pas besoin de le rigidifier. Cependant, il manque des **critères formels de transition** entre phases.

**Besoin identifié** :  
- Champ `decision_type` pour préciser la nature de la décision
- Traçabilité des transitions de statut

---

#### Pattern 2 : Autorité Organique Monoauteur (2/5)

**Observation** :  
100% des documents ont le même auteur : `"Greg Catteau"`.

**Conséquence** :  
La gouvernance est **méritocratique-fondatrice** : l'autorité découle de l'acte de création.

**Enseignement pour v1.1** :  
Ce modèle est **adapté à la phase Genesis** mais **non scalable** à une équipe de 5-10 contributeurs.

**Besoin critique** :  
Champ `role` pour tracer les rôles multiples (auteur, reviewer, guardian, approver).

---

#### Pattern 3 : Certification Cryptographique (5/5)

**Observation** :  
Le système de hashing SHA256 est **exemplaire**.

**Enseignement pour v1.1** :  
Aucune amélioration nécessaire. Préserver cette infrastructure intacte.

---

#### Pattern 4 : Validation par Cohérence Interne (3/5)

**Observation** :  
Les documents se légitiment par leurs **relations mutuelles** plutôt que par approbation externe.

**Enseignement pour v1.1** :  
Enrichir les relations pour permettre la **contestation explicite** et la **gouvernance distribuée**.

**Besoin identifié** :  
Nouvelles relations : `refutes`, `extends`, `governs`, `inspired_by`.

---

### 3.2 Besoins Fonctionnels vs Conceptuels

#### Besoins Fonctionnels (Opérationnels)

**Besoin 1 : Multi-auteurs**  
Tracer les contributeurs multiples sur un même document.

**Besoin 2 : Validations collégiales**  
Identifier qui a approuvé une décision (ADR).

**Besoin 3 : Transitions de statut**  
Tracer quand et pourquoi un document change de statut.

**Besoin 4 : Filtrage par domaine**  
Catégoriser les documents par scope (technique, organisationnel, éthique).

#### Besoins Conceptuels (Sémantiques)

**Besoin 1 : Expressivité des relations**  
Distinguer inspiration, dépendance, gouvernance, contestation.

**Besoin 2 : Granularité des statuts**  
Différencier "Accepté" définitif vs conditionnel vs expérimental.

**Besoin 3 : Intent métier**  
Identifier le pattern du document (decision, reflection, rule, experiment).

---

### 3.3 Tensions Identifiées

#### Tension 1 : Rigueur vs Souplesse

**Description** :  
Le schéma v1.0 est **rigoureux** (validation CI/CD stricte) mais aussi **souple** (champs OPTIONAL nombreux).

**Question pour v1.1** :  
Faut-il ajouter des champs REQUIRED pour forcer la traçabilité, au risque de compliquer l'adoption ?

**Recommandation** :  
Maintenir la philosophie actuelle : nouveaux champs = OPTIONAL par défaut.

---

#### Tension 2 : Complexité vs Clarté

**Description** :  
Chaque nouveau champ augmente la **charge cognitive** pour les contributeurs.

**Risque** :  
Surengineering si on anticipe trop de cas d'usage futurs.

**Recommandation** :  
**Principe de parcimonie** : N'ajouter que les champs **réellement nécessaires**, validés empiriquement.

---

#### Tension 3 : Scalabilité vs Simplicité

**Description** :  
Le schéma v1.0 est **simple** (8 champs) mais **non scalable** (monoauteur).

**Question pour v1.1** :  
Comment ajouter les champs pour la collaboration sans perdre la simplicité ?

**Recommandation** :  
Champs pour collaboration = OPTIONAL, avec **exemples clairs** pour faciliter l'adoption.

---

## IV. Propositions d'Évolution

### 4.1 Vue d'Ensemble des Nouveaux Champs

Cette section présente les **5 nouveaux champs** proposés pour le schéma v1.1, avec scoring de pertinence.

| Champ | Type | Priorité | Score Pertinence | Rétrocompatibilité |
|-------|------|----------|------------------|-------------------|
| `role` | object | **Critique** | 5/5 | ✅ Pleine |
| `decision_type` | string | **Recommandé** | 4/5 | ⚠️ Partielle |
| `scope` | string | **Recommandé** | 4/5 | ✅ Pleine |
| `pattern` | string | Optionnel | 3/5 | ✅ Pleine |
| `relations` (enrichies) | object | **Recommandé** | 4/5 | ⚠️ À implémenter |

---

### 4.2 Champ `role` – Rôles Multiples

#### 4.2.1 Définition

**Type** : `object`  
**Catégorie** : OPTIONAL (pour rétrocompatibilité)  
**Objectif** : Tracer les **rôles multiples** dans la création et validation d'un document.

#### 4.2.2 Structure Proposée

```yaml
role:
  author:
    - name: "Greg Catteau"
      email: "greg@relinium.org"  # Optionnel
  reviewers:  # Optionnel
    - name: "Jane Doe"
      reviewed_at: "2025-11-05"
  guardian:  # Optionnel, unique
    name: "Greg Catteau"
  approved_by:  # Optionnel, pour ADR
    - name: "Tech Lead"
      approved_at: "2025-11-05"
```

#### 4.2.3 Exemple Concret

```yaml
# ADR-0010 : Choix de base de données
---
id: "ADR-0010"
type: "ADR"
status: "Accepté"
date: "2025-12-01"
version: "1.0.0"
role:
  author:
    - name: "Greg Catteau"
  reviewers:
    - name: "Jane Doe"
      reviewed_at: "2025-12-02"
    - name: "John Smith"
      reviewed_at: "2025-12-03"
  guardian:
    name: "Greg Catteau"
  approved_by:
    - name: "Greg Catteau"
      approved_at: "2025-12-05"
    - name: "Tech Lead"
      approved_at: "2025-12-05"
---
```

#### 4.2.4 Justification

**Problème résolu** :  
- Traçabilité des validations collégiales
- Support des processus collaboratifs
- Distinction claire entre création et approbation

**Compatibilité v1.0** :  
✅ **Pleine** : Le champ `author` (RECOMMENDED) reste valide. Le champ `role` est OPTIONAL et vient l'enrichir.

**Dépendances** :  
Aucune. Champ autonome.

**Score de pertinence** : **5/5** (Critique)  
- Résout le besoin n°1 identifié dans l'audit
- Nécessaire pour passer d'une gouvernance monoauteur à collaborative
- Impact majeur sur la scalabilité

---

### 4.3 Champ `decision_type` – Précision des Statuts

#### 4.3.1 Définition

**Type** : `string`  
**Catégorie** : OPTIONAL  
**Objectif** : Enrichir le champ `status` avec une **granularité accrue** pour les décisions.

#### 4.3.2 Valeurs Proposées

```yaml
decision_type:
  type: string
  enum:
    - "accepted"        # Accepté définitivement
    - "accepted_conditional"  # Accepté sous conditions
    - "experimental"    # Accepté à titre expérimental
    - "rejected"        # Rejeté avec justification
    - "superseded"      # Remplacé par une nouvelle décision
    - "deprecated"      # Déprécié mais pas encore supersédé
```

#### 4.3.3 Exemple Concret

```yaml
# ADR-0015 : Choix d'architecture microservices
---
id: "ADR-0015"
type: "ADR"
status: "Accepté"
decision_type: "experimental"
date: "2025-12-10"
version: "1.0.0"
author: "Greg Catteau"
tags: ["architecture", "microservices", "experimental"]
---

# Contenu du document explique :
# - Cette décision est acceptée à titre expérimental pour 6 mois
# - Elle sera réévaluée en juin 2026 avec un ADR de confirmation ou superseding
```

#### 4.3.4 Justification

**Problème résolu** :  
- Distinguer "Accepté" définitif vs conditionnel vs expérimental
- Tracer les décisions **contestées** ou **temporaires**
- Clarifier la sémantique "Accepté" vs "Certifié"

**Compatibilité v1.0** :  
⚠️ **Partielle** : Le champ `status` reste inchangé. `decision_type` vient l'affiner pour les ADR uniquement.

**Dépendances** :  
- S'applique principalement aux documents de type ADR
- Peut être étendu aux RFC (à discuter)

**Score de pertinence** : **4/5** (Recommandé)  
- Résout une tension identifiée dans l'audit (statuts ambigus)
- Impact moyen-élevé sur l'expressivité
- Optionnel, donc pas bloquant

---

### 4.4 Champ `scope` – Domaine d'Application

#### 4.4.1 Définition

**Type** : `string`  
**Catégorie** : OPTIONAL  
**Objectif** : Catégoriser les documents selon leur **domaine d'application**.

#### 4.4.2 Valeurs Proposées

```yaml
scope:
  type: string
  enum:
    - "technical"       # Infrastructure, code, architecture
    - "organizational"  # Processus, méthodologies, gouvernance
    - "ethical"        # Valeurs, principes, charte
    - "spiritual"      # Philosophie, sens, vision
    - "mixed"          # Plusieurs domaines
```

#### 4.4.3 Exemple Concret

```yaml
# ADR-0001 : Repo Driven by Docs-First
---
id: "ADR-0001"
type: "ADR"
status: "Accepté"
date: "2025-01-05"
author: "Greg Catteau"
version: "1.0.0"
scope: "organizational"  # ← Nouveau champ
tags: ["governance", "methodology", "docs-first"]
links:
  cited_by: ["RFC-001", "RFC-002"]
---
```

#### 4.4.4 Justification

**Problème résolu** :  
- Filtrage par domaine d'expertise
- Séparation claire entre préoccupations techniques et éthiques
- Processus de validation différenciés par domaine

**Compatibilité v1.0** :  
✅ **Pleine** : Champ OPTIONAL, aucun impact sur les documents existants.

**Dépendances** :  
Aucune. Champ autonome.

**Score de pertinence** : **4/5** (Recommandé)  
- Résout une lacune identifiée dans l'audit
- Impact moyen sur la lisibilité et la navigation
- Facilite la gouvernance par domaine d'expertise

---

### 4.5 Champ `pattern` – Méta-classification

#### 4.5.1 Définition

**Type** : `string`  
**Catégorie** : OPTIONAL  
**Objectif** : Identifier l'**intent métier** du document au-delà de son type formel.

#### 4.5.2 Valeurs Proposées

```yaml
pattern:
  type: string
  enum:
    - "decision"      # Document décisionnel
    - "reflection"    # Document de réflexion
    - "observation"   # Document factuel
    - "experiment"    # Document d'expérimentation
    - "rule"          # Document normatif
```

#### 4.5.3 Exemple Concret

```yaml
# ADR-0001 : Repo Driven by Docs-First
---
id: "ADR-0001"
type: "ADR"          # ← Cycle de vie
pattern: "decision"  # ← Intent métier
status: "Accepté"
scope: "organizational"
---
```

#### 4.5.4 Justification

**Problème résolu** :  
- Recherche par intent plutôt que par type formel
- Identification des documents inspirants vs normatifs
- Enrichissement sémantique du registre

**Compatibilité v1.0** :  
✅ **Pleine** : Champ OPTIONAL, aucun impact.

**Dépendances** :  
Peut être déduit du champ `type`, mais apporte une granularité supplémentaire.

**Score de pertinence** : **3/5** (Optionnel)  
- Opportunité identifiée, pas une nécessité critique
- Impact moyen sur la sémantique
- Peut être ajouté progressivement

---

### 4.6 Relations Enrichies – Typologie des Liens

#### 4.6.1 Nouvelles Relations Proposées

| Relation | Sémantique | Exemple d'usage | Priorité |
|----------|-----------|-----------------|----------|
| `inspired_by` | Inspiration sans dépendance | RFC inspiré par ADR | Recommandé |
| `governs` | Gouvernance explicite | Charte régit les ADR | Recommandé |
| `extends` | Extension sans remplacement | ADR étend un autre ADR | Recommandé |
| `refutes` | Contestation explicite | RFC conteste un ADR | Optionnel |

#### 4.6.2 Exemples Concrets

```yaml
# RFC-010 : Architecture alternative
---
id: "RFC-010"
type: "RFC"
status: "En discussion"
links:
  inspired_by: ["ADR-0001"]  # ← Inspiration philosophique
  refutes: ["RFC-008"]       # ← Désaccord explicite
  cites: ["OBS-0015"]        # ← Dépendance factuelle
---
```

```yaml
# CHARTER-001 : Charte éthique du projet
---
id: "CHARTER-001"
type: "ADR"
status: "Accepté"
pattern: "rule"
scope: "ethical"
links:
  governs: ["ADR-0001", "RFC-001", "RFC-002"]  # ← Gouvernance
---
```

#### 4.6.3 Justification

**Problème résolu** :  
- Expressivité accrue des relations
- Traçabilité des controverses et débats
- Mécanisme de contestation explicite

**Compatibilité v1.0** :  
⚠️ **À implémenter** : Nécessite extension du schéma `links` et validation CI/CD.

**Dépendances** :  
- Validation des IDs référencés
- Détection des relations circulaires
- Mise à jour du script de registre

**Score de pertinence** : **4/5** (Recommandé)  
- Résout une limite majeure identifiée dans l'audit
- Impact élevé sur la richesse sémantique
- Nécessaire pour une gouvernance distribuée

---

### 4.7 Tableau Récapitulatif des Propositions

| Champ | Type | Catégorie | Score | Complexité | Priorité |
|-------|------|-----------|-------|------------|----------|
| `role` | object | OPTIONAL | 5/5 | Moyenne | **Critique** |
| `decision_type` | string | OPTIONAL | 4/5 | Faible | **Recommandé** |
| `scope` | string | OPTIONAL | 4/5 | Faible | **Recommandé** |
| `pattern` | string | OPTIONAL | 3/5 | Faible | Optionnel |
| Relations enrichies | object | OPTIONAL | 4/5 | Élevée | **Recommandé** |

**Philosophie** : Tous les nouveaux champs sont OPTIONAL pour préserver la rétrocompatibilité et la simplicité d'adoption.

---

## V. Impacts Prévisibles

### 5.1 Impact sur la CI/CD

#### 5.1.1 Validation YAML/JSON

**Changements nécessaires** :
- Mettre à jour `document_schema_v1.1.yaml`
- Générer `document_schema_v1.1.json`
- Adapter `scripts/validate_frontmatter.py`

**Nouvelles validations à implémenter** :
```python
# Validation du champ role
if 'role' in frontmatter:
    validate_role_structure(frontmatter['role'])
    validate_email_format(frontmatter['role']['author'])
    validate_dates(frontmatter['role']['reviewers'])

# Validation du champ scope
if 'scope' in frontmatter:
    validate_enum(frontmatter['scope'], ['technical', 'organizational', 'ethical', 'spiritual', 'mixed'])

# Validation des nouvelles relations
if 'links' in frontmatter:
    validate_enriched_relations(frontmatter['links'])
    check_circular_dependencies(frontmatter['links'])
```

**Temps estimé d'implémentation** : 2-3 heures

---

#### 5.1.2 Workflow GitHub Actions

**Modifications à apporter** :
```yaml
# .github/workflows/validate-frontmatter.yml
- name: Validate Frontmatter Schema v1.1
  run: |
    python3 scripts/validate_frontmatter.py --schema v1.1
    python3 scripts/validate_relations.py  # Nouveau script
```

**Nouveaux scripts** :
- `validate_relations.py` : Valide la cohérence des relations enrichies
- `check_circular_deps.py` : Détecte les dépendances circulaires

**Impact** : Minimal. Les documents v1.0 restent valides.

---

### 5.2 Impact sur le Registre

#### 5.2.1 Structure du Registre

**Enrichissement du `registry.yaml`** :
```yaml
# Exemple de document dans le registre v1.1
- id: "ADR-0001"
  type: "ADR"
  status: "Accepté"
  scope: "organizational"  # ← Nouveau champ
  pattern: "decision"      # ← Nouveau champ
  role:                    # ← Nouveau champ
    author:
      - name: "Greg Catteau"
    guardian:
      name: "Greg Catteau"
  links:
    cited_by: ["RFC-001", "RFC-002"]
    governs_by: ["CHARTER-001"]  # ← Nouvelle relation
```

#### 5.2.2 Script de Génération

**Modifications à `generate_registry.py`** :
- Parser les nouveaux champs optionnels
- Gérer les relations enrichies
- Calculer les métriques par scope
- Générer des index par pattern

**Temps estimé** : 3-4 heures

---

#### 5.2.3 Nouvelles Capacités

**Requêtes possibles** :
```python
# Tous les documents de scope "technical"
filter_by_scope("technical")

# Tous les documents de pattern "decision"
filter_by_pattern("decision")

# Documents gouvernés par la charte
get_governed_by("CHARTER-001")

# Documents avec multi-auteurs
filter_by_collaboration()
```

---

### 5.3 Impact sur la Lecture Humaine

#### 5.3.1 Lisibilité

**Avantages** :
- Meilleure compréhension du contexte (scope, pattern)
- Traçabilité des rôles (qui a fait quoi)
- Relations plus expressives

**Risques** :
- Frontmatter plus long (peut atteindre 15-20 lignes)
- Charge cognitive légèrement accrue

**Mitigation** :
- Tous les nouveaux champs sont OPTIONAL
- Exemples clairs dans le guide
- Templates par type de document

#### 5.3.2 Maintenance

**Facilitations** :
- Identification rapide du responsable (guardian)
- Traçabilité des approbations
- Navigation sémantique (relations enrichies)

**Défis** :
- Maintenir les relations bidirectionnelles à jour
- Cohérence entre `author` (v1.0) et `role.author` (v1.1)

**Solution** : Script de migration automatique.

---

### 5.4 Impact sur la Migration

#### 5.4.1 Stratégie de Migration

**Approche recommandée** : Migration progressive et non-bloquante.

```
Phase 1: Nouveaux documents utilisent v1.1
Phase 2: Migration progressive des documents existants
Phase 3: Dépréciation douce de v1.0 (sans casser)
```

#### 5.4.2 Script de Migration

**Fonctionnalités du script** :
```python
# migrate_schema_v1_to_v1.1.py

def migrate_document(doc_path):
    """Migre un document de v1.0 vers v1.1"""
    
    # 1. Parser le frontmatter v1.0
    fm = parse_frontmatter(doc_path)
    
    # 2. Enrichir avec nouveaux champs (si applicable)
    if 'author' in fm:
        fm['role'] = {
            'author': [{'name': fm['author']}],
            'guardian': {'name': fm['author']}
        }
    
    # 3. Déduire scope depuis tags
    fm['scope'] = deduce_scope(fm['tags'])
    
    # 4. Déduire pattern depuis type
    fm['pattern'] = deduce_pattern(fm['type'])
    
    # 5. Écrire le nouveau frontmatter
    write_frontmatter(doc_path, fm, version="1.1.0")
```

**Temps estimé** : 1-2 heures de développement

---

#### 5.4.3 Période de Coexistence

**Durée recommandée** : **6 mois minimum**

**Pendant cette période** :
- Les deux versions coexistent (v1.0 et v1.1)
- La CI valide les deux formats
- Le registre supporte les deux
- Migration progressive des documents critiques d'abord

**Fin de coexistence** :
- Tous les documents migrés vers v1.1
- Dépréciation officielle de v1.0 (mais reste lisible)
- Mise à jour de la documentation

---

## VI. Stratégie de Transition

### 6.1 Étapes Recommandées

#### Étape 1 : RFC de Validation (Semaine 1)

**Livrable** : `RFC-003-schema-evolution-v1.1.md`

**Contenu** :
- Présentation des nouveaux champs
- Justification basée sur OBS-SCHEMA-0001 et OBS-GOVERNANCE-0001
- Exemples concrets
- Stratégie de migration

**Validation** :
- Revue par les contributeurs potentiels
- Feedback sur la complexité perçue
- Ajustements si nécessaire

---

#### Étape 2 : Prototypage (Semaine 2)

**Livrable** : 3-5 documents de test avec v1.1

**Documents tests** :
- 1 ADR avec `role` multi-auteurs
- 1 RFC avec `scope` et `pattern`
- 1 OBS avec relations enrichies
- 1 ADR avec `decision_type: experimental`

**Objectif** :
- Valider la lisibilité
- Tester les outils de validation
- Identifier les problèmes d'adoption

---

#### Étape 3 : Implémentation Technique (Semaine 3)

**Livrables** :
- `document_schema_v1.1.yaml`
- `document_schema_v1.1.json`
- `scripts/validate_frontmatter.py` (mise à jour)
- `scripts/migrate_schema_v1_to_v1.1.py`
- `.github/workflows/validate-frontmatter.yml` (mise à jour)

**Tests** :
- Validation des documents v1.0 (rétrocompatibilité)
- Validation des documents v1.1 (nouveaux champs)
- Migration automatique d'un document pilote

---

#### Étape 4 : Audit de Compatibilité (Semaine 4)

**Livrable** : Rapport d'audit de compatibilité

**Vérifications** :
- Tous les documents v1.0 restent valides
- La CI accepte les deux versions
- Le registre s'enrichit correctement
- Aucune régression détectée

---

#### Étape 5 : Déploiement dans le Registre (Semaine 5)

**Livrable** : Registre v1.1 avec enrichissements

**Nouvelles fonctionnalités** :
- Index par `scope`
- Index par `pattern`
- Graphe des relations enrichies
- Métriques de collaboration (multi-auteurs)

---

#### Étape 6 : Migration Progressive (6 mois)

**Planning** :
```
Mois 1: Migration des documents critiques (ADR, RFC actifs)
Mois 2-4: Migration des OBS et POC
Mois 5: Migration des documents de sprint
Mois 6: Vérification finale et clôture
```

**Critères de priorisation** :
1. Documents cités par beaucoup d'autres
2. Documents en statut "En discussion" ou "Ouvert"
3. Documents récents (< 6 mois)
4. Documents archivés (dernière priorité)

---

### 6.2 Livrables Intermédiaires

| Livrable | Type | Semaine | Propriétaire |
|----------|------|---------|--------------|
| RFC-003 | Document | 1 | Greg Catteau |
| Documents de test | Prototypes | 2 | Équipe |
| Schéma v1.1 | YAML/JSON | 3 | Greg Catteau |
| Scripts de validation | Python | 3 | Équipe |
| Script de migration | Python | 3 | Équipe |
| Rapport d'audit | Document | 4 | Greg Catteau |
| Registre v1.1 | YAML | 5 | Automatique |
| Guide de migration | Markdown | 5 | Greg Catteau |

---

### 6.3 Critères de Succès

#### Critères Techniques

- ✅ Rétrocompatibilité : 100% des documents v1.0 valides avec v1.1
- ✅ Validation CI : Aucune régression détectée
- ✅ Performance : Temps de validation < 5 secondes
- ✅ Migration : Script automatique fonctionnel

#### Critères Fonctionnels

- ✅ Adoption : Au moins 3 contributeurs utilisent v1.1
- ✅ Lisibilité : Feedback positif sur les nouveaux champs
- ✅ Scalabilité : Support de 10+ contributeurs démontré
- ✅ Sémantique : Relations enrichies utilisées dans 5+ documents

#### Critères Organisationnels

- ✅ Documentation : Guide complet disponible
- ✅ Formation : 0 question récurrente sur v1.1
- ✅ Migration : 80% des documents migrés en 6 mois
- ✅ Gouvernance : Processus de validation collégiale opérationnel

---

## VII. Philosophie et Horizon

### 7.1 Philosophie de l'Évolution

> *"Un système souverain ne grandit pas par rupture, mais par discernement."*

#### 7.1.1 Principes Directeurs

**1. Maintenir la Simplicité**

L'évolution vers v1.1 ne doit jamais sacrifier la **simplicité fondatrice** du schéma v1.0.

**Garde-fous** :
- Tous les nouveaux champs sont OPTIONAL
- Maximum 5 nouveaux champs par version majeure
- Chaque champ doit résoudre un besoin observé empiriquement
- Pas d'anticipation excessive de cas d'usage futurs

**Philosophie** :  
*"La complexité naît du besoin, jamais de la prévoyance."*

---

**2. Préserver la Traçabilité**

Chaque évolution du schéma doit elle-même être **tracée et justifiée**.

**Mécanisme** :
- RFC pour proposer l'évolution
- OBS pour documenter les patterns observés
- ADR pour valider la décision d'évoluer
- Certification cryptographique du nouveau schéma

**Philosophie** :  
*"Le schéma évolue, mais son histoire demeure lisible."*

---

**3. Ne Jamais Rendre Obsolètes les Versions Précédentes**

Le schéma v1.0 reste **éternellement valide**. Les documents v1.0 ne doivent jamais devenir illisibles.

**Garantie** :
- Rétrocompatibilité obligatoire
- Coexistence des versions pendant au moins 6 mois
- Migration progressive, jamais forcée
- Les anciens documents restent consultables

**Philosophie** :  
*"La mémoire ne se réécrit pas, elle s'enrichit."*

---

#### 7.1.2 Équilibre Rigueur / Agilité

**Tension fondamentale** :
```
RIGUEUR                    vs                    AGILITÉ
(Validation stricte)                        (Flexibilité)
        ↓                                           ↓
Certification                                 Adaptation
Automatisation                                Évolution
Cohérence                                     Spontanéité
```

**Résolution de la tension** :

> *"Être rigoureux sur l'essentiel, flexible sur l'accessoire."*

**Essentiel (rigoureux)** :
- Champs REQUIRED : `id`, `type`, `status`, `date`
- Validation CI/CD automatique
- Intégrité cryptographique (hashes)

**Accessoire (flexible)** :
- Champs OPTIONAL : tout le reste
- Tags libres
- Relations optionnelles
- Métadonnées enrichies

---

### 7.2 Garde-Fous contre la Dérive

#### Garde-Fou 1 : Principe de Parcimonie

**Règle** : N'ajouter un champ que si au moins **3 documents** du corpus actuel en auraient bénéficié.

**Exemple** :
- ✅ `role` : Aurait été utile pour 100% des documents (collaboration future)
- ✅ `scope` : Aurait clarifié 80% des documents
- ❌ `estimated_reading_time` : Non observé comme besoin

---

#### Garde-Fou 2 : Validation Empirique

**Règle** : Prototyper sur 3-5 documents avant d'adopter un nouveau champ.

**Processus** :
1. Identifier un besoin dans un OBS
2. Prototyper le champ sur 3 documents
3. Recueillir du feedback
4. Ajuster ou abandonner

---

#### Garde-Fou 3 : Audit Semestriel

**Règle** : Tous les 6 mois, auditer l'utilisation réelle des champs optionnels.

**Métriques à mesurer** :
```yaml
# Exemple de métrique d'utilisation
field_usage:
  role:
    total_documents: 50
    documents_using: 45
    adoption_rate: 90%
    status: "✅ Bien adopté"
  
  pattern:
    total_documents: 50
    documents_using: 10
    adoption_rate: 20%
    status: "⚠️ Peu utilisé, à réévaluer"
```

**Actions** :
- Adoption < 30% → Questionner la pertinence
- Adoption < 10% → Déprécier le champ
- Adoption > 80% → Envisager de le rendre RECOMMENDED

---

### 7.3 Horizon : Vers v1.2 et au-delà

#### 7.3.1 Évolutions Potentielles Futures

**Champs envisagés (non confirmés)** :
- `lifecycle_transitions` : Traçabilité des changements de statut
- `deprecated_at` : Date de dépréciation explicite
- `expires_at` : Date d'expiration pour décisions temporaires
- `related_external` : Liens vers ressources externes (issues GitHub, etc.)

**Nouveau type de document** :
- `EXPERIMENT` : Pour les expérimentations scientifiques
- `POLICY` : Pour les politiques organisationnelles
- `CHARTER` : Pour les chartes et manifestes

---

#### 7.3.2 Évolution de la Gouvernance

**Vision à 2 ans** :
- Passage d'une gouvernance **monoauteur** à **collaborative**
- Processus de validation **collégial** pour les ADR
- Notion de **guardian** pour préserver la cohérence architecturale
- Mécanisme de **vote** ou **consensus** pour décisions majeures

**Mécanisme envisagé** :
```yaml
# ADR-0020 : Décision avec validation collégiale
---
id: "ADR-0020"
type: "ADR"
status: "Accepté"
role:
  author:
    - name: "Greg Catteau"
  approved_by:
    - name: "Greg Catteau"
      approved_at: "2026-03-10"
      vote: "approve"
    - name: "Jane Doe"
      approved_at: "2026-03-11"
      vote: "approve_with_conditions"
      conditions: "Ajouter tests de sécurité"
    - name: "John Smith"
      approved_at: "2026-03-12"
      vote: "abstain"
  guardian:
    name: "Greg Catteau"
decision:
  type: "accepted_conditional"
  consensus_threshold: "66%"  # 2/3 des approbateurs
  reached_at: "2026-03-12"
---
```

---

#### 7.3.3 Intégration avec Outils Externes

**Horizon 2-3 ans** :
- **Obsidian** : Plugin pour naviguer le graphe Relinium
- **GitHub Issues** : Liens bidirectionnels docs ↔ issues
- **CI/CD** : Génération automatique de changelogs depuis les ADR
- **Dashboard** : Visualisation du graphe documentaire

---

### 7.4 Citation Finale : La Loi Documentaire

> *"La loi documentaire n'est pas écrite une fois pour toutes — elle s'affine à mesure que la vérité se clarifie."*

Cette mission explore la façon dont Relinium peut continuer à grandir sans perdre sa cohérence, en traduisant les observations humaines en règles de validation documentaires.

**Enseignements clés** :

1. **L'observation précède la norme** : Ce document n'a rien prescrit, seulement observé et proposé.

2. **La cohérence est organique** : Les nouveaux champs émergent des besoins réels, pas d'anticipations théoriques.

3. **La rigueur sert l'humain** : La validation automatique libère l'esprit pour se concentrer sur le sens.

4. **L'autorité est temporaire** : Le schéma monoauteur actuel évoluera vers une gouvernance collaborative.

5. **Le schéma est vivant** : Comme le projet qu'il documente, le schéma doit **évoluer sans trahir** ses principes fondateurs.

---

## 📊 Annexes

### Annexe A : Tableau Comparatif v1.0 vs v1.1

| Aspect | v1.0 | v1.1 (Proposé) |
|--------|------|----------------|
| Champs REQUIRED | 4 | 4 (inchangé) |
| Champs RECOMMENDED | 2 | 2 (inchangé) |
| Champs OPTIONAL | 2 | 7 (+5 nouveaux) |
| Types de documents | 5 | 5 (inchangé) |
| Types de relations | 4 | 8 (+4 nouvelles) |
| Support multi-auteurs | ❌ | ✅ |
| Granularité statuts | Moyenne | Élevée |
| Filtrage par domaine | ❌ | ✅ |
| Intent métier explicite | ❌ | ✅ |
| Rétrocompatibilité | N/A | ✅ 100% |

---

### Annexe B : Checklist de Migration

```markdown
## Checklist pour Migrer un Document de v1.0 vers v1.1

### Phase 1 : Lecture
- [ ] Lire le document actuel
- [ ] Identifier les contributeurs réels (auteur, relecteurs, etc.)
- [ ] Identifier le domaine d'application (scope)
- [ ] Identifier l'intent métier (pattern)

### Phase 2 : Enrichissement
- [ ] Ajouter le champ `role` si plusieurs contributeurs
- [ ] Ajouter le champ `scope` selon le domaine
- [ ] Ajouter le champ `pattern` selon l'intent
- [ ] Ajouter `decision_type` si ADR avec nuance
- [ ] Enrichir `links` avec nouvelles relations si applicable

### Phase 3 : Validation
- [ ] Exécuter `python3 scripts/validate_frontmatter.py --schema v1.1`
- [ ] Vérifier que le document reste lisible
- [ ] Comparer avec la version v1.0 (diff)

### Phase 4 : Commit
- [ ] Commit avec message explicite : `chore: migrate DOC-XXXX to schema v1.1`
- [ ] Vérifier que la CI passe
- [ ] Mettre à jour le registre (automatique)
```

---

### Annexe C : Scores de Pertinence Récapitulatifs

| Proposition | Score Pertinence | Score Urgence | Score Complexité | Score Final |
|-------------|------------------|---------------|------------------|-------------|
| `role` | 5/5 | 5/5 | 3/5 | **4.3/5** |
| `decision_type` | 4/5 | 3/5 | 2/5 | **3.7/5** |
| `scope` | 4/5 | 4/5 | 2/5 | **3.7/5** |
| Relations enrichies | 4/5 | 4/5 | 4/5 | **4.0/5** |
| `pattern` | 3/5 | 2/5 | 2/5 | **2.7/5** |

**Interprétation** :
- Score > 4.0 → **Priorité critique**
- Score 3.5-4.0 → **Priorité recommandée**
- Score < 3.5 → **Priorité optionnelle**

---

### Annexe D : Philosophie en Citations

> *"La grammaire évolue, mais le sens demeure."*

> *"Un système souverain ne grandit pas par rupture, mais par discernement."*

> *"La complexité naît du besoin, jamais de la prévoyance."*

> *"Le schéma évolue, mais son histoire demeure lisible."*

> *"La mémoire ne se réécrit pas, elle s'enrichit."*

> *"Être rigoureux sur l'essentiel, flexible sur l'accessoire."*

> *"La loi documentaire n'est pas écrite une fois pour toutes — elle s'affine à mesure que la vérité se clarifie."*

---

## 🌟 Conclusion

### Synthèse Exécutive

L'exploration de l'évolution du schéma documentaire Relinium vers v1.1 révèle un **besoin clair et urgent** d'enrichissement pour supporter une gouvernance collaborative à l'échelle.

**Constats clés** :
- ✅ Le schéma v1.0 est exemplaire dans sa simplicité et sa rigueur
- ⚠️ Il présente des lacunes structurelles pour la collaboration
- ✅ Les patterns de gouvernance observés guident naturellement l'évolution
- ⚠️ L'équilibre simplicité/expressivité doit être préservé

**Recommandations prioritaires** :
1. **Critique** : Implémenter le champ `role` pour la collaboration
2. **Recommandé** : Ajouter `scope` et `decision_type` pour la sémantique
