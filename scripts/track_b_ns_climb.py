#!/usr/bin/env python3
"""
NS climb law: c the field makes, on the blob and on B18 paths.

Classical NS. No Q1. No ε. Prescribed c=8 sits on the ODE
(B11c). t=0 random packets do not produce it (B12b). A
short packet run does not (B13a). This write asks the
signed-strain blob and the B18 trajectories. j_bar versus
typed j* at t=0 is a static offset, not a climb.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_balance import VOL
from track_b_climb_law import C_SAVE, hats_climb
from track_b_coherent import blob_packet
from track_b_evolve import ifrk2_step, packet_stats, shell_masses
from track_b_field_occ import DT, NU, STEPS, paths, scaled_packet
from track_b_lemmas import curl, rec

OFFSET_MIN = 0.5
_READ: dict[str, dict] | None = None


def euler_mean(uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, jstar: int) -> dict:
    uh, vh, wh = uh.copy(), vh.copy(), wh.copy()
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    j0 = packet_stats(shell_masses(oxh, oyh, ozh, k2, VOL), jstar)["jbar"]
    for _ in range(STEPS):
        uh, vh, wh = ifrk2_step(
            uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, 0.0, DT
        )
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    jT = packet_stats(shell_masses(oxh, oyh, ozh, k2, VOL), jstar)["jbar"]
    t = STEPS * DT
    return {
        "jbar0": float(j0),
        "jbarT": float(jT),
        "c_mean": float((jT - j0) / max(t, 1e-30)),
        "T": float(t),
    }


def readings() -> dict[str, dict]:
    global _READ
    if _READ is None:
        uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, jstar = scaled_packet()
        pack_t0_v = hats_climb(uh, vh, wh, kx, ky, kz, k2, NU, jstar)
        pack_t0_e = hats_climb(uh, vh, wh, kx, ky, kz, k2, 0.0, jstar)
        blob = blob_packet()
        blob_t0_v = hats_climb(
            blob["uh"], blob["vh"], blob["wh"], blob["kx"], blob["ky"], blob["kz"],
            blob["k2"], NU, 3,
        )
        blob_t0_e = hats_climb(
            blob["uh"], blob["vh"], blob["wh"], blob["kx"], blob["ky"], blob["kz"],
            blob["k2"], 0.0, 3,
        )
        visc = paths()
        pack_eu = euler_mean(uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, jstar)
        blob_eu = euler_mean(
            blob["uh"], blob["vh"], blob["wh"], blob["kx"], blob["ky"], blob["kz"],
            blob["k2"], blob["k2_safe"], blob["dealias"], 3,
        )
        _READ = {
            "packet": {
                "jstar": jstar,
                "t0_visc_c": pack_t0_v["c"],
                "t0_euler_c": pack_t0_e["c"],
                "c_mean_visc": visc["packet"]["c_mean"],
                "c_mean_euler": pack_eu["c_mean"],
                "jbar0": visc["packet"]["jbar0"],
                "jbarT_visc": visc["packet"]["jbarT"],
                "jbarT_euler": pack_eu["jbarT"],
                "offset": pack_t0_v["jbar"] - float(jstar),
                "sigma": pack_t0_v["sigma"],
                "finite": all(
                    map(
                        lambda x: x == x and abs(x) < 1e30,
                        (
                            pack_t0_v["c"],
                            pack_t0_e["c"],
                            visc["packet"]["c_mean"],
                            pack_eu["c_mean"],
                        ),
                    )
                ),
            },
            "blob": {
                "jstar": 3,
                "t0_visc_c": blob_t0_v["c"],
                "t0_euler_c": blob_t0_e["c"],
                "c_mean_visc": visc["blob"]["c_mean"],
                "c_mean_euler": blob_eu["c_mean"],
                "jbar0": visc["blob"]["jbar0"],
                "jbarT_visc": visc["blob"]["jbarT"],
                "jbarT_euler": blob_eu["jbarT"],
                "offset": blob_t0_v["jbar"] - 3.0,
                "sigma": blob_t0_v["sigma"],
                "finite": all(
                    map(
                        lambda x: x == x and abs(x) < 1e30,
                        (
                            blob_t0_v["c"],
                            blob_t0_e["c"],
                            visc["blob"]["c_mean"],
                            blob_eu["c_mean"],
                        ),
                    )
                ),
            },
        }
    return _READ


def lemma_field_c() -> dict:
    rows = readings()
    ok = all(r["finite"] and r["sigma"] >= 0.5 for r in rows.values())
    return rec(
        "B20_field_c",
        "c = d j_bar / dt is readable on the signed-strain blob and on B18 packet/blob paths",
        "pass" if ok else "fail",
        "t=0 from the vorticity RHS. Mean from Δj_bar / T on IF-RK2. Same box as B13 / B18. Typed j* is not substituted.",
        t0_visc={"packet": rows["packet"]["t0_visc_c"], "blob": rows["blob"]["t0_visc_c"]},
        t0_euler={"packet": rows["packet"]["t0_euler_c"], "blob": rows["blob"]["t0_euler_c"]},
        c_mean_visc={"packet": rows["packet"]["c_mean_visc"], "blob": rows["blob"]["c_mean_visc"]},
        c_mean_euler={"packet": rows["packet"]["c_mean_euler"], "blob": rows["blob"]["c_mean_euler"]},
        jbar0={"packet": rows["packet"]["jbar0"], "blob": rows["blob"]["jbar0"]},
        sigma={"packet": rows["packet"]["sigma"], "blob": rows["blob"]["sigma"]},
        c_save=C_SAVE,
    )


def lemma_blob_t0_not_saving() -> dict:
    blob = readings()["blob"]
    any_save = blob["t0_visc_c"] >= C_SAVE or blob["t0_euler_c"] >= C_SAVE
    return rec(
        "B20a_blob_t0_not_saving",
        "the signed-strain blob at t=0 produces c ≥ 8",
        "fail" if not any_save else "open",
        "Viscous t=0 c ≈ −2. Euler ≈ 0. Coherence of swirl is not a saving climb.",
        t0_visc_c=blob["t0_visc_c"],
        t0_euler_c=blob["t0_euler_c"],
        c_save=C_SAVE,
        sigma=blob["sigma"],
    )


def lemma_paths_not_saving() -> dict:
    rows = readings()
    any_save = any(
        r[k] >= C_SAVE
        for r in rows.values()
        for k in ("c_mean_visc", "c_mean_euler")
    )
    return rec(
        "B20b_paths_not_saving",
        "mean c on B18 packet and blob paths (visc and Euler) reaches c ≥ 8",
        "fail" if not any_save else "open",
        "Viscous means are negative. Euler means sit near 0. Letting the clock run did not hand us B11c.",
        c_mean_visc={"packet": rows["packet"]["c_mean_visc"], "blob": rows["blob"]["c_mean_visc"]},
        c_mean_euler={"packet": rows["packet"]["c_mean_euler"], "blob": rows["blob"]["c_mean_euler"]},
        c_save=C_SAVE,
    )


def lemma_blob_visc_not_ladder() -> dict:
    blob = readings()["blob"]
    down = blob["jbarT_visc"] < blob["jbar0"]
    return rec(
        "B20c_blob_visc_not_ladder",
        "viscosity on the signed-strain blob is a ladder for j_bar",
        "fail" if down else "open",
        "Along the B18 blob path, j_bar falls. Same direction as the t=0 RHS. Viscosity is not a climb.",
        jbar0=blob["jbar0"],
        jbarT=blob["jbarT_visc"],
        c_mean_visc=blob["c_mean_visc"],
    )


def lemma_offset_not_climb() -> dict:
    pack = readings()["packet"]
    static_then_down = pack["offset"] >= OFFSET_MIN and pack["c_mean_visc"] < 0.0
    return rec(
        "B20d_offset_not_climb",
        "j_bar > typed j* at t=0 is a climb",
        "fail" if static_then_down else "open",
        "Packet j_bar ≈ 2.97 versus typed 2 is a static offset. Then j_bar falls. Do not substitute j_bar for typed j* and call it B11c.",
        jstar=pack["jstar"],
        jbar0=pack["jbar0"],
        offset=pack["offset"],
        c_mean_visc=pack["c_mean_visc"],
        blob_offset=readings()["blob"]["offset"],
    )


def lemma_ns_climb_not_close() -> dict:
    return rec(
        "B20e_ns_climb_not_X_a_priori",
        "a field climb at this box closes a bound for classical X",
        "open",
        "NS did not force c=8 here. Finer/longer is B13e. Typing c=8 into the PDE is a retune. Not continuation.",
    )


def lemma_ns_climb_not_a_retune() -> dict:
    return rec(
        "B20f_not_a_pde_retune",
        "reading c from the vorticity RHS, or writing c=8 into classical Navier–Stokes, is a retune of the PDE",
        "fail",
        "The PDE is untouched. c is a knob on the estimate. No Q1. No ε. Do not type B11c into the equation.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_field_c(),
        lemma_blob_t0_not_saving(),
        lemma_paths_not_saving(),
        lemma_blob_visc_not_ladder(),
        lemma_offset_not_climb(),
        lemma_ns_climb_not_close(),
        lemma_ns_climb_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "NS climb law; c the field makes on blob and B18 paths",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. c the field makes, not a c we type. "
                "j_bar versus typed j* at t=0 is an offset, not a climb."
            ),
            "domain_verdict": "open",
            "c_save": C_SAVE,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Finer/longer climb (B13e). The climb sketch is not an NS a priori "
            "(B11e). NS did not force a saving c (B11d). B4c stands. "
            "Do not write c=8 into the PDE."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_ns_climb.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("NS climb law. c the field makes.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
