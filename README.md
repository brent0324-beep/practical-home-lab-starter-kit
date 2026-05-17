# Practical Home Lab Starter Kit for Network Engineers

Build a secure, repeatable Linux-based network engineering lab with GNS3,
Ansible, remote access, and practical documentation habits.

This repo is a free starter kit for network engineers who want a home lab that
feels closer to production work than a pile of disconnected VMs. It focuses on
small, defensible choices: a hardened Linux host, documented topology, GNS3 for
network simulation, Ansible for repeatable checks, and remote access that does
not depend on risky shortcuts.

The examples are intentionally sanitized. Copy the structure, not the literal
values. Replace lab addresses, hostnames, usernames, SSH keys, and inventories
with your own private lab details.

## Repo Navigation

Start here:

- [docs/example-lab-topology.md](docs/example-lab-topology.md) shows the sample
  lab shape.
- [docs/linux-host-setup.md](docs/linux-host-setup.md) prepares the Linux base.
- [docs/gns3-setup.md](docs/gns3-setup.md) connects the network simulation
  layer.
- [docs/security-hardening.md](docs/security-hardening.md) covers SSH, UFW, and
  secret-handling basics.
- [docs/ansible-workflows.md](docs/ansible-workflows.md) explains the read-only
  automation flow.

Then use:

- [templates/](templates/) for sanitized copyable examples.
- [ansible/](ansible/) for basic Ansible inventory and playbooks.
- [docs/release-checklist.md](docs/release-checklist.md) before publishing
  changes or release notes.

## Who This Is For

- Network engineers building automation skills without waiting for a work lab.
- Students who want a realistic Linux, GNS3, and Ansible workflow.
- Engineers refreshing fundamentals around SSH, UFW, inventory, and runbooks.
- Anyone who wants a lab that can be rebuilt and documented cleanly.

## What This Is Not

- It is not a production network design.
- It is not a replacement for vendor documentation.
- It is not a collection of real device credentials or private inventories.
- It is not a promise of employment, certification, income, or operational
  readiness.
- It is not meant to expose lab services directly to the internet.

## What You Will Build

The starter kit assumes one Linux lab host, one or more GNS3 topologies, and a
small management network for automation.

```text
Admin laptop
    |
    | SSH or VPN
    v
Linux lab host
    |-- GNS3 server and projects
    |-- Ansible control directory
    |-- UFW host firewall
    |-- SSH hardened for key-based access
    |
    v
Virtual network devices on a private lab subnet
```

This is not a full enterprise design. It is a practical foundation that helps
you practice the same habits that matter in professional network engineering:
versioned configuration, repeatable commands, change notes, access control, and
rollback thinking.

## Repo Map

- [docs/architecture.md](docs/architecture.md) explains the reference design.
- [docs/linux-host-setup.md](docs/linux-host-setup.md) walks through the host
  baseline.
- [docs/gns3-setup.md](docs/gns3-setup.md) covers GNS3 setup and project
  hygiene.
- [docs/security-hardening.md](docs/security-hardening.md) gives a practical
  SSH, UFW, and maintenance checklist.
- [docs/remote-access.md](docs/remote-access.md) covers safer remote access
  patterns.
- [docs/ansible-workflows.md](docs/ansible-workflows.md) introduces the sample
  Ansible inventory and playbooks.
- [docs/troubleshooting.md](docs/troubleshooting.md) collects common failure
  modes and checks.
- [templates/](templates/) contains copyable sanitized examples.
- [ansible/](ansible/) contains basic working Ansible examples.

## Quick Start

This is the suggested first pass:

1. Install a current Ubuntu Server or Debian host for the lab.
2. Create a normal admin user and enable SSH key-based access.
3. Apply a default-deny UFW policy with explicit SSH and lab-management rules.
4. Install GNS3 server and verify you can create a simple test topology.
5. Install Ansible on the control host or inside a dedicated project venv.
6. Copy `ansible/inventory.example.ini` to a local untracked inventory file.
7. Replace placeholder hostnames and private lab IPs with your own lab values.
8. Run the sample ping and show-version playbooks against test devices.

Example Ansible workflow:

```bash
ansible-inventory -i ansible/inventory.example.ini --list
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/ping-lab.yml
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/show-version.yml
```

Validation commands:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/validate.sh scripts/redaction-check.sh
git diff --check
```

## Suggested Lab Standards

- Use private lab address space only, such as `10.10.10.0/24`.
- Keep device names boring and descriptive, such as `lab-r1` or `gns3-sw1`.
- Use SSH keys instead of reusable shared passwords.
- Keep real inventories, vault files, and secrets out of Git.
- Write down every topology assumption before troubleshooting automation.
- Treat the lab host like infrastructure, not like a disposable laptop.

## Example Workflow

1. Start a GNS3 topology with one router and one switch.
2. Confirm the Linux host can reach the device management interfaces.
3. Add devices to a sanitized Ansible inventory.
4. Run `ansible/playbooks/ping-lab.yml` to verify reachability.
5. Run `ansible/playbooks/show-version.yml` to collect basic facts.
6. Save notes about what changed, what worked, and what needs cleanup.

## Future Bundle Direction

This free repo is designed to stand on its own. A future paid PDF/template
bundle may add a more polished workbook, expanded topology diagrams, lab
worksheets, checklists, and deeper troubleshooting examples. The free material
will remain useful as a public starting point.

See [product/free-vs-paid-scope.md](product/free-vs-paid-scope.md) for the
current boundary between public content and possible future bundle material.

## Security Notice

All examples in this repository must be sanitized. Do not commit real passwords,
PSKs, private keys, tokens, customer data, public-facing addresses, account
details, or private environment information.

Before committing changes, run:

```bash
./scripts/redaction-check.sh
```
