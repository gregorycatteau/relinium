---
id: "OBS-0100"
type: "OBS"
status: "Synthétisé"
date: "2025-11-08"
author: "Équipe Relinium Genesis"
version: "1.0"
tags: ["ssot", "exploration", "governance", "registry"]
links:
  cites: ["ADR-0001", "OBS-0001", "OBS-0002", "OBS-0003"]
---

# OBS-SSOT-EXPLORATION — Exploration documentaire de Relinium

- **Statut** : 🟢 Observation active
- **Date** : 2025-01-04
- **Auteur** : Agent d'exploration documentaire
- **Version** : 1.0
- **Mission** : Cartographier, analyser et comprendre la dynamique documentaire de Relinium

---

## 🎯 Préambule

Ce document est le fruit d'une exploration approfondie de la matière documentaire de Relinium. Il ne prescrit aucune structure définitive, mais observe, décrit et questionne ce qui existe pour révéler les patterns d'organisation cohérente, évolutive et vérifiable.

> _"On ne bâtit pas la demeure avant d'avoir observé la trajectoire du vent."_

---

## 1️⃣ CARTOGRAPHIE EXHAUSTIVE DE L'EXISTANT

### 1.1 Structure des répertoires principaux

```
relinium/
├── docs/                    [Documentation principale - 7 sous-domaines]
│   ├── 00-overview/        [Vision, principes, vocabulaire]
│   ├── 01-genesis/         [Fondations, charte de la matière]
│   ├── 02-strategy/        [Roadmap, axes de développement]
│   ├── 03-architecture/    [Décisions techniques - 3 types]
│   │   ├── decisions/      [ADR - Architecture Decision Records]
│   │   ├── rfcs/           [RFC - Request For Comments]
│   │   └── observations/   [OBS - Observations techniques]
│   ├── 04-risk/            [Modèles de menaces, registre de risques]
│   ├── 05-governance/      [Rôles, processus de décision]
│   ├── 06-ops/             [Opérations, maintenance, incidents]
│   └── 07-contrib/         [Guides de contribution, style]
│
├── lab/                     [Espace expérimental - 5 zones]
│   ├── pocs/               [POCs par composant - 8 familles]
│   │   ├── framework/      [4 candidats: axum, django, fastapi, gin]
│   │   ├── database/       [4 candidats: postgresql, mariadb, mongodb, sqlite]
│   │   ├── proxy/          [3 candidats: caddy, nginx, traefik]
│   │   ├── auth/           [3 candidats: authelia, keycloak, internal]
│   │   ├── storage/        [2 candidats: fs-local, minio]
│   │   ├── runtime/        [3 candidats: go, python, rust]
│   │   ├── observability/  [2 candidats: logs-basic, prometheus-grafana]
│   │   └── container/      [2 candidats: docker-compose, podman]
│   ├── stacks/             [Vide - préparé pour combinaisons complètes]
│   ├── scripts/            [Utilitaires: bench, checks, templates]
│   ├── seeds/              [Données de test transverses]
│   └── manifest.yaml       [Inventaire déclaratif des composants]
│
├── .github/                 [Gouvernance technique - 3 zones]
│   ├── workflows/          [CI/CD - validation docs]
│   ├── ISSUE_TEMPLATE/     [Templates d'issues]
│   └── CODEOWNERS          [Responsabilités]
│
└── [Racine]                 [Fichiers de gouvernance + compatibilité]
    ├── README.md           [Vision globale]
    ├── CONTRIBUTING.md     [Process de contribution]
    ├── GOVERNANCE.md       [Modèle de gouvernance]
    ├── SECURITY.md         [Politique de sécurité]
    ├── CODE_OF_CONDUCT.md  [Code de conduite]
    ├── LICENSE             [Licence]
    ├── Makefile            [Automatisation]
    ├── pocs/ → lab/pocs/   [Symlink compatibilité]
    ├── scripts/ → lab/scripts/ [Symlink compatibilité]
    └── seeds/ → lab/seeds/ [Symlink compatibilité]
```

### 1.2 Inventaire par type de document

#### **Documents de gouvernance** (8 fichiers racine)
- **Nature** : Contrats sociaux, règles du jeu, cadres éthiques
- **Stabilité** : Haute - modification rare et cérémonielle
- **Audience** : Tout acteur du projet (contributeur, utilisateur, observateur)

