---
id: "EXPLORE-SSOT-V1_1-100PCT-0001"
id_root: "EXPLORE-SSOT-V1_1-100PCT-0001"
version: "v1"
type: "analysis"
status: "Active"
title: "Exploration structurelle vers un SSOT 100% prouvable – SSOT v1.1"
scope: "organizational"
pattern: "exploration"
decision_type: "assessment"
created_at: "2025-11-06T10:36:40Z"
authors:
  - id: "cline"
    role: "explorer"
roles:
  - name: "Explorer"
    actor: "Cline"
links:
  relates_to:
    - "VAL-SSOT-V1_1-0001"
    - "SELFCRIT-SSOT-V1_1-0001"
    - "MIRROR-SSOT-V1_1-0001"
    - "TRUTH-SSOT-V1_1-0001"
  evidence:
    - "reports/validation/SSOT_V1_1_VALIDATION_CODEX.md"
    - "reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE.md"
    - "reports/validation/SSOT_V1_1_MIRROR_CODEX.md"
    - "reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT.md"
self_hash: sha256:afaaedfb62a149726c1765519c6f1839af38c4d06afda26034cb0d53bf4a5277
---

# Exploration structurelle vers un SSOT 100% prouvable – SSOT v1.1

## 1. Contexte et objectif

- Truth Index Global actuel (mesuré par TruthKeeper): 0.56 (intervalle observé 0.56–0.62, valeur consolidée ~0.60).
  - Codex (global): 0.46
  - Cline (corrigé): 0.48
  - Miroir Codex (indice de véracité): 0.62
- Enseignements clés consolidés (Codex + Cline + Miroir + TruthKeeper):
  - Discipline partielle: séquence de hash non verrouillée, placeholders laissés en production, pas de re-vérification “après écriture”.
  - Registre incomplet: lignées manquantes (RFC-004, OBS-*), métadonnées partielles (hash/statut).
  - Preuves solides localement (non-modification des originaux) mais non routinisées (manifest snapshot obsolète, auto-référence non résolue).
  - Biais linguistique: qualificatifs absolus ou “acceptable pour un pilote” sans métrique.

Question centrale: Quelles transformations structurelles (registre, scripts, CI, schéma, gouvernance) rendraient toute contestation externe mathématiquement réfutable et permettraient d’atteindre un Truth Index arbitrairement proche de 1.0, vérifiable par tout auditeur outillé ou humain ?

## 2. Définition d’un SSOT “100% prouvable” (invariants vérifiables)

Invariants de registre
- R-1 Couverture totale: 100% des documents normatifs (ADR, RFC, OBS, SPRINT_DOC) présents dans `docs/_registry/registry_v1.1.yaml` avec (id_root, versions[].id, status, version, date, file_path, hash).
  - Test auditeur (algo): comparer inventaire `docs/03-architecture/**/*.{md,yaml}` + `docs/observatory/*.md` + `docs/sprints/**` à `registry_v1.1.yaml` et signaler tout document normatif non référencé ou sans hash/statut.
  - Commande indicative: `rg -n "^(id:|type:|status:)" docs/03-architecture | awk '{print $1}' | sort` vs. entrée YAML parsée.

- R-2 Lignées complètes: aucune lignée orpheline (chaque `id_root` pointe vers au moins une version et toute version v2+ déclare `previous_hash` + `links.supersedes` cohérents).
  - Test auditeur: pour chaque version v2+, recalculer le SHA256 du fichier supplanté et comparer à `previous_hash`. Vérifier que `id_root` reste constant.
  - Script (pseudo): parse registry → for v2+: sha256(file_superseded) == previous_hash.

Invariants cryptographiques
- C-1 Zéro mismatch: 0 divergence entre les hashes consignés (registre/manifest/hash files) et les recalculs réels au commit de référence.
  - Test: `sha256sum $(yq '.lineages[].versions[].file_path' -r docs/_registry/registry_v1.1.yaml)` et comparer aux valeurs YAML.

- C-2 Zéro placeholder: aucun `sha256:(to_be_calculated)` dans tout artefact de preuve d’un sprint marqué Terminé/Certifié (manifest, progress, hashes).
  - Test: `rg -n "to_be_calculated" docs/sprints/SSOT-v1.1/03-validation && exit 1`.

- C-3 Auto-référence résolue: toute ressource qui se signe elle-même est soit:
  - (A) exclue de son propre hashing (champ `self_hash` ignoré au calcul), soit
  - (B) signée via un mécanisme externe (signature GPG/Keyless) et ne déclare pas `self_hash` comme empreinte.
  - Test: pipeline de vérification dédié (cf. §4 Bloc B).

Invariants CI/CD
- P-1 Vérification systématique: toute modification d’un document SSOT déclenche auto-vérif (hash-check, schema-check, registry-coverage).
  - Test: logs CI obligatoires, “required checks” sur la branche par défaut.

- P-2 Merge gate: aucun merge possible si l’une des vérifications échoue.
  - Test: configuration “branch protection” + statut CI rouge bloque merge.

