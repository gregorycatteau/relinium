---
id: "SPRINT-0001"
type: "SPRINT"
status: "En cours"
date: "2025-11-13"
author: "Agent Codex"
version: "1.2.0"
tags: ["sprint", "inventaire", "stack", "phase1"]
links:
  cites: ["OBS-0001", "RFC-0002"]
self_hash: sha256:a7a5cbc9a2baae0d4a7040915ebde91592fe9d512e0c1d176a3e0371264299dd
---

# SPRINT-0001 — Inventaire détaillé des candidats

## Objectif
Utiliser le référentiel OBS-0001 pour confirmer les candidats existants (runtimes, frameworks, SGBD, proxys, authentification, stockage, observabilité, conteneurisation) et sélectionner 3 à 4 candidats par famille en vue des futures phases de POC, sans trancher sur les décisions techniques.

## Tâches à mener
- Lire `docs/03-architecture/observations/OBS-0001-backend-composants-inventaire-v2.md` et en extraire la liste exhaustive des technologies candidates.
- Choisir 3 à 4 technologies par famille pour les prochaines expérimentations et POC ciblés.
- Consulter la documentation officielle de chaque candidat pour consigner installation, licence, maturité communautaire et toute spécificité notable.
- Compiler les liens et ressources utiles afin d'alimenter les prochaines phases d'évaluation.

## Compléments et références
*(À compléter pendant le sprint pour agréger liens additionnels, prises de notes ou ressources externes.)*

## Candidats sélectionnés
- **Runtime / langage** : Python, Go, Rust, Node.js (TypeScript)
- **Framework web** : Django, FastAPI, Gin, Actix Web
- **Persistance (SGBD)** : PostgreSQL, MariaDB/MySQL, MongoDB, SQLite
- **Cache / Queue / Pub-Sub** : Redis, RabbitMQ, NATS, Kafka
- **Reverse proxy / Gateway** : Caddy, Nginx, Traefik, Envoy
- **Authentification / Autorisation** : Auth interne, Keycloak, Authelia
- **Stockage de fichiers** : FS local, MinIO
- **Observabilité** : Logs JSON natifs, Prometheus + Grafana, OpenTelemetry
- **Conteneurisation / Orchestration** : Docker/Compose, Podman, Kubernetes

Les sélections s'appuient sur `OBS-0001`, `RFC-0002` et les documentations officielles associées (python.org, go.dev, rust-lang.org, nodejs.org, djangoproject.com, fastapi.tiangolo.com, gin-gonic.com, actix.rs, postgresql.org, mariadb.org, mongodb.com, sqlite.org, redis.io, rabbitmq.com, nats.io, kafka.apache.org, caddyserver.com, nginx.org, traefik.io, envoyproxy.io, keycloak.org, authelia.com, min.io, prometheus.io, grafana.com, opentelemetry.io, docker.com, podman.io, kubernetes.io).

## Journal de version 1.2.0
- Alignement du périmètre de sélection avec la routine documentaire automatisée (`make new-doc`) afin de garantir la traçabilité des futures itérations.
