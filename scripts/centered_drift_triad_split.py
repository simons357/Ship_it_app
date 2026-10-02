"""Symmetrized real-triad coefficient and channel split of T_c.

Next calculation after the first adversarial triad test.
Not a closure theorem. NS is not solved.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

import ns_lemma_star_core as core
import centered_drift_triad_test as cdt

Mode = Tuple[int, int, int]
SEP_RATIO = 8.0  # eigenvalue max/min; L^2 >= 8 is separated
HH_L_FACTOR = 1.0  # both inputs at least the output eigenvalue


def add(k: Mode, p: Mode) -> Mode:
    return (k[0] + p[0], k[1] + p[1], k[2] + p[2])


def neg(k: Mode) -> Mode:
    return (-k[0], -k[1], -k[2])


def coupling_gamma(p: Mode, q: Mode, A, B, C) -> float:
    """Γ = Im( conj(C) · ((q·A)B + (p·B)A) ). Equals τ_r from the (p,q) pairs."""
    qf = np.array(q, dtype=float)
    pf = np.array(p, dtype=float)
    raw = np.dot(qf, A) * B + np.dot(pf, B) * A
    r = add(p, q)
    raw = core.project_perp(r, raw)
    return float(np.imag(np.dot(np.conj(C), raw)))


def real_triad_field(p: Mode, q: Mode, A, B, C) -> core.Field:
    field = core.Field()
    r = add(p, q)
    field.set_mode(p, A)
    field.set_mode(q, B)
    field.set_mode(r, C)
    return field


def aligned_closer(p: Mode, q: Mode, A, B, phase: float = -math.pi / 2) -> core.Field:
    """C along e^{i phase} P_r((q·A)B+(p·B)A), unit |C|."""
    qf = np.array(q, dtype=float)
    pf = np.array(p, dtype=float)
    r = add(p, q)
    raw = core.project_perp(r, np.dot(qf, A) * B + np.dot(pf, B) * A)
    nrm = float(np.linalg.norm(raw))
    if nrm < 1e-15:
        raise ValueError("vanishing closer")
    C = np.exp(1j * phase) * (raw / nrm)
    return real_triad_field(p, q, A, B, C)


def classify_triangle(lp: float, lq: float, lk: float) -> str:
    """Classify the ordered interaction (p,q) → k=p+q."""
    vals = (lp, lq, lk)
    mx, mn = max(vals), min(vals)
    if lk + 1e-12 < lp and lk + 1e-12 < lq and min(lp, lq) >= HH_L_FACTOR * lk:
        return "hh_to_l"
    if mn > 0 and mx / mn >= SEP_RATIO:
        return "separated"
    return "comparable"


def pair_contributions(field: core.Field) -> List[dict]:
    """Exact ordered-pair split of T_c. Each pair keeps Im, not abs."""
    _, _, _, _, Lambda = core.moments(field)
    keys = list(field.modes.keys())
    rows = []
    Tc = 0.0
    for p in keys:
        vp = field.modes[p]
        for q in keys:
            vq = field.modes[q]
            k = add(p, q)
            if k == (0, 0, 0) or k not in field.modes:
                continue
            vk = field.modes[k]
            qf = np.array(q, dtype=float)
            raw = 1j * np.dot(qf, vp) * vq
            bk = core.project_perp(k, raw)
            I3 = -float(np.real(np.dot(bk, np.conj(vk))))
            ell = core.lam(k)
            piece = ell * (ell - Lambda) * I3
            Tc += piece
            rows.append(
                {
                    "p": p,
                    "q": q,
                    "k": k,
                    "lp": core.lam(p),
                    "lq": core.lam(q),
                    "lk": ell,
                    "I3": I3,
                    "piece": piece,
                    "channel": classify_triangle(core.lam(p), core.lam(q), ell),
                }
            )
    return rows


def split_Tc(field: core.Field) -> dict:
    rec = cdt.record(field)
    rows = pair_contributions(field)
    channels = {"comparable": 0.0, "separated": 0.0, "hh_to_l": 0.0}
    for row in rows:
        channels[row["channel"]] += row["piece"]
    pieces = sum(row["piece"] for row in rows)
    rec.update(
        {
            "T_c_pairs": pieces,
            "T_comparable": channels["comparable"],
            "T_separated": channels["separated"],
            "T_hh_to_l": channels["hh_to_l"],
            "n_pairs": len(rows),
            "split_residual": abs(pieces - rec["T_c"]),
            "R_star": core.R_star(field)["R_star"],
        }
    )
    return rec


def phase_sweep_near_scale(n_phase: int = 24) -> dict:
    p, q = (1, 0, 0), (0, 1, 0)
    A = np.array([0.0, 1.0, 0.0], dtype=complex)
    B = np.array([1.0, 0.0, 1.0], dtype=complex)
    rows = []
    for i in range(n_phase):
        phi = 2 * math.pi * i / n_phase
        field = aligned_closer(p, q, A, B, phase=phi)
        rec = split_Tc(field)
        rec["phase"] = phi
        rec.pop("tau", None)
        rows.append(rec)
    tcs = [r["T_c"] for r in rows]
    ratios = [r["T_c"] / r["D_s"] if r["D_s"] > 0 else float("nan") for r in rows]
    return {
        "n": n_phase,
        "max_Tc": max(tcs),
        "min_Tc": min(tcs),
        "max_Tc_over_Ds": max(ratios),
        "min_Tc_over_Ds": min(ratios),
        "note_phase_Tc": 16 / 5,
        "note_phase_ratio": 4 / 3,
        "rows": rows,
    }


def hh_to_l_triad() -> core.Field:
    """Same-shell HH→L: p=(2,2,1), q=(-2,-2,1), r=(0,0,2), α=9, β=4."""
    p, q = (2, 2, 1), (-2, -2, 1)
    A = core.project_perp(p, np.array([1.0, 0.0, -2.0], dtype=complex))
    B = core.project_perp(q, np.array([0.0, 1.0, 2.0], dtype=complex))
    A = A / np.linalg.norm(A)
    B = B / np.linalg.norm(B)
    return aligned_closer(p, q, A, B, phase=-math.pi / 2)


def comparable_neighbors() -> List[dict]:
    """Nearby lattice closers, still comparable (max/min λ ≤ 4)."""
    A = np.array([0.0, 1.0, 0.0], dtype=complex)
    B = np.array([1.0, 0.0, 1.0], dtype=complex)
    out = []
    for q in ((0, 1, 0), (0, 1, 1), (1, 1, 0), (0, 2, 1)):
        p = (1, 0, 0)
        r = add(p, q)
        if r == (0, 0, 0):
            continue
        lp, lq, lr = core.lam(p), core.lam(q), core.lam(r)
        if max(lp, lq, lr) / min(lp, lq, lr) >= SEP_RATIO:
            continue
        Bq = core.project_perp(q, B)
        if np.linalg.norm(Bq) < 1e-15:
            continue
        Bq = Bq / np.linalg.norm(Bq) * np.linalg.norm(B)
        try:
            field = aligned_closer(p, q, A, Bq, phase=-math.pi / 2)
        except ValueError:
            continue
        rec = split_Tc(field)
        rec["p"] = p
        rec["q"] = q
        rec["r"] = r
        rec["channel_of_r"] = classify_triangle(lp, lq, lr)
        rec.pop("tau", None)
        out.append(rec)
    return out


def annular_two_shell(alpha: int, beta: int, rng: np.random.Generator, eps: float = 0.05) -> dict:
    """Exact-shell α plus aligned closer on β. Near-scale if |α-β| small."""
    w = core.random_shell_field(alpha, rng, target_E=1.0)
    z, raw = core.build_closing_direction(w, beta)
    if z is None:
        return {"alpha": alpha, "beta": beta, "empty_closer": True, "ns_solved": False}
    sign = core.choose_closing_sign(w, z)
    field = core.combine_eps(w, z, sign * eps)
    rec = split_Tc(field)
    rec.update(
        {
            "alpha": alpha,
            "beta": beta,
            "eps": eps,
            "K_alpha_beta": core.K_alpha_beta(w, alpha, beta),
            "empty_closer": False,
        }
    )
    rec.pop("tau", None)
    return rec


def run(seed: int = 20260922) -> dict:
    note = cdt.record(cdt.near_scale_triad())
    note_split = split_Tc(cdt.near_scale_triad())
    sep = split_Tc(cdt.separated_triad(8))
    hh_field = hh_to_l_triad()
    hh = split_Tc(hh_field)
    hh_flip = split_Tc(hh_field.scale(-1))
    sweep = phase_sweep_near_scale(24)
    neighbors = comparable_neighbors()
    rng = np.random.default_rng(seed)
    annular = [
        annular_two_shell(5, 4, rng),
        annular_two_shell(5, 6, rng),
        annular_two_shell(9, 8, rng),
        annular_two_shell(9, 4, rng),
    ]
    near_shell_eps = []
    for eps in (0.2, 0.1, 0.05, 0.025):
        rec = annular_two_shell(5, 4, np.random.default_rng(seed), eps=eps)
        if rec.get("empty_closer"):
            continue
        near_shell_eps.append(
            {
                "eps": eps,
                "T_c": rec["T_c"],
                "D_s": rec["D_s"],
                "X": rec["X"],
                "ratio": rec["T_c"] / rec["D_s"] if rec["D_s"] else None,
                "R_star": rec.get("R_star"),
            }
        )
    p, q = (1, 0, 0), (0, 1, 0)
    A = np.array([0.0, 1.0, 0.0], dtype=complex)
    B = np.array([1.0, 0.0, 1.0], dtype=complex)
    C = np.array([0.0, 0.0, 1.0], dtype=complex) * (-1j)
    gamma = coupling_gamma(p, q, A, B, C)
    return {
        "need_star": "not this page",
        "ns_solved": False,
        "note_Tc": note["T_c"],
        "note_split": {
            "T_c": note_split["T_c"],
            "T_comparable": note_split["T_comparable"],
            "T_separated": note_split["T_separated"],
            "T_hh_to_l": note_split["T_hh_to_l"],
            "split_residual": note_split["split_residual"],
        },
        "gamma_note": gamma,
        "separated_L8": {
            "T_c": sep["T_c"],
            "D_s": sep["D_s"],
            "T_comparable": sep["T_comparable"],
            "T_separated": sep["T_separated"],
            "T_hh_to_l": sep["T_hh_to_l"],
            "ratio": sep["T_c"] / sep["D_s"],
        },
        "hh_to_l": {
            "T_c": hh["T_c"],
            "T_c_flip": hh_flip["T_c"],
            "D_s": hh["D_s"],
            "T_comparable": hh["T_comparable"],
            "T_separated": hh["T_separated"],
            "T_hh_to_l": hh["T_hh_to_l"],
            "ratio": hh["T_c"] / hh["D_s"] if hh["D_s"] else None,
            "ratio_flip": hh_flip["T_c"] / hh_flip["D_s"] if hh_flip["D_s"] else None,
            "Lambda": hh["Lambda"],
        },
        "phase_sweep": {
            "max_Tc": sweep["max_Tc"],
            "min_Tc": sweep["min_Tc"],
            "max_Tc_over_Ds": sweep["max_Tc_over_Ds"],
            "min_Tc_over_Ds": sweep["min_Tc_over_Ds"],
        },
        "comparable_neighbors": [
            {
                "q": rec["q"],
                "T_c": rec["T_c"],
                "D_s": rec["D_s"],
                "ratio": rec["T_c"] / rec["D_s"] if rec["D_s"] else None,
                "T_comparable": rec["T_comparable"],
                "channel_of_r": rec["channel_of_r"],
            }
            for rec in neighbors
        ],
        "annular": [
            {
                "alpha": a.get("alpha"),
                "beta": a.get("beta"),
                "T_c": a.get("T_c"),
                "D_s": a.get("D_s"),
                "ratio": (a["T_c"] / a["D_s"]) if a.get("D_s") else None,
                "R_star": a.get("R_star"),
                "T_comparable": a.get("T_comparable"),
                "T_hh_to_l": a.get("T_hh_to_l"),
                "T_separated": a.get("T_separated"),
                "K_alpha_beta": a.get("K_alpha_beta"),
                "empty_closer": a.get("empty_closer", False),
            }
            for a in annular
        ],
        "near_shell_eps": near_shell_eps,
        "K_formula": "not written; tautological (T_c - theta nu D_s)_+/X is not content",
    }


def main() -> int:
    summary = run()
    out = Path(__file__).resolve().parents[1] / "results" / "centered_drift_triad_split.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
