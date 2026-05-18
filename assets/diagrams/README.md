# Diagram Assets

This directory contains README-friendly SVG visuals for the public repo. All
visuals are sanitized examples and must not include real addresses, hostnames,
credentials, keys, tokens, PSKs, account data, or private environment details.

The editable source diagrams live in `diagrams/` as Mermaid files. These SVGs
are presentation assets for README, demos, blog posts, and videos.

## Current SVGs

- `starter-kit-overview.svg` gives a high-level README hero visual for the full
  starter-kit workflow.
- `lab-topology-placeholder.svg` shows the example lab topology: trusted access,
  Linux lab host, GNS3 server, management network, and automation workflow.
- `remote-access-flow-placeholder.svg` focuses on private remote access, edge
  filtering, UFW, and SSH.
- `ansible-control-flow-placeholder.svg` shows inventory, group vars, safe
  playbooks, private management access, and local review artifacts.

## Maintenance Notes

- Keep labels generic and example-only.
- Prefer SVG for sharp README rendering.
- Keep Mermaid source files as the canonical editable architecture source.
- Review every visual before public release.
