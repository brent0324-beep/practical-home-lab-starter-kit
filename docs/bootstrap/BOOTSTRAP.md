# Bootstrap

<!--
Generated Markdown template for docs/bootstrap/BOOTSTRAP.md.
Source of truth: config/repository_bootstrap.yml
Renderer: scripts/render_repository_bootstrap.py
Do not hand-edit generated BOOTSTRAP.md except emergency repair.
-->

> Generated file. Source of truth: `config/repository_bootstrap.yml`
>
> Template: `templates/repository_bootstrap_template.md`
>
> Renderer: `scripts/render_repository_bootstrap.py`
>
> Live session context: `docs/bootstrap/SESSION_STATE.md`
>
> Do not hand-edit `docs/bootstrap/BOOTSTRAP.md` except emergency repair.
>
> Preserve repository boundaries, public-safe artifacts, repository validation,
> and no-force-push controls.

## Repository Identity

- Name: `Practical Home Lab Starter Kit`
- Root: `project root`
- Default branch: `main`
- Working branch rule: main is the public integration branch; scoped feature branches are optional for maintainers

## Repository Purpose

- Summary: Public educational home-lab starter kit plus labctl, a spec-driven Containerlab deployment engine for fast, repeatable lab environments.
- Scope: Preserve a contributor-friendly, public-safe repository that pairs sanitized Linux, GNS3, and Ansible references with a validated JSON/YAML lab-spec workflow and saved profiles for one-command redeploy.

## Repository Classification

- Repo class: public product repository
- Posture: open source, GitHub synchronized

## Governance Model

- Hierarchy:
- AGENTS.md
- SECURITY.md
- CONTRIBUTING.md
- docs/sanitized-example-policy.md
- docs/publication-checklist.md
- docs/release-checklist.md
- docs/governance/*.md
- task-specific user instructions
- Local mode: public-repo lite
- Operator approval: Push, merge, release, force push, destructive cleanup, and credential or environment mutation require explicit operator approval.

## Safety Boundaries

- labctl labs are host-local by default; nodes bind to internal bridge networks with no published ports. External exposure (published ports, LAN bridging, VPN reach) is opt-in only and must be a deliberate operator decision, recognizing that Docker/containerlab bypass UFW.
- Keep the repository public-safe, beginner-friendly, and reference-focused.
- labctl lifecycle operations may create, inspect, and destroy Docker containers and networks ONLY when labeled io.labctl.managed=true; never mutate unmanaged containers, host services, packages, SSH, or firewall settings.
- Destroy operations must be scoped by explicit lab name and the managed label; no blanket prune of unmanaged Docker resources.
- Governance and docs changes must not alter labctl runtime behavior or release packaging as a side effect.
- Do not weaken validation, redaction, no-force-push, or repository-boundary controls.

## Privacy Boundaries

- Do not place secrets, tokens, credentials, keys, inventories, backups, unpublished media, or local-only notes in bootstrap or session artifacts.
- Keep generated engineering-session artifacts local, Git ignored, and free of sensitive environment details.
- Use placeholders, private lab ranges, and generic hostnames in public examples.

## Architecture Summary

- Public docs, sanitized templates, and example scripts remain the primary product surface.
- Governance v2 Lite adds repository-local bootstrap, session, prompt, and bundle tooling for maintainers without changing product functionality.
- Generated engineering-session artifacts live under generated/ and remain non-canonical.
- labctl (src/labctl/) renders validated lab specs into native Containerlab topologies and wraps deploy/status/destroy; Containerlab remains the execution engine.

## Important Directories

- `docs/bootstrap/`: generated public bootstrap and live session-state context
- `docs/governance/`: public governance references, prompt standard, and engineering session workflow documentation
- `scripts/`: validation, bundle generation, prompt rendering, and session wrappers
- `templates/`: bootstrap, repository-context, session-history, and prompt source templates
- `profiles/`: lite prompt defaults and repository design profiles for engineering sessions
- `schemas/`: prompt specification schema references
- `generated/`: ignored repository context, session history, prompt smoke output, and migration bundles
- `src/labctl/`: labctl CLI, spec validation, topology renderer, lifecycle wrappers
- `labs/examples/`: sanitized flagship example lab specs and startup fixtures
- `profiles/labs/`: saved variable profiles for one-command lab redeployment
- `schemas/`: prompt schema plus lab spec and lab profile schema references

## Validation Commands

- Engineering session: `./scripts/session`
- Required: `./scripts/validate.sh`
- Redaction: `./scripts/redaction-check.sh`
- Repository finalization: `./scripts/validate_repo_finalization.sh`
- Prompt standard: `python3 scripts/validate_prompt_standard.py`
- Diff hygiene: `git diff --check`

## SMCPP Status

- Mode: Governance v2 Lite
- Readiness profile: ./scripts/validate.sh, ./scripts/redaction-check.sh, ./scripts/validate_repo_finalization.sh, and git diff --check
- Notes:
- SMCPP means governed feature completion into the configured integration branch.
- When explicitly authorized, SMCPP may perform validation, finalization checks, commit if required, feature push, PR creation, merge into main, feature branch cleanup, prune, and final reporting.
- SMCPP does not authorize release creation, force push, validation bypass, unrelated repository mutation, credential mutation, secret mutation, or environment mutation.

## Major Capabilities

- Public-safe starter kit documentation for Linux, GNS3, Ansible, remote access, and validation habits.
- Sanitized templates and example scripts for lab workflows.
- Governance v2 Lite engineering-session initialization with bootstrap rendering, repository context, session history, prompt rendering, and migration bundle generation.
- Public-safety validation, redaction checks, and repository finalization guardrails.

## Major Decisions

- Preserve docs/bootstrap/BOOTSTRAP.md as the public bootstrap entrypoint.
- Keep live or changing context in docs/bootstrap/SESSION_STATE.md.
- Keep generated engineering-session artifacts ignored and out of tracked source history.
- Use repository-local wording so public contributors can understand the workflow without repository-private governance context.

## Current Constraints

- Governance adoption must not change product functionality or release packaging.
- Contributor documentation should stay concise and public-oriented.
- Generated session artifacts must remain deterministic, local, and Git ignored.
- Validation must remain safe, local, and readable for maintainers.

## Known Technical Debt

- Session state is still maintainer-authored and may drift if not refreshed.
- Prompt and bundle tooling are intentionally lighter than larger governance repositories.
- Bootstrap rendering depends on local Python with YAML support.

## Outstanding Governance Work

- Refresh docs/bootstrap/SESSION_STATE.md at session start and before major handoff.
- Keep lite prompt, bundle, and bootstrap assets aligned with future shared standards updates.
- Expand tests only where they materially improve maintainability for this public repository.

## Warnings / Inconsistencies

- docs/bootstrap/BOOTSTRAP.md is generated and should not be hand-edited during normal workflow.
- The safety boundary intentionally permits scoped Docker mutation for labctl (managed-label only), diverging from the original docs-only prohibition. This is a deliberate product-scope decision, not a weakened control.
- Generated prompts and migration bundles are maintainer artifacts, not canonical tracked source.

## Live Session State

- Path: `docs/bootstrap/SESSION_STATE.md`
- Guidance:
- Keep live or changing context out of config/repository_bootstrap.yml.
- Review or refresh session state at session start, after validation changes, and before major handoff.
- Use Git and validation commands for current state instead of stale notes.

## Shared Standard References

- `Shared Governance v2 bootstrap context standard`
- `Shared Governance v2 session-state standard`
- `Shared Governance v2 prompt lifecycle integration standard`
- `Shared Governance v2 migration bundle guidance`
