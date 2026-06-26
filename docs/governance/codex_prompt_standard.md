# Codex Prompt Standard

## Purpose

This repository uses YAML as the canonical source format for governed Codex
implementation prompts.

Generated prompts are preferred over manually repeated boilerplate.

## Canonical Roles

- Markdown: human-readable rendered prompts, auditability, and review output
- YAML: canonical prompt specification, template, profile, and task input
- JSON: schemas and validation only

## Required Section Order

Rendered prompts must use this section order:

1. `MODEL RECOMMENDATION`
2. `Repository`
3. `Current Known State`
4. `Goal`
5. `Non-negotiable Constraints`
6. `Agentic Loop Scope`
7. `SMCPP LIFECYCLE`
8. `Builder Scope`
9. `Explicit Non-goals`
10. `Validation`
11. `Release History`
12. `Brent Usefulness Evaluator`
13. `Final Report`
14. `END OF CODEX PROMPT`

## Local Artifacts

- `templates/implementation_prompt.yaml`
- `profiles/governance.yaml`
- `schemas/prompt_schema.json`
- `scripts/render_codex_prompt.py`
- `scripts/validate_prompt_standard.py`

## SMCPP Integration

Rendered prompts must include `## SMCPP LIFECYCLE` when the selected prompt
profile enables SMCPP posture.

For this repository:

```text
SMCPP = governed feature completion into the configured integration branch.
```

The prompt renderer must keep operator approvals explicit and must not treat
prompt text as authorization to push, merge, release, force push, bypass
validation, or mutate secrets or environments.
