#!/usr/bin/env bash
# Local preview of the magazine + VAL8000 little box.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-8765}"
echo "Cosmic Graffiti · VAL8000 little box"
echo "Open http://127.0.0.1:${PORT}/"
echo "Issue 1: http://127.0.0.1:${PORT}/issue1.html"
echo "Click the red-eye square. Ctrl-C to stop."
exec python3 -m http.server "$PORT" --bind 127.0.0.1
