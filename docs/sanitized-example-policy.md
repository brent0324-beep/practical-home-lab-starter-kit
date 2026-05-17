# Sanitized Example Policy

All public examples in this repository must be sanitized. The goal is to make
examples realistic enough to teach the workflow without exposing real
environments.

## Allowed Example Values

- Private lab ranges such as `10.10.10.0/24`.
- Placeholder hostnames such as `lab-host`, `lab-r1`, and `lab-sw1`.
- Placeholder usernames such as `labadmin`.
- Example domains such as `lab.example`.
- Example paths that do not reveal a real user or organization.

## Not Allowed

- Real credentials.
- Private SSH keys.
- VPN keys or PSKs.
- API tokens.
- Public-facing infrastructure addresses.
- Customer, employer, account, or billing data.
- Device serial numbers.
- Real production configs.
- Screenshots that reveal private inventory or access details.

## Review Standard

If an example could reasonably be mistaken for a real environment, sanitize it
further. Prefer boring placeholder names and clearly private lab ranges.

## Before Commit

Run:

```bash
./scripts/redaction-check.sh
```

The script is a guardrail, not a complete security review. Always inspect
examples manually before publishing.
