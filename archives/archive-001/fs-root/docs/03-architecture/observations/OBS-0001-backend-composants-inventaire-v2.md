---
id: "OBS-0001-v2"
id_root: "OBS-0001"
type: "OBS"
title: "Inventaire initial des backends et composants (succession v2)"
status: "Ouvert"
date: "2025-11-05"
author: "Greg Catteau"
version: "2.0"
previous_hash: "sha256:069b167f03f0781c94c4f763f906e65df0ece237a101ea04bf0217b526ce1c2a"
scope: "technical"
pattern: "observation"
tags: ["backend", "composants", "inventaire", "exploration", "ssot-v1.1"]
links:
  supersedes: "OBS-0001"
  cites: ["RFC-0002"]
  cited_by: ["OBS-0002"]
self_hash: sha256:cad9481068a47b94ea073b93252fec999ba43fe346a9242ac5631d6bc6521dad
---

# OBS-0001 — Inventaire initial des backends et composants

---

## 1️⃣ Objectif

Recenser, sans hiérarchie ni préférence, l'ensemble des **composants potentiels** qui pourraient constituer la future stack backend de Relinium.

Cette observation constitue la **matière brute** avant toute phase de comparaison ou de scoring.  
Elle permet de comprendre *ce qui existe* dans notre matière numérique avant de "purifier" (analyser) puis "structurer" (sélectionner).

---

## 2️⃣ Méthodologie d'observation

Chaque composant est décrit à partir de **sources publiques et tests rapides** (documentation officielle, benchmarks publiés, expériences internes).

Pour chaque famille, on note :
- 🧩 **Nom & écosystème**
- ⚙️ **Nature / rôle**
- 🔍 **Forces observées**
- ⚠️ **Faiblesses observées**
- 🧮 **Niveau de maturité perçu (1–5)**
- 📎 **Références** (lien doc officielle ou projet exemplaire)

> Ces observations ne tranchent rien.  
> Elles servent à alimenter la future **phase "Clarifier"** du processus (RFC-002 §5B).

---

## 3️⃣ Runtimes / Langages (base d'exécution)

| Langage | Nature | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|----------|--------|------------------|-----------------------|----------------|-----------|
| **Python** | Interprété, orienté objet | Large écosystème, productivité élevée, doc claire, grande compatibilité | Moins performant sur calculs lourds, overhead GIL | 5 | https://www.python.org |
| **Go** | Compilé, statiquement typé | Simplicité, performance, binaires statiques, tooling intégré | Gestion des erreurs parfois verbeuse, génériques récents | 4 | https://go.dev |
| **Rust** | Compilé, mémoire sûre | Sécurité mémoire, performance, zéro runtime | Courbe d'apprentissage abrupte, écosystème web encore jeune | 4 | https://www.rust-lang.org |
| **Node.js (TypeScript)** | Interprété, JS moteur V8 | Large communauté, async natif, typage optionnel via TS | Empilement rapide, écosystème inégal en qualité | 4 | https://nodejs.org |

---

## 4️⃣ Frameworks Web

| Framework | Langage | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|------------|----------|------------------|-----------------------|----------------|-----------|
| **Django** | Python | Sécurité intégrée, ORM complet, admin, maturité | Poids important, rigidité structurelle | 5 | https://www.djangoproject.com |
| **FastAPI** | Python | Modernité, typage, rapidité, DX | Auth et admin à assembler | 4 | https://fastapi.tiangolo.com |
| **Gin** | Go | Performance, simplicité | Middleware basique, authentification à coder | 4 | https://gin-gonic.com |
| **Fiber** | Go | Syntaxe Express-like, très rapide | Maturité moyenne, peu de standards | 3 | https://gofiber.io |
| **Actix Web** | Rust | Ultra performant, orienté async | Complexité d'apprentissage, API changeante | 4 | https://actix.rs |
| **Axum** | Rust | Sécurité typée, clarté, stabilité croissante | Moins d'exemples, moins d'extensions | 3 | https://docs.rs/axum/latest/axum/ |

---

## 5️⃣ Bases de données

| SGBD | Type | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|-------|------|------------------|-----------------------|----------------|-----------|
| **PostgreSQL** | SQL | Robuste, riche, extensions, transactions, RLS | Plus lourd à maintenir | 5 | https://www.postgresql.org |
| **MariaDB/MySQL** | SQL | Populaire, bonne compatibilité | Moins avancé sur features modernes | 4 | https://mariadb.org |
| **SQLite** | SQL embarqué | Légèreté, zéro config | Non adapté à forte charge concurrente | 3 | https://sqlite.org |
| **MongoDB** | NoSQL | Flexible, facile pour objets JSON | Moins strict sur schémas, consommation mémoire | 4 | https://www.mongodb.com |
| **CouchDB** | NoSQL distribué | Sync orientée mobile/offline | Performances variables, réplication complexe | 3 | https://couchdb.apache.org |

