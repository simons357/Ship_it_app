"""Instantaneous M−ΛN cancellation after the L-doors. Not a close.

Exact: T_c = M − Λ N = Σ_k λ(λ−Λ) T_k,
N = Σ λ T_k, M = Σ λ² T_k, T_k = −Re(B̂_k · conj(v_k)).

On v_n: N = 0 (locked), so T_c = M and
R_mn = |T_c| / (|M| + Λ|N|) = 1.
No uniform instantaneous θ<1.

Signed spectral:
R_sign = |T_c| / Σ |λ(λ−Λ) T_k|.
Above/below Λ:
R_ab = |T_c| / (|T_hi| + |T_lo|).

Neither ratio is a useful K. A small
ratio on one family is not a remainder.

Do not overwrite stokes_moments.py.
Do not restore ★.
Do not seat B★.
Do not cash Attack-2 C_*.
Do not start leftover 1.
Do not split M and ΛN by Sobolev as
the first move.
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
    nonlinear_B,
    probe,
    scale_field,
)
from bstar_attack import separated_triad  # noqa: E402
from bstar_symmetrize import fft_probe, power_law_field  # noqa: E402
from fourier_triangle import isosceles_hh_l  # noqa: E402
from ns_lemma_star_core import Field  # noqa: E402
from verify_pr24_closure_review import growing_layer_field  # noqa: E402

OUT = ROOT / "results" / "mn_cancel.json"


def T_c_n(n: int) -> float:
    return 3.0 * (n**5) * (3 * n * n + 3 * n + 1)


def field_to_stokes_dict(field: Field) -> dict:
    return {k: v.copy() for k, v in field.modes.items()}


def T_k_from_B(field: dict, Buu: dict) -> dict:
    out = {}
    for k, vk in field.items():
        bk = Buu.get(k, np.zeros(3, dtype=np.complex128))
        out[k] = -float(np.vdot(bk, vk).real)
    return out


def signed_pieces(field: dict, Buu: dict, lam: float) -> dict:
    tk = T_k_from_B(field, Buu)
    t_hi = 0.0
    t_lo = 0.0
    abs_sum = 0.0
    n_acc = 0.0
    m_acc = 0.0
    tc_acc = 0.0
    for k, t in tk.items():
        l = k_norm2(k)
        n_acc += l * t
        m_acc += (l * l) * t
        c = l * (l - lam) * t
        tc_acc += c
        abs_sum += abs(c)
        if l > lam:
            t_hi += c
        elif l < lam:
            t_lo += c
    r_sign = abs(tc_acc) / abs_sum if abs_sum > 0 else float("nan")
    ab = abs(t_hi) + abs(t_lo)
    r_ab = abs(tc_acc) / ab if ab > 0 else float("nan")
    return {
        "N_from_Tk": n_acc,
        "M_from_Tk": m_acc,
        "Tc_from_Tk": tc_acc,
        "T_hi": t_hi,
        "T_lo": t_lo,
        "R_sign": r_sign,
        "R_ab": r_ab,
        "abs_vertex": abs_sum,
    }


def ratios_from_probe(pr) -> dict:
    n, m, tc, lam = pr.N, pr.M, pr.Tc, pr.Lambda
    maj = abs(m) + abs(lam) * abs(n)
    r_mn = abs(tc) / maj if maj > 0 else float("nan")
    return {
        "E": pr.E,
        "X": pr.X,
        "Y": pr.Y,
        "Lambda": lam,
        "Ds": pr.Ds,
        "N": n,
        "M": m,
        "Tc": tc,
        "R_mn": r_mn,
        "N_is_zero": abs(n) < 1e-8,
    }


def score_field(field: dict, label: str) -> dict:
    field = enforce_reality(field)
    pr = probe(field, label=label)
    row = ratios_from_probe(pr)
    Buu = nonlinear_B(field)
    signed = signed_pieces(field, Buu, pr.Lambda)
    # Identity lock: spectral T_k rebuilds probe N, M, T_c.
    row["N_match"] = abs(signed["N_from_Tk"] - pr.N) < 1e-8 * max(1.0, abs(pr.N))
    row["M_match"] = abs(signed["M_from_Tk"] - pr.M) < 1e-8 * max(1.0, abs(pr.M))
    row["Tc_match"] = abs(signed["Tc_from_Tk"] - pr.Tc) < 1e-8 * max(1.0, abs(pr.Tc))
    row["R_sign"] = signed["R_sign"]
    row["R_ab"] = signed["R_ab"]
    row["T_hi"] = signed["T_hi"]
    row["T_lo"] = signed["T_lo"]
    row["label"] = label
    return row


def from_fft(pr: dict, label: str) -> dict:
    n, m, tc, lam = pr["N"], pr["M"], pr["Tc"], pr["Lambda"]
    maj = abs(m) + abs(lam) * abs(n)
    r_mn = abs(tc) / maj if maj > 0 else float("nan")
    return {
        "E": pr["E"],
        "X": pr["X"],
        "Y": pr["Y"],
        "Lambda": lam,
        "Ds": pr["Ds"],
        "N": n,
        "M": m,
        "Tc": tc,
        "R_mn": r_mn,
        "N_is_zero": abs(n) < 1e-8,
        "label": label,
    }


def amplitude_scan() -> dict:
    base = field_to_stokes_dict(isosceles_hh_l())
    rows = []
    for a in (0.05, 0.2, 1.0, 4.0):
        row = score_field(scale_field(base, a), f"amp{a}")
        row["amp"] = a
        rows.append(row)
    r_mn = [r["R_mn"] for r in rows]
    r_sign = [r["R_sign"] for r in rows]
    r_ab = [r["R_ab"] for r in rows]
    return {
        "rows": rows,
        "R_mn_flat": max(r_mn) / min(r_mn) < 1.01,
        "R_sign_flat": max(r_sign) / min(r_sign) < 1.01,
        "R_ab_flat": max(r_ab) / min(r_ab) < 1.01,
        "identities": all(r["N_match"] and r["M_match"] and r["Tc_match"] for r in rows),
    }


def record() -> dict:
    amp = amplitude_scan()
    families = []
    vn_closed = []
    for n in (1, 4, 8, 10):
        row = score_field(growing_layer_field(n), f"vn{n}")
        families.append(row)
        tc = T_c_n(n)
        vn_closed.append(
            {
                "n": n,
                "N_closed": 0.0,
                "M_closed": tc,
                "Tc_closed": tc,
                "R_mn_closed": 1.0,
                "N_live": row["N"],
                "M_live": row["M"],
                "Tc_live": row["Tc"],
                "R_mn_live": row["R_mn"],
                "R_sign": row["R_sign"],
                "R_ab": row["R_ab"],
            }
        )
    for m in (1, 8):
        families.append(score_field(separated_triad(m), f"sep{m}"))
    imag = []
    for K, ngrid in ((4, 32), (6, 32), (8, 48)):
        pr = fft_probe(power_law_field(K, 2.0, "imag"), n=ngrid)
        row = from_fft(pr, f"imagK{K}")
        families.append(row)
        imag.append(row)

    vn = [r for r in families if r["label"].startswith("vn")]
    sep = [r for r in families if r["label"].startswith("sep")]

    vn_N_zero = all(r["N_is_zero"] for r in vn)
    vn_R_mn_one = all(abs(r["R_mn"] - 1.0) < 1e-8 for r in vn)
    vn_closed_match = all(
        abs(c["Tc_live"] - c["Tc_closed"]) < 1e-6 * max(1.0, abs(c["Tc_closed"]))
        and abs(c["N_live"]) < 1e-8
        for c in vn_closed
    )

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "not_attack2_Cstar": True,
        "do_not_split_MN_by_sobolev": True,
        "homogeneity": {
            "M_N_Tc_degree": 3,
            "R_mn_scale_invariant": True,
            "R_sign_scale_invariant": True,
            "if_theta_sat": "R_mn <= θ < 1 would be instantaneous cancellation; still need |M|+Λ|N|",
        },
        "amplitude": amp,
        "identities_sit": bool(amp["identities"] and vn_closed_match),
        "vn_N_zero": vn_N_zero,
        "vn_R_mn_one": vn_R_mn_one,
        "vn_closed_match": vn_closed_match,
        "instantaneous_MN_dead": bool(vn_N_zero and vn_R_mn_one),
        "sits_as_universal_theta": False,
        "g4_stays_open": True,
        "families": families,
        "vn_closed": vn_closed,
        "vn_table": [
            {
                "label": r["label"],
                "N": r["N"],
                "M": r["M"],
                "Tc": r["Tc"],
                "R_mn": r["R_mn"],
                "R_sign": r["R_sign"],
                "R_ab": r["R_ab"],
            }
            for r in vn
        ],
        "imag_table": [
            {"label": r["label"], "R_mn": r["R_mn"], "N": r["N"], "M": r["M"], "Tc": r["Tc"]}
            for r in imag
        ],
        "sep_table": [
            {
                "label": r["label"],
                "R_mn": r["R_mn"],
                "R_sign": r["R_sign"],
                "R_ab": r["R_ab"],
                "N": r["N"],
            }
            for r in sep
        ],
    }
    # Signed door: v_n does not force R_sign = 1, but a useful K
    # does not follow from a finite ratio. Record growth only.
    out["vn_R_sign"] = [r["R_sign"] for r in vn]
    out["vn_R_ab"] = [r["R_ab"] for r in vn]
    out["imag_R_mn_not_one"] = all(r["R_mn"] < 0.999 for r in imag)
    out["sits_as_universal_theta"] = False
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
