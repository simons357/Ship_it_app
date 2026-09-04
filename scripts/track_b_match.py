#!/usr/bin/env python3
"""
Field glue as an a priori: a wrong-sign sketch is not a bound.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B19: both Ẋ readable. B19a: j*=2 model sign mismatches NS.
B19b: the packet is not the B9b blowup. This write asks whether
matching the sketch closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_field_glue import (
    lemma_alpha_not_cubic,
    lemma_field_rates,
    lemma_not_the_blowup,
    lemma_sign_mismatch,
)
from track_b_lemmas import rec


def lemma_match_priori_readable() -> dict:
    rates = lemma_field_rates()
    sign = lemma_sign_mismatch()
    blow = lemma_not_the_blowup()
    ok = (
        rates["verdict"] == "pass"
        and sign["verdict"] == "fail"
        and blow["verdict"] == "fail"
        and not sign["sign_match"]
        and sign["Xdot_model"] > 0.0
        and sign["Xdot_ns"] < 0.0
        and blow["dX_model"] > 0.0
        and blow["dX_ns"] < 0.0
    )
    return rec(
        "B30_match_readable",
        "model versus NS rates, sign mismatch, and model-grows / field-falls are readable together",
        "pass" if ok else "fail",
        "Model Ẋ = +2.25. NS Ẋ ≈ −22.5. Eight steps: model X grows. NS X falls. Typed c is not written into the PDE.",
        Xdot_ns=sign["Xdot_ns"],
        Xdot_model=sign["Xdot_model"],
        dX_ns=blow["dX_ns"],
        dX_model=blow["dX_model"],
        sign_match=sign["sign_match"],
    )


def lemma_match_not_a_priori() -> dict:
    sign = lemma_sign_mismatch()
    return rec(
        "B30a_match_not_a_priori",
        "matching the two-regime sketch to NS Ẋ closes a bound for classical X",
        "fail",
        "The sketch pointed up. The field pointed down. A wrong-sign ODE is not continuation.",
        Xdot_ns=sign["Xdot_ns"],
        Xdot_model=sign["Xdot_model"],
    )


def lemma_shrink_alpha_not_continuation() -> dict:
    cub = lemma_alpha_not_cubic()
    return rec(
        "B30b_shrink_alpha_not_continuation",
        "shrinking α_c until the signs match is a continuation argument for classical X",
        "fail",
        "Implied α sits near 0 on the packet and ~0.006 on the blob. The sketch used 0.4 and 0.2. Detuning α_c is a knob.",
        alpha_ratio=cub["alpha_ratio"],
    )


def lemma_wrong_sign_not_ns() -> dict:
    blow = lemma_not_the_blowup()
    return rec(
        "B30c_wrong_sign_not_ns",
        "a typed ODE that grows while the packet falls is still an NS a priori",
        "fail",
        "B9b is a typed fat cubic. This field cancelled. Do not sit the sketch as the packet.",
        dX_ns=blow["dX_ns"],
        dX_model=blow["dX_model"],
    )


def lemma_match_not_integral_max() -> dict:
    return rec(
        "B30d_match_not_integral_max",
        "matching model Ẋ to NS Ẋ is an integral bound on the max vorticity",
        "fail",
        "A sign of Ẋ is not ∫‖ω‖_∞. A sketch that points the wrong way is not the max criterion.",
    )


def lemma_climb_leftover() -> dict:
    return rec(
        "B30e_climb_leftover",
        "a field climb law closes X",
        "fail",
        "Scored as B20e / B31. A missing saving rate is not continuation. Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). DNS leftover is B23e. Do not spawn n=64.",
    )


def lemma_match_priori_not_a_retune() -> dict:
    return rec(
        "B30f_not_a_pde_retune",
        "scoring field glue as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. α_c is a knob on the estimate: a number you can miss. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_match_priori_readable(),
        lemma_match_not_a_priori(),
        lemma_shrink_alpha_not_continuation(),
        lemma_wrong_sign_not_ns(),
        lemma_match_not_integral_max(),
        lemma_climb_leftover(),
        lemma_match_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "field glue as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. Sign of Ẋ is a number. "
                "The j*=2 sketch grows. The NS packet falls."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). "
            "Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). "
            "NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). DNS leftover is B23e. Finer (n>32) stays a box knob (B22e). "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_match.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Field glue as an a priori. A wrong-sign sketch is not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
