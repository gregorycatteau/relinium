# Relinium AGENTS.md

This file defines repository-specific operating rules for work inside `relinium`.
It adds constraints to the global `~/.codex/AGENTS.md`.
If a rule here conflicts with the global file, follow the stricter rule.

## Repository posture

- Treat this repository as security-sensitive and traceability-sensitive by default.
- Preserve SSOT integrity over convenience.
- Keep changes minimal, reviewable, and attributable.
- Keep source truth, evidence, analysis artifacts, and operational tooling clearly separated.

## Repository boundaries

- The main working domain is `ssot-root`.
- Do not assume files outside `ssot-root` are in scope unless the user explicitly expands scope.
- Operate only in the minimum required directory subtree for the task.

## Write zones

- Default to read-only inspection.
- Unless the user explicitly expands scope, normal writable work must stay limited to `ssot-root/analysis`, `ssot-root/tools`, and `ssot-root/ssot_canon/docs`.
- `ssot-root/core` is controlled and impact-sensitive. Edit it only when the task directly targets schemas, validation, or core contract logic, and state the impact first.
- Do not treat `ssot-root/core` as a casual general-purpose write area.
- Treat `ssot-root/evidence_lake`, `ssot-root/personal_vault`, and `ssot-root/ssot_canon/registry` as protected by default.
- Do not modify protected areas unless the user explicitly requests that exact change and the impact is stated first.

## SSOT discipline

- Treat canonical definitions, registries, schemas, and mappings as controlled sources of truth.
- Do not make speculative edits to SSOT structures.
- Do not edit derived, mirrored, exported, or generated content before checking whether the canonical source should be changed instead.
- When a change affects traceability, state the source of truth, downstream impact, and regeneration scope before editing.

## Evidence and custody

- Treat evidence, vault content, sealed or unsealed material, and analyst outputs as distinct classes of data.
- Preserve originals by default.
- Do not rewrite, normalize, rename, deduplicate, or move evidence automatically.
- Do not mount evidence or images read-write unless the user explicitly requests it and the impact is stated first.
- If an action could alter provenance, timestamps, hashes, or custody assumptions, state that before acting.

## Analysis outputs

- Keep requests, scripts, patterns, and results logically separated.
- Do not overwrite prior analysis outputs unless the user explicitly asks for replacement.
- Prefer creating new result artifacts over mutating prior findings when traceability matters.
- Do not perform broad regeneration, refresh, or re-export of derived content unless the user explicitly requests that wider regeneration scope.
- Distinguish raw evidence facts, analysis outputs, and interpretive conclusions in all reporting.

## Secrets and private data

- Treat `personal_vault`, auth artifacts, tokens, cookies, keys, user data, and private identifiers as highly sensitive.
- Do not print or copy sensitive values when a path, fingerprint, or redacted reference is enough.
- Do not move sensitive data into less protected areas of the repository.
- Do not include sensitive values in patches, commit messages, summaries, or logs.

## Review, audit, and forensics modes

- In review mode, report findings first. Do not silently switch into implementation unless the user asks for changes.
- In audit mode, prioritize integrity, provenance, data flow, access boundaries, and regression risk.
- In forensic mode, stay read-only unless the user explicitly requests a writable action.
- Do not execute untrusted artifacts from evidence, vault, or imported datasets as part of casual inspection.

## Verification expectations

- Do not claim repository changes are verified unless verification was actually performed.
- Label outcomes explicitly as `not tested`, `statically reviewed`, `partially verified`, or `fully verified`.
- Prefer the narrowest safe verification path before broader checks.
- If a change touches SSOT or protected data structures, run the narrowest relevant consistency checks available.
- If no safe verification path exists, say so plainly.

## Multi-agent rules

- Only one agent may hold write ownership for a given file set unless coordination is explicit.
- Review-oriented agents must not silently implement.
- Use separate agents only for clearly separated scopes such as review, schema inspection, analysis tooling, or documentation updates.
- Do not split overlapping custody-sensitive areas across agents.

## Expected change discipline

- Explain non-trivial edits before making them.
- Use the smallest effective patch.
- Do not broaden scope from docs to data, from tooling to evidence, or from analysis to canonical state without saying so explicitly.
- When in doubt, stop at inspection and ask for confirmation before touching protected areas.
