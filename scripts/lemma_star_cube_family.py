#!/usr/bin/env python3
"""
Named SuperGrok cube family against the locked Lemma★ evaluator.

    v̂_n(k) = [k1 (-k1² + i n k2) / n^7] (-k2, k1, 0)
    for integer k with |k_j| ≤ n, k ≠ 0.

This is not Fourier dilation v(n·). Support grows with n.
Not a proof. Not H1. NS is not solved.
Screenshots are not a kill stamp. The locked R_star is the check.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ns_attacks.ns_lemma_star_core import (  # noqa: E402
    D_s_direct_form,
    D_s_moment_form,
    Field,
    R_star,
    T_c_from_MN,
    moments,
)
from track_b_lemmas import rec  # noqa: E402

# SuperGrok wrote both this fraction and ~3.9677e-8. They disagree.
# The fraction evaluates to ~3.967e-10. Neither is the discrete R_star/n^3.
C_BOX_NUM = 1523085778924828999575
C_BOX_DEN = 3839130303817223093956294737922
C_BOX = C_BOX_NUM / C_BOX_DEN
C_BOX_FLOAT_CLAIMED = 3.9677e-8


def cube_amp(n: int, k: tuple[int, int, int]) -> np.ndarray:
    """Exact mode formula from the screenshot dump. Already div-free."""
    k1, k2, _k3 = k
    alpha = (k1 * (-(k1**2) + 1j * n * k2)) / (n**7)
    return alpha * np.array([-k2, k1, 0.0], dtype=complex)


def is_canonical(k: tuple[int, int, int]) -> bool:
    for c in k:
        if c != 0:
            return c > 0
    return False


def cube_field(n: int) -> Field:
    """Build v_n. set_mode writes the conjugate partner."""
    if int(n) < 1:
        raise ValueError("cube half-width n must be a positive integer.")
    n = int(n)
    f = Field()
    for k1 in range(-n, n + 1):
        for k2 in range(-n, n + 1):
            for k3 in range(-n, n + 1):
                k = (k1, k2, k3)
                if k == (0, 0, 0) or not is_canonical(k):
                    continue
                w = cube_amp(n, k)
                if np.linalg.norm(w) == 0.0:
                    continue
                f.set_mode(k, w)
    return f


def _divfree_reality(field: Field, tol: float = 1e-10) -> dict:
    max_div = 0.0
    max_real = 0.0
    missing = 0
    for k, vk in field.modes.items():
        max_div = max(max_div, abs(complex(np.dot(np.array(k, dtype=float), vk))))
        nk = tuple(-x for x in k)
        if nk not in field.modes:
            missing += 1
            continue
        max_real = max(
            max_real, float(np.linalg.norm(field.modes[nk] - np.conj(vk)))
        )
    return {
        "n_modes": len(field.modes),
        "max_kdot_v": max_div,
        "max_reality_err": max_real,
        "missing_conjugates": missing,
        "ok": max_div <= tol and max_real <= tol and missing == 0,
    }


def row(n: int) -> dict:
    v = cube_field(n)
    setup = _divfree_reality(v)
    r = R_star(v)
    E, X, Y, Z, Lam = moments(v)
    ds_m = D_s_moment_form(X, Y, Z)
    ds_d = D_s_direct_form(v, Lam)
    N, M, Tc_mn = T_c_from_MN(v, Lam)
    rev = R_star(v.scale(-1.0))
    amp = R_star(v.scale(3.0))
    rs = float(r["R_star"])
    tc = float(r["T_c"])
    rs_rev = float(rev["R_star"])
    rs_best = max(rs, rs_rev)
    return {
        "n": n,
        "n_modes": setup["n_modes"],
        "setup": setup,
        "E": float(E),
        "X": float(X),
        "Y": float(Y),
        "Z": float(Z),
        "Lambda": float(Lam),
        "Ds_moment": float(ds_m),
        "Ds_direct": float(ds_d),
        "Ds_match": abs(ds_m - ds_d) <= 1e-9 * max(abs(ds_m), abs(ds_d), 1.0),
        "N": float(N),
        "M": float(M),
        "T_c": tc,
        "T_c_MN": float(Tc_mn),
        "T_c_reverse": float(rev["T_c"]),
        "R_star": rs,
        "R_star_reverse": rs_rev,
        "R_star_best": rs_best,
        "R_star_amp": float(amp["R_star"]),
        "amp_flat": abs(rs - float(amp["R_star"])) <= 1e-10 * max(abs(rs), 1e-30),
        "Tc_odd": abs(float(rev["T_c"]) + tc) <= 1e-10 * max(abs(tc), 1e-30),
        "n3_E": float(n**3 * E),
        "Y_over_n": float(Y / n),
        "Ds_over_n3": float(ds_d / (n**3)),
        "Tc_over_n2": float(tc / (n**2)),
        "R_star_over_n3": rs / (n**3) if n else float("nan"),
        "R_star_best_over_n3": rs_best / (n**3) if n else float("nan"),
        "c_box": C_BOX,
    }


def sweep(nmax: int = 3) -> dict:
    rows = [row(n) for n in range(1, int(nmax) + 1)]
    best = [r["R_star_best"] for r in rows]
    ratios = [r["R_star_best_over_n3"] for r in rows]
    growing = len(best) >= 2 and all(
        best[i + 1] > best[i] * 1.05 for i in range(len(best) - 1)
    )
    positive_scale = all(x > 0.0 and np.isfinite(x) for x in ratios)
    return {
        "meta": {
            "slot": "B",
            "write": "Lemma★ cube family against the lock",
            "family": "vhat_n(k) = k1(-k1^2 + i n k2) n^{-7} (-k2, k1, 0) on |k_j|<=n",
            "tuning_the_pde": False,
            "lemma_star_open": True,
            "h1_started": False,
            "new_family_arrived": True,
            "screenshots_are_a_stamp": False,
            "kill": False,
            "c_box_claimed": C_BOX,
            "nmax": int(nmax),
            "R_star_best_grows": growing,
            "R_star_over_n3_positive": positive_scale,
        },
        "rows": rows,
    }


def lemmas(payload: dict) -> list[dict]:
    rows = payload["rows"]
    setup_ok = all(r["setup"]["ok"] and r["Ds_match"] for r in rows)
    amp_odd = all(r["amp_flat"] and r["Tc_odd"] for r in rows)
    finite = all(np.isfinite(r["R_star_best"]) for r in rows)
    growing = bool(payload["meta"]["R_star_best_grows"])
    return [
        rec(
            "LScube_named",
            "growing cube family is now named on this branch",
            "pass",
            "Support |k_j|<=n. Not v(n·). Screenshots named it; this book builds it.",
        ),
        rec(
            "LScube_lock_first",
            "check locked Ds, Tc, R★ before a kill stamp",
            "pass",
            "Desk rule. SuperGrok screenshots are not the evaluator.",
        ),
        rec(
            "LScube_div_real",
            "div-free and v_{-k}=conj(v_k) on v_n",
            "pass" if setup_ok else "fail",
            "Admissible on the cube. Not Hadamard well-posedness of NSE.",
        ),
        rec(
            "LScube_amp_odd",
            "R★(av)=R★(v); Tc odd",
            "pass" if amp_odd else "fail",
            "Amplitude invariant sits. Reverse is required.",
        ),
        rec(
            "LScube_screenshot_stamp",
            "screenshots stamp unrestricted ★ false",
            "fail",
            "A named family is a check. The lock stamps, not SuperGrok.",
        ),
        rec(
            "LScube_bernstein_every_n",
            "degree-52 Bernstein certificate for every n>=2",
            "fail",
            "SuperGrok did not regenerate it. This book does not either.",
        ),
        rec(
            "LScube_ns_solved",
            "cube family solves NS or starts H1",
            "fail",
            "Not a trajectory. Not WRITE (6). ★ => GR still one way.",
        ),
        rec(
            "LScube_unrestricted_killed",
            "unrestricted Lemma★ is killed",
            "fail",
            (
                "Locked samples are finite. Growth on a short n-list "
                "is a clue, not R★→∞. ★ stays OPEN."
                if finite
                else "A non-finite R★ would be the vacuous or singular case."
            ),
            R_star_best=[r["R_star_best"] for r in rows],
            R_star_best_over_n3=[r["R_star_best_over_n3"] for r in rows],
            grows=growing,
        ),
    ]


def run(nmax: int = 3, out: Path | None = None) -> dict:
    payload = sweep(nmax=nmax)
    rows = lemmas(payload)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for item in rows:
        counts[item["verdict"]] += 1
    payload["lemmas"] = rows
    payload["counts"] = counts
    payload["domain_verdict"] = "open"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--nmax", type=int, default=3)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    payload = run(nmax=args.nmax, out=args.out)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
