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
