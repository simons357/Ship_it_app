#!/usr/bin/env python3
"""Three-shear exact-shell field: K_{1,2} = 2/3.

Floor of sup K, not the 16/9 ceiling.
Does not overwrite stokes_moments.py.
NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from attack9b_exact_shell_K import K_of_w  # noqa: E402
from stokes_moments import enforce_reality  # noqa: E402

# w = (sin y, sin z, sin x)
# sin θ = (e^{iθ} − e^{-iθ}) / (2i)
THREE_SHEAR = {
    (0, 1, 0): np.array([-0.5j, 0.0, 0.0], dtype=np.complex128),
    (0, 0, 1): np.array([0.0, -0.5j, 0.0], dtype=np.complex128),
    (1, 0, 0): np.array([0.0, 0.0, -0.5j], dtype=np.complex128),
}


def three_shear_field() -> dict:
    return enforce_reality({k: v.copy() for k, v in THREE_SHEAR.items()})


def run() -> dict:
    w = three_shear_field()
    rec = K_of_w(w, 1.0, 2.0)
    e = rec["E_w"]
    return {
        "field": "w=(sin y, sin z, sin x)",
        "alpha": 1.0,
        "beta": 2.0,
        "E": e,
        "E_exact": 1.5,
        "K": rec["K"],
        "K_exact": 2.0 / 3.0,
        "PiB_L2_sq": rec["PiB_L2_sq"],
        "PiB_L2_sq_exact": 0.75,
        "floor_of_sup_K": 2.0 / 3.0,
        "old_aligned_9B_max": 0.641,
        "claimed_ceiling": 16.0 / 9.0,
        "clears_old_max": rec["K"] > 0.641,
        "under_claimed_ceiling": rec["K"] < 16.0 / 9.0,
        "is_C0": False,
        "proves_16_over_9": False,
        "ns_solved": False,
        "exact_shell_9d": "CLAIMED",
        "ok": (
            abs(e - 1.5) < 1e-12
            and abs(rec["PiB_L2_sq"] - 0.75) < 1e-12
            and abs(rec["K"] - 2.0 / 3.0) < 1e-12
        ),
        "note": (
            "Hand-built floor K=2/3. Not the 16/9 bound. "
            "Not C0. NS not solved."
        ),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="")
    args = p.parse_args()
    payload = run()
    text = json.dumps(payload, indent=2)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n")
        print("wrote", out)
    else:
        print(text)
    print("K =", payload["K"], "exact 2/3:", payload["ok"])
    print("NS solved:", payload["ns_solved"])
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
