# labctl Quickstart

Estimated five-minute setup and deploy for fresh Brent-like environment:

1. Install container prerequisites
   - `docker` with permissions for your user (no `sudo` in commands below).
   - `containerlab` in `PATH`.
   - `sudo usermod -aG clab_admins <user>`, then fully log out and log back in.
2. Run validator checks:
   - `./scripts/validate_lab_specs.py`
3. Generate a topology from a saved profile:
   - `./scripts/labctl render labs/examples/two-node-point-to-point/lab.yaml --profile profiles/labs/two-node-ptp-fast.yaml --output /tmp/two-node-ptp.clab.yml`
4. Deploy the lab:
   - `./scripts/labctl deploy labs/examples/two-node-point-to-point/lab.yaml --profile profiles/labs/two-node-ptp-fast.yaml`
5. Confirm lifecycle status:
   - `./scripts/labctl status two-node-ptp`
6. Tear down cleanly:
   - `./scripts/labctl destroy two-node-ptp`

## Notes

- `labctl` always executes lifecycle actions through the `containerlab` binary.
- `destroy` requires an explicit lab name and does not provide bulk deletion.
- `startup_config` and bind source entries reject absolute paths and parent traversal
  (for example `../`) before any runtime command runs.
- The repository tracks only specs, schemas, and docs; local outputs are written to
  the `.clab.yml` path you specify.

## Network exposure and firewalls

By default, labctl labs are host-local. Each lab's management network is an
internal Docker bridge (for example `172.30.90.0/24` for the two-node example),
and the nodes are reachable only from the host running the lab. labctl does not
publish node ports to external interfaces, so a default lab is not exposed to
your LAN or the internet.

One important caveat if you plan to change that: containerlab uses Docker's
networking, and Docker manipulates iptables directly, ahead of UFW. Docker's
rules are evaluated in the FORWARD chain before UFW's INPUT rules see the
packet, so UFW does not govern container traffic by default. This is a known
Docker design decision, not a bug. It does not expose your labs on its own —
nothing routes to the lab bridges unless you add that routing — but it means
that if you later publish ports, bridge a lab to your LAN, or reach labs over a
VPN, UFW will not be the control protecting them.

If you need to restrict lab reachability once you introduce routing, the
reliable options are the Docker-provided DOCKER-USER iptables chain (rules
there apply before Docker's own and survive Docker restarts), binding to
localhost, or an upstream/cloud firewall that sits outside the host.

Remote access to labs (for example over WireGuard) is intentionally out of
scope for now and will be treated as an explicit, opt-in feature if a concrete
need arises — not something a lab does by default.
