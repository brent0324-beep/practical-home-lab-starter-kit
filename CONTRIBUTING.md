# Contributing

Contributions should make the starter kit more practical, safer, clearer, or
easier to reuse in a sanitized home lab context.

## Contribution Rules

- Use sanitized examples only.
- Use private lab address ranges in examples.
- Use placeholder hostnames such as `lab-r1`, `lab-sw1`, and `lab-host`.
- Use placeholder usernames such as `labadmin`.
- Do not include real secrets, private keys, PSKs, tokens, public-facing
  addresses, customer data, account details, or private environment details.
- Do not include screenshots that reveal private inventory, device serials, or
  access details.
- Keep paid bundle references modest and factual.

## Branch Naming

Use short, descriptive branch names:

- `docs/improve-gns3-setup`
- `templates/add-inventory-example`
- `diagrams/update-remote-access-flow`
- `scripts/strengthen-validation`

Avoid branch names that include customer names, employer names, internal project
names, account identifiers, or private environment labels.

## Before Opening a Pull Request

Run:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/validate.sh scripts/redaction-check.sh
git diff --check
```

Also review Markdown manually for clarity, broken links, and examples that could
be mistaken for real environment data.

## Example Safety Rules

Good examples:

- `lab-r1`
- `labadmin`
- `10.10.10.0/24`
- `lab.example`

Do not use:

- Real device names.
- Real usernames tied to a person or organization.
- Public-facing infrastructure addresses.
- Real configs copied from production, customers, employers, or private labs.

## No-Secrets Policy

Never commit real credentials, private keys, PSKs, tokens, account data, private
inventory exports, or sensitive environment details. If you accidentally stage
or commit sensitive data, stop and report it through the security process rather
than opening a normal public discussion with the value included.

## Content Style

- Write for working network engineers.
- Prefer practical steps over abstract advice.
- Keep examples small enough to audit.
- Document assumptions and boundaries.
- Avoid guaranteed career, certification, or income claims.
