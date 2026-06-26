# Validation Policy

## Existing Validation

Preserve the existing validation entrypoints:

```bash
./scripts/session
./scripts/validate.sh
./scripts/redaction-check.sh
```

`scripts/validate.sh` verifies required public files and expected public
content. `scripts/redaction-check.sh` performs high-signal redaction checks for
secret-like patterns. `scripts/session` is the maintainer-facing Governance v2
Lite engineering-session entrypoint that renders bootstrap context, generates
repository/session artifacts, verifies prompt rendering, and checks the
migration bundle.

## Finalization Validation

The repository finalization entrypoint is:

```bash
./scripts/validate_repo_finalization.sh
```

It is read-only and checks:

- governance document presence
- `config/artifact_policy.json` validity
- runtime and private path ignore coverage
- staged sensitive environment data posture
- staged runtime artifact posture
- staged unpublished media posture
- staged generated packaging posture
- ignore coverage for generated engineering-session artifacts
- ownership

It must not read private notes, local inventories, draft screenshots, generated
packages, or unpublished media contents.

## Required Checks Before Commit Handoff

Run:

```bash
./scripts/session
./scripts/validate.sh
./scripts/redaction-check.sh
./scripts/validate_repo_finalization.sh
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh scripts/validate_repo_finalization.sh
git diff --check
```

## Pre-Commit Checks

After repo-level `.pre-commit-config.yaml` and `.gitleaks.toml` are present,
local source hygiene can be checked with:

```bash
pre-commit install
pre-commit run --all-files
```

The Gitleaks hook requires `gitleaks` on `PATH` and must use redacted output.
Pre-commit checks must not scan ignored draft media, screenshots, local
inventories, private notes, packaging scratch files, or unpublished artifacts as
source.

## Release Validation

Before publication or release, also complete manual review using:

```text
docs/publication-checklist.md
docs/release-checklist.md
```

Manual review is required because automated redaction checks cannot reliably
judge screenshots, diagrams, videos, or whether an example looks too real.
