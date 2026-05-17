#!/usr/bin/env bash
set -euo pipefail

# Sanitized UFW example for a private lab host.
# Review and adapt before running on any real system.

TRUSTED_ADMIN_NET="10.10.0.0/16"
LAB_MANAGEMENT_NET="10.10.10.0/24"

sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH from trusted private admin networks only.
sudo ufw allow from "$TRUSTED_ADMIN_NET" to any port 22 proto tcp comment "SSH from trusted lab admin network"

# Optional GNS3 web/API access from the lab management subnet.
sudo ufw allow from "$LAB_MANAGEMENT_NET" to any port 3080 proto tcp comment "GNS3 from lab management subnet"

# Optional ICMP troubleshooting is handled by the host OS and UFW defaults.

sudo ufw logging on
sudo ufw --force enable
sudo ufw status verbose
