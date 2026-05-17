# Public Demo Walkthrough

Use this sequence for a safe public demo of the v0.1 starter kit. The demo
should show the repo structure and workflow without exposing any real lab data.

## Demo Goals

- Explain what the starter kit is.
- Show the architecture visually.
- Demonstrate the validation and redaction workflow.
- Show sanitized templates and read-only Ansible examples.
- Keep all examples private-range and placeholder-based.

## 1. Open the README

Show on screen:

- Project title and opening section.
- Key Features.
- Quick Start.
- Visual Architecture.

Talking point:

This repo is a practical foundation for a Linux-based network engineering home
lab, not a production design.

## 2. Show the Topology Diagram

Show on screen:

- `diagrams/lab-topology.mmd`
- `docs/example-lab-topology.md`

Talking point:

The Linux lab host anchors GNS3, Ansible, SSH, UFW, documentation, and the
private management network.

## 3. Show Remote Access Guardrails

Show on screen:

- `diagrams/remote-access-flow.mmd`
- `docs/remote-access.md`
- `docs/security-hardening.md`

Talking point:

Remote access should be narrow, documented, and protected by SSH keys and UFW.

## 4. Show Ansible Workflow

Show on screen:

- `diagrams/ansible-control-flow.mmd`
- `ansible/inventory.example.ini`
- `ansible/playbooks/ping-lab.yml`
- `ansible/playbooks/show-version.yml`

Terminal commands to demonstrate:

```bash
ansible-inventory -i ansible/inventory.example.ini --list
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/ping-lab.yml
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/show-version.yml
```

If no test devices are available, explain the commands without running them
against a real environment.

## 5. Show Templates

Show on screen:

- `templates/lab-inventory.example.ini`
- `templates/network-device-vars.example.yml`
- `templates/ufw-rules.example.sh`
- `templates/ssh-hardening-checklist.md`

Talking point:

These are sanitized examples. Real inventories, keys, tokens, PSKs, and private
configs do not belong in public repos.

## 6. Run Guardrail Checks

Terminal commands to demonstrate:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh
git diff --check
```

Talking point:

The checks are guardrails. They do not replace human review.

## 7. Show Local Packaging

Terminal command:

```bash
./scripts/package-release.sh
```

Show on screen:

```bash
ls -lh dist/
```

Talking point:

The archive is a local package output and `dist/` is ignored by Git.

## 8. Close

Show on screen:

- `docs/sanitized-example-policy.md`
- `docs/publication-checklist.md`
- `product/next-phase-roadmap.md`

Closing point:

Start small, document the lab, validate before sharing, and expand only after
the basics are repeatable.
