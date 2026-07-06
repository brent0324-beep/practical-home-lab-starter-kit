# Session State

**Branch:** feature/labctl-phase2-network (Phase 2 committed, pending SMCPP)
**Session goal:** promote labctl Phase 2 network fixes through governed main
integration
**Last validated:** ./scripts/validate.sh PASS, live two-lab smoke test PASS

## Where things stand

labctl Phase 1 shipped to main (spec-driven Containerlab engine: validate /
render / deploy / status / destroy, managed-label scoping, saved profiles,
schema validation). A dev.to blog post and static cover are published.

Phase 2 is committed on feature/labctl-phase2-network and validated against
real Docker but not yet merged:
- Per-lab uniquely-named mgmt networks (clab-<labname>) prevent subnet
  collisions between coexisting labs.
- Stale-network preflight raises a clean labctl error on subnet mismatch.
- Failed deploys clean up their own network (no orphans).
- Destroy is scoped to a lab's own network; other labs untouched.
- Fixed the three-node BGP triangle example (had duplicate endpoints; had
  never actually been deployed, was broken and public on main since Phase 1).
- Smoke test now covers both example labs.

Live gate proven: 5 containers coexisting across 2 distinct networks,
scoped teardown, stale-network diagnostic all verified.

## Next up

- Authorize SMCPP + MAIN PROMOTION APPROVED to merge Phase 2 (also fixes the
  broken BGP example currently public on main).
- Remaining Phase 2 backlog item: decide mgmt-network exposure policy
  (host-local vs VPN-reachable) and document DOCKER-USER / UFW bypass in the
  quickstart. Leaning host-local; VPN deferred until a concrete need.
- Next content piece: three-node BGP lab walkthrough (now that it works).

## Loose threads

- SESSION_STATE is hand-maintained; a future governance ticket may add
  scripts/update_session_state.py to auto-fill the mechanical fields (branch,
  HEAD, last validation) while leaving curated prose untouched.
- VHS `Set Framerate` is ignored by the installed build; use the Pillow
  frame-reduction script for the dev.to 500-frame cap. Prefer smaller tape
  dimensions + MP4 for embedded demos.
- Consider a pyproject/pip install path so `python3 -m labctl` works without
  the ./scripts/labctl wrapper.
