# Practical Home Lab Starter Kit for Network Engineers

Build a secure Linux-based network engineering lab with GNS3, Ansible, remote access, and repeatable workflows.

## Visual Overview

<p align="center">
  <img src="assets/diagrams/starter-kit-overview.png"
       alt="Practical Home Lab Starter Kit Overview"
       width="1000">
</p>

<p align="center">
  <em>Sanitized example overview of the Linux, GNS3, Ansible, remote access, validation, and documentation workflow.</em>
</p>

## Current Status

v0.1 public foundation...

# Diagram Assets

This directory contains README-friendly visuals for the public repo. All visuals
are sanitized examples and must not include real addresses, hostnames,
credentials, keys, tokens, PSKs, account data, or private environment details.

The editable source diagrams live in `diagrams/` as Mermaid files. Assets here
are presentation visuals for the README, demos, blog posts, and videos.

## Primary README Visual

- `starter-kit-overview.png` is the primary README hero visual. It gives a
  polished high-level overview of the Linux, GNS3, Ansible, remote access,
  validation, and documentation workflow.

## Supporting Technical SVGs

- `starter-kit-overview.svg` is the editable SVG version of the overview visual.
- `lab-topology-placeholder.svg` shows the example lab topology: trusted access,
  Linux lab host, GNS3 server, management network, and automation workflow.
- `remote-access-flow-placeholder.svg` focuses on private remote access, edge
  filtering, UFW, and SSH.
- `ansible-control-flow-placeholder.svg` shows inventory, group vars, safe
  playbooks, private management access, and local review artifacts.

## Maintenance Notes

- Keep labels generic and example-only.
- Use the PNG as the README hero image.
- Use SVGs as reusable technical support visuals.
- Keep Mermaid source files as the canonical editable architecture source.
- Review every visual before public release.
