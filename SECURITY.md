# Security Policy

This repository contains lab-only examples for a Linux-based network engineering
home lab. It must not contain real secrets or private environment details.

## Sensitive Information Rules

Do not commit:

- Real credentials.
- Private SSH keys.
- VPN keys or PSKs.
- API tokens.
- Public-facing infrastructure addresses.
- Customer, employer, account, or billing data.
- Device serial numbers or private inventory exports.
- Screenshots that reveal sensitive lab or personal details.

Use sanitized examples and placeholder values throughout the repo.

## Reporting Concerns

If you find a likely secret or private detail in this repository:

1. Do not copy it into public discussion.
2. Open a minimal issue or contact the maintainer through the project channel
   with the file path and a short description.
3. Avoid including the sensitive value itself.

If this repository is later published under an organization, replace this
section with that organization's preferred private reporting process.

## Lab Safety

The examples are intended for isolated home labs and private address space. Do
not expose lab services broadly without understanding the access path, firewall
rules, logging, and rollback plan.

Before release, run:

```bash
./scripts/redaction-check.sh
```
