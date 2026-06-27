# RFC Draft - Detecteur de mouvement documentaire v0.1

## Statut

Draft prospectif. Non implemente.

## Objectif

Le detecteur de mouvement documentaire vise a repondre a la question:

> Qui a fait quoi, sur quel document, depuis quelle session ou source technique,
> et avec quel niveau de confiance ?

Il observe creations, modifications, deplacements et suppressions, puis correle
les evenements filesystem avec des sources d'audit externes lorsque celles-ci
sont disponibles et autorisees.

## Pourquoi un watcher seul ne suffit pas

Un watcher filesystem peut indiquer qu'un chemin a change, mais il ne donne pas
toujours l'acteur. Il peut aussi perdre des evenements, subir des overflows ou
voir seulement une partie de la chronologie. Il doit donc etre complete par une
reconciliation periodique et par des sources d'audit.

## Sources possibles

- Linux: auditd, fanotify, eBPF futur.
- Windows: Security logs, USN Journal, Sysmon futur.
- NAS: logs SMB/NFS selon constructeur.
- Active Directory: authentification, sessions et comptes.
- SharePoint/Microsoft 365.
- Google Drive/Workspace.
- Nextcloud.
- GED metier.

## Modele d'attribution

Champs conceptuels:

- actor_id;
- account_id;
- session_id;
- source_ip;
- device_ref;
- event_time;
- source_system;
- confidence_score;
- evidence_refs.

Niveaux de confiance:

- certain: log GED signe ou audit OS robuste;
- strong: session + IP + action correlees;
- medium: evenement fichier + session probable;
- weak: changement detecte sans acteur fiable.

## Limites

- NAT/VPN;
- comptes partages;
- logs desactives;
- horloges divergentes;
- erreurs de correlation;
- attribution probabiliste;
- politiques de retention differentes selon les systemes.

## Exigences securite

- Connecteurs read-only.
- Autorisation explicite sur les systemes observes.
- Pas de collecte de contenu brut.
- Minimisation des donnees.
- Redaction des identifiants sensibles si necessaire.
- Preuve horodatee des observations et de leur source.
- Journalisation des limites et trous de collecte.

## Relation avec la cartographie documentaire

La cartographie produit l'etat initial scelle. Le detecteur observe ensuite les
transitions. Une reconciliation periodique compare les evenements detectes avec
un nouveau snapshot pour identifier les pertes de watcher ou les derives.
