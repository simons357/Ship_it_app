#!/usr/bin/env python3
"""
Leftover close as an a priori: scoring leftovers does not write X.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B14d–B23e are scored. Geometry, budget, net, blob,
clock, glue, climb, sketch, longer path, DNS, finer
box, finer DNS. This write asks whether that catalog
closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_dns import lemma_finer_still_open
from track_b_finer import lemma_finer_not_a_priori
from track_b_lemmas import rec
from track_b_mesh import lemma_mesh_priori_readable


def lemma_close_priori_readable() -> dict:
    mesh = lemma_mesh_priori_readable()
    finer = lemma_finer_not_a_priori()
    dns = lemma_finer_still_open()
    ok = (
        mesh["verdict"] == "pass"
        and finer["verdict"] == "fail"
        and dns["verdict"] == "fail"
        and mesh["T_long"] > mesh["t_room"]
        and mesh["c_inc_max"] < mesh["c_save"]
    )
    return rec(
        "B35_close_readable",
        "finer-box miss, finer-DNS miss, and the leftover catalog are readable together",
        "pass" if ok else "fail",
        "B22e and B23e are scored. The leftover knobs missed. Typed c is not written into the PDE.",
        T_long=mesh["T_long"],
        t_room=mesh["t_room"],
        c_inc_max=mesh["c_inc_max"],
        c_save=mesh["c_save"],
    )


def lemma_close_not_a_priori() -> dict:
    return rec(
        "B35a_close_not_a_priori",
        "a leftover close writes a bound for classical X",
        "fail",
        "A catalog of fails is not continuation. Leftover knobs are knobs on the check. They do not write X.",
    )


def lemma_catalog_not_continuation() -> dict:
    return rec(
        "B35b_catalog_not_continuation",
        "scoring B14d through B23e is a continuation argument for classical X",
        "fail",
        "Continuation is an estimate, not a list of missed slogans. The field still has no bound.",
    )


def lemma_fails_not_ns() -> dict:
    return rec(
        "B35c_fails_not_ns",
        "a stack of leftover fails is still an NS a priori",
        "fail",
        "Failing a knob is not sitting the packet. Do not promote a catalog to a type.",
    )


def lemma_close_not_integral_max() -> dict:
    return rec(
        "B35d_close_not_integral_max",
        "leftover closes are an integral bound on the max vorticity",
        "fail",
        "A leftover close is a knob on the check. It is not ∫‖ω‖_∞. Beale still asks for the max.",
    )


def lemma_domain_leftover() -> dict:
    return rec(
        "B35e_domain_leftover",
        "classical regularity is decided by leftover closes",
        "open",
        "The leftover knobs are scored. The leftover is the object: a closed estimate for X. Domain B stays open.",
    )


def lemma_close_priori_not_a_retune() -> dict:
    return rec(
        "B35f_not_a_pde_retune",
        "scoring leftover closes as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. Leftover closes are knobs on the check. No Q1. No ε. Do not type c=8 into the equation. Do not spawn n=64.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_close_priori_readable(),
        lemma_close_not_a_priori(),
        lemma_catalog_not_continuation(),
        lemma_fails_not_ns(),
        lemma_close_not_integral_max(),
        lemma_domain_leftover(),
        lemma_close_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "leftover close as an a priori",
            "tuning_the_pde": False,
            "spawned_n64": False,
            "tesla": (
                "exacting, not a jerk. A leftover close is a knob on the check. "
                "It does not write X."
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
            "Leftover close is not an a priori (B34e). Regularity stays open. "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_close.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Leftover close as an a priori. Scoring leftovers does not write X.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
