#!/usr/bin/env bash
# labctl live smoke test: two-lab deploy/status/destroy, per-lab management
# networks, label-scoped teardown, and state registry lifecycle against Docker.
set -uo pipefail
cd /opt/products/practical-home-lab-starter-kit || { echo "FAIL: repo not found"; exit 1; }

TWO_NODE_LAB=two-node-ptp
TWO_NODE_SPEC=labs/examples/two-node-point-to-point/lab.yaml
TWO_NODE_PROFILE=profiles/labs/two-node-ptp-fast.yaml
TWO_NODE_TOPOLOGY=labs/examples/two-node-point-to-point/lab.clab.yml
TWO_NODE_RUNTIME=labs/examples/two-node-point-to-point/clab-${TWO_NODE_LAB}
TWO_NODE_RENDER=/tmp/${TWO_NODE_LAB}.render.yml

BGP_LAB=bgp-triangle
BGP_SPEC=labs/examples/three-node-bgp-triangle/lab.yaml
BGP_TOPOLOGY=labs/examples/three-node-bgp-triangle/lab.clab.yml
BGP_RUNTIME=labs/examples/three-node-bgp-triangle/clab-${BGP_LAB}
BGP_RENDER=/tmp/${BGP_LAB}.render.yml

LABEL=io.labctl.managed=true
FAIL=0

cleanup() {
  if command -v containerlab >/dev/null 2>&1; then
    [ -f "$TWO_NODE_TOPOLOGY" ] && containerlab destroy -t "$TWO_NODE_TOPOLOGY" --cleanup >/dev/null 2>&1 || true
    [ -f "$BGP_TOPOLOGY" ] && containerlab destroy -t "$BGP_TOPOLOGY" --cleanup >/dev/null 2>&1 || true
  fi
  rm -rf \
    "$TWO_NODE_RUNTIME" "$TWO_NODE_TOPOLOGY" "$TWO_NODE_RENDER" \
    "$BGP_RUNTIME" "$BGP_TOPOLOGY" "$BGP_RENDER" \
    .labctl
}

trap cleanup EXIT

render_lab() {
  lab="$1"
  spec="$2"
  profile="$3"
  render_out="$4"
  expected_network="$5"

  if [ -n "$profile" ]; then
    ./scripts/labctl render "$spec" --profile "$profile" > "$render_out" 2>/dev/null
  else
    ./scripts/labctl render "$spec" > "$render_out" 2>/dev/null
  fi

  if grep -Eq 'mgmt-ipv4:.*/[0-9]+' "$render_out"; then
    echo "  FAIL: $lab node mgmt-ipv4 still carries a CIDR suffix"; FAIL=1
  else
    echo "  $lab node mgmt-ipv4 bare: OK"
  fi
  grep -Eq '^\s*ipv4-subnet:' "$render_out" && echo "  $lab mgmt.ipv4-subnet present: OK" || { echo "  FAIL: $lab has no mgmt subnet block"; FAIL=1; }
  grep -Eq "^\s*network: ${expected_network}$" "$render_out" && echo "  $lab mgmt.network: OK" || { echo "  FAIL: $lab missing expected mgmt network ${expected_network}"; FAIL=1; }
  grep -q 'netshoot:v0.16' "$render_out" && echo "  $lab image tag v0.16: OK" || { echo "  WARN: $lab netshoot:v0.16 not found"; }
}

deploy_lab() {
  spec="$1"
  profile="$2"
  if [ -n "$profile" ]; then
    ./scripts/labctl deploy "$spec" --profile "$profile"
  else
    ./scripts/labctl deploy "$spec"
  fi
}

managed_count() {
  docker ps --filter label=$LABEL --format '{{.Names}}' | wc -l
}

echo "=== 0. Preconditions ==="
groups | grep -q clab_admins && echo "  clab_admins: OK" || { echo "  clab_admins: MISSING (re-login needed)"; FAIL=1; }
docker ps >/dev/null 2>&1 && echo "  docker socket: OK" || { echo "  docker socket: DENIED"; FAIL=1; }
command -v containerlab >/dev/null && echo "  containerlab: $(containerlab version 2>/dev/null | awk '/version:/{print $2; exit}')" || { echo "  containerlab: MISSING"; FAIL=1; }
[ "$FAIL" -eq 0 ] || { echo "ABORT: preconditions failed"; exit 1; }

