#!/usr/bin/env bash
set -euo pipefail

echo "Running basic redaction check..."

fail=0

# High-signal patterns only. Avoid flagging documentation that merely says
# "do not commit passwords" or .gitignore rules like *.secret.
patterns=(
  "BEGIN RSA PRIVATE KEY"
  "BEGIN OPENSSH PRIVATE KEY"
  "BEGIN PRIVATE KEY"
  "AKIA[0-9A-Z]{16}"
  "ghp_[A-Za-z0-9_]{20,}"
  "github_pat_[A-Za-z0-9_]{20,}"
  "xox[baprs]-[A-Za-z0-9-]{10,}"
  "api[_-]?key[[:space:]]*[:=][[:space:]]*['\"][^'\"]+['\"]"
  "token[[:space:]]*[:=][[:space:]]*['\"][^'\"]+['\"]"
  "password[[:space:]]*[:=][[:space:]]*['\"][^'\"]+['\"]"
  "psk[[:space:]]*[:=][[:space:]]*['\"][^'\"]+['\"]"
)

for pattern in "${patterns[@]}"; do
  if grep -REIn --exclude-dir=.git --exclude="redaction-check.sh" "$pattern" .; then
    echo "Potential sensitive pattern found: $pattern"
    fail=1
  fi
done

if [[ "$fail" -ne 0 ]]; then
  echo "Redaction check failed."
  exit 1
fi

echo "Redaction check passed."
