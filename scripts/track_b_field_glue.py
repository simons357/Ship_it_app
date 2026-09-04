#!/usr/bin/env python3
"""
Field glue: the B9 ODE, read against NS Ẋ.

Classical NS. No Q1. No ε. Typed j*=2 CONC grows on the
sketch (B9b). The NS packet at the same box falls.
Sign of Ẋ is a number. α_c is a different number.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_balance import production_dissipation
from track_b_coherent import blob_packet
from track_b_evolve import packet_stats, shell_masses
from track_b_field_occ import DT, NU, STEPS, VOL, paths, scaled_packet
from track_b_glue import alpha_c, gamma_c, model_xdot, step_x
from track_b_lemmas import curl, rec

ALPHA_RATIO_MAX = 0.1
_RATES: dict[str, dict] | None = None


def field_rates(uh, vh, wh, kx, ky, kz, k2, nu: float, jstar: int) -> dict:
    pd = production_dissipation(uh, vh, wh, kx, ky, kz, nu)
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    st = packet_stats(shell_masses(oxh, oyh, ozh, k2, VOL), jstar)
    x = pd["X"]
    a = alpha_c(jstar)
    g = gamma_c(jstar, nu)
    xd_m = model_xdot(x, jstar, nu, True)
    cub_ns = 2.0 * pd["P"]
    visc_ns = 2.0 * pd["D"]
    a_imp = cub_ns / max(x**3, 1e-30)
    g_imp = visc_ns / max(x, 1e-30)
    return {
        "jstar": jstar,
        "jbar": st["jbar"],
        "sigma": st["sigma"],
        "X": x,
        "Xdot_ns": pd["Xdot"],
        "Xdot_model": xd_m,
        "alpha": a,
        "alpha_imp": a_imp,
        "alpha_ratio": abs(a_imp) / max(a, 1e-30),
        "gamma": g,
        "gamma_imp": g_imp,
        "visc_ratio": visc_ns / max(g * x, 1e-30),
        "sign_match": (pd["Xdot"] > 0.0) == (xd_m > 0.0),
        "P": pd["P"],
        "D": pd["D"],
    }


def model_delta(x0: float, jstar: int, nu: float, dt: float, steps: int) -> float:
    x = float(x0)
    for _ in range(steps):
        x = step_x(x, True, jstar, nu, dt)
        x = max(x, 0.0)
    return x - x0


def rates() -> dict[str, dict]:
    global _RATES
    if _RATES is None:
        uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, jstar = scaled_packet()
        pack = field_rates(uh, vh, wh, kx, ky, kz, k2, NU, jstar)
        blob = blob_packet()
        blob_r = field_rates(
            blob["uh"],
            blob["vh"],
            blob["wh"],
            blob["kx"],
            blob["ky"],
            blob["kz"],
            blob["k2"],
            NU,
            3,
        )
        ns = paths()
        pack["dX_ns"] = ns["packet"]["XT"] - ns["packet"]["X0"]
        blob_r["dX_ns"] = ns["blob"]["XT"] - ns["blob"]["X0"]
        pack["dX_model"] = model_delta(pack["X"], 2, NU, DT, STEPS)
        blob_r["dX_model"] = model_delta(blob_r["X"], 3, NU, DT, STEPS)
        _RATES = {"packet": pack, "blob": blob_r}
    return _RATES


def lemma_field_rates() -> dict:
    rows = rates()
    ok = all(
        r["sigma"] >= 0.5 and abs(r["Xdot_ns"]) > 0.0 and abs(r["Xdot_model"]) > 0.0
        for r in rows.values()
    )
    return rec(
        "B19_field_rates",
        "model Ẋ and NS Ẋ are both readable on the working-box packet and the signed-strain blob",
        "pass" if ok else "fail",
        "Same box as B13 / B17 / B18. Typed j* as in the sketch. j_bar is reported, not substituted.",
        Xdot_ns={"packet": rows["packet"]["Xdot_ns"], "blob": rows["blob"]["Xdot_ns"]},
        Xdot_model={"packet": rows["packet"]["Xdot_model"], "blob": rows["blob"]["Xdot_model"]},
        jbar={"packet": rows["packet"]["jbar"], "blob": rows["blob"]["jbar"]},
        sigma={"packet": rows["packet"]["sigma"], "blob": rows["blob"]["sigma"]},
    )


def lemma_sign_mismatch() -> dict:
    pack = rates()["packet"]
    return rec(
        "B19a_sign_mismatch",
        "the j*=2 CONC model has the same sign of Ẋ as the NS packet",
        "fail" if not pack["sign_match"] else "open",
        "Model Ẋ = +2.25. NS Ẋ ≈ −22.5. The sketch points up. The field points down.",
        Xdot_ns=pack["Xdot_ns"],
        Xdot_model=pack["Xdot_model"],
        sign_match=pack["sign_match"],
        jstar=pack["jstar"],
        jbar=pack["jbar"],
    )


def lemma_not_the_blowup() -> dict:
    pack = rates()["packet"]
    same_way = (pack["dX_ns"] > 0.0) == (pack["dX_model"] > 0.0)
    return rec(
        "B19b_not_the_blowup",
        "the working-box NS packet is the B9b blowup path",
        "fail" if not same_way else "open",
        "Eight steps: model X grows. NS X falls. B9b is a typed ODE, not this field.",
        dX_ns=pack["dX_ns"],
        dX_model=pack["dX_model"],
    )


def lemma_alpha_not_cubic() -> dict:
    rows = rates()
    calibrated = any(r["alpha_ratio"] >= ALPHA_RATIO_MAX for r in rows.values())
    return rec(
        "B19c_alpha_not_the_cubic",
        "α_c(j*) is the field cubic 2∫ω·Sω / X³",
        "fail" if not calibrated else "open",
        "Implied α sits near 0 on the packet (cancellation) and ~0.006 on the blob. The sketch used 0.4 and 0.2.",
        alpha={"packet": rows["packet"]["alpha"], "blob": rows["blob"]["alpha"]},
        alpha_imp={"packet": rows["packet"]["alpha_imp"], "blob": rows["blob"]["alpha_imp"]},
        alpha_ratio={"packet": rows["packet"]["alpha_ratio"], "blob": rows["blob"]["alpha_ratio"]},
    )


def lemma_gamma_not_visc() -> dict:
    pack = rates()["packet"]
    close = abs(pack["visc_ratio"] - 1.0) < 0.5
    return rec(
        "B19d_gamma_not_visc",
        "ν 2^{2j*} X is the NS visc term 2ν‖∇ω‖₂² on the j*=2 packet",
        "fail" if not close else "open",
        "2D / (γ X) ≈ 5.6. Bernstein-scale γ under-counts dissipation on a fat packet. j_bar sits near 3.",
        visc_ratio=pack["visc_ratio"],
        gamma=pack["gamma"],
        gamma_imp=pack["gamma_imp"],
        jbar=pack["jbar"],
    )


def lemma_field_glue_not_close() -> dict:
    return rec(
        "B19e_field_glue_not_X_a_priori",
        "matching the sketch to NS Ẋ closes a bound for classical X",
        "fail",
        "Scored as B30. A wrong-sign sketch is not continuation. The leftover cubic was not the field. NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer leftover is B22e.",
    )


def lemma_field_glue_not_a_retune() -> dict:
    return rec(
        "B19f_not_a_pde_retune",
        "reading model Ẋ against NS Ẋ, or shrinking α_c until they match, is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. α_c is a knob on the estimate. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_field_rates(),
        lemma_sign_mismatch(),
        lemma_not_the_blowup(),
        lemma_alpha_not_cubic(),
        lemma_gamma_not_visc(),
        lemma_field_glue_not_close(),
        lemma_field_glue_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "field glue; B9 ODE against NS Ẋ",
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
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer leftover is B22e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_field_glue.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Field glue. The sketch against NS Ẋ.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
