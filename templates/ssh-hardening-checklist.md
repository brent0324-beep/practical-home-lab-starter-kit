# SSH Hardening Checklist

Use this checklist before relying on SSH for lab administration.

## Access

- [ ] Use a named admin account instead of direct root access.
- [ ] Install a unique public SSH key for the admin account.
- [ ] Confirm sudo access works for the admin account.
- [ ] Keep a recovery console or working session available while changing SSH.

## Server Settings

Review the active SSH server configuration:

```bash
sudo sshd -T | sort
```

Target posture:

- [ ] Direct root SSH login disabled.
- [ ] Public key authentication enabled.
- [ ] Password-based SSH disabled when keys are confirmed working.
- [ ] X11 forwarding disabled unless explicitly needed.
- [ ] Allowed users or groups limited to lab administrators.

## Firewall

- [ ] UFW default incoming policy is deny.
- [ ] SSH is allowed only from trusted admin networks.
- [ ] Remote access rules are documented.
- [ ] `sudo ufw status verbose` output matches the intended policy.

## Logging and Review

- [ ] SSH service logs are available.
- [ ] Failed login attempts are reviewed periodically.
- [ ] Old keys are removed when no longer needed.
- [ ] Local private keys are never committed to Git.
