---
id: "ALIGN-VALIDATION-SSOT-V1_1-PHASE1"
id_root: "ALIGN-VALIDATION-SSOT-V1_1-PHASE1"
version: "1.0"
type: "SPRINT_DOC"
status: "Active"
title: "SSOT v1.1 — Align Validation Phase 1 (S9-ALIGN)"
date: "2025-11-06"
scope: "organizational"
pattern: "observation"
created_at: "2025-11-06T19:05:00Z"
authors:
  - id: "cline"
    role: "author"
roles:
  - name: "Author"
    actor: "Cline"
links:
  cites:
    - "docs/_registry/registry_v1.1_v2.yaml"
    - "docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES-v2.yaml"
    - "docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846-v2.yaml"

self_hash: sha256:cf1eaf1473a352d1bfda125655e9c208409ebd94dab856f70eb33de72cec2b18
---

# SSOT v1.1 — Align Validation Phase 1 (S9-ALIGN)

Ce rapport documente la création et la certification cryptographique des 11 successeurs (-v2) des fichiers critiques (catégories A, B, E) afin d’obtenir un pipeline strict vert sur le périmètre des hashs et manifests.

## Tableau de succession certifiée

Colonnes:
- Original: chemin du prédécesseur
- Successeur: chemin du -v2
- previous_hash: SHA256(prédécesseur), inscrit dans le successeur
- self_hash: auto-hash du successeur (exclusion de la ligne self_hash pour Markdown/YAML front matter v1.1)
- Statut: Active/Superseded selon le registre v1.1_v2

| Original | Successeur | previous_hash | self_hash | Statut |
|---|---|---:|---:|---|
| docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_PROOF_EVIDENCE.md | docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_PROOF_EVIDENCE-v2.md | sha256:5aa74d858fd8c4ed106d6c977317b6a278d15ea5a372fd05f20e22bc656b67ca | sha256:53bd2f7a4db1de371b6c2cd5091e4b13d2d780367e6c40191f25edd1db0d7b07 | Active |
| docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_STRICT_PLAN.md | docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_STRICT_PLAN-v2.md | sha256:c4ba98862451c4b79799ce3d22a0da78c926eefa6e3abbe9fe454a4b50147133 | sha256:eadaea0193f3480c05c50bf1f13d4b00a83304bfe850cd401002e08d3ef888d6 | Active |
| reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT.md | reports/analysis/SSOT_V1_1_TRUTHKEEPER_REPORT-v2.md | sha256:755de2828188d1fdc15020b499d55a33d7608ddd744bb0dbaf46a71054517524 | sha256:5dad0cbefb9810c3ba2e0a5ba9e6587123f374491933165a629683326c93ed8f | Active |
| reports/analysis/SSOT_V1_1_100PCT_EXPLORATION.md | reports/analysis/SSOT_V1_1_100PCT_EXPLORATION-v2.md | sha256:f7083ac304c720d0487e5836f9305e7eeeb59f90f1efdace8f0253df1c7ef0bb | sha256:1516ebda4edd10d41e811c88ade5888a9a7496091e9fda57b0004c0919cf72ec | Active |
| reports/validation/SSOT_V1_1_VALIDATION_CODEX.md | reports/validation/SSOT_V1_1_VALIDATION_CODEX-v2.md | sha256:3cabcc27ab3e4563652d8c1b74e982f90cf6e1440465f38f83fb6e2938819056 | sha256:ee77c82bcb139cca7db6f10e7ce868354e92a39f2ab2d9439c66ba147c63a5ef | Active |
| reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE.md | reports/validation/SSOT_V1_1_SELFCRITIQUE_CLINE-v2.md | sha256:e45168f7726e11d44492936fc6542f3a6b0c84a3c4392192144b7d3757e119f0 | sha256:fd53ea61204a57af04cf48494bbec207be8eb126889ea2c7a3186cc1bd6f6f63 | Active |
| reports/validation/SSOT_V1_1_MIRROR_CODEX.md | reports/validation/SSOT_V1_1_MIRROR_CODEX-v2.md | sha256:143a17a04cfc6f5147baa2509dfca436de3525a595708367380bb38752221efe | sha256:55a0e961aaa5f4eb7e6818cf19c39ac3fef6843f852b5a44881163979ae2f032 | Active |
| docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PILOT_PLAN.md | docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_PILOT_PLAN-v2.md | sha256:4635b67272f12f993a22aef7b513afc3d11dcee6776d2cf4ddc7bd14340e4c25 | sha256:672151768f0a7a93dab1268f9acd1472844df0e0d1450cc05f87e1b0e83e2343 | Active |
| docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS.yaml | docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_PROGRESS-v2.yaml | sha256:42a1e5b0879e867b0f21de1730b88bb47641a036258322ff7bde4b0f750a4f8f | sha256:17f996bcf317f930e294ad9829d7277f8e82bec83b0eb6a25df7b9c60a8a42d8 | Active |
| docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml | docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES-v2.yaml | sha256:0644fd047415845d64539397b466ef96a95e1e40a6240b3e178190d1b67cda26 | sha256:42737fdade8d06f3beffdd6c51c4c874d37001db5a15cdda702aa25309c97ea9 | Active |
| docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846.yaml | docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846-v2.yaml | sha256:477ba35f179888361a010a1623cb5a943cde75cadc27441c8796fddb5a634173 | sha256:68f402544aea7092e71f56cc848ad697e64b34e87542e1cf93d1e52a3051f907 | Active |

## Triple-check

- H-1 self_hash: Validé (v2) — méthode d’exclusion appliquée (front matter v1.1)
- H-2 previous_hash: OK — égal au SHA256 du prédécesseur
- H-3 placeholders: Aucun dans HASHES-v2 et MANIFEST-v2
- R-1 registre: registry_v1.1_v2.yaml à jour (v2 Active, anciens Superseded)
- V-1 pipeline strict: OK sur le périmètre ciblé (hashes + manifests)

## Références

- Registre v1.1_v2: docs/_registry/registry_v1.1_v2.yaml
- Manifeste des hashs v2: docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES-v2.yaml
- Manifest snapshot v2: docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_SNAPSHOT_MANIFEST_20251106_0846-v2.yaml
