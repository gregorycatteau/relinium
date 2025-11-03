# OBS-0002 — Tests initiaux & POCs minimaux (agnostiques)

- **Statut** : 🟢 Ouvert (phase d'observation — tests)
- **Date** : 2025-01-03
- **Auteur** : Équipe Relinium Genesis
- **Version** : 1.0
- **Références** :
  - [RFC-002 — Matrice d'exploration et de scoring (agnostique)](../rfcs/RFC-002-backend-et-composants-scoring-matrix.md)
  - [OBS-0001 — Inventaire initial des backends et composants](OBS-0001-backend-composants-inventaire.md)

---

## 1) Intention

Définir des **POC minimaux, reproductibles et comparables** pour évaluer les candidats (backend & composants) **sans biais**.  
Chaque test vise des **constats observables** : sécurité, souveraineté/local-first, sobriété, DX, perf, primitives data/auth, observabilité, interop.

> _Règle d'or :_ un POC est **le plus petit ensemble** permettant de démontrer la faisabilité d'un usage Relinium, avec **journalisation** et **mesures**.

---

## 2) Contexte commun (agnostique)

- Un répertoire par POC, ex : `pocs/<famille>/<candidat>/`.
- Un script **run local** (sans cloud) : `make dev`, `make test`, `make bench`, `make stop`.
- Variables sensibles via `.env.example` (jamais `.env` commité).
- Logs en **texte** (+ JSON si dispo).
- Bench simple : `hey` ou `wrk` (équivalent selon écosystème).
- Mesure ressources : `docker stats` ou OS équivalent (RAM/CPU).

---

## 3) Jeu d'essai minimal (commun)

- **Rôles** : `viewer`, `editor`, `admin`.
- **Utilisateur de test** : `contact@pixelprowlers.io` / `Admin#Test123` (si auth interne).
- **Ressource** : `document` { id, title, tags[], visibility(`public|private`), body(markdown), created_at }.
- **Fichiers** : un `.md` de 2–5 Ko + un upload de 20–50 Mo (généré localement).

---

## 4) POCs par famille

### 4.1 Runtime / Framework Web (candidat agnostique)

**Objectif :** Démarrer un service HTTP local implémentant 5 endpoints REST + 1 tâche async.

**Endpoints requis :**
- `POST /auth/login` → token/session (si auth interne)  
- `POST /documents` → créer (body: title, body, tags, visibility)  
- `GET /documents?search=...&page=1&size=20` → liste paginée + filtre LIKE  
- `GET /documents/:id` → lecture  
- `PUT /documents/:id` → MAJ (réservé editor/admin)  
- `POST /uploads` → upload fichier (20–50 Mo), retour hash + chemin  
- (**Async**) tâche : `POST /documents/:id/summarize` → crée un résumé en tâche de fond, endpoint `GET /tasks/:task_id` pour statut

**Sécurité minimale :**
- Validation d'entrée stricte (schémas/typage).  
- Désactivation d'erreurs verbeuses en prod.  
- Headers sécurité basiques (même côté app si pas de proxy) :
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: no-referrer`
  - `X-Frame-Options: DENY` (ou CSP frame-ancestors)
  - `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'` (si applicable)  
- Rate-limit `/auth/login` (ex : 5 req/min/IP).

**DX / Commandes attendues :**
- `make dev` → run local/hot-reload si possible  
- `make test` → tests unitaires CRUD + auth + upload  
- `make bench` → bench GET /documents (p50/p95), RAM/CPU  
- `make stop`

**Journal à produire :**
- `POC.md` (contexte, version, liens doc)  
- `RESULTS.md` (mesures chiffrées, RAM/CPU, remarques)  
- `SECURITY.md` (middlewares, headers, validations, points encore faibles)

---

### 4.2 Persistance (SQL/NoSQL)

**Objectif :** Implémenter la persistance de `document` + sessions/tokens.

**Tests requis :**
- Migrations init + rollback.  
- CRUD complet, index sur `title` et `tags`.  
- Pagination performante (LIMIT/OFFSET ou curseurs).  
- Transaction : création + upload (simulateur) atomique.  
- Contrainte `visibility` correcte.  

**Journal :**
- `SCHEMA.sql` ou migrations.  
- Temps de migration, taille DB, latence médiane lecture/écriture (échantillon).  
- Points forts/faibles constatés (verbatims).

---

### 4.3 Cache / Queue / Pub-Sub

**Objectif :** Exécuter la tâche `summarize` en asynchrone.

**Tests requis :**
- Envoi d'une tâche → statut → résultat.  
- Résilience si worker down/up.  
- Timeout + retry (ex : max 3 retries).  
- Mesures de latence moyenne.

**Journal :**
- `RESULTS.md` (latence, cas d'échec, reprise).  
- Gestion des erreurs / dead-letter (si dispo).

---

### 4.4 Reverse Proxy / Gateway (facultatif en POC 1)

**Objectif :** Ajouter un proxy **en local** avec TLS local (auto) ou simple HTTP local, *sans imposer de techno*.

**Tests requis :**
- Proxy → service app.  
- Headers sécurité ajoutés au niveau proxy.  
- Limitation taille upload (ex : 64 Mo).  
- Logs d'accès.

**Journal :**
- Conf proxy (ex: `conf.<proxy>.md`), avantages/inconvénients observés.  

---

### 4.5 AuthN/AuthZ

**Objectif :** Implémenter **auth interne simple** (sessions ou token) **ou** démo OIDC local (facultatif au POC 1).

**Tests requis :**
- Login OK/KO, verrouillage progressif si bruteforce.  
- Rôles appliqués : `viewer` (lecture publique), `editor` (CRUD), `admin` (tout).  
- Token expiré → 401.

**Journal :**
- Schéma flux d'auth, rotation tokens (si existante), stockage des sessions.

---

### 4.6 Stockage fichiers

**Objectif :** Uploader un fichier 20–50 Mo et retourner hash + chemin.

**Tests requis :**
- Upload in-range (OK), hors-range (413).  
- Vérification hash (intégrité).  
- Dossier de stockage local (`./data/uploads`) ou driver S3-compatible (facultatif POC 1).

**Journal :**
- Débit moyen, erreurs, nettoyage.

---

### 4.7 Observabilité

**Objectif :** Avoir **au minimum** logs structurés.

**Tests requis :**
- Logs JSON (si possible), niveaux (info/warn/error).  
- Compteur des requêtes par endpoint (optionnel).  
- Traçage simple (correlation-id en header) — si facile.

**Journal :**
- Exemple de log (sanitisé), pertinence pour debug.

---

### 4.8 Conteneurisation (facultatif POC 1)

**Objectif :** Fournir un `compose.yaml` minimal **optionnel**, si cela **simplifie** la reproduction.

**Tests requis :**
- `docker compose up` → service accessible.  
- `docker stats` → RAM/CPU en idle et sous bench léger.

**Journal :**
- Ressources mesurées, complexité ajoutée par la conteneurisation.

---

## 5) Mesures & Benchmarks (standards)

- **Bench lecture** : `GET /documents?page=1&size=20` (données seedées : 500 docs).  
  - Outil : `hey -n 1000 -c 20 http://localhost:PORT/documents?page=1&size=20`  
  - **Collecter** : p50, p95, req/s, erreurs, RAM/CPU (moyenne).  
- **Bench upload** : fichier 20–50 Mo.  
  - **Collecter** : durée, erreurs, RAM/CPU pic.  
- **Auth** : 50 logins successifs (non bruteforce).  
  - **Collecter** : taux d'échec anormal, latence.

> Les chiffres ne sont qu'indicatifs et **ne servent pas encore à juger** : ils aident à comprendre l'ordre de grandeur et la stabilité initiale.

---

## 6) Tests "hacker mindset" (obligatoires, légers)

- **Bruteforce doux** : 20 tentatives rapides `/auth/login` avec mauvais mot de passe → verrouillage progressif et log d'alerte.  
- **Injection** : JSON malformés / types erronés → 4xx propre, **pas** de stacktrace brute.  
- **Accès** : essayer de lire un `document` `private` en `viewer` → 403.  
- **Upload** : au-delà du seuil → 413 propre.

**Journal "SECURITY.md" par POC** :
- Middlewares actifs  
- Validation d'entrées (lib/outillage)  
- Headers sécurité  
- Limites et TODO

---

## 7) Modèle de journal standard (à copier dans chaque POC)

### POC.md
- But, versions, instructions `make`, dépendances, variables, liens docs.

### RESULTS.md
- **Perf** : p50/p95, req/s, RAM/CPU (idle & bench), taille binaire (si compilé).  
- **DX** : installation (painless/douloureux), clarté des erreurs, lisibilité du code.  
- **Ergonomie** : temps réel pour MVP, friction.

### SECURITY.md
- **Validation** : schémas, sanitization, erreurs masquées.  
- **Contrôles** : rate-limit, auth, rôles, uploads (taille & content-type).  
- **Headers** : liste exacte envoyée.  
- **Observations** : points forts/faibles et TODO de durcissement.

---

## 8) Critères de succès d'un POC

- **Reproductible** par un autre dev en < 30 min.  
- **Endpoints** et **tests de base** OK.  
- **Journal** rempli et déposé.  
- **Pas** de dépendance cloud **obligatoire**.  
- **Sécurité minimale** activée (validation, rate-limit login, headers).

---

## 9) Prochaine étape

Une fois 2–3 POCs par famille réalisés :
- Remplir la **matrice RFC-002** (notes 0–5 par critère).  
- Proposer **2–3 ensembles cohérents** (backend + DB + proxy + auth + stockage).  
- Ouvrir **ADR-0002** (choix du backend & des premiers composants) avec :
  - le **gagnant**,  
  - les **compromis**,  
  - un **plan par phases** (MVP → optimisation → durcissement avancé).

---

> _"Un POC n'est pas une promesse de production ; c'est une lampe torche dans une pièce encore obscure."_  
> — Relinium Genesis
