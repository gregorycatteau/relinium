---
name: relinium-core-impact-review
description: Use when a Relinium task touches or reviews `ssot-root/core`, schema files, validation rules, or core contracts and you need an impact-focused review before editing or approving the change. Do not use for evidence handling, generic docs work, or narrow analysis-output tasks that do not affect core schemas, validation, or contract logic.
---

# Relinium Core Impact Review

Use this skill when `ssot-root/core` is in scope. The goal is to review impact before implementation or approval, not to silently implement core edits.

## Review focus

- Identify whether the target is a schema definition, validation rule, contract mapping, canonical structure, or another core contract surface.
- State why `ssot-root/core` must be touched instead of a documentation, tooling, or analysis path.
- Check whether the requested change affects canonical structure, validation semantics, data shape, invariants, or downstream compatibility.
- Check whether related files in `core/schema` or `core/validation` are likely to need synchronized review.
- If the contract boundary or downstream impact is unclear, stop at inspection and surface the ambiguity before editing.

## Do

- Review the narrowest relevant files first.
- Call out compatibility, invariants, traceability, regeneration impact, and dependent structures.
- Distinguish between direct contract changes and documentation-only clarifications.
- If review shows the requested change belongs outside `ssot-root/core`, stop and reroute to the correct canonical or writable surface before editing.
- Recommend the smallest safe verification path before broader checks.

## Do not

- Do not treat `ssot-root/core` as routine implementation territory.
- Do not silently change core schemas or validation rules during a review-only task.
- Do not assume a local edit is isolated if it changes document shape, analysis request/result shape, registry assumptions, event semantics, or dependent validation logic.
- Do not claim safety without explaining the impact surface.

## Minimum output

Report:

1. touched core surface
2. contract impact
3. likely downstream consumers, mirrors, or dependent structures
4. minimum safe verification path
