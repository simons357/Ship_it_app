#!/usr/bin/env python3
"""
Signed-strain blob as an a priori: one-sided is not a bound.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B17: named blob + signed strain. B17a: net sits on P_+.
B17b: cubic is not live versus D. This write asks whether
that leftover closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_coherent import (
    CANCEL_MIN,
    PD_MAX,
    SIGMA_MIN,
    lemma_coherent_field,
    lemma_cubic_not_live,
    lemma_net_is_plus,
)
from track_b_lemmas import rec


def lemma_blob_priori_readable() -> dict:
    field = lemma_coherent_field()
    plus = lemma_net_is_plus()
    cubic = lemma_cubic_not_live()
    ok = (
        field["verdict"] == "pass"
        and plus["verdict"] == "pass"
        and cubic["verdict"] == "fail"
        and field["sigma"] >= SIGMA_MIN
        and plus["cancel"] >= CANCEL_MIN
        and abs(cubic["P_over_D"]) < PD_MAX
        and cubic["Xdot"] < 0.0
    )
    return rec(
        "B28_blob_readable",
        "signed-strain blob, one-sided net, and visc-owned cubic are readable together",
        "pass" if ok else "fail",
        "Cancel sits near 0.83. P/D sits near 0.008. Ẋ < 0. Typed c is not written into the PDE.",
        sigma=field["sigma"],
        cancel=plus["cancel"],
        P_over_D=cubic["P_over_D"],
        Xdot=cubic["Xdot"],
    )


def lemma_onesided_not_a_priori() -> dict:
    cubic = lemma_cubic_not_live()
    return rec(
        "B28a_onesided_not_a_priori",
        "a one-sided (ω·Sω)_+ leftover closes a bound for classical X",
        "fail",
        "Coherence killed cancellation. It did not make P large versus D. A leftover is not continuation.",
        P_over_D=cubic["P_over_D"],
        Xdot=cubic["Xdot"],
    )


def lemma_sign_not_a_class() -> dict:
    return rec(
        "B28b_sign_not_a_class",
        "sitting a blob where S_zz keeps a sign is a geometric class that bounds X",
        "fail",
        "Localization in z is a knob. A z-independent tube in the same strain still cancels (B17c). Do not promote a sign to a type.",
    )


def lemma_peaked_not_integral_max() -> dict:
    return rec(
        "B28c_peaked_not_integral_max",
        "an L² bound on this peaked blob is an integral bound on the max vorticity",
        "fail",
        "‖ω‖_∞/‖ω‖₂ climbed from 0.2 to ~2.4. The criterion still asks for ∫‖ω‖_∞. Do not improve a peaked packet into the max.",
    )


def lemma_nu_not_continuation() -> dict:
    return rec(
        "B28d_nu_not_continuation",
        "turning ν down until Ẋ>0 is a continuation argument for classical X",
        "fail",
        "That is a knob on the check. B17f already missed the retune. The working box stayed ν=0.1. Do not spawn a thinner visc.",
    )


def lemma_occupation_leftover() -> dict:
    return rec(
        "B28e_occupation_leftover",
        "field occupation of CONC closes X",
        "fail",
        "Scored as B18e / B29. A clock that stays CONC is not continuation. Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Regularity leftover is open. Do not spawn n=64.",
    )


def lemma_blob_priori_not_a_retune() -> dict:
    return rec(
        "B28f_not_a_pde_retune",
        "scoring the signed-strain blob as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. One-sided is a knob on the estimate: a leftover you can miss. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_blob_priori_readable(),
        lemma_onesided_not_a_priori(),
        lemma_sign_not_a_class(),
        lemma_peaked_not_integral_max(),
        lemma_nu_not_continuation(),
        lemma_occupation_leftover(),
        lemma_blob_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "signed-strain blob as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. One-sided is a number. "
                "Large versus D is a different number. "
                "A leftover that no longer cancels is not a bound."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). "
            "Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Regularity leftover is open. Finer (n>32) stays a box knob (B22e). "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_blob.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Signed-strain blob as an a priori. One-sided is not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
