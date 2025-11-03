# OBS-0003 — Calibration & SLOs de référence

- **Statut** : 🟢 Ouvert (calibration & gates)
- **Date** : 2025-01-03
- **Auteur** : Équipe Relinium Genesis
- **Version** : 1.0
- **Référence** : RFC-002, OBS-0001, OBS-0002

---

## 1. Intention

Ce document fixe le **référentiel** qui servira à juger objectivement les POCs et les ensembles techniques.  
Il précise **ce que Relinium optimise** (finalité produit) et fournit les **SLOs**, les **fitness functions** et les **kill-switches** qui protègent la finalité.

---

## 2. Objectifs produit (priorités)

1. **Sécurité & souveraineté** — données sous contrôle, local-first, durcissement obligatoire.  
2. **Sobriété & accessibilité** — fonctionne sur VPS modeste & laptop standard.  
3. **Productivité & durabilité** — développer vite sans accumuler une dette technique excessive.  
4. **Scalabilité réaliste** — montée en charge cohérente avec des associations/collectifs (pas hyperscale).

Ces priorités servent de boussole : les SLOs et les gates les traduisent en seuils mesurables.

---

## 3. Environnements de référence (cibles de test)

| Profil | CPU | RAM | Stockage | Usage cible |
|---|---:|---:|---:|---|
| Laptop dev | 4–8 coeurs | 16 GB | SSD | Dev local, hot-reload |
| VPS asso (cible MVP) | 2 vCPU | 4 GB | 80 GB | Déploiement d'une asso basique |
| VPS MCM (prod small) | 4 vCPU | 8–16 GB | 200 GB | Coop multi-services |

**Règle** : mesurer prioritairement sur **VPS asso (2vCPU / 4GB)**. Les seuils et scores sont calibrés sur cet environnement.

---

## 4. SLOs minimaux (objectifs & seuils KO)

> Les SLOs sont regroupés par domaine. Pour chaque métrique : *objectif* (confort), *seuil* (acceptable) et *KO* (kill-switch).

### 4.1 Performance & Sobriété

- **Latence p95 GET /documents (500 docs)**  
  - Objectif : **< 200 ms**  
  - Seuil acceptable : **< 400 ms**  
  - KO : **≥ 400 ms**
- **RAM idle service API (uniquement process)**  
  - Objectif : **< 200 MiB**  
  - Seuil acceptable : **< 400 MiB**  
  - KO : **≥ 600 MiB**
- **Throughput stable** (20 req/s) sans erreurs 5xx sur VPS cible  
  - Objectif : stable à 20 req/s  
  - KO : erreurs 5xx > 1% sous charge modérée

### 4.2 Sécurité (non négociable)

- **Validation d'entrée** : schémas + sanitization — **KO si absent**  
- **Rate-limit login** : présent (ex: 5 req/min/IP) — **KO si absent**  
- **Gestion d'erreurs** : pas de stacktrace publique — **KO si fuite**  
- **Headers de base** (X-Content-Type-Options, Referrer-Policy, X-Frame-Options/CSP) — **KO si impossible de les poser**

### 4.3 Opérabilité

- **Installation & run** : `make dev` / `make test` → service up en **< 30 min**  
  - KO si > 60 min pour un développeur raisonnable
- **Migrations DB** : versionnées & rollback possible — **KO si migrations non reproductibles**
- **Logs** : logs lisibles + corrélations (correlation-id) — KO si logs absents

### 4.4 Coût

- **Budget VPS MVP** : déploiement viable ≤ **15 €/mois** sur offre VPS grand public (approx. 2vCPU/4GB)  
  - KO si coût initial > 25 €/mois pour MVP

---

## 5. Fitness functions (tests automatisables)

Chaque fitness function devient un **gate CI** (pass/fail). Exemple de suites :

- **security_fitness()**  
  - tests: rate-limit present, validation schema, réponse 4xx sur payload malformé, headers présents  
  - fail => blocage PR
- **resource_fitness()**  
  - tests: RAM idle < seuil_KO, p95 < seuil_KO sous bench light  
  - fail => alerte et marquage "re-eval"
- **sovereignty_fitness()**  
  - tests: boot offline (no external network call required), no phone-home during startup  
  - fail => rejet immédiat
- **operability_fitness()**  
  - tests: `make dev` completes, `make test` passes, documentation minimale (README) present  
  - fail => bloque merge

---

## 6. Kill-switch (conditions éliminatoires immédiates)

Un POC ou ensemble est **disqualifié** si l'une des conditions suivantes est vraie :
- Dépendance cloud **obligatoire** pour démarrer (phone-home non désactivable).  
- Absence de validation d'entrée / erreurs exposant stacktraces.  
- RAM idle ≥ **600 MiB** (sur VPS 2vCPU/4GB) pour un service API minimal.  
- Impossibilité technique d'ajouter des headers de sécurité au proxy ou à l'app.  
- Migration DB non reproductible / absence totale de versioning de schéma.

---

## 7. Tableau de notation 0–5 normalisé sur les SLOs

