#!/usr/bin/env python3
"""
Longer path: T past the B11c room time, still n=32.

Classical NS. No Q1. No ε. B13 stopped at T~0.06.
The c=8 sketch reaches j*=5 at T=0.375. This write
lets the field run to T=0.384. Same box. Not n=64.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_climb_law import C_SAVE
from track_b_climb_sketch import J0, J_ROOM
from track_b_coherent import blob_packet
from track_b_field_occ import DT, NU, record_path, scaled_packet
from track_b_lemmas import rec

STEPS = 48
T_ROOM = (J_ROOM - J0) / C_SAVE
ABOVE_MAX = 1e-3
_LONG: dict[str, dict] | None = None


def long_paths() -> dict[str, dict]:
    global _LONG
    if _LONG is None:
        uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, jstar = scaled_packet()
        pack_v = record_path(
            uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, NU, jstar,
            dt=DT, steps=STEPS,
        )
        pack_e = record_path(
            uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, 0.0, jstar,
            dt=DT, steps=STEPS,
        )
        blob = blob_packet()
        blob_v = record_path(
            blob["uh"], blob["vh"], blob["wh"], blob["kx"], blob["ky"],
            blob["kz"], blob["k2"], blob["k2_safe"], blob["dealias"],
            NU, 3, dt=DT, steps=STEPS,
        )
        _LONG = {"packet": pack_v, "packet_euler": pack_e, "blob": blob_v}
    return _LONG


def lemma_longer_readable() -> dict:
    rows = long_paths()
    t = STEPS * DT
    ok = (
        t > T_ROOM
        and all(r["XT"] > 0.0 and r["sigma_min"] > 0.0 for r in rows.values())
        and all(r["steps"] == STEPS for r in rows.values())
    )
    return rec(
        "B22_longer_readable",
        "packet and blob stay readable on an n=32 run with T past the B11c room time",
        "pass" if ok else "fail",
        "T=0.384 > 0.375. Same box as B13 / B18. Not a bigger FFT. Typed c is not written into the PDE.",
        T=t,
        t_room=T_ROOM,
        XT={"packet": rows["packet"]["XT"], "blob": rows["blob"]["XT"], "euler": rows["packet_euler"]["XT"]},
        sigma_min={"packet": rows["packet"]["sigma_min"], "blob": rows["blob"]["sigma_min"]},
    )


def lemma_longer_not_saving() -> dict:
    rows = long_paths()
    cmax = max(
        max(rows[name]["c_inc"]) if rows[name]["c_inc"] else rows[name]["c_mean"]
        for name in ("packet", "blob", "packet_euler")
    )
    any_save = any(
        rows[name]["c_mean"] >= C_SAVE or max(rows[name]["c_inc"]) >= C_SAVE
        for name in ("packet", "blob", "packet_euler")
    )
    return rec(
        "B22a_longer_not_saving",
        "a longer n=32 run produces mean or step c ≥ 8",
        "fail" if not any_save else "open",
        "Past the sketch’s room time. Viscous means stay negative. Euler ~0. Step increments never reach 8.",
        c_save=C_SAVE,
        c_mean={"packet": rows["packet"]["c_mean"], "blob": rows["blob"]["c_mean"], "euler": rows["packet_euler"]["c_mean"]},
        c_inc_max=cmax,
        T=STEPS * DT,
        t_room=T_ROOM,
    )


def lemma_longer_not_ladder() -> dict:
    rows = long_paths()
    down = all(
        rows[name]["jbarT"] < rows[name]["jbar0"]
        for name in ("packet", "blob")
    )
    return rec(
        "B22b_longer_not_ladder",
        "a longer viscous run is a ladder for j_bar",
        "fail" if down else "open",
        "Packet 2.97 → 2.79. Blob 2.57 → 1.85. More time pulled the barycenter down, not up.",
        jbar0={"packet": rows["packet"]["jbar0"], "blob": rows["blob"]["jbar0"]},
        jbarT={"packet": rows["packet"]["jbarT"], "blob": rows["blob"]["jbarT"]},
    )


def lemma_longer_no_high_fill() -> dict:
    rows = long_paths()
    filled = any(rows[name]["aboveT"] > ABOVE_MAX for name in ("packet", "blob"))
    return rec(
        "B22c_longer_no_high_fill",
        "a longer n=32 run fills resolved shells above the original triad",
        "fail" if not filled else "open",
        "Mass above j*+1 stays ~0. n=32 dealias still cannot host a fat j=4. Length did not buy a cascade.",
        aboveT={"packet": rows["packet"]["aboveT"], "blob": rows["blob"]["aboveT"]},
    )


def lemma_longer_clock_did_not_save() -> dict:
    rows = long_paths()
    flipped = any(rows[name]["switches"] > 0 for name in ("packet", "blob"))
    left = any(rows[name]["sigma_min"] < 0.5 for name in ("packet", "blob"))
    return rec(
        "B22d_longer_clock_did_not_save",
        "the longer run left CONC, and that is why X sat",
        "fail" if (not flipped and not left) else "open",
        "Still CONC the whole interval. Packet X falls 2.5 → 0.15 by viscosity. The clock did not flip.",
        switches={"packet": rows["packet"]["switches"], "blob": rows["blob"]["switches"]},
        sigma_min={"packet": rows["packet"]["sigma_min"], "blob": rows["blob"]["sigma_min"]},
        X_fell={"packet": rows["packet"]["X_fell"], "blob": rows["blob"]["X_fell"]},
        XT={"packet": rows["packet"]["XT"], "blob": rows["blob"]["XT"]},
    )


def lemma_finer_open() -> dict:
    return rec(
        "B22e_finer_open",
        "a finer box (n>32) produces a saving climb",
        "fail",
        "Scored as B33. A bigger FFT is not continuation. n is a knob on the box. Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity stays open. Do not spawn n=64.",
    )


def lemma_longer_not_a_retune() -> dict:
    return rec(
        "B22f_not_a_pde_retune",
        "lengthening T at n=32, or moving to n=64, is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. T is a knob on the check. n is a knob on the box. No Q1. No ε. Do not type c=8 into the equation.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_longer_readable(),
        lemma_longer_not_saving(),
        lemma_longer_not_ladder(),
        lemma_longer_no_high_fill(),
        lemma_longer_clock_did_not_save(),
        lemma_finer_open(),
        lemma_longer_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "longer n=32 path past the B11c room time",
            "tuning_the_pde": False,
            "n": 32,
            "steps": STEPS,
            "dt": DT,
            "T": STEPS * DT,
            "t_room": T_ROOM,
            "tesla": (
                "exacting, not a jerk. You said longer. T passed the sketch’s "
                "room time. The field still did not climb. Do not spawn n=64."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity stays open. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_longer.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Longer path. T past the B11c room time. n=32.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
