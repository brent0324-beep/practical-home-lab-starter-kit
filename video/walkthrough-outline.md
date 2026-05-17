# Walkthrough Outline

Target length: 5 to 7 minutes.

## Scene 1: Opening and Promise

- Show the README.
- Explain that the repo helps network engineers build a secure, repeatable
  Linux-based lab.
- State the boundary: this is a lab foundation, not production design.

## Scene 2: Full Visual Architecture

- Open `diagrams/lab-topology.mmd`.
- Show the remote admin workstation, home router/firewall, Linux lab host, GNS3
  server, management network, and virtual devices.
- Emphasize private lab ranges and documentation.

## Scene 3: Remote Access Path

- Open `diagrams/remote-access-flow.mmd`.
- Explain the trusted local network or private VPN path.
- Point out UFW default deny and key-based SSH.

## Scene 4: Linux Host and GNS3

- Open `docs/linux-host-setup.md`.
- Open `docs/gns3-setup.md`.
- Show how the Linux host anchors GNS3 projects, notes, and lab services.

## Scene 5: Ansible Control Flow

- Open `diagrams/ansible-control-flow.mmd`.
- Open `ansible/inventory.example.ini`.
- Open `ansible/playbooks/ping-lab.yml`.
- Open `ansible/playbooks/show-version.yml`.
- Explain why read-only validation comes before configuration changes.

## Scene 6: Templates and Guardrails

- Show the UFW and SSH hardening templates.
- Show `CONTRIBUTING.md` and `SECURITY.md`.
- Explain that real local values stay outside public commits.

## Scene 7: Release Checks

- Run `./scripts/validate.sh`.
- Run `./scripts/redaction-check.sh`.
- Mention `bash -n scripts/validate.sh scripts/redaction-check.sh`.
- Mention `git diff --check`.
- Explain that checks are guardrails, not a substitute for human review.

## Scene 8: Free Repo and Future Bundle

- Invite users to fork the repo and adapt it to their own private lab.
- Mention that a future bundle may add a polished workbook and expanded
  templates, while the free repo remains useful.
