# POCs par composant (héritage) → vers des « stacks » complètes

Ce répertoire conserve l’organisation historique des POCs par **famille de composant** (framework, database, proxy, runtime, storage, observability, container, auth, etc.). Chaque POC suit le triptyque documentaire:
- POC.md — objectif, périmètre, protocole d’essai, prérequis
- RESULTS.md — résultats (p95, RAM/CPU, logs), analyse, verdict (PASS/WARN/KO)
- SECURITY.md — surface d’attaque, posture, menaces, durcissements

Philosophie (docs-first)
- Aucune expérimentation sans documentation.
- Exécution locale reproductible en priorité (sobriété, simplicité).
- Les résultats alimentent les OBS/RFC/ADR sous `docs/03-architecture`.

Frontières et rôles
- pocs/common/ — actifs partagés (ex: générateur de fichiers, échantillons), destinés aux POCs. Pour des jeux de données plus larges/structurés, préférer `lab/seeds/`.
- lab/seeds/ — seeds de données transverses au Lab (ex: corpus, fixtures). Distinct des assets « utilitaires » de `pocs/common`.
- lab/scripts/ — scripts utilitaires transverses au Lab (bench, checks, templates). Les POCs peuvent les invoquer mais doivent rester autonomes.

Compatibilité et chemins
- Pour éviter de casser les usages historiques, des liens de compatibilité peuvent exister à la racine: `pocs/`, `scripts/`, `seeds/` → `lab/...`.
- Le `Makefile` accepte `POC=pocs/<famille>/<candidat>`. Avec compatibilité, ce chemin pointe sur `lab/pocs/...`.

Bonnes pratiques POC
- Un POC = un répertoire dédié: `pocs/<famille>/<candidat>/`
- Préciser clairement:
  - Objectif, critères de succès, périmètre
  - Étapes d’exécution locale (dev/test/bench/stop)
  - Hypothèses/limites et risques
- Standardiser les mesures: latence (p95), RAM/CPU, taille des assets, logs

Cap vers les « stacks »
- Les POCs par composant éclairent les contraintes unitaires.
- Les **stacks** (dans `lab/stacks/`) assembleront plusieurs composants (ex: Django + PostgreSQL + Caddy) avec le même triptyque documentaire.
- Chaque stack visera un scénario réaliste (build, run, observabilité, sécurité) avec scripts dédiés si nécessaire.

Contribution
- Ajouter un nouveau POC = créer un dossier avec le triptyque et des instructions reproductibles.
- Mettre à jour `lab/manifest.yaml` pour inventorier le nouveau composant.
- Reporter les observations significatives dans `docs/03-architecture` (OBS/RFC/ADR).
