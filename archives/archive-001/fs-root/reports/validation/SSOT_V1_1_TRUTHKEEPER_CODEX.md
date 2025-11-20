---
id: SPRINT_DOC-0060-CODEX
id_root: SPRINT_DOC-0060
version: "1.3"
type: SPRINT_DOC
status: Active
date: 2025-11-07
scope: organizational
pattern: validation
title: SSOT Truthkeeper — Codex Validation Report
authors:
  - id: codex
    role: verifier
roles:
  - name: Verifier
    actor: Codex
links:
  relates_to:
    - reports/truthkeeper/truthkeeper_manifest.json
    - reports/truthkeeper/truthkeeper_bundle_2025-v1.tar.gz
    - docs/_registry/registry_v1.1_v6.yaml
previous_hash: sha256:3f1f63f9c5351a5e119ab117a422ff2c5f56e9f8ffe19639184817713aaad34a
---
# Truthkeeper – Rapport Codex

Ce rapport atteste la conformité mathématique du « Proof Bundle » et la cohérence de la chaîne de registres v1 → v6 (phase S10).

## Résumé

- Bundle: `reports/truthkeeper/truthkeeper_bundle_2025-v1.tar.gz`
- SHA256(bundle): `sha256:f29e8bc0476614093b65fd8f44b8dbd6cddce9a699e1a3ee19c176777d0e51b1`
- Manifest: `reports/truthkeeper/truthkeeper_manifest.json`
- Snapshot: `reports/truthkeeper/SSOT_V1_1_TRUTHKEEPER_SNAPSHOT.yaml`
- Registre v6: `docs/_registry/registry_v1.1_v6.yaml`

## Commandes exécutées (triple-check strict global)

```bash
python scripts/ssot_registry_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v6.yaml
python scripts/ssot_hash_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v6.yaml
python scripts/ssot_schema_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v6.yaml
```

Résultat: code de sortie global = 0 (OK).

## Vérifications

1) previous_hash(v6) = SHA256(v5) — conforme  
2) self_hash(v6) reproduit (calcul v1.1) — conforme  
3) Tous les SHA256 du `truthkeeper_manifest.json` vérifiés — conformes  
4) Signature SHA256 du bundle = somme attendue — conforme  
5) Reproductibilité: commandes et workflow `.github/workflows/ssot-proof.yml` rejouables — conforme

## Scores

| Axe | Score | Commentaire |
|------|-------|-------------|
| proof_chain_integrity | 1.00 | previous/self_hash exacts |
| coverage_snapshot | 1.00 | registres + validations inclus |
| bundle_consistency | 1.00 | hashes internes concordants |
| ci_gate_strict_global | 1.00 | code 0 confirmé |
| audit_reproducibility | 1.00 | commandes et hashes rejouables |

Verdict final: ✅ Truthkeeper Certified – SSOT Relinium 100 % Audit-Proof.
