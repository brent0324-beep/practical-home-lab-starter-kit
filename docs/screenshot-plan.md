# Screenshot Plan

Use this plan to create clean public screenshots for the README, a blog post,
or a short video walkthrough. All screenshots must use sanitized examples only.

## Recommended Repo Screenshots

- README opening section with Key Features visible.
- Quick Start section.
- Visual Architecture section.
- Repository tree showing `docs/`, `diagrams/`, `templates/`, and `ansible/`.
- Release or publication checklist.

## Minimum Screenshot Set

- README hero or overview visual from `assets/diagrams/starter-kit-overview.svg`.
- Lab topology diagram from `assets/diagrams/lab-topology-placeholder.svg`.
- Terminal validation output from `./scripts/validate.sh`.
- Ansible example output from a sanitized lab or a carefully reviewed dry demo.
- Optional GNS3 topology screenshot with all labels sanitized.

## Recommended Terminal Captures

Capture successful output for:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/validate.sh scripts/redaction-check.sh scripts/package-release.sh
git diff --check
```

Optional packaging capture:

```bash
./scripts/package-release.sh
ls -lh dist/
```

Do not capture terminal history, usernames, shell prompts, local absolute paths,
environment variables, real device output, or private hostnames.

## Diagram Screenshots

Recommended diagram captures:

- `diagrams/lab-topology.mmd`
- `diagrams/remote-access-flow.mmd`
- `diagrams/ansible-control-flow.mmd`

Use rendered Mermaid output when possible. Keep labels readable at blog and
README widths.

## README Image Strategy

Use images sparingly. The README should remain useful as text, with diagrams
linked as source files. If rendered images are added later:

- Store them under a dedicated image directory.
- Keep Mermaid source as the canonical editable version.
- Use descriptive alt text.
- Review every image for sensitive data before publishing.

## Video Thumbnail Ideas

- Clean topology diagram with the title "Practical Network Home Lab".
- Split view of README and Mermaid topology.
- Terminal validation success next to the lab topology diagram.
- Linux host plus GNS3 plus Ansible control flow.

Avoid thumbnails that look like guaranteed career, income, or certification
claims.
