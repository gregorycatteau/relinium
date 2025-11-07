# LAB_REFACTOR_NOTES — Refactor du Relinium Experimental Lab

Date: 2025-11-04  
Auteur: Cline (assistance)  
Philosophie: « L’humain d’abord, la technique comme prolongement. La documentation comme trace de la transformation. »

## 1) Contexte et objectifs

- Problème initial:
  - Zone expérimentale éparpillée (pocs/, scripts/, seeds/ à la racine).
  - Organisation par composant alors que l’évaluation OBS/RFC/ADR vise des stacks complètes.
  - Manque de manifeste global et de README explicatifs côté Lab.

- Objectifs de ce refactor (sans modifier le contenu des fichiers):
  - Créer un espace **lab/** dédié et cohérent pour l’expérimental.
  - Introduire **lab/stacks/** (préparé, vide) pour accueillir les combinaisons complètes.
  - Clarifier les rôles entre `pocs/common`, `lab/seeds` et `lab/scripts`.
  - Préserver la compatibilité des chemins historiques (`pocs/`, `scripts/`, `seeds/`) via des symlinks.
  - Ne pas impacter la CI (docs-first) ni `.github/`.

## 2) Actions réalisées

- Création d’un espace de documentation et de gouvernance du Lab:
  - `lab/README.md` (philosophie, structure, exécution d’un POC).
  - `lab/pocs/README.md` (héritage « par composant » et passerelle vers « stacks »).
  - `lab/manifest.yaml` (squelette déclaratif: inventaire des composants + stacks planifiées).

- Réorganisation des répertoires (contenus non modifiés):
  - `git mv pocs -> lab/pocs`
  - `git mv scripts -> lab/scripts`
  - `git mv seeds -> lab/seeds` (si présent; cible créée si le répertoire était vide ou non suivi)
  - Création de `lab/stacks/` (vide).

- Compatibilité ascendante (chemins historiques):
  - Création de liens symboliques à la racine:
    - `pocs -> lab/pocs`
    - `scripts -> lab/scripts`
    - `seeds -> lab/seeds`
  - But: éviter toute casse sur les chemins existants (Makefile, docs, habitudes).

- Préservation d’historique:
  - Déplacements effectués via `git mv` pour conserver l’historique Git des fichiers suivis.

## 3) Structure post-refactor (extrait)

- Racine (inchangés): `docs/`, `.github/`, `README.md`, `Makefile`, etc.
- Nouveaux/actualisés:
  - `lab/`
    - `README.md` (nouveau)
    - `manifest.yaml` (nouveau)
    - `pocs/` (ex-`pocs/`)
      - `README.md` (nouveau)
      - familles existantes (framework, database, proxy, etc.)
    - `scripts/` (ex-`scripts/`)
    - `seeds/` (ex-`seeds/` si présent)
    - `stacks/` (vide)

- Compatibilité (symlinks à la racine):
  - `pocs -> lab/pocs`
  - `scripts -> lab/scripts`
  - `seeds -> lab/seeds`

Note: les symlinks permettent de continuer à utiliser des chemins tels que:
- `POC=pocs/framework/fastapi` dans le Makefile
- `./scripts/bench_light.sh` référencé dans certains docs

## 4) Vérification CI et chemins

- CI (`.github/workflows/ci-docs.yml`) vérifie la présence de fichiers à la racine (README.md, SECURITY.md, etc.) et la structure de `docs/`.  
  => Aucun job ne dépend de `pocs/`, `scripts/`, `seeds/`.  
  => Le déplacement vers `lab/` est donc **sans impact** pour la CI.

- Références documentaires:
  - `docs/03-architecture/observations/OBS-0003-calibration-et-SLOs.md` mentionne `./scripts/bench_light.sh`.  
    Grâce au symlink `scripts -> lab/scripts`, le chemin **reste fonctionnel**.
  - Le `Makefile` guide vers `POC=pocs/...` (ex: `pocs/framework/fastapi`).  
    Grâce au symlink `pocs -> lab/pocs`, ce flux **reste fonctionnel**.

## 5) Commandes/approche utilisée (résumé)

Déplacements et compatibilité (exécuté dans un shell, version adaptée pour Git + symlinks):
```
# Préparer les stacks
mkdir -p lab/stacks

# Déplacements (préservent l’historique Git)
git mv pocs lab/
git mv scripts lab/
git mv seeds lab/  # si suivi; sinon mkdir -p lab/seeds ; rmdir seeds (si vide)

# Symlinks de compatibilité à la racine
[ -e "pocs" ] || ln -s lab/pocs pocs
[ -e "scripts" ] || ln -s lab/scripts scripts
[ -e "seeds" ] || ln -s lab/seeds seeds
```

Important: l’erreur zsh « parse error near `)' » rencontrée initialement provenait d’un collage multi-lignes mal interprété par le shell. Les étapes ont été rejouées avec un script bash correctement échappé.

## 6) Décisions documentées

- Choix d’un dossier **lab/** unique pour l’expérimental afin de:
  - concentrer POCs, seeds et scripts,
  - préparer l’arrivée de **stacks** complètes,
  - clarifier la frontière entre « code du dépôt » (docs, gouvernance) et « laboratoire ».
- Conservation stricte des contenus (aucune édition de POC/RESULTS/SECURITY).
- **Symlinks** pour compatibilité immédiate des chemins historiques.
- Aucune modification de `.github/` ni de `docs/`.

## 7) Recommandations et prochaines étapes

- Stacks:
  - Totems à créer en premier:  
    - `lab/stacks/django-postgresql-caddy/`  
    - `lab/stacks/fastapi-postgresql-traefik/`  
    - `lab/stacks/axum-postgresql-nginx/`  
  - Pour chaque stack: répliquer le triptyque (POC.md/RESULTS.md/SECURITY.md), préciser protocole, scripts dédiés (ultérieurement).

- Seeds vs pocs/common:
  - Clarifier la frontière:
    - `pocs/common/` = utilitaires et échantillons légers pour POCs unitaires,
    - `lab/seeds/` = corpus/fixtures transverses et/ou plus volumineux.
  - Si besoin, migrer des jeux de données de `pocs/common` vers `lab/seeds`.

- Scripts:
  - Laisser en l’état sous `lab/scripts/` pour compat.
  - À terme, documenter des conventions d’appel (`make bench`, `make test`, etc.).
  - Option d’amélioration: outillage génératif basé sur `lab/manifest.yaml` (création de squelettes POC/stack).

- Compatibilité et dette:
  - Conserver les symlinks tant que le parc documentaire et les habitudes dépendent des chemins historiques.  
  - Si un jour on souhaite supprimer les symlinks:  
    - mettre à jour le `Makefile` (et docs) pour pointer vers `lab/pocs/...`,  
    - communiquer un guide de migration aux contributeurs.

- Plateformes:
  - Reminder: sur Windows, Git peut nécessiter `core.symlinks=true` pour que les symlinks soient bien gérés. Documenter ce point pour les contributeurs Windows.

## 8) Validation finale

- Fichiers existants: **non modifiés**, uniquement déplacés (historique Git préservé).
- CI: **préservée** (verrou sur docs/ et fichiers racine uniquement).
- Chemins historiques: **préservés** via symlinks `pocs/`, `scripts/`, `seeds/`.
- Lab: **structuré et prêt** pour accueillir les premières stacks.

Fin de note — ce fichier peut être supprimé après stabilisation (ou archivé sous `docs/06-ops/` comme journal de migration).
