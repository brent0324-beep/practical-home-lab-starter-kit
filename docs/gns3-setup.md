# GNS3 Setup

GNS3 is the network simulation layer for this starter kit. Keep the setup simple
at first: one project, one management subnet, and a few devices you can reach
from Ansible.

## Install Direction

Use the official GNS3 documentation for current package details. At a high
level, you will choose between:

- Local GNS3 server on the Linux host.
- GNS3 VM.
- Remote GNS3 server with a desktop client.

For a home lab, the local Linux host or GNS3 VM approach is usually easiest to
reason about.

## First Project

Create a project named `starter-routing-lab` or similar. Add:

- One router.
- One switch.
- One management cloud or bridge connected to the Linux host.
- A private management subnet such as `10.10.10.0/24`.

Example addressing:

```text
lab-r1  10.10.10.11
lab-r2  10.10.10.12
lab-sw1 10.10.10.21
```

These values are placeholders. Replace them with your own private lab plan.

## Project Hygiene

For each GNS3 project, document:

- Purpose of the lab.
- Device images and versions.
- Management IP plan.
- Login method.
- Starting configuration source.
- Known-good verification command.
- Cleanup or reset process.

Keep exported GNS3 projects out of public repositories if they contain licensed
images, real configs, or private details.

## Ansible Connectivity

Before writing playbooks, confirm basic reachability:

```bash
ping 10.10.10.11
ssh labadmin@10.10.10.11
```

Then test Ansible with the sample inventory:

```bash
ansible -i ansible/inventory.example.ini lab_network -m ping
```

Network devices often require platform-specific connection settings. The sample
files use conservative placeholders and should be adjusted for your device OS.

## Common Setup Mistakes

- Mixing management and lab traffic without documenting it.
- Changing GNS3 addressing but forgetting to update Ansible inventory.
- Using device images without recording their version.
- Troubleshooting automation before basic SSH reachability works.
- Exporting projects that contain private configs.
