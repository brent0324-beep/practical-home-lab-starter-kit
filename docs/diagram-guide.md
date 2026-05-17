# Diagram Guide

The Mermaid diagrams under `diagrams/` are the visual source of truth for the
starter lab architecture. They are meant to support the README, a blog post, a
future PDF bundle, and a short video walkthrough.

## Diagram Map

- `diagrams/lab-topology.mmd` is the full reference architecture.
- `diagrams/remote-access-flow.mmd` explains how an admin reaches the lab host.
- `diagrams/ansible-control-flow.mmd` explains how Ansible reaches GNS3 virtual
  routers and switches.

## How the Diagrams Map to the Lab

The remote admin workstation is the operator's laptop or desktop. It should
connect over a trusted local network or private VPN, not broad unaudited access.

The home router or firewall represents the edge of the home network. It should
not forward lab services unless that access path is intentionally designed and
documented.

The Linux lab host is the center of the design. It runs SSH, UFW, lab notes,
GNS3, and optionally the Ansible control workflow.

The GNS3 server runs the virtual network nodes. The diagrams show routers and a
switch, but the same model can support firewalls, Linux test clients, or other
virtual appliances if they are documented.

The management network is a private lab subnet. It gives SSH and Ansible a
stable path to device management interfaces.

The Ansible control path is intentionally read-only at first. Reachability and
show-command collection should work before any configuration-changing workflow
is added.

## Blog and PDF Use

For a blog post, use the full topology diagram early, then use the remote access
and Ansible diagrams when those sections appear.

For a PDF bundle, each diagram can become a chapter figure:

- Architecture overview.
- Remote access and security boundary.
- Automation workflow.

Rendered diagrams should be checked for legibility before publishing.

## Video Use

The walkthrough video should reveal the diagrams in this order:

1. Full lab topology.
2. Remote access flow.
3. Ansible control flow.

That order helps viewers understand the whole system before zooming into access
and automation details.

## Maintenance Rules

- Keep diagram labels sanitized.
- Update diagrams when topology examples change.
- Keep README, `docs/example-lab-topology.md`, and diagrams consistent.
- Do not add real public addresses, credentials, tokens, or private details.