---

## 6️⃣ Caches / Queues / Pub-Sub

| Composant | Type | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|------------|------|------------------|-----------------------|----------------|-----------|
| **Redis** | Cache / Queue | Simple, rapide, multi-usage | Volatile par défaut, peu de persistance native | 5 | https://redis.io |
| **RabbitMQ** | AMQP Queue | Fiable, durable, bien documenté | Setup plus lourd, monitoring nécessaire | 4 | https://www.rabbitmq.com |
| **NATS** | Pub/Sub distribué | Très léger, scalable | Moins d'outillage intégré | 3 | https://nats.io |
| **Kafka** | Stream distribué | Résilience, forte scalabilité | Complexité, ressources lourdes | 3 | https://kafka.apache.org |

---

## 7️⃣ Reverse Proxy / Gateway

| Composant | Type | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|------------|------|------------------|-----------------------|----------------|-----------|
| **Caddy** | Proxy web auto-TLS | Configuration simple, HTTP/3, sécurité par défaut | Moins modulable qu'Nginx | 5 | https://caddyserver.com |
| **Nginx** | Proxy / serveur web | Ultra éprouvé, performant, stable | Configuration complexe, verbose | 5 | https://nginx.org |
| **Traefik** | Reverse proxy dynamique | Intégré Docker/K8s, observabilité native | Moins léger en usage simple | 4 | https://traefik.io |
| **Envoy** | Proxy L7 distribué | Très puissant, gRPC, observabilité | Très complexe à maintenir | 3 | https://www.envoyproxy.io |

---

## 8️⃣ Authentification / Autorisation

| Solution | Type | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|-----------|------|------------------|-----------------------|----------------|-----------|
| **Auth interne** | Simple | Sobriété, local-first, sans dépendance externe | Maintenance custom, extensibilité limitée | 4 | - |
| **Keycloak** | OIDC/SSO | Complet, extensible, open source | Lourd, setup complexe | 4 | https://www.keycloak.org |
| **Authelia** | Reverse proxy SSO | Léger, intégré à Caddy/Nginx | Moins de docs, écosystème réduit | 3 | https://www.authelia.com |

---

## 9️⃣ Stockage fichiers

| Solution | Type | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|-----------|------|------------------|-----------------------|----------------|-----------|
| **FS local** | Stockage direct | Simplicité, offline, lisibilité | Non scalable, dépend au serveur | 5 | - |
| **MinIO** | S3-compatible | API standard, auto-hébergeable | Setup plus complexe | 4 | https://min.io |

---

## 🔟 Observabilité

| Stack | Type | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|--------|------|------------------|-----------------------|----------------|-----------|
| **Logs JSON natifs** | Logging | Simples, universels | Peu d'outillage sans stack additionnelle | 5 | - |
| **Prometheus + Grafana** | Métriques | Standard open-source | Courbe d'apprentissage | 4 | https://prometheus.io |
| **OpenTelemetry** | Traces / Metrics / Logs | Standard émergent, interopérable | Mise en œuvre complexe | 3 | https://opentelemetry.io |

---

## 11️⃣ Conteneurisation / Orchestration

| Technologie | Type | Forces observées | Faiblesses observées | Maturité (1–5) | Référence |
|--------------|------|------------------|-----------------------|----------------|-----------|
| **Docker / Compose** | Conteneur / orchestration locale | Standard industriel, facile à reproduire | Dépend Docker Inc., consommation | 5 | https://www.docker.com |
| **Podman** | Conteneur rootless | Sécurité accrue, open | Moins documenté pour stack complexe | 4 | https://podman.io |
| **Kubernetes** | Orchestrateur distribué | Scalable, riche écosystème | Overkill pour MVP | 3 | https://kubernetes.io |

---

## 12️⃣ Synthèse initiale

Ce premier inventaire dessine **les matériaux disponibles** pour Relinium.  
Il montre qu'aucun choix n'est évident : la maturité, la sobriété et la sécurité varient selon les contextes d'usage.

L'étape suivante consistera à :
- Prioriser les **composants à tester en premier** (selon pertinence et accessibilité),
- Construire les **POC minimalistes** associés,
- Et documenter les premiers résultats dans `OBS-0002-tests-initiaux.md`.

---

> _"Avant de forger l'outil, il faut connaître la nature du métal."_  
> — Relinium Genesis
