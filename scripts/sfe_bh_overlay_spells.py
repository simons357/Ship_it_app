#!/usr/bin/env python3
"""SFE ↔ black-hole overlay spells — hunt structure without prejudice.

The Simons Field Equation (archived framework):
  Δ((P·H·ψ)² λ) = Φ
  H_SFE = Σ n^{-1/2} N_n + (g/2) Σ N_i N_j/gcd(i,j) − source

Phase folklore:
  Phase I (coherent):  E_0 > -1/2
  Phase II (collapsed): E_0 ≤ -1/2  — maximum concentration / "horizon"

These spells do NOT assume the overlay is true. They:
  1. Build comparable 1D profiles on sites n=1..N (mapped to r)
  2. Cross-correlate with Schwarzschild exterior templates
  3. Report concentration, phase thresholds, and accidental alignments

Usage:
  python3 scripts/sfe_bh_overlay_spells.py [Nmax]
  python3 scripts/sfe_bh_overlay_spells.py 500 1000
"""
from __future__ import annotations

import json
import sys
from math import gcd


def isprime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True
from pathlib import Path

import numpy as np

ARTIFACT_DIR = Path("/opt/cursor/artifacts")
HORIZON_FLOOR = -0.5  # SFE / Bridge* phase line in archived notes
SPECTRAL_TARGET = -1.0 / (2.0 * np.pi)  # Route C λ_min / log N target


def mat_inverse_gcd_norm(N: int) -> np.ndarray:
    q = np.empty((N, N))
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = 1.0 / (gcd(i, j) * (i * j) ** 0.5)
            q[i - 1, j - 1] = q[j - 1, i - 1] = v
    return q


def mat_raw_gcd(N: int) -> np.ndarray:
    q = np.empty((N, N))
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = 1.0 / gcd(i, j)
            q[i - 1, j - 1] = q[j - 1, i - 1] = v
    return q


def normalize_profile(v: np.ndarray) -> np.ndarray:
    v = np.abs(v.astype(float))
    s = v.sum()
    return v / s if s > 0 else v


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = a - a.mean()
    b = b - b.mean()
    den = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / den) if den > 0 else 0.0


def schwarzschild_templates(N: int) -> dict[str, np.ndarray]:
    """Map site n to radius r_n = n/N in (0,1]; compare exterior templates."""
    r = np.arange(1, N + 1, dtype=float) / N
    r_h = 1.0 / N  # inner cutoff (discrete horizon proxy)
    r = np.clip(r, r_h, 1.0)
    return {
        "g_tt_exterior": np.clip(1.0 - r_h / r, 0.0, 1.0),
        "inv_r": r_h / r,
        "inv_r_sqrt": np.sqrt(r_h / r),
        "tortoise_decay": np.exp(-1.0 / r),  # crude exterior falloff
        "photon_sphere_bump": np.exp(-((r - 0.75) ** 2) / (2 * 0.08**2)),
    }


def sfe_discrete_profiles(N: int) -> dict[str, np.ndarray]:
    n = np.arange(1, N + 1, dtype=float)
    q = mat_inverse_gcd_norm(N)
    evals, evecs = np.linalg.eigh(q)
    v_star = evecs[:, 0]
    if v_star.sum() < 0:
        v_star = -v_star

    v_alt = (-1.0) ** (n + 1) / np.sqrt(n)
    harmonic = 1.0 / np.sqrt(n)
    prime_mask = np.array([1.0 if isprime(int(k)) else 0.0 for k in n])
    row_degree = q.sum(axis=1)

    g = 0.5
    h = np.diag(1.0 / np.sqrt(n)) + g * mat_raw_gcd(N)
    _, vec = np.linalg.eigh(h)
    sfe_ground = vec[:, 0]

    return {
        "lambda_min_mode": normalize_profile(v_star),
        "alternating": normalize_profile(v_alt),
        "harmonic_free": normalize_profile(harmonic),
        "prime_sites": normalize_profile(prime_mask + 1e-12),
        "row_degree": normalize_profile(row_degree),
        "sfe_toy_ground": normalize_profile(sfe_ground),
    }


def concentration_index(p: np.ndarray) -> float:
    """Herfindahl: 1 = all mass on one site (BH collapse caricature)."""
    return float(np.sum(p * p))


def phase_readout(N: int) -> dict[str, float]:
    q = mat_inverse_gcd_norm(N)
    lam_min = float(np.linalg.eigvalsh(q)[0])
    logn = np.log(N)
    return {
        "lambda_min": lam_min,
        "lambda_min_over_logN": lam_min / logn,
        "spectral_target": SPECTRAL_TARGET,
        "ratio_to_target": lam_min / logn / SPECTRAL_TARGET,
        "below_half_floor": lam_min < HORIZON_FLOOR,
        "phase_II_by_floor": lam_min <= HORIZON_FLOOR,
    }


def overlay_matrix(N: int) -> tuple[dict[str, dict[str, float]], dict]:
    bh = schwarzschild_templates(N)
    sfe = sfe_discrete_profiles(N)
    corr: dict[str, dict[str, float]] = {}
    for sname, sprof in sfe.items():
        corr[sname] = {}
        for bname, bprof in bh.items():
            corr[sname][bname] = pearson(sprof, bprof)

    meta = {
        "N": N,
        "best_pairs": [],
    }
    pairs = [
        (s, b, corr[s][b])
        for s in corr
        for b in corr[s]
    ]
    pairs.sort(key=lambda x: -abs(x[2]))
    meta["best_pairs"] = [
        {"sfe": s, "bh": b, "pearson": round(r, 4)} for s, b, r in pairs[:8]
    ]
    return corr, meta


