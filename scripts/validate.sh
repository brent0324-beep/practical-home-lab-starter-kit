#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
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
  "CHANGELOG.md:v0.1.0"
  "CONTRIBUTING.md:sanitized examples"
  "SECURITY.md:Sensitive Information Rules"
  "LICENSE.md:No final open source license"
  "docs/security-hardening.md:SSH"
  "docs/remote-access.md:UFW"
  "docs/ansible-workflows.md:inventory"
  "docs/example-lab-topology.md:Management network"
  "docs/release-checklist.md:redaction-check.sh"
  "product/free-vs-paid-scope.md:Stays Free"
  "product/v0.1-launch-plan.md:v0.1"
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

if [[ "$fail" -ne 0 ]]; then
  echo "Validation failed."
  exit 1
fi

echo "Validation passed."
