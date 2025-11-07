---
id: "ADR-0001"
type: "ADR"
status: "Accepté"
date: "2025-01-05"
author: "Greg Catteau"
version: "1.0.0"
tags: ["governance", "methodology", "docs-first"]
links:
  cited_by: ["RFC-001", "RFC-002"]
---

# ADR-0001 – Repo Driven by Docs-First

---

## 🧭 Contexte

Le projet **Relinium** démarre sur une base vide, sans code.  
Avant d'écrire la première ligne, il est nécessaire de définir une approche structurante pour éviter la dérive, le gaspillage d'énergie et la perte de sens.

La plupart des projets logiciels commencent directement par le développement, reléguant la documentation à une tâche secondaire.  
Cette méthode entraîne :
- des incohérences entre les intentions et la mise en œuvre,  
- une dette conceptuelle rapide,  
- une méconnaissance des risques et dépendances réelles,  
- et une perte de vision collective à mesure que le code s'accumule.

Relinium, en revanche, se veut **un projet de sens avant d'être un projet de code**.  
Il s'agit d'un espace vivant où la documentation **est la matière première** du développement.

---

## 💡 Décision

Nous adoptons une approche **docs-first**.  
Cela signifie que **chaque élément du projet** (technique, organisationnel, éthique ou sécuritaire) doit être **pensé, décrit et documenté** avant toute implémentation.

Le dépôt Relinium constitue donc **la mémoire vivante du projet**, où la documentation guide le code, et non l'inverse.

**Concrètement :**
1. Aucun développement n'est amorcé sans un document de référence (vision, RFC ou ADR).  
2. Chaque décision technique majeure doit être accompagnée d'un ADR.  
3. Les choix d'architecture, de stack ou de modèle de données seront validés après discussion dans une RFC.  
4. Le code doit refléter les décisions prises, et non les précéder.  
5. La documentation est considérée comme un **artefact exécutable** au même titre que le code source.

---

## ⚙️ Conséquences

### Positives
- Vision claire et partagée avant toute implémentation.  
- Réduction des erreurs de direction et du refactoring non justifié.  
- Historique complet des choix et des raisons derrière chaque décision.  
- Facilite la montée en compétence de nouveaux contributeurs.  
- Permet d'intégrer l'éthique, la sécurité et la gouvernance dès la conception.

### Négatives
- Temps initial plus long avant d'obtenir du code exécutable.  
- Peut frustrer les profils orientés "delivery immédiate".  
- Exige une rigueur rédactionnelle continue.

### Dette technique potentielle
- Risque de désynchronisation entre la doc et le code si la discipline n'est pas tenue.

---

## 🔐 Sécurité et intégrité

- L'approche docs-first permet une **traçabilité complète** des choix affectant la sécurité.  
- Les modèles de menaces et mitigations sont intégrés dans le cycle documentaire.  
- La signature des commits et la protection des branches principales sont obligatoires.

---

## 🧱 Alternatives envisagées

### Option A – Code First
Rejetée, car contraire à la philosophie du projet.  
Elle conduit rapidement à une perte d'alignement entre l'intention et l'action.

### Option B – Hybrid Approach (Code + Doc en parallèle)
Écartée, car elle maintient une confusion sur la hiérarchie des priorités.  
Le code prend toujours le dessus sur la réflexion à long terme.

---

## 🪶 Conséquences humaines

- Installe une culture du **temps long** et du **travail réfléchi**.  
- Favorise la **transparence** et la **compréhension mutuelle**.  
- Donne à chaque contributeur la possibilité d'être acteur du sens, pas seulement du code.

---

## 🧩 Liens associés

- [RFC-001 – Choix de stack initiale (à venir)](../rfcs/RFC-001-choix-stack-initiale.md)  
- [docs/01-genesis/charte_matiere.md](../../01-genesis/charte_matiere.md)  
- [docs/00-overview/vision.md](../../00-overview/vision.md)

---

> _"La documentation n'est pas le récit du projet. Elle en est la conscience."_  
> — Relinium Genesis
