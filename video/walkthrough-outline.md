# Walkthrough Outline

Target length: 3 to 5 minutes.

## 1. Repo Overview

- Show the README.
- Explain the purpose of the starter kit.
- Point out the security notice and sanitized examples.

## 2. Architecture

- Open `docs/architecture.md`.
- Show the Linux host, GNS3, Ansible, and management subnet relationship.
- Emphasize private lab ranges and documentation.

## 3. Host and Security

- Open `docs/linux-host-setup.md`.
- Open `docs/security-hardening.md`.
- Mention SSH keys, UFW, patching, and secret handling.

## 4. GNS3 and Ansible

- Open `docs/gns3-setup.md`.
- Open `ansible/inventory.example.ini`.
- Open `ansible/playbooks/ping-lab.yml`.
- Explain the read-only first workflow.

## 5. Templates

- Show the UFW and SSH hardening templates.
- Explain that real local values should stay outside public commits.

## 6. Validation

- Run `./scripts/validate.sh`.
- Run `./scripts/redaction-check.sh`.
- Explain that these checks are basic guardrails, not a substitute for review.

## 7. Close

- Invite users to fork the repo and adapt it to their own private lab.
- Mention that a future bundle may add a polished workbook and expanded
  templates, while the free repo remains useful.
