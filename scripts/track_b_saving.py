#!/usr/bin/env python3
"""
NS climb as an a priori: a field that did not make c=8 is not a bound.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B20: c readable on blob and B18 paths. B20a: blob t=0
does not produce c≥8. B20b: path means do not. This write
asks whether that reading closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_climb_law import C_SAVE
from track_b_lemmas import rec
from track_b_ns_climb import (
    lemma_blob_t0_not_saving,
    lemma_blob_visc_not_ladder,
    lemma_field_c,
    lemma_offset_not_climb,
    lemma_paths_not_saving,
)


def lemma_saving_priori_readable() -> dict:
    field = lemma_field_c()
    blob = lemma_blob_t0_not_saving()
    paths = lemma_paths_not_saving()
    ok = (
        field["verdict"] == "pass"
        and blob["verdict"] == "fail"
        and paths["verdict"] == "fail"
        and blob["t0_visc_c"] < C_SAVE
        and blob["t0_euler_c"] < C_SAVE
        and all(c < C_SAVE for c in paths["c_mean_visc"].values())
        and all(c < C_SAVE for c in paths["c_mean_euler"].values())
    )
    return rec(
        "B31_saving_readable",
        "field c, blob t=0 miss, and path-mean miss are readable together",
        "pass" if ok else "fail",
        "Viscous t=0 c ≈ −2. Path means stay negative. Typed c is not written into the PDE.",
        t0_visc_c=blob["t0_visc_c"],
        t0_euler_c=blob["t0_euler_c"],
        c_mean_visc=paths["c_mean_visc"],
        c_mean_euler=paths["c_mean_euler"],
        c_save=C_SAVE,
    )


def lemma_field_c_not_a_priori() -> dict:
    paths = lemma_paths_not_saving()
    return rec(
        "B31a_field_c_not_a_priori",
        "a field climb at this box closes a bound for classical X",
        "fail",
        "The field did not hand us c=8. A missing saving rate is not continuation.",
        c_mean_visc=paths["c_mean_visc"],
    )


def lemma_offset_not_continuation() -> dict:
    off = lemma_offset_not_climb()
    return rec(
        "B31b_offset_not_continuation",
        "j_bar > typed j* at t=0 is a continuation argument for classical X",
        "fail",
        "Packet j_bar ≈ 2.97 versus typed 2 is a static offset. Then j_bar falls. Do not substitute a reading for B11c.",
        offset=off["offset"],
        c_mean_visc=off["c_mean_visc"],
    )


def lemma_ladder_not_a_class() -> dict:
    lad = lemma_blob_visc_not_ladder()
    return rec(
        "B31c_ladder_not_a_class",
        "viscosity pulling j_bar down is a geometric class that bounds X",
        "fail",
        "Dissipation owned the barycenter here. That is a reading, not a type. Do not promote a fall to a class.",
        jbar0=lad["jbar0"],
        jbarT=lad["jbarT"],
    )


def lemma_c_not_integral_max() -> dict:
    return rec(
        "B31d_c_not_integral_max",
        "reading c from the vorticity field is an integral bound on the max vorticity",
        "fail",
        "A barycenter rate is not ∫‖ω‖_∞. A missing climb is not the max criterion.",
    )


def lemma_sketch_leftover() -> dict:
    return rec(
        "B31e_sketch_leftover",
        "matching the prescribed-c sketch closes X",
        "fail",
        "Scored as B21e / B32. A short window is not the sitting. Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Regularity leftover is open. Do not spawn n=64.",
    )


def lemma_saving_priori_not_a_retune() -> dict:
    return rec(
        "B31f_not_a_pde_retune",
        "scoring NS climb as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. c is a knob on the estimate: a number you can miss. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_saving_priori_readable(),
        lemma_field_c_not_a_priori(),
        lemma_offset_not_continuation(),
        lemma_ladder_not_a_class(),
        lemma_c_not_integral_max(),
        lemma_sketch_leftover(),
        lemma_saving_priori_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "NS climb as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. c the field makes, not a c we type. "
                "It did not give you c=8."
            ),
            "domain_verdict": "open",
            "c_save": C_SAVE,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). "
            "Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). "
            "NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Regularity leftover is open. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_saving.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("NS climb as an a priori. A field that did not make c=8 is not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
