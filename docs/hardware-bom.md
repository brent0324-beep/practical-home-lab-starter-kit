# Hardware and BOM Guidance

This guide gives general hardware guidance for a Linux-based network engineering
home lab. It avoids exact prices because hardware availability and pricing
change often.

## Lab Host Profiles

| Profile | Good For | General Shape |
| --- | --- | --- |
| Budget | Learning Linux, GNS3 basics, small Ansible tests | Used mini PC, older desktop, or modest VM host |
| Balanced | Multiple GNS3 nodes, repeatable automation practice | Modern mini PC or small desktop with more RAM and NVMe |
| Power-user | Larger topologies, multiple appliances, heavier testing | Workstation-class desktop or dedicated server-style host |

## CPU Guidance

Budget:

- 4 cores can work for small labs.
- Prefer hardware virtualization support.
- Avoid very old CPUs if GNS3 appliances feel sluggish.

Balanced:

- 6 to 8 modern cores is a practical sweet spot.
- Higher single-thread performance helps interactive lab work.
- More cores help when multiple virtual devices run at once.

Power-user:

- 8 or more cores gives room for larger topologies.
- Prioritize stable thermals under sustained load.
- Avoid buying more CPU than your RAM and storage can support.

## RAM Guidance

- 16 GB can support a modest lab.
- 32 GB is a stronger target for repeated GNS3 work.
- 64 GB or more is useful for larger topologies and heavier appliances.

RAM is often the first real limit in a network lab. If choosing between a small
CPU upgrade and more RAM, more RAM is usually the safer lab investment.

## NVMe and Storage Guidance

- Use SSD or NVMe storage for the lab host.
- Keep enough space for GNS3 projects, appliance disks, logs, and backups.
- Prefer a clean directory structure for lab notes and exported projects.
- Back up important GNS3 projects before major changes.

Avoid running active lab workloads from slow external drives unless you are only
testing very small topologies.

## NIC Considerations

- One reliable NIC is enough for many virtual-only labs.
- Two NICs can help separate home LAN access from lab management or external
  test paths.
- USB NICs can be useful, but quality varies.
- Document which interface is used for host access, GNS3 bridges, and lab
  management.

For public examples, use placeholder interface names and private lab ranges.

## Noise, Power, and Location

- Mini PCs are quiet and power-efficient for most starter labs.
- Old rack servers can be loud, power-hungry, and inconvenient at home.
- Desktops may be a good middle ground if you need more RAM or expansion.
- Place the host where cooling and network access are reliable.

The best home lab host is one you can leave running, patch, and actually use.

## What to Avoid

- Hardware with too little RAM for your intended topology.
- Very slow disks for virtual appliance storage.
- Loud gear you will not tolerate running.
- Unsupported NICs or Wi-Fi-only lab host designs.
- Mixing real production equipment details into public lab docs.
- Building a large topology before the small version is stable.

Start with a host that can run one router, one switch, and Ansible checks
comfortably. Expand after the workflow is repeatable.
