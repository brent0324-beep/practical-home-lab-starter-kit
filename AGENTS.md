# Practical Home Lab Starter Kit Agent Guide

## Repository Scope

This repository is a public-facing educational starter kit for network
engineers building sanitized home lab workflows.

Work must stay scoped to:

```text
/opt/products/practical-home-lab-starter-kit
```

Do not modify other repositories, live infrastructure, system configuration,
firewall rules, SSH settings, packages, services, Docker state, or host runtime
state.

## Public Repository Posture

Preserve the repository as beginner-friendly, educational, reference-focused,
and publicly consumable.

The repository must not contain:

- real infrastructure details
- customer environments
- employer information
- production credentials
- VPN keys or PSKs
- SSH private keys
- API tokens
- serial numbers
- public IPs associated with real infrastructure
- screenshots containing sensitive information
- unpublished personal notes or local-only artifacts

Examples must remain sanitized and use placeholders, private lab ranges, generic
hostnames, and generic usernames.

## Governance References

Repository-specific governance lives under:

```text
docs/governance/
```

Existing public safety documents remain first-class controls:

```text
SECURITY.md
CONTRIBUTING.md
docs/sanitized-example-policy.md
docs/publication-checklist.md
docs/release-checklist.md
docs/repo-boundary-policy.md
```

Shared workstation governance is referenced from:

```text
/opt/codex-standards/docs/global_governance_baseline.md
/opt/codex-standards/docs/governance/
```

Project-specific public-repo redaction and sanitization rules are stricter than
the shared baseline and must be preserved.

## Runtime and Private Artifact Rules

Runtime artifacts must remain ignored unless explicitly promoted as sanitized
public assets.

Runtime artifacts include draft screenshots, screenshot staging areas, local
inventory exports, local Ansible output, packaging scratch files, build outputs,
temporary media production files, personal notes, and unpublished content.

Do not inspect, print, expose, stage, commit, or summarize private local
artifact contents.

## Git Workflow

- Inspect repository state before edits.
- Preserve existing public content and release assets.
- Do not commit unless explicitly instructed.
- Do not push unless explicitly instructed.
- Do not force push.
- Run validation and redaction checks before commit handoff.
- Confirm runtime/private artifacts are not staged.

## Validation

Default validation before commit handoff:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
./scripts/validate_repo_finalization.sh
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh scripts/validate_repo_finalization.sh
git diff --check
```

`scripts/validate_repo_finalization.sh` is read-only and checks governance,
artifact policy, ignore coverage, staged private/runtime artifacts, staged
generated packaging artifacts, and ownership.
