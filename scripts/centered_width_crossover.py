"""Relative-width conventions: r^2 = D_s / (Lambda Y) = (sigma_lambda / Lambda)^2.

The unique exponent that makes D_s/Y have the scale of kappa = sqrt(Lambda)
is r ~ kappa^{-1/2}. That is arithmetic, not a stamped crossover theorem.
B^{prim} is not constructed here. NS is not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import centered_drift_triad_test as cdt  # noqa: E402
import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402


def from_moments(E: float, X: float, Y: float, Z: float, Lam: float, Ds: float) -> dict:
    r2 = Ds / (Lam * Y) if Lam > 0 and Y > 0 else float("nan")
    r = r2**0.5 if r2 == r2 and r2 >= 0 else float("nan")
    r_from_sigma = ((X * Ds) ** 0.5) / Y if Y else float("nan")
    kappa = Lam**0.5 if Lam > 0 else float("nan")
    thresh = kappa ** (-0.5) if kappa == kappa and kappa > 0 else float("nan")
    Ds_over_Y = Ds / Y if Y else float("nan")
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Lambda": Lam,
        "D_s": Ds,
        "r": r,
        "r_from_sigma_over_Lambda": r_from_sigma,
        "r_conventions_match": abs(r - r_from_sigma) <= 1e-12 * max(1.0, abs(r_from_sigma)),
        "kappa": kappa,
        "kappa_inv_sqrt": thresh,
        "Ds_over_Y": Ds_over_Y,
        "Lambda_r2": Lam * r2 if r2 == r2 else float("nan"),
        "Ds_over_Y_matches_Lambda_r2": abs(Ds_over_Y - Lam * r2) <= 1e-12 * max(1.0, abs(Ds_over_Y)),
        "region": "BROAD" if r == r and thresh == thresh and r >= thresh else "NARROW",
    }


def of_field(field: core.Field) -> dict:
    E, X, Y, Z, Lam = core.moments(field)
    Ds = core.D_s_moment_form(X, Y, Z)
    return from_moments(E, X, Y, Z, Lam, Ds)


def annular_field(alpha: int, beta: int, eps: float, seed: int = 20260922):
    rng = np.random.default_rng(seed)
    w = core.random_shell_field(alpha, rng, target_E=1.0)
    z, _raw = core.build_closing_direction(w, beta)
    if z is None:
        return None
    sign = core.choose_closing_sign(w, z)
    return core.combine_eps(w, z, sign * eps)


def run() -> dict:
    note = of_field(cdt.near_scale_triad())
    sep = of_field(cdt.separated_triad(8))
    vn = []
    for n in (1, 2, 4, 8):
        rec = of_field(gl.growing_layer(n))
        vn.append({"n": n, **rec})
    near = []
    for eps in (0.2, 0.1, 0.05, 0.025):
        field = annular_field(5, 4, eps)
        if field is None:
            continue
        rec = of_field(field)
        near.append({"eps": eps, "r": rec["r"], "kappa_inv_sqrt": rec["kappa_inv_sqrt"], "region": rec["region"]})
    rows = [note, sep] + vn
    return {
        "ns_solved": False,
        "crossover_stamped": False,
        "B_prim_constructed": False,
        "loop_families_on_this_tree": False,
        "r_definition": "sqrt(D_s / (Lambda Y)) = sigma_lambda / Lambda",
        "crossover_arithmetic": "r = kappa^{-1/2} => D_s/Y = kappa",
        "note_triad": note,
        "separated_L8": sep,
        "growing_layer": vn,
        "near_shell": near,
        "v_n_crosses_to_broad": vn[0]["region"] == "NARROW" and vn[-1]["region"] == "BROAD",
        "all_conventions_match": all(r["r_conventions_match"] and r["Ds_over_Y_matches_Lambda_r2"] for r in rows),
        "note": (
            "Relative width r is sigma_lambda/Lambda, not absolute sigma_lambda, "
            "and Lambda is Y/X, not a single-mode |k|^2. "
            "The -1/2 exponent is the unique scale that makes D_s/Y ~ kappa. "
            "Not a stamped decision theorem. B_prim not invented. NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "centered_width_crossover.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
