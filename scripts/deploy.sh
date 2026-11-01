#!/usr/bin/env bash
set -euo pipefail
# Host-side deployment. Keep this checkout outside the public web directory.
VERBAL_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
exec python3 "$VERBAL_ROOT/scripts/deploy.py" "$@"
