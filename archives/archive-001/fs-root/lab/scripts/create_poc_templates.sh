#!/usr/bin/env bash
# Script pour créer les templates POC.md, RESULTS.md, SECURITY.md dans tous les dossiers POC

set -euo pipefail

POC_TEMPLATE='# POC – [À REMPLACER : nom du candidat]

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
- `make test`  : lancer les tests unitaires / d'"'"'intégration
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
'

RESULTS_TEMPLATE='# RESULTS – [À REMPLACER : nom du candidat]

## 1. Résumé
- Verdict global (subjectif) : [OK / mitigé / KO]
- Points forts :
- Points faibles :

## 2. Mesures de performance (VPS 2vCPU/4GB si possible)
### Bench lecture – GET /documents?page=1&size=20
- Commande : `hey -n 1000 -c 20 http://localhost:PORT/documents?page=1&size=20`
- p50 :
- p95 :
- req/s :
- Erreurs (4xx/5xx) :

### Bench upload – POST /uploads (fichier 20–50 Mo)
- Durée moyenne :
- Erreurs :
- Observations :

### Ressources
- RAM idle (MiB) :
- RAM peak (MiB) :
- CPU moyen (% estimé) :
- Temps de cold start (s) :

## 3. DX / Ergonomie
- Temps d'"'"'installation (lecture POC + setup) :
- Clarté des erreurs :
- Lisibilité du code :

## 4. Correspondance avec SLOs (OBS-0003)
- Latence p95 OK ? [Oui/Non]
- RAM idle dans les seuils ? [Oui/Non]
- Souveraineté (offline) respectée ? [Oui/Non]
- Coût estimé (VPS) :

## 5. Notes pour la matrice RFC-002
- Performance & sobriété (0–5) :
- Sécurité / durcissement (0–5) :
- Souveraineté / local-first (0–5) :
- Maintenabilité / DX / etc. (0–5) :
- Commentaires :
'

SECURITY_TEMPLATE='# SECURITY – [À REMPLACER : nom du candidat]

## 1. Validation & sanitization
- Bibliothèques / mécanismes utilisés :
- Endpoints couverts :
- Comportement sur JSON malformé / types erronés :

## 2. Contrôles de sécurité
### Rate limiting
- Présent sur /auth/login ? [Oui/Non]
- Paramètres (req/min/IP) :
- Implémentation :

### AuthN / AuthZ
- Mode auth : [sessions / JWT / OIDC / autre]
- Rôles implémentés : [viewer/editor/admin]
- Vérification accès document "private" par viewer → 403 ? [Oui/Non]

### Uploads
- Limite de taille :
- Contrôle du type de fichier ? :
- Gestion des erreurs (fichier trop gros) :

## 3. Headers de sécurité
- X-Content-Type-Options :
- Referrer-Policy :
- X-Frame-Options ou CSP frame-ancestors :
- Content-Security-Policy (si applicable) :

## 4. Logs & observabilité
- Format logs : [texte / JSON]
- Infos loggées : [correlation-id, user-id, endpoint, status, latence]
- Erreurs critiques loggées ? :
- Journaux d'"'"'accès disponibles ? :

## 5. Tests "hacker mindset"
- Bruteforce doux /auth/login (20 tentatives) : résultat :
- Injection JSON malformé : résultat :
- Accès document private en viewer : résultat :
- Upload overflow (> max autorisé) : résultat :

## 6. Dépendances & vulnérabilités
- Outils de scan (pip-audit / npm audit / cargo audit / govulncheck / autre) :
- Vulnérabilités critiques détectées ? :
- Actions de mitigation :

## 7. Conclusion sécurité
- Niveau global : [OK / A renforcer / KO]
- Points critiques :
- Recommandations :
'

# Créer les templates dans tous les dossiers POC
for d in \
  pocs/runtime/python \
  pocs/runtime/go \
  pocs/runtime/rust \
  pocs/framework/django \
  pocs/framework/fastapi \
  pocs/framework/gin \
  pocs/framework/axum \
  pocs/database/postgresql \
  pocs/database/mariadb \
  pocs/database/sqlite \
  pocs/database/mongodb \
  pocs/proxy/caddy \
  pocs/proxy/nginx \
  pocs/proxy/traefik \
  pocs/auth/internal \
  pocs/auth/keycloak \
  pocs/auth/authelia \
  pocs/storage/fs-local \
  pocs/storage/minio \
  pocs/observability/logs-basic \
  pocs/observability/prometheus-grafana \
  pocs/container/docker-compose \
  pocs/container/podman
do
  echo "$POC_TEMPLATE" > "$d/POC.md"
  echo "$RESULTS_TEMPLATE" > "$d/RESULTS.md"
  echo "$SECURITY_TEMPLATE" > "$d/SECURITY.md"
done

echo "✅ Templates créés dans tous les dossiers POC"
