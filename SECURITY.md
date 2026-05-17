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

## What Counts as a Security Concern

For this lab repository, security concerns include:

- Real secrets committed to the repo.
- Private keys, PSKs, tokens, or account data in examples.
- Public-facing infrastructure addresses that appear to identify a real system.
- Real customer, employer, or private environment details.
- Guidance that encourages exposing lab services broadly without safeguards.
- Screenshots or diagrams that reveal sensitive details.

## What Is Not Usually a Vulnerability

The following are usually documentation or support issues, not vulnerabilities:

- A placeholder lab IP such as `10.10.10.11`.
- A sanitized hostname such as `lab-r1`.
- A missing optional hardening step.
- A disagreement about tool choice.
- A broken Markdown link.
- A sample command that needs clearer explanation.

Open a documentation issue for those cases unless sensitive data is involved.

## Reporting Concerns

If you find a likely secret or private detail in this repository:

1. Do not copy it into public discussion.
2. Open a minimal issue or contact the maintainer through the project channel
   with the file path and a short description.
3. Avoid including the sensitive value itself.

If this repository is later published under an organization, replace this
section with that organization's preferred private reporting process.

## Sensitive-Data Exposure Reports

When reporting sensitive-data exposure, include:

- The file path.
- The section or line context.
- The type of concern.
- A suggested sanitized replacement, if obvious.

Do not include the exposed value itself. Do not post real device configs, private
inventories, terminal output, screenshots, or keys in issues or pull requests.

## Lab Safety

The examples are intended for isolated home labs and private address space. Do
not expose lab services broadly without understanding the access path, firewall
rules, logging, and rollback plan.

Before release, run:

```bash
./scripts/redaction-check.sh
```
