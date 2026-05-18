# Walkthrough Outline

Target length: 5 to 7 minutes.

## Quick Demo Version: 3 to 5 Minutes

Use this version for a short launch walkthrough.

1. Open the README and show the opening, Visual Preview, and Key Features.
2. Open `assets/diagrams/lab-topology-placeholder.svg` and explain the lab
   shape.
3. Open `diagrams/lab-topology.mmd` to show the editable Mermaid source.
4. Show `scripts/bootstrap-lab-host.example.sh` and
   `scripts/setup-ufw-baseline.example.sh`; explain dry-run behavior.
5. Run:

```bash
./scripts/bootstrap-lab-host.example.sh
./scripts/setup-ufw-baseline.example.sh
./scripts/validate.sh
./scripts/redaction-check.sh
```

6. Close on the sanitized-example policy and roadmap.

## Suggested Recording Order

Record the easiest, lowest-risk sections first so the early footage is mostly
static and easy to re-take.

1. README overview: opening, Visual Preview, Key Features, and What This Is Not.
2. Static diagrams: rendered topology preview, then Mermaid source files.
3. Documentation pages: Linux host setup, GNS3 setup, remote access, and
   sanitized-example policy.
4. Templates and example scripts: UFW, SSH hardening, bootstrap, and validation
   scripts.
5. Terminal validation: run validation, redaction, shell syntax, and whitespace
   checks last after the recording environment is clean.
6. Closing shot: return to the README or roadmap once the terminal output has
   been reviewed.

The easiest sections to record first are the README overview, diagram walkthrough,
and docs tour because they do not depend on live command output. Record terminal
commands later, after browser cleanup, shell prompt cleanup, and a test capture.

## Narration Visual Map

- Intro narration: show the README title, Visual Preview, and Key Features.
- Lab topology narration: show `assets/diagrams/starter-kit-overview.png` or
  `diagrams/lab-topology.mmd`.
- Remote access narration: show `diagrams/remote-access-flow.mmd` and the SSH
  or UFW documentation.
- Linux and GNS3 narration: show `docs/linux-host-setup.md`,
  `docs/gns3-setup.md`, and a clean repository tree.
- Ansible narration: show `diagrams/ansible-control-flow.mmd`,
  `ansible/inventory.example.ini`, and the read-only playbooks.
- Guardrails narration: show `docs/sanitized-example-policy.md`,
  `SECURITY.md`, and validation commands in a clean terminal.
- Closing narration: show the README, roadmap, or release checklist.

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
- Run `bash -n scripts/*.sh`.
- Run `git diff --check`.
- Explain that checks are guardrails, not a substitute for human review.

## Scene 8: Free Repo and Future Bundle

- Invite users to fork the repo and adapt it to their own private lab.
- Mention that a future bundle may add a polished workbook and expanded
  templates, while the free repo remains useful.
