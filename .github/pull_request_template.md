## Summary

Describe what changed and why.

## Type of Change

- [ ] Documentation improvement
- [ ] Template/example update
- [ ] Diagram update
- [ ] Validation or tooling update
- [ ] Product planning update

## Safety Review

- [ ] Examples are sanitized.
- [ ] No real credentials, PSKs, tokens, private keys, account data, or private
      environment details are included.
- [ ] No public-facing infrastructure addresses are included.
- [ ] Hostnames, usernames, IPs, and configs use placeholder lab values.
- [ ] Screenshots or diagrams, if added, contain sanitized labels only.

## Validation

- [ ] `./scripts/validate.sh`
- [ ] `./scripts/redaction-check.sh`
- [ ] `bash -n scripts/validate.sh scripts/redaction-check.sh`
- [ ] `git diff --check`

## Notes

Add any review notes, assumptions, or follow-up items.
