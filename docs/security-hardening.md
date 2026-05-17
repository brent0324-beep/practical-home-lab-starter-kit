# Security Hardening

Home labs are still infrastructure. They may not hold production data, but they
can expose your network if remote access, SSH, firewall policy, and secrets are
handled casually.

## Minimum Baseline

- Keep the OS patched.
- Use a normal admin account with sudo.
- Disable direct root SSH login.
- Prefer SSH keys.
- Use UFW or another host firewall.
- Keep real secrets out of Git.
- Back up important configs before large changes.

## SSH Hardening

Review `/etc/ssh/sshd_config` or the distribution-specific drop-in directory.
Common settings to evaluate:

```text
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
X11Forwarding no
AllowUsers labadmin
```

Apply changes carefully:

```bash
sudo sshd -t
sudo systemctl reload ssh
```

Keep a known-good session open while testing a new session.

## Firewall Baseline

UFW is enough for many small labs:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 10.10.0.0/16 to any port 22 proto tcp
sudo ufw enable
sudo ufw status verbose
```

Adapt the source network to your trusted admin subnet. Do not blindly copy rules
from public examples.

## Secret Handling

Never commit:

- Private SSH keys.
- Real device credentials.
- VPN keys or PSKs.
- Cloud tokens.
- Real customer or employer data.
- Screenshots containing private inventory details.

Use placeholders in examples and local ignored files for real values.

## Maintenance Routine

Weekly:

- Apply package updates.
- Review failed SSH login attempts.
- Confirm firewall status.
- Check disk usage.

Monthly:

- Export or back up important GNS3 projects.
- Review stale users and keys.
- Confirm that local private files are ignored by Git.
- Run the repo redaction check before publishing changes.
