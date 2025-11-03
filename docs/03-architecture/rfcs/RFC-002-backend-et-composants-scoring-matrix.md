# RFC-002 — Matrice d'exploration et de scoring : backend & composants (agnostique)

- **Statut** : 🟡 En discussion
- **Date** : 2025-01-03
- **Auteur** : Équipe Relinium Genesis
- **Version** : 1.0

---

## 1) Intention (sans présupposé)

Nous choisissons le **backend** et les **composants clés** de Relinium via une démarche **agnostique** : aucune technologie n'est présupposée (runtime, framework web, base de données, files d'attente, reverse proxy, authentification, stockage de fichiers, observabilité, conteneurisation).

**Garde-fous non négociables :**
- **Sécurité & souveraineté** : exécutable localement, contrôlable, sans dépendance cloud imposée.
- **Sobriété & lisibilité** : empreinte maîtrisée, approche compréhensible et pérenne.
- **Traçabilité & réversibilité** : décisions documentées (ADR), migration possible sans lock-in déraisonnable.

---

## 2) Portée

Cette RFC définit :
- Une **grille de critères pondérés** (100 pts) pour comparer les **candidats par composant**.
- Un **protocole d'évaluation** (Observer → Clarifier → Recomposer → Stabiliser).
- Des **POC minimalistes** reproductibles pour noter objectivement.
- Des **"kill-switch"** (seuils d'élimination) pour éviter les mauvais choix.

**Hors scope** : design UI/UX, textes marketing, feuille de route détaillée (couverts par d'autres docs).

---

## 3) Grille de critères & pondérations (100 pts)

| # | Critère | Poids | Ce que l'on mesure |
|---|---|---:|---|
| 1 | **Sécurité / Durcissement** | **25** | Surface d'attaque, middlewares/guardrails, politique d'en-têtes, validation des entrées, gestion secrets, historique CVE, patchs, durcissement possible. |
| 2 | **Souveraineté / Local-first** | **15** | Exécution locale/offline, absence de dépendances propriétaires imposées, compatibilité multi-plateformes, possibilité d'audit. |
| 3 | **Maintenabilité & bus factor** | **10** | Clarté structurante, conventions, outillage, risques "héros", migrations, courbe d'apprentissage. |
| 4 | **Productivité dev (DX)** | **10** | Rapidité MVP, scaffolding, CLI, tooling, hot reload, typage, qualité docs exemples. |
| 5 | **Performance & sobriété** | **10** | Latence p50/p95, conso RAM/CPU, stabilité sous charge, overhead minimal. |
| 6 | **Primitives data & auth** | **8** | ORM/ODM, transactions, migrations, RBAC/ABAC, OAuth2/SSO possible, sessions. |
| 7 | **Observabilité** | **5** | Logs structurés, métriques, traces, intégrations standards (OTel/Prometheus/etc.). |
| 8 | **Maturité écosystème** | **7** | Qualité documentation, cadence releases, santé communauté, longévité. |
| 9 | **Interopérabilité** | **5** | API REST/GraphQL, webhooks, jobs/queues, streaming, i18n, formats standards. |
|10 | **Documentation & pédagogie** | **3** | Clarté pour un nouveau dev, guides pas-à-pas, exemples conformes aux bonnes pratiques. |
|11 | **Licences & conformité** | **2** | Licences permissives/compatibles, usages associatifs/éthiques, conformité de base. |

> Barème par critère : **0–5** (0 = KO, 5 = excellent). Score pondéré = note × poids / 5. Total /100.

---

## 4) Catalogue des composants à explorer (agnostique)

- **Runtime / Langage** : Python, Go, Rust, (autres).
- **Framework Web** : Django, FastAPI, Flask, Gin, Fiber, Axum, Actix, (autres).
- **Persistance (SQL/NoSQL)** : PostgreSQL, MariaDB/MySQL, SQLite, MongoDB, CouchDB, (autres).
- **Cache / Queue / Pub-Sub** : Redis, RabbitMQ/AMQP, NATS, Kafka (si pertinent), (autres).
- **Reverse proxy / Gateway** : Caddy, Nginx, Traefik, Envoy, (autres).
- **AuthN/AuthZ** : interne (sessions, RBAC) vs. SSO/OIDC (Keycloak, Authelia, etc.). 
- **Stockage de fichiers** : FS local, S3-compatible (MinIO), (autres).
- **Observabilité** : logs (JSON), métriques, traces – stacks variées.
- **Conteneurisation / Orchestration** : Docker/Compose, Podman, (K8s ultérieur en option).
  
**Remarque** : la **combinaison** backend ≠ un unique choix ; on notera **chaque brique** puis on évaluera la cohérence des ensembles.

---

## 5) Protocole d'évaluation — Méthode en 4 temps

### (A) Observer (sans juger)

- Lister **3–4 candidats** par composant.
- Noter la **documentation officielle**, les exemples, la facilité d'installation.
- Définir un **MVP d'usage neutre** de Relinium pour les POC :
  1. **Auth** locale minimale + rôles (viewer/editor/admin).
  2. **CRUD** sur une ressource "document" (titre, tags, markdown, visibilité).
  3. **Recherche simple** (LIKE) + pagination.
  4. **Upload** d'un petit fichier (10–50 Mo).
  5. **Tâche asynchrone** (ex: notification / indexation légère).
  
> Aucun outil imposé : chaque candidat peut utiliser ses briques natives.

### (B) Clarifier (mesurer)

- Appliquer la **grille 0–5** sur chaque critère, **par composant**.
- Bench rapide (ex: `hey`/`wrk`) : p50/p95 sur lecture doc + auth + list.
- Mesurer RAM/CPU (`docker stats` ou OS équivalent).
- Vérifier les **capas de sécurité** (middlewares, validation, headers).
- Vérifier l'**exécution locale/offline**, l'absence de télémétrie forcée.

### (C) Recomposer (comparer)

- Remplir la **matrice générale** (cf. §7) et **par composant** (cf. §8).
- **Kill-switch** (élimination directe si) :
  - Dépendance non désactivable à un service cloud propriétaire.
  - Pas de mécanismes minimaux de durcissement/validation.
  - Empreinte mémoire absurde vs. gain (pour MVP documentaire).
- Proposer **2–3 ensembles cohérents** (ensemble = {runtime+framework+DB+proxy+auth+…}).

### (D) Stabiliser (documenter)

- Publier les **scores**, les **POC** et les **logs**.
- Ouvrir **ADR-0002** (choix du backend & premiers composants) basé sur la matrice.
- Définir **Phase 1 (MVP), Phase 2 (optimisation), Phase 3 (durcissement avancé)**.

---

## 6) Tests "hacker mindset" (génériques, pour chaque POC)

- **Bruteforce auth** : flood POST `/login` → rate-limit / lockout progressif / journalisation.
- **Injection & schémas** : JSON malformé ou types erronés → 4xx propre (pas de stacktrace brute).
- **Contrôle d'accès** : ressource `private` accessible par "viewer" → 403 attendu.
- **Upload** : dépassement taille → 413 + message propre, pas de crash.
- **Headers** : tester présence de base (X-Content-Type-Options, Referrer-Policy, etc.), CORS, CSP paramétrable.

> L'objectif n'est pas l'exhaustivité, mais la **faisabilité** du durcissement minimal dès le MVP.

---

## 7) Matrice générale (exemple à remplir)

```markdown
| Critère | Poids | Ensemble A | Ensemble B | Ensemble C |
|---|---:|---:|---:|---:|
| Sécurité / Durcissement | 25 |  ?  |  ?  |  ?  |
| Souveraineté / Local-first | 15 |  ?  |  ?  |  ?  |
| Maintenabilité / Bus factor | 10 |  ?  |  ?  |  ?  |
| Productivité dev (DX) | 10 |  ?  |  ?  |  ?  |
| Performance & sobriété | 10 |  ?  |  ?  |  ?  |
| Primitives data & auth | 8 |  ?  |  ?  |  ?  |
| Observabilité | 5 |  ?  |  ?  |  ?  |
| Maturité écosystème | 7 |  ?  |  ?  |  ?  |
| Interopérabilité | 5 |  ?  |  ?  |  ?  |
| Documentation & pédagogie | 3 |  ?  |  ?  |  ?  |
| Licences & conformité | 2 |  ?  |  ?  |  ?  |
| **Score total /100** | 100 |  ?? |  ?? |  ?? |
```

---

## 8) Matrice par composant (exemples à dupliquer)

### 8.1 Runtime / Langage

| Critère \ Candidat | Python | Go | Rust | Autre |
|---|---:|---:|---:|---:|
| Sécurité / Durcissement (25) |  ? |  ? |  ? |  ? |
| Souveraineté / Local-first (15) |  ? |  ? |  ? |  ? |
| Maintenabilité / Bus factor (10) |  ? |  ? |  ? |  ? |
| Productivité dev (10) |  ? |  ? |  ? |  ? |
| Performance & sobriété (10) |  ? |  ? |  ? |  ? |
| Observabilité (5) |  ? |  ? |  ? |  ? |
| Maturité écosystème (7) |  ? |  ? |  ? |  ? |
| Interopérabilité (5) |  ? |  ? |  ? |  ? |
| Doc & pédagogie (3) |  ? |  ? |  ? |  ? |
| Licences & conformité (2) |  ? |  ? |  ? |  ? |
| **Score /100** |  ?? |  ?? |  ?? |  ?? |

### 8.2 Framework Web

_Dupliquer pour Django, FastAPI, Gin, Fiber, Axum, Actix, etc._

### 8.3 Persistance

_PostgreSQL, MariaDB/MySQL, SQLite, MongoDB, …_

### 8.4 Cache / Queue

_Redis, RabbitMQ/AMQP, NATS, Kafka si besoin, …_

### 8.5 Reverse proxy / Gateway

_Caddy, Nginx, Traefik, Envoy, …_

### 8.6 AuthN/AuthZ

_Interne, OIDC avec Keycloak/Authelia, …_

### 8.7 Stockage fichiers

_FS local, S3-compatible, …_

### 8.8 Observabilité

_Logs, métriques, traces_

### 8.9 Conteneurisation / Orchestration

_Docker/Compose, Podman, …_

**NB** : Ne rien présumer. Tester les combinaisons minimales viables.

---

## 9) Livrables attendus

1. **POCs reproductibles** (scripts, README locaux).
2. **Matrices complétées** (composant & ensembles).
3. **Logs de bench** p50/p95 + RAM/CPU.
4. **Checklists sécurité** (middlewares/headers/validation).
5. **Recommandation finale** (2–3 ensembles) + proposition d'ADR-0002.
6. **Plan par phases** (MVP → optimisation → durcissement).

---

## 10) Questions ouvertes

- Quel niveau de "sobriété" visons-nous sur un laptop moyen ? (seuils RAM/CPU)
- Quelle priorité donnons-nous à la vitesse de livraison vs. sécurité mémoire ?
- Jusqu'où voulons-nous automatiser (scaffolding, admin UI) au stade MVP ?

---

## 11) Prochaines étapes

1. **Valider cette RFC** via discussion (7 jours minimum)
2. **Lancer les POCs** selon le protocole en 4 temps
3. **Remplir les matrices** au fur et à mesure
4. **Documenter dans ADR-0002** les choix retenus
5. **Itérer** si nécessaire avec retours terrain

---

_Cette RFC suit le processus "docs-first" de Relinium : toute décision structurante est documentée avant implémentation._

**Refs** : ADR-0001 (repo driven by docs-first), RFC-001 (choix stack initiale)
