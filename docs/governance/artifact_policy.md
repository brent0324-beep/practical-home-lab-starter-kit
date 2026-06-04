# Artifact Policy

## Purpose

Artifact governance keeps the public starter kit useful while preventing local
runtime, private, draft, and packaging artifacts from entering Git history.

The machine-readable policy is:

```text
config/artifact_policy.json
```

## Public Source Artifacts

Tracked public source artifacts include:

- README, changelog, release notes, license, security, and contribution docs
- public documentation under `docs/`
- sanitized templates under `templates/`
- sanitized Ansible examples under `ansible/`
- Mermaid diagrams under `diagrams/`
- reviewed public assets under `assets/`
- blog, video, media, and product planning documents
- validation and example scripts
- GitHub issue and pull request templates
- governance documentation

These artifacts must remain sanitized and public-safe.

## Public Asset Artifacts

Reviewed assets under `assets/` may be tracked when they are sanitized and
intended for public README, diagram, screenshot, or demo use.

Tracked public images and diagrams must not reveal sensitive details.

## Runtime and Private Artifacts

The following must remain ignored unless explicitly sanitized and promoted:

- draft screenshots
- screenshot staging areas
- local inventory exports
- local Ansible output
- generated backups
- packaging scratch files
- build output under `dist/`
- raw, edited, audio, thumbnail, and screenshot media workspaces
- personal notes
- unpublished content
- private infrastructure details

## Packaging Artifacts

Release packages are generated artifacts. The packaging workflow may write under
`dist/`, but generated archives and scratch files remain ignored.

Before publication, inspect release package contents through the documented
release process and run redaction checks.

## Review Rule

Before commit handoff, run:

```bash
./scripts/validate_repo_finalization.sh
```

This checks artifact policy validity, ignore coverage, staged runtime/private
artifact posture, staged package artifact posture, and ownership without reading
private local content.