echo "=== 0b. Render sanity ==="
render_lab "$TWO_NODE_LAB" "$TWO_NODE_SPEC" "$TWO_NODE_PROFILE" "$TWO_NODE_RENDER" "clab-two-node-ptp"
render_lab "$BGP_LAB" "$BGP_SPEC" "" "$BGP_RENDER" "clab-bgp-triangle"
[ "$FAIL" -eq 0 ] || { echo "ABORT: render still malformed; do not deploy"; exit 1; }

echo "=== 1. Deploy both labs ==="
deploy_lab "$TWO_NODE_SPEC" "$TWO_NODE_PROFILE" || { echo "  FAIL: two-node deploy exited nonzero"; FAIL=1; }
deploy_lab "$BGP_SPEC" "" || { echo "  FAIL: bgp-triangle deploy exited nonzero"; FAIL=1; }

echo "=== 2. Status both labs ==="
./scripts/labctl status "$TWO_NODE_LAB" || { echo "  FAIL: two-node status"; FAIL=1; }
./scripts/labctl status "$BGP_LAB" || { echo "  FAIL: bgp-triangle status"; FAIL=1; }

echo "=== 3. Managed containers up (expect 5) ==="
N=$(managed_count)
docker ps --filter label=$LABEL
[ "$N" -eq 5 ] && echo "  count=5: OK" || { echo "  FAIL: expected 5, got $N"; FAIL=1; }

echo "=== 4. Distinct management networks exist ==="
docker network inspect clab-two-node-ptp >/dev/null 2>&1 && echo "  clab-two-node-ptp: OK" || { echo "  FAIL: missing clab-two-node-ptp"; FAIL=1; }
docker network inspect clab-bgp-triangle >/dev/null 2>&1 && echo "  clab-bgp-triangle: OK" || { echo "  FAIL: missing clab-bgp-triangle"; FAIL=1; }

echo "=== 5. State registry tracks both labs ==="
if [ -f .labctl/state.json ] && grep -q "$TWO_NODE_LAB" .labctl/state.json && grep -q "$BGP_LAB" .labctl/state.json; then
  echo "  both tracked: OK"
else
  echo "  FAIL: both labs not tracked"; FAIL=1
fi

echo "=== 6. Destroy two-node lab; BGP must remain ==="
./scripts/labctl destroy "$TWO_NODE_LAB" || { echo "  FAIL: two-node destroy exited nonzero"; FAIL=1; }
LEFT_AFTER_ONE=$(managed_count)
docker ps --filter label=$LABEL
[ "$LEFT_AFTER_ONE" -eq 3 ] && echo "  bgp remains count=3: OK" || { echo "  FAIL: expected 3 remaining, got $LEFT_AFTER_ONE"; FAIL=1; }
docker network inspect clab-two-node-ptp >/dev/null 2>&1 && { echo "  FAIL: two-node network still exists"; FAIL=1; } || echo "  two-node network removed: OK"
docker network inspect clab-bgp-triangle >/dev/null 2>&1 && echo "  bgp network remains: OK" || { echo "  FAIL: bgp network missing"; FAIL=1; }
./scripts/labctl status "$BGP_LAB" || { echo "  FAIL: bgp-triangle status after two-node destroy"; FAIL=1; }

echo "=== 7. Destroy BGP lab ==="
./scripts/labctl destroy "$BGP_LAB" || { echo "  FAIL: bgp-triangle destroy exited nonzero"; FAIL=1; }

echo "=== 8. Teardown clean (expect EMPTY) ==="
LEFT=$(docker ps -a --filter label=$LABEL --format '{{.Names}}' | wc -l)
docker ps -a --filter label=$LABEL
[ "$LEFT" -eq 0 ] && echo "  none remain: OK" || { echo "  FAIL: $LEFT managed containers left"; FAIL=1; }

echo "=== 9. State registry deregistered ==="
if [ -f .labctl/state.json ] && { grep -q "$TWO_NODE_LAB" .labctl/state.json || grep -q "$BGP_LAB" .labctl/state.json; }; then
  echo "  FAIL: lab still tracked"; FAIL=1
else
  echo "  deregistered: OK"
fi

echo "======================================"
[ "$FAIL" -eq 0 ] && echo "SMOKE TEST: PASS - clear for SMCPP checklist" || echo "SMOKE TEST: FAIL - do not authorize SMCPP"
exit $FAIL
