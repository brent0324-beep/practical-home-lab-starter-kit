# Release Notes: v0.1.0 Draft

This is the draft v0.1.0 local release package for the Practical Home Lab
Starter Kit for Network Engineers.

## Purpose

This release prepares the repo to be useful as a public GitHub starter kit and
as the foundation for future blog, video, PDF, and template-bundle work.

## What Is Included

- Public README with quick-start workflow and repo navigation.
- Architecture, GNS3, Linux host, security, remote access, Ansible, and
  troubleshooting documentation.
- Diagram-ready Mermaid architecture files.
- Sanitized templates for inventory, network variables, UFW, and SSH hardening.
- Basic read-only Ansible examples.
- Video walkthrough outline and narration draft.
- Product planning docs for free vs paid scope and launch sequencing.
- GitHub issue and pull request templates.
- Contribution, security, publication, and sanitization guidance.
- Local packaging script for creating a tarball under `dist/`.

## What Is Not Included

- Real credentials or secrets.
- Real private keys, PSKs, tokens, account data, or private environment details.
- Real public-facing infrastructure addresses.
- Production-ready network design guarantees.
- Paid-product delivery files.

## Validation

Before packaging or publishing, run:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh
git diff --check
```

## Packaging

Create a local archive with:

```bash
./scripts/package-release.sh
```

The archive is written under `dist/`, which is intentionally ignored by Git.
