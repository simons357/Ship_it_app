#!/usr/bin/env python3
"""Uniform R_★ attack — Λ-relative HH/HL/LL + maximizer / kill search.

Live target (PRODUCT-BLOCK):
    sup_v R_★(v) < ∞
with a geometry-only constant. Equivalently finite C_geom in
    (T_c)_+^2 ≤ C_geom D_s E Y.

This script:
  1. Splits T_c into Λ-relative HH / HL / LL input channels
     (mode k is H iff λ_k ≥ θ Λ; default θ=1).
  2. Searches maximizers of R_★ over two-shell, near-shell,
     triad-packet, and random-band families (finite samples).
  3. Records whether any sample kills the packaging (R_★→∞ or
     clearly diverging with a control parameter).

Honesty locks (do not soften):
  - Does NOT prove Lemma★ / uniform R_★.
  - Does NOT claim Clay / NS Statement B closed.
  - Does NOT revive |T_c| ≤ C ‖v‖₂ X^{3/2} (algebraically false:
    a³ vs a⁴ under v ↦ a v).
  - Finite max R_★ ≠ supremum; numerics ≠ proof.
  - Probes are subordinate to analysis (not an HPC/supercomputer arms race).
  - Kill lane remains LIVE if no diverging family is found.
  - Policy: docs/ns-review/RESEARCH-POLICY.md
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ns_lemma_star_core import (  # noqa: E402
    Field,
    R_star,
    B_hat_at,
    lam,
    moments,
    project_perp,
    shell_wavevectors,
    T_c_direct,
)


ARTIFACT_DIR = Path("/opt/cursor/artifacts/uniform-rstar-attack")


def _rand_perp(k, rng: np.random.Generator) -> np.ndarray:
    w = rng.normal(size=3) + 1j * rng.normal(size=3)
    return project_perp(k, w)


def _is_high(k, Lambda: float, theta: float) -> bool:
    return lam(k) >= theta * Lambda


def T_c_lambda_channels(field: Field, theta: float = 1.0) -> dict:
    """
    Λ-relative Bony input-channel split of T_c.

    For each triad parent pair (p, q) with p+q=k contributing to B_hat_k,
    classify:
      HH if λ_p ≥ θΛ and λ_q ≥ θΛ
      HL if exactly one of λ_p, λ_q ≥ θΛ
      LL otherwise
    then accumulate the usual centered weight λ_k(λ_k−Λ) T_k^(channel).

    This is an *input-channel* diagnostic (historical “HH→L” label), not a
    proved high→low output map.
    """
    E, X, Y, Z, Lambda = moments(field)
    if X <= 0:
        raise ValueError("empty / zero field")

    B_chan = {"HH": {}, "HL": {}, "LL": {}}

    def add(ch: str, k: tuple, vec: np.ndarray) -> None:
        B_chan[ch][k] = B_chan[ch].get(k, np.zeros(3, dtype=complex)) + vec

    keys = list(field.modes.keys())
    for p in keys:
        vp = field.modes[p]
        lp = lam(p)
        p_hi = lp >= theta * Lambda
        for q in keys:
            vq = field.modes[q]
            lq = lam(q)
            q_hi = lq >= theta * Lambda
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            qf = np.array(q, dtype=float)
            coeff = 1j * np.dot(qf, vp)
            contrib = project_perp(k, coeff * vq)
            if p_hi and q_hi:
                ch = "HH"
            elif p_hi or q_hi:
                ch = "HL"
            else:
                ch = "LL"
            add(ch, k, contrib)

    out = {}
    for ch, Bf in B_chan.items():
        Tc = 0.0
        for k, bk in Bf.items():
            vk = field.modes.get(k)
            if vk is None:
                continue
            Tk = -float(np.real(np.dot(bk, np.conj(vk))))
            lk = lam(k)
            Tc += lk * (lk - Lambda) * Tk
        out[ch] = Tc

    Tc_full = T_c_direct(field, Lambda)
    Tc_sum = out["HH"] + out["HL"] + out["LL"]
    abs_tot = abs(out["HH"]) + abs(out["HL"]) + abs(out["LL"])
    return {
        "theta": theta,
        "Lambda": Lambda,
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "T_c_full": Tc_full,
        "T_c_HH": out["HH"],
        "T_c_HL": out["HL"],
        "T_c_LL": out["LL"],
        "T_c_channel_sum": Tc_sum,
        "channel_sum_err": abs(Tc_sum - Tc_full),
        "HH_frac_abs": abs(out["HH"]) / max(abs_tot, 1e-300),
        "HL_frac_abs": abs(out["HL"]) / max(abs_tot, 1e-300),
        "LL_frac_abs": abs(out["LL"]) / max(abs_tot, 1e-300),
    }


def two_shell_field(
    n1: int,
    n2: int,
    rng: np.random.Generator,
    amp2: float = 1.0,
    per_shell: int = 4,
    phases: np.ndarray | None = None,
) -> Field:
    f = Field()
    phase_i = 0
    for n, amp in ((n1, 1.0), (n2, amp2)):
        ks = shell_wavevectors(n, canonical_only=True)
        if not ks:
            raise ValueError(f"empty shell n={n}")
        pick = list(ks)
        rng.shuffle(pick)
        for k in pick[: max(1, min(per_shell, len(pick)))]:
            w = amp * _rand_perp(k, rng)
            if phases is not None and phase_i < len(phases):
                w = w * np.exp(1j * float(phases[phase_i]))
                phase_i += 1
            f.set_mode(k, w)
    return f.normalize(1.0)


def near_shell_field(
    n: int,
    eps_shell: int,
    eps_amp: float,
    rng: np.random.Generator,
    per_main: int = 6,
    per_eps: int = 2,
) -> Field:
    """Main shell n plus small energy on a nearby shell (near-shell packet)."""
    f = Field()
    for shell, amp, n_pick in (
        (n, 1.0, per_main),
        (eps_shell, eps_amp, per_eps),
    ):
        ks = shell_wavevectors(shell, canonical_only=True)
        if not ks:
            raise ValueError(f"empty shell n={shell}")
        pick = list(ks)
        rng.shuffle(pick)
        for k in pick[: max(1, min(n_pick, len(pick)))]:
            f.set_mode(k, amp * _rand_perp(k, rng))
    return f.normalize(1.0)


def triad_packet_field(
    p: tuple,
    q: tuple,
    rng: np.random.Generator,
    amp_r: float = 1.0,
) -> Field:
    """
    Conjugate-closed triad packet on {±p, ±q, ±r} with r = p+q
    (when r ≠ 0 and lattice). Classic stretching probe.
    """
    r = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
    if r == (0, 0, 0):
        raise ValueError("degenerate triad")
    f = Field()
    for k, amp in ((p, 1.0), (q, 1.0), (r, amp_r)):
        f.set_mode(k, amp * _rand_perp(k, rng))
    return f.normalize(1.0)


def random_band_field(kmax: int, rng: np.random.Generator, n_modes: int = 8) -> Field:
    f = Field()
    chosen: set[tuple] = set()
    guard = 0
    while len(chosen) < n_modes and guard < 8000:
        guard += 1
        k = tuple(int(x) for x in rng.integers(-kmax, kmax + 1, size=3))
        if k == (0, 0, 0) or k in chosen or tuple(-x for x in k) in chosen:
            continue
        if k[0] * k[0] + k[1] * k[1] + k[2] * k[2] > kmax * kmax:
            continue
        chosen.add(k)
        f.set_mode(k, _rand_perp(k, rng))
    if len(chosen) < 3:
        raise ValueError("band too thin")
    return f.normalize(1.0)


def measure(field: Field, family: str, theta: float = 1.0) -> dict:
    rec = R_star(field, verify=True)
    ch = T_c_lambda_channels(field, theta=theta)
    rs = rec["R_star"]
    row = {
        "family": family,
        "E": float(rec["E"]),
        "X": float(rec["X"]),
        "Y": float(rec["Y"]),
        "Z": float(rec["Z"]),
        "Lambda": float(rec["Lambda"]),
        "D_s": float(rec["D_s"]),
        "T_c": float(rec["T_c"]),
        "R_star": None if rs == float("inf") else float(rs),
        "R_star_inf": bool(rs == float("inf")),
        "vacuous": bool(rec.get("vacuous_single_shell")),
        "T_c_HH": ch["T_c_HH"],
        "T_c_HL": ch["T_c_HL"],
        "T_c_LL": ch["T_c_LL"],
        "HH_frac_abs": ch["HH_frac_abs"],
        "HL_frac_abs": ch["HL_frac_abs"],
        "LL_frac_abs": ch["LL_frac_abs"],
        "channel_sum_err": ch["channel_sum_err"],
        "theta": theta,
    }
    return row


def maximize_two_shell(
    n1: int,
    n2: int,
    rng: np.random.Generator,
    n_trials: int = 40,
    amp2: float = 1.0,
    theta: float = 1.0,
) -> dict:
    best = None
    for t in range(n_trials):
        f = two_shell_field(n1, n2, rng, amp2=amp2, per_shell=4)
        # local phase jitter refine
        row = measure(f, f"two_shell_{n1}_{n2}_a{amp2}_t{t}", theta=theta)
        if row["vacuous"] or row["R_star"] is None:
            continue
        if best is None or row["R_star"] > best["R_star"]:
            best = row
    if best is None:
        return {
            "family": f"two_shell_{n1}_{n2}_a{amp2}",
            "error": "no_nonvacuous_sample",
        }
    best["family"] = f"two_shell_max_{n1}_{n2}_a{amp2}"
    return best


def maximize_near_shell(
    n: int,
    eps_shell: int,
    rng: np.random.Generator,
    n_trials: int = 30,
    theta: float = 1.0,
) -> dict:
    best = None
    for t, eps_amp in enumerate(
        list(rng.uniform(0.02, 0.4, size=n_trials))
    ):
        f = near_shell_field(n, eps_shell, float(eps_amp), rng)
        row = measure(
            f, f"near_shell_{n}_{eps_shell}_eps{eps_amp:.3f}_t{t}", theta=theta
        )
        if row["vacuous"] or row["R_star"] is None:
            continue
        if best is None or row["R_star"] > best["R_star"]:
            best = row
            best["eps_amp"] = float(eps_amp)
    if best is None:
        return {"family": f"near_shell_{n}_{eps_shell}", "error": "empty"}
    best["family"] = f"near_shell_max_{n}_{eps_shell}"
    return best


def maximize_triad(
    rng: np.random.Generator,
    n_trials: int = 50,
    theta: float = 1.0,
) -> dict:
    # Fixed classical stretching triad + random nearby lattice triads
    seeds = [
        ((1, 0, 0), (2, 1, 0)),
        ((1, 1, 0), (2, -1, 0)),
        ((3, 1, 0), (-1, 2, 0)),
        ((2, 2, 1), (1, -2, 1)),
        ((4, 1, 0), (-2, 3, 0)),
    ]
    best = None
    for t in range(n_trials):
        if t < len(seeds):
            p, q = seeds[t]
        else:
            p = tuple(int(x) for x in rng.integers(-4, 5, size=3))
            q = tuple(int(x) for x in rng.integers(-4, 5, size=3))
            if p == (0, 0, 0) or q == (0, 0, 0):
                continue
        r = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
        if r == (0, 0, 0):
            continue
        try:
            f = triad_packet_field(p, q, rng, amp_r=float(rng.uniform(0.3, 2.0)))
            row = measure(f, f"triad_{p}_{q}_t{t}", theta=theta)
        except Exception as e:  # noqa: BLE001
            continue
        if row["vacuous"] or row["R_star"] is None:
            continue
        if best is None or row["R_star"] > best["R_star"]:
            best = row
            best["p"] = list(p)
            best["q"] = list(q)
            best["r"] = list(r)
    if best is None:
        return {"family": "triad_packet", "error": "empty"}
    best["family"] = "triad_packet_max"
    return best


def amplitude_scaling_false_product_check(rng: np.random.Generator) -> dict:
    """
    Document (again) that |T_c| / (‖v‖₂ X^{3/2}) is NOT scale-invariant:
    under v ↦ a v, numerator ~ a³, denominator ~ a⁴, so ratio → 0 as a→∞
    and → ∞ as a→0 — cannot be a universal product bound.
    R_★ is amplitude-invariant (should stay flat).
    """
    f0 = two_shell_field(1, 5, rng, amp2=1.0, per_shell=3)
    rows = []
    for a in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        f = f0.scale(a)
        rec = R_star(f, verify=True)
        E, X = float(rec["E"]), float(rec["X"])
        Tc = float(rec["T_c"])
        v2 = math.sqrt(max(E, 0.0))
        prod = v2 * (X ** 1.5) if X > 0 else float("nan")
        rows.append(
            {
                "a": a,
                "T_c": Tc,
                "R_star": None
                if rec["R_star"] == float("inf")
                else float(rec["R_star"]),
                "abs_Tc_over_v2_X32": (abs(Tc) / prod) if prod > 0 else None,
            }
        )
    # R_star should be ~constant; false product ratio should track 1/a
    rs = [r["R_star"] for r in rows if r["R_star"] is not None]
    prods = [r["abs_Tc_over_v2_X32"] for r in rows if r["abs_Tc_over_v2_X32"]]
    return {
        "rows": rows,
        "R_star_relative_spread": (
            (max(rs) - min(rs)) / max(max(rs), 1e-300) if rs else None
        ),
        "false_product_ratio_max_over_min": (
            max(prods) / max(min(prods), 1e-300) if prods else None
        ),
        "note": (
            "R_★ amplitude-invariant; |T_c|/(‖v‖₂ X^{3/2}) collapses under "
            "a↦ large a (a³/a⁴). False universal product discarded."
        ),
    }


def run(seed: int = 20260912, theta: float = 1.0, quick: bool = False) -> dict:
    rng = np.random.default_rng(seed)
    rows: list[dict] = []

    n_two = 8 if quick else 24
    n_near = 10 if quick else 20
    n_triad = 20 if quick else 40
    n_band = 8 if quick else 16

    # --- two-shell maximizers ---
    for n1, n2, amp2 in [
        (1, 2, 1.0),
        (1, 5, 1.0),
        (2, 8, 0.5),
        (3, 6, 1.0),
        (1, 17, 0.25),
        (5, 10, 1.0),
        (5, 13, 1.0),
        (2, 10, 1.0),
    ]:
        try:
            rows.append(
                maximize_two_shell(
                    n1, n2, rng, n_trials=n_two, amp2=amp2, theta=theta
                )
            )
        except Exception as e:  # noqa: BLE001
            rows.append({"family": f"two_shell_{n1}_{n2}", "error": str(e)})

    # --- near-shell ---
    for n, eps in [(1, 2), (2, 3), (5, 6), (5, 8), (9, 10), (10, 13)]:
        try:
            rows.append(
                maximize_near_shell(n, eps, rng, n_trials=n_near, theta=theta)
            )
        except Exception as e:  # noqa: BLE001
            rows.append({"family": f"near_shell_{n}_{eps}", "error": str(e)})

    # --- triad packets ---
    rows.append(maximize_triad(rng, n_trials=n_triad, theta=theta))

    # --- random bands ---
    for i, kmax in enumerate([2, 3, 4, 5, 6]):
        for j in range(n_band // 5 + 1):
            try:
                f = random_band_field(kmax, rng, n_modes=6 + i)
                rows.append(
                    measure(f, f"random_band_kmax{kmax}_j{j}", theta=theta)
                )
            except Exception as e:  # noqa: BLE001
                rows.append(
                    {"family": f"random_band_kmax{kmax}_j{j}", "error": str(e)}
                )

    # --- HH-heavy construction: many high modes, tiny low ---
    for ah in (1.0, 5.0, 20.0):
        try:
            f = two_shell_field(1, 17, rng, amp2=ah, per_shell=5)
            rows.append(measure(f, f"hh_heavy_1_17_ah{ah}", theta=theta))
        except Exception as e:  # noqa: BLE001
            rows.append({"family": f"hh_heavy_ah{ah}", "error": str(e)})

    false_prod = amplitude_scaling_false_product_check(rng)

    finite = [
        r
        for r in rows
        if r.get("R_star") is not None and not r.get("R_star_inf")
    ]
    max_rs = max((r["R_star"] for r in finite), default=None)
    best = (
        max(finite, key=lambda r: r["R_star"]) if finite else None
    )
    hh_fracs = [r["HH_frac_abs"] for r in finite if "HH_frac_abs" in r]
    chan_errs = [
        r["channel_sum_err"] for r in finite if "channel_sum_err" in r
    ]

    # Kill heuristic: R_★ exploding with a control parameter on HH-heavy
    # amp series, or any R_star_inf with D_s>0 (should not happen).
    kill_found = False
    kill_notes = []
    hh_series = [
        r for r in rows if str(r.get("family", "")).startswith("hh_heavy")
    ]
    if len(hh_series) >= 2:
        rs_vals = [r["R_star"] for r in hh_series if r.get("R_star") is not None]
        if rs_vals and max(rs_vals) > 100 * max(min(rs_vals), 1e-12):
            kill_found = True
            kill_notes.append(
                "HH-heavy amp series shows >100× R_★ growth (investigate)"
            )
    for r in rows:
        if r.get("R_star_inf") and not r.get("vacuous"):
            kill_found = True
            kill_notes.append(f"non-vacuous R_star=inf at {r.get('family')}")

    summary = {
        "attack": "uniform_rstar_lambda_channels",
        "theta_Lambda_cut": theta,
        "seed": seed,
        "n_rows": len(rows),
        "n_finite_R_star": len(finite),
        "max_R_star": max_rs,
        "best_family": None if best is None else best.get("family"),
        "best_row": best,
        "mean_HH_frac_abs": float(np.mean(hh_fracs)) if hh_fracs else None,
        "p90_HH_frac_abs": float(np.percentile(hh_fracs, 90)) if hh_fracs else None,
        "max_channel_sum_err": float(max(chan_errs)) if chan_errs else None,
        "kill_found": kill_found,
        "kill_notes": kill_notes,
        "false_product_check": false_prod,
        "status": {
            "PRODUCT_BLOCK": "OPEN",
            "uniform_R_star": "OPEN",
            "Lemma_star_DA_NS_1": "HYPOTHESIS",
            "Clay_Statement_B": "NOT_SOLVED",
            "kill_lane": "LIVE" if not kill_found else "TRIGGERED_INVESTIGATE",
            "numerics_are_proof": False,
            "false_X32_universal": "DISCARDED",
        },
        "analytic_reduction_pointer": (
            "docs/ns-review/UNIFORM-RSTAR-ATTACK.md — if HH controlled "
            "and HL/LL classical, uniform R_★ closes; HH still open."
        ),
        "note": (
            "Finite-sample ceilings only. max R_★ here does not prove "
            "sup R_★ < ∞. Absence of kill ≠ theorem."
        ),
    }

    return {"summary": summary, "rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=20260912)
    ap.add_argument("--theta", type=float, default=1.0, help="H iff λ_k ≥ θ Λ")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument(
        "--out-dir",
        type=str,
        default=str(ARTIFACT_DIR),
    )
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = run(seed=args.seed, theta=args.theta, quick=args.quick)
    summary = payload["summary"]

    out_json = out_dir / "uniform_rstar_attack.json"
    out_json.write_text(json.dumps(payload, indent=2, default=str))

    lines = [
        "uniform_rstar_attack — Λ-relative HH/HL/LL + maximizer search",
        summary["note"],
        f"status: PRODUCT-BLOCK={summary['status']['PRODUCT_BLOCK']}  "
        f"kill_lane={summary['status']['kill_lane']}  "
        f"Clay={summary['status']['Clay_Statement_B']}",
        f"max_R_star={summary['max_R_star']!r}  "
        f"best={summary['best_family']!r}",
        f"mean_HH_frac={summary['mean_HH_frac_abs']!r}  "
        f"p90_HH_frac={summary['p90_HH_frac_abs']!r}",
        f"max_channel_sum_err={summary['max_channel_sum_err']!r}",
        f"kill_found={summary['kill_found']}  notes={summary['kill_notes']}",
        "",
        "top finite R_star samples:",
    ]
    finite = sorted(
        [
            r
            for r in payload["rows"]
            if r.get("R_star") is not None and not r.get("R_star_inf")
        ],
        key=lambda r: r["R_star"],
        reverse=True,
    )
    for r in finite[:15]:
        lines.append(
            f"  R*={r['R_star']:.6e}  HH%={r.get('HH_frac_abs', float('nan')):.3f}  "
            f"Tc={r['T_c']:.4e}  {r['family']}"
        )

    fp = summary["false_product_check"]
    lines.append("")
    lines.append("false-product amplitude check:")
    lines.append(f"  {fp['note']}")
    lines.append(
        f"  R_star_rel_spread={fp['R_star_relative_spread']!r}  "
        f"false_prod_max/min={fp['false_product_ratio_max_over_min']!r}"
    )
    for r in fp["rows"]:
        lines.append(
            f"  a={r['a']}: R*={r['R_star']}  "
            f"|Tc|/(v2 X^3/2)={r['abs_Tc_over_v2_X32']}"
        )

    out_txt = out_dir / "uniform_rstar_attack.txt"
    text = "\n".join(lines) + "\n"
    out_txt.write_text(text)
    print(text)
    print(f"wrote {out_json}")
    print(f"wrote {out_txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
