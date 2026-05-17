# Architecture

The reference architecture is a small Linux-based lab host that supports GNS3,
Ansible, secure remote access, and repeatable documentation. The goal is not to
mirror a corporate network. The goal is to build a lab that teaches production
habits while staying safe enough to run at home.

## Reference Topology

```text
Admin workstation
  |
  | SSH or VPN
  v
Linux lab host
  |-- GNS3 server
  |-- Ansible control files
  |-- local documentation
  |-- UFW firewall
  |
  +-- lab management bridge: 10.10.10.0/24
        |-- lab-r1: 10.10.10.11
        |-- lab-r2: 10.10.10.12
        |-- lab-sw1: 10.10.10.21
```

All addresses are examples. Use your own private lab ranges and keep them
consistent across GNS3, Ansible, diagrams, and notes.

## Design Principles

- Keep management traffic separate from simulated data-plane traffic.
- Prefer key-based SSH and named admin users.
- Use default-deny firewall rules on the host.
- Keep lab state reproducible with inventories, templates, and notes.
- Separate real secrets from public examples.
- Document assumptions before troubleshooting symptoms.

## Core Components

The Linux host is the stable base. It runs GNS3, stores lab projects, and acts as
the Ansible control node unless you choose to run Ansible from a separate admin
workstation.

GNS3 provides the network topology. Each project should have a short purpose,
management IP plan, device image notes, and a known-good snapshot or export
process.

Ansible provides repeatable checks and lightweight automation. Start with ping,
facts, show commands, and configuration backups before moving into configuration
changes.

UFW and SSH hardening reduce the chance that convenience turns into exposure.
The lab should be reachable only from trusted local networks or a private remote
access path.

## Recommended Directory Pattern

```text
lab-root/
  ansible/
    inventories/
    playbooks/
    group_vars/
  gns3-notes/
  diagrams/
  change-log.md
  troubleshooting.md
```

This repository keeps public examples in `ansible/` and `templates/`. Your real
local lab can use the same shape while excluding private files from Git.

## Expansion Path

Start with one router, one switch, and one automation workflow. Add complexity
only when the previous layer is documented and repeatable.

Good next steps include:

- Dual-router routing labs.
- VLAN and trunking labs.
- NAT and firewall policy labs.
- Config backup automation.
- Golden configuration comparisons.
- Simple CI checks for inventory and documentation.
