# AI Voiceover Script Draft

## Opening

This practical home lab starter kit is for network engineers who want a secure,
repeatable place to practice Linux, GNS3, Ansible, and remote access workflows.

The goal is not to build a massive virtual data center on day one. The goal is
to build a small lab that is documented, reachable, and safe to improve.

## Section 1: Architecture

Start with one Linux host. This host runs GNS3, stores your lab notes, and can
act as the Ansible control node. Keep the management network simple, using a
private lab subnet and boring device names like lab-r1 and lab-sw1.

## Section 2: Security

Before adding complexity, harden the basics. Use SSH keys, disable direct root
login, restrict inbound access with UFW, and keep real secrets out of Git.

## Section 3: GNS3

Create a small GNS3 project with one router and one switch. Confirm the host can
reach the device management interfaces before you troubleshoot automation.

## Section 4: Ansible

Use the sample inventory and read-only playbooks to test reachability and collect
basic version output. Once that works, you can add backups and controlled config
changes.

## Closing

The free repo gives you the foundation: documentation, examples, templates, and
validation scripts. Build the small version first, then expand it one reliable
step at a time.
