#!/usr/bin/env python3
"""
Tube budget as an a priori: B4c is a packet budget, not a bound.

Classical NS. No Q1. No ε. No Φ cancel.
B4c: full D_tube budgets |I_tube| on packets.
B5b: the extra 1/r² piece, alone, does not.
This write asks whether either reading closes X.
They do not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_angular import lemma_angular_not_dominate, scan_packets
from track_b_hardy_tube import lemma_packet_absorbed
from track_b_lemmas import rec


def lemma_tube_readable() -> dict:
    pack = lemma_packet_absorbed()
    ang = lemma_angular_not_dominate()
    scan = scan_packets()
    ok = (
        pack["verdict"] == "pass"
        and ang["verdict"] == "fail"
        and min(scan["R_ang"]) > 1.0
        and max(scan["R_D"]) < 1.0
        and scan["climbs"]
        and scan["D_falls"]
    )
    return rec(
        "B24_tube_readable",
        "B4c packet budget and B5b angular ratio are readable together",
        "pass" if ok else "fail",
        "R_D sits below 1 and falls with j*. R_ang sits above 1 and climbs. Full D_tube budgets the packet. Angular does not. Typed c is not written into the PDE.",
        R_ang=scan["R_ang"],
        R_D=scan["R_D"],
    )


def lemma_angular_not_a_priori() -> dict:
    return rec(
        "B24a_angular_not_a_priori",
        "the extra 1/r² piece closes a bound for classical X",
        "fail",
        "R_ang > 1 and climbs. A failed Poincaré is not continuation. B5b already missed domination.",
    )


def lemma_b4c_not_a_priori() -> dict:
    return rec(
        "B24b_b4c_not_a_priori",
        "the B4c packet tube budget is a closed a priori bound for classical X",
        "fail",
        "B4c budgets |I_tube| on a packet class. B4b killed all-data Hardy. B23c: one triad is not Leray. A budget is not continuation.",
    )


def lemma_rd_not_bounded() -> dict:
    scan = scan_packets()
    small = max(scan["R_D"]) < 0.05
    return rec(
        "B24c_rd_not_bounded",
        "R_D ≪ 1 on packets implies X ∈ L∞",
        "fail" if small else "open",
        "Dissipation beats the tube source on this class. That is a ratio, not Beale. DNS-never-blew-up is refused. So is tube-ratio-never-blew-up.",
        R_D=scan["R_D"],
    )


def lemma_not_revive_hardy_or_phi() -> dict:
    return rec(
        "B24d_not_revive_hardy_or_phi",
        "therefore revive all-data Hardy, or cancel to Φ = Γ/r²",
        "fail",
        "B4b and B5e already failed those slogans. Keep Γ. Keep 1/r^4. B4c still budgets the packet. Do not cancel to Φ.",
    )


def lemma_geometry_leftover() -> dict:
    return rec(
        "B24e_geometry_leftover",
        "packet geometry closes X",
        "fail",
        "Scored as B14d / B25. Lipschitz plus a conditional is not continuation. Stretching budget leftover is B15e.",
    )


def lemma_tube_not_a_retune() -> dict:
    return rec(
        "B24f_not_a_pde_retune",
        "scoring the tube budget as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The ratio is a knob on the estimate. No Q1. No ε. No Φ cancel.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_tube_readable(),
        lemma_angular_not_a_priori(),
        lemma_b4c_not_a_priori(),
        lemma_rd_not_bounded(),
        lemma_not_revive_hardy_or_phi(),
        lemma_geometry_leftover(),
        lemma_tube_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "tube budget as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. You asked the tube. Full D budgets "
                "the packet. Angular loses. Neither reading is a bound. "
                "Do not cancel to Φ."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget leftover is B15e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_tube.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Tube budget as an a priori. A packet budget is not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
