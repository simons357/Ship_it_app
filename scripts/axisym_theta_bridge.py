#!/usr/bin/env python3
"""Run θ lab diagnostics (not a bridge to (A); not WRITE (6))."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.axisym_theta_bridge import run_theta_bridge_battery


def main() -> None:
    out = run_theta_bridge_battery(n_trials=100, seed=41)
    print(json.dumps(out, indent=2, default=float))


if __name__ == "__main__":
    main()
