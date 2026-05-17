# Changelog

All notable changes to this starter kit should be documented here.

This project uses practical release notes rather than strict semantic-versioning
claims. Version numbers are intended to help readers understand the maturity of
the public content.

## v0.1.0 Draft

Draft local release package for the Practical Home Lab Starter Kit for Network
Engineers. This release is intended to be a safe public foundation: useful as a
free GitHub starter kit, structured enough to support a blog post and video, and
organized enough to become the base for a future paid PDF/template bundle.

The v0.1.0 scope focuses on sanitized documentation, architecture diagrams,
basic Ansible examples, GitHub readiness assets, and local release packaging. It
does not include real lab inventories, real device configurations, private
access details, or production-ready deployment claims.

### Added

- Public README landing page for a Linux-based network engineering lab.
- Documentation for architecture, Linux host setup, GNS3, remote access,
  security hardening, Ansible workflows, and troubleshooting.
- Sanitized templates for lab inventory, network variables, UFW rules, and SSH
  hardening review.
- Basic read-only Ansible examples for reachability and command collection.
- Product planning notes for public content and future paid bundle scope.
- Video outline and voiceover draft for a short walkthrough.
- Mermaid diagrams for lab topology, remote access, and Ansible control flow.
- GitHub pull request and issue templates for public repository hygiene.
- Publication, sanitized-example, repository-boundary, and local-release
  checklists.
- Local release packaging script that creates a `dist/` archive while excluding
  `.git` and previous release archives.
- Validation and redaction scripts for basic release checks.

### Release Notes

- All example hostnames, users, addresses, and paths are placeholders.
- No real credentials, private keys, tokens, PSKs, customer data, or account
  details should be included in this repository.
- The v0.1.0 release is intended as a useful public foundation, not a complete
  production lab design.
- `dist/` artifacts are local build outputs and should not be committed.
