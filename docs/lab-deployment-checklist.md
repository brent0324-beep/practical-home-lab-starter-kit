# Lab Deployment Checklist

Use this checklist before treating a lab host and topology as ready for regular
practice. Keep local values private and use sanitized examples in public notes.

## Linux Host Readiness

- [ ] Supported Linux release installed.
- [ ] Normal admin user created.
- [ ] System packages updated.
- [ ] Hostname documented with a sanitized public equivalent.
- [ ] SSH service installed and reachable from trusted networks.
- [ ] Disk space checked for GNS3 projects and backups.
- [ ] CPU and RAM sufficient for the first topology.
- [ ] Lab workspace directory created.

Suggested checks:

```bash
hostnamectl
ip addr show
ip route show
df -h
free -h
```

## Remote Access Readiness

- [ ] SSH keys tested.
- [ ] Direct root SSH login disabled where appropriate.
- [ ] Password-based SSH disabled after key access is verified.
- [ ] UFW default incoming policy set to deny.
- [ ] SSH allowed only from trusted private networks.
- [ ] Remote access path documented.
- [ ] Recovery access plan confirmed before firewall changes.

Suggested checks:

```bash
sudo sshd -t
sudo ufw status verbose
```

## GNS3 Readiness

- [ ] GNS3 installed or reachable.
- [ ] First project created.
- [ ] Device image versions documented privately.
- [ ] Management network planned.
- [ ] Virtual router and switch nodes start cleanly.
- [ ] Linux host can reach management interfaces.
- [ ] Topology diagram or notes created.

Suggested checks:

```bash
ping 10.10.10.11
ping 10.10.10.21
```

These addresses are examples only. Replace them with your private lab values.

## Ansible Readiness

- [ ] Ansible installed on the control node.
- [ ] Inventory copied from example to a local untracked file.
- [ ] Device groups reflect the topology.
- [ ] Vendor group vars reviewed.
- [ ] Read-only playbooks tested first.
- [ ] Output reviewed for sensitive details before sharing.

Suggested checks:

```bash
ansible-inventory -i ansible/inventory.example.ini --list
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/ping-lab.yml
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/show-version.yml
```

## Security and Sanitization

- [ ] No real credentials in Git.
- [ ] No private keys, PSKs, or tokens in Git.
- [ ] No account data or private environment details in Git.
- [ ] Public examples use placeholder names and private lab ranges.
- [ ] Screenshots reviewed before sharing.
- [ ] Diagrams reviewed before sharing.

## Repo Validation

Run before publishing changes:

```bash
./scripts/validate.sh
./scripts/redaction-check.sh
bash -n scripts/*.sh
git diff --check
```

## Ready Criteria

- [ ] The lab can be explained from the README, diagrams, and topology notes.
- [ ] The Linux host is reachable through a controlled path.
- [ ] GNS3 nodes are reachable on the management network.
- [ ] Ansible read-only checks run against test devices.
- [ ] Public docs contain sanitized examples only.
