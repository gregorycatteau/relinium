# POC – [À REMPLACER : nom du candidat]

## 1. Contexte
- Famille : [runtime|framework|database|proxy|auth|storage|observability|container]
- Candidat : [nom]
- Version(s) testée(s) :
- Date :
- Auteur :

## 2. Objectifs du POC
- Implémenter : endpoints, persistance, auth, upload, tasks async selon OBS-0002.
- Vérifier : SLOs & kill-switch OBS-0003.

## 3. Environnement de test
- Machine / VPS :
- OS :
- CPU / RAM :
- Version du langage / runtime :
- Version du framework / DB / proxy :

## 4. Installation & commandes
### Pré-requis
- [outils nécessaires]

### Commandes
- `make dev`   : lancer le service en dev
- `make test`  : lancer les tests unitaires / d'intégration
- `make bench` : lancer le bench léger
- `make stop`  : arrêter / nettoyer

## 5. Endpoints implémentés (si applicable)
- POST /auth/login
- POST /documents
- GET  /documents
- GET  /documents/:id
- PUT  /documents/:id
- POST /uploads
- POST /documents/:id/summarize
- GET  /tasks/:task_id

## 6. Limitations connues
- [TODO]

## 7. TODO / pistes
- [TODO]

