#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
  "RELEASE_NOTES.md"
  ".github/pull_request_template.md"
  ".github/ISSUE_TEMPLATE/config.yml"
  ".github/ISSUE_TEMPLATE/documentation-improvement.md"
  ".github/ISSUE_TEMPLATE/security-sanitization-review.md"
  "assets/README.md"
  "assets/screenshots/README.md"
  "assets/diagrams/README.md"
  "assets/diagrams/lab-topology-placeholder.svg"
  "assets/diagrams/remote-access-flow-placeholder.svg"
  "assets/diagrams/ansible-control-flow-placeholder.svg"
  "blog/README.md"
  "blog/build-secure-linux-network-engineering-lab.md"
  "CHANGELOG.md"
  "LICENSE.md"
  "CONTRIBUTING.md"
  "SECURITY.md"
  "docs/architecture.md"
  "docs/hardware-bom.md"
  "docs/lab-deployment-checklist.md"
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
  "docs/public-demo-walkthrough.md"
  "docs/screenshot-plan.md"
  "diagrams/README.md"
  "diagrams/rendering-notes.md"
  "diagrams/lab-topology.mmd"
  "diagrams/remote-access-flow.mmd"
  "diagrams/ansible-control-flow.mmd"
  "templates/ufw-rules.example.sh"
  "templates/ssh-hardening-checklist.md"
  "templates/lab-inventory.example.ini"
  "templates/network-device-vars.example.yml"
  "ansible/inventory.example.ini"
  "ansible/README.md"
  "ansible/playbooks/ping-lab.yml"
  "ansible/playbooks/show-version.yml"
  "ansible/playbooks/backup-running-config.example.yml"
  "ansible/playbooks/show-interfaces.example.yml"
  "ansible/playbooks/show-inventory.example.yml"
  "ansible/group_vars/all.example.yml"
  "ansible/group_vars/cisco_ios.example.yml"
  "ansible/group_vars/arista_eos.example.yml"
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
  "product/linkedin-launch-post.md"
  "product/reddit-launch-guidance.md"
  "product/content-expansion-ideas.md"
  "product/video-expansion-roadmap.md"
  "product/linkedin-launch-post-v2.md"
  "product/reddit-value-first-post.md"
  "product/paid-bundle-v0.1-outline.md"
  "product/gumroad-listing-draft.md"
  "product/launch-sequence-tonight.md"
  "scripts/package-release.sh"
  "scripts/bootstrap-lab-host.example.sh"
  "scripts/setup-ufw-baseline.example.sh"
  "scripts/validate-lab-host.example.sh"
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
  "README.md:v0.1 public foundation"
  "README.md:Key Features"
  "README.md:Why This Project Exists"
  "README.md:Future Roadmap"
  "README.md:Visual Preview"
  "README.md:assets/diagrams/lab-topology-placeholder.svg"
  "README.md:assets/diagrams/remote-access-flow-placeholder.svg"
  "README.md:assets/diagrams/ansible-control-flow-placeholder.svg"
  "README.md:docs/hardware-bom.md"
  "README.md:docs/lab-deployment-checklist.md"
  "README.md:ansible/playbooks/show-interfaces.example.yml"
  "README.md:blog/"
  "README.md:blog/build-secure-linux-network-engineering-lab.md"
  "RELEASE_NOTES.md:v0.1.0"
  ".github/pull_request_template.md:Safety Review"
  ".github/ISSUE_TEMPLATE/config.yml:blank_issues_enabled"
  ".github/ISSUE_TEMPLATE/documentation-improvement.md:Documentation improvement"
  ".github/ISSUE_TEMPLATE/security-sanitization-review.md:Security or sanitization review"
  "assets/README.md:Assets"
  "assets/screenshots/README.md:Screenshot Assets"
  "assets/diagrams/README.md:Diagram Assets"
  "assets/diagrams/lab-topology-placeholder.svg:Lab topology placeholder"
  "assets/diagrams/remote-access-flow-placeholder.svg:Remote access flow placeholder"
  "assets/diagrams/ansible-control-flow-placeholder.svg:Ansible control flow placeholder"
  "blog/README.md:Blog Drafts"
  "blog/build-secure-linux-network-engineering-lab.md:GNS3"
  "blog/build-secure-linux-network-engineering-lab.md:Ansible"
  "blog/build-secure-linux-network-engineering-lab.md:Linux"
  "blog/build-secure-linux-network-engineering-lab.md:remote access"
  "CHANGELOG.md:v0.1.0"
  "CHANGELOG.md:dist/"
  "CONTRIBUTING.md:sanitized examples"
  "CONTRIBUTING.md:Branch Naming"
  "CONTRIBUTING.md:No-Secrets Policy"
  "SECURITY.md:Sensitive Information Rules"
  "SECURITY.md:What Counts as a Security Concern"
  "LICENSE.md:No final open source license"
  "docs/security-hardening.md:SSH"
  "docs/hardware-bom.md:Hardware and BOM Guidance"
  "docs/lab-deployment-checklist.md:Lab Deployment Checklist"
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
  "docs/public-demo-walkthrough.md:Public Demo Walkthrough"
  "docs/screenshot-plan.md:Screenshot Plan"
  "diagrams/README.md:Diagram Strategy"
  "diagrams/rendering-notes.md:Diagram Rendering Notes"
  "diagrams/lab-topology.mmd:flowchart"
  "diagrams/remote-access-flow.mmd:flowchart"
  "diagrams/ansible-control-flow.mmd:flowchart"
  "product/free-vs-paid-scope.md:Stays Free"
  "product/free-vs-paid-scope.md:Free lab deployment checklist"
  "product/v0.1-launch-plan.md:v0.1"
  "product/pdf-bundle-table-of-contents.md:Paid PDF Bundle"
  "product/github-launch-readme-review.md:GitHub Launch README Review"
  "product/v0.1-release-summary.md:v0.1 Release Summary"
  "product/next-phase-roadmap.md:Next Phase Roadmap"
  "product/github-repo-description.md:Short Description"
  "product/v0.1-github-release-draft.md:Release Title"
  "product/social-launch-draft.md:Social Launch Draft"
  "product/linkedin-launch-post.md:LinkedIn Launch Post"
  "product/reddit-launch-guidance.md:Reddit Launch Guidance"
  "product/content-expansion-ideas.md:Content Expansion Ideas"
  "product/video-expansion-roadmap.md:Video Expansion Roadmap"
  "product/linkedin-launch-post-v2.md:LinkedIn Launch Post v2"
  "product/reddit-value-first-post.md:Reddit Value-First Post"
  "product/paid-bundle-v0.1-outline.md:Paid Bundle v0.1 Outline"
  "product/gumroad-listing-draft.md:Gumroad Listing Draft"
  "product/launch-sequence-tonight.md:Launch Sequence Tonight"
  "scripts/package-release.sh:tar"
  "scripts/bootstrap-lab-host.example.sh:DRY RUN"
  "scripts/setup-ufw-baseline.example.sh:APPLY=1"
  "scripts/validate-lab-host.example.sh:Safe read-only checks"
  "video/walkthrough-outline.md:Scene 1"
  "video/walkthrough-outline.md:Quick Demo Version"
  "video/ai-voiceover-script-draft.md:Target length: 5 to 7 minutes"
  "video/ai-voiceover-script-draft.md:Short Launch Video Version"
  "templates/ufw-rules.example.sh:ufw"
  "ansible/playbooks/ping-lab.yml:ansible.builtin.wait_for"
  "ansible/playbooks/show-version.yml:show version"
  "ansible/README.md:Vendor Grouping"
  "ansible/group_vars/cisco_ios.example.yml:cisco.ios.ios"
  "ansible/group_vars/arista_eos.example.yml:arista.eos.eos"
)

for check in "${required_terms[@]}"; do
  file="${check%%:*}"
  term="${check#*:}"
  if [[ -f "$file" ]] && ! grep -Fq "$term" "$file"; then
    echo "Required term not found in $file: $term"
    fail=1
  fi
done

ansible_example_playbooks=(
  "ansible/playbooks/backup-running-config.example.yml"
  "ansible/playbooks/show-interfaces.example.yml"
  "ansible/playbooks/show-inventory.example.yml"
)

for playbook in "${ansible_example_playbooks[@]}"; do
  if [[ -f "$playbook" ]]; then
    if ! grep -Fq "hosts:" "$playbook"; then
      echo "Ansible example playbook missing hosts: $playbook"
      fail=1
    fi
    if ! grep -Fq "tasks:" "$playbook"; then
      echo "Ansible example playbook missing tasks: $playbook"
      fail=1
    fi
  fi
done

while IFS= read -r script; do
  if ! bash -n "$script"; then
    echo "Shell script syntax check failed: $script"
    fail=1
  fi
done < <(find scripts -type f -name "*.sh" | sort)

if [[ "$fail" -ne 0 ]]; then
  echo "Validation failed."
  exit 1
fi

echo "Validation passed."
