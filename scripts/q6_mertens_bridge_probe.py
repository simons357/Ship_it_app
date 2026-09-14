#!/usr/bin/env python3
"""Print the Q6 → Mertens obstruction table. Not a proof of RH."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "docs" / "papers" / "gcd" / "q6_mertens_bridge.py"


def _load():
    spec = importlib.util.spec_from_file_location("q6_mertens_bridge", MOD)
    if spec is None or spec.loader is None:
        raise ImportError(MOD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    bridge = _load()
    rows = bridge.probe_table((20, 30, 50, 80, 100, 150, 200))
    cols = (
        "N",
        "lambda_min_A_over_logN",
        "rayleigh_A_one",
        "rayleigh_A_mu",
        "squarefree_U",
        "target_two_pi",
        "M",
    )
    print(" ".join(f"{c:>24}" for c in cols))
    for row in rows:
        cells = []
        for c in cols:
            val = row[c]
            if c == "N" or c == "M":
                cells.append(f"{int(val):>24d}")
            else:
                cells.append(f"{float(val):>24.6f}")
        print(" ".join(cells))
    print("target constant -1/(2π) =", bridge.MINUS_ONE_OVER_TWO_PI)
    print("Clay is NOT CLAIMED. Transfer remains OPEN.")


if __name__ == "__main__":
    main()
