---
name: relinium-ssot-change-plan
description: Use when a task proposes or implies a change to Relinium SSOT content, canonical structures, mappings, policies, controlled docs, or other controlled repository data and you need to plan the change safely before editing. Do not use for pure read-only evidence handling or for narrow implementation work already confined to approved write paths and carrying no SSOT or traceability impact.
---

# Relinium SSOT Change Plan

Use this skill before making non-trivial changes that could affect source-of-truth boundaries, derived content, or traceability. This skill is for safe change framing and planning, not for silently transitioning into edits on protected or ambiguous targets.

## Apply this workflow

- Identify the exact target path and classify it as canonical, derived, tooling, analysis, evidence, vault, or protected.
- State whether the requested change is read-only review, narrow edit, wider regeneration, or protected-area change.
- Identify the likely source of truth before editing anything.
- State the downstream surfaces that may be affected: registry, schemas, mappings, docs, analysis artifacts, templates, or derived outputs.
- If the request is ambiguous about source of truth or scope, stop and clarify before editing.
- If the target is protected, evidence-related, or vault-related, stop at planning unless the user explicitly requests that edit.
- Prefer the narrowest safe verification path before broader checks.

## Do

- Prefer the narrowest change that satisfies the request.
- Keep canonical changes explicit and attributable.
- Call out when a requested change actually belongs in canonical content instead of a derived or mirrored file.
- State regeneration scope before any refresh of derived outputs.
- Label verification status explicitly after the work: `not tested`, `statically reviewed`, `partially verified`, or `fully verified`.

## Do not

- Do not make speculative edits to SSOT structures.
- Do not edit derived content first when the canonical source is the correct change point.
- Do not broaden a narrow documentation or tooling task into registry, schema, or evidence changes without saying so first.
- Do not expand write scope beyond the stated target paths unless the scope change is restated explicitly first.
- Do not present a change as low-risk if it touches controlled sources of truth.
- Do not treat completion of the plan as permission to edit protected or ambiguous targets.

## Output pattern

Before editing, give a short plan with:

1. target path
2. content class
3. source of truth
4. downstream impact
5. intended verification scope
