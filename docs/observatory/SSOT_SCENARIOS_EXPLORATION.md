# SSOT_SCENARIOS_EXPLORATION — Scénarios d'organisation documentaire

- **Statut** : 🔍 Exploration comparative
- **Date** : 2025-01-04
- **Auteur** : Agent d'exploration documentaire
- **Version** : 1.0
- **Source** : OBS-SSOT-EXPLORATION.md + DNA-v0.1.yaml

---

## 🎯 Objectif

À partir des invariants détectés dans le DNA v0.1 et des observations terrain, ce document propose et compare plusieurs modèles d'organisation possibles pour le futur SSOT (Single Source of Truth) de Relinium.

**Principe directeur** : Aucun modèle n'est imposé. Chaque scénario est évalué selon sa robustesse, sa capacité à absorber l'incertitude, et sa facilité d'audit.

---

## 1️⃣ CRITÈRES D'ÉVALUATION

### 1.1 Grille d'analyse

| Critère | Poids | Description |
|---------|-------|-------------|
| **Scalabilité documentaire** | 🔥 5 | Croissance du projet sans réorganisation majeure |
| **Absorption de l'incertitude** | 🔥 5 | Gestion des versions, bifurcations, contradictions |
| **Auditabilité humaine** | ⚙️ 4 | Compréhension intuitive, navigation aisée |
| **Auditabilité machine** | ⚙️ 4 | Validation automatisée, extraction de métadonnées |
| **Maintenabilité** | ⚙️ 4 | Effort requis pour maintenir la cohérence |
| **Résilience aux migrations** | ⚙️ 3 | Capacité à absorber des restructurations |
| **Compatibilité outillage** | ⚙️ 3 | Facilité d'intégration d'outils (CI, générateurs) |

### 1.2 Échelle de notation

- ✅ **Excellent** (5/5) : Critère pleinement satisfait
- 🟢 **Bon** (4/5) : Critère bien satisfait avec marge d'amélioration
- 🟡 **Moyen** (3/5) : Critère partiellement satisfait, compromis nécessaires
- 🟠 **Faible** (2/5) : Critère peu satisfait, risques identifiés
- 🔴 **Insuffisant** (1/5) : Critère non satisfait, blocage potentiel

---

## 2️⃣ SCÉNARIO A — STRUCTURE ACTUELLE CONSOLIDÉE

### 2.1 Description

Conserver la structure actuelle (docs/ + lab/) en la consolidant :
- Remplir les zones vides (00-overview, 01-genesis, 02-strategy, 04-risk)
- Maintenir la séparation docs/ (source de vérité) / lab/ (expérimentation)
- Améliorer les liens entre documents
- Ajouter un registre central des documents

```
relinium/
├── docs/                    [SSOT - Source de vérité]
│   ├── 00-overview/         [Vision, principes, glossaire]  ← À remplir
│   ├── 01-genesis/          [Charte de la matière]         ← À remplir
│   ├── 02-strategy/         [Roadmap, axes]                ← À remplir
│   ├── 03-architecture/     [ADR/RFC/OBS]                  ✓ Opérationnel
│   ├── 04-risk/             [Threat model, risk register]  ← À remplir
│   ├── 05-governance/       [Processus détaillés]          ← À enrichir
│   ├── 06-ops/              [Runbooks, incidents]          ← À structurer
│   ├── 07-contrib/          [Guides spécialisés]           ← À enrichir
│   └── _registry/           [Index central]                ← À créer
│
├── lab/                     [Expérimentation]
│   ├── pocs/                [Tests composants]             ✓ Opérationnel
│   ├── stacks/              [Tests intégrés]               ← À développer
│   ├── scripts/             [Utilitaires]                  ✓ Opérationnel
│   └── seeds/               [Données test]                 ← À remplir
│
└── [Racine]                 [Gouvernance + compatibilité]  ✓ Stable
```

### 2.2 Avantages

✅ **Continuité forte**
- Pas de rupture avec l'existant
- Symlinks préservés (pocs/, scripts/, seeds/)
- Contributeurs gardent leurs repères

✅ **Clarté de séparation**
- docs/ = décisionnel, figé ou évolutif selon type
- lab/ = expérimental, temporaire
- Intentions claires pour chaque zone

✅ **Scalabilité modulaire**
- Chaque domaine (00-07) est indépendant
- Ajout de sous-domaines facile (ex: docs/08-legal/)

✅ **Outillage existant**
- CI déjà configurée sur docs/
- Makefile opérationnel sur lab/

