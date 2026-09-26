"""Explicit K-candidate score sheet for the comparable / near-shell piece.

Uniform energy-class slots are tested on v_n (aspect 6: comparable).
Instantaneous Young packaging is an identity, not a bound.
Claimed 16/9 is a restricted-class majorant, not this remainder.
NS is not solved. Not a closure theorem.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import growing_layer_counterexample as gl  # noqa: E402
import centered_drift_triad_split as split  # noqa: E402
import centered_drift_triad_test as cdt  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402

THETA = 0.5
NU = 1.0
C_SHELL = 16.0 / 9.0
SLOT_KEYS = (
    "T_c_over_E",
    "T_c_over_sqrtX",
    "T_c_over_X",
    "T_c_over_Y",
    "T_c_over_EL",
    "T_c_over_EY",
    "T_c_over_sqrtDsEY",
)


def _finite(x: float) -> bool:
    return x == x and abs(x) != float("inf")


def slots(rec: dict) -> dict:
    Tc = max(float(rec["T_c"]), 0.0)
    E, X, Y, Ds, Lam, R = (
        float(rec["E"]),
        float(rec["X"]),
        float(rec["Y"]),
        float(rec["D_s"]),
        float(rec["Lambda"]),
        float(rec["R_star"]),
    )
    young = (R * E * Y) / (4.0 * THETA * NU) if _finite(R) else float("nan")
    shell_rem = (C_SHELL * E * Y) / (4.0 * THETA * NU)
    out = {
        "T_c_plus": Tc,
        "T_c_over_E": Tc / E if E else None,
        "T_c_over_sqrtX": Tc / (X**0.5) if X else None,
        "T_c_over_X": Tc / X if X else None,
        "T_c_over_Y": Tc / Y if Y else None,
        "T_c_over_EL": Tc / (E * Lam) if E and Lam else None,
        "T_c_over_EY": Tc / (E * Y) if E and Y else None,
        "T_c_over_sqrtDsEY": Tc / ((Ds * E * Y) ** 0.5) if Ds > 0 and E and Y else None,
        "K_taut": (Tc - THETA * NU * Ds) / X if X and Tc > THETA * NU * Ds else 0.0,
        "K_Y_taut": (Tc - THETA * NU * Ds) / Y if Y and Tc > THETA * NU * Ds else 0.0,
        "K_inst": (R * E * Lam) / (4.0 * THETA * NU) if _finite(R) else None,
        "K_Y_inst": (R * E) / (4.0 * THETA * NU) if _finite(R) else None,
        "K_shell_claimed": (C_SHELL * E * Lam) / (4.0 * THETA * NU),
        "K_Y_shell_claimed": (C_SHELL * E) / (4.0 * THETA * NU),
        "young_remainder": young,
        "shell_remainder": shell_rem,
        "young_covers": bool(Tc <= THETA * NU * Ds + young + 1e-8) if _finite(young) else False,
        "shell_covers": bool(Tc <= THETA * NU * Ds + shell_rem + 1e-8),
        "R_star": R,
    }
    return out


def compact(rec: dict, extra: tuple = ()) -> dict:
    keys = (
        "E",
        "X",
        "Y",
        "Lambda",
        "D_s",
        "T_c",
        "R_star",
        "T_c_plus",
        *SLOT_KEYS,
        "K_taut",
        "K_Y_taut",
        "K_inst",
        "K_Y_inst",
        "K_shell_claimed",
        "young_covers",
        "shell_covers",
        *extra,
    )
    return {k: rec[k] for k in keys if k in rec}


def with_moments(field) -> dict:
    rec = core.R_star(field)
    rec.update(slots(rec))
    return rec


def slot_growth(rows: list) -> dict:
    a, b = rows[0], rows[-1]
    out = {}
    for key in SLOT_KEYS:
        va, vb = a[key], b[key]
        out[key] = {
            "n1": va,
            "n_last": vb,
            "ratio": (vb / va) if va else None,
            "grows": bool(va and vb > 2.0 * va),
        }
    out["R_star"] = {
        "n1": a["R_star"],
        "n_last": b["R_star"],
        "ratio": b["R_star"] / a["R_star"],
        "grows": b["R_star"] > 2.0 * a["R_star"],
    }
    return out


def run() -> dict:
    note = with_moments(cdt.near_scale_triad())
    sep = with_moments(cdt.separated_triad(8))
    vn = []
    for n in (1, 2, 4, 8):
        r = gl.record(n)
        r.update(slots(r))
        vn.append({"n": n, **compact(r)})
    annular = []
    for eps in (0.2, 0.1, 0.05, 0.025):
        rec = split.annular_two_shell(5, 4, np.random.default_rng(20260922), eps=eps)
        if rec.get("empty_closer"):
            continue
        rec.update(slots(rec))
        annular.append(
            {
                "eps": eps,
                "T_c": rec["T_c"],
                "D_s": rec["D_s"],
                "X": rec["X"],
                "R_star": rec["R_star"],
                "T_c_over_X": rec["T_c_over_X"],
                "T_c_over_Ds": rec["T_c"] / rec["D_s"] if rec["D_s"] else None,
                "K_inst": rec["K_inst"],
                "K_shell_claimed": rec["K_shell_claimed"],
                "young_covers": rec["young_covers"],
                "shell_covers": rec["shell_covers"],
            }
        )
    growth = slot_growth(vn)
    return {
        "ns_solved": False,
        "theta": THETA,
        "nu": NU,
        "C_shell_claimed": C_SHELL,
        "comparable_class_contains_v_n": True,
        "v_n_aspect": 6,
        "note_triad": compact(note),
        "separated_L8": compact(sep),
        "growing_layer": vn,
        "near_shell": annular,
        "slot_growth_v_n": growth,
        "uniform_slots_killed_by_v_n": [
            "E",
            "sqrt(X)",
            "X",
            "Y",
            "E Lambda",
            "E Y",
            "sqrt(D_s E Y) with uniform C",
        ],
        "all_young_covers": all(
            [note["young_covers"], sep["young_covers"]]
            + [r["young_covers"] for r in vn]
            + [r["young_covers"] for r in annular]
        ),
        "all_uniform_slots_grow_on_v_n": all(growth[k]["grows"] for k in SLOT_KEYS),
        "K_formula_proved": None,
        "K_formula": "not written",
        "note": (
            "K_inst is Young packaging of instantaneous R_star, an identity, not a bound. "
            "K_shell_claimed uses 16/9 and is restricted; v_n leaves that class. "
            "Uniform energy-class slots die on v_n. "
            "NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "centered_drift_k_candidates.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
