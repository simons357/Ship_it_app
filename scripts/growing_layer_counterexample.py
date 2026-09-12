#!/usr/bin/env python3
"""Growing-layer family vs the locked unrestricted Lemma★ core.

v_n(x,y,z) = D_n(z) (U_1(nx,ny), U_2(nx,ny), 0)
D_n(z) = sum_{|j|≤n} e^{ijz}
U = (-ψ_y, ψ_x),  ψ = cos x + cos(x+y) + cos(2x+y)

Fourier (this book's Field / set_mode):
  hat v(n r1, n r2, j) = (i/2)(-r2, r1, 0)
  r ∈ {±(1,0), ±(1,1), ±(2,1)},  |j|≤n.

Evaluator only. NS not solved. Not a singular NSE solution.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import ns_lemma_star_core as core  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "growing_layer.json"

R_PLANAR = ((1, 0), (-1, 0), (1, 1), (-1, -1), (2, 1), (-2, -1))

CLAIMED = {
    1: {"T_c": 21.0, "R_star": 0.001398359660043},
    2: {"T_c": 1824.0, "R_star": 0.002574888688615},
    3: {"T_c": 26973.0, "R_star": 0.003771825398057},
    4: {"T_c": 187392.0, "R_star": 0.004972851263004},
}


def growing_layer(n: int) -> core.Field:
    if n < 1:
        raise ValueError("n >= 1")
    f = core.Field()
    seen = set()
    for r1, r2 in R_PLANAR:
        amp = 0.5j * np.array([-float(r2), float(r1), 0.0], dtype=complex)
        for j in range(-n, n + 1):
            k = (n * r1, n * r2, j)
            if k == (0, 0, 0) or k in seen:
                continue
            f.set_mode(k, amp)
            seen.add(k)
            seen.add((-k[0], -k[1], -k[2]))
    return f


def formula_Tc(n: int) -> float:
    return 3.0 * (n**5) * (3 * n * n + 3 * n + 1)


def N_of(field: core.Field) -> float:
    total = 0.0
    for k, vk in field.modes.items():
        Bk = core.B_hat_at(field, k)
        Tk = -float(np.real(np.dot(Bk, np.conj(vk))))
        total += core.lam(k) * Tk
    return total


def hygiene(field: core.Field) -> dict:
    max_div = 0.0
    max_real = 0.0
    for k, vk in field.modes.items():
        max_div = max(max_div, abs(complex(np.dot(np.array(k, dtype=float), vk))))
        nk = (-k[0], -k[1], -k[2])
        max_real = max(max_real, float(np.linalg.norm(field.modes[nk] - np.conj(vk))))
    return {
        "n_modes": len(field.modes),
        "max_k_dot_v": max_div,
        "max_reality": max_real,
        "div_free": max_div < 1e-12,
        "real_valued": max_real < 1e-12,
    }


def record(n: int) -> dict:
    f = growing_layer(n)
    rec = core.R_star(f, verify=True, tol=1e-9)
    h = hygiene(f)
    N = N_of(f)
    Tc_form = formula_Tc(n)
    return {
        "n": n,
        **h,
        "E": rec["E"],
        "X": rec["X"],
        "Y": rec["Y"],
        "Z": rec["Z"],
        "Lambda": rec["Lambda"],
        "D_s": rec["D_s"],
        "T_c": rec["T_c"],
        "N": N,
        "R_star": rec["R_star"],
        "T_c_formula": Tc_form,
        "T_c_matches_formula": abs(rec["T_c"] - Tc_form) < 1e-6 * max(1.0, Tc_form),
        "elementary_lower": n / 165888.0,
        "R_over_n": rec["R_star"] / n,
        "vacuous_single_shell": rec["vacuous_single_shell"],
    }


def run(ns=(1, 2, 3, 4, 5, 6, 8)) -> dict:
    rows = [record(n) for n in ns]
    claimed_ok = True
    for r in rows:
        c = CLAIMED.get(r["n"])
        if not c:
            continue
        if abs(r["T_c"] - c["T_c"]) > 1e-6 * c["T_c"]:
            claimed_ok = False
        if abs(r["R_star"] - c["R_star"]) > 1e-12:
            claimed_ok = False
    climbs = all(rows[i]["R_star"] > rows[i - 1]["R_star"] for i in range(1, len(rows)))
    payload = {
        "ns_solved": False,
        "singular_nse": False,
        "family": "growing_layer_v_n",
        "unrestricted_lemma_star": "KILLED_as_uniform_bound_on_this_family",
        "evaluator": "scripts/ns_lemma_star_core.py",
        "cited_commit_has_proof_files": False,
        "cited_commit": "213e103ff83db18519d98d2274346c884af901dd",
        "rows": rows,
        "claimed_n1_to_n4_match": claimed_ok,
        "R_star_climbs_on_sample": climbs,
        "all_div_free_real": all(r["div_free"] and r["real_valued"] for r in rows),
        "all_N_zero": all(abs(r["N"]) < 1e-8 for r in rows),
        "all_Ds_positive": all(r["D_s"] > 1e-12 for r in rows),
        "note": (
            "Exact-shell 9D bound is a different statement and is not stamped here. "
            "Proof markdown was not on the cited commit. "
            "This is not a Navier-Stokes singularity."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    return payload


def main():
    payload = run()
    print(json.dumps({k: payload[k] for k in payload if k != "rows"}, indent=2))
    for r in payload["rows"]:
        print(
            f"n={r['n']} modes={r['n_modes']} Tc={r['T_c']:.6g} "
            f"R★={r['R_star']:.12g} R★/n={r['R_over_n']:.6g}"
        )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
