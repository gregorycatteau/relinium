# 🌐 Relinium

> _Reprendre la main sur le numérique. Créer un espace vivant, sobre et souverain._

---

## 🜂 Introduction

**Relinium** est un projet libre et ouvert né d'une idée simple :  
le numérique ne doit plus être un outil de captation, mais un **terrain de réconciliation** entre l'humain, la technologie et le vivant.

Ici, avant d'écrire la moindre ligne de code, nous **documentons le sens** :  
ce que nous faisons, pourquoi nous le faisons, et comment nous le ferons de manière juste, sécurisée et durable.  

Ce dépôt constitue la **métacognition du projet**, sa conscience en développement.  
C'est ici que l'on pose les fondations — valeurs, principes, choix structurants, risques, méthodes.

---

## 🧭 Objectif

Construire un **écosystème numérique coopératif** où :

- Chaque individu garde la **souveraineté** sur ses données et ses outils.  
- Les contributions **humaines** (et non seulement techniques) sont reconnues.  
- Le code et la documentation **évoluent ensemble**, de manière traçable et réversible.  
- La technologie reste **au service du vivant**, jamais l'inverse.

---

## 🧩 Pourquoi ce dépôt est (encore) vide

Nous commençons par ce qui est le plus important : **le sens**.  
Aucune ligne de code n'est écrite tant que nous n'avons pas clarifié :

1. Les **valeurs** qui orientent chaque décision.  
2. La **charte de la matière** (notre rapport au numérique).  
3. La **structure documentaire et décisionnelle** (ADR, RFC).  
4. Les **risques et mitigations** préalables.

Tout cela est visible dans le dossier [`/docs`](./docs).

---

## 📚 Structure du projet

```text
relinium/
├─ README.md              ← Vous êtes ici
├─ LICENSE
├─ CODE_OF_CONDUCT.md
├─ CONTRIBUTING.md
├─ SECURITY.md
├─ GOVERNANCE.md
├─ docs/
│  ├─ 00-overview/        ← Vision, principes, vocabulaire commun
│  ├─ 01-genesis/         ← Fondations et charte de la matière
│  ├─ 02-strategy/        ← Roadmap et axes de développement
│  ├─ 03-architecture/    ← Décisions techniques (ADR / RFC)
│  ├─ 04-risk/            ← Modèle de menaces et registre de risques
│  ├─ 05-governance/      ← Rôles, processus de décision
│  ├─ 06-ops/             ← Maintenance, sauvegarde, incidents
│  └─ 07-contrib/         ← Guide pour contributeurs et style
```

---

## 🧱 Premiers repères

### 🔹 Lire d'abord

- **Vision globale** → `docs/00-overview/vision.md`
- **Principes directeurs** → `docs/00-overview/principles.md`
- **Charte de la Matière** → `docs/01-genesis/charte_matiere.md`

### 🔹 Comprendre la logique

- **Décisions d'architecture** → `docs/03-architecture/decisions/`
- **Propositions d'évolution** → `docs/03-architecture/rfcs/`

### 🔹 Suivre les risques

- **Modèle de menaces** → `docs/04-risk/threat_model.md`
- **Registre des risques** → `docs/04-risk/risk_register.md`

---

## ⚖️ Principes clés

| Principe | Description |
|----------|-------------|
| **Transparence** | Tout ce qui peut être expliqué doit l'être en termes simples. |
| **Souveraineté** | Chaque utilisateur reste maître de ses données et de ses choix. |
| **Sobriété** | On conçoit ce qui est nécessaire, rien de plus. |
| **Sécurité** | Les menaces sont anticipées dès la conception. |
| **Traçabilité** | Les décisions sont documentées et auditées (ADR). |
| **Accessibilité** | Le projet doit rester compréhensible par tous, techniciens ou non. |

---

## 🛡️ Sécurité et gouvernance

- **Relinium** suit une logique **security-by-design**.
- Les principes et procédures de sécurité sont documentés dans `SECURITY.md`.
- La gouvernance collective est décrite dans `GOVERNANCE.md`.

Toute contribution majeure est accompagnée d'un **ADR** (Architecture Decision Record)  
et d'une revue croisée entre contributeurs pairs.

---

## 🤝 Contribuer

Nous accueillons toute contribution respectueuse du cadre défini.  
Avant toute action :

1. Lire `CONTRIBUTING.md`.
2. Proposer une **issue** ou une **RFC** pour discussion.
3. Rédiger un **ADR** si vous introduisez un choix structurant.

---

## 🧩 État actuel

| Domaine | Statut | Description |
|---------|--------|-------------|
| **Documentation** | 🟩 En cours | Vision, principes et charte de la matière en rédaction |
| **Architecture** | ⬜ À venir | Choix de stack et modèle de données |
| **Sécurité** | 🟨 Initialisée | Threat model et registre des risques créés |
| **Gouvernance** | 🟨 En cours | Processus de décision en définition |

---

## 📅 Prochaines étapes

1. Rédiger **ADR-0001** – Repo driven by docs-first.
2. Ouvrir **RFC-001** – Choix de stack initiale (frontend / backend / infra).
3. Définir le premier cycle de transformation : **Observation → Clarification**.
4. Documenter le rôle de chaque participant.

---

## 📜 Licence

**Licence à définir** — probablement MIT ou licence éthique maison (ouverte, non extractive).  
Le projet sera conçu pour rester libre mais non exploitable commercialement sans accord explicite.

---

## ✉️ Contact

Pour toute question, suggestion ou contribution :  
**contact [at] relinium.io**

---

> _"Avant de coder le monde, commençons par le comprendre."_  
> — **Relinium Genesis**
