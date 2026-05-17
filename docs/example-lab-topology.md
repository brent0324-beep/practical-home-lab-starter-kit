# Example Lab Topology

This sample topology shows how the starter kit pieces fit together. It is a
sanitized example, not a required design.

## Diagram Files

The diagram-ready source files live under `diagrams/`:

- `diagrams/lab-topology.mmd` shows the complete lab architecture.
- `diagrams/remote-access-flow.mmd` shows the approved remote access path.
- `diagrams/ansible-control-flow.mmd` shows how Ansible reaches lab devices.

See `docs/diagram-guide.md` for guidance on how these diagrams map to the
README, blog post, PDF bundle, and video walkthrough.

## Topology Summary

```text
Remote admin laptop
  |
  | SSH over VPN or trusted local network
  v
Linux lab host
  |-- GNS3 server
  |-- Ansible control workflow
  |-- UFW firewall
  |-- SSH service for administration
  |
  +-- Management network: 10.10.10.0/24
        |
        |-- lab-r1  10.10.10.11
        |-- lab-r2  10.10.10.12
        |-- lab-sw1 10.10.10.21
```

All values are placeholders. Replace them with your own private lab addresses
and hostnames.

## Components

The Linux lab host is the stable base. It stores notes, runs GNS3, hosts the
management bridge, and can act as the Ansible control node.

The GNS3 server runs virtual router and switch nodes. Keep the first topology
small: two routers, one switch, and a management connection back to the Linux
host.

The management network gives Ansible and SSH a predictable path to device
management interfaces. It should use private address space and should be
documented in the inventory and topology notes.

The Ansible control workflow starts with read-only validation:

1. Confirm the device management port is reachable.
2. Run a basic version command.
3. Save notes about device identity and platform.
4. Add backup or compliance tasks only after read-only checks are reliable.

The remote access path should be narrow. Use local access when possible. If
remote access is needed, prefer a private VPN or trusted access tool and keep SSH
restricted to expected source networks.

## Example Device Roles

| Device | Role | Example Address | Notes |
| --- | --- | --- | --- |
| `lab-host` | Linux lab host | `10.10.10.5` | Runs GNS3 and Ansible examples |
| `lab-r1` | Virtual router | `10.10.10.11` | First routing node |
| `lab-r2` | Virtual router | `10.10.10.12` | Second routing node |
| `lab-sw1` | Virtual switch | `10.10.10.21` | Access or transit switching |

## Operational Flow

1. Connect to the Linux lab host over the approved access path.
2. Start the GNS3 project and confirm device links are up.
3. Verify the management network from the Linux host.
4. Run the Ansible reachability playbook.
5. Run the read-only command collection playbook.
6. Update lab notes with any topology, inventory, or access changes.

## Documentation Artifacts

Keep these artifacts together:

- Topology diagram or ASCII map.
- Mermaid source diagrams.
- Management IP plan.
- Ansible inventory.
- Device image/version notes.
- Remote access notes.
- Change log and troubleshooting notes.
