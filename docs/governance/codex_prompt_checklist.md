# Codex Prompt Checklist

Use this checklist when reviewing prompt-rendering changes.

## Required Assets

- `templates/implementation_prompt.yaml`
- `profiles/governance.yaml`
- `schemas/prompt_schema.json`
- `scripts/render_codex_prompt.py`
- `scripts/validate_prompt_standard.py`
- `templates/task_prompt_spec.example.yaml`

## Required Prompt Properties

- `END OF CODEX PROMPT` is the final line.
- `Brent Usefulness Evaluator` is present.
- `## SMCPP LIFECYCLE` is rendered when SMCPP is enabled.
- Generated prompts are preferred over manually repeated boilerplate.
- Public-safe wording is preserved throughout the rendered prompt.

## Review Questions

- Does the prompt stay repository-local and contributor-friendly?
- Does the prompt avoid internal paths, sensitive environment details, and
  secret-like content?
- Does the prompt keep SMCPP lifecycle gates explicit?
