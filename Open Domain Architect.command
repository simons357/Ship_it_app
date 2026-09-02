#!/bin/bash
# Double-click this file on a Mac (or run it from Terminal) to open Domain Architect.
# It must stay in the Ship_it_app folder, next to the domain_architect package.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONUNBUFFERED=1
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

fail() {
  echo "$1" >&2
  if command -v osascript >/dev/null 2>&1; then
    osascript -e "display dialog \"$1\" buttons {\"OK\"} default button 1"
  fi
  exit 1
}

if [[ ! -d "$ROOT/domain_architect" ]]; then
  fail "Put this launcher in the Ship_it_app folder, next to the domain_architect package."
fi

PY=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PY="$(command -v "$candidate")"
    break
  fi
done
if [[ -z "$PY" ]]; then
  fail "Domain Architect needs Python 3. Install it from python.org or Homebrew, then open this file again."
fi

exec "$PY" -m domain_architect app "$@"
