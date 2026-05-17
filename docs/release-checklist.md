# Release Checklist

Use this checklist before tagging or publishing a release.

## Required Checks

- [ ] Run `./scripts/validate.sh`.
- [ ] Run `./scripts/redaction-check.sh`.
- [ ] Run `bash -n scripts/validate.sh scripts/redaction-check.sh`.
- [ ] Run `git diff --check`.

## Markdown Review

- [ ] README has clear navigation and quick start steps.
- [ ] Docs use consistent headings.
- [ ] Links point to existing files.
- [ ] Commands are copyable and use sanitized values.
- [ ] Future paid bundle references are tasteful and not misleading.

## Template Review

- [ ] Templates contain placeholder values only.
- [ ] Inventories use private lab address ranges.
- [ ] No real secrets or private environment details are present.
- [ ] Examples are small enough for readers to audit.

## Diagram Review

- [ ] Diagrams use sanitized labels.
- [ ] No real public-facing addresses are shown.
- [ ] Management, remote access, and lab traffic paths are clear.
- [ ] Diagram assumptions match the README and docs.

## Video Script Review

- [ ] Voiceover avoids overpromising.
- [ ] Screens shown in the video contain sanitized examples only.
- [ ] Validation and redaction checks are mentioned.
- [ ] The paid bundle reference, if included, is brief and factual.

## Final Release Notes

- [ ] Update `CHANGELOG.md`.
- [ ] Confirm license status.
- [ ] Confirm the worktree is clean.
- [ ] Do not push until the release commit has been reviewed.
