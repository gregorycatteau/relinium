# Gouvernance — Phase Genesis

Relinium est actuellement en **phase Genesis**, la phase fondatrice où les bases du projet sont posées avec soin.

## État actuel : Gouvernance Solo

Le projet est maintenu par un seul contributeur principal pendant cette phase initiale. Cette configuration temporaire permet d'établir les fondations solides avant d'ouvrir vers une gouvernance plus collective.

### Rôles cumulés (temporaires)

| Rôle | Détenteur | Responsabilités |
|------|-----------|-----------------|
| **Product Owner** | Greg Catteau | Vision stratégique, valeurs du projet, priorisation des fonctionnalités |
| **Architecte** | Greg Catteau | Structure technique, choix d'architecture, sécurité, cohérence |
| **Mainteneur** | Greg Catteau | Gestion des branches, reviews, merges, releases, CI/CD |
| **Documentaliste** | Greg Catteau | Rédaction et validation des RFC/ADR, cohérence documentaire |
| **Modérateur** | Greg Catteau | Application du Code de conduite, résolution de conflits |

Ces rôles sont **intentionnellement cumulés** pendant la phase Genesis pour :
- Garantir la cohérence de la vision initiale
- Établir les processus et méthodes de travail
- Documenter les décisions fondatrices
- Créer les premiers patterns réutilisables

## Principes de gouvernance

### Transparence radicale

- **Toutes les décisions** sont documentées publiquement (ADR, RFC)
- **Aucune décision en coulisse** : tout passe par le dépôt public
- **Traçabilité complète** : historique Git + documentation
- **Communication ouverte** : issues, discussions, PRs accessibles à tous

### Docs-First

Chaque décision structurante suit ce processus :

1. **Discussion** → Issue ou RFC pour recueillir des avis
2. **Documentation** → Rédaction d'un ADR (Architecture Decision Record)
3. **Validation** → Revue par pairs (quand applicable)
4. **Implémentation** → Code ou mise en œuvre
5. **Vérification** → Tests et validation de la solution

### Sécurité intégrée

- Modèle de menaces avant toute implémentation
- Revue de sécurité systématique
- Commits signés obligatoires pour les mainteneurs
- Audit des dépendances

### Éthique et respect

- Application stricte du Code de conduite
- Pas de discrimination, harcèlement ou attaque personnelle
- Critique constructive des idées, jamais des personnes
- Environnement bienveillant et inclusif

## Process décisionnel actuel

### Décisions techniques (ADR)

Toute décision architecturale ou technique significative :

1. Identification du besoin ou problème
2. Recherche et analyse des options
3. Rédaction d'un ADR documentant :
   - Contexte et problème
   - Options considérées
   - Décision retenue et justification
   - Conséquences et impacts
4. Placement dans `docs/03-architecture/decisions/`
5. Référencement dans les commits et PRs concernés

### Évolutions majeures (RFC)

Pour les changements importants impactant l'architecture ou l'usage :

1. Rédaction d'une RFC (Request for Comments)
2. Publication pour discussion ouverte
3. Période de commentaires (minimum 7 jours)
4. Synthèse des retours
5. Décision finale documentée via ADR
6. Implémentation

### Modifications mineures

Les changements mineurs (typos, clarifications, etc.) peuvent être :
- Proposés via PR directe
- Revus et mergés rapidement
- Sans ADR si non structurants

## Évolution vers une gouvernance collégiale

La gouvernance solo est **temporaire**. L'objectif est d'évoluer vers un modèle plus participatif.

### Critères de transition

Le passage à une gouvernance collégiale interviendra quand :
- ✅ Fondations documentaires complètes (vision, principes, charte)
- ✅ Processus de décision documentés et testés
- ✅ Code de conduite établi et appliqué
- ✅ Premier cycle fonctionnel implémenté
- ✅ Communauté de contributeurs actifs (≥ 3 personnes régulières)
- ✅ Confiance mutuelle établie

### Modèle cible

À terme, le projet visera :

#### Cercles de responsabilité

- **Cercle Vision** : définit les orientations stratégiques
- **Cercle Technique** : décisions d'architecture et stack
- **Cercle Sécurité** : revue et validation sécurité
- **Cercle Communauté** : modération, accueil, communication
- **Cercle Ops** : déploiement, monitoring, incidents

#### Prise de décision

- **Consensus par consentement** : pas d'objection raisonnable = validation
- **Décision par les personnes concernées** : ceux qui font décident
- **Veto explicite avec justification** : pas de blocage sans explication
- **Escalade transparente** : si désaccord, escalade documentée

