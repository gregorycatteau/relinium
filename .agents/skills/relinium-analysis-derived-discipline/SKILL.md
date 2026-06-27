---
name: relinium-analysis-derived-discipline
description: Use when a Relinium task creates, edits, reviews, or regenerates analysis requests, patterns, scripts, results, or other derived outputs under `ssot-root/analysis`, or when a task may refresh derived artifacts from canonical sources. Do not use for core-schema review, protected evidence handling, or broad repository planning not centered on analysis assets or derived content.
---

# Relinium Analysis and Derived Discipline

Use this skill when handling non-canonical analysis assets or derived outputs whose traceability must be preserved.

## Working surfaces

- `ssot-root/analysis`
- Analysis areas such as requests, patterns, scripts, and results

## Apply this workflow

- Classify the task as request authoring, pattern update, script change, result generation, or review of derived artifacts.
- Keep requests, patterns, scripts, and results logically separated.
- Identify whether the task changes a canonical input, a reusable analysis asset, or a derived output.
- If the canonical source is unclear, stop at inspection and surface the ambiguity before editing.
- If the task may trigger refresh of existing outputs, state the regeneration scope before proceeding.

## Do

- Prefer new result artifacts over overwriting prior results when traceability matters.
- Keep derived artifacts attributable to a specific request, source, pattern, or analysis change.
- Keep result generation narrow and attributable to a specific request or pattern change.
- When replacement is explicitly requested, record which prior result is being superseded and keep lineage explicit in the response.
- Review canonical inputs before changing derived artifacts that depend on them.
- Use the narrowest safe verification path before broader checks.
- Label the final verification status explicitly: `not tested`, `statically reviewed`, `partially verified`, or `fully verified`.

## Do not

- Do not overwrite prior analysis outputs unless the user explicitly asks for replacement.
- Do not perform broad regeneration, refresh, or re-export of derived content unless the user explicitly requests that wider regeneration scope.
- Do not blur raw evidence facts, analysis outputs, and interpretive conclusions.
- Do not treat a result artifact as a source of truth when the canonical source lives elsewhere.
- Do not silently switch from review of derived artifacts into rewriting outputs unless the user asks for changes.
