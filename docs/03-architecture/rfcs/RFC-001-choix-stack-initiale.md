# RFC-001 – Choix de stack initiale (frontend / backend / infra)

- **Statut**: 🟡 En discussion  
- **Date**: 2025-11-03  
- **Auteur**: Équipe Relinium Genesis  
- **Version**: 1.0  

---

## 🎯 Résumé

Cette RFC vise à déterminer les fondations techniques de **Relinium**, à savoir le choix de la stack initiale côté frontend, backend et infrastructure.  
L'objectif n'est pas d'imposer des choix précoces, mais d'établir un cadre d'analyse basé sur les **valeurs fondatrices du projet** : souveraineté, sobriété, sécurité et évolutivité.  

Les décisions finales découleront d'un ou plusieurs **ADR** qui valideront chaque couche (ex : ADR-0002-backend-choice, ADR-0003-frontend-choice).

---

## 🧭 Motivation

Avant de coder, il est nécessaire de s'assurer que la base technique :
- soit **accessible** à des développeurs aux profils variés (open, documentée, maintenable),  
- permette une **installation locale souveraine** (offline-ready, sans dépendances toxiques),  
- respecte les **contraintes de sécurité dès la conception**,  
- et soit cohérente avec la **méthodologie docs-first** adoptée dans [ADR-0001](../decisions/ADR-0001-repo-driven-by-docs-first.md).

---

## 🧱 Périmètre de la RFC

Cette RFC couvre :
1. Les **langages** et **frameworks** à utiliser (frontend / backend).  
2. Les **outils de déploiement** et de gestion (infra, CI/CD, conteneurs).  
3. Les **critères de sélection** et leur pondération.  
4. Les **propositions de stack** à comparer.  

Elle ne statue pas encore sur le design UI, la gouvernance technique, ni la stack IA — ces sujets feront l'objet de RFC spécifiques.

---

## ⚖️ Critères de sélection

| Domaine | Critère | Poids | Description |
|----------|----------|-------|-------------|
| **Sécurité** | Isolation, chiffrement, auditabilité | 🔥 5 | Tout choix doit permettre un contrôle total des données et dépendances. |
| **Souveraineté** | Dépendance à des services externes | 🔥 5 | Doit pouvoir tourner localement, sans cloud propriétaire. |
| **Sobriété** | Performance, empreinte énergétique | ⚙️ 4 | Stack légère, sans surcouche inutile. |
| **Accessibilité** | Apprentissage, documentation | ⚙️ 4 | Stack compréhensible pour devs expérimentés et débutants. |
| **Scalabilité** | Modularité, maintenabilité | ⚙️ 3 | Croissance possible sans réécriture. |
| **Interopérabilité** | API, protocoles standard | ⚙️ 3 | Doit communiquer facilement avec d'autres outils open-source. |
| **Communauté** | Vitalité open-source, support | ⚙️ 3 | Stack vivante, non abandonnée. |

---

## 🧩 Candidats envisagés

### **Backend**
| Option | Description | Avantages | Risques / Points faibles |
|--------|--------------|------------|---------------------------|
| **Django (Python)** | Framework complet, robuste, excellent ORM, admin intégré. | Stabilité, sécurité, communauté mature. | Courbe d'apprentissage, lourdeur initiale. |
| **FastAPI (Python)** | API moderne, rapide, typée, async. | Performance, simplicité, typage fort. | Moins structurant que Django. |
| **Go (Gin/Fiber)** | Backend léger, compilé, hautes performances. | Rapidité, faible empreinte, sécurité mémoire. | Moins de ressources "haut niveau". |
| **Rust (Axum/Actix)** | Sécurité mémoire et performance ultime. | Souveraineté, fiabilité, performance. | Courbe d'apprentissage raide, tooling exigeant. |

### **Frontend**
| Option | Description | Avantages | Risques / Points faibles |
|--------|--------------|------------|---------------------------|
| **Nuxt 4 (Vue 3 + TS)** | Framework SSR/SSG moderne, excellent pour les apps documentées. | Rapidité, simplicité, accessibilité, SSR natif. | Moins d'outillage IA intégré. |
| **Next.js 15 (React)** | Référence marché, écosystème vaste. | Documentation, compatibilité large. | Dépendance plus forte à Vercel, surcouche lourde. |
| **SvelteKit** | Framework léger et réactif, proche du hardware. | Sobriété, performance, faible empreinte. | Moins de maturité sur projets complexes. |

### **Infrastructure / Orchestration**
| Option | Description | Avantages | Risques / Points faibles |
|--------|--------------|------------|---------------------------|
| **Docker + Compose** | Standard, simple à maintenir. | Portabilité, isolation, reproductibilité. | Non idéal pour scaling massif. |
| **Podman** | Alternative 100% open source à Docker. | Rootless, sécurité renforcée. | Moins documenté. |
| **Caddy** | Reverse proxy auto-HTTPS, HTTP/3, mTLS possible. | Simplicité, sécurité-by-default. | Moins d'outillage avancé qu'un Traefik. |
| **Traefik** | Proxy dynamique, orienté microservices. | Observabilité, intégration CI/CD. | Plus complexe à configurer. |

---

## 🧩 Propositions de combinaisons initiales

### **Option A — Django + Nuxt + Caddy**
> Stack stable, éprouvée, souveraine et compréhensible.

- Backend solide, sécurisé et complet.  
- Front SSR performant, UX accessible.  
- Proxy simple, certificat auto, HTTP/3.  
- Idéale pour un MVP humainement gérable.  

**Orientation :** base recommandée pour tests internes.

---

### **Option B — FastAPI + SvelteKit + Traefik**
> Stack plus légère, plus rapide à itérer.

- API Python moderne.  
- Front très léger.  
- Proxy évolutif.  
- Convient à une approche modulaire et à des environnements distribués.

---

### **Option C — Rust + Nuxt + Caddy**
> Stack "paranoïaque", ultra-sécurisée.

- Rust backend pour les traitements critiques.  
- Nuxt pour l'expérience utilisateur.  
- Caddy pour la couche réseau mTLS et auto-renewal.

**Orientation :** prototype souverain et hautement sécurisé.

---

## 🧮 Éléments à valider

- Nombre de contributeurs capables de travailler sur chaque stack.  
- Compatibilité avec les objectifs pédagogiques et collectifs de Relinium.  
- Possibilité de faire tourner l'app **en local, sans dépendances cloud**.  
- Niveau de maintenance exigé par stack.

---

## 🔐 Impact sécurité

Chaque stack devra être accompagnée d'un **ADR spécifique** sur :
1. L'isolation des environnements.  
2. Le modèle d'authentification et de permissions.  
3. La gestion des secrets et de la configuration.  
4. Le modèle de chiffrement interne / externe.  

Le tout alimentera le registre de risques (`docs/04-risk/risk_register.md`).

---

## 🧭 Étapes suivantes

1. Collecte des avis des contributeurs (via discussion GitHub / issues).  
2. Choix des 2 stacks finalistes pour test (Prototype A / Prototype B).  
3. Création des ADR associés :
   - ADR-0002 – Choix du backend.
   - ADR-0003 – Choix du frontend.
   - ADR-0004 – Choix du proxy et orchestration.
4. Validation collective → merge final dans `main`.

---

> _"Avant de choisir une technologie, choisissons un rythme."_  
> — Relinium Genesis
