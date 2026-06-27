# RFC - Cartographie documentaire v0.1

## Statut

Proposition.

## Objectif

La cartographie documentaire permet de photographier rapidement l'etat observable
d'une arborescence documentaire sans importer les fichiers dans Relinium. Le but
est de prouver ce qui etait present, a quel emplacement, a quel instant, avec
quelles metadonnees observables et, si possible, avec quelle empreinte de
contenu.

Le cas prioritaire est l'observation defensive en contexte d'audit, de fraude ou
de preservation d'etat avant modification hostile. Le premier niveau de preuve
doit donc privilegier la vitesse: prouver immediatement la presence et
l'emplacement, puis renforcer progressivement la preuve du contenu.

## Non-objectifs

- Importer ou copier les fichiers scannes.
- Modifier les fichiers scannes.
- Suivre les symlinks par defaut.
- Attribuer magiquement une action a un utilisateur sans source d'audit robuste.
- Remplacer le SSOT fichier comme couche de gouvernance.

## Vocabulaire

- Snapshot documentaire: capture datee d'une arborescence.
- Observation fichier: enregistrement d'un objet observe sur le filesystem.
- Observation chemin: preuve qu'un chemin relatif etait observable ou a produit
  une erreur.
- Empreinte contenu: hash complet du contenu, calcule en streaming.
- Empreinte emplacement: hash d'un chemin relatif normalise et d'une racine
  logique.
- Empreinte metadonnees: hash d'un JSON canonique de metadonnees autorisees.
- Preuve de presence: preuve qu'un chemin existait pendant le scan.
- Preuve de non-modification: preuve forte seulement avec hash complet.
- Preuve de deplacement: correlation entre identite filesystem, fingerprint et
  changement de chemin.
- Preuve de suppression: absence constatee lors d'une reconciliation apres une
  presence anterieure.
- Snapshot scelle: snapshot finalise avec hash global reproductible.

## Niveaux de preuve

### PRESENCE

Mode ultra rapide. Il ne lit pas le contenu des fichiers.

Donnees observees:

- chemin relatif a la racine scannee;
- type: fichier, dossier, symlink, autre;
- taille;
- mtime UTC;
- permissions;
- identifiants device/inode si disponibles;
- erreur d'acces si presente;
- metadata_hash;
- location_hash;
- observation_hash.

Ce mode prouve la presence et l'emplacement observables. Il ne prouve pas le
contenu.

### FINGERPRINT

Mode rapide qui lit seulement des blocs controles:

- premiers N octets;
- derniers N octets;
- taille;
- metadata_hash;
- location_hash;
- fingerprint_hash.

Ce mode renforce la preuve de contenu sans lire tout le fichier. Ce n'est pas
une preuve cryptographique complete du contenu.

### CONTENT futur

Mode de hash SHA-256 complet du contenu, en streaming, en arriere-plan ou basse
priorite. Le fichier n'est jamais importe dans Relinium.

### SEALED SNAPSHOT

Chaque scan produit un evenement de scellement:

- snapshot_id;
- started_at UTC;
- finished_at UTC;
- duration_ms monotone;
- scanner_version;
- observation_count;
- error_count;
- snapshot_hash stable fonde sur les observation_hash tries.

Une signature locale et un horodatage externe pourront etre ajoutes plus tard.

## Format NDJSON

Le prototype v0.1 produit un flux NDJSON avec quatre types d'evenements:

- snapshot_started;
- observation;
- scan_error;
- snapshot_sealed.

Le NDJSON peut etre scelle immediatement et ingere plus tard par Django dans
PostgreSQL. Il ne contient pas de chemin absolu ni de contenu brut.

## Securite

- Le scanner est read-only.
- Les chemins sont relatifs et normalises.
- Les symlinks ne sont pas suivis par defaut.
- Les erreurs sont enregistrees sans interrompre tout le scan.
- Aucun contenu brut n'est ecrit.
- Les noms de fichiers peuvent etre redacted dans un mode dedie.
- L'utilisation doit rester limitee aux systemes autorises.

## Limites techniques

- Un fichier peut changer pendant le scan.
- Un fichier peut disparaitre entre l'enumeration et l'observation.
- Les permissions peuvent bloquer l'observation ou le fingerprint.
- Les timestamps filesystem peuvent etre manipules.
- L'horloge systeme peut etre contestee.
- Les watchers filesystem futurs peuvent perdre des evenements.

Relinium doit rendre ces limites visibles dans les observations et les rapports.

## Integration future

PostgreSQL devient la boite noire operationnelle: snapshots, observations,
fingerprints, erreurs, jobs, seals, evenements de mouvement et etats de workflow.
Le SSOT fichier reste la couche de gouvernance: regles, contrats, schemas,
politiques, invariants et evenements canoniques append-only.

Django ingere les NDJSON scelles, applique les regles SSOT avant les ecritures
en base, expose GraphQL, puis le cockpit affiche les snapshots et leurs niveaux
de preuve.
