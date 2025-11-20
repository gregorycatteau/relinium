---
id: "OBS-0004"
type: "OBS"
status: "Ouvert"
date: "2025-11-12"
author: "Agent Codex"
version: "1.0.0"
tags: ["candidats", "revue", "backend"]
links:
  cites: ["SPRINT-0001", "OBS-0001", "RFC-0002"]
self_hash: sha256:ba379b2c47f0b1719a5a50f57f1fa3a522fe9a8bda19c7db60144e7832bcf9c1
---

# OBS-0004 — Revue communautaire des candidats backend

## Intention
Présenter aux responsables POC la sélection de candidats par famille définie dans `SPRINT-0001` (issue d'`OBS-0001`) afin d'obtenir une validation collective avant de lancer les POC ciblés et la phase de scoring documentée dans `OBS-0002`. Cette observation prépare la bascule vers l'exécution en s'assurant que chaque famille dispose d'un consensus minimal.

## Synthèse des sélections à valider
- **Runtime / langage** : Python, Go, Rust, Node.js (TypeScript)
  - *Justification* : combiner productivité (Python, Node.js) et performance/mémoire sûre (Go, Rust) avec une forte disponibilité de bibliothèques et de retours d'expérience.
  - *Action* : responsables runtime à confirmer la présence d'au moins un langage interprété et un langage compilé.
- **Framework web** : Django, FastAPI, Gin, Actix Web
  - *Justification* : couverture Python (full-stack + API rapide) et options Go/Rust pour explorer sobriété/performance ; documentation et communautés actives.
  - *Action* : pilotes API/backend à valider la répartition Python/Go/Rust et signaler des manques éventuels.
- **Persistance (SGBD)** : PostgreSQL, MariaDB/MySQL, MongoDB, SQLite
  - *Justification* : combinaison SQL avancé, SQL classique, NoSQL document et embarqué léger pour POC rapides ; maturité éprouvée.
  - *Action* : responsables data/storage à confirmer la nécessité des quatre modes ou à proposer des alternatives (ex. Timeseries) si critiques.
- **Cache / Queue / Pub-Sub** : Redis, RabbitMQ, NATS, Kafka
  - *Justification* : spectre du cache simple aux bus distribués, couvrant AMQP, Pub/Sub léger et streaming massif ; documentation abondante.
  - *Action* : équipe intégration à préciser priorités (latence vs. throughput) avant POC.
- **Reverse proxy / Gateway** : Caddy, Nginx, Traefik, Envoy
  - *Justification* : combiner simplicité auto-TLS, standard historique, intégration cloud-native et proxy L7 avancé ; tous largement supportés.
  - *Action* : responsables réseau/sécurité à confirmer le besoin d'un proxy dynamique vs. statique.
- **Authentification / Autorisation** : Auth interne, Keycloak, Authelia
  - *Justification* : conserver une option maison pour sobriété et deux solutions OSS reconnues pour l'OIDC/SSO ; communautés actives.
  - *Action* : équipe identité à valider la couverture des scénarios (MFA, délégation, intégration proxy).
- **Stockage de fichiers** : FS local, MinIO
  - *Justification* : juxtaposer la simplicité pour POC et une cible S3-compatible auto-hébergée.
  - *Action* : responsables stockage à confirmer si un troisième candidat (ex. Backblaze/S3 managé) doit être ajouté.
- **Observabilité** : Logs JSON natifs, Prometheus + Grafana, OpenTelemetry
  - *Justification* : progression naturelle du logging minimal aux métriques standardisées et traces interopérables.
  - *Action* : équipe observabilité à aligner l'effort initial (stack minimale vs. instrumentation complète).
- **Conteneurisation / Orchestration** : Docker/Compose, Podman, Kubernetes
  - *Justification* : couvrir l'outillage local standard, l'alternative rootless et la cible orchestrée pour environnements distribués.
  - *Action* : responsables plateforme à confirmer les environnements de test nécessaires.

Chaque famille est invitée à commenter directement en référence à `RFC-0002` pour assurer la traçabilité des décisions.

## Actions attendues
1. Discuter cette revue dans le cadre de `RFC-0002` afin de formaliser l'accord ou les ajustements.
2. Documenter toute modification proposée (ajout/retrait de candidats) et déclencher, si nécessaire, une mise à jour de `SPRINT-0001` et de la présente observation.
3. Confirmer la liste finale avant d'ouvrir les POC et la phase de scoring/`OBS-0002`.