| Document | Rôle observé | Fréquence de modification |
|----------|--------------|---------------------------|
| README.md | Portail d'entrée, vision synthétique | Moyenne |
| CONTRIBUTING.md | Protocole d'engagement contributif | Faible |
| GOVERNANCE.md | Règles de décision collective | Très faible |
| SECURITY.md | Contrat de sécurité | Faible |
| CODE_OF_CONDUCT.md | Charte éthique | Très faible |
| LICENSE | Cadre légal | Immuable |
| Makefile | Automatisation technique | Moyenne |
| .gitignore | Frontière public/privé | Faible |

#### **Documents architecturaux** (docs/03-architecture/ - 3 types)

**Type ADR** (Architecture Decision Records) - 1 document observé
- **Nature** : Décisions structurantes prises et justifiées
- **Format** : ADR-NNNN-titre.md
- **Stabilité** : Immuable une fois accepté (principe historique)
- **Cycle de vie** : Proposition → Discussion → Acceptation/Rejet → Archivage
- **Exemple observé** : ADR-0001 (Repo driven by docs-first)

**Type RFC** (Request For Comments) - 2 documents observés
- **Nature** : Propositions ouvertes à discussion
- **Format** : RFC-NNN-titre.md
- **Stabilité** : Fluide pendant discussion, se cristallise en ADR
- **Cycle de vie** : Ébauche → Discussion → Maturation → ADR ou abandon
- **Exemples observés** : 
  - RFC-001 (Choix stack initiale)
  - RFC-002 (Backend et scoring matrix)

**Type OBS** (Observations) - 3 documents observés
- **Nature** : Rapports d'observation technique, inventaires
- **Format** : OBS-NNNN-titre.md
- **Stabilité** : Vivant - s'enrichit au fil des découvertes
- **Cycle de vie** : Ouvert → En observation → Synthétisé → Peut alimenter RFC
- **Exemples observés** :
  - OBS-0001 (Inventaire composants backend)
  - OBS-0002 (Tests initiaux)
  - OBS-0003 (Calibration et SLOs)

#### **Documents expérimentaux** (lab/pocs/ - triptyque POC)

**Triptyque systématique pour chaque POC** (27 POCs × 3 fichiers = 81 documents)
- **POC.md** : Protocole, objectif, environnement, commandes
- **RESULTS.md** : Résultats bruts, métriques, verdict
- **SECURITY.md** : Surface d'attaque, menaces, durcissements

**Métadonnées communes observées** :
- Famille (framework, database, proxy, etc.)
- Candidat (nom de la technologie)
- Version testée
- Date, auteur
- Statut (existing, planned, idea)

#### **Documents de manifeste** (métadonnées structurelles)

**lab/manifest.yaml** - Inventaire déclaratif
- Liste exhaustive des composants existants
- Planification des stacks futures
- Conventions d'exécution (make targets)
- Philosophie et principes du Lab

### 1.3 Densité et profondeur documentaire

#### Zones à forte densité
1. **docs/03-architecture/** : Zone la plus documentée
   - 1 ADR, 2 RFC, 3 OBS = 6 documents
   - Profondeur modérée (1 niveau de sous-dossiers)
   - Lien fort avec lab/pocs/

2. **lab/pocs/** : Zone la plus volumineuse
   - 27 POCs × triptyque = 81 documents techniques
   - Profondeur de 3 niveaux (lab/pocs/famille/candidat/)
   - Structure hautement régulière

#### Zones à faible densité (mais haute intention)
1. **docs/00-overview/** : Vide mais nommé
2. **docs/01-genesis/** : Vide mais nommé
3. **docs/02-strategy/** : Vide mais nommé
4. **docs/04-risk/** : Vide mais mentionné (threat_model.md, risk_register.md)
5. **docs/05-governance/** : Vide mais GOVERNANCE.md existe à la racine
6. **docs/06-ops/** : 1 document (email-normalization-report.md)
7. **docs/07-contrib/** : Vide mais CONTRIBUTING.md existe à la racine
8. **lab/stacks/** : Vide mais préparé (3 stacks planifiées dans manifest.yaml)
9. **lab/seeds/** : Vide ou très léger

### 1.4 Interdépendances documentaires observées

#### Liens explicites (citations directes)
- ADR-0001 → RFC-001 (référence mutuelle)
- RFC-001 → ADR-0001 (justification méthodologique)
- OBS-0001 → RFC-002 (lien de référence)
- CONTRIBUTING.md → ADR + RFC (processus)
- GOVERNANCE.md → ADR (validation)
- lab/README.md → docs/03-architecture/ (traçabilité OBS/RFC/ADR)

#### Liens implicites (flux logique)
- POC.md → RESULTS.md → (potentiellement) OBS → RFC → ADR
- Observation terrain (lab/) → Synthèse (OBS) → Proposition (RFC) → Décision (ADR)
- manifest.yaml ↔ lab/pocs/ (inventaire structurel)
- SECURITY.md ↔ POC/*/SECURITY.md (cohérence sécuritaire)

