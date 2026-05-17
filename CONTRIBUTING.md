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

## Content Style

- Write for working network engineers.
- Prefer practical steps over abstract advice.
- Keep examples small enough to audit.
- Document assumptions and boundaries.
- Avoid guaranteed career, certification, or income claims.
