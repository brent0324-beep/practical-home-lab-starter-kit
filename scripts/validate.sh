#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
  "RELEASE_NOTES.md"
  ".github/pull_request_template.md"
  ".github/ISSUE_TEMPLATE/config.yml"
  ".github/ISSUE_TEMPLATE/documentation-improvement.md"
  ".github/ISSUE_TEMPLATE/security-sanitization-review.md"
  "CHANGELOG.md"
  "LICENSE.md"
  "CONTRIBUTING.md"
  "SECURITY.md"
  "docs/architecture.md"
  "docs/linux-host-setup.md"
  "docs/gns3-setup.md"
  "docs/remote-access.md"
  "docs/security-hardening.md"
  "docs/ansible-workflows.md"
  "docs/troubleshooting.md"
  "docs/product-roadmap.md"
  "docs/example-lab-topology.md"
  "docs/release-checklist.md"
  "docs/diagram-guide.md"
  "docs/publication-checklist.md"
  "docs/sanitized-example-policy.md"
  "docs/repo-boundary-policy.md"
  "docs/local-release-process.md"
  "docs/github-publication-process.md"
  "diagrams/README.md"
  "diagrams/lab-topology.mmd"
  "diagrams/remote-access-flow.mmd"
  "diagrams/ansible-control-flow.mmd"
  "templates/ufw-rules.example.sh"
  "templates/ssh-hardening-checklist.md"
  "templates/lab-inventory.example.ini"
  "templates/network-device-vars.example.yml"
  "ansible/inventory.example.ini"
  "ansible/playbooks/ping-lab.yml"
  "ansible/playbooks/show-version.yml"
  "ansible/group_vars/all.example.yml"
  "video/walkthrough-outline.md"
  "video/ai-voiceover-script-draft.md"
  "product/paid-bundle-outline.md"
  "product/launch-checklist.md"
  "product/content-funnel.md"
  "product/free-vs-paid-scope.md"
  "product/v0.1-launch-plan.md"
  "product/pdf-bundle-table-of-contents.md"
  "product/github-launch-readme-review.md"
  "product/v0.1-release-summary.md"
  "product/next-phase-roadmap.md"
  "product/github-repo-description.md"
  "product/v0.1-github-release-draft.md"
  "product/social-launch-draft.md"
  "scripts/package-release.sh"
)

fail=0

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file"
    fail=1
    continue
  fi

  line_count="$(wc -l < "$file" | tr -d ' ')"
  if [[ "$line_count" -lt 3 ]]; then
    echo "Required file has too little content: $file"
    fail=1
  fi
done

required_terms=(
  "README.md:secure"
  "README.md:GNS3"
  "README.md:Ansible"
  "README.md:What This Is Not"
  "README.md:Visual Architecture"
  "README.md:With this repo today"
  "README.md:v0.1 local release candidate"
  "RELEASE_NOTES.md:v0.1.0"
  ".github/pull_request_template.md:Safety Review"
  ".github/ISSUE_TEMPLATE/config.yml:blank_issues_enabled"
  ".github/ISSUE_TEMPLATE/documentation-improvement.md:Documentation improvement"
  ".github/ISSUE_TEMPLATE/security-sanitization-review.md:Security or sanitization review"
  "CHANGELOG.md:v0.1.0"
  "CHANGELOG.md:dist/"
  "CONTRIBUTING.md:sanitized examples"
  "CONTRIBUTING.md:Branch Naming"
  "CONTRIBUTING.md:No-Secrets Policy"
  "SECURITY.md:Sensitive Information Rules"
  "SECURITY.md:What Counts as a Security Concern"
  "LICENSE.md:No final open source license"
  "docs/security-hardening.md:SSH"
  "docs/remote-access.md:UFW"
  "docs/ansible-workflows.md:inventory"
  "docs/example-lab-topology.md:Management network"
  "docs/example-lab-topology.md:diagrams/lab-topology.mmd"
  "docs/diagram-guide.md:Diagram Map"
  "docs/release-checklist.md:redaction-check.sh"
  "docs/publication-checklist.md:Publication Checklist"
  "docs/sanitized-example-policy.md:Sanitized Example Policy"
  "docs/repo-boundary-policy.md:Repository Boundary Policy"
  "docs/local-release-process.md:Local Release Process"
  "docs/github-publication-process.md:GitHub Publication Process"
  "diagrams/README.md:Diagram Strategy"
  "diagrams/lab-topology.mmd:flowchart"
  "diagrams/remote-access-flow.mmd:flowchart"
  "diagrams/ansible-control-flow.mmd:flowchart"
  "product/free-vs-paid-scope.md:Stays Free"
  "product/v0.1-launch-plan.md:v0.1"
  "product/pdf-bundle-table-of-contents.md:Paid PDF Bundle"
  "product/github-launch-readme-review.md:GitHub Launch README Review"
  "product/v0.1-release-summary.md:v0.1 Release Summary"
  "product/next-phase-roadmap.md:Next Phase Roadmap"
  "product/github-repo-description.md:Short Description"
  "product/v0.1-github-release-draft.md:Release Title"
  "product/social-launch-draft.md:Social Launch Draft"
  "scripts/package-release.sh:tar"
  "video/walkthrough-outline.md:Scene 1"
  "video/ai-voiceover-script-draft.md:Target length: 5 to 7 minutes"
  "templates/ufw-rules.example.sh:ufw"
  "ansible/playbooks/ping-lab.yml:ansible.builtin.wait_for"
  "ansible/playbooks/show-version.yml:show version"
)

for check in "${required_terms[@]}"; do
  file="${check%%:*}"
  term="${check#*:}"
  if [[ -f "$file" ]] && ! grep -Fq "$term" "$file"; then
    echo "Required term not found in $file: $term"
    fail=1
  fi
done

if ! bash -n scripts/package-release.sh; then
  echo "Package script syntax check failed."
  fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  echo "Validation failed."
  exit 1
fi

echo "Validation passed."
