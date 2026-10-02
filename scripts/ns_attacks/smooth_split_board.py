#!/usr/bin/env python3
"""Board for the 2 Oct 2026 smooth-split finite-C estimate.

A successful run verifies:
  * Fourier identities on the small-case families
  * the DA six-mode family (square j) including N = -2(2j+1)

It does not:
  * evaluate Cs or Mmult numerically
  * pay the cutoff-uniform gradient time budget
  * prove global NSE regularity
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ns_attacks.six_mode_family import run_family  # noqa: E402
from ns_attacks.sqrt_estimate_attack import run_board  # noqa: E402

THEOREM = (
    "|Lambda N| <= (4+6 Mmult) Cs g sqrt(Y Ds); "
    "|Tc| <= (7+6 Mmult) Cs g sqrt(Y Ds)"
)
STATUS = (
    "FINITE C PROVED (smooth split, fixed 2pi torus, instantaneous); "
    "time budget OPEN; NSE regularity NOT established"
)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--max-j", type=int, default=36)
    args = parser.parse_args(argv)

    small = run_board()
    family = run_family(max_j=args.max_j)
    payload = {
        "theorem": THEOREM,
        "status": STATUS,
        "lower_bound_witness": "prior exact witness C>0.4 remains necessary; not optimized here",
        "time_budget": "OPEN — (log Lambda)' <= C^2 g^2 / (2 nu) is not a paid integral of g^2",
        "regularity": "NOT established",
        "small_case": small,
        "six_mode": family,
    }
    print(f"Theorem: {THEOREM}")
    print(f"Status:  {STATUS}")
    print(f"Small-case identities: {small['identities_verified']}")
    print(f"Six-mode N claim:      {family['all_N_match_claim']}")
    print()
    print("Square-j six-mode rows:")
    for rec in family["square_j_rows"]:
        print(
            f"  j={rec['j']}: N={rec['N']} claimed={rec['claimed_N']} "
            f"match={rec['N_matches_claim']}  "
            f"Ds/(ΛY)={rec['Ds_over_Lambda_Y']}  lead={rec['claimed_lead']}"
        )
    print()
    print("4j Ds/(ΛY) (should approach 1):")
    checks = family["Ds_lead_check"]
    stride = max(1, (len(checks) + 7) // 8)
    for rec in checks[::stride]:
        print(f"  j={rec['j']}: {rec['4j_Ds_over_Lambda_Y']}")
    if checks and checks[-1] not in checks[::stride]:
        print(f"  j={checks[-1]['j']}: {checks[-1]['4j_Ds_over_Lambda_Y']}")
    print()
    print(f"Time budget: {payload['time_budget']}")
    print(f"Regularity:  {payload['regularity']}")
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")
        print(f"wrote {args.json}")
    ok = small["identities_verified"] and family["all_N_match_claim"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
