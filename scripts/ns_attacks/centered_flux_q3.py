#!/usr/bin/env python3
"""Independent flux-algebra check for the ChatGPT q=3 progress note.

Exact rational Fourier convolution on a two-shell triad. No floating-point
triad sums for T_c or D_s. L^3 gradient norms are grid quadratures only.

Honesty lock
------------
★ NOT proved. NS NOT solved. Kill lane LIVE.
The stated target |T_c| ≤ C ||∇u||_3 √D_s is NOT a universal bound:
amplitude scaling kills any field-independent C. Near-shell still rules
out T_c ≤ C ν D_s and shows why a √D_s factor is the right leading
perturbation order. Conditional AM-GM is algebra, not a proof.
Controlling ∫ ||∇u||_3² dt remains a separate open task.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, Sequence, Tuple

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

    def imag(self) -> Fraction:
        return self.im

    def to_complex(self) -> complex:
        return complex(float(self.re), float(self.im))

    def as_pair(self) -> Tuple[str, str]:
        return (str(self.re), str(self.im))

    def __repr__(self) -> str:
        return f"C({self.re}, {self.im})"


I = C(0, 1)
ZERO = C(0, 0)


def _as_c(value: C | Fraction | int | str) -> C:
    if isinstance(value, C):
        return value
    return C(value, 0)


Vec = Tuple[C, C, C]
Field = Dict[Mode, Vec]


def _vadd(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _vscale(s: C | Fraction | int, v: Vec) -> Vec:
    c = _as_c(s)
    return (c * v[0], c * v[1], c * v[2])


def _vdot(a: Vec, b: Vec) -> C:
    """Euclidean a·b (no conjugation)."""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _vdot_conj(a: Vec, b: Vec) -> C:
    """a · conj(b)."""
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


def Ds_variance_sum(field: Field, Lam: Fraction | None = None) -> Fraction:
    if Lam is None:
        Lam = moments(field)["Lambda"]
    acc = Fraction(0)
    for k, v in field.items():
        lam = Fraction(k_norm2(k))
        if lam == 0:
            continue
        acc += lam * (lam - Lam) ** 2 * _vabs2(v)
    return acc


def Ds_double_sum(field: Field) -> Fraction:
    modes = [(Fraction(k_norm2(k)), _vabs2(v)) for k, v in field.items() if k_norm2(k) > 0]
    X = sum((lam * e for lam, e in modes), Fraction(0))
    acc = Fraction(0)
    for lam_k, ek in modes:
        for lam_l, el in modes:
            acc += lam_k * lam_l * (lam_k - lam_l) ** 2 * ek * el
    return acc / (2 * X)


def Ds_two_shell(alpha: Fraction, beta: Fraction, e_alpha: Fraction, e_beta: Fraction) -> Fraction:
    denom = alpha * e_alpha + beta * e_beta
    return alpha * beta * (alpha - beta) ** 2 * e_alpha * e_beta / denom


def shell_energies(field: Field) -> Dict[int, Fraction]:
    shells: Dict[int, Fraction] = {}
    for k, v in field.items():
        lam = k_norm2(k)
        if lam == 0:
            continue
        shells[lam] = shells.get(lam, Fraction(0)) + _vabs2(v)
    return shells


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
    """T_k = −Re(B̂_k · conj(v_k)). Signed. No absolute values."""
    Buu = nonlinear_B(field)
    Tk: Dict[Mode, Fraction] = {}
    for k, vk in field.items():
        if k_norm2(k) == 0:
            continue
        bk = Buu.get(k, (ZERO, ZERO, ZERO))
        Tk[k] = -_vdot_conj(bk, vk).real()
    return Tk


def flux_moments(field: Field) -> Dict[str, Fraction]:
    """Energy-cancellation, N, M, T_c, and the centered rewrite of N."""
    m = moments(field)
    Lam = m["Lambda"]
    Tk = transfer_Tk(field)
    sum_Tk = sum(Tk.values(), Fraction(0))
    N = sum((Fraction(k_norm2(k)) * t for k, t in Tk.items()), Fraction(0))
    M = sum((Fraction(k_norm2(k)) ** 2 * t for k, t in Tk.items()), Fraction(0))
    N_centered = sum(((Fraction(k_norm2(k)) - Lam) * t for k, t in Tk.items()), Fraction(0))
    Tc_from_NM = M - Lam * N
    Tc_direct = sum(
        (Fraction(k_norm2(k)) * (Fraction(k_norm2(k)) - Lam) * t for k, t in Tk.items()),
        Fraction(0),
    )
    # M = Σ(λ−Λ)² T_k + 2Λ N + Λ² Σ T_k
    quad = sum(((Fraction(k_norm2(k)) - Lam) ** 2 * t for k, t in Tk.items()), Fraction(0))
    Tc_from_quad = quad + Lam * N
    return {
        "sum_Tk": sum_Tk,
        "N": N,
        "M": M,
        "N_centered": N_centered,
        "boundary_Lambda_sum_Tk": Lam * sum_Tk,
        "Tc": Tc_from_NM,
        "Tc_direct": Tc_direct,
        "Tc_from_quad": Tc_from_quad,
        "Lambda": Lam,
        **m,
    }


def Lambda_prime_rhs(Tc: Fraction, Ds: Fraction, X: Fraction, nu: Fraction) -> Fraction:
    return (2 / X) * (Tc - nu * Ds)


def Lambda_prime_from_XY(
    N: Fraction, M: Fraction, X: Fraction, Y: Fraction, Z: Fraction, nu: Fraction
) -> Fraction:
    Xp = -2 * nu * Y + 2 * N
    Yp = -2 * nu * Z + 2 * M
    return (Yp * X - Y * Xp) / (X * X)


def scale_field(field: Field, amp: Fraction | int) -> Field:
    a = Fraction(amp)
    return {k: _vscale(a, v) for k, v in field.items()}


def near_shell_triad(eps: Fraction | int | str) -> Field:
    """Main shell λ=4 plus a closing mode on λ=8 with amplitude ε.

    Modes
        p = (2,0,0), v_p = (0, 1, 0)
        q = (0,2,0), v_q = (0, 0, i)
        k = (2,2,0), v_k = (0, 0, ε)
    plus Hermitian conjugates. p+q=k is an exact lattice triad, so the
    leading transfer onto the closing shell is linear in ε.
    """
    eps = Fraction(eps)
    field: Field = {
        (2, 0, 0): (ZERO, C(1), ZERO),
        (0, 2, 0): (ZERO, ZERO, I),
        (2, 2, 0): (ZERO, ZERO, C(eps)),
    }
    return enforce_reality(field)


# Five exact parameter values used for the independent reproduction.
NEAR_SHELL_EPSILONS: Tuple[Fraction, ...] = (
    Fraction(1, 2),
    Fraction(1, 4),
    Fraction(1, 8),
    Fraction(1, 16),
    Fraction(1, 32),
)


def closed_Ds_near_shell(eps: Fraction) -> Fraction:
    """D_s = 256 ε² / (1+ε²) for the locked two-shell triad above."""
    return Fraction(256) * eps * eps / (1 + eps * eps)


def closed_Tc_near_shell(eps: Fraction) -> Fraction:
    """T_c = 64 ε (2+ε²) / (1+ε²) for the locked two-shell triad above."""
    return Fraction(64) * eps * (2 + eps * eps) / (1 + eps * eps)


def grad_L3(field: Field, n_grid: int = 32) -> float:
    """||∇u||_{L^3(T³)} with mean-normalized Lebesgue measure.

    |∇u| = (Σ_{i,j} |∂_j u_i|²)^{1/2}. Trapezoid / DFT quadrature.
    This is numerical. T_c and D_s are never taken from this grid.
    """
    N = int(n_grid)
    if N < 8:
        raise ValueError("n_grid too small")
    kx = np.fft.fftfreq(N) * N
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij")
    wave = [KX, KY, KZ]
    uhat = [np.zeros((N, N, N), dtype=np.complex128) for _ in range(3)]
    for (a, b, c), v in field.items():
        if max(abs(a), abs(b), abs(c)) >= N // 2:
            raise ValueError("mode exceeds grid Nyquist")
        uhat[0][a % N, b % N, c % N] = v[0].to_complex()
        uhat[1][a % N, b % N, c % N] = v[1].to_complex()
        uhat[2][a % N, b % N, c % N] = v[2].to_complex()
    jac2 = np.zeros((N, N, N), dtype=np.float64)
    scale = float(N) ** 3
    for i in range(3):
        for j in range(3):
            phys = np.fft.ifftn(1j * wave[j] * uhat[i]) * scale
            jac2 += np.abs(phys) ** 2
    grad_norm = np.sqrt(jac2)
    return float(np.mean(grad_norm**3) ** (1.0 / 3.0))


def am_gm_remainder(C: float, grad_L3_norm: float, nu: float) -> float:
    """C ||∇u||_3 √D_s ≤ ν D_s + C² ||∇u||_3² / (4ν); this is the second term."""
    if nu <= 0:
        raise ValueError("nu must be positive")
    return (C * C * grad_L3_norm * grad_L3_norm) / (4.0 * nu)


@dataclass(frozen=True)
class NearShellRow:
    eps: str
    Tc: str
    Ds: str
    Ds_closed: str
    Tc_closed: str
    Tc_over_eps: str
    Ds_over_eps2: str
    abs_Tc_over_Ds: str
    abs_Tc_over_sqrt_Ds: str
    E: str
    Y: str
    Lambda: str
    grad_L3: float
    rho_q3: float
    rho_q3Y: float
    R_star: float


def _frac_str(x: Fraction) -> str:
    return str(x)


def _sqrt_frac(x: Fraction) -> float:
    return float(x) ** 0.5


def probe_near_shell(eps: Fraction, n_grid: int = 32) -> NearShellRow:
    field = near_shell_triad(eps)
    flux = flux_moments(field)
    Tc = flux["Tc"]
    Ds = flux["Ds"]
    Ds_cl = closed_Ds_near_shell(eps)
    Tc_cl = closed_Tc_near_shell(eps)
    if Ds != Ds_cl:
        raise AssertionError(f"Ds mismatch: {Ds} != {Ds_cl}")
    if Tc != Tc_cl:
        raise AssertionError(f"Tc mismatch: {Tc} != {Tc_cl}")
    g3 = grad_L3(field, n_grid=n_grid)
    sqrt_Ds = _sqrt_frac(Ds)
    Y = flux["Y"]
    E = flux["E"]
    rho_q3 = abs(float(Tc)) / (g3 * sqrt_Ds)
    rho_q3Y = abs(float(Tc)) / (g3 * (float(Y) ** 0.5) * sqrt_Ds)
    Tc_plus = max(Tc, Fraction(0))
    R_star = float(Tc_plus * Tc_plus / (Ds * E * Y))
    return NearShellRow(
        eps=_frac_str(eps),
        Tc=_frac_str(Tc),
        Ds=_frac_str(Ds),
        Ds_closed=_frac_str(Ds_cl),
        Tc_closed=_frac_str(Tc_cl),
        Tc_over_eps=_frac_str(Tc / eps),
        Ds_over_eps2=_frac_str(Ds / (eps * eps)),
        abs_Tc_over_Ds=_frac_str(abs(Tc) / Ds),
        abs_Tc_over_sqrt_Ds=f"{abs(float(Tc)) / sqrt_Ds:.12e}",
        E=_frac_str(E),
        Y=_frac_str(Y),
        Lambda=_frac_str(flux["Lambda"]),
        grad_L3=g3,
        rho_q3=rho_q3,
        rho_q3Y=rho_q3Y,
        R_star=R_star,
    )


def amplitude_scaling_kill(eps: Fraction = Fraction(1, 8), amps: Sequence[int] = (1, 2, 4)) -> list[dict]:
    """|T_c| / (||∇u||_3 √D_s) grows like amplitude. Universal C is impossible."""
    rows = []
    base = near_shell_triad(eps)
    for a in amps:
        field = scale_field(base, a)
        flux = flux_moments(field)
        g3 = grad_L3(field)
        rho = abs(float(flux["Tc"])) / (g3 * _sqrt_frac(flux["Ds"]))
        rows.append(
            {
                "amp": a,
                "Tc": str(flux["Tc"]),
                "Ds": str(flux["Ds"]),
                "grad_L3": g3,
                "rho_q3": rho,
                "rho_q3_over_amp": rho / a,
            }
        )
    return rows


def run_reproduction(n_grid: int = 32) -> dict:
    identities = {}
    field = near_shell_triad(Fraction(1, 8))
    flux = flux_moments(field)
    identities["energy_cancellation_sum_Tk"] = str(flux["sum_Tk"])
    identities["boundary_term_Lambda_sum_Tk"] = str(flux["boundary_Lambda_sum_Tk"])
    identities["N_equals_centered"] = flux["N"] == flux["N_centered"]
    identities["Tc_NM_equals_direct"] = flux["Tc"] == flux["Tc_direct"]
    identities["Tc_NM_equals_quad"] = flux["Tc"] == flux["Tc_from_quad"]
    identities["Ds_variance"] = Ds_variance_sum(field) == flux["Ds"]
    identities["Ds_double"] = Ds_double_sum(field) == flux["Ds"]
    nu = Fraction(1, 10)
    identities["Lambda_prime_matches"] = Lambda_prime_rhs(
        flux["Tc"], flux["Ds"], flux["X"], nu
    ) == Lambda_prime_from_XY(flux["N"], flux["M"], flux["X"], flux["Y"], flux["Z"], nu)

    rows = [probe_near_shell(eps, n_grid=n_grid) for eps in NEAR_SHELL_EPSILONS]
    tc_over_ds = [float(Fraction(r.abs_Tc_over_Ds)) for r in rows]
    increasing = all(tc_over_ds[i] < tc_over_ds[i + 1] for i in range(len(tc_over_ds) - 1))

    summary = {
        "harness": "centered_flux_q3_exact_rational",
        "date": "2026-10-01",
        "source_note": "ChatGPT Work / Centered Flux progress screenshots",
        "ns_solved": False,
        "lemma_star_proved": False,
        "kill_lane": "LIVE",
        "identities": identities,
        "near_shell_rows": [r.__dict__ for r in rows],
        "abs_Tc_over_Ds_increases_as_eps_falls": increasing,
        "linear_viscosity_bound_T_c_le_C_nu_Ds": "KILLED_by_near_shell",
        "stated_q3_bound_universal_C": "KILLED_by_amplitude_scaling",
        "square_root_Ds_leading_order": "CONFIRMED_on_locked_triad",
        "closed_forms": {
            "Ds": "256 ε² / (1+ε²)",
            "Tc": "64 ε (2+ε²) / (1+ε²)",
            "Tc_over_Ds": "(2+ε²) / (4ε)",
            "Tc_over_sqrt_Ds": "4 (2+ε²) / √(1+ε²)  →  8",
        },
        "homogeneous_repair_candidates": [
            "|T_c| ≤ C ||∇u||_3 √(Y D_s)",
            "|T_c| ≤ C ||∇u||_3² √D_s",
        ],
        "amplitude_scaling": amplitude_scaling_kill(),
        "conditional_am_gm": (
            "IF |T_c| ≤ C ||∇u||_3 √D_s THEN T_c − ν D_s ≤ C² ||∇u||_3² / (4ν). "
            "Hypothesis false as a universal bound; algebra of the implication is correct."
        ),
        "open": [
            "Lemma★ / sup R_★ < ∞",
            "any homogeneous replacement of the q=3 target",
            "control of ∫ ||∇u||_3² dt",
            "DA-NS-2",
        ],
        "caution": (
            "Exact convolution verifies identities and the near-shell obstruction. "
            "It does not prove ★ and does not close Clay Statement B."
        ),
    }
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--n-grid", type=int, default=32)
    args = ap.parse_args()
    summary = run_reproduction(n_grid=args.n_grid)
    print(json.dumps(summary, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2) + "\n")
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
