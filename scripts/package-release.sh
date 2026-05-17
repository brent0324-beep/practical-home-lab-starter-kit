#!/usr/bin/env bash
set -euo pipefail

version="${1:-v0.1.0}"
project_name="practical-home-lab-starter-kit"
archive_name="${project_name}-${version}.tar.gz"
dist_dir="dist"
archive_path="${dist_dir}/${archive_name}"

mkdir -p "$dist_dir"

tar \
  --exclude=".git" \
  --exclude=".agents" \
  --exclude=".codex" \
  --exclude="$dist_dir" \
  --exclude="./.agents" \
  --exclude="./.codex" \
  --exclude="./$dist_dir" \
  --transform "s,^,${project_name}-${version}/," \
  -czf "$archive_path" \
  .

echo "Created ${archive_path}"
