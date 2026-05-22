#!/usr/bin/env bash
set -euo pipefail

# Example only. This script prints the Golden Path command sequence.
# It does not contact devices, change host configuration, or write files.

echo "Golden Path demo: dry-run command sequence"
echo

echo "1. Orient in the repository:"
echo "   tree -L 2"
echo

echo "2. Review the lab foundation docs:"
echo "   less README.md"
echo "   less docs/golden-path-operational-workflow.md"
echo "   less docs/linux-host-setup.md"
echo "   less docs/security-hardening.md"
echo "   less docs/gns3-setup.md"
echo

echo "3. Inspect sanitized Ansible inventory examples:"
echo "   sed -n '1,160p' ansible/inventory.example.ini"
echo "   sed -n '1,160p' templates/lab-inventory.example.ini"
echo

echo "4. Preview read-only Ansible validation commands:"
echo "   ansible-inventory -i ansible/inventory.example.ini --list"
echo "   ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/ping-lab.yml"
echo "   ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/show-version.yml"
echo "   ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/show-interfaces.example.yml"
echo

echo "5. Run local repo validation before publishing:"
echo "   ./scripts/validate.sh"
echo "   ./scripts/redaction-check.sh"
echo "   bash -n scripts/*.sh"
echo "   git diff --check"
echo

echo "6. Generate a private review artifact:"
echo "   # Example only: write local notes outside public commits if they contain real lab details."
echo "   # A real workflow could summarize checks passed, gaps found, and next actions."
echo

echo "Real lab commands would go after manual reachability checks and only against private, authorized lab devices."
echo "Keep real inventories, keys, and environment details out of Git."
