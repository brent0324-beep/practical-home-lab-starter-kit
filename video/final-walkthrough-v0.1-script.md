# Final Walkthrough v0.1 Narration Script

Target length: 3 to 5 minutes.

Tone: practical, engineer-to-engineer, concise, and educational.

## 0:00 Intro

[show top of GitHub repo]

This is the Practical Home Lab Starter Kit for Network Engineers.

The goal is simple: give a home lab enough structure that it is repeatable,
documented, and safe to share. This is not a production network design, and it
is not a giant lab build. It is a starting point for Linux, GNS3, Ansible, SSH,
UFW, diagrams, and validation habits.

## 0:20 Project Overview

[show README]

At the top of the README, the repo explains the basic idea. A lot of home labs
start as separate pieces: a Linux box, a GNS3 project, a few SSH sessions, some
Ansible tests, and notes in different places.

This repo puts those pieces into one public-safe structure. You can plan a small
topology, prepare a Linux lab host, connect virtual devices, run read-only
Ansible checks, and review the docs before publishing anything.

Everything here is sanitized. The examples are meant to show structure, not real
private values.

## 0:55 Hero Visual

[scroll to hero visual]

This overview image is the quick mental model for the lab.

There is an admin workstation, a controlled access path, a Linux lab host, GNS3,
Ansible, validation scripts, and documentation. The important part is not the
exact topology. The important part is that the access path, lab host, virtual
devices, automation, and review process are all connected.

That gives you a lab you can explain later, instead of a collection of one-off
terminal sessions.

## 1:25 Technical Diagrams

[scroll to Technical Diagrams]

The Technical Diagrams section is where the README moves from the high-level
view into the supporting architecture.

The editable sources live in the `diagrams` directory as Mermaid files. The
rendered assets under `assets` are for README and demo use. That split matters:
you can keep the diagrams versioned as text, then render visuals for readers,
videos, or documentation.

## 1:55 Example Remote Access Flow

[show Example Remote Access Flow]

The remote access diagram is intentionally conservative.

The lab should not depend on broad exposed access. The pattern is an approved
trusted path into the Linux lab host, with filtering and host firewall policy in
front of the services you care about.

For a real lab, you would adapt this to your own private network and access
model. For the public repo, the diagram stays generic and avoids exposing
private environment details.

## 2:25 Example Ansible Control Flow

[show Example Ansible Control Flow]

The Ansible control flow is also deliberately small.

Inventory and group variables feed safe playbooks. Those playbooks reach lab
devices over the private management path, then produce local review artifacts.

The first milestone is not pushing configuration. The first milestone is proving
that inventory, reachability, credentials handling, and device type assumptions
are correct.

## 2:55 Ansible Workflows

[open Ansible workflows]

The Ansible workflow doc keeps that same pattern.

Start with the example inventory and group vars. Copy them before adding private
values. Then run basic checks: inventory parsing, reachability, and a read-only
show command.

The workflow is: update topology notes, update inventory, confirm reachability,
run a read-only check, save useful output, then make one controlled change.

That order is slower than guessing, but it is much easier to troubleshoot.

## 3:35 Validation

[show validation section]

Before publishing changes, the repo has a small validation flow.

Run the repository validation script, run the redaction check, run shell syntax
checks, and check the Git diff for whitespace issues. These checks do not
replace human review, but they catch common misses: missing files, incomplete
docs, shell syntax problems, and high-signal secret patterns.

For public lab content, that review step is part of the workflow, not an
afterthought.

## 4:05 Hardware BOM

[open hardware-bom.md]

The hardware BOM guide is intentionally practical.

It does not chase exact prices. Instead, it describes budget, balanced, and
power-user lab host profiles. For many starter labs, RAM and storage matter more
than buying the biggest CPU. A small reliable host that you can leave running,
patch, and document is usually more useful than loud hardware you avoid using.

Start with enough capacity for one router, one switch, and the Ansible checks.
Expand once the workflow is stable.

## 4:40 Closing CTA

[return to README or repo top]

That is the v0.1 walkthrough: a small, secure, repeatable foundation for a home
network engineering lab.

Check out the repo, clone it, and adapt it safely for your own private lab. Keep
real inventories, secrets, account details, and environment-specific values out
of public commits.

Feedback is welcome, especially around the docs, diagrams, and starter workflow.
