#!/usr/bin/env python3
"""Near-shell + HH→L Lemma★ kill search (complete signed Tc; two-shell Ds).

Uses the locked formulas from LEMMA_STAR_SHAPE_FORM.md:
  - two-shell closed form for Ds when the field is bi-shell
  - complete signed Tc (never abs of triad Im)
  - R_★ = Tc^2 / (Ds ||v||_2^2 Y)

HH→L channel fractions diagnose mechanism; kill decision uses complete Tc only.

NS is NOT solved. Numerics ≠ proof.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ns_attacks.stokes_moments import (  # noqa: E402
    Ds_two_shell,
    almost_single_shell_field,
    enforce_reality,
    high_triad_field,
    k_norm2,
    make_divfree_amp,
    moments,
    probe,
    random_field,
    scale_field,
    shell_energies,
    two_shell_field,
)


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def Tc_by_channel(field, k_cut: float) -> dict:
    """Signed N,M,Tc per Bony parent channel (diagnostic only)."""
    from ns_attacks.stokes_moments import leray_project

    keys = list(field.keys())
    B_chan = {"HH": {}, "HL": {}, "LL": {}}

    def add(ch, k, vec):
        B_chan[ch][k] = B_chan[ch].get(k, np.zeros(3, dtype=np.complex128)) + vec

    for p in keys:
        up = field[p]
        pn = np.sqrt(k_norm2(p))
        for q in keys:
            uq = field[q]
            qn = np.sqrt(k_norm2(q))
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            coeff = 1j * np.dot(np.array(q, dtype=np.float64), up)
            contrib = leray_project(k, coeff * uq)
            if pn >= k_cut and qn >= k_cut:
                ch = "HH"
            elif pn >= k_cut or qn >= k_cut:
                ch = "HL"
            else:
                ch = "LL"
            add(ch, k, contrib)

    m = moments(field)
    Lam = m["Lambda"]
    out = {}
    for ch, Bf in B_chan.items():
        N = 0.0 + 0.0j
        M = 0.0 + 0.0j
        for k, bk in Bf.items():
            kn2 = k_norm2(k)
            if kn2 == 0:
                continue
            uk = field.get(k, np.zeros(3, dtype=np.complex128))
            Tk = -np.dot(bk, np.conjugate(uk))
            N += kn2 * Tk
            M += (kn2 * kn2) * Tk
        N = float(N.real)
        M = float(M.real)
        out[ch] = {"N": N, "M": M, "Tc": M - Lam * N}
    out["cut"] = k_cut
    out["Lambda"] = Lam
    # Complete Tc = sum of channel Tcs (signed)
    out["Tc_complete_from_channels"] = (
        out["HH"]["Tc"] + out["HL"]["Tc"] + out["LL"]["Tc"]
    )
    return out


def hh_to_L_two_shell(
    amp_low: float,
    amp_high: float,
    k_low=(1, 0, 0),
    k_high=(8, 3, 2),
    k_high2=(8, -3, 2),
    phase: float = 0.4,
):
    """Low + two high modes so HH parents can hit the low shell."""
    f = two_shell_field(amp_low, amp_high, k_low=k_low, k_high=k_high, phase=phase)
    f2 = dict(f)
    v = make_divfree_amp(k_high2, (0.2, 1.0, -0.3))
    n = np.linalg.norm(v)
    if n > 0:
        f2[k_high2] = (amp_high / n) * v * np.exp(1j * phase)
    return enforce_reality(f2)


def two_shell_Ds_check(field) -> dict:
    """Compare moments Ds vs two-shell closed form when exactly two λ-shells."""
    shells = shell_energies(field)
    m = moments(field)
    out = {
        "n_shells": len(shells),
        "Ds_moments": m["Ds"],
        "Ds_two_shell_closed": None,
        "abs_err": None,
    }
    if len(shells) == 2:
        (a, ea), (b, eb) = list(shells.items())
        closed = Ds_two_shell(a, b, ea, eb)
        out["Ds_two_shell_closed"] = closed
        out["abs_err"] = abs(closed - m["Ds"])
        out["shells"] = {str(a): ea, str(b): eb}
    return out


def run(seed: int = 17, n_almost: int = 200, n_hh: int = 120) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    rows = []
    best = {"abs_R_star": 0.0}
    two_shell_errs = []
    hh_fracs = []
    kill_Ds0_Tc = 0
    vacuous_shell = 0

    def consider(field, tag: str, cut: float | None = None):
        nonlocal best, kill_Ds0_Tc, vacuous_shell
        r = probe(field)
        ds_chk = two_shell_Ds_check(field)
        if ds_chk["abs_err"] is not None:
            two_shell_errs.append(ds_chk["abs_err"])

        ch = None
        if cut is not None:
            ch = Tc_by_channel(field, cut)
            tot = abs(ch["HH"]["Tc"]) + abs(ch["HL"]["Tc"]) + abs(ch["LL"]["Tc"])
            hh_fracs.append(abs(ch["HH"]["Tc"]) / max(tot, 1e-30))
            # Sanity: channel sum ≈ complete Tc (signed)
            assert abs(ch["Tc_complete_from_channels"] - r.Tc) < 1e-6 * max(1.0, abs(r.Tc))

        if r.Ds <= 1e-30:
            if abs(r.Tc) <= 1e-14:
                vacuous_shell += 1
            else:
                kill_Ds0_Tc += 1

        row = {
            "tag": tag,
            "R_star": float(r.ratio_R_star) if np.isfinite(r.ratio_R_star) else None,
            "Tc": float(r.Tc),
            "Ds": float(r.Ds),
            "E": float(r.E),
            "Y": float(r.Y),
            "Lambda": float(r.Lambda),
            "n_shells": ds_chk["n_shells"],
            "Ds_two_shell_err": ds_chk["abs_err"],
            "HH_Tc": None if ch is None else ch["HH"]["Tc"],
            "HL_Tc": None if ch is None else ch["HL"]["Tc"],
            "LL_Tc": None if ch is None else ch["LL"]["Tc"],
            "note": "kill uses complete signed Tc; HH is diagnostic only",
        }
        rows.append(row)
        if row["R_star"] is not None and abs(row["R_star"]) > best["abs_R_star"]:
            best = {
                "abs_R_star": abs(row["R_star"]),
                "R_star": row["R_star"],
                "tag": tag,
                "Tc": row["Tc"],
                "Ds": row["Ds"],
                "HH_Tc": row["HH_Tc"],
            }

    # Near almost-single-shell sweep (live kill attempt)
    for eps in [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]:
        for n_pert in [1, 2, 3, 5]:
            for j in range(max(1, n_almost // 28)):
                f = almost_single_shell_field(rng, n_pert=n_pert, eps=eps)
                consider(f, f"almost_eps={eps}_np={n_pert}_{j}")

    # Exact two-shell Ds closed-form stress + HH→L with second high mode
    for al in [0.1, 1.0, 5.0]:
        for ah in [0.1, 1.0, 10.0, 50.0]:
            f = two_shell_field(al, ah)
            consider(f, f"twoshell_{al}_{ah}")
            f_hh = hh_to_L_two_shell(al, ah)
            kns = [np.sqrt(k_norm2(k)) for k in f_hh]
            cut = 0.5 * (min(kns) + max(kns))
            consider(f_hh, f"hhL_{al}_{ah}", cut=cut)

    # Phase / polarization HH→L barrage
    for i in range(n_hh):
        al = float(rng.uniform(0.05, 2.0))
        ah = float(rng.uniform(0.5, 40.0))
        phase = float(rng.uniform(0, 2 * np.pi))
        f_hh = hh_to_L_two_shell(al, ah, phase=phase)
        # randomize high mode seeds slightly via scale
        if rng.random() < 0.5:
            f_hh = scale_field(f_hh, float(rng.uniform(0.5, 3.0)))
        kns = sorted(np.sqrt(k_norm2(k)) for k in f_hh)
        cut = kns[len(kns) // 2]
        consider(f_hh, f"hhL_rand_{i}", cut=cut)

    # Separated triads (complete Tc)
    for s in [1, 2, 4, 8, 16]:
        f = high_triad_field(amp=1.0, k1=(4 * s, 2 * s, s), k2=(-3 * s, s, s))
        kns = [np.sqrt(k_norm2(k)) for k in f]
        consider(f, f"sep_{s}", cut=0.5 * min(kns))

    # Random broadband control
    for i in range(40):
        f = random_field(rng, kmax=6, n_modes=14, amp=1.0)
        kns = sorted(np.sqrt(k_norm2(k)) for k in f)
        cut = kns[len(kns) // 2] if kns else 2.0
        consider(f, f"rand_{i}", cut=cut)

    R_vals = [abs(r["R_star"]) for r in rows if r["R_star"] is not None]
    killed = bool(kill_Ds0_Tc > 0 or (R_vals and max(R_vals) > 1e3))

    summary = {
        "harness": "lemma_star_near_shell_hhL",
        "canonical_R_star": "Tc^2 / (Ds * ||v||_2^2 * Y); signed complete Tc",
        "n_samples": len(rows),
        "max_R_star": float(max(R_vals)) if R_vals else None,
        "R_star_p95": float(np.percentile(R_vals, 95)) if R_vals else None,
        "best": best,
        "two_shell_Ds_closed_form_max_abs_err": (
            float(max(two_shell_errs)) if two_shell_errs else None
        ),
        "HH_frac_mean": float(np.mean(hh_fracs)) if hh_fracs else None,
        "HH_frac_p90": float(np.percentile(hh_fracs, 90)) if hh_fracs else None,
        "pure_shell_vacuous": vacuous_shell,
        "kill_Ds0_nonzero_Tc": kill_Ds0_Tc,
        "LemmaStar_killed": killed,
        "verdict": "KILL_LemmaStar" if killed else "SURVIVE_numeric_gap_remains",
        "caution": (
            "HH→L fractions identify mechanism only; kill criterion uses complete "
            "signed Tc (no abs on triad Im). Finite max R_★ on this search is NOT "
            "a proof of uniform C_geom."
        ),
        "ns_solved": False,
    }
    summary = _py(summary)
    print("=== NEAR-SHELL + HH→L SEARCH ===", flush=True)
    print(json.dumps({k: v for k, v in summary.items() if k != "best"}, indent=2), flush=True)
    print("best=", json.dumps(summary["best"], indent=2), flush=True)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--n-almost", type=int, default=200)
    ap.add_argument("--n-hh", type=int, default=120)
    args = ap.parse_args()
    summary = run(seed=args.seed, n_almost=args.n_almost, n_hh=args.n_hh)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
