"""Centered spectral barycenter: D_s = X Var_p(λ), T_c = X Cov_p(λ, t).

t_k = T_k / |u_k|^2 is stretching per mode energy.
T_c / D_s is the OLS slope of t on λ under the enstrophy measure.
Algebra plus a score on the live families. Not a remainder theorem.
NS is not solved.
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

THETA = 0.5
NU = 1.0
BAND_ETA = 0.5  # relative: |λ − Λ| / Λ ≤ η is the barycenter band


def mode_rows(field: core.Field) -> tuple[list[dict], dict]:
    E, X, Y, Z, Lam = core.moments(field)
    if X <= 0:
        raise ValueError("X must be positive")
    rows = []
    N = 0.0
    Tc = 0.0
    Ds = 0.0
    for k, vk in field.modes.items():
        e = float(np.vdot(vk, vk).real)
        ell = core.lam(k)
        Bk = core.B_hat_at(field, k)
        Tk = -float(np.real(np.dot(Bk, np.conj(vk))))
        N += ell * Tk
        Tc += ell * (ell - Lam) * Tk
        Ds += ell * (ell - Lam) ** 2 * e
        p = (ell * e) / X
        t = Tk / e if e > 1e-15 else 0.0
        rows.append(
            {
                "k": k,
                "lam": ell,
                "e": e,
                "T": Tk,
                "p": p,
                "t": t,
            }
        )
    return rows, {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "D_s": Ds,
        "T_c": Tc,
        "N": N,
    }


def barycenter(field: core.Field) -> dict:
    rows, mom = mode_rows(field)
    X, Lam, Ds, Tc, N = mom["X"], mom["Lambda"], mom["D_s"], mom["T_c"], mom["N"]
    p_sum = sum(r["p"] for r in rows)
    mean_lam = sum(r["p"] * r["lam"] for r in rows)
    mean_t = sum(r["p"] * r["t"] for r in rows)
    var = sum(r["p"] * (r["lam"] - Lam) ** 2 for r in rows)
    cov = sum(r["p"] * (r["lam"] - Lam) * r["t"] for r in rows)
    mean_t2 = sum(r["p"] * r["t"] * r["t"] for r in rows)
    var_t = mean_t2 - mean_t * mean_t
    sig_lam = var**0.5 if var > 0 else 0.0
    sig_t = var_t**0.5 if var_t > 0 else 0.0
    corr = cov / (sig_lam * sig_t) if sig_lam > 0 and sig_t > 0 else None
    slope = cov / var if var > 0 else None
    rel_width = sig_lam / Lam if Lam else None
    band_ds = 0.0
    band_tc = 0.0
    wing_ds = 0.0
    wing_tc = 0.0
    n_band = 0
    for r in rows:
        central = Lam > 0 and abs(r["lam"] - Lam) / Lam <= BAND_ETA
        dpiece = r["p"] * X * (r["lam"] - Lam) ** 2
        tpiece = r["p"] * X * (r["lam"] - Lam) * r["t"]
        if central:
            band_ds += dpiece
            band_tc += tpiece
            n_band += 1
        else:
            wing_ds += dpiece
            wing_tc += tpiece
    return {
        **mom,
        "p_sum": p_sum,
        "Lambda_from_p": mean_lam,
        "mean_t": mean_t,
        "N_over_X": N / X,
        "Var_p_lambda": var,
        "Cov_p_lambda_t": cov,
        "sigma_lambda": sig_lam,
        "sigma_t": sig_t,
        "corr": corr,
        "slope": slope,
        "rel_width": rel_width,
        "X_Var": X * var,
        "X_Cov": X * cov,
        "band_eta": BAND_ETA,
        "n_modes": len(rows),
        "n_band": n_band,
        "band_Ds_frac": band_ds / Ds if Ds else None,
        "wing_Ds_frac": wing_ds / Ds if Ds else None,
        "band_Tc_frac": band_tc / Tc if abs(Tc) > 1e-15 else None,
        "wing_Tc_frac": wing_tc / Tc if abs(Tc) > 1e-15 else None,
        "slope_minus_theta_nu": (slope - THETA * NU) if slope is not None else None,
        "absorbed_at_theta": bool(slope is not None and slope <= THETA * NU),
        "identities_ok": (
            abs(p_sum - 1.0) < 1e-9
            and abs(mean_lam - Lam) < 1e-9
            and abs(X * var - Ds) < 1e-8 * max(1.0, abs(Ds))
            and abs(X * cov - Tc) < 1e-8 * max(1.0, abs(Tc))
            and abs(mean_t - N / X) < 1e-9
        ),
    }


def annular_field(alpha: int, beta: int, eps: float, seed: int = 20260922):
    rng = np.random.default_rng(seed)
    w = core.random_shell_field(alpha, rng, target_E=1.0)
    z, _raw = core.build_closing_direction(w, beta)
    if z is None:
        return None
    sign = core.choose_closing_sign(w, z)
    return core.combine_eps(w, z, sign * eps)


def compact(rec: dict, extra: tuple = ()) -> dict:
    keys = (
        "E",
        "X",
        "Y",
        "Lambda",
        "D_s",
        "T_c",
        "N",
        "mean_t",
        "Var_p_lambda",
        "Cov_p_lambda_t",
        "sigma_lambda",
        "sigma_t",
        "corr",
        "slope",
        "rel_width",
        "band_Ds_frac",
        "wing_Ds_frac",
        "band_Tc_frac",
        "wing_Tc_frac",
        "absorbed_at_theta",
        "identities_ok",
        *extra,
    )
    return {k: rec[k] for k in keys if k in rec}


def run() -> dict:
    note = barycenter(cdt.near_scale_triad())
    note2 = barycenter(cdt.near_scale_triad().scale(2.0))
    sep = barycenter(cdt.separated_triad(8))
    vn = []
    for n in (1, 2, 4, 8):
        rec = barycenter(gl.growing_layer(n))
        vn.append({"n": n, **compact(rec)})
    annular = []
    for eps in (0.2, 0.1, 0.05, 0.025):
        field = annular_field(5, 4, eps)
        if field is None:
            continue
        rec = barycenter(field)
        annular.append(
            {
                "eps": eps,
                "slope": rec["slope"],
                "Var_p_lambda": rec["Var_p_lambda"],
                "rel_width": rec["rel_width"],
                "corr": rec["corr"],
                "sigma_t": rec["sigma_t"],
                "T_c": rec["T_c"],
                "D_s": rec["D_s"],
                "absorbed_at_theta": rec["absorbed_at_theta"],
                "identities_ok": rec["identities_ok"],
            }
        )
    slopes = [r["slope"] for r in vn]
    widths = [r["rel_width"] for r in vn]
    return {
        "ns_solved": False,
        "theta": THETA,
        "nu": NU,
        "band_eta": BAND_ETA,
        "K_formula_proved": None,
        "K_formula": "not written",
        "note_triad": compact(note),
        "note_triad_amp2": {
            "slope": note2["slope"],
            "Var_p_lambda": note2["Var_p_lambda"],
            "rel_width": note2["rel_width"],
            "slope_over_amp1": note2["slope"] / note["slope"] if note["slope"] else None,
            "identities_ok": note2["identities_ok"],
        },
        "separated_L8": compact(sep),
        "growing_layer": vn,
        "near_shell": annular,
        "v_n_slope_decreases": all(slopes[i] < slopes[i - 1] for i in range(1, len(slopes))),
        "v_n_absorbed_at_theta": all(r["absorbed_at_theta"] for r in vn),
        "v_n_rel_width_bounded": max(widths) < 0.4 and min(widths) > 0.2,
        "near_shell_slope_grows": annular[-1]["slope"] > 2.0 * annular[0]["slope"],
        "near_shell_var_shrinks": annular[-1]["Var_p_lambda"] < 0.5 * annular[0]["Var_p_lambda"],
        "all_identities_ok": all(
            [note["identities_ok"], note2["identities_ok"], sep["identities_ok"]]
            + [r["identities_ok"] for r in vn]
            + [r["identities_ok"] for r in annular]
        ),
        "note": (
            "D_s = X Var_p(lambda) and T_c = X Cov_p(lambda, t) are identities. "
            "Slope T_c/D_s is not a shape invariant (doubles under amplitude). "
            "Fat v_n stays absorbed at theta=1/2; barycenter collapse is the face. "
            "NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "centered_spectral_barycenter.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
