#!/usr/bin/env python3
"""Attack |T_c| ≤ C ||∇u||_3 √(Y D_s) on the centered torus.

Companion to the 1 Oct 2026 centered-flux / q=3 note. That note killed
T_c ≤ C ν D_s (near-shell) and |T_c| ≤ C ||∇u||_3 √D_s (amplitude).
It left two amplitude-homogeneous √D_s repairs OPEN. This harness
attacks them.

Honesty lock
------------
★ NOT proved. NS NOT solved. Kill lane LIVE. Clay B is not closed.
A bounded sample is not a proof. A killed family is not a singular
Navier–Stokes solution.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

Mode = Tuple[int, int, int]


class C:
    """Gaussian rational a+bi with a,b ∈ Q."""

    __slots__ = ("re", "im")

    def __init__(self, re: Fraction | int | str = 0, im: Fraction | int | str = 0) -> None:
        self.re = Fraction(re)
        self.im = Fraction(im)

    def __add__(self, other: "C") -> "C":
        other = _as_c(other)
        return C(self.re + other.re, self.im + other.im)

    def __sub__(self, other: "C") -> "C":
        other = _as_c(other)
        return C(self.re - other.re, self.im - other.im)

    def __neg__(self) -> "C":
        return C(-self.re, -self.im)

    def __mul__(self, other: "C | Fraction | int") -> "C":
        other = _as_c(other)
        return C(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def __truediv__(self, other: "C | Fraction | int") -> "C":
        other = _as_c(other)
        den = other.re * other.re + other.im * other.im
        if den == 0:
            raise ZeroDivisionError("complex division by zero")
        return C(
            (self.re * other.re + self.im * other.im) / den,
            (self.im * other.re - self.re * other.im) / den,
        )

    def conj(self) -> "C":
        return C(self.re, -self.im)

    def abs2(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def real(self) -> Fraction:
        return self.re

    def to_complex(self) -> complex:
        return complex(float(self.re), float(self.im))

    def __repr__(self) -> str:
        return f"C({self.re}, {self.im})"


I = C(0, 1)
ZERO = C(0, 0)
Vec = Tuple[C, C, C]
Field = Dict[Mode, Vec]


def _as_c(value: C | Fraction | int | str) -> C:
    if isinstance(value, C):
        return value
    return C(value, 0)


def _vadd(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _vscale(s: C | Fraction | int, v: Vec) -> Vec:
    c = _as_c(s)
    return (c * v[0], c * v[1], c * v[2])


def _vdot(a: Vec, b: Vec) -> C:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _vdot_conj(a: Vec, b: Vec) -> C:
    return a[0] * b[0].conj() + a[1] * b[1].conj() + a[2] * b[2].conj()


def _vabs2(v: Vec) -> Fraction:
    return v[0].abs2() + v[1].abs2() + v[2].abs2()


def k_norm2(k: Mode) -> int:
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def k_vec(k: Mode) -> Vec:
    return (C(k[0]), C(k[1]), C(k[2]))


def leray_project(k: Mode, v: Vec) -> Vec:
    kn2 = k_norm2(k)
    if kn2 == 0:
        return (ZERO, ZERO, ZERO)
    kv = _vdot(k_vec(k), v)
    return _vadd(v, _vscale(-kv / kn2, k_vec(k)))


def enforce_reality(field: Field) -> Field:
    out: Field = {}
    for k, v in field.items():
        if k == (0, 0, 0):
            continue
        proj = leray_project(k, v)
        mk = (-k[0], -k[1], -k[2])
        out[k] = proj
        out[mk] = (proj[0].conj(), proj[1].conj(), proj[2].conj())
    return out


def moments(field: Field) -> Dict[str, Fraction]:
    E = X = Y = Z = Fraction(0)
    for k, v in field.items():
        lam = Fraction(k_norm2(k))
        if lam == 0:
            continue
        amp2 = _vabs2(v)
        E += amp2
        X += lam * amp2
        Y += lam * lam * amp2
        Z += lam * lam * lam * amp2
    if X == 0:
        raise ValueError("empty or mean-only field")
    Lam = Y / X
    Ds = Z - Lam * Y
    return {"E": E, "X": X, "Y": Y, "Z": Z, "Lambda": Lam, "Ds": Ds}


def nonlinear_B(field: Field) -> Field:
    """B̂_k = i P_k Σ_{p+q=k} (q·v_p) v_q. Exact Q[i] convolution."""
    keys = list(field.keys())
    raw: Dict[Mode, Vec] = {}
    for p in keys:
        vp = field[p]
        for q in keys:
            vq = field[q]
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            coeff = I * _vdot(k_vec(q), vp)
            raw[k] = _vadd(raw.get(k, (ZERO, ZERO, ZERO)), _vscale(coeff, vq))
    return {k: leray_project(k, v) for k, v in raw.items()}


def transfer_Tk(field: Field) -> Dict[Mode, Fraction]:
    Buu = nonlinear_B(field)
    Tk: Dict[Mode, Fraction] = {}
    for k, vk in field.items():
        if k_norm2(k) == 0:
            continue
        bk = Buu.get(k, (ZERO, ZERO, ZERO))
        Tk[k] = -_vdot_conj(bk, vk).real()
    return Tk


def flux_moments(field: Field) -> Dict[str, Fraction]:
    m = moments(field)
    Lam = m["Lambda"]
    Tk = transfer_Tk(field)
    N = sum((Fraction(k_norm2(k)) * t for k, t in Tk.items()), Fraction(0))
    M = sum((Fraction(k_norm2(k)) ** 2 * t for k, t in Tk.items()), Fraction(0))
    Tc = M - Lam * N
    Tc_direct = sum(
        (Fraction(k_norm2(k)) * (Fraction(k_norm2(k)) - Lam) * t for k, t in Tk.items()),
        Fraction(0),
    )
    return {"N": N, "M": M, "Tc": Tc, "Tc_direct": Tc_direct, **m}


def ahalf_B_sq(field: Field) -> Fraction:
    """||A^{1/2} B(u,u)||_2^2 = Σ λ |B̂_k|^2. Exact Q."""
    Buu = nonlinear_B(field)
    acc = Fraction(0)
    for k, bk in Buu.items():
        lam = Fraction(k_norm2(k))
        if lam == 0:
            continue
        acc += lam * _vabs2(bk)
    return acc


def scale_field(field: Field, amp: Fraction | int) -> Field:
    a = Fraction(amp)
    return {k: _vscale(a, v) for k, v in field.items()}


def near_shell_triad(eps: Fraction | int | str) -> Field:
    """Main shell λ=4 plus a closing mode on λ=8 with amplitude ε."""
    eps = Fraction(eps)
    field: Field = {
        (2, 0, 0): (ZERO, C(1), ZERO),
        (0, 2, 0): (ZERO, ZERO, I),
        (2, 2, 0): (ZERO, ZERO, C(eps)),
    }
    return enforce_reality(field)


NEAR_SHELL_EPSILONS: Tuple[Fraction, ...] = (
    Fraction(1, 2),
    Fraction(1, 4),
    Fraction(1, 8),
    Fraction(1, 16),
    Fraction(1, 32),
)


def closed_Ds_near_shell(eps: Fraction) -> Fraction:
    return Fraction(256) * eps * eps / (1 + eps * eps)


def closed_Tc_near_shell(eps: Fraction) -> Fraction:
    return Fraction(64) * eps * (2 + eps * eps) / (1 + eps * eps)


def growing_layer(n: int) -> Field:
    """v_n of the unrestricted-★ growing-layer family (PR #74 / 12 Sep)."""
    if n < 1:
        raise ValueError("n ≥ 1")
    planar = ((1, 0), (-1, 0), (1, 1), (-1, -1), (2, 1), (-2, -1))
    field: Field = {}
    half_i = C(0, Fraction(1, 2))
    for r1, r2 in planar:
        coeff = _vscale(half_i, (C(-r2), C(r1), ZERO))
        for j in range(-n, n + 1):
            k = (n * r1, n * r2, j)
            field[k] = coeff
    return field


def closed_Tc_growing_layer(n: int) -> Fraction:
    return Fraction(3) * n**5 * (3 * n * n + 3 * n + 1)


def separated_two_shell(gap: int) -> Field:
    """Two-shell triad with eigenvalue ratio (α+gap-ish) / α growing in gap."""
    # p=(1,0,0) λ=1, q=(0,1,0) λ=1, k=(1,1,0) λ=2 — gap 1.
    # High copy: p=(m,0,0), q=(0,m,0), k=(m,m,0); ratio 2, not near-shell.
    m = int(gap)
    field: Field = {
        (m, 0, 0): (ZERO, C(1), ZERO),
        (0, m, 0): (ZERO, ZERO, I),
        (m, m, 0): (ZERO, ZERO, C(1)),
    }
    return enforce_reality(field)


def random_cubelet(seed: int = 0, amp: int = 1) -> Field:
    """Mean-zero div-free field on the 3×3×3 cubelet, rational amplitudes."""
    rng = np.random.default_rng(seed)
    field: Field = {}
    for a in range(-1, 2):
        for b in range(-1, 2):
            for c in range(-1, 2):
                k = (a, b, c)
                if k <= (0, 0, 0):
                    continue
                re = [Fraction(int(rng.integers(-3, 4)), 2) for _ in range(3)]
                im = [Fraction(int(rng.integers(-3, 4)), 2) for _ in range(3)]
                field[k] = (C(re[0], im[0]), C(re[1], im[1]), C(re[2], im[2]))
    return scale_field(enforce_reality(field), amp)


def field_to_uhat(field: Field, n_grid: int) -> List[np.ndarray]:
    N = int(n_grid)
    uhat = [np.zeros((N, N, N), dtype=np.complex128) for _ in range(3)]
    for (a, b, c), v in field.items():
        if max(abs(a), abs(b), abs(c)) >= N // 2:
            raise ValueError("mode exceeds grid Nyquist")
        uhat[0][a % N, b % N, c % N] = v[0].to_complex()
        uhat[1][a % N, b % N, c % N] = v[1].to_complex()
        uhat[2][a % N, b % N, c % N] = v[2].to_complex()
    return uhat


def grad_L3_from_uhat(uhat: Sequence[np.ndarray]) -> float:
    N = uhat[0].shape[0]
    kx = np.fft.fftfreq(N) * N
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij")
    wave = [KX, KY, KZ]
    jac2 = np.zeros((N, N, N), dtype=np.float64)
    scale = float(N) ** 3
    for i in range(3):
        for j in range(3):
            phys = np.fft.ifftn(1j * wave[j] * uhat[i]) * scale
            jac2 += np.abs(phys) ** 2
    return float(np.mean(np.sqrt(jac2) ** 3) ** (1.0 / 3.0))


def grad_L3(field: Field, n_grid: int = 32) -> float:
    return grad_L3_from_uhat(field_to_uhat(field, n_grid))


def _min_image(coord: np.ndarray) -> np.ndarray:
    return (coord + math.pi) % (2 * math.pi) - math.pi


def _grid_coords(n_grid: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    N = int(n_grid)
    xs = np.linspace(0.0, 2.0 * math.pi, N, endpoint=False)
    return np.meshgrid(xs, xs, xs, indexing="ij")


def physical_to_uhat(u_phys: Sequence[np.ndarray]) -> List[np.ndarray]:
    N = u_phys[0].shape[0]
    return [np.fft.fftn(comp) / float(N) ** 3 for comp in u_phys]


def project_uhat(uhat: Sequence[np.ndarray]) -> List[np.ndarray]:
    N = uhat[0].shape[0]
    kx = np.fft.fftfreq(N) * N
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij")
    kn2 = KX * KX + KY * KY + KZ * KZ
    kn2[0, 0, 0] = 1.0
    div = KX * uhat[0] + KY * uhat[1] + KZ * uhat[2]
    out = [
        uhat[0] - KX * div / kn2,
        uhat[1] - KY * div / kn2,
        uhat[2] - KZ * div / kn2,
    ]
    out[0][0, 0, 0] = 0.0
    out[1][0, 0, 0] = 0.0
    out[2][0, 0, 0] = 0.0
    return out


def _wave_numbers(n_grid: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    N = int(n_grid)
    kx = np.fft.fftfreq(N) * N
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij")
    kn2 = KX * KX + KY * KY + KZ * KZ
    return KX, KY, KZ, kn2


def spectral_moments(uhat: Sequence[np.ndarray]) -> Dict[str, float]:
    KX, KY, KZ, kn2 = _wave_numbers(uhat[0].shape[0])
    amp2 = sum(np.abs(uhat[i]) ** 2 for i in range(3))
    E = float(np.sum(amp2))
    X = float(np.sum(kn2 * amp2))
    Y = float(np.sum(kn2 * kn2 * amp2))
    Z = float(np.sum(kn2 * kn2 * kn2 * amp2))
    if X == 0.0:
        raise ValueError("empty spectral field")
    Lam = Y / X
    return {"E": E, "X": X, "Y": Y, "Z": Z, "Lambda": Lam, "Ds": Z - Lam * Y}


def spectral_B(uhat: Sequence[np.ndarray]) -> List[np.ndarray]:
    """B̂ = P(u·∇u)̂, matching B̂_k = i P_k Σ (q·v_p) v_q."""
    N = uhat[0].shape[0]
    KX, KY, KZ, kn2 = _wave_numbers(N)
    wave = [KX, KY, KZ]
    scale = float(N) ** 3
    u_phys = [np.fft.ifftn(uhat[i]) * scale for i in range(3)]
    adv = [np.zeros((N, N, N), dtype=np.complex128) for _ in range(3)]
    for i in range(3):
        for j in range(3):
            dji = np.fft.ifftn(1j * wave[j] * uhat[i]) * scale
            adv[i] = adv[i] + u_phys[j] * dji
    Bhat = [np.fft.fftn(adv[i]) / scale for i in range(3)]
    return project_uhat(Bhat)


def spectral_flux(uhat: Sequence[np.ndarray]) -> Dict[str, float]:
    m = spectral_moments(uhat)
    Lam = m["Lambda"]
    Bhat = spectral_B(uhat)
    KX, KY, KZ, kn2 = _wave_numbers(uhat[0].shape[0])
    Tk = np.zeros(uhat[0].shape, dtype=np.float64)
    for i in range(3):
        Tk -= np.real(Bhat[i] * np.conjugate(uhat[i]))
    N = float(np.sum(kn2 * Tk))
    M = float(np.sum(kn2 * kn2 * Tk))
    ahalf_sq = float(sum(np.sum(kn2 * np.abs(Bhat[i]) ** 2) for i in range(3)))
    n_modes = int(np.sum(sum(np.abs(uhat[i]) for i in range(3)) > 1e-12))
    return {"N": N, "M": M, "Tc": M - Lam * N, "ahalf_B_sq": ahalf_sq, "n_modes": n_modes, **m}


def localized_curl_bump(ell: float, n_grid: int = 48, twist: float = 0.35) -> List[np.ndarray]:
    """Divergence-free localized bump: curl of a twisted Gaussian stream."""
    X, Y, Z = _grid_coords(n_grid)
    x = _min_image(X)
    y = _min_image(Y)
    z = _min_image(Z)
    r2 = x * x + y * y + z * z
    phi = np.exp(-r2 / (2.0 * ell * ell)) * (1.0 + twist * x)
    # u = curl(0, 0, φ) + small vertical swirl from ∂z of a second stream
    dphi_dx = -x / (ell * ell) * phi + twist * np.exp(-r2 / (2.0 * ell * ell))
    dphi_dy = -y / (ell * ell) * phi
    psi = twist * np.exp(-r2 / (2.0 * ell * ell)) * y
    dpsi_dx = -x / (ell * ell) * psi
    dpsi_dz = -z / (ell * ell) * psi
    u = dphi_dy
    v = -dphi_dx
    w = dpsi_dx - dpsi_dz * 0.0
    # add a helical lift so T_c need not vanish by planar symmetry
    w = w + twist * (-z / (ell * ell)) * phi
    uhat = project_uhat(physical_to_uhat([u, v, w]))
    return uhat


def log_envelope_triad(delta: float, n_grid: int = 48) -> List[np.ndarray]:
    """Near-shell triad multiplied by a log envelope, then projected.

    W^{1,3} barely fails L^∞. The envelope log(δ² + r²) makes
    ||u||_∞ / ||∇u||_3 grow like (log)^{2/3} as δ → 0.
    """
    field = near_shell_triad(Fraction(1, 4))
    uhat0 = field_to_uhat(field, n_grid)
    scale = float(n_grid) ** 3
    phys = [np.fft.ifftn(uhat0[i]) * scale for i in range(3)]
    X, Y, Z = _grid_coords(n_grid)
    r2 = _min_image(X) ** 2 + _min_image(Y) ** 2 + _min_image(Z) ** 2
    env = np.log(delta * delta + r2)
    env = env - float(np.mean(env))
    weighted = [phys[i] * env for i in range(3)]
    return project_uhat(physical_to_uhat(weighted))


def ratios_from_exact(field: Field, n_grid: int) -> dict:
    flux = flux_moments(field)
    Tc = float(flux["Tc"])
    Ds = float(flux["Ds"])
    Y = float(flux["Y"])
    E = float(flux["E"])
    if Ds <= 0.0:
        raise ValueError("D_s must be positive")
    g3 = grad_L3(field, n_grid=n_grid)
    sqrt_Ds = math.sqrt(Ds)
    sqrt_Y = math.sqrt(Y)
    ahalf2 = float(ahalf_B_sq(field))
    ahalf = math.sqrt(max(ahalf2, 0.0))
    pairing_rhs = ahalf * sqrt_Ds
    return {
        "Tc": str(flux["Tc"]),
        "Ds": str(flux["Ds"]),
        "Y": str(flux["Y"]),
        "E": str(flux["E"]),
        "Lambda": str(flux["Lambda"]),
        "grad_L3": g3,
        "rho_Y": abs(Tc) / (g3 * sqrt_Y * sqrt_Ds),
        "rho_g32": abs(Tc) / (g3 * g3 * sqrt_Ds),
        "rho_star": (max(Tc, 0.0) ** 2) / (Ds * E * Y),
        "rho_linear": abs(Tc) / Ds,
        "pairing_gap": pairing_rhs - abs(Tc),
        "rho_pairing": ahalf / (g3 * sqrt_Y),
        "ahalf_B": ahalf,
    }


def ratios_from_uhat(uhat: Sequence[np.ndarray]) -> dict:
    flux = spectral_flux(uhat)
    Tc = flux["Tc"]
    Ds = flux["Ds"]
    Y = flux["Y"]
    E = flux["E"]
    if Ds <= 1e-18:
        raise ValueError(f"D_s too small: {Ds}")
    g3 = grad_L3_from_uhat(uhat)
    sqrt_Ds = math.sqrt(Ds)
    sqrt_Y = math.sqrt(Y)
    ahalf = math.sqrt(max(flux["ahalf_B_sq"], 0.0))
    return {
        "Tc": Tc,
        "Ds": Ds,
        "Y": Y,
        "E": E,
        "Lambda": flux["Lambda"],
        "n_modes": flux["n_modes"],
        "grad_L3": g3,
        "rho_Y": abs(Tc) / (g3 * sqrt_Y * sqrt_Ds),
        "rho_g32": abs(Tc) / (g3 * g3 * sqrt_Ds),
        "rho_star": (max(Tc, 0.0) ** 2) / (Ds * E * Y),
        "rho_linear": abs(Tc) / Ds,
        "pairing_gap": ahalf * sqrt_Ds - abs(Tc),
        "rho_pairing": ahalf / (g3 * sqrt_Y),
        "ahalf_B": ahalf,
    }


def _monotonic_increasing(values: Sequence[float], slack: float = 0.0) -> bool:
    return all(values[i] + slack < values[i + 1] for i in range(len(values) - 1))


def run_attack(n_grid_sparse: int = 32, n_grid_bump: int = 48) -> dict:
    probe = near_shell_triad(Fraction(1, 8))
    exact_flux = flux_moments(probe)
    spec_flux = spectral_flux(field_to_uhat(probe, n_grid_sparse))
    spectral_matches_exact = abs(spec_flux["Tc"] - float(exact_flux["Tc"])) < 1e-8 and (
        abs(spec_flux["Ds"] - float(exact_flux["Ds"])) < 1e-8
    )

    near_rows = []
    for eps in NEAR_SHELL_EPSILONS:
        field = near_shell_triad(eps)
        flux = flux_moments(field)
        if flux["Tc"] != closed_Tc_near_shell(eps):
            raise AssertionError("near-shell T_c closed form failed")
        if flux["Ds"] != closed_Ds_near_shell(eps):
            raise AssertionError("near-shell D_s closed form failed")
        row = ratios_from_exact(field, n_grid=n_grid_sparse)
        row["eps"] = str(eps)
        near_rows.append(row)

    amp_rows = []
    base = near_shell_triad(Fraction(1, 8))
    for a in (1, 2, 4):
        row = ratios_from_exact(scale_field(base, a), n_grid=n_grid_sparse)
        row["amp"] = a
        amp_rows.append(row)

    grow_rows = []
    for n in (1, 2, 3, 4, 5):
        field = growing_layer(n)
        flux = flux_moments(field)
        if flux["Tc"] != closed_Tc_growing_layer(n):
            raise AssertionError(f"growing-layer T_c lock failed at n={n}: {flux['Tc']}")
        # Dirichlet kernel peak is width ~1/n; need Nyquist > 2n and a few points on the peak.
        n_grid = max(32, 8 * n)
        row = ratios_from_exact(field, n_grid=n_grid)
        row["n"] = n
        grow_rows.append(row)

    sep_rows = []
    for m in (1, 2, 3, 4):
        row = ratios_from_exact(separated_two_shell(m), n_grid=max(32, 8 * m))
        row["m"] = m
        sep_rows.append(row)

    rand_rows = []
    for seed in range(8):
        field = random_cubelet(seed=seed)
        if moments(field)["Ds"] == 0:
            continue
        row = ratios_from_exact(field, n_grid=16)
        row["seed"] = seed
        rand_rows.append(row)

    bump_rows = []
    for ell in (0.90, 0.65, 0.48, 0.36):
        uhat = localized_curl_bump(ell, n_grid=n_grid_bump)
        row = ratios_from_uhat(uhat)
        row["ell"] = ell
        bump_rows.append(row)

    log_rows = []
    for delta in (0.55, 0.35, 0.22, 0.14):
        uhat = log_envelope_triad(delta, n_grid=n_grid_bump)
        row = ratios_from_uhat(uhat)
        row["delta"] = delta
        log_rows.append(row)

    pairing_ok = all(r["pairing_gap"] >= -1e-9 for r in near_rows + grow_rows + sep_rows + rand_rows)

    rhoY_near = [r["rho_Y"] for r in near_rows]
    rhoY_amp = [r["rho_Y"] for r in amp_rows]
    rhoY_grow = [r["rho_Y"] for r in grow_rows]
    rhoY_bump = [r["rho_Y"] for r in bump_rows]
    rhoY_log = [r["rho_Y"] for r in log_rows]
    rho32_bump = [r["rho_g32"] for r in bump_rows]
    rho_lin = [r["rho_linear"] for r in near_rows]
    rho_q3_amp = [
        abs(float(Fraction(r["Tc"]))) / (r["grad_L3"] * math.sqrt(float(Fraction(r["Ds"]))))
        for r in amp_rows
    ]

    amp_Y_rel = max(rhoY_amp) / min(rhoY_amp) if rhoY_amp else float("nan")
    linear_increases = _monotonic_increasing(rho_lin, slack=0.0)
    q3_amp_increases = _monotonic_increasing(rho_q3_amp, slack=0.0)

    # Kill tests: a family kills a candidate if the ratio is unbounded
    # along the designed parameter. We only certify a kill when the
    # sample is monotone and the last/first ratio exceeds a factor 2.
    def _factor(vals: Sequence[float]) -> float:
        return vals[-1] / vals[0] if vals and vals[0] > 0 else float("nan")

    # A family kills a universal C only if the ratio keeps growing in the
    # designed asymptotic regime. A torus-scale transient (first bump
    # width comparable to the box) is not a kill.
    def _tail_kill(vals: Sequence[float], min_factor: float = 2.0, tail: int = 3) -> bool:
        if len(vals) < tail:
            return False
        last = list(vals[-tail:])
        return _monotonic_increasing(last) and _factor(last) >= min_factor

    candidate_Y_status = "OPEN"
    kill_family = None
    for name, vals in (
        ("growing_layer", rhoY_grow),
        ("localized_bump", rhoY_bump),
        ("log_envelope", rhoY_log),
        ("separated_two_shell", [r["rho_Y"] for r in sep_rows]),
    ):
        if _tail_kill(vals):
            candidate_Y_status = f"KILLED_by_{name}"
            kill_family = name
            break

    # Alternate |T_c| ≤ C ||∇u||_3² √D_s is supercritical for a localized
    # bump: predicted ρ_{g32} ~ ℓ^{-1/2}. Certify when the resolved tail
    # collapses after multiplying by √ℓ.
    resolved = [r for r in bump_rows if float(r["ell"]) <= 0.70]
    collapse = [r["rho_g32"] * math.sqrt(float(r["ell"])) for r in resolved]
    g32_tail = [r["rho_g32"] for r in resolved]
    g32_collapse_spread = (max(collapse) / min(collapse)) if collapse else float("nan")
    candidate_g32_status = "OPEN"
    if (
        len(g32_tail) >= 3
        and _monotonic_increasing(g32_tail)
        and g32_collapse_spread < 1.15
    ):
        candidate_g32_status = "KILLED_by_localized_bump_ell_to_the_minus_half"

    summary = {
        "harness": "tc_sqrt_yds_2026-10-01",
        "date": "2026-10-01",
        "ns_solved": False,
        "lemma_star_proved": False,
        "kill_lane": "LIVE",
        "candidate": "|T_c| ≤ C ||∇u||_3 √(Y D_s)",
        "candidate_status": candidate_Y_status,
        "kill_family": kill_family,
        "alternate_candidate": "|T_c| ≤ C ||∇u||_3² √D_s",
        "alternate_status": candidate_g32_status,
        "pairing_identity_holds": pairing_ok,
        "spectral_matches_exact_on_triad": spectral_matches_exact,
        "inherited_kills": {
            "T_c_le_C_nu_Ds": "KILLED_by_near_shell" if linear_increases else "CHECK_FAILED",
            "T_c_le_C_gradL3_sqrt_Ds": "KILLED_by_amplitude" if q3_amp_increases else "CHECK_FAILED",
        },
        "amplitude_rho_Y_relative_spread": amp_Y_rel,
        "bump_g32_sqrt_ell_collapse_spread": g32_collapse_spread,
        "near_shell_rho_Y_limit_observed": rhoY_near[-1],
        "max_rho_Y": {
            "near_shell": max(rhoY_near),
            "amplitude": max(rhoY_amp),
            "growing_layer": max(rhoY_grow),
            "separated_two_shell": max(r["rho_Y"] for r in sep_rows),
            "random_cubelet": max(r["rho_Y"] for r in rand_rows) if rand_rows else None,
            "localized_bump": max(rhoY_bump),
            "log_envelope": max(rhoY_log),
        },
        "factors": {
            "rho_Y_growing_layer": _factor(rhoY_grow),
            "rho_Y_localized_bump": _factor(rhoY_bump),
            "rho_Y_log_envelope": _factor(rhoY_log),
            "rho_g32_localized_bump": _factor(rho32_bump),
            "rho_Y_near_shell": _factor(rhoY_near),
        },
        "near_shell": near_rows,
        "amplitude": amp_rows,
        "growing_layer": grow_rows,
        "separated_two_shell": sep_rows,
        "random_cubelet": rand_rows,
        "localized_bump": bump_rows,
        "log_envelope": log_rows,
        "open": [
            "Lemma★ / sup R_★ < ∞",
            "candidate |T_c| ≤ C ||∇u||_3 √(Y D_s) unless this run killed it",
            "control of ∫ ||∇u||_3² dt",
            "DA-NS-2",
        ],
        "caution": (
            "Exact convolution locks identities and inherited kills. "
            "Localized / log probes are grid FFT. A bounded sample is not a "
            "proof. This does not close Clay Statement B."
        ),
    }
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--n-grid-sparse", type=int, default=32)
    ap.add_argument("--n-grid-bump", type=int, default=48)
    args = ap.parse_args()
    summary = run_attack(n_grid_sparse=args.n_grid_sparse, n_grid_bump=args.n_grid_bump)
    print(json.dumps({k: summary[k] for k in (
        "harness", "ns_solved", "lemma_star_proved", "candidate",
        "candidate_status", "alternate_status", "inherited_kills",
        "max_rho_Y", "factors", "pairing_identity_holds",
    )}, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2) + "\n")
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
