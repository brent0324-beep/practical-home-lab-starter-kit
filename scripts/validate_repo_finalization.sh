#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"

cd "$ROOT_DIR"

failures=0

fail() {
  printf '[FAIL] %s\n' "$1"
  failures=$((failures + 1))
}

pass() {
  printf '[PASS] %s\n' "$1"
}

if [[ "$(git rev-parse --show-toplevel)" != "$ROOT_DIR" ]]; then
  fail "repository root mismatch"
else
  pass "repository root scoped to $ROOT_DIR"
fi

required_files=(
  "AGENTS.md"
  "docs/governance/README.md"
  "docs/governance/security.md"
  "docs/governance/secret_handling.md"
  "docs/governance/artifact_policy.md"
  "docs/governance/runtime_data_policy.md"
  "docs/governance/git_workflow.md"
  "docs/governance/validation_policy.md"
  "docs/governance/engineering_session_workflow.md"
  "docs/governance/codex_prompt_standard.md"
  "docs/governance/codex_prompt_checklist.md"
  "docs/bootstrap/BOOTSTRAP.md"
  "docs/bootstrap/SESSION_STATE.md"
  "config/repository_bootstrap.yml"
  "config/artifact_policy.json"
  "SECURITY.md"
  "CONTRIBUTING.md"
  "docs/sanitized-example-policy.md"
  "docs/publication-checklist.md"
  "docs/release-checklist.md"
)

missing=0
for file in "${required_files[@]}"; do
  if [[ ! -s "$file" ]]; then
    missing=$((missing + 1))
  fi
done

if (( missing > 0 )); then
  fail "governance or public safety files missing or empty: $missing"
else
  pass "governance and public safety files present"
fi

if python3 -m json.tool config/artifact_policy.json >/dev/null; then
  pass "artifact policy JSON is valid"
else
  fail "artifact policy JSON is invalid"
fi

ignore_samples=(
  "media/raw/runtime-check.mkv"
  "media/edited/runtime-check.mkv"
  "media/audio/runtime-check.wav"
  "media/thumbnails/runtime-check.png"
  "media/screenshots/runtime-check.png"
  "screenshots/work/runtime-check.png"
  "screenshots/drafts/runtime-check.png"
  "inventories/runtime-check.ini"
  "inventory/runtime-check.ini"
  "ansible/output/runtime-check.txt"
  "ansible/outputs/runtime-check.txt"
  "ansible/backups/runtime-check.cfg"
  "tmp/runtime-check.txt"
  "scratch/runtime-check.txt"
  "private/runtime-check.md"
  "notes/private/runtime-check.md"
  "unpublished/runtime-check.md"
  "dist/runtime-check.tar.gz"
  "generated/repository_context.md"
  "generated/session_history.md"
  "generated/prompts/runtime-check.md"
  "generated/migration_bundles/runtime-check.zip"
  ".env"
  "secrets/runtime-check.txt"
)

ignore_misses=0
for sample in "${ignore_samples[@]}"; do
  if ! git check-ignore -q "$sample"; then
    ignore_misses=$((ignore_misses + 1))
  fi
done

if (( ignore_misses > 0 )); then
  fail "runtime, private, packaging, or secret ignore coverage misses: $ignore_misses"
else
  pass "runtime, private, packaging, and secret paths remain ignored"
fi

tracked_runtime_count="$(
  git ls-files |
    awk '
      function allowed(path) {
        return path == "media/raw/.gitkeep" ||
          path == "media/edited/.gitkeep" ||
          path == "media/audio/.gitkeep" ||
          path == "media/thumbnails/.gitkeep" ||
          path == "media/screenshots/.gitkeep"
      }
      /^(dist|inventories|inventory|private|unpublished|tmp|scratch)\// ||
      /^notes\/private\// ||
      /^ansible\/(output|outputs|backups)\// ||
      /^screenshots\/(work|drafts)\// ||
      /^media\/(raw|edited|audio|thumbnails|screenshots)\// {
        if (!allowed($0)) count++
      }
      END { print count + 0 }
    '
)"

if (( tracked_runtime_count > 0 )); then
  fail "tracked runtime or private artifact paths found: $tracked_runtime_count"
else
  pass "no tracked runtime or private artifacts except placeholders"
fi

staged_private_count="$(
  git diff --cached --name-only |
    awk '
      /^\.env($|\.)/ ||
      /(^|\/)(secrets|tokens|credentials)(\/|$)/ ||
      /\.(key|pem|p12|pfx|psk|secret)$/ ||
      /(^|\/)(private|unpublished)(\/|$)/ ||
      /^notes\/private\// {
        count++
      }
      END { print count + 0 }
    '
)"

if (( staged_private_count > 0 )); then
  fail "staged sensitive-environment, secret, or local-only paths found: $staged_private_count"
else
  pass "no staged sensitive-environment, secret, or local-only paths"
fi

staged_runtime_count="$(
  git diff --cached --name-only |
    awk '
      /^(inventories|inventory|tmp|scratch)\// ||
      /^ansible\/(output|outputs|backups)\// ||
      /^screenshots\/(work|drafts)\// ||
      /^media\/(raw|edited|audio|thumbnails|screenshots)\// {
        count++
      }
      END { print count + 0 }
    '
)"

if (( staged_runtime_count > 0 )); then
  fail "staged runtime artifact paths found: $staged_runtime_count"
else
  pass "no staged runtime artifacts"
fi

staged_unpublished_media_count="$(
  git diff --cached --name-only |
    awk '
      /^starter-kit-review\// ||
      /^media\/(raw|edited|audio|thumbnails|screenshots)\// ||
      /^screenshots\/(work|drafts)\// ||
      /\.(mkv|mp4|mov|wav|mp3)$/ {
        count++
      }
      END { print count + 0 }
    '
)"

if (( staged_unpublished_media_count > 0 )); then
  fail "staged unpublished media artifact paths found: $staged_unpublished_media_count"
else
  pass "no staged unpublished media artifacts"
fi

staged_package_count="$(
  git diff --cached --name-only |
    awk '
      /^dist\// ||
      /\.(tar\.gz|zip)$/ {
        count++
      }
      END { print count + 0 }
    '
)"

if (( staged_package_count > 0 )); then
  fail "staged generated packaging artifacts found: $staged_package_count"
else
  pass "no staged generated packaging artifacts"
fi

staged_engineering_session_count="$(
  git diff --cached --name-only |
    awk '
      /^generated\/repository_context\.md$/ ||
      /^generated\/session_history\.md$/ ||
      /^generated\/prompts\// ||
      /^generated\/migration_bundles\// {
        count++
      }
      END { print count + 0 }
    '
)"

if (( staged_engineering_session_count > 0 )); then
  fail "staged generated engineering-session artifacts found: $staged_engineering_session_count"
else
  pass "no staged generated engineering-session artifacts"
fi

ownership_mismatch_count="$(
  find "$ROOT_DIR" -xdev \( ! -user bainet -o ! -group bainet \) -printf '.' 2>/dev/null | wc -c
)"

if (( ownership_mismatch_count > 0 )); then
  fail "non-bainet ownership entries found: $ownership_mismatch_count"
else
  pass "ownership is bainet:bainet"
fi

if (( failures > 0 )); then
  printf 'Repository finalization validation: FAIL (%d failures)\n' "$failures"
  exit 1
fi

printf 'Repository finalization validation: PASS\n'
