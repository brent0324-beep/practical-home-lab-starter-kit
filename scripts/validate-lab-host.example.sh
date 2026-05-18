#!/usr/bin/env bash
set -euo pipefail

# Example only. Safe read-only checks for a Linux lab host.
# This script does not change host configuration.

echo "Lab host validation example"
echo

echo "Host identity:"
hostnamectl 2>/dev/null || hostname
echo

echo "Network addresses:"
ip addr show
echo

echo "Routes:"
ip route show
echo

echo "SSH service status:"
systemctl is-active ssh 2>/dev/null || true
echo

echo "UFW status:"
sudo ufw status verbose 2>/dev/null || echo "UFW status unavailable or sudo required."
echo

echo "Tool availability:"
for tool in git python3 ansible ansible-playbook; do
  if command -v "$tool" >/dev/null 2>&1; then
    echo "found: $tool"
  else
    echo "missing: $tool"
  fi
done
