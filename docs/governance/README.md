# Practical Home Lab Governance

## Purpose

This directory contains normalized governance for the Practical Home Lab Starter
Kit. It complements the existing public-facing security, contribution,
publication, release, and redaction documents without replacing them.

## Governance Hierarchy

Apply guidance in this order:

1. `AGENTS.md`
2. `SECURITY.md`
3. `CONTRIBUTING.md`
4. `docs/sanitized-example-policy.md`
5. `docs/publication-checklist.md`
6. `docs/release-checklist.md`
7. `docs/governance/*.md`
8. documented repository-local maintainer workflows, when applicable
9. task-specific user instructions

If guidance conflicts, preserve the stricter public safety, redaction,
repository-boundary, secret-handling, ownership, and no-force-push rule.

## Document Map

- `security.md`: public-repo security and infrastructure disclosure posture.
- `secret_handling.md`: credentials, keys, PSKs, tokens, and private detail
  handling.
- `artifact_policy.md`: source, public assets, runtime, private, and packaging
  artifact classes.
- `runtime_data_policy.md`: local-only media, screenshots, inventories, Ansible
  output, and unpublished content handling.
- `git_workflow.md`: commit, staging, release, and no-force-push rules.
- `validation_policy.md`: validation, redaction, finalization, and release
  review expectations.

## Normalization Order

Use this order for future governance work:

1. governance docs and artifact policy
2. `.gitignore` coverage
3. validation and redaction checks
4. pre-commit and Gitleaks configuration
5. CI workflow

Automation must not inspect or publish local private notes, sensitive
environment files, draft media, screenshot staging areas, or generated
packaging artifacts.