---

## 2️⃣ INTENTIONS DÉTECTÉES

### 2.1 Par zone documentaire

#### **docs/** - La conscience du projet
**Intention première** : Être la source unique de vérité (SSOT) pour toutes les décisions
- Structuration par domaine (overview, genesis, strategy, architecture, risk, governance, ops, contrib)
- Principe : "La documentation n'est pas le récit, elle en est la conscience"
- Séparation claire : décisions (ADR) / discussions (RFC) / observations (OBS)

**Intention secondaire** : Traçabilité historique complète
- ADR immuables = mémoire des choix
- RFC évolutifs = journal des réflexions
- OBS vivants = carnet de terrain

#### **lab/** - Le laboratoire expérimental
**Intention première** : Tester avant de décider
- Approche scientifique : protocole (POC.md) → expérience → résultat (RESULTS.md)
- Isolation des composants (pocs/) avant assemblage (stacks/)
- Reproductibilité : make dev/test/bench/stop

**Intention secondaire** : Documentation comme trace de transformation
- Triptyque systématique (POC/RESULTS/SECURITY)
- Principe : "L'humain d'abord, la technique comme prolongement"
- manifest.yaml comme "métadonnée de métadonnées"

#### **Racine** - Le contrat social
**Intention première** : Établir les règles du jeu
- Gouvernance, sécurité, contribution, éthique
- Accessibilité immédiate (README first)
- Symlinks de compatibilité (pocs/, scripts/, seeds/) = respect de l'historique

### 2.2 Philosophie sous-jacente (extraite des documents)

**Principe cardinal : Docs-First**
- Citation ADR-0001 : "Documentation = artefact exécutable"
- Rien ne se code sans document de référence
- Le code reflète les décisions, ne les précède pas

**Principe humain : Temps long et travail réfléchi**
- CONTRIBUTING.md : "Discuter avant de coder"
- GOVERNANCE.md : "Transparence radicale"
- lab/README.md : "Traçabilité par la documentation"

**Principe écologique : Sobriété et souveraineté**
- README.md : "Sobre et souverain"
- RFC-001 : Critères de sélection (sobriété poids 4/5)
- lab/manifest.yaml : "Exécution locale, reproductible, sobre"

**Principe scientifique : Observer → Clarifier → Décider**
- OBS → RFC → ADR (flux observé)
- lab/pocs/ : protocole expérimental rigoureux
- "Avant de forger l'outil, connaître la nature du métal" (OBS-0001)

---

## 3️⃣ POINTS DE TENSION

### 3.1 Redondances structurelles

#### **Gouvernance distribuée vs. centralisée**
- GOVERNANCE.md (racine) vs. docs/05-governance/ (vide)
- **Tension** : Où placer les futurs documents de gouvernance ?
- **Observation** : Gouvernance.md pourrait être l'index, 05-governance/ les détails

#### **Contribution distribuée vs. centralisée**
- CONTRIBUTING.md (racine) vs. docs/07-contrib/ (vide)
- **Tension** : Même pattern que gouvernance
- **Observation** : CONTRIBUTING.md = guide général, 07-contrib/ = guides spécialisés

