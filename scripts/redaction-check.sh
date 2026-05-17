#!/usr/bin/env bash
set -euo pipefail

echo "Running basic redaction check..."

patterns=(
  "password"
  "passwd"
  "secret"
  "private_key"
  "BEGIN RSA PRIVATE KEY"
  "BEGIN OPENSSH PRIVATE KEY"
  "token="
  "api_key"
  "psk"
)

fail=0

for pattern in "${patterns[@]}"; do
  if grep -RIn --exclude-dir=.git --exclude="redaction-check.sh" "$pattern" .; then
    echo "Potential sensitive pattern found: $pattern"
    fail=1
  fi
done

if [[ "$fail" -ne 0 ]]; then
  echo "Redaction check failed."
  exit 1
fi

echo "Redaction check passed."
