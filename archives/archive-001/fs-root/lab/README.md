# Relinium Experimental Lab

Le dossier `lab/` est l’espace expérimental du projet Relinium. Il héberge les POCs, les scripts utilitaires, les seeds de données et prépare l’exécution de stacks techniques complètes (ex: Django + PostgreSQL + Caddy).

Philosophie
- Humain d’abord, technique comme prolongement. La documentation est la trace de la transformation.
- Docs-first: chaque expérimentation (POC ou stack) est traçable via un triptyque minimal: POC.md, RESULTS.md, SECURITY.md.
- Reproductibilité et sobriété: exécutions locales par défaut, sans cloud ni dépendances implicites.

Objectifs du Lab
- Évaluer des composants isolés (frameworks, bases de données, proxys, observabilité, etc.).
- Préparer des « stacks » cohérentes, combinant plusieurs composants pour refléter un système exploitable.
- Capitaliser sous forme d’OBS/RFC/ADR et converger vers des choix éclairés.

Structure
- lab/pocs/: POCs par composant (hérités de la structure actuelle). Chaque POC suit le triptyque POC.md / RESULTS.md / SECURITY.md.
- lab/stacks/: espace destiné aux POCs « stack » complets (ex: django-postgres-caddy). Vide pour l’instant.
- lab/scripts/: scripts utilitaires du Lab (bench, checks, templates, etc.).
- lab/seeds/: seeds de données (à distinguer des assets « communs » des POCs).
- lab/manifest.yaml: manifeste des composants existants et des stacks prévues (squelette évolutif).
- lab/pocs/README.md: conventions spécifiques à l’organisation par composant et passerelle vers les « stacks ».

Compatibilité et chemins
- Pour éviter toute rupture, des liens de compatibilité peuvent être fournis à la racine (pocs/, scripts/, seeds/) pointant vers lab/.
- La CI existante reste focalisée sur docs/ et les fichiers de gouvernance; aucune dépendance directe à lab/ n’est requise.

Exécuter un POC (local)
- Principe général: chaque POC doit pouvoir être exécuté localement, avec un petit jeu de commandes standard:
  - make dev    POC=pocs/<famille>/<candidat>
  - make test   POC=pocs/<famille>/<candidat>
  - make bench  POC=pocs/<famille>/<candidat>
  - make stop   POC=pocs/<famille>/<candidat>
- Remarque: si des liens de compatibilité sont en place, l’argument POC continue d’utiliser le préfixe pocs/ (ex: POC=pocs/framework/fastapi). Internellement, cela pointe vers lab/pocs/...
- Les scripts utilitaires standards se trouvent sous lab/scripts/ (ou via lien scripts/ si présent).

Conventions POC/stack (docs-first)
- POC.md: objectif, protocole d’essai, prérequis, limites.
- RESULTS.md: résultats bruts et synthèse (p95, RAM/CPU, logs, verdict).
- SECURITY.md: surface d’attaque, posture, menaces et durcissements.

Évolution vers les stacks
- Les POCs par composant apprennent les contraintes unitaires.
- Les « stacks » regroupent des combinaisons testables et prêtes à l’emploi, avec leur propre triptyque.
- Les stacks viseront des scénarios réalistes (build, run, observabilité, sécurité).

Contribution
- Principe: un nouveau POC = un nouveau dossier avec triptyque et instructions reproductibles.
- Ajouter/mettre à jour lab/manifest.yaml lorsque vous introduisez un nouveau composant ou une nouvelle stack planifiée.
- Documenter toute décision structurante via OBS/RFC/ADR.

Références
- docs/03-architecture/observations (OBS)
- docs/03-architecture/rfcs (RFC)
- docs/03-architecture/decisions (ADR)

Note
Ce Lab est un espace mouvant. La clarté, la traçabilité et la compatibilité priment. Les outils (Makefile, scripts, Docker, etc.) viendront après validation des structures et conventions.