#### **Sécurité distribuée**
- SECURITY.md (racine, politique générale)
- docs/04-risk/ (vide mais mentionné : threat_model.md, risk_register.md)
- lab/pocs/*/SECURITY.md (81 fichiers de sécurité spécifique)
- **Tension** : Risque de désynchronisation entre niveaux
- **Observation** : Hiérarchie : SECURITY.md (politique) → 04-risk/ (modèle) → pocs/SECURITY.md (implémentation)

#### **Compatibilité historique via symlinks**
- pocs/ → lab/pocs/ (symlink)
- scripts/ → lab/scripts/ (symlink)
- seeds/ → lab/seeds/ (symlink)
- **Tension** : Dette technique, confusion pour nouveaux contributeurs
- **Observation** : LAB_REFACTOR_NOTES.md documente cette transition
- **Question** : Jusqu'à quand maintenir ces symlinks ?

### 3.2 Zones vides mais nommées (intentions vs. réalité)

#### **Répertoires intentionnels mais vides**
| Répertoire | Intention déclarée | Documents manquants |
|------------|-------------------|---------------------|
| docs/00-overview/ | Vision, principes, vocabulaire | vision.md, principles.md, glossary.md |
| docs/01-genesis/ | Charte de la matière | charte_matiere.md |
| docs/02-strategy/ | Roadmap, axes | roadmap.md, axes.md |
| docs/04-risk/ | Menaces, risques | threat_model.md, risk_register.md |
| docs/05-governance/ | Processus, rôles | (détails de gouvernance) |
| docs/07-contrib/ | Guides | style_guide.md, conventions.md |
| lab/stacks/ | POCs complets | django-postgresql-caddy/, etc. |
| lab/seeds/ | Données test | (seeds transverses) |

**Observation** : Structure anticipatoire forte, contenu différé
**Question** : S'agit-il d'un scaffold intentionnel ou d'une dette documentaire ?

### 3.3 Documents orphelins ou faiblement reliés

#### **Documents isolés**
- **docs/06-ops/email-normalization-report.md** : Document technique isolé
  - Pas de lien explicite avec d'autres documents
  - Pas dans une famille claire (ops/reports/, ops/runbooks/ ?)
  - **Observation** : Pourrait être le premier d'une série de rapports ops

- **LAB_REFACTOR_NOTES.md** (racine) : Document de transition
  - Temporaire par nature
  - Devrait migrer vers docs/06-ops/migrations/ ou être supprimé

### 3.4 Chemins documentaires naturels (séquences logiques)

#### **Flux observé : Expérimentation → Décision**
```
1. lab/pocs/framework/fastapi/POC.md
   → Protocole expérimental
2. lab/pocs/framework/fastapi/RESULTS.md
   → Résultats mesurés
3. docs/03-architecture/observations/OBS-0001-backend-composants-inventaire.md
   → Synthèse comparative
4. docs/03-architecture/rfcs/RFC-001-choix-stack-initiale.md
   → Proposition de choix
5. docs/03-architecture/decisions/ADR-000X-choix-backend.md (à venir)
   → Décision actée
```

**Observation** : Flux cohérent mais incomplet (ADR finaux manquants)

#### **Flux observé : Gouvernance → Application**
```
1. GOVERNANCE.md (racine)
   → Principes généraux
2. CONTRIBUTING.md (racine)
   → Process contributif
3. CODE_OF_CONDUCT.md (racine)
   → Règles éthiques
4. .github/CODEOWNERS
   → Responsabilités techniques
5. .github/workflows/ci-docs.yml
   → Validation automatique
```

**Observation** : Flux complet et opérationnel

---

## 4️⃣ LIENS ÉMERGENTS

### 4.1 Relations implicites fortes

#### **lab/manifest.yaml ↔ Structure des POCs**
- manifest.yaml déclare 27 composants
- Structure lab/pocs/ reflète exactement cette liste
- **Lien émergent** : manifest.yaml = single source of truth structurelle
- **Potentiel** : Génération automatique de POCs à partir du manifeste

#### **OBS + RFC → ADR (pipeline décisionnel)**
- OBS-0001 alimente RFC-002 (référence explicite)
- RFC-001 cite ADR-0001 (validation méthodologique)
- **Lien émergent** : Les OBS sont la matière première des RFC
- **Potentiel** : Automatiser les liens bidirectionnels

#### **Triptyque POC ↔ Critères RFC**
- POC.md décrit l'environnement et le protocole
- RESULTS.md fournit les métriques
- RFC-001 définit des critères de sélection pondérés
- **Lien émergent** : Les RESULTS.md alimentent directement les matrices de scoring
- **Potentiel** : Scoring automatisé depuis RESULTS.md structurés

### 4.2 Patterns d'organisation émergents

#### **Pattern : Numérotation séquentielle**
- ADR-NNNN (ex: ADR-0001)
- RFC-NNN (ex: RFC-001)
- OBS-NNNN (ex: OBS-0001)
- **Observation** : Numérotation séquentielle = ordre chronologique
- **Question** : Comment gérer les bifurcations ? (ADR-0001 → ADR-0001-bis ?)

#### **Pattern : Triptyque systématique**
- Appliqué à 100% des POCs (POC/RESULTS/SECURITY)
- **Observation** : Structure prédictible = facilite l'automatisation
- **Potentiel** : Étendre aux stacks (lab/stacks/*/STACK.md, RESULTS.md, SECURITY.md)

