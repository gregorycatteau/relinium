---
name: relinium-write-scope-guard
description: Use when a Relinium task may cross write boundaries, touch protected areas, or expand from a narrow file change into a wider repository operation. Do not use for purely read-only review or when the write scope is already clearly limited to a single safe path and no scope expansion is implied.
---

# Relinium Write Scope Guard

Use this skill to keep repository changes inside the minimum safe writable area.

## Default writable stance

- Default to read-only inspection.
- Unless the user explicitly expands scope, normal writable work stays limited to `ssot-root/analysis`, `ssot-root/tools`, and `ssot-root/ssot_canon/docs`.
- Treat `ssot-root/core` as controlled and impact-sensitive, not as a casual write area.
- Treat `ssot-root/evidence_lake`, `ssot-root/personal_vault`, and `ssot-root/ssot_canon/registry` as protected by default.

## Apply this workflow

- State the minimum directory scope required for the task.
- Distinguish where the edit will occur from what the edit may impact, and scope both explicitly before editing.
- List any path outside the default writable scope before editing it.
- If `ssot-root/core` is involved, explain why the task genuinely targets schemas, validation, or core contract logic.
- If a protected area is implicated, stop and require explicit user intent before editing.

## Do

- Keep edits in the smallest practical subtree.
- Say when the task is moving from docs to data, tooling to canonical content, or analysis to protected material.
- Call out write-scope expansion before requesting approval or making edits.

## Do not

- Do not operate outside the minimum required directory scope.
- Do not treat a trusted repository as permission to expand write scope silently.
- Do not let a review or audit task drift into implementation across multiple zones without saying so.
- Do not touch protected areas because they appear nearby or structurally related.
