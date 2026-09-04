#!/usr/bin/env python3
"""
Finer box as an a priori: a bigger FFT is not continuation.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B22: longer n=32 past room time did not produce c=8.
B22c: n=32 dealias still cannot host a fat j=4.
This write asks whether n>32 closes X. It does not.
Do not spawn n=64.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_climb_law import C_SAVE
from track_b_lemmas import rec
from track_b_longer import (
    ABOVE_MAX,
    T_ROOM,
    lemma_longer_no_high_fill,
    lemma_longer_not_saving,
    lemma_longer_readable,
)
from track_b_window import lemma_window_priori_readable


def lemma_finer_priori_readable() -> dict:
    lng = lemma_longer_readable()
    miss = lemma_longer_not_saving()
    fill = lemma_longer_no_high_fill()
    win = lemma_window_priori_readable()
    ok = (
        lng["verdict"] == "pass"
        and miss["verdict"] == "fail"
        and fill["verdict"] == "fail"
        and win["verdict"] == "pass"
        and lng["T"] > T_ROOM
        and miss["c_inc_max"] < C_SAVE
        and fill["aboveT"]["packet"] < ABOVE_MAX
        and fill["aboveT"]["blob"] < ABOVE_MAX
        and win["T"] < win["t_room"]
    )
    return rec(
        "B33_finer_readable",
        "longer n=32 miss, empty high shells, and the short window are readable together",
        "pass" if ok else "fail",
        "T=0.384 > 0.375. Mass above j*+1 stays ~0. n=32 dealias cannot host a fat j=4. Typed c is not written into the PDE.",
        T=lng["T"],
        t_room=T_ROOM,
        c_inc_max=miss["c_inc_max"],
        aboveT=fill["aboveT"],
        window_T=win["T"],
        c_save=C_SAVE,
    )


def lemma_finer_not_a_priori() -> dict:
    fill = lemma_longer_no_high_fill()
    return rec(
        "B33a_finer_not_a_priori",
        "a finer box (n>32) closes a bound for classical X",
        "fail",
        "A bigger FFT is not continuation. n is a knob on the box. The working box already cannot host the cascade the slogan wants.",
        aboveT=fill["aboveT"],
    )


def lemma_fft_not_continuation() -> dict:
    miss = lemma_longer_not_saving()
    return rec(
        "B33b_fft_not_continuation",
        "cashing n=64 after a decaying n=32 path is a continuation argument for classical X",
        "fail",
        "Continuation is an estimate, not a finer mesh. Past the sitting of c=8 the path still decayed. Do not spawn n=64.",
        T=miss["T"],
        t_room=miss["t_room"],
        c_inc_max=miss["c_inc_max"],
    )


def lemma_n64_not_ns() -> dict:
    return rec(
        "B33c_n64_not_ns",
        "an unrun n=64 box is still an NS a priori",
        "fail",
        "The field on this box went down. A box you did not run is not the packet. Do not sit a finer FFT as the estimate.",
    )


def lemma_finer_not_integral_max() -> dict:
    return rec(
        "B33d_finer_not_integral_max",
        "a finer box is an integral bound on the max vorticity",
        "fail",
        "n is a knob on the check. A mesh is not ∫‖ω‖_∞. DNS-never-blew-up at a finer n is the same refused slogan.",
    )


def lemma_dns_finer_leftover() -> dict:
    return rec(
        "B33e_dns_finer_leftover",
        "a finer box makes the DNS run an a priori",
        "fail",
        "Scored as B23e / B34. A finer DNS run is not continuation. Leftover close is not an a priori (B34e). Regularity stays open. Do not spawn n=64.",
    )


def lemma_finer_priori_not_a_retune() -> dict:
    return rec(
        "B33f_not_a_pde_retune",
        "scoring a finer box as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. n is a knob on the box. No Q1. No ε. Do not type c=8 into the equation. Do not spawn n=64.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_finer_priori_readable(),
        lemma_finer_not_a_priori(),
        lemma_fft_not_continuation(),
        lemma_n64_not_ns(),
        lemma_finer_not_integral_max(),
        lemma_dns_finer_leftover(),
        lemma_finer_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "finer box as an a priori",
            "tuning_the_pde": False,
            "n": 32,
            "spawned_n64": False,
            "tesla": (
                "exacting, not a jerk. A bigger FFT is not continuation. "
                "n is a knob on the box. Do not spawn n=64."
            ),
            "domain_verdict": "open",
            "c_save": C_SAVE,
            "t_room": T_ROOM,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). "
            "Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). "
            "NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). "
            "Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity stays open. "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_finer.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Finer box as an a priori. A bigger FFT is not continuation.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
