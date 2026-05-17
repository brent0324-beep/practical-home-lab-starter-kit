#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
  "docs/architecture.md"
  "docs/linux-host-setup.md"
  "docs/gns3-setup.md"
  "docs/remote-access.md"
  "docs/security-hardening.md"
  "docs/ansible-workflows.md"
  "docs/troubleshooting.md"
  "docs/product-roadmap.md"
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
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file"
    exit 1
  fi
done

echo "Validation passed."
