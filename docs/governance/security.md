# Security

## Public Repository Security Posture

This repository is intended to be public. Security controls focus on preventing
accidental disclosure while keeping examples useful for beginner and working
network engineers.

All public content must remain:

- sanitized
- educational
- example-only
- modest in claims
- free of customer, employer, production, or private lab details

## Infrastructure Disclosure Controls

Do not publish:

- public IPs associated with real infrastructure
- real hostnames or usernames tied to a person or organization
- real network inventories
- real device configurations
- device serial numbers
- private topology diagrams
- screenshots with private paths, addresses, sessions, inventory, or account
  details

Use private lab ranges, generic labels, and placeholder values.

## Screenshot Review

Screenshots must be reviewed before becoming public assets.

Review for:

- terminal prompts
- usernames
- hostnames
- paths
- public or private addresses that reveal a real environment
- SSH, VPN, or cloud details
- device serials
- inventory names
- browser tabs, URLs, and account details

Draft screenshots and screenshot work areas are runtime artifacts until they are
sanitized and intentionally promoted.

## Release Review

Before publication or release, run validation, redaction, finalization checks,
and manual review. The redaction check is a guardrail, not a substitute for
human inspection.

Release review should include README, docs, templates, diagrams, screenshots,
media, product planning notes, blog drafts, and package contents.
