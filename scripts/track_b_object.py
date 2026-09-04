#!/usr/bin/env python3
"""
Regularity leftover as an a priori: leftover knobs do not decide X.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B14d–B35d are scored. Leftover closes are knobs on
the check. This write asks whether leftover knobs
decide classical regularity. They do not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_close import lemma_close_not_a_priori, lemma_close_priori_readable
from track_b_lemmas import rec


def lemma_object_priori_readable() -> dict:
    close = lemma_close_priori_readable()
    not_ap = lemma_close_not_a_priori()
    ok = (
        close["verdict"] == "pass"
        and not_ap["verdict"] == "fail"
        and close["T_long"] > close["t_room"]
        and close["c_inc_max"] < close["c_save"]
    )
    return rec(
        "B36_object_readable",
        "leftover catalog miss and leftover-close miss are readable together",
        "pass" if ok else "fail",
        "B34e and B35a are scored. Leftover knobs missed. Typed c is not written into the PDE.",
        T_long=close["T_long"],
        t_room=close["t_room"],
        c_inc_max=close["c_inc_max"],
        c_save=close["c_save"],
    )


def lemma_object_not_a_priori() -> dict:
    return rec(
        "B36a_object_not_a_priori",
        "leftover knobs decide classical regularity",
        "fail",
        "Leftover knobs are knobs on the check. The leftover is the object: a closed estimate for X. Sit down.",
    )


def lemma_object_not_continuation() -> dict:
    return rec(
        "B36b_object_not_continuation",
        "scoring the leftover catalog is continuation for classical X",
        "fail",
        "Continuation is an estimate, not a finished leftover list. B35b already missed that slogan.",
    )


def lemma_object_not_ns() -> dict:
    return rec(
        "B36c_object_not_ns",
        "naming the leftover as the object is still an NS a priori",
        "fail",
        "Naming the object is not sitting the packet. Do not promote a desk sentence to a type.",
    )


def lemma_object_not_integral_max() -> dict:
    return rec(
        "B36d_object_not_integral_max",
        "the leftover catalog is an integral bound on the max vorticity",
        "fail",
        "A leftover list is not ∫‖ω‖_∞. Beale still asks for the max.",
    )


def lemma_object_not_regularity() -> dict:
    return rec(
        "B36e_object_not_regularity",
        "this leftover close decides classical regularity",
        "fail",
        "No. Domain B stays open. The leftover is X. Do not spawn n=64. Do not type c=8 into the PDE.",
    )


def lemma_object_priori_not_a_retune() -> dict:
    return rec(
        "B36f_not_a_pde_retune",
        "scoring leftover knobs as not deciding regularity is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. Leftover knobs are knobs on the check. No Q1. No ε. Do not type c=8 into the equation. Do not spawn n=64.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_object_priori_readable(),
        lemma_object_not_a_priori(),
        lemma_object_not_continuation(),
        lemma_object_not_ns(),
        lemma_object_not_integral_max(),
        lemma_object_not_regularity(),
        lemma_object_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "regularity leftover as an a priori",
            "tuning_the_pde": False,
            "spawned_n64": False,
            "tesla": (
                "exacting, not a jerk. Leftover knobs are scored. "
                "The leftover is the object. Sit down."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). "
            "Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). "
            "NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). "
            "Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). "
            "Leftover close is not an a priori (B34e). Regularity leftover is not an a priori (B35e). "
            "Regularity stays open. Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_object.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Regularity leftover as an a priori. Leftover knobs do not decide X.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