### 2.3 Limites

🟠 **Zones vides créent de la confusion**
- ~60% de docs/ est vide
- Risque de "fausse promesse" pour nouveaux contributeurs
- Structure anticipatoire peut sembler sur-ingénieurée

🟡 **Redondances gouvernance/contrib**
- GOVERNANCE.md (racine) vs. docs/05-governance/
- CONTRIBUTING.md (racine) vs. docs/07-contrib/
- Risque de désynchronisation entre niveaux

🟡 **Pas de registre central natif**
- Navigation manuelle entre documents
- Liens en Markdown mais pas de graph

exploitable
- Recherche de documents par métadonnées impossible

### 2.4 Évaluation

| Critère | Note | Justification |
|---------|------|---------------|
| Scalabilité documentaire | 🟢 4/5 | Structure modulaire permet la croissance, mais zones vides peuvent freiner |
| Absorption incertitude | 🟢 4/5 | Séparation lab/docs gère bien l'expérimental vs. décidé |
| Auditabilité humaine | 🟡 3/5 | Intuitive mais zones vides créent confusion |
| Auditabilité machine | 🟡 3/5 | Possible mais nécessite ajout d'outillage (registre, frontmatter) |
| Maintenabilité | 🟢 4/5 | Structure claire facilite maintenance |
| Résilience migrations | 🟢 4/5 | Symlinks et modularité facilitent ajustements |
| Compatibilité outillage | ✅ 5/5 | CI/CD déjà en place, extensible |

**Score global** : 26/35 (74%)

### 2.5 Conditions de viabilité

Pour que ce scénario soit optimal :
1. **Remplir progressivement les zones vides** (roadmap claire)
2. **Créer docs/_registry/** (index central des documents)
3. **Clarifier hiérarchie** GOVERNANCE.md → docs/05-governance/ (index vs. détails)
4. **Automatiser la validation** des liens et métadonnées
5. **Documenter la philosophie** des zones dans chaque README.md de domaine

---

## 3️⃣ SCÉNARIO B — UNIFICATION DOCS-CENTRIC

### 3.1 Description

Fusionner lab/ dans docs/ pour une source unique :
- docs/ devient l'unique racine documentaire
- lab/ devient docs/08-lab/ ou docs/experiments/
- Tout est "documentation", certains documents sont expérimentaux

```
relinium/
├── docs/                    [SSOT unique et total]
│   ├── 00-overview/         [Vision, principes]
│   ├── 01-genesis/          [Charte]
│   ├── 02-strategy/         [Roadmap]
│   ├── 03-architecture/     [ADR/RFC/OBS]
│   │   ├── decisions/
│   │   ├── rfcs/
│   │   ├── observations/
│   │   └── experiments/     [Ex-lab/pocs/, statut expérimental]
│   ├── 04-risk/             [Sécurité]
│   ├── 05-governance/       [Processus]
│   ├── 06-ops/              [Opérations]
│   ├── 07-contrib/          [Contribution]
│   ├── 08-lab/              [Zone expérimentale intégrée]
│   │   ├── pocs/
│   │   ├── stacks/
│   │   └── seeds/
│   ├── 09-tools/            [Scripts, utilitaires]
│   └── _meta/               [Registre, DNA, indices]
│
└── [Racine]                 [Gouvernance + rétrocompat]
```

### 3.2 Avantages

✅ **SSOT authentique**
- Une seule arborescence pour tout
- Pas de question "où documenter X ?"
- docs/ est LA source de vérité absolue

✅ **Cohérence philosophique**
- "Docs-first" appliqué littéralement
- Même l'expérimentation est documentation
- lab/pocs/*/POC.md devient docs/.../experiments/POC.md

✅ **Uniformisation des métadonnées**
- Même format frontmatter partout
- Même système de numérotation
- Même process de validation

✅ **Registre centralisé naturel**
- docs/_meta/ contient tout (DNA, registre, indices)
- Navigation facilitée

### 3.3 Limites

🔴 **Rupture majeure avec l'existant**
- Migration massive nécessaire
- Symlinks plus complexes ou à supprimer
- Risque de perte d'historique Git si mal géré

🔴 **Confusion conceptuelle**
- lab/ actuel = "pas encore décidé"
- L'intégrer à docs/ = "c'est documenté donc validé" ?
- Risque de dilution du statut "source de vérité"

