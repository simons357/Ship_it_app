#!/usr/bin/env python3
"""
Alignment as an a priori: geometry is a number, not a bound.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B14: strain identity on E_c. B14a: CONC is not depleted.
B14c: CF as a conditional. This write asks whether that
frame closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_geometry import (
    lemma_cf_conditional,
    lemma_conc_not_depleted,
    lemma_strain_identity,
    samples,
)
from track_b_lemmas import rec


def lemma_align_readable() -> dict:
    ident = lemma_strain_identity()
    conc = lemma_conc_not_depleted()
    cf = lemma_cf_conditional()
    ok = (
        ident["verdict"] == "pass"
        and conc["verdict"] == "fail"
        and cf["verdict"] == "pass"
        and conc["median_cos3"] > 0.25
        and cf["mean_ratio_low"] < cf["mean_ratio_high"]
    )
    return rec(
        "B25_align_readable",
        "strain identity, undepleted CONC, and the CF conditional are readable together",
        "pass" if ok else "fail",
        "Eigenframe residual is roundoff. Median |cos α_3| sits near 1/2. IF less aligned, stretching is smaller. Typed c is not written into the PDE.",
        median_cos3=conc["median_cos3"],
        mean_ratio_low=cf["mean_ratio_low"],
        mean_ratio_high=cf["mean_ratio_high"],
    )


def lemma_depletion_not_a_priori() -> dict:
    conc = lemma_conc_not_depleted()
    return rec(
        "B25a_depletion_not_a_priori",
        "3-CONC depletion of |cos α_3| closes a bound for classical X",
        "fail",
        "Median sits near 1/2. CONC is a spectrum, not an alignment. A slogan the packets miss is not continuation.",
        median_cos3=conc["median_cos3"],
    )


def lemma_frame_not_a_priori() -> dict:
    return rec(
        "B25b_frame_not_a_priori",
        "Ring Lipschitz plus the CF conditional is a closed a priori for classical X",
        "fail",
        "Direction slowly varying is not direction aligned (B14b). IF less aligned, stretching is smaller (B14c). An if is not continuation.",
    )


def lemma_median_not_a_class() -> dict:
    rows = samples()
    med = float(sum(r["median_cos3"] for r in rows) / max(len(rows), 1))
    return rec(
        "B25c_median_not_a_class",
        "median |cos α_3| ~ 1/2 on E_c is a geometric class that bounds X",
        "fail",
        "Random on the sphere is not a class. Majda: do not promote CONC to a geometric type.",
        median_cos3=med,
    )


def lemma_cf_not_bkm() -> dict:
    return rec(
        "B25d_cf_not_bkm",
        "the CF conditional on E_c is Beale–Kato–Majda",
        "fail",
        "A smaller stretching efficiency on a subset of E_c is not ∫‖ω‖_∞. Do not glue Constantin–Fefferman to Biot–Savart.",
    )


def lemma_budget_leftover() -> dict:
    return rec(
        "B25e_budget_leftover",
        "the aligned stretching budget closes X",
        "fail",
        "Scored as B15e / B26. A share of (ω·Sω)_+ is not continuation. Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer leftover is B22e. Do not spawn n=64.",
    )


def lemma_align_not_a_retune() -> dict:
    return rec(
        "B25f_not_a_pde_retune",
        "scoring alignment as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. Alignment is a knob on the estimate: a number you can miss. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_align_readable(),
        lemma_depletion_not_a_priori(),
        lemma_frame_not_a_priori(),
        lemma_median_not_a_class(),
        lemma_cf_not_bkm(),
        lemma_budget_leftover(),
        lemma_align_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "alignment as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. Alignment is a number. "
                "You can miss 0.25. The packets miss it. "
                "A conditional is not a bound."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer leftover is B22e. Finer (n>32) stays a box knob (B22e). "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_align.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Alignment as an a priori. A number you can miss is not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
