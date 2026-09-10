#!/usr/bin/env python3
"""Honest NS/SND analytic probe — toolkit checks, NOT a Theorem H / Clay proof.

Computes on synthetic Fourier / band-limited fields:

1. Dyadic shell energy ratios rho = J/X (SND diagnostic shape only).
2. A discrete Ring-Lemma-style inequality check on random band-limited
   direction fields (geometric toolkit stress test).
3. Documents that c* = 6/pi^2 is an arithmetic constant (zeta(2)^{-1}),
   not a proved continuum NS SND floor.

Does not claim regularity, SND-U, or Clay Statement (B).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DISCLAIMER = (
    "PROBE ONLY. Numerics here do not prove Theorem H, SND-U, or Clay B. "
    "SND-C under X<=M remains conditional; SND-U remains open."
)

CSTAR_ARITHMETIC = 6.0 / (math.pi**2)  # zeta(2)^{-1}


@dataclass
class ShellProbeResult:
    n_modes: int
    n_trials: int
    mean_rho: float
    min_rho: float
    max_rho: float
    fraction_rho_below_cstar_arithmetic: float
    note: str


@dataclass
class RingProbeResult:
    n_trials: int
    n_points: int
    lipschitz_bound: float
    mean_left: float
    mean_right: float
    fraction_inequality_holds: float
    note: str


def dyadic_shell_index(k_norm: np.ndarray) -> np.ndarray:
    """Map |k| to dyadic shell index j with support roughly in [2^j, 2^{j+1})."""
    kn = np.maximum(k_norm, 1e-12)
    return np.floor(np.log2(kn)).astype(int)


def shell_energy_ratios(
    rng: np.random.Generator,
    n_modes: int = 512,
    n_trials: int = 200,
    dim: int = 3,
) -> ShellProbeResult:
    """Synthetic Fourier energy on random shells; report rho = J/X."""
    rhos: list[float] = []
    for _ in range(n_trials):
        # Random wavevectors and complex amplitudes (synthetic, not NS solutions).
        k = rng.normal(size=(n_modes, dim))
        # Bias a subset toward a dominant shell to span rho in (0,1].
        if rng.random() < 0.5:
            j_dom = int(rng.integers(2, 6))
            angles = rng.normal(size=(n_modes, dim))
            angles /= np.linalg.norm(angles, axis=1, keepdims=True) + 1e-12
            radii = (2.0**j_dom) * (1.0 + 0.3 * rng.random(n_modes))
            k = angles * radii[:, None]
        amp = rng.normal(size=n_modes) + 1j * rng.normal(size=n_modes)
        # Enstrophy proxy ~ |k|^2 |u_hat|^2
        kn = np.linalg.norm(k, axis=1)
        x_mode = (kn**2) * (np.abs(amp) ** 2)
        shells = dyadic_shell_index(kn)
        # Aggregate per shell
        uniq = np.unique(shells)
        x_shell = np.array([float(x_mode[shells == j].sum()) for j in uniq])
        X = float(x_shell.sum())
        if X <= 0:
            continue
        J = float(x_shell.max())
        rhos.append(J / X)
    arr = np.asarray(rhos, dtype=float)
    below = float(np.mean(arr < CSTAR_ARITHMETIC)) if len(arr) else 0.0
    return ShellProbeResult(
        n_modes=n_modes,
        n_trials=len(arr),
        mean_rho=float(arr.mean()) if len(arr) else float("nan"),
        min_rho=float(arr.min()) if len(arr) else float("nan"),
        max_rho=float(arr.max()) if len(arr) else float("nan"),
        fraction_rho_below_cstar_arithmetic=below,
        note=(
            "Synthetic Fourier energy only. rho can sit below 6/pi^2 without "
            "saying anything about continuum NS solutions."
        ),
    )


def ring_lemma_bandlimited_check(
    rng: np.random.Generator,
    n_trials: int = 100,
    n_points: int = 64,
    lipschitz_bound: float = 2.0,
) -> RingProbeResult:
    """Check a toy inequality inspired by band-limited direction control.

    Model: on the unit sphere sample, let xi be a Lipschitz unit direction field
    (synthetic). A Ring-style geometric bound compares a stretching proxy
    |xi · (grad xi) · xi| against Lip(xi)^2. This is a toolkit stress test on
    random fields — not the continuum Ring Lemma proof.
    """
    holds = 0
    lefts: list[float] = []
    rights: list[float] = []
    for _ in range(n_trials):
        # Random points on S^2 (normalize Gaussians).
        pts = rng.normal(size=(n_points, 3))
        pts /= np.linalg.norm(pts, axis=1, keepdims=True) + 1e-12
        # Build a mildly Lipschitz direction by projecting a smooth map.
        # xi(x) = normalize(A x + eps noise) with ||A|| controlled.
        A = rng.normal(size=(3, 3)) * (lipschitz_bound / 4.0)
        raw = pts @ A.T + 0.05 * rng.normal(size=pts.shape)
        xi = raw / (np.linalg.norm(raw, axis=1, keepdims=True) + 1e-12)
        # Finite-difference stretch proxy between neighbors.
        # Pair each point with its nearest neighbor.
        d2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(axis=2)
        np.fill_diagonal(d2, np.inf)
        nn = np.argmin(d2, axis=1)
        dxi = xi - xi[nn]
        dist = np.sqrt(d2[np.arange(n_points), nn]) + 1e-12
        grad_proxy = np.linalg.norm(dxi, axis=1) / dist
        # Left: mean |xi · Δxi| / dist  (directional stretch)
        left = float(np.mean(np.abs((xi * dxi).sum(axis=1)) / dist))
        right = float(lipschitz_bound**2)
        lefts.append(left)
        rights.append(right)
        # Toy inequality: directional stretch bounded by Lip^2 (loose).
        if left <= right + 1e-9:
            holds += 1
    return RingProbeResult(
        n_trials=n_trials,
        n_points=n_points,
        lipschitz_bound=lipschitz_bound,
        mean_left=float(np.mean(lefts)) if lefts else float("nan"),
        mean_right=float(np.mean(rights)) if rights else float("nan"),
        fraction_inequality_holds=holds / max(n_trials, 1),
        note=(
            "Band-limited geometric stress test on synthetic direction fields. "
            "Passing does not prove the continuum Ring Lemma or SND."
        ),
    )


def arithmetic_cstar_note() -> dict:
    zeta2 = math.pi**2 / 6.0
    return {
        "cstar_arithmetic": CSTAR_ARITHMETIC,
        "zeta2": zeta2,
        "identity": "6/pi^2 == 1/zeta(2)",
        "holds": abs(CSTAR_ARITHMETIC * zeta2 - 1.0) < 1e-12,
        "fluids_status": (
            "analogy_only — not a proved continuum NS SND floor "
            "(see ARCHON adversarial verdict Gap H5)"
        ),
    }


def run_probe(seed: int = 20260825) -> dict:
    rng = np.random.default_rng(seed)
    shell = shell_energy_ratios(rng)
    ring = ring_lemma_bandlimited_check(rng)
    payload = {
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "disclaimer": DISCLAIMER,
        "seed": seed,
        "shell_energy_ratios": asdict(shell),
        "ring_lemma_toy_check": asdict(ring),
        "cstar_arithmetic": arithmetic_cstar_note(),
        "claim_lock": {
            "SND-U": "open / hypothesis",
            "SND-C": "conditional under X<=M",
            "Clay_B": "NOT resolved",
            "numerics_prove_theorem_h": False,
        },
    }
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional JSON output path",
    )
    parser.add_argument("--seed", type=int, default=20260825)
    args = parser.parse_args(argv)
    payload = run_probe(seed=args.seed)
    text = json.dumps(payload, indent=2)
    print(text)
    print(file=sys.stderr)
    print(DISCLAIMER, file=sys.stderr)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
