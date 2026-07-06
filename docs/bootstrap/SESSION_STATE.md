# Session State

- Repository: `Practical Home Lab Starter Kit`
- Updated: `2026-07-06`

# Session State

**Branch:** main (labctl Phase 1 merged and promoted)
**Last validated:** ./scripts/session PASS, live smoke test PASS

## Where things stand

labctl Phase 1 MVP is shipped and public on main. Spec-driven Containerlab
deployment engine: validate / render / deploy / status / destroy, with
managed-label lifecycle scoping, saved profiles, schema validation, and two
flagship example labs (two-node point-to-point, three-node BGP triangle).
Bootstrap safety boundary was amended to scope Docker mutation to labctl's
managed label; divergence logged.

Presence content published: a dev.to blog post ("spin up a two-node network
lab in five minutes") with inline images and a static terminal cover. A VHS
demo tape lives in demo/ as the reproducible source for future demos.

## Next up (Phase 2 backlog, logged in outstanding_governance_work)

- Per-lab uniquely-named mgmt network to prevent subnet collisions
- Detect existing mgmt network with mismatched subnet; fail with clean error
- Smoke test should clean up its own containerlab runtime directory
- Decide mgmt-network exposure policy (host-local vs VPN); document
  DOCKER-USER / UFW bypass behavior

## Loose threads

- VHS `Set Framerate` is ignored by the installed build; frame reduction is
  done via a Pillow post-process script if a future GIF needs the 500-frame
  dev.to cap. Prefer smaller tape dimensions + MP4 for embedded demos.
- Consider a pip/pyproject install path so `python3 -m labctl` works without
  the ./scripts/labctl wrapper.

## Current Branch

- Branch: `main`
- Session goal: adopt Governance v2 Lite engineering-session workflow for this
  public repository

## Working Tree Status

- Status: verify with `git status --short --branch`; scoped governance adoption
  changes may be present during the current session
- Scope guard: keep changes inside this repository and preserve the
  contributor-friendly public posture

## Recent Commit History

- `6c06bb4` Sanitize public governance references
- `392cd09` Add Home Lab CI validation workflow
- `3c797b0` Add pre-commit configuration

## Active Feature Branches

- Current active branch: `main`
- Additional local feature branches: none expected; verify locally if needed

## Validation Status

- Required command: `./scripts/session`
- Last result: `PASS`
- Last run: `2026-06-26 during the Governance v2 Lite adoption session`
- Current posture: repository validation, redaction checks, finalization
  validation, prompt verification, and migration-bundle verification are
  required before handoff

## Current Release Target

- Target: Governance v2 Lite engineering-session adoption for maintainer
  productivity

## Current Sprint/Session Goal

- Add generated bootstrap context, repository context, session history, prompt
  rendering, and migration-bundle tooling without changing product behavior

## Current MVP Definition

- `./scripts/session` generates repository context, session history, prompt
  smoke output, and a migration bundle
- `docs/bootstrap/BOOTSTRAP.md` remains the public bootstrap entrypoint
- generated engineering-session artifacts remain Git ignored
- public-safety, redaction, and validation checks remain intact

## Success Criteria

- required bootstrap, prompt, schema, and session assets exist
- `./scripts/session` completes successfully
- rendered prompt output includes `## SMCPP LIFECYCLE`
- migration bundle contains the required bootstrap and session artifacts
- validation and public-safety checks pass

## Known Pain Points

- session state is maintainer-authored and can drift if not refreshed
- generated bootstrap sync depends on local Python with YAML support
- the public repo needs lighter wording than larger governance repositories

## Operator Feedback

- keep the wording public-oriented
- do not expose repository-private governance details or private filesystem
  paths
- do not push, merge, release, or change product behavior as part of adoption

## Pending Operator Decisions

- Whether to invoke SMCPP later for governed feature-completion actions

## Last Approved UX Preview

- Not applicable

## Top Technical Debt

- bootstrap and session-state maintenance are still partly manual
- engineering-session validation will remain intentionally lighter than
  larger governance repositories

## Known Warnings

- `docs/bootstrap/BOOTSTRAP.md` is generated and should not be hand-edited
  during normal workflow
- generated prompts and migration bundles are maintainer artifacts, not
  canonical source

## Next Action

- Create the scoped governance adoption commit, then await explicit operator
  approval before any push, merge, release, or SMCPP lifecycle mutation

## Roadmap

- Current: adopt Governance v2 Lite engineering-session architecture
- Next: use the generated bundle and prompt workflow for maintainer re-entry
- Later: refine lite validation and reporting as contributor needs evolve
- Someday: automate safe session-state refresh where it materially improves
  maintainability

## Hard Architectural Boundaries

- keep work scoped to this repository
- do not add secrets, credentials, private addresses, unpublished media, or
  local inventories
- do not weaken validation, redaction, no-force-push, or operator-approval
  controls
