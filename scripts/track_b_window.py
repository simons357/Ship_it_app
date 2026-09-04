#!/usr/bin/env python3
"""
Climb sketch as an a priori: a short window is not the sitting.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B21: ODE and NS readable on T=0.064. B21a: c=8 has not
reached the viscous room. B21b: the sitting path is not
the packet. This write asks whether matching the sketch
closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_climb_law import C_SAVE
from track_b_climb_sketch import (
    J_ROOM,
    lemma_delta_j_not_prescribed,
    lemma_not_the_room,
    lemma_not_the_sitting,
    lemma_window_rates,
)
from track_b_lemmas import rec


def lemma_window_priori_readable() -> dict:
    rates = lemma_window_rates()
    room = lemma_not_the_room()
    sit = lemma_not_the_sitting()
    ok = (
        rates["verdict"] == "pass"
        and room["verdict"] == "fail"
        and sit["verdict"] == "fail"
        and room["jT"] < J_ROOM
        and room["T"] < room["t_room"]
        and sit["dX_ode"] > 0.0
        and sit["dX_ns"] < 0.0
        and not sit["sign_match"]
    )
    return rec(
        "B32_window_readable",
        "window rates, missed viscous room, and sketch-grows / field-falls are readable together",
        "pass" if ok else "fail",
        "j: 2 → 2.51. Room is j=5 at T=0.375. This window is 0.064. Typed c is not written into the PDE.",
        jT=room["jT"],
        t_room=room["t_room"],
        T=room["T"],
        dX_ode=sit["dX_ode"],
        dX_ns=sit["dX_ns"],
        sign_match=sit["sign_match"],
        c_save=C_SAVE,
    )


def lemma_window_not_a_priori() -> dict:
    sit = lemma_not_the_sitting()
    return rec(
        "B32a_window_not_a_priori",
        "matching the c=8 sketch to this NS window closes a bound for classical X",
        "fail",
        "The sketch grew. The field fell. A short window is not the sitting of B11c.",
        dX_ode=sit["dX_ode"],
        dX_ns=sit["dX_ns"],
    )


def lemma_short_not_continuation() -> dict:
    room = lemma_not_the_room()
    return rec(
        "B32b_short_not_continuation",
        "cashing B11c on T=0.064 is a continuation argument for classical X",
        "fail",
        "The sitting is a long ODE. This box is short. Time to the room is 0.375. Do not cash a later save.",
        T=room["T"],
        t_room=room["t_room"],
        jT=room["jT"],
    )


def lemma_growing_not_ns() -> dict:
    dj = lemma_delta_j_not_prescribed()
    return rec(
        "B32c_growing_not_ns",
        "a typed ODE that climbs while the packet falls is still an NS a priori",
        "fail",
        "Prescribed Δj = 0.512. NS Δj_bar ≈ −0.015. Do not sit the sketch as the packet.",
        dj_ode=dj["dj_ode"],
        dj_ns=dj["dj_ns"],
    )


def lemma_window_not_integral_max() -> dict:
    return rec(
        "B32d_window_not_integral_max",
        "matching the sketch on this window is an integral bound on the max vorticity",
        "fail",
        "A short-window sign of Ẋ is not ∫‖ω‖_∞. A growing sketch against a falling packet is not the max criterion.",
    )


def lemma_finer_box_leftover() -> dict:
    return rec(
        "B32e_finer_leftover",
        "a finer box (n>32) closes X",
        "fail",
        "Scored as B22e / B33. A bigger FFT is not continuation. Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity leftover is not an a priori (B35e). Regularity stays open. Do not spawn n=64.",
    )


def lemma_window_priori_not_a_retune() -> dict:
    return rec(
        "B32f_not_a_pde_retune",
        "scoring the climb sketch as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The window is a knob on the check. No Q1. No ε. Do not type c=8 into the equation.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_window_priori_readable(),
        lemma_window_not_a_priori(),
        lemma_short_not_continuation(),
        lemma_growing_not_ns(),
        lemma_window_not_integral_max(),
        lemma_finer_box_leftover(),
        lemma_window_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "climb sketch as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. The sitting of c=8 is a long ODE. "
                "This window is short. The field did not follow."
            ),
            "domain_verdict": "open",
            "c_save": C_SAVE,
            "j_room": J_ROOM,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). "
            "Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). "
            "NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). "
            "Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity leftover is not an a priori (B35e). Regularity stays open. Finer (n>32) stays a box knob (B22e). "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_window.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Climb sketch as an a priori. A short window is not the sitting.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
