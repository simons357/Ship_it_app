#!/usr/bin/env python3
"""Extra-factor diagnostics on the growing-layer family.

Not a theorem. Unrestricted ★ is already dead. This only records which
field functionals grow on v_n, so a replacement inequality can be
stated honestly.

NS not solved. Not a singular NSE solution.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "growing_layer_replacement_factors.json"


def spectral_support(field: core.Field) -> dict:
    masses: dict[float, float] = {}
    for k, vk in field.modes.items():
        lam = core.lam(k)
        e = float(np.vdot(vk, vk).real)
        masses[lam] = masses.get(lam, 0.0) + e
    lambdas = sorted(masses)
    return {
        "n_shells": len(lambdas),
        "lambda_min": lambdas[0],
        "lambda_max": lambdas[-1],
        "aspect": lambdas[-1] / lambdas[0],
        "occupied_eigenvalues": lambdas,
    }


def factor_row(n: int) -> dict:
    rec = gl.record(n)
    field = gl.growing_layer(n)
    spec = spectral_support(field)
    rms = math.sqrt(rec["X"] / rec["E"])
    sqrt_lmax = math.sqrt(spec["lambda_max"])
    return {
        "n": n,
        "n_modes": rec["n_modes"],
        "n_shells": spec["n_shells"],
        "lambda_min": spec["lambda_min"],
        "lambda_max": spec["lambda_max"],
        "aspect": spec["aspect"],
        "lambda_min_is_n2": abs(spec["lambda_min"] - n * n) < 1e-12,
        "lambda_max_is_6n2": abs(spec["lambda_max"] - 6 * n * n) < 1e-12,
        "aspect_is_6": abs(spec["aspect"] - 6.0) < 1e-12,
        "E": rec["E"],
        "X": rec["X"],
        "Y": rec["Y"],
        "Z": rec["Z"],
        "Lambda": rec["Lambda"],
        "D_s": rec["D_s"],
        "T_c": rec["T_c"],
        "R_star": rec["R_star"],
        "R_over_n": rec["R_over_n"],
        "sqrt_X_over_E": rms,
        "sqrt_lambda_max": sqrt_lmax,
        "R_star_over_sqrt_X_over_E": rec["R_star"] / rms,
        "R_star_over_sqrt_lambda_max": rec["R_star"] / sqrt_lmax,
        "R_star_over_n_shells": rec["R_star"] / spec["n_shells"],
        "R_star_times_aspect": rec["R_star"] * spec["aspect"],
        "div_free": rec["div_free"],
        "real_valued": rec["real_valued"],
    }


def run(ns=(1, 2, 3, 4, 5, 6, 8)) -> dict:
    rows = [factor_row(n) for n in ns]
    payload = {
        "ns_solved": False,
        "singular_nse": False,
        "unrestricted_lemma_star": "KILLED_as_uniform_bound_on_this_family",
        "bounded_aspect_excludes_v_n": False,
        "aspect_on_this_family": 6.0,
        "note": (
            "v_n occupies lambda in [n^2, 6n^2], so aspect is exactly 6. "
            "A restriction lambda_max/lambda_min <= R for any R >= 6 still "
            "contains this family and therefore cannot restore unrestricted ★. "
            "Ratios R_star / sqrt(X/E) and R_star / sqrt(lambda_max) are "
            "diagnostics on this family only — not a proved replacement."
        ),
        "rows": rows,
        "all_aspect_6": all(r["aspect_is_6"] for r in rows),
        "all_div_free_real": all(r["div_free"] and r["real_valued"] for r in rows),
        "R_star_climbs": all(
            rows[i]["R_star"] > rows[i - 1]["R_star"] for i in range(1, len(rows))
        ),
        "R_over_sqrt_XE_does_not_climb_like_R": (
            rows[-1]["R_star_over_sqrt_X_over_E"]
            < rows[0]["R_star_over_sqrt_X_over_E"]
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    return payload


def main() -> None:
    payload = run()
    print(json.dumps({k: payload[k] for k in payload if k != "rows"}, indent=2))
    for r in payload["rows"]:
        print(
            f"n={r['n']} shells={r['n_shells']} "
            f"λ∈[{r['lambda_min']:.0f},{r['lambda_max']:.0f}] "
            f"aspect={r['aspect']:.0f} "
            f"R★={r['R_star']:.6g} "
            f"R★/√(X/E)={r['R_star_over_sqrt_X_over_E']:.6g} "
            f"R★/√λmax={r['R_star_over_sqrt_lambda_max']:.6g}"
        )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
