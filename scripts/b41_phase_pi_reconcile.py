#!/usr/bin/env python3
"""Identify and map the four π-offset G3 phase targets vs lock zeros.

Rerun-only arithmetic on data/R2. Does not claim G6-A or NSE regularity.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from r2_lock_tsvs import WEAK_IDENTITIES, load_tsv_matrix, wrap01

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "data" / "R2"
OUT = ROOT / "results" / "b41"
OUT.mkdir(parents=True, exist_ok=True)

PI_ROWS = (0, 5, 10, 11)


def main() -> None:
    M = [[int(x) for x in row] for row in load_tsv_matrix(R2 / "M.tsv")]
    b_g3 = [row[0] for row in load_tsv_matrix(R2 / "b_exact.tsv")]
    js = json.loads((R2 / "g3_corrected_channel_quotient.json").read_text())

    # Confirm exact half-turn vs 0
    for i in PI_ROWS:
        assert wrap01(b_g3[i] - 0) in (Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2))
        # -1/2 wraps to 1/2 under wrap01 difference from 0
        assert b_g3[i] == Fraction(-1, 2)

    b_mapped = list(b_g3)
    for i in PI_ROWS:
        b_mapped[i] = wrap01(b_g3[i] + Fraction(1, 2))
        assert b_mapped[i] == 0

    id_ok = True
    for j, coeffs in WEAK_IDENTITIES.items():
        acc = [0] * 12
        for i, a in coeffs.items():
            for c in range(12):
                acc[c] += a * M[i][c]
        id_ok = id_ok and (acc == M[j])

    payload = {
        "pi_offset_rows": list(PI_ROWS),
        "labels": [js["Gamma"][i].get("labels") for i in PI_ROWS],
        "g3_turn": [str(b_g3[i]) for i in PI_ROWS],
        "mapped_turn": [str(b_mapped[i]) for i in PI_ROWS],
        "convention_map": (
            "On rows 0,5,10,11 only: b_lock = b_G3 + π (mod 2π). "
            "Equivalent to flipping sign of g_sym before b = π/2 - arg(g_sym)."
        ),
        "weak_identities_on_disk_M": id_ok,
        "g6a_via_raw_r2_identity": False,
        "g6a_via_explicit_convention_bridge": "possible only if bridge is recorded; not stamped here",
        "ns_regularity": "open",
    }
    out = OUT / "phase_pi_reconciliation.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    print(f"wrote {out}")
    assert id_ok
    assert all(b_mapped[i] == 0 for i in PI_ROWS)


if __name__ == "__main__":
    main()
