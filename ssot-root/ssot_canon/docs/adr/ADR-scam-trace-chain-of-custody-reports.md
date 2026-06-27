# ADR - Scam Trace, custody et rapports Anti-Scam

Statut: accepte pour MVP

## Contexte

Relinium doit fournir une filiere operationnelle anti-scam utilisable depuis le cockpit humain, sans confondre gouvernance SSOT, stockage operationnel, preuve originale et rapports derives.

## Decision

La filiere technique s'appelle `scam_trace` et le nom humain est Relinium Anti-Scam.

PostgreSQL est la boite noire operationnelle des dossiers anti-scam. Il stocke les dossiers, metadonnees d'artefacts, hashes, reponses, indicateurs, timelines, evenements de custody, rapports Markdown et correlations.

Le SSOT reste la gouvernance de la filiere. Les RFC, ADR et process definissent le perimetre, les limites defensives, les obligations de minimisation et les invariants de transmission humaine.

GraphQL est l'interface metier principale pour le front Anti-Scam. REST existant est preserve pour le cockpit SSOT.

Nuxt est le cockpit operateur. Il expose un parcours guide: dossier, preuve, questionnaire, timeline, indicateurs, rapports et correlations.

Go est reserve aux outils rapides et defensifs de hash, scellement et observation. La logique metier principale reste dans Django pour conserver les controles, mutations, validations et modeles au meme endroit.

## Justification

PostgreSQL convient a l'etat operationnel, aux relations entre dossiers et aux migrations. Il evite tout fallback SQLite et garde une piste auditables des mutations metier.

Le SSOT ne doit pas devenir une base de dossiers victimes. Il encadre la filiere, mais les cas vivants appartiennent a PostgreSQL.

GraphQL permet au front de lire exactement les vues metier necessaires sans exposer les zones sensibles du depot.

Nuxt permet une interface francophone utilisable par un operateur, avec explications et statuts.

Go est utile pour produire une empreinte locale verifiable d'un artefact sans upload, sans modification du fichier et sans logique d'orchestration metier.

## Contraintes de securite

- aucune action automatique dangereuse;
- aucun clic automatique sur lien suspect;
- aucun telechargement distant pendant l'analyse MVP;
- aucun rapport soumis automatiquement;
- validation humaine obligatoire avant transmission;
- minimisation des champs potentiellement sensibles;
- pas de secrets en clair;
- pas d'exposition de `personal_vault`, `vault_index` ou `users/user_template`;
- pas de modification de `ssot-root/event_kernel` ni des streams append-only.

## Consequences

Les rapports sont prepares en Markdown et restent au statut brouillon tant qu'un humain ne les marque pas relus. Les correlations restent indicatives. Les artefacts lourds restent references ou hashes, pas copies en base par defaut.