🟠 **Complexité accrue**
- docs/ devient très volumineux
- Profondeur augmente (docs/03-architecture/experiments/pocs/...)
- Navigation plus lourde

🟡 **Scripts et seeds dans docs/**
- Conceptuellement étrange (ce ne sont pas des documents)
- Pourrait polluer le corpus documentaire

### 3.4 Évaluation

| Critère | Note | Justification |
|---------|------|---------------|
| Scalabilité documentaire | 🟢 4/5 | Unique racine facilite croissance mais profondeur peut poser problème |
| Absorption incertitude | 🟡 3/5 | Dilution du statut "expérimental" vs. "validé" |
| Auditabilité humaine | 🟡 3/5 | Volumétrie rend navigation plus complexe |
| Auditabilité machine | ✅ 5/5 | Uniformité maximale = automatisation optimale |
| Maintenabilité | 🟡 3/5 | Migration complexe, maintenance lourde ensuite |
| Résilience migrations | 🔴 2/5 | Rupture forte, difficile à revenir en arrière |
| Compatibilité outillage | 🟢 4/5 | CI à adapter mais bénéfice de l'uniformité |

**Score global** : 24/35 (69%)

### 3.5 Conditions de viabilité

Pour que ce scénario soit viable :
1. **Migration progressive** (pas de big bang)
2. **Maintenir rétrocompatibilité** (redirections, symlinks temporaires)
3. **Clarifier sémantique** (expérimental vs. validé via statuts clairs)
4. **Séparer scripts/seeds** (peut-être hors de docs/, ou docs/_assets/)
5. **Outillage robuste** pour compenser la complexité

---

## 4️⃣ SCÉNARIO C — APPROCHE FÉDÉRÉE (Multi-SSOT)

### 3.1 Description

Plusieurs SSOT thématiques au lieu d'un unique :
- docs/ = SSOT décisionnel (ADR, RFC, gouvernance)
- lab/ = SSOT expérimental (POCs, tests, résultats)
- knowledge/ = SSOT connaissances (guides, tutoriels, glossaire)
- Chaque SSOT a son DNA spécifique

```
relinium/
├── docs/                    [SSOT Décisionnel]
│   ├── architecture/        [ADR, RFC]
│   ├── governance/          [Processus, règles]
│   ├── risk/                [Sécurité, menaces]
│   └── _meta/               [DNA décisionnel]
│
├── lab/                     [SSOT Expérimental]
│   ├── pocs/                [Tests composants]
│   ├── stacks/              [Tests intégrés]
│   ├── seeds/               [Données]
│   └── _meta/               [DNA expérimental]
│
├── knowledge/               [SSOT Connaissance]
│   ├── guides/              [Tutoriels, how-to]
│   ├── references/          [Glossaire, API]
│   ├── vision/              [Vision, principes]
│   └── _meta/               [DNA connaissance]
│
└── [Racine]                 [Orchestration des SSOT]
    └── _registry/           [Registre global inter-SSOT]
```

### 4.2 Avantages

✅ **Séparation des préoccupations maximale**
- Chaque SSOT a sa logique propre
- Moins de risque de confusion conceptuelle
- Audiences différentes pour chaque SSOT

✅ **Autonomie des domaines**
- Équipes peuvent gérer leur SSOT indépendamment
- Évolutions parallèles possibles
- Moins de contention sur les décisions structurelles

✅ **Flexibilité**
- Chaque SSOT peut évoluer à son rythme
- Ajout/suppression de SSOT facile
- Expérimentations possibles sans impacter le reste

### 4.3 Limites

🔴 **Complexité organisationnelle**
- Qui décide ce qui va où ?
- Frontières entre SSOT floues (ex: guides vs. observations)
- Risque de multiplication anarchique des SSOT

🔴 **Synchronisation difficile**
- Liens inter-SSOT complexes à maintenir
- Risque de contradiction entre SSOT
- Registre global devient critique et complexe

🔴 **Auditabilité fragmentée**
- Pas de vue d'ensemble immédiate
- Navigation entre SSOT requiert apprentissage
- Recherche transverse complexe

🟠 **Overhead de gouvernance**
- DNA par SSOT = maintenance multipliée
- Processus de validation par SSOT
- Risque de divergence des pratiques

### 4.4 Évaluation

| Critère | Note | Justification |
|---------|------|---------------|
| Scalabilité documentaire | ✅ 5/5 | Modularité maximale, chaque SSOT scale indépendamment |
| Absorption incertitude | 🟢 4/5 | Excellente isolation, mais synchronisation délicate |
| Auditabilité humaine | 🟠 2/5 | Fragmentation rend vue d'ensemble difficile |
| Auditabilité machine | 🟡 3/5 | Possible mais nécessite orchestration complexe |
| Maintenabilité | 🟠 2/5 | Overhead important, risque de désynchronisation |
| Résilience migrations | 🟢 4/5 | Chaque SSOT peut migrer indépendamment |
| Compatibilité outillage | 🟡 3/5 | Outillage doit gérer multi-SSOT |

**Score global** : 23/35 (66%)

### 4.5 Conditions de viabilité

Pour que ce scénario soit viable :
1. **Définir frontières claires** entre SSOT (matrice de décision)
2. **Registre global robuste** avec liens bidirectionnels automatiques
3. **Gouvernance inter-SSOT** (qui arbitre les conflits ?)
4. **Outillage d'orchestration** (recherche transverse, validation cohérence)
5. **Documentation explicite** du modèle fédéré pour contributeurs

---

## 5️⃣ SCÉNARIO D — APPROCHE TEMPORELLE (Timeline-Based)

### 5.1 Description

Organisation chronologique avec snapshots immuables :
- Chaque décision/observation crée un snapshot daté
- L'historique devient navigable comme une timeline
- Versions figées coexistent avec version "HEAD"

```
relinium/
├── timeline/                [Snapshots chronologiques]
│   ├── 2025-01/             [Snapshot mensuel ou par jalon]
│   │   ├── decisions/
│   │   ├── observations/
│   │   └── experiments/
│   ├── 2025-02/
│   └── current/             [État actuel, volatile]
│
├── index/                   [Accès par thématique]
│   ├── by-topic/            [Index thématique]
│   ├── by-type/             [Index par type (ADR, RFC, OBS)]
│   └── by-status/           [Index par statut]
│
└── _meta/                   [DNA, registres, graphes]
```

### 5.2 Avantages

✅ **Immutabilité maximale**
- Chaque snapshot est figé
- Impossible de "perdre" un état passé
- Audit historique total

✅ **Gestion des versions native**
- Pas besoin de git blame
- Chaque période a sa cohérence propre
- Facilite les comparaisons temporelles

✅ **Traçabilité ultime**
- Évolution du projet tracée naturellement
- Identification claire des pivots
- Documentation = time machine

### 5.3 Limites

🔴 **Navigation très complexe**
- Trouver l'information actuelle difficile
- Multiplication des fichiers (redondance)
- Courbe d'apprentissage raide

🔴 **Maintenance explosive**
- Chaque modif = nouveau snapshot ?
- Taille du dépôt explose rapidement
- Git devient surchargé

🔴 **Pas adapté à la phase Genesis**
- Trop peu de contenu pour justifier snapshots
- Sur-ingénierie pour un projet naissant
- Complexité disproportionnée

🟠 **Recherche thématique complexe**
- Index indispensables mais lourds à maintenir
- Risque de désynchronisation index/timeline

### 5.4 Évaluation

| Critère | Note | Justification |
|---------|------|---------------|
| Scalabilité documentaire | 🟡 3/5 | Scale mais au prix d'une explosion volumétrique |
| Absorption incertitude | ✅ 5/5 | Parfait pour versions, bifurcations, contradictions |
| Auditabilité humaine | 🔴 1/5 | Navigation très complexe, contre-intuitive |
| Auditabilité machine | 🟢 4/5 | Structure prédictible = automatisation facile |
| Maintenabilité | 🔴 1/5 | Overhead insoutenable pour équipe réduite |
| Résilience migrations | 🟡 3/5 | Chaque snapshot isolé mais migrations lourdes |
| Compatibilité outillage | 🟡 3/5 | Nécessite outillage spécifique (timeline browser) |

**Score global** : 20/35 (57%)

### 5.5 Conditions de viabilité

Pour que ce scénario soit viable :
1. **Projet mature** avec historique riche (pas adapté à Genesis)
2. **Outillage de navigation** dédié (time machine, diff entre snapshots)
3. **Automatisation totale** des snapshots et indices
4. **Équipe dédiée** à la maintenance documentaire
5. **Besoin réel d'immutabilité forte** (réglementaire, audit légal)

---

## 6️⃣ SYNTHÈSE COMPARATIVE

### 6.1 Tableau récapitulatif

| Scénario | Score | Complexité | Adéquation Genesis | Rupture | Recommandation |
|----------|-------|------------|-------------------|---------|----------------|
| **A - Actuel consolidé** | 26/35 (74%) | Moyenne | ✅ Excellente | Faible | **Recommandé** |
| **B - Unification docs/** | 24/35 (69%) | Haute | 🟡 Moyenne | Forte | Possible à terme |
| **C - Fédération multi-SSOT** | 23/35 (66%) | Très haute | 🟠 Faible | Forte | Non recommandé |
| **D - Timeline-based** | 20/35 (57%) | Extrême | 🔴 Inadapté | Très forte | Non adapté Genesis |

### 6.2 Recommandation principale

**🎯 Scénario A (Structure actuelle consolidée) est le plus adapté** pour les raisons suivantes :

1. **Continuité** : Pas de rupture majeure, respect de l'existant
2. **Équilibre** : Bon compromis complexité / bénéfices
3. **Pragmatisme** : Adapté à la phase Genesis et à l'équipe actuelle
4. **Évolutivité** : Peut évoluer vers B si besoin futur
5. **Opérationnalité** : Outillage déjà en place (CI, Makefile)

### 6.3 Path d'évolution recommandé

**Phase 1 (Genesis - actuelle)** : Scénario A consolidé
- Remplir zones vides progressivement
- Créer docs/_registry/
- Améliorer liens entre documents
- Ajouter frontmatter YAML

**Phase 2 (Croissance)** : Enrichissement A ou transition vers B
- Si volume docs/ explose : maintenir A avec meilleures outillage
- Si confusion lab/docs persiste : évaluer transition vers B
- Décision basée sur métriques réelles (nb docs, contributions, feedback)

**Phase 3 (Maturité)** : Optimisation continue
- Automatisation poussée (génération, validation, recherche)
- Possibilité d'éléments de C (SSOT thématiques) si équipe grandit
- Jamais D sauf besoin réglementaire spécifique

---

## 7️⃣ RECOMMANDATIONS OPÉRATIONNELLES

### 7.1 Actions prioritaires (Scénario A)

**Court terme (1-3 mois)**
1. Créer `docs/_registry/registry.yaml` (index central)
2. Documenter la philosophie de chaque domaine (00-07) via README.md
3. Remplir docs/00-overview/ (vision.md, principles.md, glossary.md)
4. Créer docs/04-risk/ (threat_model.md, risk_register.md)
5. Ajouter YAML frontmatter aux ADR/RFC/OBS existants

**Moyen terme (3-6 mois)**
1. Développer lab/stacks/ (première stack complète)
2. Enrichir docs/05-governance/ (workflows détaillés)
3. Structurer docs/06-ops/ (runbooks, incidents, migrations)
4. Créer des guides spécialisés dans docs/07-contrib/
5. Automatiser validation des liens (CI)

**Long terme (6-12 mois)**
1. Évaluer pertinence des symlinks (migration progressive ?)
2. Implémenter recherche avancée (par métadonnées)
3. Créer visualisation du graphe documentaire
4. Considérer tooling de génération (squelettes ADR/RFC/OBS)
5. Réévaluer structure si croissance forte (vers B ?)

### 7.2 Métriques de succès

Pour valider que le scénario choisi fonctionne :

**Métriques quantitatives**
- Taux de remplissage docs/ : cible 80% dans 6 mois
- Nombre de liens brisés : cible 0 maintenu en continu
- Temps moyen de navigation (document recherché → trouvé) : < 2 min
- Taux de documents obsolètes non marqués : < 5%

**Métriques qualitatives**
- Feedback contributeurs : structure claire ? (enquête semestrielle)
- Facilité d'onboarding : nouveau contributeur comprend structure < 30 min ?
- Cohérence perçue : ADR/RFC/OBS bien reliés ?

---

## 8️⃣ CONCLUSION

L'exploration des scénarios révèle que **la structure actuelle de Relinium est déjà robuste** et ne nécessite pas de refonte majeure. Les améliorations recommandées sont **incrémentales et pragmatiques** :

1. **Consolider** (remplir les zones vides)
2. **Outiller** (registre, validation, automatisation)
3. **Clarifier** (philosophie de chaque domaine)
4. **Mesurer** (métriques de succès)

Le projet est en excellente position pour **scaler documentairement** sans sacrifier sa lisibilité ni sa maintenabilité.

> _"La meilleure architecture est celle qui grandit avec le projet,_  
> _sans jamais sacrifier la clarté ni l'intention."_

---

**Fin de l'exploration des scénarios**
