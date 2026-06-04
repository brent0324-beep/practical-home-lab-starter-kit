# Git Workflow

## Baseline Rules

- Inspect `git status --short` before edits.
- Keep changes scoped to `/opt/products/practical-home-lab-starter-kit`.
- Preserve existing public documentation, release assets, validation scripts,
  publication guidance, and redaction controls.
- Do not commit unless explicitly instructed.
- Do not push unless explicitly instructed.
- Do not force push.
- Do not rewrite shared history unless explicitly requested and separately
  reviewed.

## Staging Rules

Do not stage:

- real credentials, tokens, keys, PSKs, or secrets
- real infrastructure details
- customer, employer, production, account, or billing data
- local inventories
- local Ansible output or backups
- draft screenshots or screenshot workspaces
- raw or edited media
- generated packaging output
- personal notes
- unpublished content

Only stage public-safe source, sanitized examples, reviewed public assets,
governance docs, and validation scripts.

## Before Commit Handoff

Run:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
./scripts/validate_repo_finalization.sh
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh scripts/validate_repo_finalization.sh
git diff --check
git status --short
```

Stop if private content, runtime artifacts, generated packages, or unpublished
media are staged.

## Public Release Boundary

Before tagging, publishing, or posting launch content, complete:

- `docs/publication-checklist.md`
- `docs/release-checklist.md`
- manual screenshot/media review
- package content review
- redaction validation
