# Build a Secure Linux-Based Network Engineering Home Lab

Network home labs often start with good intent and then drift into a pile of
unconnected pieces: a GNS3 project here, a Linux box there, a few SSH sessions,
some Ansible tests, and notes scattered across different files.

That works for exploration. It becomes a problem when you want the lab to be
repeatable, secure, and easy to explain.

This article walks through a practical starter architecture for a Linux-based
network engineering lab using GNS3, Ansible, remote access guardrails, and
sanitized documentation habits.

The companion GitHub repo is here:

```text
https://github.com/brent0324-beep/practical-home-lab-starter-kit
```

## The Problem This Lab Solves

A useful lab should answer a few basic questions:

- What is the topology?
- How do I access it?
- Which network is used for management?
- Where is the inventory?
- Which checks are safe to run first?
- What can be shared publicly without exposing private details?

The starter kit gives those answers a simple structure.

## Practical Architecture

The reference design is intentionally small:

```text
Remote admin workstation
  |
  | SSH over trusted local network or private VPN-style access
  v
Linux lab host
  |-- GNS3 server
  |-- Ansible control workflow
  |-- UFW firewall
  |-- SSH service
  |
  +-- Private management network
        |-- virtual router
        |-- virtual switch
        |-- additional lab nodes
```

The Linux host is the anchor. It runs or supports the tools that make the lab
repeatable:

- GNS3 for virtual routers and switches.
- Ansible for read-only validation and later automation.
- SSH for administration.
- UFW for a simple host firewall baseline.
- Markdown and Mermaid for documentation and diagrams.

## Start With the Host

Before building a large topology, make the Linux host boring and reliable.

Good first checks include:

```bash
hostnamectl
ip addr show
ip route show
df -h
free -h
```

The repo includes hardware and BOM guidance so you can think through CPU, RAM,
NVMe, NICs, noise, power, and what to avoid. The advice is general on purpose:
exact prices change, but the tradeoffs stay familiar.

## Keep Remote Access Narrow

Remote access is useful, but it should not be casual.

The baseline model is:

- Use SSH keys.
- Disable direct root login where appropriate.
- Use UFW with a default-deny incoming policy.
- Allow SSH only from trusted private networks.
- Prefer local-only access unless remote access is intentionally designed.

The goal is not complexity. The goal is a small access path you can explain and
audit.

## Use GNS3 for the Network Layer

GNS3 provides the simulated network devices. Start small:

- One virtual router.
- One virtual switch.
- One private management network.
- One documented topology.

Do not troubleshoot Ansible until basic management reachability works. Confirm
that the Linux host can reach the virtual device management addresses first.

## Use Ansible Read-Only First

Ansible should start as a validation tool, not a configuration hammer.

Useful first commands:

```bash
ansible-inventory -i ansible/inventory.example.ini --list
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/ping-lab.yml
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/show-version.yml
```

After that, expand carefully with read-only show commands and local backup
artifacts. The starter kit includes example playbooks for interface summaries,
inventory output, and running configuration backup to a local artifact path.

## Sanitize Everything Public

Public lab documentation should be useful without revealing a real environment.

Use placeholder values:

- `lab-host`
- `lab-r1`
- `lab-sw1`
- `labadmin`
- `10.10.10.0/24`
- `lab.example`

Do not publish real credentials, private keys, PSKs, tokens, account data,
public-facing infrastructure addresses, customer data, employer data, or private
environment details.

## Validate Before Sharing

The repo includes basic guardrail checks:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/*.sh
git diff --check
```

These checks do not replace review. They help catch missing files, shell syntax
issues, whitespace problems, and high-signal sensitive patterns before you share
the repo or a derived lab writeup.

## What You Can Build Today

With the starter kit, you can:

- Plan a small Linux-based lab host.
- Document a GNS3 management topology.
- Run safe Ansible validation examples.
- Use sanitized templates for public notes.
- Follow a deployment checklist.
- Prepare screenshots, diagrams, and walkthrough content.

It is not a production network design. It is a practical foundation for building
better lab habits.

## GitHub Repo

Use the free starter kit here:

```text
https://github.com/brent0324-beep/practical-home-lab-starter-kit
```

The repo is meant to stand on its own. Future PDF or template material can add
polish, printable worksheets, and deeper implementation packs later, but the
public version should remain useful.
