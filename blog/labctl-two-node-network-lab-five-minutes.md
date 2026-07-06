# A running two-node network lab in five minutes, from one YAML file

I spend a lot of time standing up throwaway network environments to reproduce a
bug, test a config change, or try something before it touches anything real. The
setup tax was always the annoying part. Containerlab already solved the hard
problem of running network topologies as containers, but I still found myself
hand-writing topology files, remembering the same boilerplate, and fixing the
same small mistakes every time.

So I built a thin layer on top of it called `labctl`: you describe a lab in a
short YAML spec, and it renders a valid Containerlab topology, deploys it, and
tears it down cleanly. Saved profiles let me redeploy my most common labs with
a single command. This post walks through the fastest possible path: a two-node
lab, running, in about five minutes.

## What you need first

A Linux host with Docker and Containerlab installed. One setup step that trips
people up: Containerlab gates Docker access through a group, so add yourself to
it and start a fresh login session before you deploy.

```bash
sudo usermod -aG clab_admins "$USER"
# then log out and back in (a new login session, not just a new terminal)
groups | grep clab_admins
```

Skip the re-login and your first deploy fails with a permission error that looks
scarier than it is. That is the whole gotcha.

## The spec

Here is a complete two-node `labctl` spec: two Linux nodes wired together, each
with a management address and a startup config.

```yaml
name: two-node-ptp
description: "Two-router point-to-point lab scaffold for quick routing exercises."
api_version: "1.0"
mgmt_ipv4_subnet: "172.30.90.0/24"
nodes:
  router-a:
    kind: linux
    image: docker.io/nicolaka/netshoot:v0.16
    mgmt_ipv4: 172.30.90.111
    startup_config: startup/router-a.cfg
    binds:
      - startup/router-a.cfg:/tmp/router-a.cfg:ro
  router-b:
    kind: linux
    image: docker.io/nicolaka/netshoot:v0.16
    mgmt_ipv4: 172.30.90.112
    startup_config: startup/router-b.cfg
    binds:
      - startup/router-b.cfg:/tmp/router-b.cfg:ro
links:
  - endpoints:
      - router-a:eth1
      - router-b:eth1
```

That is it. Two nodes, one link, a management subnet. The `netshoot` image is a
networking-tools container, so each node comes with `ping`, `tcpdump`,
`iproute2`, and the rest already inside. That makes it handy for testing
connectivity once the lab is up.

## Deploy it

The repo ships this lab under `labs/examples/two-node-point-to-point/`. The
example spec is variable-friendly, so this command applies the included saved
profile for the addressing shown above.

```bash
./scripts/labctl deploy labs/examples/two-node-point-to-point/lab.yaml \
  --profile profiles/labs/two-node-ptp-fast.yaml
```

A few seconds later, both nodes are running:

```text
╭────────────────────────────┬───────────┬─────────┬────────────────╮
│            Name            │   Image   │  State  │ IPv4 Address   │
├────────────────────────────┼───────────┼─────────┼────────────────┤
│ clab-two-node-ptp-router-a │ netshoot  │ running │ 172.30.90.111  │
│ clab-two-node-ptp-router-b │ netshoot  │ running │ 172.30.90.112  │
╰────────────────────────────┴───────────┴─────────┴────────────────╯
```

Drop into a node and confirm the link works:

```bash
docker exec -it clab-two-node-ptp-router-a ping 172.30.90.112
```

## Saved profiles: the part that actually saves time

The single spec is nice, but the reason I use this daily is profiles. A profile
is a set of saved variables, so a lab I run constantly becomes one command with
no editing:

```bash
./scripts/labctl deploy labs/examples/two-node-point-to-point/lab.yaml \
  --profile profiles/labs/two-node-ptp-fast.yaml
```

Same topology, my preferred addressing and settings applied, zero typing.
Multiply that across the handful of labs I spin up in a week and it is the
difference between "let me set that up" and "it is already running."

## Tear it down

Cleanup is scoped and explicit. It removes exactly the lab you name and nothing
else:

```bash
./scripts/labctl destroy two-node-ptp
```

Every topology `labctl` renders carries managed labels, and lifecycle state is
tracked locally. `destroy` will not prune unrelated containers, and it refuses
to act on a lab name it did not deploy. That constraint mattered enough to me
that it is enforced in code, not just convention.

## Why the spec, not just Containerlab directly

Containerlab is the engine here. I am not reimplementing any of it. What the
spec buys you is a smaller, validated surface: the fields you actually change,
checked before anything runs, with saved profiles on top. It is also a clean
contract. Because a lab is just a validated YAML document, anything that can
emit that document can drive the engine. That is where this goes next: a chat or
operational interface that takes "give me a three-node BGP lab" and hands the
engine a spec.

For now, though, the win is the boring one that compounds: I think of a
topology, and it is running before I have finished my coffee.

`labctl` is open source. The two-node example above ships in the repo, along
with a three-node BGP lab if you want something with more moving parts.
