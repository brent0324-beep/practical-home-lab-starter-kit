# Engineering Session Workflow

## Purpose

This repository adopts a Governance v2 Lite engineering-session workflow for
maintainers.

The goal is to provide compact, repeatable session context without making the
public repository feel like a maintainer-only governance system.

## Architecture

The lite workflow keeps the same core sequence as the shared Governance v2
pattern:

1. Repository Bootstrap
2. Repository Context
3. Repository Design Principles
4. Session State
5. Prompt Renderer

In this repository, the pieces are public-safe and repository-local:

- `config/repository_bootstrap.yml`: durable bootstrap source of truth
- `docs/bootstrap/BOOTSTRAP.md`: generated public bootstrap
- `docs/bootstrap/SESSION_STATE.md`: bounded live session context
- `generated/repository_context.md`: generated repository snapshot for
  re-entry
- `generated/session_history.md`: compact recent-session history
- `templates/implementation_prompt.yaml`: canonical prompt template
- `profiles/governance.yaml`: lite public-repo prompt defaults
- `schemas/prompt_schema.json`: prompt schema reference
- `scripts/session`: maintainer engineering-session wrapper

## Maintainer Workflow

1. Review `AGENTS.md`, `docs/bootstrap/BOOTSTRAP.md`, and
   `docs/bootstrap/SESSION_STATE.md`.
2. Run `./scripts/session`.
3. Review the generated repository context, session history, prompt smoke
   output, and migration bundle summary.
4. Run the normal repository validation and public-safety checks before commit
   handoff.

Public contributors do not need to use the engineering-session tooling to read
or contribute to the starter kit.

## Generated Artifact Boundary

The following are generated maintainer artifacts and must remain Git ignored:

- `generated/repository_context.md`
- `generated/session_history.md`
- `generated/prompts/*`
- `generated/migration_bundles/*`

These artifacts are useful for session re-entry and bundle packaging, but they
are not canonical tracked source.

## SMCPP Posture

This repository uses the following canonical definition:

```text
SMCPP = governed feature completion into the configured integration branch.
```

When explicitly authorized, SMCPP may include:

- validation
- finalization checks
- commit if required
- feature push
- PR creation
- merge into `main`
- feature branch cleanup
- prune
- final reporting

SMCPP does not authorize release creation, force push, validation bypass,
unrelated repository mutation, credential mutation, secret mutation, or
environment mutation.

## Contributor Clarity

The engineering-session workflow exists for maintainers. Public contributors
only need the documented repository files, examples, and validation commands.
