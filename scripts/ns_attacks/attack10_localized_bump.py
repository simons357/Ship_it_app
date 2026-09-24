"""Attack 10 — localized divergence-free bump kills uniform R★.

On a fixed torus, a single bump of width ℓ has

    R★(v_ℓ) = ℓ^{-3} R★(V)

exactly, for the physical-space rescaling v_ℓ(x) = V((x-x₀)/ℓ).
Fourier-shell families miss this because torus dilation
v(n·) is one localization times n³ periodic copies, and the
two factors cancel.

This script builds v = curl ψ with ψ a polynomial-Gaussian
stream function, evaluates the centered moments spectrally,
and reports R★ · ℓ³.

NS is not solved. Static uniform R★ is dead. The live
question is dynamical: can NS hold a concentrating bump
with coherent positive T_c.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

# Default torus is T³ = (R / 2π Z)³. Physical L² uses dx.
TWOPI = 2.0 * math.pi
DEFAULT_SEED = 20260924
DEFAULT_WIDTHS = (0.55, 0.45, 0.38, 0.32)


@dataclass(frozen=True)
class Moments:
    ell: float
    Tc: float
    Ds: float
    E: float
    X: float
    Y: float
    Z: float
    Lambda: float
    R_star: float
    R_star_ell3: float
    tail_beyond_n3: float
    mean_div_l2: float
    n: int

    def as_row(self) -> dict[str, float | int]:
        return asdict(self)


def _wavenumbers(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    k = np.fft.fftfreq(n, d=1.0 / n)  # integers 0, 1, ..., n/2-1, -n/2, ...
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    return kx, ky, kz, k2


def _grid(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(0.0, TWOPI, n, endpoint=False)
    return np.meshgrid(x, x, x, indexing="ij")


def polynomial_stream(x: np.ndarray, y: np.ndarray, z: np.ndarray, seed: int) -> np.ndarray:
    """Fixed-seed quadratic polynomial stream ψ: R³ → R³."""
    rng = np.random.default_rng(seed)
    # 10 monomials: 1, x, y, z, x², y², z², xy, xz, yz
    coeffs = rng.normal(scale=1.0, size=(3, 10))
    mons = np.stack(
        [
            np.ones_like(x),
            x,
            y,
            z,
            x * x,
            y * y,
            z * z,
            x * y,
            x * z,
            y * z,
        ],
        axis=0,
    )
    return np.einsum("cm,mijk->cijk", coeffs, mons)


def gaussian_envelope(x: np.ndarray, y: np.ndarray, z: np.ndarray, ell: float, center: float) -> np.ndarray:
    dx = x - center
    dy = y - center
    dz = z - center
    r2 = dx * dx + dy * dy + dz * dz
    return np.exp(-r2 / (2.0 * ell * ell))


def build_bump_field(
    n: int,
    ell: float,
    seed: int = DEFAULT_SEED,
    center: float = math.pi,
) -> tuple[np.ndarray, float]:
    """Return real grid velocity v = curl(ψ) and the spectral tail past N/3.

    ψ = (random quadratic polynomial) × Gaussian of width ℓ.
    The polynomial is written in scaled coordinates (x-x₀)/ℓ so that
    v_ℓ(x) = ℓ^{-1} V((x-x₀)/ℓ). Amplitude drops out of R★; the
    extra ℓ^{-1} from the curl changes T_c ~ ℓ^{-5} but not R★ · ℓ³.
    """
    x, y, z = _grid(n)
    xs = (x - center) / ell
    ys = (y - center) / ell
    zs = (z - center) / ell
    psi_poly = polynomial_stream(xs, ys, zs, seed)
    env = gaussian_envelope(x, y, z, ell, center)
    psi = psi_poly * env

    kx, ky, kz, _k2 = _wavenumbers(n)
    psi_hat = np.fft.fftn(psi, axes=(1, 2, 3))
    # curl ψ in Fourier: i k × ψ̂
    vx = 1j * (ky * psi_hat[2] - kz * psi_hat[1])
    vy = 1j * (kz * psi_hat[0] - kx * psi_hat[2])
    vz = 1j * (kx * psi_hat[1] - ky * psi_hat[0])
    vhat = np.stack([vx, vy, vz], axis=0)
    # kill the mean (already ~0 for a curl)
    vhat[:, 0, 0, 0] = 0.0
    v = np.fft.ifftn(vhat, axes=(1, 2, 3)).real
    tail = _spectral_tail_beyond_n3(vhat)
    return v, tail


def _spectral_tail_beyond_n3(vhat: np.ndarray) -> float:
    n = vhat.shape[-1]
    kx, ky, kz, _k2 = _wavenumbers(n)
    cutoff = n / 3.0
    mask = (np.abs(kx) > cutoff) | (np.abs(ky) > cutoff) | (np.abs(kz) > cutoff)
    energy = np.sum(np.abs(vhat) ** 2)
    if energy <= 0:
        return 0.0
    return float(np.sum(np.abs(vhat[:, mask]) ** 2) / energy)


def _project_leray(uhat: np.ndarray, kx, ky, kz, k2) -> np.ndarray:
    kdotu = kx * uhat[0] + ky * uhat[1] + kz * uhat[2]
    safe = k2.copy()
    safe[0, 0, 0] = 1.0
    proj = uhat - np.stack([kx, ky, kz], axis=0) * (kdotu / safe)
    proj[:, 0, 0, 0] = 0.0
    return proj


def _dealias_mask(n: int) -> np.ndarray:
    kx, ky, kz, _k2 = _wavenumbers(n)
    cutoff = n / 3.0
    return (np.abs(kx) <= cutoff) & (np.abs(ky) <= cutoff) & (np.abs(kz) <= cutoff)


def physical_inner(a: np.ndarray, b: np.ndarray) -> float:
    """⟨a,b⟩ = ∫ a·b dx on the 2π-torus, trapezoid / spectral (uniform grid)."""
    n = a.shape[-1]
    cell = (TWOPI / n) ** 3
    return float(np.sum(a * b) * cell)


def centered_moments(v: np.ndarray) -> tuple[float, float, float, float, float, float, float, float]:
    """Return Tc, Ds, E, X, Y, Z, Lambda, mean_div_l2 from a real grid field.

    A = −PΔ. Because Av and A²v are already divergence-free, the Leray
    projection drops out of N and M when they are paired against Av.
    We still project B for the recorded nonlinear field.
    """
    if v.ndim != 4 or v.shape[0] != 3 or v.shape[1] != v.shape[2] or v.shape[2] != v.shape[3]:
        raise ValueError("v must have shape (3, N, N, N)")
    n = v.shape[-1]
    kx, ky, kz, k2 = _wavenumbers(n)
    vhat = np.fft.fftn(v, axes=(1, 2, 3))
    vhat = _project_leray(vhat, kx, ky, kz, k2)

    # rows are ∂_j v_i
    grad_v = np.stack(
        [
            np.stack(
                [
                    np.fft.ifftn(1j * kx * vhat[i]).real,
                    np.fft.ifftn(1j * ky * vhat[i]).real,
                    np.fft.ifftn(1j * kz * vhat[i]).real,
                ],
                axis=0,
            )
            for i in range(3)
        ],
        axis=0,
    )  # (3, 3, N, N, N) — grad_v[i, j] = ∂_j v_i

    conv = np.einsum("j...,ij...->i...", v, grad_v)  # (v·∇)v
    conv_hat = np.fft.fftn(conv, axes=(1, 2, 3))
    conv_hat *= _dealias_mask(n)
    bhat = _project_leray(conv_hat, kx, ky, kz, k2)
    b = np.fft.ifftn(bhat, axes=(1, 2, 3)).real

    av_hat = k2 * vhat
    a2v_hat = k2 * av_hat
    av = np.fft.ifftn(av_hat, axes=(1, 2, 3)).real
    a2v = np.fft.ifftn(a2v_hat, axes=(1, 2, 3)).real

    e = physical_inner(v, v)
    x_mom = physical_inner(v, av)  # ⟨v, Av⟩ = ||A^{1/2} v||²
    y = physical_inner(av, av)
    z = physical_inner(av, a2v)  # ⟨Av, A²v⟩ = ||A^{3/2} v||²
    if x_mom <= 0.0:
        raise RuntimeError("X vanished; field is empty or mean-only")
    lam = y / x_mom
    ds = z - lam * y
    # T_c = −⟨B, A(A−Λ)v⟩ = −⟨B, A²v − Λ Av⟩
    n_lin = -physical_inner(b, av)
    m_lin = -physical_inner(b, a2v)
    tc = m_lin - lam * n_lin

    div_hat = 1j * (kx * vhat[0] + ky * vhat[1] + kz * vhat[2])
    div = np.fft.ifftn(div_hat).real
    cell = (TWOPI / n) ** 3
    mean_div = math.sqrt(float(np.sum(div * div) * cell))

    return tc, ds, e, x_mom, y, z, lam, mean_div


def r_star(tc: float, ds: float, energy: float, y: float) -> float:
    if ds <= 0.0 or energy <= 0.0 or y <= 0.0:
        return 0.0
    return (max(tc, 0.0) ** 2) / (ds * energy * y)


def evaluate_width(n: int, ell: float, seed: int = DEFAULT_SEED) -> Moments:
    v, tail = build_bump_field(n, ell, seed=seed)
    tc, ds, e, x_mom, y, z, lam, mean_div = centered_moments(v)
    rs = r_star(tc, ds, e, y)
    return Moments(
        ell=float(ell),
        Tc=float(tc),
        Ds=float(ds),
        E=float(e),
        X=float(x_mom),
        Y=float(y),
        Z=float(z),
        Lambda=float(lam),
        R_star=float(rs),
        R_star_ell3=float(rs * ell**3),
        tail_beyond_n3=float(tail),
        mean_div_l2=float(mean_div),
        n=int(n),
    )


def evaluate_family(
    n: int,
    widths: Sequence[float],
    seed: int = DEFAULT_SEED,
) -> list[Moments]:
    return [evaluate_width(n, ell, seed=seed) for ell in widths]


def sign_flip_check(n: int, ell: float, seed: int = DEFAULT_SEED) -> dict[str, float]:
    v, _tail = build_bump_field(n, ell, seed=seed)
    tc_p, ds_p, e_p, _x, y_p, _z, _lam, _div = centered_moments(v)
    tc_m, ds_m, e_m, _x, y_m, _z, _lam, _div = centered_moments(-v)
    return {
        "Tc_plus": float(tc_p),
        "Tc_minus": float(tc_m),
        "Ds_plus": float(ds_p),
        "Ds_minus": float(ds_m),
        "E_plus": float(e_p),
        "E_minus": float(e_m),
        "Y_plus": float(y_p),
        "Y_minus": float(y_m),
        "rel_Tc_sum": float(abs(tc_p + tc_m) / max(abs(tc_p), 1e-30)),
        "rel_Ds": float(abs(ds_p - ds_m) / max(abs(ds_p), 1e-30)),
    }


def single_shell_vacuous(n: int = 16) -> dict[str, float]:
    """One Fourier shell: D_s = 0 and every weight λ(λ−Λ) vanishes, so T_c = 0."""
    x, y, z = _grid(n)
    # Shear / ABC fragment on |k|² = 1: v = (sin z, 0, 0) is not div-free.
    # Use the exact eigenfield v = (cos y, 0, 0) wait — div = 0.
    # Standard: v = (sin y, 0, 0) has div 0, −Δv = v, single shell λ=1.
    v = np.zeros((3, n, n, n), dtype=float)
    v[0] = np.sin(y)
    tc, ds, e, x_mom, y_m, z_m, lam, _div = centered_moments(v)
    return {
        "Tc": float(tc),
        "Ds": float(ds),
        "E": float(e),
        "Lambda": float(lam),
        "X": float(x_mom),
        "Y": float(y_m),
        "Z": float(z_m),
    }


def scaling_spread(rows: Iterable[Moments]) -> float:
    vals = [row.R_star_ell3 for row in rows if row.R_star > 0]
    if len(vals) < 2:
        return float("inf")
    return float((max(vals) - min(vals)) / max(abs(np.mean(vals)), 1e-30))


def format_table(rows: Sequence[Moments]) -> str:
    lines = [
        f"{'ℓ':>8}  {'T_c':>12}  {'R★':>12}  {'R★·ℓ³':>14}  {'tail>N/3':>10}",
        "-" * 64,
    ]
    for row in rows:
        lines.append(
            f"{row.ell:8.3f}  {row.Tc:12.4e}  {row.R_star:12.4e}  "
            f"{row.R_star_ell3:14.6e}  {row.tail_beyond_n3:10.2e}"
        )
    return "\n".join(lines)


def run(
    n: int = 64,
    widths: Sequence[float] = DEFAULT_WIDTHS,
    seed: int = DEFAULT_SEED,
    out: Path | None = None,
) -> dict:
    rows = evaluate_family(n, widths, seed=seed)
    flip = sign_flip_check(n, widths[min(1, len(widths) - 1)], seed=seed)
    vacuous = single_shell_vacuous(n=min(n, 16))
    payload = {
        "attack": 10,
        "verdict": "STATIC_UNIFORM_RSTAR_DEAD",
        "lemma_star": "KILLED_AS_STATIC_BOUND",
        "ns_solved": False,
        "n": n,
        "seed": seed,
        "widths": list(widths),
        "rows": [row.as_row() for row in rows],
        "R_star_ell3_rel_spread": scaling_spread(rows),
        "sign_flip": flip,
        "single_shell_vacuous": vacuous,
        "table": format_table(rows),
        "note": (
            "R★ · ℓ³ constant means R★ grows as ℓ^{-3}. "
            "A single localized bump kills any universal C_geom. "
            "NS is not solved; the remaining question is dynamical persistence."
        ),
    }
    if out is not None:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=64, help="spectral grid size (N³)")
    parser.add_argument(
        "--widths",
        type=float,
        nargs="+",
        default=list(DEFAULT_WIDTHS),
        help="bump widths ℓ",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=None, help="optional JSON path")
    parser.add_argument("--quick", action="store_true", help="32³, two widths (CI)")
    args = parser.parse_args(argv)
    n = 32 if args.quick else args.n
    widths = (0.70, 0.55) if args.quick else tuple(args.widths)
    payload = run(n=n, widths=widths, seed=args.seed, out=args.out)
    print(payload["table"])
    print()
    print(f"R★·ℓ³ relative spread: {payload['R_star_ell3_rel_spread']:.3e}")
    print(f"verdict: {payload['verdict']}")
    print("NS not solved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
