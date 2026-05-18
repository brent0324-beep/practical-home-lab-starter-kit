#!/usr/bin/env bash
set -euo pipefail

# Example only. Review before running on any real lab host.
# Default behavior is dry-run: it prints the UFW commands and changes nothing.
# Set APPLY=1 only after replacing TRUSTED_ADMIN_NET with your private lab range.

APPLY="${APPLY:-0}"
TRUSTED_ADMIN_NET="${TRUSTED_ADMIN_NET:-10.10.0.0/16}"
LAB_MANAGEMENT_NET="${LAB_MANAGEMENT_NET:-10.10.10.0/24}"

run_or_print() {
  if [[ "$APPLY" == "1" ]]; then
    "$@"
  else
    printf 'DRY RUN:'
    printf ' %q' "$@"
    printf '\n'
  fi
}

echo "UFW baseline example."
echo "Trusted admin network: ${TRUSTED_ADMIN_NET}"
echo "Lab management network: ${LAB_MANAGEMENT_NET}"
echo "Review these private lab ranges before applying."

run_or_print sudo ufw default deny incoming
run_or_print sudo ufw default allow outgoing
run_or_print sudo ufw allow from "$TRUSTED_ADMIN_NET" to any port 22 proto tcp comment "SSH from trusted lab admin network"
run_or_print sudo ufw allow from "$LAB_MANAGEMENT_NET" to any port 3080 proto tcp comment "GNS3 from lab management subnet"
run_or_print sudo ufw logging on

echo "Dry-run complete. To apply after review, run: APPLY=1 $0"