Invariants de langage (sémantique)
- L-1 Zéro superlatif non prouvable: termes comme “acceptable”, “correct”, “garanti/guaranteed” interdits sans métrique jointe (référence à score, hash, registre, test).
  - Test: linter sémantique (regex + exceptions marquées) exécuté en CI.

- L-2 DoD factuelle: aucune DoD marquée ✅ sans preuve liée dans `links.evidence` et hash vérifiable.
  - Test: linter DoD, et “policy test”: si `to_be_calculated` détecté, DoD=❌.

Note de vérification “self_hash”
- Par convention vérifiable, le `self_hash` d’un fichier “document” est calculé sur le contenu complet en excluant la ligne `self_hash:` (résolution d’auto-référence). La preuve et la commande sont fournies en §4 (Bloc B).

## 3. Cartographie des écarts actuels (source croisée Codex • Cline • Miroir • TruthKeeper)

Axe Structure / Registre
- GAP-REGISTRY-0001 (Critique) — Source: Codex
  - RFC-004 absente de `registry_v1.1.yaml` bien qu’existante (docs/03-architecture/rfcs/RFC-004-alignment-protocol.md).
  - Impact: invisibilité du protocole fondateur → auditeur ne peut pas tracer la norme elle-même.

- GAP-REGISTRY-0002 (Élevée) — Source: Codex, Self-critique
  - OBS-0001/0002/0003 listés en pending_migration sans hash/statut.
  - Impact: pas de preuve d’intégrité ni de statut → couverture et traçabilité incomplètes.

- GAP-ID-0001 (Moyenne-Élevée) — Source: Codex, Self-critique
  - Incohérence nominale RFC-001 vs RFC-0001 (id_root vs id original).
  - Impact: lignée rompue aux yeux d’un outil → intervention humaine requise.

Axe Cryptographique
- GAP-HASH-0001 (Critique) — Source: Codex
  - Mismatch de hashs dans le snapshot manifest (progress, hashes) et self-hash du manifest faux.
  - Impact: manifest inutilisable comme preuve.

- GAP-HASH-0002 (Élevée) — Source: Codex, Self-critique
  - Placeholders `to_be_calculated` dans `SSOT_V1_1_HASHES.yaml`.
  - Impact: DoD “hashs consignés” déclarée mais non démontrable.

Axe Process/CI
- GAP-CI-0001 (Élevée) — Source: Mirror, TruthKeeper
  - Absence de “hash-after-final” et de re-vérification post-écriture, pas de gate CI.
  - Impact: dérive entre déclaration et réalité non empêchée.

Axe Langage/DoD
- GAP-LANG-0001 (Moyenne) — Source: Mirror
  - Qualificatifs absolus sans preuve (“Immutabilité: GUARANTEED”) et usage d’“acceptable pour un pilote”.
  - Impact: augmente le risque de divergence perçue vs mesurée.

## 4. Propositions de modifications structurelles (carte des transformations)

Bloc A — Registre & lignées
- A1 Étendre `registry_v1.1.yaml` à 100% des documents normatifs (ajout RFC-004, complétion OBS-0001/2/3 avec hash + statut).
  - Type: registre
  - Axes améliorés: cohérence_inter_agents, maturité_preuve
  - Effet estimé sur Truth Index: +0.05 global (Registre +0.10)
  - Vérification auditeur:
    - Script “coverage”: lister (docs/**/*) normatifs vs `registry_v1.1.yaml` → 0 manquants
    - Commande: `python -c '...'` (check YAML vs FS), ou `rg` + `yq` + diff.

- A2 Normaliser la lignée RFC: décider si `id_root` = RFC-001 (hérite du legacy) ou migrer l’original vers RFC-0001, puis aligner registre + front matters.
  - Type: ADR (décision de normalisation) + registre
  - Axes: structure, documentaire
  - Effet: +0.02 global (Structure +0.05)
  - Vérification: requête sur registre → `id_root` unique et stable, test de traversée de lignée passe à 100%.

Bloc B — Cryptographie & preuve
- B1 Standard “self_hash-excluding-self”: calculer l’empreinte de chaque document en excluant la ligne `self_hash:` (résolution d’auto-référence).
  - Type: script + convention
  - Axes: maturité_preuve, discipline_documentaire
  - Effet: +0.03 global
  - Vérification (procédure reproductible):
    - `sed '/^self_hash:/d' TARGET | sha256sum | awk '{print "sha256:"$1}'`
    - Comparer au `self_hash` déclaré; 0 mismatch attendu.

- B2 “Hash-after-final”: règle et script qui recalculent tous les hashs après la dernière modification, puis comparent aux valeurs consignées (manifest/registry/hash files).
  - Type: script + CI
  - Axes: discipline, maturité_preuve
  - Effet: +0.04 global (Cryptographie +0.07)
  - Vérification: CI échoue si un seul mismatch; logs CI exportables.

