# Secret Handling

## Sensitive Material

Never commit or publish:

- credentials
- passwords or passphrases
- SSH private keys
- VPN keys
- PSKs
- API tokens
- cloud credentials
- private inventory exports
- account, billing, customer, employer, or production data
- device serial numbers
- screenshots or videos containing private details

## Handling Rules

- Use sanitized placeholders in public examples.
- Keep real lab values in local ignored files outside tracked source.
- Do not copy real configs into the repository and edit them down.
- Create fresh placeholder examples instead of adapting private material.
- Report likely exposure by path and concern type, not by secret value.
- Do not include sensitive values in issues, pull requests, commit messages, or
  release notes.

## Public Examples

Allowed public examples include:

- `10.10.10.0/24`
- `lab-host`
- `lab-r1`
- `lab-sw1`
- `labadmin`
- `lab.example`

Do not use values that could be mistaken for a real production, customer,
employer, or personal environment.

## Secret Scanning

The existing redaction check remains the first local guardrail:

```bash
./scripts/redaction-check.sh
```

Gitleaks or equivalent scanning should target tracked public content and
sanitized examples. It must not require opening private local notes, ignored
draft media, local inventories, or packaging scratch files.

Run from the repository root:

```bash
gitleaks detect --source . --config .gitleaks.toml --redact --no-banner
```

Use redacted output only. If a finding appears, report the path and rule ID, not
the secret value.