#### **Pattern : Statut en émoji**
- ✅ Accepté (ADR)
- 🟡 En discussion (RFC)
- 🟢 Ouvert (OBS)
- **Observation** : Visibilité immédiate de l'état
- **Question** : Standardiser davantage ? (⚠️ Déprécié, ❌ Rejeté, 🔒 Figé)

#### **Pattern : Métadonnées structurées en en-tête**
Observé dans tous les documents ADR/RFC/OBS :
```markdown
- **Statut** : [émoji] [état]
- **Date** : YYYY-MM-DD
- **Auteur** : [nom]
- **Version** : X.Y
```
**Observation** : Prêt pour extraction automatisée (YAML frontmatter)

### 4.3 Cohérence documentaire observée

#### **Points forts**
1. **Terminologie stable** : ADR, RFC, OBS utilisés de manière cohérente
2. **Structure régulière** : En-têtes similaires, sections récurrentes
3. **Liens bidirectionnels** : Les documents se citent mutuellement
4. **Traçabilité temporelle** : Dates systématiques
5. **Signature claire** : Auteurs identifiés

#### **Points de vigilance**
1. **Versions** : Présentes mais pas de politique de versioning explicite
2. **Statuts** : Utilisés mais pas de machine d'état formelle (transitions)
3. **Archivage** : Pas de process clair pour documents obsolètes
4. **Recherche** : Pas d'index global, recherche manuelle nécessaire

---

## 5️⃣ ZONES MUETTES (silence documentaire)

### 5.1 Intentions déclarées mais non matérialisées

#### **Vision et principes** (docs/00-overview/)
- README.md cite "docs/00-overview/vision.md" (absent)
- README.md cite "docs/00-overview/principles.md" (absent)
- ADR-0001 cite "docs/01-genesis/charte_matiere.md" (absent)
- **Impact** : Les fondations philosophiques existent oralement mais pas textuellement

#### **Modèle de menaces** (docs/04-risk/)
- SECURITY.md cite "docs/04-risk/threat_model.md" (absent)
- SECURITY.md cite "docs/04-risk/risk_register.md" (absent)
- **Impact** : La sécurité est un principe mais pas un corpus opérationnel

#### **Roadmap stratégique** (docs/02-strategy/)
- README.md mentionne "docs/02-strategy/" comme zone de roadmap
- Complètement vide
- **Impact** : Pas de visibilité sur l'évolution future du projet

### 5.2 Processus implicites non documentés

#### **Cycle de vie d'un document**
- Comment un RFC devient-il ADR ?
- Qui valide ? Quel processus de vote ?
- Quand archive-t-on un document obsolète ?
- **Observation** : GOVERNANCE.md décrit le processus général, mais pas le workflow précis

#### **Workflow Git**
- Branches protégées ?
- Revue obligatoire ?
- Signature des commits ?
- **Observation** : SECURITY.md et CONTRIBUTING.md mentionnent ces points, mais pas de workflow.md consolidé

#### **Maintenance documentaire**
- Fréquence de révision des docs ?
- Qui surveille la cohérence entre docs/ et code ?
- Comment détecter les docs obsolètes ?
- **Observation** : Silence total

### 5.3 Métadonnées manquantes

#### **Relations structurées**
- Pas de graphe explicite ADR ← RFC ← OBS
- Liens en Markdown mais pas en métadonnées exploitables
- **Potentiel** : Tags, références croisées automatisables

