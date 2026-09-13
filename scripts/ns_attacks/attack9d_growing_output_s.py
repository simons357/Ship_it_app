#!/usr/bin/env python3
"""Attack 9D live lane — growing output support s on the 9B family.

Does NOT rebuild Freiman-AP (already dead).
Does NOT rebuild fixed-s Θ(m²)-on-one-k (analytically excluded).
Calls the team sweep already in attack9b_output_counting.py.

Not a proof. NS is not solved. Lemma★ stays OPEN.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ns_attacks.attack9b_output_counting import _py, run  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=1390)
    ap.add_argument("--n-trials", type=int, default=12)
    args = ap.parse_args()
    summary = run(seed=args.seed, n_trials=args.n_trials)
    summary["attack"] = "9D-growing-s"
    summary["note"] = (
        "Wrapper around 9B output counting. Fixed-s 9D excluded. "
        "Growing s samples finite. Not C0. NS not solved."
    )
    slim = {k: v for k, v in summary.items() if k != "growing_rows"}
    print(json.dumps(_py(slim), indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(_py(summary), indent=2))
        print(f"wrote {args.out}", flush=True)
    return 0 if summary["verdict"].startswith("FIXED_S") else 1


if __name__ == "__main__":
    raise SystemExit(main())
