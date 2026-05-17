# Remote Access

Remote access is useful, but it should be treated as part of the lab design, not
as an afterthought. The safest default is to keep the lab reachable only from
your local network. If you need external access, prefer a private VPN or a
trusted zero-trust access tool over exposing SSH directly.

## Recommended Options

Local-only access:

- Best for most labs.
- Simple to secure and troubleshoot.
- Requires being on the home network.

VPN access:

- Good for travel or remote study.
- Keeps services off the open internet.
- Requires careful key and device management.

SSH bastion pattern:

- Useful when you have multiple lab hosts.
- One hardened entry point.
- Requires strict firewall and logging.

## SSH Baseline

Recommended posture:

- Use SSH keys.
- Disable direct root login.
- Limit allowed users.
- Use UFW to restrict SSH to trusted source networks.
- Keep logs enabled.
- Test a second session before closing a working session.

Avoid:

- Exposing SSH broadly.
- Reusing personal passwords across devices.
- Copying private keys into lab repos.
- Publishing screenshots that show real hostnames or addresses.

## UFW Example

See `templates/ufw-rules.example.sh` for a sanitized starting point. Review each
rule before applying it to your system.

Typical policy:

```text
default deny incoming
default allow outgoing
allow SSH from trusted admin subnet
allow lab management traffic from the lab host
```

## Operational Notes

Record the remote access method in your lab documentation:

- Who should be able to connect.
- From where.
- Using which authentication method.
- What services are reachable.
- How access is disabled during an incident.

Remote access should be boring, narrow, and easy to audit.