def snd_shell_caricature(N: int) -> dict[str, float]:
    """Caricature: shell j gets weight j^{-2} (enstrophy-like) vs harmonic j^{-1/2}."""
    j = np.arange(1, N + 1, dtype=float)
    weights = j ** -2
    weights /= weights.sum()
    rho_max = float(weights.max())
    j_star = int(weights.argmax()) + 1
    return {
        "rho_max": rho_max,
        "j_star": j_star,
        "snd_ok_at_rho0_0.5": rho_max <= 0.5,
        "comment": "Discrete shell toy — not NS data",
    }


def run_spells(sizes: list[int]) -> dict:
    report: dict = {"spells": {}, "leads": []}

    for N in sizes:
        corr, meta = overlay_matrix(N)
        phase = phase_readout(N)
        profiles = sfe_discrete_profiles(N)
        conc = {k: concentration_index(v) for k, v in profiles.items()}
        snd = snd_shell_caricature(N)

        block = {
            "phase": phase,
            "concentration": conc,
            "snd_caricature": snd,
            "overlay_best": meta["best_pairs"],
            "full_correlations": corr,
        }
        report["spells"][str(N)] = block

        best = meta["best_pairs"][0] if meta["best_pairs"] else None
        if best and abs(best["pearson"]) > 0.85:
            report["leads"].append(
                f"N={N}: strong overlay {best['sfe']} ↔ {best['bh']} "
                f"(r={best['pearson']})"
            )

    report["interpretation"] = interpret(report)
    return report


def interpret(report: dict) -> list[str]:
    lines = [
        "Spell readout (honest — correlation ≠ proof):",
        "",
        "1. PHASE LINE: λ_min(Q̃) < -1/2 for moderate N ⇒ discrete operator sits in "
        "archived 'Phase II' by the -1/2 floor folklore. That matches 'collapsed/concentrated' "
        "narrative but is NOT the same as a black hole.",
        "",
        "2. SPECTRAL HORIZON CONSTANT: λ_min/log N ≈ -1/(2π) (Route C) is a different "
        "number from -1/2. Two 'horizons' exist in the stack — do not merge without proof.",
        "",
        "3. OVERLAY: If |Pearson| > 0.85 between λ_min mode profile and a BH template, "
        "flag for manual review — may be harmonic weight artifact (1/√n ~ 1/√r).",
        "",
        "4. SFE TOY HAMILTONIAN: diag(n^{-1/2}) + g·(1/gcd) ground state is the discrete "
        "spell for 'free harmonic + prime pressure'. Compare its concentration to v*.",
        "",
        "5. NEXT SPELL (outside box): couple shell enstrophy ODE (T2) to λ_min ODE in log N — "
        "look for same -1/(2π) constant in both flows.",
    ]

    for lead in report.get("leads", []):
        lines.insert(5, f"   → LEAD: {lead}")

    return lines


def print_report(report: dict) -> None:
    print("=" * 72)
    print("SFE ↔ BLACK-HOLE OVERLAY SPELLS")
    print("=" * 72)
    for N, block in report["spells"].items():
        print(f"\n--- N = {N} ---")
        ph = block["phase"]
        print(
            f"  λ_min={ph['lambda_min']:.6f}  λ/log N={ph['lambda_min_over_logN']:.6f}  "
            f"target={ph['spectral_target']:.6f}  ratio={ph['ratio_to_target']:.3f}  "
            f"Phase-II floor? {ph['phase_II_by_floor']}"
        )
        print("  Concentration (Herfindahl, 1=collapse):")
        for k, v in sorted(block["concentration"].items(), key=lambda x: -x[1]):
            print(f"    {k:20s} {v:.4f}")
        print("  Best BH overlays (Pearson):")
        for p in block["overlay_best"][:5]:
            print(f"    {p['sfe']:20s} ↔ {p['bh']:20s}  r = {p['pearson']:+.4f}")
        print(f"  SND shell caricature: ρ_max={block['snd_caricature']['rho_max']:.4f} "
              f"at j*={block['snd_caricature']['j_star']}")

    print("\n" + "=" * 72)
    for line in report["interpretation"]:
        print(line)
    print("=" * 72)


def main() -> None:
    sizes = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [100, 500, 1000]
    report = run_spells(sizes)
    print_report(report)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    out_json = ARTIFACT_DIR / "sfe_bh_overlay_spells.json"
    # trim full corr for json size
    slim = {
        "spells": {
            k: {
                "phase": v["phase"],
                "concentration": v["concentration"],
                "overlay_best": v["overlay_best"],
                "snd_caricature": v["snd_caricature"],
            }
            for k, v in report["spells"].items()
        },
        "leads": report["leads"],
        "interpretation": report["interpretation"],
    }
    out_json.write_text(json.dumps(slim, indent=2))
    print(f"\nWrote {out_json}")


if __name__ == "__main__":
    main()
