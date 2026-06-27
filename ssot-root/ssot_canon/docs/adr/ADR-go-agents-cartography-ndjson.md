# ADR - Agents Go, cartographie documentaire et NDJSON scelle

## Statut

Accepte pour prototype v0.1.

## Decision

Relinium utilisera une arborescence Go multi-binaires sous `apps/go/`.

Le premier binaire est `relinium-cartography-scan`, dedie a la cartographie
documentaire. Le detecteur de mouvement documentaire sera un binaire separe dans
un palier ulterieur.

Le prototype produit d'abord un NDJSON scelle. L'ecriture PostgreSQL directe est
repoussee a une option future.

## Pourquoi Go

Go est adapte aux outils systeme defensifs:

- binaire autonome;
- concurrence simple et controlable;
- lecture filesystem efficace;
- hash en streaming;
- deploiement plus simple que Python sur postes heterogenes;
- standard library suffisante pour un prototype auditable.

## Pourquoi `apps/go/`

Relinium aura probablement plusieurs binaires:

- cartographie documentaire;
- detecteur de mouvement documentaire;
- connecteurs d'audit futurs;
- outils d'ingestion ou de verification.

Une seule racine Go permet de partager les paquets internes:

- `internal/evidence`;
- `internal/hashing`;
- `internal/ndjson`;
- `internal/seal`;
- `internal/fsutil`;
- `internal/cartography`;
- plus tard `internal/motion` et `internal/connectors`.

## Pourquoi NDJSON scelle avant PostgreSQL direct

En contexte anti-fraude, la premiere exigence est de capturer vite et de sceller
localement. Une dependance immediate a PostgreSQL peut ralentir ou bloquer la
preuve si le reseau, les credentials ou la base ne sont pas disponibles.

Le NDJSON scelle:

- est append-friendly;
- peut etre conserve comme artefact probatoire;
- peut etre ingere plus tard;
- evite de perdre l'observation si PostgreSQL est indisponible;
- garde le scanner simple et defensif.

PostgreSQL reste la boite noire operationnelle future pour les observations,
snapshots, jobs, seals et workflows.

## Pourquoi repousser le watcher

Un watcher filesystem ne suffit pas a prouver un etat initial. Il peut perdre
des evenements, subir des overflows, manquer des informations d'acteur et ne pas
voir l'historique anterieur. Le palier v0.1 doit d'abord produire un snapshot
initial fiable et scelle. La surveillance quasi temps reel viendra ensuite avec
reconciliation periodique obligatoire.

## Pourquoi un detecteur de mouvement separe

La cartographie photographie un etat. Le detecteur de mouvement observe des
transitions et tente de les attribuer. Ce sont deux responsabilites distinctes:

- la cartographie privilegie la preuve de presence;
- le mouvement privilegie la chronologie, la correlation et l'attribution.

Les separer garde les binaires auditables et limite les privileges necessaires.

## Attribution utilisateur/IP

Un watcher filesystem seul ne permet pas une attribution fiable. L'attribution
necessite des connecteurs read-only vers des sources d'audit:

- logs OS;
- logs NAS/SMB/AD;
- journaux cloud ou GED;
- sessions, IP, comptes et horloges correlees.

Relinium devra exposer un niveau de confiance:

- certain: log GED signe ou audit OS robuste;
- strong: session + IP + action correlees;
- medium: evenement fichier + session probable;
- weak: changement detecte sans acteur fiable.

## Prospective - Detecteur de mouvement documentaire v0.2

Le detecteur v0.2 pourra combiner:

- filesystem watcher;
- audit OS;
- logs NAS/SMB/Active Directory;
- connecteurs SharePoint/Microsoft 365;
- connecteurs Google Drive/Workspace;
- Nextcloud;
- GED metier;
- correlation actor_id, account_id, session_id, source_ip;
- confidence_score d'attribution.

Limites a traiter:

- NAT/VPN;
- comptes partages;
- logs desactives;
- horloges divergentes;
- attribution probabiliste;
- exigences legales/RGPD;
- autorisation explicite avant collecte.

Tous les connecteurs devront etre read-only, minimiser les donnees collectees et
ne jamais collecter le contenu brut des fichiers.