#### Rôles distribués

- **Mainteneurs** : plusieurs personnes avec droits de merge
- **Reviewers** : contributeurs expérimentés validant les PRs
- **Contributeurs** : toute personne proposant du code/docs
- **Observateurs** : communauté suivant le projet

### Garde-fous

Même en gouvernance distribuée :
- Les valeurs fondatrices restent inchangeables (sauf RFC majeure)
- Le Code de conduite s'applique à tous
- Les décisions structurantes passent par ADR
- La sécurité n'est jamais négociable

## Rôles et permissions actuels

### Sur GitHub

| Niveau | Qui | Permissions |
|--------|-----|-------------|
| Admin | @gregorycatteau | Toutes permissions, settings, protections |
| Maintainer | (à venir) | Merge, releases, labels |
| Contributor | Tous | Fork, PR, issues, discussions |

### Processus d'ajout de mainteneurs

Critères pour devenir mainteneur (phase future) :
1. Contributions régulières et qualitatives (≥ 6 mois)
2. Compréhension profonde de la vision et des valeurs
3. Respect exemplaire du Code de conduite
4. Maîtrise des processus (ADR, RFC, revues)
5. Confiance établie avec l'équipe existante
6. 2FA activée sur GitHub + commits signés

Process :
1. Proposition par un mainteneur existant
2. Validation par consensus des mainteneurs
3. Période de mentorat (3 mois)
4. Accès graduel aux permissions
5. Documentation publique de l'ajout

## Résolution de conflits

### Conflits techniques

1. Discussion via issue ou RFC
2. Présentation des arguments et alternatives
3. Documentation des pour/contre
4. Décision via ADR
5. Engagement de tous à respecter la décision

### Conflits interpersonnels

1. Médiation privée par un modérateur
2. Si échec : escalade vers l'équipe de gouvernance
3. Application du Code de conduite si violation
4. Sanctions graduées si nécessaire
5. Post-mortem anonymisé pour améliorer les processus

### Conflits de vision

1. Retour aux valeurs fondatrices
2. RFC pour discuter l'alignement
3. Vote formel si nécessaire (phase collégiale)
4. Documentation de la décision
5. Fork respectueux si désaccord profond

## Financement et ressources

### Phase actuelle

- **Autofinancement** : le projet est porté bénévolement
- **Pas de sponsors** pour l'instant
- **Infrastructure** : services gratuits ou minimaux

### Phase future

Si le projet nécessite des ressources :
- **Transparence totale** : budgets et dépenses publics
- **Décision collective** : validation de la gouvernance
- **Pas de capture commerciale** : indépendance préservée
- **Licence protectrice** : utilisation libre mais non extractive

## Communication

### Canaux officiels

- **GitHub Issues** : discussions techniques et propositions
- **GitHub Discussions** : échanges communautaires (à activer)
- **Email** : contact [at] relinium.io pour questions privées
- **Documentation** : source de vérité pour toutes les décisions

### Réunions (phase collégiale future)

- Synchrones seulement si nécessaire
- Compte-rendu public systématique
- Décisions validées par écrit (pas de décision orale seule)

## Révision de la gouvernance

Ce document est **vivant** et sera revu :
- Tous les 6 mois minimum
- Lors de changements majeurs dans le projet
- Lors de l'intégration de nouveaux mainteneurs
- Sur proposition motivée de la communauté

Toute modification suit le processus RFC → ADR.

## Questions fréquentes

### Pourquoi une gouvernance solo au départ ?

Pour établir des fondations solides, cohérentes et documentées. Une fois ces bases posées, il sera plus facile d'ouvrir la gouvernance.

### Quand la gouvernance deviendra-t-elle collective ?

Quand les critères de transition seront remplis (voir section "Évolution vers une gouvernance collégiale").

### Comment devenir contributeur ?

Lire `CONTRIBUTING.md` et proposer des PRs ou participer aux discussions.

### Comment devenir mainteneur ?

Contribuer régulièrement, montrer une compréhension profonde du projet, gagner la confiance de l'équipe. Le processus sera formalisé lors de la phase collégiale.

### Et si je ne suis pas d'accord avec une décision ?

Proposer une RFC pour rouvrir la discussion. Les décisions ne sont jamais définitives si de nouveaux arguments solides émergent.

---

**La gouvernance de Relinium évolue avec le projet, toujours au service de ses valeurs fondatrices.**

_Document version 1.0 — Phase Genesis — Dernière mise à jour : 2025-01-03_
