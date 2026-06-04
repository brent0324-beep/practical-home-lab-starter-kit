# Runtime Data Policy

## Boundary

The repository boundary is:

```text
repository = sanitized public starter-kit source
runtime = local lab data, draft media, packaging output, unpublished content
```

Runtime data remains local-only and ignored by default.

## Runtime Data Classes

Runtime data includes:

- draft screenshots
- screenshot work directories
- local Ansible inventory exports
- local Ansible command output
- generated backups
- local lab validation output
- raw and edited media recordings
- temporary audio, thumbnails, and screenshots
- package archives and packaging scratch
- personal notes
- unpublished content
- private lab configs or topology notes

## Storage Locations

Runtime paths should remain ignored:

```text
dist/
media/raw/
media/edited/
media/audio/
media/thumbnails/
media/screenshots/
screenshots/work/
screenshots/drafts/
inventories/
inventory/
ansible/output/
ansible/outputs/
ansible/backups/
tmp/
scratch/
private/
notes/private/
unpublished/
```

Only `.gitkeep` placeholders should be tracked where the repository intentionally
keeps empty workspace directories.

## Publication Rule

Before publication, confirm:

- draft screenshots are not staged
- local inventories are not staged
- Ansible output and backups are not staged
- generated packages are not staged accidentally
- raw or edited media is not staged
- private notes and unpublished content are not staged
- reviewed public assets are sanitized

Use:

```bash
./scripts/validate_repo_finalization.sh
./scripts/redaction-check.sh
```
