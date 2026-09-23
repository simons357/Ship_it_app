"""CS pairing remainder after the energy-class ladder. Not a close.

Exact: |T_c| <= ||L||_2 sqrt(D_s),
L = (ω·∇)u − (u·∇)ω (full field).
AM-GM: T_c <= θν D_s + ||L||_2^2 / (4θν).
Then K = ||L||_2^2 / (4θν X).

Two amplitude-legal useful doors:
  ||L||_2 <= C sqrt(E X)  =>  K ~ E
  ||L||_2 <= C X          =>  K ~ X/ν, (log Λ)' <= C' E/ν

The tight projection onto (A−Λ)ω is
  ||P L||_2 = |T_c|/sqrt(D_s),
hence K ~ T_c^2 / (D_s X) = R_★ E Λ. That is ★. Dead.

R_L = ||L||_2 / sqrt(X Y) is the B★ CS door. Not useful
even if bounded (AM-GM remainder Y/ν).

Do not overwrite stokes_moments.py.
Do not restore ★.
Do not seat B★.
Do not cash Attack-2 C_*.
Do not start leftover 1.
This is not docs/CS-REMAINDER.md (ABC evaluator).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from stokes_moments import (  # noqa: E402
    enforce_reality,
    k_norm2,
    probe,
    scale_field,
)
from bstar_attack import separated_triad  # noqa: E402
from bstar_symmetrize import fft_probe, omega_hat, power_law_field  # noqa: E402
from fourier_triangle import isosceles_hh_l  # noqa: E402
from ns_lemma_star_core import Field  # noqa: E402
from verify_pr24_closure_review import growing_layer_field  # noqa: E402

OUT = ROOT / "results" / "l_door.json"


def field_to_stokes_dict(field: Field) -> dict:
    return {k: v.copy() for k, v in field.modes.items()}


def L_hat(field: dict) -> dict:
    """Fourier of L = (ω·∇)u − (u·∇)ω, both orders, all landings."""
    field = enforce_reality(field)
    keys = list(field.keys())
    L: dict = {}
    for p in keys:
        up = field[p]
        wp = omega_hat(p, up)
        for q in keys:
            uq = field[q]
            wq = omega_hat(q, uq)
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            qv = np.array(q, dtype=np.float64)
            # Sign matches BSTAR-PROOF: L = (ω·∇)u − (u·∇)ω.
            contrib = 1j * (np.dot(wp, qv) * uq - np.dot(up, qv) * wq)
            L[k] = L.get(k, np.zeros(3, dtype=np.complex128)) + contrib
    return L


def L_norms(field: dict) -> dict:
    field = enforce_reality(field)
    pr = probe(field)
    L = L_hat(field)
    full = 0.0
    on = 0.0
    for k, lk in L.items():
        e = float(np.vdot(lk, lk).real)
        full += e
        if k in field:
            on += e
    l2 = math.sqrt(max(full, 0.0))
    l2_on = math.sqrt(max(on, 0.0))
    e, x, y, ds, tc = pr.E, pr.X, pr.Y, pr.Ds, abs(pr.Tc)
    r_le = l2 / math.sqrt(e * x) if e > 0 and x > 0 else float("nan")
    r_lx = l2 / x if x > 0 else float("nan")
    r_l = l2 / math.sqrt(x * y) if x > 0 and y > 0 else float("nan")
    tight = (tc / math.sqrt(ds) / x) if ds > 0 and x > 0 else float("nan")
    star_rem = (
        (tc * tc) / (ds * x) if ds > 0 and x > 0 else float("nan")
    )
    star_from_r = (
        pr.ratio_box * e * (y / x) if x > 0 and pr.ratio_box == pr.ratio_box else float("nan")
    )
    return {
        "E": e,
        "X": x,
        "Y": y,
        "Lambda": pr.Lambda,
        "Ds": ds,
        "Tc_abs": tc,
        "L2": l2,
        "L2_on": l2_on,
        "leak_L": ((full - on) / full) if full > 0 else 0.0,
        "R_LE": r_le,
        "R_LX": r_lx,
        "R_L": r_l,
        "tight_over_X": tight,
        "star_remainder": star_rem,
        "star_remainder_from_R": star_from_r,
        "R_star": pr.ratio_box,
    }


def from_fft(pr: dict) -> dict:
    e, x, y, l2, tc = pr["E"], pr["X"], pr["Y"], pr["L2"], abs(pr["Tc"])
    ds = pr["Ds"]
    return {
        "E": e,
        "X": x,
        "Y": y,
        "Lambda": pr["Lambda"],
        "Ds": ds,
        "Tc_abs": tc,
        "L2": l2,
        "R_LE": l2 / math.sqrt(e * x) if e > 0 and x > 0 else float("nan"),
        "R_LX": l2 / x if x > 0 else float("nan"),
        "R_L": pr["R_L"],
        "R_B": pr["R_B"],
    }


def amplitude_scan() -> dict:
    base = field_to_stokes_dict(isosceles_hh_l())
    rows = []
    for a in (0.05, 0.2, 1.0, 4.0):
        row = L_norms(scale_field(base, a))
        row["amp"] = a
        rows.append(row)
    r_le = [r["R_LE"] for r in rows]
    r_lx = [r["R_LX"] for r in rows]
    r_l = [r["R_L"] for r in rows]
    return {
        "rows": rows,
        "R_LE_flat": max(r_le) / min(r_le) < 1.01,
        "R_LX_flat": max(r_lx) / min(r_lx) < 1.01,
        "R_L_flat": max(r_l) / min(r_l) < 1.01,
        "L_degree": 2,
    }


def record() -> dict:
    amp = amplitude_scan()
    families = []
    for n in (1, 4, 8, 10):
        row = L_norms(growing_layer_field(n))
        row["label"] = f"vn{n}"
        families.append(row)
    for m in (1, 8):
        row = L_norms(separated_triad(m))
        row["label"] = f"sep{m}"
        families.append(row)
    for K, ngrid in ((4, 32), (6, 32), (8, 48)):
        pr = fft_probe(power_law_field(K, 2.0, "imag"), n=ngrid)
        row = from_fft(pr)
        row["label"] = f"imagK{K}"
        families.append(row)

    vn = [r for r in families if r["label"].startswith("vn")]
    imag = [r for r in families if r["label"].startswith("imag")]
    sep = [r for r in families if r["label"].startswith("sep")]

    # Tight door equals ★ remainder on v_n (same object).
    tight_is_star = all(
        abs(r["star_remainder"] - r["star_remainder_from_R"]) < 1e-8 * max(1.0, abs(r["star_remainder"]))
        for r in vn
    )

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "not_abc_cs_remainder_page": True,
        "not_attack2_Cstar": True,
        "homogeneity": {
            "L_degree": 2,
            "EXY_degree": 2,
            "LE_door": "||L||_2 <= C sqrt(E X)  =>  K ~ E",
            "LX_door": "||L||_2 <= C X  =>  K ~ X/ν, (log Λ)' <= C E/ν",
            "RL_door": "||L||_2 <= C sqrt(X Y)  =>  K ~ Y/ν  (B★ CS; not useful)",
            "tight_door": "|T_c|/sqrt(D_s) / X  =  R_★ E Λ / X * X  →  ★",
            "if_LE_sits": "Λ' <= 2 C' E",
            "if_LX_sits": "(log Λ)' <= C' E/ν",
        },
        "amplitude": amp,
        "tight_is_star": tight_is_star,
        "families": families,
        "vn_R_LE_grows": vn[-1]["R_LE"] > vn[0]["R_LE"],
        "vn_R_LX_grows": vn[-1]["R_LX"] > vn[0]["R_LX"],
        "imag_R_LE_grows": imag[-1]["R_LE"] > imag[0]["R_LE"],
        "imag_R_LX_grows": imag[-1]["R_LX"] > imag[0]["R_LX"],
        "sep_R_LE_grows": sep[-1]["R_LE"] > sep[0]["R_LE"],
        "sits_as_universal_C": False,
        "LE_door_dead": True,
        "LX_door_not_seated": True,
        "g4_stays_open": True,
        "vn_table": [
            {
                "label": r["label"],
                "R_LE": r["R_LE"],
                "R_LX": r["R_LX"],
                "R_L": r["R_L"],
                "leak_L": r["leak_L"],
                "Lambda": r["Lambda"],
            }
            for r in vn
        ],
        "imag_table": [
            {
                "label": r["label"],
                "R_LE": r["R_LE"],
                "R_LX": r["R_LX"],
                "R_L": r["R_L"],
                "Lambda": r["Lambda"],
            }
            for r in imag
        ],
        "sep_table": [
            {"label": r["label"], "R_LE": r["R_LE"], "R_LX": r["R_LX"]}
            for r in sep
        ],
    }
    out["LE_door_dead"] = bool(out["vn_R_LE_grows"] and out["imag_R_LE_grows"])
    out["LX_door_not_seated"] = bool(out["vn_R_LX_grows"] and out["imag_R_LX_grows"])
    out["sits_as_universal_C"] = False
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