#### **Versions et historique**
- Versions présentes mais pas de CHANGELOG par document
- Pas de git blame facilité
- **Potentiel** : Frontmatter YAML avec historique

#### **Glossaire et ontologie**
- Termes récurrents : docs-first, SSOT, triptyque, souveraineté, sobriété
- Mais pas de docs/00-overview/glossary.md
- **Impact** : Risque d'ambiguïté terminologique à mesure que le projet grandit

---

## 6️⃣ MÉTRIQUES QUANTITATIVES

### 6.1 Volumétrie documentaire

| Zone | Fichiers | Répertoires | Profondeur max |
|------|----------|-------------|----------------|
| docs/ | 6 actuels | 7 domaines | 3 niveaux |
| lab/pocs/ | 81 (27×3) | 35 | 4 niveaux |
| lab/ total | ~85 | ~40 | 4 niveaux |
| Racine | 8 gouvernance | - | - |
| .github/ | ~10 | 3 | 2 niveaux |
| **TOTAL** | ~110 fichiers documentaires | - | - |

### 6.2 Densité par type

| Type | Quantité | Statut moyen |
|------|----------|--------------|
| ADR | 1 | Accepté |
| RFC | 2 | En discussion |
| OBS | 3 | Ouvert |
| POC triptyque | 81 | Mixte (existing/planned) |
| Gouvernance | 8 | Stable |
| Manifeste | 1 | Vivant |

### 6.3 Taux de remplissage

| Domaine | Planifié | Rempli | Taux |
|---------|----------|--------|------|
| docs/00-overview/ | 3-5 docs | 0 | 0% |
| docs/01-genesis/ | 2-3 docs | 0 | 0% |
| docs/02-strategy/ | 2-4 docs | 0 | 0% |
| docs/03-architecture/ | Évolutif | 6 | 100% (actuel) |
| docs/04-risk/ | 2-3 docs | 0 | 0% |
| docs/05-governance/ | 3-5 docs | 1 (racine) | 20% |
| docs/06-ops/ | Évolutif | 1 | Initial |
| docs/07-contrib/ | 2-4 docs | 1 (racine) | 25% |
| lab/pocs/ | 27 composants | 27 | 100% |
| lab/stacks/ | 3 planifiées | 0 | 0% |

**Observation globale** : Forte densité expérimentale (lab/pocs/), faible densité fondationnelle (docs/0X-overview, genesis, strategy)

---

## 7️⃣ SYNTHÈSE OBSERVATOIRE

### 7.1 Ce que révèle la matière documentaire

#### **Un projet en phase Genesis authentique**
- Structure anticipatoire (scaffold) forte
- Contenu différé intentionnellement
- Philosophie docs-first appliquée rigoureusement
- Priorité à la méthode sur la vitesse

#### **Une approche scientifique du développement**
- Expérimentation systématique (lab/)
- Observation → Clarification → Décision (OBS → RFC → ADR)
- Traçabilité comme valeur cardinale
- Reproductibilité privilégiée

#### **Une tension entre idéal et pragmatisme**
- Idéal : Tout documenter avant de coder
- Pragmatisme : Expérimenter dans lab/ pour apprendre
- Résolution : Le lab est l'espace du "pas encore décidé"

#### **Une architecture documentaire fractale**
- Pattern triptyque se répète (POC/RESULTS/SECURITY)
- Même logique à différents niveaux (docs/, lab/, racine)
- Métadonnées structurées similaires partout
- **Observation** : Prêt à scaler

### 7.2 Constats vérifiables

1. ✅ **100% des POCs suivent le triptyque** (POC/RESULTS/SECURITY)
2. ✅ **100% des décisions techniques passent par docs/03-architecture/**
3. ✅ **Aucun code sans document de référence** (principe respecté)
4. ⚠️ **~60% des zones docs/ sont vides** (intentionnel mais incomplet)
5. ⚠️ **Liens entre documents présents mais non exploitables automatiquement**
6. ⚠️ **Pas de registre central des documents** (navigation manuelle)

### 7.3 Questions émergentes pour la suite

#### **Sur la structure**
- Faut-il maintenir la séparation docs/ vs. lab/ ou unifier dans docs/lab/ ?
- Comment gérer les stacks dans lab/stacks/ ? (même tripty
