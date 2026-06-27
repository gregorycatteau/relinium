---
name: relinium-evidence-safe-handling
description: Use when a Relinium task involves `ssot-root/evidence_lake`, `ssot-root/personal_vault`, unseal material, or other evidence-like artifacts and you need custody-safe handling. Do not use for ordinary tooling or documentation changes that do not inspect or affect evidence, vault, or protected personal data.
---

# Relinium Evidence Safe Handling

Use this skill for read-only evidence work, custody-sensitive inspection, and protected personal-data handling.

## Protected surfaces

- `ssot-root/evidence_lake`
- `ssot-root/personal_vault`
- `ssot-root/personal_vault/evidence_unseal`

## Apply this workflow

- Start in read-only mode.
- Classify the task as inspection, hashing/metadata review, reporting/documentation of findings, or explicitly requested writable action.
- State whether the artifact is original evidence, unsealed material, vault content, or an analysis derivative.
- If the artifact class or custody status is unclear, stop at inspection and surface the ambiguity before proceeding.
- If custody status cannot be confirmed, treat the artifact as custody-sensitive by default.
- If the task could alter provenance, timestamps, hashes, or custody assumptions, say so before acting.

## Do

- Preserve originals.
- Prefer narrow reads, metadata inspection, and hashing over broader handling when they are sufficient.
- Use path references, fingerprints, hashes, or redacted excerpts instead of copying sensitive contents.
- Distinguish raw facts from interpretation.
- Keep evidence, analysis outputs, and private data clearly separated in the response.

## Do not

- Do not rewrite, normalize, rename, deduplicate, or move evidence automatically.
- Do not mount evidence or images read-write unless the user explicitly requests it and the impact is stated first.
- Do not execute untrusted artifacts from evidence or vault content during casual inspection.
- Do not expose secrets or private data when a redacted reference is enough.
- Do not follow symlinks blindly in custody-sensitive workflows.

## Closing requirement

State clearly whether the work remained read-only or involved a writable action.
