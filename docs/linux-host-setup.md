# Linux Host Setup

This guide assumes Ubuntu Server or Debian on a dedicated lab host, mini PC, or
VM. The commands are examples and should be adapted to your distribution,
hardware, and local policy.

## Baseline Goals

- Use a supported Linux release.
- Keep the host updated.
- Use a normal admin user with sudo.
- Enable SSH key-based access.
- Apply a simple host firewall.
- Keep GNS3 and Ansible project files organized.

## Initial Update

```bash
sudo apt update
sudo apt upgrade
sudo apt install git curl vim ufw python3 python3-venv python3-pip
```

Reboot after kernel or core system updates:

```bash
sudo reboot
```

## User and SSH Access

Create a named admin user for lab work. Do not use shared accounts for normal
administration.

```bash
sudo adduser labadmin
sudo usermod -aG sudo labadmin
```

Add your public SSH key to the new user's `authorized_keys` file. Use a unique
key for lab access when possible.

Recommended SSH posture:

- Disable direct root login.
- Prefer public key authentication.
- Keep a recovery path before closing your current SSH session.
- Avoid committing SSH config files that contain private host details.

## Useful Packages

```bash
sudo apt install ansible net-tools tcpdump bridge-utils
```

Install virtualization dependencies according to your GNS3 platform choice. For
local appliance labs, you may need KVM, libvirt, or Docker. Install only what you
use and document it in your lab notes.

## Workspace Layout

Create a predictable workspace:

```bash
mkdir -p ~/lab/{ansible,gns3-notes,diagrams,backups}
```

Keep public examples separate from local private files. A good pattern is to
copy `*.example.*` files into local names that are ignored by Git.

## Basic Health Checks

```bash
hostnamectl
ip addr
ip route
sudo ufw status verbose
ansible --version
```

Capture the host baseline in your notes:

- Linux distribution and version.
- CPU, RAM, and storage.
- GNS3 version.
- Ansible version.
- Lab management subnet.
- Remote access method.
