#!/usr/bin/env bash
set -euo pipefail

# Example only. Review before running on any real lab host.
# Default behavior is dry-run: it prints suggested commands and changes nothing.
# Set APPLY=1 only after reviewing the package list and host requirements.

APPLY="${APPLY:-0}"

packages=(
  git
  curl
  vim
  ufw
  python3
  python3-venv
  python3-pip
  ansible
  tcpdump
)

run_or_print() {
  if [[ "$APPLY" == "1" ]]; then
    "$@"
  else
    printf 'DRY RUN:'
    printf ' %q' "$@"
    printf '\n'
  fi
}

echo "Bootstrap example for a sanitized Linux lab host."
echo "Review packages and distro compatibility before applying."

run_or_print sudo apt update
run_or_print sudo apt install -y "${packages[@]}"

echo "Suggested local workspace:"
echo "DRY RUN: mkdir -p ~/lab/{ansible,gns3-notes,diagrams,backups}"

if [[ "$APPLY" == "1" ]]; then
  mkdir -p "$HOME/lab"/{ansible,gns3-notes,diagrams,backups}
fi

echo "Complete. APPLY=${APPLY}"
