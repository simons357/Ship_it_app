#!/usr/bin/env python3
"""
Stretching budget as an a priori: a share is not a bound.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B15: (ω·Sω)_+ on E_c. B15a: CF weights the budget.
B15b: majority from the aligned cap. This write asks
whether that share closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_lemmas import rec
from track_b_stretch import (
    HIGH,
    WMEAN_GAP,
    evolved,
    lemma_budget_readable,
    lemma_cf_weights_budget,
    lemma_majority_aligned,
    t0_samples,
)


def lemma_payers_readable() -> dict:
    bud = lemma_budget_readable()
    wgt = lemma_cf_weights_budget()
    maj = lemma_majority_aligned()
    ok = (
        bud["verdict"] == "pass"
        and wgt["verdict"] == "pass"
        and maj["verdict"] == "pass"
        and all(g > WMEAN_GAP for g in wgt["gaps"])
        and all(f > 0.5 for f in maj["frac_pos_hi"])
    )
    return rec(
        "B26_payers_readable",
        "stretching budget, CF weight, and aligned majority are readable together",
        "pass" if ok else "fail",
        "Weighted |cos α_3| sits above the unweighted mean. A majority of (ω·Sω)_+ on E_c comes from the aligned cap. Typed c is not written into the PDE.",
        gaps=wgt["gaps"],
        frac_pos_hi=maj["frac_pos_hi"],
        high=HIGH,
    )


def lemma_share_not_a_priori() -> dict:
    rows = t0_samples()
    fracs = [r["frac_pos_hi"] for r in rows]
    return rec(
        "B26a_share_not_a_priori",
        "an aligned (ω·Sω)_+ share closes a bound for classical X",
        "fail",
        "A 65% share is a number. X is still the L² enstrophy. A payer count is not continuation.",
        frac_pos_hi=fracs,
    )


def lemma_emptying_not_continuation() -> dict:
    visc = evolved()["visc"]
    euler = evolved()["euler"]
    visc_hi = [r["end"]["frac_pos_hi"] for r in visc]
    euler_hi = [r["end"]["frac_pos_hi"] for r in euler]
    meds = [r["end"]["median_cos3"] for r in visc]
    emptied = any(h < 0.5 for h in visc_hi + euler_hi) or all(m <= 0.25 for m in meds)
    return rec(
        "B26b_emptying_not_continuation",
        "time emptying the aligned cap is a continuation argument for classical X",
        "fail" if not emptied else "open",
        "B15c and B15d already missed. Median stays near 1/2. frac_hi stays ~0.65. Tesla: time was a knob. It did not empty the cap.",
        visc_frac_hi_end=visc_hi,
        euler_frac_hi_end=euler_hi,
        median_end=meds,
    )


def lemma_share_not_a_class() -> dict:
    rows = t0_samples()
    fracs = [r["frac_pos_hi"] for r in rows]
    return rec(
        "B26c_share_not_a_class",
        "a ~65% aligned share of (ω·Sω)_+ is a geometric class that bounds X",
        "fail",
        "A share on 3-shell CONC packets is not all data. Majda: do not promote a payer count to a type.",
        frac_pos_hi=fracs,
    )


def lemma_aligned_budget_not_bkm() -> dict:
    return rec(
        "B26d_aligned_budget_not_integral_max",
        "an aligned stretching budget is an integral bound on the max vorticity",
        "fail",
        "A 65% share of (ω·Sω)_+ on E_c is not ∫‖ω‖_∞. Do not glue a payer count to Biot–Savart.",
    )


def lemma_enstrophy_leftover() -> dict:
    return rec(
        "B26e_enstrophy_leftover",
        "the enstrophy balance closes X",
        "fail",
        "Scored as B16e / B27. A cancelled net is not continuation. Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer leftover is B22e. Do not spawn n=64.",
    )


def lemma_payers_not_a_retune() -> dict:
    return rec(
        "B26f_not_a_pde_retune",
        "scoring the stretching budget as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The share is a knob on the estimate: a number you can miss. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_payers_readable(),
        lemma_share_not_a_priori(),
        lemma_emptying_not_continuation(),
        lemma_share_not_a_class(),
        lemma_aligned_budget_not_bkm(),
        lemma_enstrophy_leftover(),
        lemma_payers_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "stretching budget as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. The cubic's payers are a number. "
                "Time did not empty them. A share is not a bound."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer leftover is B22e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_payers.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Stretching budget as an a priori. A share is not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
