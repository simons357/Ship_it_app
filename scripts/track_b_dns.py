#!/usr/bin/env python3
"""
DNS as an a priori: the packet runs are a check, not a bound.

Classical NS. No Q1. No ε. B13 ran T~0.06. B22 ran past
the B11c room time at the same n=32. Neither produced
c=8. This write asks whether that DNS is continuation.
It is not. Do not spawn n=64.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_climb_law import C_SAVE
from track_b_evolve import lemma_no_saving_climb, lemma_run_completes
from track_b_field_occ import DT
from track_b_lemmas import rec
from track_b_longer import STEPS, T_ROOM, lemma_longer_not_saving, lemma_longer_readable

T_LONG = STEPS * DT


def lemma_dns_readable() -> dict:
    short = lemma_run_completes()
    lng = lemma_longer_readable()
    ok = (
        short["verdict"] == "pass"
        and lng["verdict"] == "pass"
        and T_LONG > T_ROOM
    )
    return rec(
        "B23_dns_readable",
        "short and longer n=32 packet DNS are a readable check past the B11c room time",
        "pass" if ok else "fail",
        "B13 and B22 already ran. T=0.384 > 0.375. Same box. Typed c is not written into the PDE.",
        T_long=T_LONG,
        t_room=T_ROOM,
    )


def lemma_dns_not_a_priori() -> dict:
    return rec(
        "B23a_dns_not_a_priori",
        "a decaying packet DNS run is a closed a priori bound for classical X",
        "fail",
        "One IC class, finite T, finite n. X falling here does not bound X on B9b or energy-class data. Beale: a decaying packet is not ∫‖ω‖_∞.",
    )


def lemma_room_time_not_continuation() -> dict:
    lng = lemma_longer_not_saving()
    past = T_LONG > T_ROOM
    no_c = lng["verdict"] == "fail"
    return rec(
        "B23b_room_time_not_continuation",
        "running past the ODE room time is continuation for classical X",
        "fail" if (past and no_c) else "open",
        "Continuation is an estimate, not a longer interval. Past the sitting of c=8 the path still decayed.",
        T_long=T_LONG,
        t_room=T_ROOM,
        c_save=C_SAVE,
    )


def lemma_packet_not_all_data() -> dict:
    return rec(
        "B23c_packet_not_all_data",
        "the working-box CONC packet class is all classical data",
        "fail",
        "B9b fat slow CONC is not this run. Energy-class T sits on SPREAD. One triad is not Leray.",
    )


def lemma_no_blow_not_bounded() -> dict:
    short = lemma_no_saving_climb()
    lng = lemma_longer_not_saving()
    both_fail = short["verdict"] == "fail" and lng["verdict"] == "fail"
    return rec(
        "B23d_no_blow_not_bounded",
        "didn't blow on n=32 implies X ∈ L∞",
        "fail" if both_fail else "open",
        "Resolved decay is a reading. n=32 dealias cannot host the cascade the slogan wants. DNS-never-blew-up is refused as a close.",
    )


def lemma_finer_still_open() -> dict:
    return rec(
        "B23e_finer_still_open",
        "a finer box (n>32) makes the DNS run an a priori",
        "open",
        "The only remaining box knob. Same leftover as B22e. Do not spawn n=64. A bigger FFT is not continuation.",
    )


def lemma_dns_not_a_retune() -> dict:
    return rec(
        "B23f_not_a_pde_retune",
        "scoring DNS as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. T and n are knobs on the check. No Q1. No ε. Do not type c=8 into the equation.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_dns_readable(),
        lemma_dns_not_a_priori(),
        lemma_room_time_not_continuation(),
        lemma_packet_not_all_data(),
        lemma_no_blow_not_bounded(),
        lemma_finer_still_open(),
        lemma_dns_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "DNS as an a priori",
            "tuning_the_pde": False,
            "n": 32,
            "T_long": T_LONG,
            "t_room": T_ROOM,
            "tesla": (
                "exacting, not a jerk. You asked if we had to stop. "
                "We ran it. We lengthened it. It is not a bound. "
                "Sit down. Do not spawn n=64."
            ),
            "domain_verdict": "open",
            "climb_dns_dead_end": True,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Climb and DNS knobs at n=32 are scored. DNS is not an a priori (B13f). "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not write c=8 into the PDE."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_dns.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DNS as an a priori. The runs are a check, not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
