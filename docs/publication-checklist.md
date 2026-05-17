# Publication Checklist

Use this checklist before making the repository public, tagging a release, or
sharing the starter kit in a blog post or video.

## Repository Review

- [ ] README explains what the repo is in the first 30 seconds of reading.
- [ ] Repo navigation links point to existing files.
- [ ] The license status is clear.
- [ ] Contribution and security guidance are present.
- [ ] GitHub issue and pull request templates are present.

## Content Review

- [ ] Documentation uses practical network-engineer language.
- [ ] Examples are sanitized and clearly marked as placeholders.
- [ ] Diagrams use private lab labels only.
- [ ] Product references are modest and not misleading.
- [ ] Video and PDF planning docs do not overpromise outcomes.

## Safety Review

- [ ] No real secrets are present.
- [ ] No private keys or PSKs are present.
- [ ] No tokens are present.
- [ ] No public-facing infrastructure addresses are present.
- [ ] No account data or private environment details are present.
- [ ] No real configs or screenshots were copied into the repo.

## Required Commands

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/validate.sh scripts/redaction-check.sh
git diff --check
```

## Final Step

Confirm the worktree is clean before publishing or tagging.