> On applique ce barème pour chaque critère de RFC-002. Ci-dessous, exemples normalisés pour les critères clefs.

### 7.1 Performance & Sobriété (poids 10)

| Note | Condition (p95 / RAM idle) |
|---:|---|
| 5 | p95 < 120 ms **ET** RAM idle < 120 MiB |
| 4 | p95 < 200 ms **ET** RAM idle < 200 MiB |
| 3 | p95 < 300 ms **OU** RAM idle < 350 MiB |
| 2 | p95 < 400 ms **OU** RAM idle < 500 MiB |
| 1 | p95 < 600 ms **OU** RAM idle < 700 MiB |
| 0 | p95 ≥ 600 ms **OU** RAM idle ≥ 700 MiB (KO) |

### 7.2 Sécurité / Durcissement (poids 25)

| Note | Condition (presence of controls) |
|---:|---|
| 5 | All mandatory controls present + automated security tests pass |
| 4 | Controls present, minor manual hardening remaining |
| 3 | Controls partially present, documented TODOs |
| 2 | Controls weak / many manual steps |
| 1 | Controls absent or inconsistent |
| 0 | Critical missing (validation, rate-limit or error leakage) → KO |

### 7.3 Souveraineté / Local-first (poids 15)

| Note | Condition |
|---:|---|
| 5 | Boot offline, no external services required, all components self-hostable |
| 4 | Boot offline possible with documented switches (opt-in) |
| 3 | Some optional external services used but can be replaced |
| 2 | Heavy reliance on external services but replacement possible with effort |
| 1 | Tightly coupled to external cloud services |
| 0 | Cannot run without proprietary cloud (KO) |

### 7.4 Opérabilité / Productivité / Maintenabilité (poids combinés)

- Évaluer par temps d'installation, clarté docs, tests.  
- Utiliser barème 0–5 : 5 = dev up in <15min, tests clear, migrations smooth ; 0 = non reproductible.

> Appliquer la même logique 0–5 (exemples ci-dessus) pour tous les 11 critères de RFC-002, en les calibrant par rapport aux SLOs présentés.

---

## 8. Méthode de calibration & procédure de test

1. **Seed unique** : 500 documents + one 25MB upload (fichier binaire généré).  
2. **Environnement** : VPS cible (2vCPU/4GB). Mesurer p50/p95 avec `hey -n 1000 -c 20`.  
3. **Mesures** : p50/p95, req/s, erreurs %, RAM idle, RAM peak, CPU avg, temps cold start.  
4. **Security checks** : run automated scripts for injection/login-rate-limit/error-exposure.  
5. **Reporting** : remplir `POC.md`, `RESULTS.md`, `SECURITY.md` dans le dossier POC.  
6. **Scoring** : convertir mesures en notes 0–5 selon tableaux. Calculer score pondéré final.

---

## 9. Checklist CI — automatiser les gates (exemples à intégrer en workflow)

- [ ] **docs-ci** : README, GOVERNANCE, SECURITY présents (déjà en place).  
- [ ] **poc-smoke** : run `make test` minimal → fail si tests unitaires KO.  
- [ ] **bench-light** : exécuter un bench léger (script local ou container) → collecter p95 & RAM ; fail si dépasse seuil KO.  
- [ ] **security-scan** : exécuter audit dépendances (pip-audit / npm audit / govulncheck / cargo-audit) → fail on critical vuln.  
- [ ] **sovereignty-check** : test offline boot (simulate network restricted) → fail si phone-home during startup.  
- [ ] **artifact-check** : presence of POC.md, RESULTS.md, SECURITY.md changed/updated in PR for POCs touched.  
- [ ] **policy-gates** : require ADR link for any change that alters SLOs or kill-switch values.

**Implementation idea (GitHub Actions)** :
- Workflow `poc-validation.yml` triggered on PR to `main` or `feat/*`:
  1. Checkout
  2. Run `make test` in POC directories touched
  3. Run `./scripts/bench_light.sh` (collect p95 & RAM)
  4. Run `./scripts/security_checks.sh`
  5. Upload RESULTS.md as artifact and post summary as PR comment
  6. Fail if any KO thresholds tripped

---

## 10. Gouvernance des seuils & révision

- Les SLOs & kill-switches sont **vivants** : tout changement se fait via RFC (discussion) + ADR pour acter la révision.  
- Fréquence de revue recommandée : **quarterly** pour ajuster aux réalités hardware & coût.

---

## 11. Annexes rapides

- **Scripts recommandés** : `scripts/bench_light.sh`, `scripts/measure_memory.sh`, `scripts/security_checks.sh` (décrire plus tard).  
- **Format de rapport** : `RESULTS.md` doit contenir au minimum : environnement, bench output, RAM/CPU snapshot, verdict (PASS/WARN/KO).

---

> _"On n'évalue pas pour prouver qu'on a raison, on évalue pour savoir si la solution sert réellement la fin qu'on s'est donnée."_  
> — Relinium Genesis
