---
id: "SPRINT_DOC-0301"
id_root: "SPRINT_DOC-0301"
type: "SPRINT_DOC"
status: "Terminé"
date: "2025-11-10"
author: "Codex (mode auto-critique)"
version: "1.0"
scope: "organizational"
pattern: "observation"
previous_hash: "sha256:0000000000000000000000000000000000000000000000000000000000000000"
self_hash: sha256:bf3e0ac654fc5d29467536196e1e8b7b39e35732b61939066aaab50b78dff83f
---

## 1. Constats factuels

Les journaux `validate_frontmatter_C1H.log` et `schema_check_C1D.log` montrent qu'après plusieurs itérations, **42 % des fichiers analy­sés échouent toujours** (39/81 seulement OK). Les blocages ne sont pas concentrés sur un seul répertoire : on retrouve des écarts à la fois dans les racines historiques (`docs/03-architecture/*`), dans les sprints v1.0 et dans les artefacts récents ALIGN/PILOT (cf. `reports/analysis/validate_frontmatter_C1H.log`). L’échec n’est donc pas lié à une simple dette résiduelle mais à une méthode incapable de produire une convergence globale.

Principaux signaux :

1. **Incohérences d’ID / pattern** – exemples : `docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first.md` cite `RFC-001` sans suffixe conforme tandis que les plans ALIGN/PILOT portent encore des IDs du type `PLAN-ALIGN-*`. Cela révèle que la migration « ID-based » n’a jamais été industrialisée ; chaque équipe injecte ses propres conventions sans filtre automatisé en amont.
2. **Champs obligatoires manquants** – la quasi-totalité des artefacts SSOT-v1.0 n’a pas de `previous_hash`. Nous avons tenté de corriger les statuts/self_hash mais **aucun workflow ne remplit ni ne vérifie la filiation cryptographique pour ces fichiers hérités**, rendant impossible la preuve d’immutabilité exigée par RFC-004.
3. **Liens mixtes chemins/IDs** – malgré les correctifs récents, les LIENS (implements/cites) mélangent toujours des chemins et des IDs (ex. `reports/validation/SSOT_V1_1_ALIGN_PHASE2_CODEX.md` pointait vers des fichiers plutôt que des IDs). Le backend de validation applique une regex stricte, d’où la cascade d’erreurs.

## 2. Analyse auto-critique de la procédure suivie

### 2.1 Approche « patchwork »
Nous avons attaqué les écarts un par un, souvent en réponse à un log spécifique, sans vue système. Chaque correction (ex. réalignement d’un plan) re-génère son `self_hash`, mais **aucune orchestration n’assure que ces hashs soient répercutés dans le registre avant la prochaine passe**. Résultat : la pile « document ↔ registre ↔ scripts » reste désynchronisée et retombe en erreur à chaque passage.

### 2.2 Scripts pensés pour le périmètre v1.1, appliqués aux archives v1.0
Les scripts `ssot_*` nécessitent `previous_hash`, `id_root`, etc. Plutôt que de reconnaître que v1.0 n’a jamais été modélisé avec RFC‑004, nous avons tenté d’appliquer la même règle sans plan de succession. Cette confusion de générations explique l’impasse actuelle : tant que les fichiers v1.0 n’auront pas de successeurs v1.1 ou un statut explicite « archived_legacy », la validation restera rouge.

### 2.3 Absence de pipeline de transformation
La chaîne actuelle suit un cycle manuel : modifier le Markdown → relancer les scripts → lire des logs partiels → recommencer. Aucune étape ne garantit que l’ensemble du corpus soit recalculé/référencé en une seule passe. Le manque d’outillage pour :
- scanner les fichiers, proposer les corrections (ID, pattern, previous_hash) et
- appliquer ces corrections via un template unique

fait que chaque auteur improvise sa propre structure. Sans builder declaratif, la dérive est inévitable.

### 2.4 Gouvernance des liens insuffisante
Nous avons corrigé quelques `links.supersedes`, mais nous n’avons pas **documenté ni automatisé** l’algorithme de conversion « path → ID ». Tant que cette règle n’est pas codée dans un outil commun (ex. `scripts/normalize_links.py`), chaque nouveau document risque d’introduire de nouveaux chemins bruts, réintroduisant les mêmes erreurs que celles observées dans `validate_frontmatter_C1H.log`.

## 3. Recommandation globale

### 3.1 Établir une « couche de transition » v1.0 → v1.1
1. **Geler v1.0** : créer un manifest listant toutes les sources v1.0 avec leur hash actuel et un statut `legacy_archive`. On les exclut explicitement des contrôles stricts (`pending_migration` enrichi avec un champ `legacy: true`). Tant que cette lignée n’est pas migrée, le script doit les ignorer.
2. **Succession synthétique** : pour chaque famille v1.0, générer automatiquement un successeur `SPRINT_DOC-1xxx-v1` contenant uniquement le front matter v1.1 + lien vers l’archive. On obtient ainsi les `previous_hash` requis sans toucher à l’original. Cette étape peut être faite via un script unique qui lit le hash réel, crée le successeur et met à jour le registre.

### 3.2 Builder unique pour les front matter
Mettre en place un CLI (`scripts/ssot_transform.py`) capable de :
- relire un document,
- injecter/mettre à jour `id`, `id_root`, `pattern`, `previous_hash`,
- convertir `links.*` en IDs en s’appuyant sur `registry_v1.1.yaml`.

Ce builder devient la **seule façon** de modifier un document normatif, ce qui évite les divergences manuelles.

### 3.3 Pipeline end-to-end
1. **Étape 1 – Transformation déclarative** : builder appliqué sur l’ensemble des racines ciblées (03-architecture, sprints v1.0/v1.1, reports). Il génère un diff structuré (CSV ou JSON) avec chaque champ modifié.
2. **Étape 2 – Registre auto-mis à jour** : script qui lit ce diff et met à jour les lignées concernées, recalcule `self_hash` du registre et ajoute une entrée d’audit.
3. **Étape 3 – Validation stricte** : exécution unique des scripts `ssot_hash_check`, `ssot_schema_check`, `ssot_registry_check` avec le même périmètre. Un seul run doit produire 0 erreur avant merge.

### 3.4 Gouvernance et observabilité
- **Contrôle pré-commit** : hook Git qui refuse toute modification de fichier normatif sans passer par le builder.
- **Rapport quotidien** : pipeline CI qui publie un rapport synthétique (OK / KO par catégorie) pour éviter la dérive silencieuse.
- **Tableau d’avancement** : suivi par lignée (ex. `SPRINT_DOC-0001`), indiquant « migré / en attente / legacy ». Tant que toutes les lignées ne sont pas marquées « migré », on sait que la validation 100 % est impossible.

## 4. Conclusion

Nous échouons parce que nous **traitons les symptômes** (ex. modifier un front matter) sans résoudre les causes systémiques : mix de générations, absence d’outils de transformation, gouvernance des liens inexistante, synchronisation registre incomplète. La solution passe par une approche de migration industrielle : geler v1.0, créer des successeurs synthétiques, automatiser la réécriture des métadonnées et enchaîner transformation + registre + validation dans un pipeline unique. Tant que ces prérequis ne sont pas en place, tenter d’atteindre 100 % de conformité restera un effort Sisyphe. 
