# Ansible Examples

This directory contains sanitized Ansible examples for a network engineering
home lab. Most examples are read-only device checks. The backup example reads
device configuration and writes a local artifact for private lab review.

## Layout

```text
ansible/
  inventory.example.ini
  group_vars/
    all.example.yml
    cisco_ios.example.yml
    arista_eos.example.yml
  playbooks/
    ping-lab.yml
    show-version.yml
    show-interfaces.example.yml
    show-inventory.example.yml
    backup-running-config.example.yml
```

## Inventory Layout

`inventory.example.ini` uses sanitized hostnames and private lab addresses.
Copy it to a local untracked inventory before adding real lab devices.

Suggested local pattern:

```bash
cp ansible/inventory.example.ini ansible/inventory.ini
```

Do not commit real device inventory, real usernames, private keys, passwords,
tokens, PSKs, or private environment details.

## Vendor Grouping

Use inventory groups to separate vendors or network operating systems. Example
group variable files are provided for:

- `group_vars/cisco_ios.example.yml`
- `group_vars/arista_eos.example.yml`

In a real local lab, copy example vars to local files that match your inventory
group names and keep sensitive values outside Git.

## Safe Starter Playbooks

The example playbooks collect basic information and local artifacts:

- Reachability check.
- Version output.
- Interface summary.
- Inventory or hardware summary.
- Running config backup to a local output directory.

Review command output before sharing it. Even read-only commands can reveal
private hostnames, serial numbers, interface descriptions, or topology details.

## Local Secret Handling

If your lab needs secrets, use a local ignored file, environment-specific secret
handling, or Ansible Vault. Do not add real secrets to these example files.
