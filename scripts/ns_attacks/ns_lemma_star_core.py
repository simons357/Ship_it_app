"""ns_lemma_star_core — preferred self-contained Lemma★ shape core (SoT lock).

Exact Lemma★ shape quantities from SoT (LEMMA_STAR_SHAPE_FORM.md /
LEMMA_STAR_EXACT_FORMULAS.md). No external Stokes eigenbasis dependency.

  T^3 = (R/2πZ)^3
  v(x) = Σ_{k≠0} v_k e^{ik·x},  k·v_k = 0,  v_{-k} = conj(v_k)
  λ_k = |k|^2,  A = -PΔ,  (Av)_k = λ_k v_k
  B(v,v) = P[(v·∇)v]

  ||v||_2^2 = Σ |v_k|^2
  X = ||A^{1/2}v||_2^2 = Σ λ_k |v_k|^2
  Y = ||Av||_2^2       = Σ λ_k^2 |v_k|^2
  Z = ||A^{3/2}v||_2^2 = Σ λ_k^3 |v_k|^2
  Λ = Y/X

  D_s = Z − Y^2/X = Z − Λ Y = ||(A−Λ) A^{1/2} v||_2^2
      = Σ λ_k (λ_k−Λ)^2 |v_k|^2
      = (1/(2X)) Σ_{k,ℓ} λ_k λ_ℓ (λ_k−λ_ℓ)^2 |v_k|^2 |v_ℓ|^2   (≥ 0)
  Dual cross-check: moment form vs variance sum (and pairwise) must agree.

  B̂_k = i P_k Σ_{p+q=k} (q·v_p) v_q
  T_k = −Re(B̂_k · conj(v_k)) = Σ_{p+q=k} Im[(q·v_p)(v_q·conj(v_k))]
        (SIGNED Im — never abs)
  N = −⟨B,Av⟩ = Σ λ_k T_k
  M = −⟨AB,Av⟩ = Σ λ_k^2 T_k
  T_c = M − Λ N = Σ λ_k (λ_k−Λ) T_k   (direct triad)

  R_★(v) = (T_c)_+^2 / (D_s · ||v||_2^2 · Y)   (amp-/dilation-/ν-invariant)
  where (T_c)_+ = max(T_c, 0).

Lemma★ shape claim (OPEN; NS not solved; locks formulas only):
  ∃ C_geom < ∞  ∀ nonzero v ∈ C^∞_{div,0}(T^3):
    (T_c(v)_+)^2 ≤ C_geom · D_s(v) · ||v||_2^2 · Y(v)
  For D_s=0: one shell and T_c=0 (vacuous).

This module is the preferred self-contained core for Jonathan handoff
(R_★ / polarization probes). attack9b may keep importing stokes_moments —
that path is unchanged. Numerics here do NOT prove ★. NS is NOT solved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import numpy as np

ModeKey = Tuple[int, int, int]


# ---------------------------------------------------------------------------
# Field class — conjugate-closed Fourier Galerkin amplitudes on T^3
# ---------------------------------------------------------------------------


@dataclass
class Field:
    """Divergence-free mean-zero Fourier field: mode k → amplitude in C^3.

    Invariants (after ``enforce``):
      - no k=(0,0,0)
      - v_{-k} = conj(v_k)
      - k · v_k ≈ 0 (Leray)
    """

    modes: MutableMapping[ModeKey, np.ndarray] = field(default_factory=dict)

    def __post_init__(self) -> None:
        cleaned: Dict[ModeKey, np.ndarray] = {}
        for k, v in self.modes.items():
            cleaned[tuple(int(x) for x in k)] = np.asarray(v, dtype=np.complex128).reshape(3)
        self.modes = cleaned

    def copy(self) -> "Field":
        return Field({k: v.copy() for k, v in self.modes.items()})

    def keys(self) -> Iterable[ModeKey]:
        return self.modes.keys()

    def items(self) -> Iterable[Tuple[ModeKey, np.ndarray]]:
        return self.modes.items()

    def values(self) -> Iterable[np.ndarray]:
        return self.modes.values()

    def __contains__(self, k: ModeKey) -> bool:
        return k in self.modes

    def __getitem__(self, k: ModeKey) -> np.ndarray:
        return self.modes[k]

    def __setitem__(self, k: ModeKey, v: np.ndarray) -> None:
        self.modes[k] = np.asarray(v, dtype=np.complex128).reshape(3)

    def get(self, k: ModeKey, default: Optional[np.ndarray] = None) -> np.ndarray:
        if k in self.modes:
            return self.modes[k]
        if default is None:
            return np.zeros(3, dtype=np.complex128)
        return default

    def __len__(self) -> int:
        return len(self.modes)

    def __iter__(self) -> Iterator[ModeKey]:
        return iter(self.modes)

    def as_dict(self) -> Dict[ModeKey, np.ndarray]:
        return {k: v.copy() for k, v in self.modes.items()}

    @classmethod
    def from_mapping(cls, m: Mapping[ModeKey, np.ndarray]) -> "Field":
        return cls(dict(m))


# ---------------------------------------------------------------------------
# Linear algebra helpers
# ---------------------------------------------------------------------------


def k_norm2(k: ModeKey) -> float:
    return float(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])


def leray_project(k: ModeKey, v: np.ndarray) -> np.ndarray:
    """P_k v = v − (k·v) k / |k|^2 for k≠0; zero at k=0."""
    kn2 = k_norm2(k)
    if kn2 == 0:
        return np.zeros(3, dtype=np.complex128)
    kk = np.array(k, dtype=np.float64)
    vv = np.asarray(v, dtype=np.complex128).reshape(3)
    return vv - (np.dot(kk, vv) / kn2) * kk


def _orthonormal_pol_basis(k: ModeKey) -> Tuple[np.ndarray, np.ndarray]:
    kk = np.array(k, dtype=np.float64)
    nrm = float(np.linalg.norm(kk))
    if nrm < 1e-15:
        raise ValueError("k=0 has no polarization plane")
    seed = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(seed, kk)) > 0.9 * nrm:
        seed = np.array([0.0, 1.0, 0.0])
    e1 = seed - (np.dot(seed, kk) / (nrm * nrm)) * kk
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(kk / nrm, e1)
    e2 = e2 / np.linalg.norm(e2)
    return e1, e2


def pol_from_angles(k: ModeKey, theta: float, phi: float) -> np.ndarray:
    """Unit complex polarization in the Leray plane at k."""
    e1, e2 = _orthonormal_pol_basis(k)
    v = np.cos(theta) * e1 + np.sin(theta) * e2
    return (np.exp(1j * phi) * v).astype(np.complex128)


def make_divfree_amp(k: ModeKey, seed_vec: Sequence[float]) -> np.ndarray:
    return leray_project(k, np.array(seed_vec, dtype=np.complex128))


def enforce(field: Field) -> Field:
    """Ensure reality v_{-k}=conj(v_k) and Leray projection; drop k=0."""
    out: Dict[ModeKey, np.ndarray] = {}
    for k, v in field.items():
        if k == (0, 0, 0):
            continue
        mk = (-k[0], -k[1], -k[2])
        proj = leray_project(k, np.asarray(v, dtype=np.complex128))
        if k in out:
            continue
        if mk == k:
            out[k] = np.real(proj).astype(np.complex128)
        else:
            out[k] = proj
            out[mk] = np.conjugate(proj)
    return Field(out)


# Alias used by tests / handoff docs
enforce_reality = enforce


def scale_field(field: Field, B: float) -> Field:
    return Field({k: B * v for k, v in field.items()})


def field_energy(field: Field) -> float:
    """||v||_2^2 = Σ |v_k|^2."""
    return float(sum(np.vdot(v, v).real for v in field.values()))


def field_l2(field: Field) -> float:
    return float(np.sqrt(max(field_energy(field), 0.0)))


def normalize_field(field: Field) -> Field:
    n = field_l2(field)
    if n < 1e-30:
        raise ValueError("zero field")
    return Field({k: v / n for k, v in field.items()})


def max_div_residual(field: Field) -> float:
    """max_k |k · v_k| / (1+|k||v_k|)."""
    worst = 0.0
    for k, v in field.items():
        if k == (0, 0, 0):
            continue
        kk = np.array(k, dtype=np.float64)
        num = abs(np.dot(kk, v))
        den = 1.0 + np.linalg.norm(kk) * np.linalg.norm(v)
        worst = max(worst, float(num / den))
    return worst


def max_reality_residual(field: Field) -> float:
    """max_k ||v_{-k} − conj(v_k)||."""
    worst = 0.0
    for k, v in field.items():
        mk = (-k[0], -k[1], -k[2])
        if mk not in field.modes:
            worst = max(worst, float(np.linalg.norm(v)))
            continue
        worst = max(worst, float(np.linalg.norm(field[mk] - np.conjugate(v))))
    return worst


# ---------------------------------------------------------------------------
# Linear Stokes moments + dual D_s cross-check
# ---------------------------------------------------------------------------


def moments(field: Field) -> Dict[str, float]:
    """Linear Stokes moments. E := ||v||_2^2.

    Ds := D_s = Z − Y^2/X = Z − Λ Y.
    """
    E = X = Y = Z = 0.0
    for k, v in field.items():
        amp2 = float(np.vdot(v, v).real)
        kn2 = k_norm2(k)
        if kn2 == 0:
            continue
        E += amp2
        X += kn2 * amp2
        Y += kn2 * kn2 * amp2
        Z += kn2 * kn2 * kn2 * amp2
    Lam = Y / X if X > 0 else float("nan")
    Ds = Z - Lam * Y if X > 0 else float("nan")
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "Ds": Ds,
        "D_s": Ds,
    }


def D_s_moment(field: Field) -> float:
    """Form 1: D_s = Z − Λ Y = Z − Y^2/X."""
    return moments(field)["Ds"]


def D_s_variance_sum(field: Field, Lambda: float | None = None) -> float:
    """Form 2: D_s = Σ_k λ_k (λ_k − Λ)^2 |v_k|^2."""
    if Lambda is None:
        Lambda = moments(field)["Lambda"]
    s = 0.0
    for k, v in field.items():
        lam = k_norm2(k)
        if lam == 0:
            continue
        amp2 = float(np.vdot(v, v).real)
        s += lam * (lam - Lambda) ** 2 * amp2
    return s


def D_s_double_sum(field: Field) -> float:
    """Form 3: D_s = (1/(2X)) Σ_{k,ℓ} λ_k λ_ℓ (λ_k−λ_ℓ)^2 |v_k|^2 |v_ℓ|^2."""
    modes = [(k_norm2(k), float(np.vdot(v, v).real)) for k, v in field.items() if k_norm2(k) > 0]
    X = sum(lam * e for lam, e in modes)
    if X <= 0:
        return float("nan")
    acc = 0.0
    for lam_k, ek in modes:
        for lam_l, el in modes:
            acc += lam_k * lam_l * (lam_k - lam_l) ** 2 * ek * el
    return acc / (2.0 * X)


def D_s_cross_check(field: Field, rtol: float = 1e-9, atol: float = 1e-12) -> Dict[str, float | bool]:
    """Dual D_s cross-check: moment vs variance (and pairwise)."""
    m = D_s_moment(field)
    v = D_s_variance_sum(field)
    d = D_s_double_sum(field)
    agree_mv = abs(m - v) <= atol + rtol * max(abs(m), abs(v), 1.0)
    agree_md = abs(m - d) <= atol + rtol * max(abs(m), abs(d), 1.0) if d == d else False
    return {
        "D_s_moment": float(m),
        "D_s_variance": float(v),
        "D_s_double": float(d) if d == d else float("nan"),
        "agree_moment_variance": bool(agree_mv),
        "agree_moment_double": bool(agree_md),
        "agree": bool(agree_mv and agree_md),
    }


def Ds_two_shell(alpha: float, beta: float, e_alpha: float, e_beta: float) -> float:
    """Two-eigenvalue closed form: αβ(α−β)^2 e_α e_β / (α e_α + β e_β)."""
    denom = alpha * e_alpha + beta * e_beta
    if denom <= 0:
        return float("nan")
    return (alpha * beta * (alpha - beta) ** 2 * e_alpha * e_beta) / denom


def shell_energies(field: Field) -> Dict[float, float]:
    shells: Dict[float, float] = {}
    for k, v in field.items():
        lam = k_norm2(k)
        if lam == 0:
            continue
        shells[lam] = shells.get(lam, 0.0) + float(np.vdot(v, v).real)
    return shells


# ---------------------------------------------------------------------------
# Nonlinearity + direct triad T_c
# ---------------------------------------------------------------------------


def nonlinear_B(field: Field) -> Field:
    """B(v,v)=P[(v·∇)v]: B̂_k = i P_k Σ_{p+q=k} (q·v_p) v_q."""
    keys = list(field.keys())
    raw: Dict[ModeKey, np.ndarray] = {}
    for p in keys:
        up = field[p]
        for q in keys:
            uq = field[q]
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            q_vec = np.array(q, dtype=np.float64)
            coeff = 1j * np.dot(q_vec, up)
            contrib = coeff * uq
            raw[k] = raw.get(k, np.zeros(3, dtype=np.complex128)) + contrib
    out: Dict[ModeKey, np.ndarray] = {}
    for k, v in raw.items():
        out[k] = leray_project(k, v)
    return Field(out)


def triad_Im_transfer(field: Field) -> Dict[ModeKey, float]:
    """T_k = −Re(B̂_k · conj(v_k)) (signed; no abs)."""
    Buu = nonlinear_B(field)
    Tk: Dict[ModeKey, float] = {}
    for k, vk in field.items():
        if k_norm2(k) == 0:
            continue
        bk = Buu.get(k)
        Tk[k] = -float(np.dot(bk, np.conjugate(vk)).real)
    return Tk


def N_and_M(field: Field) -> Tuple[float, float, Field]:
    """N = −⟨B,Av⟩ = Σ λ T_k,  M = −⟨AB,Av⟩ = Σ λ^2 T_k."""
    Buu = nonlinear_B(field)
    N = 0.0 + 0.0j
    M = 0.0 + 0.0j
    keys = set(field.keys()) | set(Buu.keys())
    for k in keys:
        kn2 = k_norm2(k)
        if kn2 == 0:
            continue
        uk = field.get(k)
        bk = Buu.get(k)
        Tk = -np.dot(bk, np.conjugate(uk))
        N += kn2 * Tk
        M += (kn2 * kn2) * Tk
    return float(N.real), float(M.real), Buu


def T_c_direct(field: Field, Lambda: float | None = None) -> float:
    """Direct triad T_c = Σ_{p+q=k} λ_k(λ_k−Λ) Im[(q·v_p)(v_q·conj(v_k))] via Leray B.

    Equivalent to M − Λ N. Signed — never abs the triad sum.
    """
    if Lambda is None:
        Lambda = moments(field)["Lambda"]
    keys = list(field.keys())
    Tc = 0.0
    for p in keys:
        vp = field[p]
        for q in keys:
            vq = field[q]
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0) or k not in field:
                continue
            lam = k_norm2(k)
            if lam == 0:
                continue
            vk = field[k]
            q_vec = np.array(q, dtype=np.float64)
            coeff = 1j * np.dot(q_vec, vp)
            bk_contrib = leray_project(k, coeff * vq)
            tk_piece = -float(np.dot(bk_contrib, np.conjugate(vk)).real)
            Tc += lam * (lam - Lambda) * tk_piece
    return Tc


def T_c_from_NM(field: Field) -> float:
    """T_c = M − Λ N (inner-product SoT form)."""
    m = moments(field)
    N, M, _ = N_and_M(field)
    return M - m["Lambda"] * N


# Public aliases matching SoT naming
Tc_direct = T_c_direct
Tc_from_NM = T_c_from_NM


def R_star(field: Field) -> float:
    """Canonical shape★ quotient R_★ = (T_c)_+^2 / (D_s ||v||_2^2 Y).

    Returns nan when D_s≈0 or Y=0 or E=0 (vacuous / undefined).
    """
    f = enforce(field)
    m = moments(f)
    Tc = T_c_from_NM(f)
    Tc_plus = max(Tc, 0.0)
    E, Y, Ds = m["E"], m["Y"], m["Ds"]
    denom = Ds * E * Y
    if not (E > 0 and Y > 0 and Ds > 1e-30 and denom == denom):
        return float("nan")
    return (Tc_plus * Tc_plus) / denom


def probe_star(field: Field) -> Dict[str, float]:
    """Compact probe dict for handoff / smoke logs."""
    f = enforce(field)
    m = moments(f)
    Tc = T_c_from_NM(f)
    Tc_triad = T_c_direct(f)
    cross = D_s_cross_check(f)
    return {
        "E": m["E"],
        "X": m["X"],
        "Y": m["Y"],
        "Z": m["Z"],
        "Lambda": m["Lambda"],
        "D_s": m["Ds"],
        "T_c": Tc,
        "T_c_direct": Tc_triad,
        "T_c_plus": max(Tc, 0.0),
        "R_star": R_star(f),
        "D_s_agree": float(cross["agree"]),
        "div_residual": max_div_residual(f),
        "reality_residual": max_reality_residual(f),
    }


# ---------------------------------------------------------------------------
# Shell generators (self-contained — no external eigenbasis)
# ---------------------------------------------------------------------------


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


def modes_on_shell(alpha: int, kmax: int | None = None) -> List[ModeKey]:
    """Positive-half modes with |k|^2 = alpha (Stokes shell)."""
    if kmax is None:
        kmax = int(np.ceil(np.sqrt(alpha))) + 1
    return [k for k in positive_half_modes(kmax) if int(k_norm2(k)) == int(alpha)]


def single_shell_field(
    alpha: int = 1,
    amp: float = 1.0,
    k: ModeKey | None = None,
    theta: float = 0.3,
    phi: float = 0.7,
) -> Field:
    """Exact single Stokes eigen-shell field (conjugate-closed).

    Pure single shell ⇒ D_s=0 and typically T_c=0 (vacuous for ★).
    """
    if k is None:
        cands = modes_on_shell(alpha)
        if not cands:
            # fallback common shells
            for kk in ((1, 0, 0), (1, 1, 0), (2, 1, 0), (2, 1, 1)):
                if int(k_norm2(kk)) == int(alpha):
                    k = kk
                    break
            if k is None:
                raise ValueError(f"no lattice mode with |k|^2={alpha}")
        else:
            k = cands[0]
    elif int(k_norm2(k)) != int(alpha):
        raise ValueError(f"mode {k} has |k|^2={k_norm2(k)}, expected {alpha}")
    v = amp * pol_from_angles(k, theta, phi)
    return enforce(Field({k: v}))


def two_shell_field(
    alpha: int = 1,
    beta: int = 5,
    amp_alpha: float = 1.0,
    amp_beta: float = 0.4,
    k_alpha: ModeKey | None = None,
    k_beta: ModeKey | None = None,
    phase: float = 0.4,
) -> Field:
    """Two distinct Stokes shells — basic D_s > 0 probe."""
    fa = single_shell_field(alpha=alpha, amp=amp_alpha, k=k_alpha, theta=0.2, phi=0.0)
    fb = single_shell_field(alpha=beta, amp=amp_beta, k=k_beta, theta=0.9, phi=phase)
    out: Dict[ModeKey, np.ndarray] = dict(fa.as_dict())
    for k, v in fb.items():
        out[k] = out.get(k, np.zeros(3, dtype=np.complex128)) + v
    return enforce(Field(out))


def random_shell_field(
    rng: np.random.Generator,
    shells: Sequence[int] = (1, 2, 5),
    modes_per_shell: int = 2,
    amp: float = 1.0,
    kmax: int | None = None,
) -> Field:
    """Random conjugate-closed field on given Stokes shells (polarizations)."""
    out: Dict[ModeKey, np.ndarray] = {}
    for alpha in shells:
        cands = modes_on_shell(int(alpha), kmax=kmax)
        if not cands:
            continue
        rng.shuffle(cands)
        for k in cands[:modes_per_shell]:
            th = float(rng.uniform(0, 2 * np.pi))
            ph = float(rng.uniform(0, 2 * np.pi))
            a = float(amp * rng.uniform(0.3, 1.0))
            out[k] = a * pol_from_angles(k, th, ph)
    return enforce(Field(out))


def high_triad_field(
    amp: float = 1.0,
    k1: ModeKey = (4, 2, 1),
    k2: ModeKey = (-3, 1, 1),
    phases: Tuple[float, float, float] = (0.0, 0.3, -0.2),
    pol_seeds: Tuple[Sequence[float], Sequence[float], Sequence[float]] = (
        (1.0, 0.2, -0.5),
        (0.3, 1.0, 0.1),
        (-0.4, 0.5, 1.0),
    ),
) -> Field:
    """Fixed-shape resonant triad k1+k2+k3=0."""
    k3 = (-k1[0] - k2[0], -k1[1] - k2[1], -k1[2] - k2[2])
    field_map: Dict[ModeKey, np.ndarray] = {}
    for k, phase, seed in zip((k1, k2, k3), phases, pol_seeds):
        v = make_divfree_amp(k, seed)
        nrm = float(np.linalg.norm(v))
        if nrm < 1e-15:
            v = make_divfree_amp(k, (seed[1], seed[2], seed[0]))
            nrm = float(np.linalg.norm(v))
        v = (amp * np.exp(1j * phase) / nrm) * v
        field_map[k] = v
    return enforce(Field(field_map))


# ---------------------------------------------------------------------------
# Closing direction (9B-style) — z ∥ Π_β B(w,w)
# ---------------------------------------------------------------------------


def project_B_to_shell(Buu: Field, beta: float, tol: float = 1e-9) -> Field:
    """Π_β B: keep only modes with |k|^2 = β."""
    out: Dict[ModeKey, np.ndarray] = {}
    for k, v in Buu.items():
        if abs(k_norm2(k) - beta) <= tol:
            out[k] = leray_project(k, np.asarray(v, dtype=np.complex128))
    return enforce(Field(out))


def build_closing_direction(
    w: Field,
    beta: float,
    sign: float | None = None,
    eps_probe: float = 1e-3,
) -> Field:
    """Unit closing packet z_β ∥ Π_β B(w,w) (Attack 9B alignment).

    If ``sign`` is None, choose ± to maximize T_c stretching on w + ε z.
    Returns empty Field if Π_β B vanishes.
    Self-contained: uses only this module's triad / Leray machinery.
    """
    w = enforce(w)
    Buu = nonlinear_B(w)
    PiB = project_B_to_shell(Buu, beta)
    n2 = field_energy(PiB)
    if n2 < 1e-30:
        return Field({})

    def unit(s: float) -> Field:
        n = np.sqrt(n2)
        return Field({k: (s * v / n) for k, v in PiB.items()})

    if sign is None:
        best_s = 1.0
        best_tc = -float("inf")
        for s in (1.0, -1.0):
            z = unit(s)
            v_eps = combine_fields(w, z, eps_probe)
            tc = T_c_from_NM(v_eps)
            if tc > best_tc:
                best_tc = tc
                best_s = s
        sign = best_s
    return unit(float(sign))


def combine_fields(w: Field, z: Field, eps: float) -> Field:
    """v = w + ε z (conjugate-closed)."""
    out: Dict[ModeKey, np.ndarray] = {k: v.copy() for k, v in w.items()}
    for k, zv in z.items():
        out[k] = out.get(k, np.zeros(3, dtype=np.complex128)) + eps * zv
    return enforce(Field(out))


# ---------------------------------------------------------------------------
# CLI smoke
# ---------------------------------------------------------------------------


def _smoke() -> int:
    rng = np.random.default_rng(1390)
    f = two_shell_field(alpha=1, beta=5, amp_alpha=1.0, amp_beta=0.5)
    p = probe_star(f)
    print("two_shell probe:", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in p.items()})
    fr = random_shell_field(rng, shells=(1, 2, 5), modes_per_shell=2)
    pr = probe_star(fr)
    print("random_shell R_star:", pr["R_star"], "D_s_agree:", pr["D_s_agree"])
    w = single_shell_field(alpha=2, amp=1.0)
    z = build_closing_direction(w, beta=5)
    print("closing modes:", len(z), "energy:", field_energy(z))
    print("NS not solved. Lemma★ OPEN. This smoke is not a proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_smoke())
