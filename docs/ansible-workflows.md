# Ansible Workflows

The Ansible examples in this repo are intentionally small. The first goal is to
prove reachability and collect basic device information. Configuration changes
come later, after inventory, access, and documentation are reliable.

## Files

- `ansible/inventory.example.ini` contains sanitized lab hosts.
- `ansible/group_vars/all.example.yml` contains shared connection defaults.
- `ansible/playbooks/ping-lab.yml` tests reachability.
- `ansible/playbooks/show-version.yml` runs a read-only show command.

Copy examples before adding private values:

```bash
cp ansible/inventory.example.ini ansible/inventory.ini
cp ansible/group_vars/all.example.yml ansible/group_vars/all.yml
```

Keep real local files out of public commits.

## Basic Commands

Run an inventory check:

```bash
ansible-inventory -i ansible/inventory.example.ini --list
```

Run a reachability test:

```bash
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/ping-lab.yml
```

Run a read-only command collection playbook:

```bash
ansible-playbook -i ansible/inventory.example.ini ansible/playbooks/show-version.yml
```

## Workflow Pattern

1. Update topology notes.
2. Update inventory.
3. Confirm SSH or API reachability.
4. Run a read-only check.
5. Save command output if useful.
6. Make one controlled change.
7. Verify and document the result.

## Inventory Guidelines

- Use descriptive names like `lab-r1`.
- Group devices by role, such as routers and switches.
- Keep connection settings in group vars where possible.
- Avoid putting secrets directly in inventory.
- Use Ansible Vault or local environment handling for sensitive values.

## Before Configuration Changes

Do not start by pushing configs. First prove that you can:

- Reach every target device.
- Identify the network OS correctly.
- Collect a version or facts output.
- Back up the current config.
- Roll back manually if needed.

The sample playbooks are read-only by design so the first pass is safe.
