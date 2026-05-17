# AI Voiceover Script Draft

Target length: 5 to 7 minutes.

## Scene 1: Opening

This practical home lab starter kit is for network engineers who want a secure,
repeatable place to practice Linux, GNS3, Ansible, and remote access workflows.

The point is not to build a massive virtual data center on day one. The point is
to build a small lab that you can explain, rebuild, secure, and improve.

Everything in this repo uses sanitized examples. The hostnames, addresses, and
paths are placeholders. Keep real credentials, private keys, tokens, account
details, and private environment data out of public commits.

## Scene 2: Full Lab Topology

Start with the full topology diagram.

At the top is the remote admin workstation. That is the laptop or desktop you
use to administer the lab.

Next is the home router or firewall. This represents the edge of the home
network. The lab should not depend on broad exposed access. If remote access is
needed, use a trusted local network path or a private VPN-style access path.

The center of the design is the Linux lab host. This host runs SSH, UFW, lab
notes, GNS3, and optionally the Ansible control workflow. Treat this host like
infrastructure. Patch it, document it, and keep access narrow.

Behind the Linux host is the GNS3 server. GNS3 runs the virtual routers and
switches used for practice. In the starter topology, the sample nodes are
`lab-r1`, `lab-r2`, and `lab-sw1`.

The devices attach to a management network. The example uses private lab address
space, such as `10.10.10.0/24`. Replace that with your own private lab plan.

## Scene 3: Remote Access Flow

Now zoom in on remote access.

The safest default is local-only access. If you need access while away from the
lab, keep it private and intentional. The diagram shows the admin workstation
connecting over a trusted path, through the home firewall, to the Linux lab host.

On the Linux host, UFW should use a default-deny incoming policy. SSH should be
allowed only from trusted networks. SSH should use keys, not shared reusable
passwords, and direct root login should be disabled.

This gives you a simple rule: remote access should be boring, narrow, and easy
to audit.

## Scene 4: Linux Host and GNS3

The Linux host is where the lab becomes repeatable.

Use it to store project notes, run GNS3, keep templates, and execute validation
commands. Keep the first GNS3 project small. One router and one switch are
enough to prove the workflow. Two routers and one switch are enough to practice
basic routing and management access.

Before troubleshooting automation, confirm the basics. Is the GNS3 project
running? Are links up? Can the Linux host reach the management interface? Does
the inventory match the topology?

Most lab problems are mismatches between diagrams, inventory, firewall rules,
and actual device state.

## Scene 5: Ansible Control Flow

The Ansible control flow is intentionally simple.

Start with a sanitized inventory. Use placeholder names like `lab-r1` and
private lab addresses. Put shared connection defaults in group variables. Then
run read-only playbooks.

The first playbook checks whether the device management port is reachable from
the control node. The second playbook runs a basic `show version` command.

That is enough for a useful first milestone. You have proved the lab host, GNS3
topology, management network, inventory, and Ansible connection path all line up.

Only after that should you add backups, compliance checks, or configuration
changes.

## Scene 6: Templates and Guardrails

The repo includes templates for UFW rules, SSH hardening, lab inventory, and
network device variables. These are examples to copy and adapt, not files where
you should store real secrets.

Before publishing any change, run the validation script and the redaction check.
The validation script confirms required files exist and contain expected starter
content. The redaction check looks for high-signal secret patterns.

These checks do not replace human review. They are guardrails that make mistakes
less likely.

## Closing

The free repo gives you the foundation: documentation, examples, templates, and
diagram-ready architecture.

A future paid bundle may add a polished workbook, rendered diagrams, worksheets,
and deeper scenarios. But the public repo should remain useful on its own.

Build the small version first. Document what you built. Validate it. Then expand
the lab one reliable step at a time.
