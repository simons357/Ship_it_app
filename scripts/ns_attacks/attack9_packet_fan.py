#!/usr/bin/env python3
"""Attack 9 — Coherent Packet / Fan Test (Lemma★ kill lane LIVE).

Maximize complete R_★ over conjugate-closed packets P,Q,R with R=P+Q,
increasing packet cardinality m, optimizing amplitudes, phases, and
divergence-free polarizations.

Decisive output: exponent γ in R_★(v_m) ∼ m^γ
  sustained γ>0 → counterexample route
  flat → next analytic target: square-summation / orthogonality

Truth only. NS is NOT solved. Kill lane remains LIVE.
Numerics ≠ proof. Probes subordinate to analysis (not an HPC arms race).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ns_attacks.stokes_moments import (  # noqa: E402
    Field,
    ModeKey,
    Tc_from_B_field,
    Tc_from_triads,
    dilate_field,
    enforce_reality,
    make_divfree_amp,
    nonlinear_B,
    nonlinear_B_fft_dealiased,
    probe,
    scale_field,
    sum_Tk,
)

Packet = List[ModeKey]


def _orthonormal_pol_basis(k: ModeKey) -> Tuple[np.ndarray, np.ndarray]:
    """Two real orthonormal vectors spanning the plane ⊥ k."""
    kk = np.array(k, dtype=np.float64)
    nrm = np.linalg.norm(kk)
    if nrm < 1e-15:
        raise ValueError("k=0")
    # pick a seed not parallel to k
    seed = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(seed, kk)) > 0.9 * nrm:
        seed = np.array([0.0, 1.0, 0.0])
    e1 = seed - (np.dot(seed, kk) / (nrm * nrm)) * kk
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(kk / nrm, e1)
    e2 = e2 / np.linalg.norm(e2)
    return e1, e2


def pol_from_angles(k: ModeKey, theta: float, phi: float) -> np.ndarray:
    """Unit divergence-free polarization: cosθ e1 + sinθ e2, complex phase φ."""
    e1, e2 = _orthonormal_pol_basis(k)
    v = np.cos(theta) * e1 + np.sin(theta) * e2
    return (np.exp(1j * phi) * v).astype(np.complex128)


def build_fan_packets(m: int) -> Tuple[Packet, Packet, Packet]:
    """Conjugate-closed parent packets P,Q and child R=P+Q (as sets of +modes).

    Construction: m distinct high-high → low channels sharing a common low mode
    family, conjugate-closed by enforce_reality later.
    For m=1 this is a single resonant triad.
    """
    P: Packet = []
    Q: Packet = []
    R: Packet = []
    # Base low mode grows slowly with m to keep shells distinct
    for j in range(m):
        # High parents with sum landing on a low shell
        p = (4 + j, 2, 1)
        q = (-3 - j, 1, 1)
        r = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
        assert r == (1, 3, 2)
        P.append(p)
        Q.append(q)
        if r not in R:
            R.append(r)
    # Ensure R has m distinct modes by fanning the low landing
    if m > 1:
        R = []
        P, Q = [], []
        for j in range(m):
            # p + q = r_j with |p|,|q| large, |r| moderate, all distinct
            p = (5 + j, 1, 0)
            q = (-4, 2 + (j % 3), 1)
            r = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            P.append(p)
            Q.append(q)
            R.append(r)
    return P, Q, R


def packet_field(
    P: Packet,
    Q: Packet,
    R: Packet,
    amps_p: Sequence[float],
    amps_q: Sequence[float],
    amps_r: Sequence[float],
    phases_p: Sequence[float],
    phases_q: Sequence[float],
    phases_r: Sequence[float],
    thetas_p: Sequence[float],
    thetas_q: Sequence[float],
    thetas_r: Sequence[float],
) -> Field:
    """Assemble conjugate-closed field on packets P∪Q∪R."""
    field: Field = {}
    for packet, amps, phases, thetas in (
        (P, amps_p, phases_p, thetas_p),
        (Q, amps_q, phases_q, thetas_q),
        (R, amps_r, phases_r, thetas_r),
    ):
        for k, a, ph, th in zip(packet, amps, phases, thetas):
            v = pol_from_angles(k, th, ph)
            # pol_from_angles already includes phase; apply amplitude
            field[k] = a * v
    return enforce_reality(field)


def random_packet_params(m: int, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    return {
        "amps_p": rng.uniform(0.3, 1.5, size=m),
        "amps_q": rng.uniform(0.3, 1.5, size=m),
        "amps_r": rng.uniform(0.3, 1.5, size=m),
        "phases_p": rng.uniform(0, 2 * np.pi, size=m),
        "phases_q": rng.uniform(0, 2 * np.pi, size=m),
        "phases_r": rng.uniform(0, 2 * np.pi, size=m),
        "thetas_p": rng.uniform(0, 2 * np.pi, size=m),
        "thetas_q": rng.uniform(0, 2 * np.pi, size=m),
        "thetas_r": rng.uniform(0, 2 * np.pi, size=m),
    }


def field_from_params(m: int, params: Dict[str, np.ndarray]) -> Field:
    P, Q, R = build_fan_packets(m)
    return packet_field(
        P,
        Q,
        R,
        params["amps_p"],
        params["amps_q"],
        params["amps_r"],
        params["phases_p"],
        params["phases_q"],
        params["phases_r"],
        params["thetas_p"],
        params["thetas_q"],
        params["thetas_r"],
    )


def maximize_R_star_for_m(
    m: int,
    rng: np.random.Generator,
    n_trials: int = 80,
    n_refine: int = 40,
) -> Dict:
    """Random search + local phase/pol refine to max R_★ for packet size m."""
    best = {
        "m": m,
        "R_star": 0.0,
        "Tc": 0.0,
        "Tc_plus": 0.0,
        "Ds": 0.0,
        "E": 0.0,
        "Y": 0.0,
        "params": None,
        "label": f"m={m}",
    }
    for _ in range(n_trials):
        params = random_packet_params(m, rng)
        f = field_from_params(m, params)
        r = probe(f, label=f"m={m}")
        if not math.isfinite(r.ratio_R_star):
            continue
        if r.ratio_R_star > best["R_star"]:
            best.update(
                {
                    "R_star": float(r.ratio_R_star),
                    "Tc": float(r.Tc),
                    "Tc_plus": float(r.Tc_plus),
                    "Ds": float(r.Ds),
                    "E": float(r.E),
                    "Y": float(r.Y),
                    "params": {k: v.copy() for k, v in params.items()},
                }
            )
    # Local refine on phases / thetas of best
    if best["params"] is not None:
        params = {k: v.copy() for k, v in best["params"].items()}
        for _ in range(n_refine):
            trial = {k: v.copy() for k, v in params.items()}
            for key in ("phases_p", "phases_q", "phases_r", "thetas_p", "thetas_q", "thetas_r"):
                trial[key] = trial[key] + rng.normal(0, 0.35, size=m)
            for key in ("amps_p", "amps_q", "amps_r"):
                trial[key] = np.clip(trial[key] * rng.uniform(0.7, 1.3, size=m), 0.05, 5.0)
            f = field_from_params(m, trial)
            r = probe(f, label=f"m={m}-refine")
            if math.isfinite(r.ratio_R_star) and r.ratio_R_star > best["R_star"]:
                best.update(
                    {
                        "R_star": float(r.ratio_R_star),
                        "Tc": float(r.Tc),
                        "Tc_plus": float(r.Tc_plus),
                        "Ds": float(r.Ds),
                        "E": float(r.E),
                        "Y": float(r.Y),
                        "params": {k: v.copy() for k, v in trial.items()},
                    }
                )
                params = trial
    # Drop ndarray params from JSON-ready copy
    out = {k: v for k, v in best.items() if k != "params"}
    out["has_params"] = best["params"] is not None
    if best["params"] is not None:
        out["params"] = {k: v.tolist() for k, v in best["params"].items()}
    return out


def fit_gamma(ms: Sequence[int], R_vals: Sequence[float]) -> Dict:
    """Fit log R_★ = c + γ log m (ordinary least squares)."""
    xs, ys = [], []
    for m, R in zip(ms, R_vals):
        if R is None or not math.isfinite(R) or R <= 0 or m <= 0:
            continue
        xs.append(math.log(m))
        ys.append(math.log(R))
    if len(xs) < 2:
        return {"gamma": None, "intercept": None, "r2": None, "n_points": len(xs)}
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    A = np.vstack([x, np.ones_like(x)]).T
    gamma, c = np.linalg.lstsq(A, y, rcond=None)[0]
    yhat = gamma * x + c
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else None
    return {
        "gamma": float(gamma),
        "intercept": float(c),
        "r2": float(r2) if r2 is not None else None,
        "n_points": len(xs),
        "verdict": (
            "COUNTEREXAMPLE_ROUTE_gamma_gt_0"
            if gamma > 0.05
            else "FLAT_next_analytic_square_summation"
            if abs(gamma) <= 0.05
            else "DECAYING_gamma_lt_0"
        ),
    }


def run_controls(best_by_m: Dict[int, Dict], rng: np.random.Generator) -> Dict:
    """Required Attack 9 controls on a representative optimized field."""
    # Prefer largest m with params
    m_use = max((m for m, row in best_by_m.items() if row.get("params")), default=1)
    params = {k: np.asarray(v, dtype=float) for k, v in best_by_m[m_use]["params"].items()}
    base = field_from_params(m_use, params)
    r0 = probe(base)

    # 1) Amplitude invariance R_★(a v)=R_★(v)
    amp_errs = []
    for a in (0.2, 3.0, 11.0):
        r = probe(scale_field(base, a))
        amp_errs.append(abs(r.ratio_R_star - r0.ratio_R_star))

    # 2) Uniform Fourier dilation R_★(v(n·))=R_★(v)
    dil_errs = []
    for n in (2, 3):
        r = probe(dilate_field(base, n))
        dil_errs.append(abs(r.ratio_R_star - r0.ratio_R_star))

    # 3) Σ T_k = 0
    sTk = sum_Tk(base)

    # 4) Direct triad Tc vs dealiased FFT Tc (complete total Tc, not HH→L only)
    Buu_tri = nonlinear_B(base)
    Buu_fft = nonlinear_B_fft_dealiased(base)
    Tc_tri = Tc_from_triads(base)
    Tc_B = Tc_from_B_field(base, Buu_tri)
    Tc_fft = Tc_from_B_field(base, Buu_fft)
    # Also compare B̂ on occupied modes
    b_errs = []
    for k, vk in base.items():
        bt = Buu_tri.get(k, np.zeros(3, dtype=np.complex128))
        bf = Buu_fft.get(k, np.zeros(3, dtype=np.complex128))
        b_errs.append(float(np.linalg.norm(bt - bf)))

    return {
        "m_control": m_use,
        "R_star_base": float(r0.ratio_R_star),
        "Tc_total_signed": float(r0.Tc),
        "Tc_plus": float(r0.Tc_plus),
        "amp_invariance_max_abs_err": float(max(amp_errs)) if amp_errs else None,
        "dilation_invariance_max_abs_err": float(max(dil_errs)) if dil_errs else None,
        "sum_Tk": float(sTk),
        "sum_Tk_abs": float(abs(sTk)),
        "Tc_triad": float(Tc_tri),
        "Tc_from_B_triad": float(Tc_B),
        "Tc_from_B_fft": float(Tc_fft),
        "Tc_triad_vs_fft_abs_err": float(abs(Tc_tri - Tc_fft)),
        "B_mode_max_abs_err": float(max(b_errs)) if b_errs else None,
        "controls_pass": bool(
            (max(amp_errs) if amp_errs else 1) < 1e-8
            and (max(dil_errs) if dil_errs else 1) < 1e-7
            and abs(sTk) < 1e-8
            and abs(Tc_tri - Tc_fft) < 1e-6 * max(1.0, abs(Tc_tri))
        ),
        "note": (
            "Reports TOTAL Tc (complete signed), not HH→L-only. "
            "R_★ uses (Tc)_+. Amp and uniform Fourier dilation are exact invariants."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--m-min", type=int, default=1)
    ap.add_argument("--m-max", type=int, default=8)
    ap.add_argument("--trials", type=int, default=60)
    ap.add_argument("--refine", type=int, default=30)
    ap.add_argument("--seed", type=int, default=1390)
    ap.add_argument(
        "--outdir",
        type=str,
        default="/opt/cursor/artifacts/attack9_packet_fan",
    )
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    ms = list(range(args.m_min, args.m_max + 1))
    rows = []
    best_by_m: Dict[int, Dict] = {}
    print("Attack 9 — Coherent Packet/Fan Test", flush=True)
    print("Kill lane LIVE. NS not solved.", flush=True)
    for m in ms:
        print(f"  optimizing m={m} ...", flush=True)
        row = maximize_R_star_for_m(m, rng, n_trials=args.trials, n_refine=args.refine)
        rows.append(row)
        best_by_m[m] = row
        print(
            f"    R_star={row['R_star']:.6e}  Tc={row['Tc']:.6e}  "
            f"Tc_+={row['Tc_plus']:.6e}  Ds={row['Ds']:.6e}",
            flush=True,
        )

    R_vals = [row["R_star"] for row in rows]
    gamma_fit = fit_gamma(ms, R_vals)
    controls = run_controls(best_by_m, rng)

    summary = {
        "attack": 9,
        "name": "Coherent Packet/Fan Test",
        "canonical_R_star": "(Tc)_+^2 / (Ds * ||v||_2^2 * Y)",
        "kill_lane": "LIVE",
        "ns_solved": False,
        "lemma_star": "OPEN",
        "m_range": ms,
        "per_m": [{k: v for k, v in row.items() if k != "params"} for row in rows],
        "R_star_by_m": {str(m): best_by_m[m]["R_star"] for m in ms},
        "gamma_fit": gamma_fit,
        "controls": controls,
        "retired_false_claims": [
            "The kill lane is closed — FALSE; numeric non-find ≠ closed",
            "Amplitude or frequency makes the ratio smaller — FALSE for R_★; exact invariance",
        ],
        "numerics_hygiene": (
            "Do not compare legacy 0.065 / 0.073 / 1.93e-3 unless each used exact R_★."
        ),
        "truth": "NS is NOT solved. Falsification and proof both LIVE.",
    }

    (outdir / "attack9.json").write_text(json.dumps(summary, indent=2) + "\n")
    # Human-readable headline
    g = gamma_fit.get("gamma")
    headline = [
        "# Attack 9 — Coherent Packet/Fan — results",
        "",
        f"**Kill lane:** LIVE",
        f"**NS solved:** false",
        f"**Lemma★:** OPEN",
        f"**γ fit:** {g}",
        f"**γ verdict:** {gamma_fit.get('verdict')}",
        f"**controls_pass:** {controls.get('controls_pass')}",
        "",
        "| m | R_★ | Tc (total) | (Tc)_+ |",
        "|---|-----|------------|--------|",
    ]
    for row in rows:
        headline.append(
            f"| {row['m']} | {row['R_star']:.6e} | {row['Tc']:.6e} | {row['Tc_plus']:.6e} |"
        )
    headline.append("")
    headline.append(
        "Decisive: sustained γ>0 → counterexample route; "
        "flat → square-summation / orthogonality next."
    )
    (outdir / "HEADLINE.md").write_text("\n".join(headline) + "\n")

    # Simple log-log plot if matplotlib available
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.loglog(ms, [max(r, 1e-30) for r in R_vals], "o-", label="max R_★(m)")
        if g is not None and gamma_fit.get("intercept") is not None:
            xs = np.array(ms, dtype=float)
            ys = np.exp(gamma_fit["intercept"]) * xs ** g
            ax.loglog(xs, ys, "--", label=f"fit γ={g:.3f}")
        ax.set_xlabel("packet size m")
        ax.set_ylabel(r"$\mathcal{R}_\star$")
        ax.set_title("Attack 9 — coherent packet fan (kill lane LIVE)")
        ax.legend()
        ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(outdir / "R_star_vs_m.png", dpi=140)
        plt.close(fig)
    except Exception as exc:  # pragma: no cover
        (outdir / "plot_error.txt").write_text(str(exc) + "\n")

    print(json.dumps({"gamma_fit": gamma_fit, "controls_pass": controls["controls_pass"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
