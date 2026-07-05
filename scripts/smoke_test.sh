#!/usr/bin/env bash
# labctl Phase 1 live smoke test — deploy/status/destroy + label-scoped
# teardown + state registry lifecycle against a real Docker daemon.
set -uo pipefail
cd /opt/products/practical-home-lab-starter-kit || { echo "FAIL: repo not found"; exit 1; }

LAB=two-node-ptp
SPEC=labs/examples/two-node-point-to-point/lab.yaml
PROFILE=profiles/labs/two-node-ptp-fast.yaml
LABEL=io.labctl.managed=true
FAIL=0

echo "=== 0. Preconditions ==="
groups | grep -q clab_admins && echo "  clab_admins: OK" || { echo "  clab_admins: MISSING (re-login needed)"; FAIL=1; }
docker ps >/dev/null 2>&1 && echo "  docker socket: OK" || { echo "  docker socket: DENIED"; FAIL=1; }
command -v containerlab >/dev/null && echo "  containerlab: $(containerlab version 2>/dev/null | awk '/version:/{print $2; exit}')" || { echo "  containerlab: MISSING"; FAIL=1; }
[ "$FAIL" -eq 0 ] || { echo "ABORT: preconditions failed"; exit 1; }

echo "=== 0b. Render sanity (mgmt IPs bare, mgmt block present) ==="
./scripts/labctl render "$SPEC" --profile "$PROFILE" > /tmp/${LAB}.render.yml 2>/dev/null
if grep -Eq 'mgmt-ipv4:.*/[0-9]+' /tmp/${LAB}.render.yml; then
  echo "  FAIL: node mgmt-ipv4 still carries a CIDR suffix"; FAIL=1
else
  echo "  node mgmt-ipv4 bare: OK"
fi
grep -Eq '^\s*ipv4-subnet:' /tmp/${LAB}.render.yml && echo "  mgmt.ipv4-subnet present: OK" || { echo "  FAIL: no topology-level mgmt subnet block"; FAIL=1; }
grep -q 'netshoot:v0.16' /tmp/${LAB}.render.yml && echo "  image tag v0.16: OK" || echo "  WARN: netshoot:v0.16 not found"
[ "$FAIL" -eq 0 ] || { echo "ABORT: render still malformed; do not deploy"; exit 1; }

echo "=== 1. Deploy ==="
./scripts/labctl deploy "$SPEC" --profile "$PROFILE" || { echo "  FAIL: deploy exited nonzero"; FAIL=1; }

echo "=== 2. Status ==="
./scripts/labctl status "$LAB" || { echo "  FAIL: status"; FAIL=1; }

echo "=== 3. Managed containers up (expect 2) ==="
N=$(docker ps --filter label=$LABEL --format '{{.Names}}' | wc -l)
docker ps --filter label=$LABEL
[ "$N" -eq 2 ] && echo "  count=2: OK" || { echo "  FAIL: expected 2, got $N"; FAIL=1; }

echo "=== 4. State registry tracks the lab ==="
if [ -f .labctl/state.json ] && grep -q "$LAB" .labctl/state.json; then echo "  tracked: OK"; else echo "  FAIL: $LAB not tracked"; FAIL=1; fi

echo "=== 5. Destroy ==="
./scripts/labctl destroy "$LAB" || { echo "  FAIL: destroy exited nonzero"; FAIL=1; }

echo "=== 6. Teardown clean (expect EMPTY) ==="
LEFT=$(docker ps -a --filter label=$LABEL --format '{{.Names}}' | wc -l)
docker ps -a --filter label=$LABEL
[ "$LEFT" -eq 0 ] && echo "  none remain: OK" || { echo "  FAIL: $LEFT managed containers left"; FAIL=1; }

echo "=== 7. State registry deregistered ==="
if [ -f .labctl/state.json ] && grep -q "$LAB" .labctl/state.json; then echo "  FAIL: $LAB still tracked (dirty deregister)"; FAIL=1; else echo "  deregistered: OK"; fi

echo "======================================"
[ "$FAIL" -eq 0 ] && echo "SMOKE TEST: PASS — clear for SMCPP checklist" || echo "SMOKE TEST: FAIL — do not authorize SMCPP"
exit $FAIL
