#!/usr/bin/env python3
"""Attack 9D retarget — growing input AND output supports, complex polarizations.

Fixed-output Θ(m²) 9D is analytically excluded (K ≤ 16s). See
docs/math/ns_attacks/ATTACK_9B_COUNTING_CS_EXCLUSION.md.

This probe keeps frequency factors and reports
  C_obs = ||Π_β B(w,w)||₂ · √β / (α ||w||₂²)
on exact-shell w with full complex polarizations. Uniform 9B target is sup C_obs < ∞.
Growing s is allowed; K ≤ 16s does not close ★ if s→∞.

Does NOT prove Lemma★. NS is not solved. Kill lane LIVE.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ns_attacks.attack9b_exact_shell_K import (  # noqa: E402
    K_of_w,
    build_exact_shell_field,
    field_l2,
    normalize_field,
    project_B_to_shell,
    shells_up_to,
)
from ns_attacks.counting_cs import (  # noqa: E402
    K_cs_fixed_s,
    check_cs_pointwise,
    max_ordered_pairs_per_output,
    occupied_shell_keys,
    observed_C_alpha_over_sqrt_beta,
)
from ns_attacks.stokes_moments import nonlinear_B  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=str, required=True)
    ap.add_argument("--kmax", type=int, default=6)
    ap.add_argument("--seed", type=int, default=1390)
    ap.add_argument("--n-pol", type=int, default=4, help="complex polarization trials per pair")
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)
    shells = shells_up_to(args.kmax)
    alphas = sorted(shells)
    rows = []
    cs_ok = True
    count_ok = True

    for alpha in alphas:
        pos = shells[alpha]
        modes = pos  # build_exact_shell_field conjugate-closes
        n_pos = len(pos)
        betas = [b for b in alphas if b != alpha and b <= 4 * alpha]
        for beta in betas:
            best = None
            for _ in range(args.n_pol):
                amps = rng.uniform(0.3, 1.4, size=n_pos)
                thetas = rng.uniform(0, 2 * np.pi, size=n_pos)
                phis = rng.uniform(0, 2 * np.pi, size=n_pos)
                w = normalize_field(build_exact_shell_field(modes, amps, thetas, phis))
                energy = field_l2(w) ** 2
                Buu = nonlinear_B(w)
                if not check_cs_pointwise(w, Buu):
                    cs_ok = False
                PiB = project_B_to_shell(Buu, float(beta))
                occ = occupied_shell_keys(PiB, float(beta))
                s = len(occ)
                support = list(w.keys())
                m = len(support)
                max_pairs = max_ordered_pairs_per_output(support, occ) if occ else 0
                if max_pairs > m:
                    count_ok = False
                info = K_of_w(w, float(alpha), float(beta))
                cap = K_cs_fixed_s(max(s, 1), float(alpha), float(beta)) if s else 0.0
                if s and info["K"] > cap + 1e-8:
                    count_ok = False
                C_obs = observed_C_alpha_over_sqrt_beta(
                    info["PiB_L2"], float(alpha), float(beta), energy
                )
                rec = {
                    "alpha": alpha,
                    "beta": beta,
                    "m": m,
                    "n_pos": n_pos,
                    "s": s,
                    "max_pairs_per_output": max_pairs,
                    "K": info["K"],
                    "K_cap_s_beta2_over_alpha2": cap,
                    "C_obs": C_obs,
                    "PiB_L2": info["PiB_L2"],
                    "beta_over_alpha": beta / alpha,
                }
                if best is None or rec["K"] > best["K"]:
                    best = rec
            if best is not None:
                rows.append(best)

    finite_K = [r for r in rows if math.isfinite(r["K"])]
    max_row = max(finite_K, key=lambda r: r["K"]) if finite_K else {}
    max_C = max((r["C_obs"] for r in rows if math.isfinite(r.get("C_obs", float("nan")))), default=float("nan"))

    payload = {
        "attack": "9D_retarget_growing_io",
        "ns_solved": False,
        "lemma_star": "OPEN",
        "fixed_output_Theta_m2": "EXCLUDED_analytically_K_le_16s",
        "cs_pointwise_ok": cs_ok,
        "counting_ok": count_ok,
        "kmax": args.kmax,
        "n_pairs": len(rows),
        "max_K": max_row,
        "max_C_obs": max_C,
        "uniform_target": "||Pi_beta B||_2 <= C alpha/sqrt(beta) ||w||_2^2",
        "per_pair": rows,
        "verdict": "FIXED_OUTPUT_EXCLUDED_growing_io_LIVE_not_a_proof",
    }
    (outdir / "attack9d_growing_io.json").write_text(json.dumps(payload, indent=2))
    lines = [
        "# Attack 9D retarget — growing I/O, complex polarizations",
        "",
        "**NS solved:** false",
        "**Lemma★:** OPEN",
        "**Fixed-output Θ(m²):** EXCLUDED (K ≤ 16s)",
        f"**cs_pointwise_ok:** {cs_ok}",
        f"**counting_ok:** {count_ok}",
        f"**max K (this sample):** {max_row.get('K')} at (α,β)=({max_row.get('alpha')},{max_row.get('beta')}), s={max_row.get('s')}",
        f"**max C_obs:** {max_C}",
        "",
        "Finite sample ≠ proof. Kill lane LIVE if C_obs or K can grow with output support.",
        "NS not solved.",
    ]
    (outdir / "HEADLINE.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: payload[k] for k in ("cs_pointwise_ok", "counting_ok", "max_K", "max_C_obs", "verdict")}, indent=2))
    return 0 if cs_ok and count_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
