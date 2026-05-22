# Golden Path Operational Workflow

## Purpose

The Golden Path is a small, repeatable workflow for validating a Linux-based
network engineering lab without jumping straight into configuration changes.

It connects the core parts of this starter kit:

- repo orientation
- Linux lab host baseline
- documented access model
- small GNS3 topology
- sanitized Ansible inventory
- read-only validation playbooks
- local validation and redaction checks
- generated review artifact

The goal is not to build the largest possible topology. The goal is to keep the
operational workflow understandable before scaling the lab.

## Intended Audience

This workflow is written for:

- network engineers building a first repeatable home lab
- students learning how Linux, GNS3, and Ansible fit together
- engineers who want a public-safe documentation habit
- lab builders who want a small workflow they can validate before expanding

It assumes curiosity and basic command-line comfort, not a production network or
expensive hardware.

## Prerequisites

Before following the Golden Path, have:

- a local clone of this repository
- a Linux lab host or VM used only for lab work
- GNS3 installed or planned as the topology layer
- Ansible available on the control system, or a plan to install it later
- a private management network for lab-only reachability
- sanitized local notes for access, inventory, and topology assumptions

Keep real values in local untracked files. Public examples should use
placeholders only.

## Step-By-Step Workflow

1. Start with repo orientation.

   Read `README.md`, then review the build path under `docs/`. Confirm where
   the lab topology, Linux host setup, security hardening, Ansible workflow, and
   validation checks live.

2. Define the Linux lab host baseline.

   Document the host role, expected services, update process, firewall posture,
   and where lab notes will be stored. Keep the baseline boring and easy to
   explain.

3. Document the access model.

   Write down how administration reaches the lab host. Prefer a trusted local
   network or private access path. Avoid broad remote exposure, shared secrets,
   and undocumented exceptions.

4. Build the smallest useful GNS3 topology.

   Start with one virtual router, one virtual switch, and one private management
   network. Confirm reachability manually before involving automation.

5. Create a sanitized Ansible inventory.

   Use `ansible/inventory.example.ini` as the public-safe reference. Keep real
   device values in a local untracked inventory file.

6. Run read-only validation playbooks.

   Begin with reachability and show-command style checks. The starter examples
   under `ansible/playbooks/` are designed to reinforce validation before
   configuration changes.

7. Run local repo validation and redaction checks.

   Before publishing notes, screenshots, diagrams, or walkthrough material, run:

   ```bash
   ./scripts/validate.sh
   ./scripts/redaction-check.sh
   bash -n scripts/*.sh
   git diff --check
   ```

8. Generate a review artifact.

   Save a short local review note that records what was checked, what passed,
   what needs cleanup, and what should not be published. Keep that note private
   if it includes real environment details.

## Security-First Reminders

- Treat remote access as a design decision, not a convenience toggle.
- Keep real inventories, keys, vault files, and device details out of Git.
- Use placeholder values in public examples.
- Review screenshots and terminal output before sharing.
- Run read-only checks before configuration-changing playbooks.
- Keep the topology small until the access model and validation flow are clear.

## Expected Outputs

By the end of the Golden Path, you should have:

- a documented lab host role
- a documented access model
- a small GNS3 topology plan
- a sanitized inventory reference
- read-only Ansible validation output
- clean local validation and redaction checks
- a private review artifact for your own notes

These outputs are intentionally modest. They prove the workflow before the lab
gets larger.

## What Not To Do

- Do not commit real credentials, tokens, keys, private addresses, account data,
  or private environment details.
- Do not expose lab services broadly just to make remote access easier.
- Do not automate configuration changes before basic reachability and inventory
  assumptions are validated.
- Do not publish screenshots without reviewing prompts, paths, tabs, and command
  output.
- Do not grow the topology faster than the documentation and validation process
  can explain.

## Next Expansion Ideas

After the Golden Path works, expand one layer at a time:

- add a second vendor or network OS image
- add a configuration backup workflow
- add interface and routing validation checks
- create a troubleshooting checklist from real lab failures
- add monitoring or log collection for lab-only services
- record a short walkthrough using sanitized terminal output
- turn the review artifact into a repeatable worksheet
