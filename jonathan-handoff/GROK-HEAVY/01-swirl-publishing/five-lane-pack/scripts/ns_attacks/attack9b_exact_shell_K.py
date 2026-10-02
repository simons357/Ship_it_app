#!/usr/bin/env python3
"""Attack 9B — Exact-shell coherent fan + small closing packet (Lemma★).

Family:
  v_ε = w_α + ε z_β,  A w_α = α w_α,  A z_β = β z_β,
  z_β ∥ Π_β B(w_α, w_α).

Boxed quantity:
  K_{α,β} = sup_{A w = α w}  β ‖Π_β B(w,w)‖₂² / (α² ‖w‖₂⁴)

ε→0: R_★(v_ε) → K_{α,β}(w) for optimally aligned unit closing packet.
ε cancels in the limiting quotient; Ds is generated only by the closing component.

Attack 9A (AP packet) did NOT kill ★: Ds grew faster than Tc.
Truth only. NS is NOT solved. Kill lane remains LIVE.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ns_attacks.stokes_moments import (  # noqa: E402
    Field,
    ModeKey,
    Ds_two_shell,
    enforce_reality,
    k_norm2,
    leray_project,
    moments,
    nonlinear_B,
    probe,
    scale_field,
    shell_energies,
    sum_Tk,
)

ShellModes = List[ModeKey]


def _orthonormal_pol_basis(k: ModeKey) -> Tuple[np.ndarray, np.ndarray]:
    kk = np.array(k, dtype=np.float64)
    nrm = np.linalg.norm(kk)
    if nrm < 1e-15:
        raise ValueError("k=0")
    seed = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(seed, kk)) > 0.9 * nrm:
        seed = np.array([0.0, 1.0, 0.0])
    e1 = seed - (np.dot(seed, kk) / (nrm * nrm)) * kk
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(kk / nrm, e1)
    e2 = e2 / np.linalg.norm(e2)
    return e1, e2


def pol_from_angles(k: ModeKey, theta: float, phi: float) -> np.ndarray:
    e1, e2 = _orthonormal_pol_basis(k)
    v = np.cos(theta) * e1 + np.sin(theta) * e2
    return (np.exp(1j * phi) * v).astype(np.complex128)


def positive_half_modes(kmax: int) -> List[ModeKey]:
    out: List[ModeKey] = []
    for i in range(-kmax, kmax + 1):
        for j in range(-kmax, kmax + 1):
            for k in range(-kmax, kmax + 1):
                if (i, j, k) == (0, 0, 0):
                    continue
                if i > 0 or (i == 0 and j > 0) or (i == 0 and j == 0 and k > 0):
                    out.append((i, j, k))
    return out


def shells_up_to(kmax: int) -> Dict[int, ShellModes]:
    """Map α = |k|² → list of positive-half wavevectors on that shell."""
    buckets: Dict[int, ShellModes] = defaultdict(list)
    for k in positive_half_modes(kmax):
        buckets[int(k_norm2(k))].append(k)
    return dict(buckets)


def build_exact_shell_field(
    modes: Sequence[ModeKey],
    amps: Sequence[float],
    thetas: Sequence[float],
    phis: Sequence[float],
) -> Field:
    """Exact Stokes eigenfield on one shell (conjugate-closed)."""
    field: Field = {}
    for k, a, th, ph in zip(modes, amps, thetas, phis):
        if a <= 0:
            continue
        field[k] = a * pol_from_angles(k, th, ph)
    return enforce_reality(field)


def field_l2(field: Field) -> float:
    return math.sqrt(max(sum(float(np.vdot(v, v).real) for v in field.values()), 0.0))


def normalize_field(field: Field) -> Field:
    n = field_l2(field)
    if n < 1e-30:
        raise ValueError("zero field")
    return {k: v / n for k, v in field.items()}


def project_B_to_shell(Buu: Field, beta: float, tol: float = 1e-9) -> Field:
    """Π_β B: keep only modes with |k|² = β (conjugate-closed)."""
    out: Field = {}
    for k, v in Buu.items():
        if abs(k_norm2(k) - beta) <= tol:
            out[k] = leray_project(k, np.asarray(v, dtype=np.complex128))
    return enforce_reality(out)


def shell_field_norm2(field: Field) -> float:
    return sum(float(np.vdot(v, v).real) for v in field.values())


def K_of_w(w: Field, alpha: float, beta: float) -> Dict[str, float]:
    """K_{α,β}(w) = β ‖Π_β B(w,w)‖₂² / (α² ‖w‖₂⁴)."""
    w = enforce_reality(w)
    e = field_l2(w) ** 2
    Buu = nonlinear_B(w)
    PiB = project_B_to_shell(Buu, beta)
    pi_norm2 = shell_field_norm2(PiB)
    denom = (alpha ** 2) * (e ** 2)
    K = (beta * pi_norm2 / denom) if denom > 0 else float("nan")
    return {
        "K": float(K),
        "PiB_L2": float(math.sqrt(max(pi_norm2, 0.0))),
        "PiB_L2_sq": float(pi_norm2),
        "E_w": float(e),
        "alpha": float(alpha),
        "beta": float(beta),
    }


def closing_packet_from_PiB(PiB: Field, sign: float = 1.0) -> Field:
    """Unit z_β ∥ Π_β B (sign chooses stretch orientation)."""
    n2 = shell_field_norm2(PiB)
    if n2 < 1e-30:
        return {}
    n = math.sqrt(n2)
    return {k: (sign * v / n) for k, v in PiB.items()}


def combine_eps(w: Field, z: Field, eps: float) -> Field:
    out: Field = {k: v.copy() for k, v in w.items()}
    for k, zv in z.items():
        out[k] = out.get(k, np.zeros(3, dtype=np.complex128)) + eps * zv
    return enforce_reality(out)


def choose_closing_sign(w: Field, PiB: Field, eps: float = 1e-3) -> float:
    """Pick ± so that Tc(v_ε)_+ is larger (stretching)."""
    best_sign = 1.0
    best_tc = -float("inf")
    for s in (1.0, -1.0):
        z = closing_packet_from_PiB(PiB, sign=s)
        if not z:
            return 1.0
        r = probe(combine_eps(w, z, eps))
        if r.Tc > best_tc:
            best_tc = r.Tc
            best_sign = s
    return best_sign


def random_shell_params(n_modes: int, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    return {
        "amps": rng.uniform(0.2, 1.5, size=n_modes),
        "thetas": rng.uniform(0, 2 * np.pi, size=n_modes),
        "phis": rng.uniform(0, 2 * np.pi, size=n_modes),
    }


def field_from_shell_params(modes: Sequence[ModeKey], params: Dict[str, np.ndarray]) -> Field:
    return build_exact_shell_field(modes, params["amps"], params["thetas"], params["phis"])


def optimize_K_on_shell(
    alpha: int,
    beta: int,
    modes: Sequence[ModeKey],
    rng: np.random.Generator,
    n_trials: int = 80,
    n_refine: int = 40,
    max_modes: Optional[int] = None,
) -> Dict:
    """Random search + local refine of phases/pols/amps on exact shell α."""
    use_modes = list(modes)
    if max_modes is not None and len(use_modes) > max_modes:
        # Keep a coherent fan subset (deterministic by mode order + rng shuffle)
        idx = np.arange(len(use_modes))
        rng.shuffle(idx)
        use_modes = [use_modes[i] for i in sorted(idx[:max_modes])]
    n = len(use_modes)
    best = {
        "alpha": alpha,
        "beta": beta,
        "n_modes_pos": n,
        "K": 0.0,
        "PiB_L2": 0.0,
        "params": None,
        "Ds_eps0": None,
    }
    if n == 0:
        return best

    for _ in range(n_trials):
        params = random_shell_params(n, rng)
        w = normalize_field(field_from_shell_params(use_modes, params))
        # Exact-shell control
        m0 = moments(w)
        info = K_of_w(w, float(alpha), float(beta))
        if not math.isfinite(info["K"]):
            continue
        if info["K"] > best["K"]:
            best.update(
                {
                    "K": info["K"],
                    "PiB_L2": info["PiB_L2"],
                    "params": {k: v.copy() for k, v in params.items()},
                    "Ds_eps0": float(m0["Ds"]),
                    "modes": [list(k) for k in use_modes],
                }
            )

    if best["params"] is not None:
        params = {k: v.copy() for k, v in best["params"].items()}
        for _ in range(n_refine):
            trial = {k: v.copy() for k, v in params.items()}
            trial["thetas"] = trial["thetas"] + rng.normal(0, 0.4, size=n)
            trial["phis"] = trial["phis"] + rng.normal(0, 0.4, size=n)
            trial["amps"] = np.clip(trial["amps"] * rng.uniform(0.7, 1.35, size=n), 0.05, 5.0)
            w = normalize_field(field_from_shell_params(use_modes, trial))
            info = K_of_w(w, float(alpha), float(beta))
            if math.isfinite(info["K"]) and info["K"] > best["K"]:
                best.update(
                    {
                        "K": info["K"],
                        "PiB_L2": info["PiB_L2"],
                        "params": {k: v.copy() for k, v in trial.items()},
                        "Ds_eps0": float(moments(w)["Ds"]),
                    }
                )
                params = trial

    out = {k: v for k, v in best.items() if k != "params"}
    out["has_params"] = best["params"] is not None
    if best["params"] is not None:
        out["params"] = {k: v.tolist() for k, v in best["params"].items()}
    return out


def eps_limit_check(
    w: Field,
    alpha: float,
    beta: float,
    eps_list: Sequence[float],
) -> Dict:
    """Verify R_★(w+εz) → K(w) as ε→0."""
    info = K_of_w(w, alpha, beta)
    K = info["K"]
    Buu = nonlinear_B(w)
    PiB = project_B_to_shell(Buu, beta)
    if info["PiB_L2"] < 1e-14:
        return {
            "K": K,
            "PiB_L2": info["PiB_L2"],
            "rows": [],
            "limit_ok": True,
            "note": "Π_β B ≈ 0; K≈0; trivial limit",
        }
    sign = choose_closing_sign(w, PiB)
    z = closing_packet_from_PiB(PiB, sign=sign)
    rows = []
    for eps in eps_list:
        v = combine_eps(w, z, eps)
        r = probe(v, label=f"eps={eps}")
        shells = shell_energies(v)
        # two-shell Ds check when exactly two shells
        ds_closed = None
        if len(shells) == 2:
            (a, ea), (b, eb) = list(shells.items())
            ds_closed = Ds_two_shell(a, b, ea, eb)
        rel = abs(r.ratio_R_star - K) / max(K, 1e-30) if math.isfinite(r.ratio_R_star) else None
        rows.append(
            {
                "eps": float(eps),
                "R_star": float(r.ratio_R_star) if math.isfinite(r.ratio_R_star) else None,
                "Tc": float(r.Tc),
                "Tc_plus": float(r.Tc_plus),
                "Ds": float(r.Ds),
                "Ds_two_shell": float(ds_closed) if ds_closed is not None else None,
                "E": float(r.E),
                "Y": float(r.Y),
                "rel_err_to_K": float(rel) if rel is not None else None,
                "n_shells": len(shells),
            }
        )
    # Limit OK if smallest eps has small relative error (or K~0)
    finite_rows = [row for row in rows if row["rel_err_to_K"] is not None]
    if not finite_rows:
        limit_ok = K < 1e-12
    else:
        # prefer smallest eps
        finite_rows.sort(key=lambda row: row["eps"])
        limit_ok = bool(finite_rows[0]["rel_err_to_K"] < 0.15 or K < 1e-10)
    return {
        "K": float(K),
        "PiB_L2": float(info["PiB_L2"]),
        "closing_sign": float(sign),
        "rows": rows,
        "limit_ok": limit_ok,
        "rel_err_at_smallest_eps": finite_rows[0]["rel_err_to_K"] if finite_rows else None,
    }


def run_controls(w: Field, alpha: float, beta: float) -> Dict:
    """Amplitude invariance of K and R_★; exact-shell Ds≈0 at ε=0."""
    w = normalize_field(enforce_reality(w))
    m0 = moments(w)
    k0 = K_of_w(w, alpha, beta)["K"]
    amp_K_errs = []
    amp_R_errs = []
    Buu = nonlinear_B(w)
    PiB = project_B_to_shell(Buu, beta)
    sign = choose_closing_sign(w, PiB) if shell_field_norm2(PiB) > 0 else 1.0
    z = closing_packet_from_PiB(PiB, sign=sign) if shell_field_norm2(PiB) > 0 else {}
    eps = 1e-3
    base_v = combine_eps(w, z, eps) if z else w
    r0 = probe(base_v)
    for a in (0.2, 3.0, 11.0):
        wa = scale_field(w, a)
        amp_K_errs.append(abs(K_of_w(wa, alpha, beta)["K"] - k0))
        if z:
            ra = probe(scale_field(base_v, a))
            amp_R_errs.append(abs(ra.ratio_R_star - r0.ratio_R_star))
    sTk = sum_Tk(w)
    return {
        "Ds_eps0": float(m0["Ds"]),
        "Ds_eps0_ok": bool(abs(m0["Ds"]) < 1e-10),
        "K_base": float(k0),
        "amp_K_max_abs_err": float(max(amp_K_errs)) if amp_K_errs else None,
        "amp_R_star_max_abs_err": float(max(amp_R_errs)) if amp_R_errs else None,
        "sum_Tk_exact_shell": float(sTk),
        "controls_pass": bool(
            abs(m0["Ds"]) < 1e-10
            and (max(amp_K_errs) if amp_K_errs else 0) < 1e-9
            and (max(amp_R_errs) if amp_R_errs else 0) < 1e-8
        ),
        "note": (
            "Exact-shell ε=0 ⇒ Ds≈0. K and R_★ amplitude-invariant. "
            "Reports complete signed Tc in ε-probes."
        ),
    }


def default_ab_pairs(shells: Dict[int, ShellModes]) -> List[Tuple[int, int]]:
    """Several (α,β) pairs: distinct shells with enough modes on α."""
    alphas = sorted(a for a, modes in shells.items() if len(modes) >= 2)
    betas = sorted(shells.keys())
    pairs: List[Tuple[int, int]] = []
    # Prefer β = 2α (self-interaction harmonic) when available, else nearby
    candidates = [
        (1, 2),
        (1, 4),
        (2, 4),
        (2, 5),
        (3, 6),
        (4, 8),
        (5, 10),
        (5, 2),
        (6, 12),
        (8, 4),
        (9, 18),
        (10, 5),
        (13, 26),
        (4, 5),
        (5, 6),
        (6, 8),
        (8, 9),
        (9, 10),
        (2, 8),
        (3, 12),
    ]
    for a, b in candidates:
        if a in shells and b in shells and a != b and len(shells[a]) >= 1:
            pairs.append((a, b))
    # Fill with a few more systematic pairs
    for a in alphas[:8]:
        for b in betas:
            if b != a and (a, b) not in pairs:
                pairs.append((a, b))
            if len(pairs) >= 24:
                return pairs
    return pairs


def reconstruct_best_w(row: Dict) -> Optional[Field]:
    if not row.get("params") or not row.get("modes"):
        return None
    modes = [tuple(m) for m in row["modes"]]
    params = {k: np.asarray(v, dtype=float) for k, v in row["params"].items()}
    return normalize_field(field_from_shell_params(modes, params))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kmax", type=int, default=6)
    ap.add_argument("--trials", type=int, default=60)
    ap.add_argument("--refine", type=int, default=30)
    ap.add_argument("--max-modes", type=int, default=12, help="Cap positive-half modes on α fan")
    ap.add_argument("--seed", type=int, default=1390)
    ap.add_argument(
        "--outdir",
        type=str,
        default="/opt/cursor/artifacts/attack9b_exact_shell",
    )
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    shells = shells_up_to(args.kmax)
    # β may need modes beyond α's kmax for |k|²=β; extend shell table
    kmax_beta = max(args.kmax, int(math.sqrt(max(shells.keys()))) + 2)
    shells_ext = shells_up_to(max(args.kmax + 4, 8))
    pairs = default_ab_pairs(shells_ext)

    print("Attack 9B — Exact-shell + closing packet", flush=True)
    print("9A did NOT kill ★. Kill lane LIVE. NS not solved.", flush=True)

    rows = []
    best_global = {"K": -1.0}
    for alpha, beta in pairs:
        modes = shells_ext.get(alpha, [])
        if not modes:
            continue
        print(f"  optimizing K(α={alpha}, β={beta}), n_pos={len(modes)} ...", flush=True)
        row = optimize_K_on_shell(
            alpha,
            beta,
            modes,
            rng,
            n_trials=args.trials,
            n_refine=args.refine,
            max_modes=args.max_modes,
        )
        # ε-limit + controls on best w
        w = reconstruct_best_w(row)
        eps_check = None
        controls = None
        if w is not None:
            eps_check = eps_limit_check(
                w,
                float(alpha),
                float(beta),
                eps_list=(1e-1, 3e-2, 1e-2, 3e-3, 1e-3),
            )
            controls = run_controls(w, float(alpha), float(beta))
            row["eps_limit"] = {
                k: v for k, v in eps_check.items() if k != "rows"
            }
            row["eps_limit_rows"] = eps_check["rows"]
            row["controls"] = controls
        rows.append(row)
        print(
            f"    K={row['K']:.6e}  PiB_L2={row.get('PiB_L2', 0):.6e}  "
            f"Ds0={row.get('Ds_eps0')}  limit_ok={None if not eps_check else eps_check['limit_ok']}",
            flush=True,
        )
        if row["K"] > best_global["K"]:
            best_global = {
                "K": row["K"],
                "alpha": alpha,
                "beta": beta,
                "n_modes_pos": row.get("n_modes_pos"),
                "PiB_L2": row.get("PiB_L2"),
            }

    # Aggregate controls
    ctrl_pass = all(
        (r.get("controls") or {}).get("controls_pass", False)
        for r in rows
        if r.get("controls")
    )
    limit_pass = all(
        (r.get("eps_limit") or {}).get("limit_ok", False)
        for r in rows
        if r.get("eps_limit") and r.get("K", 0) > 1e-14
    )

    # JSON-safe rows (drop huge params from top summary duplicate)
    summary = {
        "attack": "9B",
        "name": "Exact-shell coherent fan + small closing packet",
        "boxed_K": "K_{α,β} = β ‖Π_β B(w,w)‖₂² / (α² ‖w‖₂⁴)",
        "relation": "lim_{ε→0} R_★(w+ε z_β) = K_{α,β}(w) for z_β ∥ Π_β B(w,w)",
        "attack_9A": "DID NOT kill ★ — Ds grew faster than Tc; Ds‖v‖²Y=O(1) false for AP family",
        "kill_lane": "LIVE",
        "ns_solved": False,
        "lemma_star": "OPEN",
        "kmax": args.kmax,
        "n_pairs": len(rows),
        "max_K": best_global,
        "per_pair": [
            {
                k: v
                for k, v in r.items()
                if k not in ("params",)
            }
            for r in rows
        ],
        "K_by_pair": {f"{r['alpha']},{r['beta']}": r["K"] for r in rows},
        "controls_all_pass": ctrl_pass,
        "eps_limit_all_pass": limit_pass,
        "caveat": (
            "Narrow ≠ Ds=O(1). Lattice amplifies (λ_k−Λ)². "
            "Next: controlled finite shell thickness — not widening AP packet."
        ),
        "truth": "NS is NOT solved. Falsification and proof both LIVE. 9A did not kill ★.",
    }
    (outdir / "attack9b.json").write_text(json.dumps(summary, indent=2) + "\n")

    # Headline
    lines = [
        "# Attack 9B — Exact-shell + closing packet — results",
        "",
        "**Attack 9A:** did **NOT** kill Lemma★ (Ds grew faster than Tc).",
        "**Kill lane:** LIVE",
        "**NS solved:** false",
        "**Lemma★:** OPEN",
        f"**max K seen:** {best_global.get('K')}",
        f"**at (α,β):** ({best_global.get('alpha')}, {best_global.get('beta')})",
        f"**controls_all_pass:** {ctrl_pass}",
        f"**eps_limit_all_pass:** {limit_pass}",
        "",
        "| α | β | n_pos | K | Π_βB L2 | Ds(ε=0) | ε-limit OK |",
        "|---|---|-------|---|---------|---------|------------|",
    ]
    for r in sorted(rows, key=lambda x: -x["K"]):
        el = r.get("eps_limit") or {}
        lines.append(
            f"| {r['alpha']} | {r['beta']} | {r.get('n_modes_pos')} | "
            f"{r['K']:.6e} | {r.get('PiB_L2', 0):.6e} | {r.get('Ds_eps0')} | "
            f"{el.get('limit_ok')} |"
        )
    lines.extend(
        [
            "",
            "Boxed: K_{α,β}=β‖Π_β B(w,w)‖₂²/(α²‖w‖₂⁴).",
            "ε→0: R_★→K for z_β∥Π_β B. Finite sample max ≠ proof. Kill lane LIVE.",
            "NS not solved.",
        ]
    )
    (outdir / "HEADLINE.md").write_text("\n".join(lines) + "\n")

    # Plot K by pair
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        labels = [f"{r['alpha']},{r['beta']}" for r in rows]
        Ks = [r["K"] for r in rows]
        order = np.argsort(Ks)[::-1]
        labels = [labels[i] for i in order]
        Ks = [Ks[i] for i in order]
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(range(len(Ks)), Ks, color="#2c5f6e")
        ax.set_xticks(range(len(Ks)))
        ax.set_xticklabels(labels, rotation=75, ha="right", fontsize=8)
        ax.set_ylabel(r"$K_{\alpha,\beta}$ (optimized on shell)")
        ax.set_title("Attack 9B — exact-shell K (kill lane LIVE; 9A did not kill ★)")
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(outdir / "K_by_ab_pair.png", dpi=140)
        plt.close(fig)

        # ε-limit plot for best pair
        best_row = max(rows, key=lambda r: r["K"])
        erows = best_row.get("eps_limit_rows") or []
        if erows:
            fig, ax = plt.subplots(figsize=(6, 4))
            eps = [row["eps"] for row in erows]
            Rs = [row["R_star"] if row["R_star"] is not None else float("nan") for row in erows]
            ax.semilogx(eps, Rs, "o-", label=r"$\mathcal{R}_\star(v_\varepsilon)$")
            ax.axhline(best_row["K"], color="#a33", linestyle="--", label=r"$K_{\alpha,\beta}(w)$")
            ax.set_xlabel(r"$\varepsilon$")
            ax.set_ylabel(r"$\mathcal{R}_\star$")
            ax.set_title(
                f"ε→0 check at (α,β)=({best_row['alpha']},{best_row['beta']})"
            )
            ax.legend()
            ax.grid(True, which="both", alpha=0.3)
            fig.tight_layout()
            fig.savefig(outdir / "R_star_eps_limit.png", dpi=140)
            plt.close(fig)
    except Exception as exc:  # pragma: no cover
        (outdir / "plot_error.txt").write_text(str(exc) + "\n")

    print(
        json.dumps(
            {
                "max_K": best_global,
                "controls_all_pass": ctrl_pass,
                "eps_limit_all_pass": limit_pass,
                "n_pairs": len(rows),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
