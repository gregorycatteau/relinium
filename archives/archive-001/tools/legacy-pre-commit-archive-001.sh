#!/bin/sh
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
FS_ROOT="$REPO_ROOT/archives/archive-001/fs-root"

cd "$FS_ROOT"

printf 'pre-commit: validating frontmatter...\n'
python scripts/validate_frontmatter.py

printf 'pre-commit: running docs-check...\n'
make docs-check
