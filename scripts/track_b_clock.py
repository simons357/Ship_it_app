#!/usr/bin/env python3
"""
Field occupation as an a priori: a clock that stays CONC is not a bound.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B18: τ_C + τ_S = T on a path. B18a: both paths stay CONC.
B18b: the clock did not save X. This write asks whether
that reading closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_field_occ import (
    CONC_FRAC_MIN,
    CLOCK_GAP,
    lemma_clock_did_not_save,
    lemma_field_clock,
    lemma_stays_conc,
    paths,
)
from track_b_lemmas import rec


def lemma_clock_priori_readable() -> dict:
    ident = lemma_field_clock()
    stay = lemma_stays_conc()
    save = lemma_clock_did_not_save()
    ok = (
        ident["verdict"] == "pass"
        and stay["verdict"] == "pass"
        and save["verdict"] == "fail"
        and all(g < CLOCK_GAP for g in ident["clock_gap"].values())
        and all(f >= CONC_FRAC_MIN for f in stay["tau_frac"].values())
        and all(s == 0 for s in save["switches"].values())
        and all(save["X_fell"].values())
    )
    return rec(
        "B29_clock_readable",
        "path clock, full CONC occupation, and visc-owned X are readable together",
        "pass" if ok else "fail",
        "τ_C = T. Zero switches. X falls by viscosity. Typed c is not written into the PDE.",
        clock_gap=ident["clock_gap"],
        tau_frac=stay["tau_frac"],
        switches=save["switches"],
        X_fell=save["X_fell"],
    )


def lemma_stay_not_a_priori() -> dict:
    save = lemma_clock_did_not_save()
    return rec(
        "B29a_stay_not_a_priori",
        "occupying 3-CONC for the whole interval closes a bound for classical X",
        "fail",
        "Both paths stay CONC and X falls. Leray’s dissipation did the work. The clock did not leave. That is not continuation.",
        switches=save["switches"],
        X_fell=save["X_fell"],
    )


def lemma_full_occ_not_short() -> dict:
    stay = lemma_stays_conc()
    return rec(
        "B29b_full_occ_not_short",
        "τ_C = T on these paths is a short CONC visit that bounds X",
        "fail",
        "B18c already missed. B8a’s collapsing hot time is a packet ODE at high j*. These fields occupied the whole interval.",
        tau_frac=stay["tau_frac"],
    )


def lemma_occ_not_live_cubic() -> dict:
    rows = paths()
    return rec(
        "B29c_occ_not_live_cubic",
        "occupation of CONC is occupation of a live cubic",
        "fail",
        "Zero live samples. |P|/D stays below 0.05. Occupation of a hat is not occupation of the cubic.",
        live_samples={"packet": rows["packet"]["live_samples"], "blob": rows["blob"]["live_samples"]},
    )


def lemma_clock_not_integral_max() -> dict:
    return rec(
        "B29d_clock_not_integral_max",
        "τ_C = T is an integral bound on the max vorticity",
        "fail",
        "A clock column is not ∫‖ω‖_∞. Full occupation of a decaying packet is not the max criterion.",
    )


def lemma_glue_leftover() -> dict:
    return rec(
        "B29e_glue_leftover",
        "matching the two-regime sketch closes X",
        "fail",
        "Scored as B19e / B30. A wrong-sign sketch is not continuation. NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity stays open. Do not spawn n=64.",
    )


def lemma_clock_priori_not_a_retune() -> dict:
    return rec(
        "B29f_not_a_pde_retune",
        "scoring field occupation as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The clock is a knob on the estimate: a number you can miss. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_clock_priori_readable(),
        lemma_stay_not_a_priori(),
        lemma_full_occ_not_short(),
        lemma_occ_not_live_cubic(),
        lemma_clock_not_integral_max(),
        lemma_glue_leftover(),
        lemma_clock_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "field occupation as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. Occupation is a number on a path. "
                "If the path never leaves CONC, the clock did not do the bound."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). "
            "Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity stays open. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_clock.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Field occupation as an a priori. A clock that stays CONC is not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
