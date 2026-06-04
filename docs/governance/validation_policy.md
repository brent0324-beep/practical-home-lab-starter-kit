# Validation Policy

## Existing Validation

Preserve the existing validation entrypoints:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
```

`scripts/validate.sh` verifies required public files and expected public
content. `scripts/redaction-check.sh` performs high-signal redaction checks for
secret-like patterns.

## Finalization Validation

The repository finalization entrypoint is:

```bash
./scripts/validate_repo_finalization.sh
```

It is read-only and checks:

- governance document presence
- `config/artifact_policy.json` validity
- runtime and private path ignore coverage
- staged private infrastructure data posture
- staged runtime artifact posture
- staged unpublished media posture
- staged generated packaging posture
- ownership

It must not read private notes, local inventories, draft screenshots, generated
packages, or unpublished media contents.

## Required Checks Before Commit Handoff

Run:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
./scripts/validate_repo_finalization.sh
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh scripts/validate_repo_finalization.sh
git diff --check
```

## Release Validation

Before publication or release, also complete manual review using:

```text
docs/publication-checklist.md
docs/release-checklist.md
```

Manual review is required because automated redaction checks cannot reliably
judge screenshots, diagrams, videos, or whether an example looks too real.