Bloc C — CI/CD & outils
- C1 Job CI “triple-check”: hash-check + registry-coverage + schema-check (v1.0 & v1.1).
  - Type: CI
  - Axes: discipline, cohérence_inter_agents
  - Effet: +0.07 global
  - Vérification: protection de branche; preuve = impossibilité de merge avec check rouge.

- C2 Linter ID/front matter/langage:
  - ID: bloquer `RFC-001` vs `RFC-0001` incohérent.
  - Front matter: refuser DoD ✅ sans `links.evidence` et hash présent.
  - Langage: refuser superlatifs non liés à métriques (liste blanche/regex).
  - Type: linter + CI
  - Effet: +0.03 global
  - Vérification: logs CI + règle linter publiées; exécution locale reproductible.

Bloc D — Gouvernance & ADR comportementale
- D1 ADR “Relinium Behavioral Framework v2”:
  - Règle “preuve avant déclaration” (aucun ✅ sans hash + registre à jour).
  - Rôle explicite des agents (Codex, TruthKeeper, Cline) et indépendance des validations.
  - Classification des divergences (critique/élevée/moyenne/faible) et trajectoires de remédiation.
  - Seuils d’états du Truth Index (Emergent <0.5, Stabilising 0.5–0.7, Reliable 0.7–0.9, Verified ≥0.9).
  - Type: ADR
  - Axes: transparence_linguistique, discipline, cohérence_inter_agents
  - Effet: +0.03 global
  - Vérification: présence de l’ADR, application mesurée via CI (règles alignées sur ADR).

## 5. Scénarios de trajectoire vers ~1.0

Scénario 1 — Rigorous Discipline First
- Ordre: C (CI) → B (Crypto) → A (Registre) → D (Gouv)
- Objectif: réduire à zéro les divergences factuelles rapidement (gate CI + triple-check).
- Risques: friction courte durée (merge bloqués), besoin d’industrialiser les scripts.
- Dépendances: disponibilité d’un runner CI et de scripts reproductibles.
- Condition de succès:
  - Truth Index ≥0.85 en 2 itérations (Discipline ≥0.80; Cryptographie ≥0.85).
  - 0 placeholders; 0 mismatch; couverture registre ≥0.95.
  - Preuve: dashboards CI + rapport d’audit automatique vert.

Scénario 2 — Proof-Led Expansion
- Ordre: A (Registre) → B (Crypto) → C (CI) → D (Gouv)
- Objectif: étendre d’abord l’espace de preuve (registre exhaustif), puis automatiser.
- Risques: période transitoire avec preuves plus larges mais non encore “gated”.
- Dépendances: qualification de l’inventaire documentaire complet.
- Condition de succès:
  - Truth Index ≥0.80 initial (Registre ≥0.75, Crypto ≥0.75), puis ≥0.90 après CI.
  - Preuve: différence couverture (avant/après) + 0 mismatch post-automation.

## 6. Synthèse & recommandations

Top 5 modifications critiques
1) CI “triple-check” bloquante (hash/registry/schema) — ferme la porte aux divergences (effet immédiat mesurable).
2) Résoudre l’auto-référence (self_hash-excluding-self) — rend les manifests auto-vérifiables.
3) Compléter `registry_v1.1.yaml` (incl. RFC-004, OBS avec hash/statut) — base de vérité exhaustive.
4) Linter ID/front matter/langage — supprime la dette sémantique et les DoD subjectives.
5) ADR de gouvernance comportementale — verrouille la culture “preuve avant déclaration”.

Blocages actuels vers 1.0
- Absence de gate CI, registres incomplets, et sémantique non-contrainte → la réalité peut diverger sans alerte.

Ce qui rendrait toute contestation réfutable
- Registre exhaustif + 0 mismatch + CI bloquante + linter sémantique + convention de hash reproductible.
- Un auditeur externe peut:
  - Rejouer les scripts, reproduire les hashes, constater la couverture et vérifier la politique de merge.
  - Prouver que tout écart est bloqué avant intégration.

---

Annexe — Procédure de vérification “self_hash” (exclusion de `self_hash:`)
- Règle: le `self_hash` est calculé sur le contenu du fichier moins la ligne `self_hash:` (pour éviter la boucle).
- Commande de référence:
```
sed '/^self_hash:/d' PATH/TO/FILE | sha256sum | awk '{print "sha256:"$1}'
```
- Conformité: la valeur obtenue doit égaler le `self_hash` déclaré.

Annexe — Triple-check CI (pseudo YAML)
```
jobs:
  docs-ssot-verify:
    steps:
      - run: pip install -r requirements.txt  # yq/pyyaml/jsonschema/rg
      - run: python scripts/validate_frontmatter.py  # v1.0 et v1.1
      - run: python scripts/audit_verify_hashes.py --mode v1_1  # étendre
      - run: python scripts/generate_registry.py --check-coverage
      - run: rg -n "to_be_calculated" docs/sprints/SSOT-v1.1/03-validation && exit 1 || true
