"""Stokes-moment / centered-drift calculus on T^3 Fourier Galerkin fields.

Truth-only numerics for Lemma★ / Route N spectral drift attacks.
Does NOT claim a proof. NS is not solved. Kill lane LIVE.

Exact lock (see docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md):

  T^3 = (R/2πZ)^3
  v(x) = sum_{k≠0} v_k e^{ik·x},  k·v_k=0,  v_{-k}=conj(v_k)
  λ_k = |k|^2,  A = -PΔ,  (Av)_k = λ_k v_k
  B(v,v) = P[(v·∇)v]

  ||v||_2^2 = sum |v_k|^2           (code alias: E)
  X = ||A^{1/2}v||_2^2 = sum λ_k |v_k|^2
  Y = ||Av||_2^2       = sum λ_k^2 |v_k|^2
  Z = ||A^{3/2}v||_2^2 = sum λ_k^3 |v_k|^2
  Λ = Y/X

  Ds = Z − Y^2/X = Z − Λ Y = ||(A−Λ) A^{1/2} v||_2^2
     = sum λ_k (λ_k−Λ)^2 |v_k|^2
     = (1/(2X)) sum_{k,ℓ} λ_k λ_ℓ (λ_k−λ_ℓ)^2 |v_k|^2 |v_ℓ|^2
  (SoT writes D_s; older docs may write script D_s = mathcal{D}_s — same object.)
  Two shells α,β with energies e_α,e_β:
     Ds = α β (α−β)^2 e_α e_β / (α e_α + β e_β)

  B̂_k = i P_k sum_{p+q=k} (q·v_p) v_q ,  P_k = I − k⊗k/|k|^2
  T_k = −Re(B̂_k · conj(v_k)) = sum_{p+q=k} Im[(q·v_p)(v_q·conj(v_k))]
        (SIGNED Im — never abs)
  N = −⟨B,Av⟩ = sum λ_k T_k
  M = −⟨AB,Av⟩ = sum λ_k^2 T_k
  Tc = −⟨B(v,v), A(A−Λ)v⟩ = M − Λ N = sum λ_k (λ_k−Λ) T_k
     = sum_{p+q=k} λ_k (λ_k−Λ) Im[(q·v_p)(v_q·conj(v_k))]
  (code: Tc = M - Lam * N — matches the inner-product SoT form)

  Sign check: Λ' = 2/X (Tc − ν Ds)

  R_★(v) = (Tc)_+^2 / (Ds · ||v||_2^2 · Y)   (amp-, dilation-, and ν-invariant)
  where (Tc)_+ = max(Tc, 0). When Tc ≥ 0, (Tc)_+^2 = Tc^2.
  For kill we care about stretching Tc > 0.

  CANONICAL quotient code name: ratio_R_star_shape  (= R_★)
  Alias:                       ratio_R_star         → same as ratio_R_star_shape
  LEGACY (different object):   ratio_star           = Tc / (E X Λ)  post-Young
                               (scales as 1/a on fixed shape; NOT R_★)

Lemma★ — FULL exact shape form (OPEN; NS not solved):
  ∃ C_geom < ∞  ∀ v ∈ C^∞_{div,0}(T^3)\\{0}:
    (Tc(v)_+)^2 ≤ C_geom · Ds(v) · ||v||_2^2 · Y(v)
  Equiv. (Ds>0): sup (Tc_+)^2 / (Ds ||v||_2^2 Y) < ∞
  For Ds=0: one shell and Tc=0.
  Viscosity packaging (0<θ<1):
    Tc ≤ θ ν Ds + C_0(θ) ν^{-1} ||u||_2^2 Y,   C_geom = 4 θ C_0(θ)
  Near-shell K_{α,β} is ONLY a restricted limiting-family probe — NOT the full lemma.

Kill criteria (shape): R_★ → ∞ on a family; or Ds=0 with Tc>0.
Failure to find a numerical counterexample does NOT close the kill lane —
falsification and proof both remain LIVE.
Pure single shell (Tc=0=Ds) is vacuous. Live attempt: almost-single-shell /
coherent packet growth (Attack 9); 9B K_{α,β} restricted family only.
HH→L can identify mechanism; only complete signed Tc kills ★.
Amplitude and uniform Fourier dilation leave R_★ exactly invariant
(do NOT claim they make the ratio smaller — that was an older non-optimized budget).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

ModeKey = Tuple[int, int, int]
Field = Dict[ModeKey, np.ndarray]  # k -> complex amplitude in C^3


def k_norm2(k: ModeKey) -> float:
    return float(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])


def leray_project(k: ModeKey, v: np.ndarray) -> np.ndarray:
    """P_k v = v − (k·v) k / |k|^2 for k≠0; zero at k=0."""
    kn2 = k_norm2(k)
    if kn2 == 0:
        return np.zeros(3, dtype=np.complex128)
    kk = np.array(k, dtype=np.float64)
    return v - (np.dot(kk, v) / kn2) * kk


def enforce_reality(field: Field) -> Field:
    """Ensure û(-k) = conjugate(û(k)); drop k=0."""
    out: Field = {}
    for k, v in field.items():
        if k == (0, 0, 0):
            continue
        mk = (-k[0], -k[1], -k[2])
        proj = leray_project(k, np.asarray(v, dtype=np.complex128))
        if k in out:
            continue
        if mk == k:
            # self-conjugate mode: force real after projection into plane
            out[k] = np.real(proj).astype(np.complex128)
        else:
            out[k] = proj
            out[mk] = np.conjugate(proj)
    return out


def scale_field(field: Field, B: float) -> Field:
    return {k: B * v for k, v in field.items()}


def dilate_field(field: Field, n: int) -> Field:
    """Uniform Fourier dilation: mode k ↦ mode n·k with the same amplitude.

    Exact shape★ identity: R_★(v(n·)) = R_★(v) for integer n ≠ 0
    (λ scales by n²; T_c, D_s, Y, ||v||₂² scale homogeneously so the quotient cancels).
    """
    if n == 0:
        raise ValueError("dilation factor n must be nonzero")
    out: Field = {}
    for k, v in field.items():
        nk = (n * k[0], n * k[1], n * k[2])
        out[nk] = np.asarray(v, dtype=np.complex128).copy()
    return enforce_reality(out)


def sum_Tk(field: Field) -> float:
    """Σ_k T_k. For the NS triad nonlinearity on mean-zero fields this vanishes
    (energy conservation of the bilinear form): Σ T_k = 0."""
    Tk = triad_Im_transfer(field)
    return float(sum(Tk.values()))


def nonlinear_B_fft_dealiased(field: Field, n_grid: int | None = None) -> Field:
    """Dealiased FFT evaluation of B(v,v)=P[(v·∇)v] on a periodic grid.

    Mathematical Fourier convention: v(x)=Σ v_k e^{ik·x}. Uses 2/3-rule dealiasing.
    For Galerkin control: Tc from this B̂ must agree with direct triad summation on
    the occupied modes of a band-limited field.
    """
    if not field:
        return {}
    kmax = max(max(abs(c) for c in k) for k in field)
    need = max(8, 3 * kmax + 2)
    if n_grid is None:
        n_grid = 2
        while n_grid < 2 * need:
            n_grid *= 2
    N = int(n_grid)
    # Store mathematical Fourier coefficients in FFT arrays
    vx = np.zeros((N, N, N), dtype=np.complex128)
    vy = np.zeros((N, N, N), dtype=np.complex128)
    vz = np.zeros((N, N, N), dtype=np.complex128)
    for (kx, ky, kz), v in field.items():
        if abs(kx) >= N // 2 or abs(ky) >= N // 2 or abs(kz) >= N // 2:
            continue
        ix, iy, iz = kx % N, ky % N, kz % N
        vx[ix, iy, iz] = v[0]
        vy[ix, iy, iz] = v[1]
        vz[ix, iy, iz] = v[2]
    # Physical fields: u = Σ û e^{ikx} = N³ ifftn(û)
    scale = float(N) ** 3
    ux = np.fft.ifftn(vx) * scale
    uy = np.fft.ifftn(vy) * scale
    uz = np.fft.ifftn(vz) * scale
    kx = np.fft.fftfreq(N) * N
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij")

    def phys_deriv(uhat, Kj):
        return np.fft.ifftn(1j * Kj * uhat) * scale

    dx_ux, dy_ux, dz_ux = phys_deriv(vx, KX), phys_deriv(vx, KY), phys_deriv(vx, KZ)
    dx_uy, dy_uy, dz_uy = phys_deriv(vy, KX), phys_deriv(vy, KY), phys_deriv(vy, KZ)
    dx_uz, dy_uz, dz_uz = phys_deriv(vz, KX), phys_deriv(vz, KY), phys_deriv(vz, KZ)
    nx = ux * dx_ux + uy * dy_ux + uz * dz_ux
    ny = ux * dx_uy + uy * dy_uy + uz * dz_uy
    nz = ux * dx_uz + uy * dy_uz + uz * dz_uz
    # Forward FFT: û = fftn(u) / N³
    Bx = np.fft.fftn(nx) / scale
    By = np.fft.fftn(ny) / scale
    Bz = np.fft.fftn(nz) / scale
    # 2/3-rule dealias
    cut = N // 3
    kx_i = np.where(np.arange(N) <= N // 2, np.arange(N), np.arange(N) - N)
    KXi, KYi, KZi = np.meshgrid(kx_i, kx_i, kx_i, indexing="ij")
    mask = np.maximum(np.maximum(np.abs(KXi), np.abs(KYi)), np.abs(KZi)) > cut
    Bx[mask] = 0
    By[mask] = 0
    Bz[mask] = 0
    out: Field = {}
    mode_set = set(field.keys())
    keys = list(field.keys())
    for p in keys:
        for q in keys:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k != (0, 0, 0):
                mode_set.add(k)
    for k in mode_set:
        kx_, ky_, kz_ = k
        if max(abs(kx_), abs(ky_), abs(kz_)) > cut:
            continue
        if abs(kx_) >= N // 2 or abs(ky_) >= N // 2 or abs(kz_) >= N // 2:
            continue
        ix, iy, iz = kx_ % N, ky_ % N, kz_ % N
        raw = np.array([Bx[ix, iy, iz], By[ix, iy, iz], Bz[ix, iy, iz]], dtype=np.complex128)
        out[k] = leray_project(k, raw)
    return out


def Tc_from_B_field(field: Field, Buu: Field, Lambda: float | None = None) -> float:
    """Complete signed Tc = −⟨B, A(A−Λ)v⟩ from a precomputed B̂ (triad or FFT).

    Equivalent to M − Λ N with N=−⟨B,Av⟩, M=−⟨AB,Av⟩ (see module docstring / SoT).
    """
    if Lambda is None:
        Lambda = moments(field)["Lambda"]
    Tc = 0.0
    for k, vk in field.items():
        lam = k_norm2(k)
        if lam == 0:
            continue
        bk = Buu.get(k, np.zeros(3, dtype=np.complex128))
        Tk = -float(np.dot(bk, np.conjugate(vk)).real)
        Tc += lam * (lam - Lambda) * Tk
    return Tc


def moments(field: Field) -> Dict[str, float]:
    """Linear Stokes moments. E := ||v||_2^2 = sum |v_k|^2.

    Ds := D_s = Z − Y^2/X = Z − Λ Y = ||(A−Λ) A^{1/2} v||_2^2
    (SoT D_s; older docs may write mathcal{D}_s — same object).
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
        "Ds_over_X": Ds / X if X > 0 else float("nan"),
    }


def Ds_variance_sum(field: Field, Lambda: float | None = None) -> float:
    """Ds = sum_k λ_k (λ_k − Λ)^2 |v_k|^2."""
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


def Ds_double_sum(field: Field) -> float:
    """Ds = (1/(2X)) sum_{k,ℓ} λ_k λ_ℓ (λ_k−λ_ℓ)^2 |v_k|^2 |v_ℓ|^2."""
    modes = [(k_norm2(k), float(np.vdot(v, v).real)) for k, v in field.items() if k_norm2(k) > 0]
    X = sum(lam * e for lam, e in modes)
    if X <= 0:
        return float("nan")
    acc = 0.0
    for lam_k, ek in modes:
        for lam_l, el in modes:
            acc += lam_k * lam_l * (lam_k - lam_l) ** 2 * ek * el
    return acc / (2.0 * X)


def Ds_two_shell(alpha: float, beta: float, e_alpha: float, e_beta: float) -> float:
    """Two-eigenvalue closed form: αβ(α−β)^2 e_α e_β / (α e_α + β e_β)."""
    denom = alpha * e_alpha + beta * e_beta
    if denom <= 0:
        return float("nan")
    return (alpha * beta * (alpha - beta) ** 2 * e_alpha * e_beta) / denom


def shell_energies(field: Field) -> Dict[float, float]:
    """Map λ = |k|^2 → e_λ = sum_{|k|^2=λ} |v_k|^2."""
    shells: Dict[float, float] = {}
    for k, v in field.items():
        lam = k_norm2(k)
        if lam == 0:
            continue
        shells[lam] = shells.get(lam, 0.0) + float(np.vdot(v, v).real)
    return shells


def nonlinear_B(field: Field) -> Field:
    """B(v,v)=P[(v·∇)v]: B̂_k = i P_k sum_{p+q=k} (q·v_p) v_q."""
    keys = list(field.keys())
    raw: Field = {}
    for p in keys:
        up = field[p]
        for q in keys:
            uq = field[q]
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            # (q · v_p) with q real — same as (v_p · q)
            q_vec = np.array(q, dtype=np.float64)
            coeff = 1j * np.dot(q_vec, up)
            contrib = coeff * uq
            raw[k] = raw.get(k, np.zeros(3, dtype=np.complex128)) + contrib
    out: Field = {}
    for k, v in raw.items():
        out[k] = leray_project(k, v)
    return out


def triad_Im_transfer(field: Field) -> Dict[ModeKey, float]:
    """T_k = sum_{p+q=k} Im[(q·v_p)(v_q · conj(v_k))]  (signed; no abs).

    Equivalent to −Re(B̂_k · conj(v_k)) with Leray-projected B̂.
    """
    Buu = nonlinear_B(field)
    Tk: Dict[ModeKey, float] = {}
    for k, vk in field.items():
        if k_norm2(k) == 0:
            continue
        bk = Buu.get(k, np.zeros(3, dtype=np.complex128))
        # −Re(B̂_k · conj(v_k)) = −Re(⟨B̂_k, v_k⟩) with ⟨a,b⟩=a·conj(b)? 
        # With Euclidean: B̂·conj(v) = sum_j B_j conj(v_j) = ⟨v, B⟩ in numpy vdot(B,v)? 
        # np.vdot(bk, vk) = sum conj(bk_i)*vk_i, so Re(B̂·conj(v)) = Re(sum B_i conj(v_i))
        # = Re(sum conj(conj(B_i) v_i)) = Re(conj(np.vdot(bk, vk))) = Re(np.vdot(vk, bk))
        # Simpler: Re(B̂ · conj(v)) = Re(np.dot(bk, np.conjugate(vk)))
        Tk[k] = -float(np.dot(bk, np.conjugate(vk)).real)
    return Tk


def Tc_from_triads(field: Field, Lambda: float | None = None) -> float:
    """Complete signed Tc = sum_{p+q=k} λ_k(λ_k−Λ) Im[(q·v_p)(v_q·conj(v_k))]."""
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
            # After Leray: Im term matches −Re(B̂·conj(v)) only with projected B.
            # Direct Im[(q·vp)(vq·conj(vk))] is the pre-projection triad; for
            # divergence-free fields P_k^* v_k = v_k so the projected form agrees
            # when summed against v_k. Use projected contribution for exact match.
            coeff = 1j * np.dot(q_vec, vp)
            raw = coeff * vq
            bk_contrib = leray_project(k, raw)
            tk_piece = -float(np.dot(bk_contrib, np.conjugate(vk)).real)
            Tc += lam * (lam - Lambda) * tk_piece
    return Tc


def N_and_M(field: Field) -> Tuple[float, float, Field]:
    """Return N, M, B(v,v) with
    N = −⟨B, A v⟩ = sum λ_k T_k
    M = −⟨AB, A v⟩ = sum λ_k^2 T_k
    where T_k = −Re(B̂_k · conj(v_k)).
    """
    Buu = nonlinear_B(field)
    N = 0.0 + 0.0j
    M = 0.0 + 0.0j
    keys = set(field) | set(Buu)
    for k in keys:
        kn2 = k_norm2(k)
        if kn2 == 0:
            continue
        uk = field.get(k, np.zeros(3, dtype=np.complex128))
        bk = Buu.get(k, np.zeros(3, dtype=np.complex128))
        # T_k = −Re(B̂·conj(u)); N = sum λ T_k
        Tk = -np.dot(bk, np.conjugate(uk))
        N += kn2 * Tk
        M += (kn2 * kn2) * Tk
    return float(N.real), float(M.real), Buu


def Lambda_prime_rhs(Tc: float, Ds: float, X: float, nu: float) -> float:
    """Λ' = 2/X (Tc − ν Ds)."""
    if X <= 0:
        return float("nan")
    return (2.0 / X) * (Tc - nu * Ds)


def Lambda_prime_from_XY(N: float, M: float, X: float, Y: float, Z: float, nu: float) -> float:
    """Λ' from X'=-2νY+2N, Y'=-2νZ+2M (sign convention identity)."""
    if X <= 0:
        return float("nan")
    Xp = -2.0 * nu * Y + 2.0 * N
    Yp = -2.0 * nu * Z + 2.0 * M
    return (Yp * X - Y * Xp) / (X * X)


@dataclass
class ProbeResult:
    E: float  # ||v||_2^2
    X: float
    Y: float
    Z: float
    Lambda: float
    Ds: float
    N: float
    M: float
    Tc: float
    # Post-Young viscosity packaging: Tc / (E X Λ) — scales as 1/a on fixed shape.
    # LEGACY name ratio_star — DIFFERENT from canonical R_★ (do not confuse).
    ratio_star: float
    # Pre-Young geometric ratio: Tc / (√E · X · Λ) — amplitude-invariant
    ratio_preyoung: float
    # Survivor C* form: Tc / (X^{3/2} Λ) — amplitude-invariant
    ratio_cstar: float
    # K=0 form: Tc / Ds  (blows ~B with amplitude)
    ratio_k0: float
    # CANONICAL shape★ quotient R_★ = (Tc)_+^2 / (Ds E Y) — amp-/dilation-/ν-invariant.
    # Code name: ratio_R_star_shape. Alias property ratio_R_star → same.
    # NOT the same as legacy ratio_star above.
    ratio_R_star_shape: float
    B_L2: float
    label: str = ""

    @property
    def Tc_plus(self) -> float:
        """Positive part (Tc)_+ = max(Tc, 0)."""
        return max(self.Tc, 0.0)

    @property
    def ratio_R_star(self) -> float:
        """Alias for complete quotient R_★ = (Tc)_+^2 / (Ds ||v||_2^2 Y)."""
        return self.ratio_R_star_shape


def probe(field: Field, label: str = "") -> ProbeResult:
    field = enforce_reality(field)
    m = moments(field)
    N, M, Buu = N_and_M(field)
    Lam = m["Lambda"]
    Tc = M - Lam * N
    Tc_plus = max(Tc, 0.0)
    E, X, Ds = m["E"], m["X"], m["Ds"]
    B_L2 = 0.0
    for v in Buu.values():
        B_L2 += float(np.vdot(v, v).real)
    B_L2 = np.sqrt(max(B_L2, 0.0))
    Y = m["Y"]
    denom_star = E * X * Lam if E > 0 and X > 0 and Lam > 0 else float("nan")
    denom_pre = (np.sqrt(E) * X * Lam) if E > 0 and X > 0 and Lam > 0 else float("nan")
    denom_cstar = (X ** 1.5) * Lam if X > 0 and Lam > 0 else float("nan")
    # Shape★: (Tc)_+^2 / (Ds ||v||_2^2 Y); XΛ = Y
    # When Tc ≥ 0, (Tc)_+^2 = Tc^2. Kill cares about stretching Tc > 0.
    denom_R_star_shape = Ds * E * Y if E > 0 and Y > 0 and Ds > 1e-30 else float("nan")

    def div(num: float, den: float) -> float:
        return num / den if den and den == den and abs(den) > 0 else float("nan")

    return ProbeResult(
        E=E,
        X=X,
        Y=Y,
        Z=m["Z"],
        Lambda=Lam,
        Ds=Ds,
        N=N,
        M=M,
        Tc=Tc,
        ratio_star=div(Tc, denom_star),
        ratio_preyoung=div(Tc, denom_pre),
        ratio_cstar=div(Tc, denom_cstar),
        ratio_k0=div(Tc, Ds) if Ds > 1e-30 else float("nan"),
        ratio_R_star_shape=div(Tc_plus * Tc_plus, denom_R_star_shape),
        B_L2=B_L2,
        label=label,
    )


def make_divfree_amp(k: ModeKey, seed_vec: Sequence[float]) -> np.ndarray:
    """Project a real seed vector to the divergence-free plane at k."""
    v = np.array(seed_vec, dtype=np.complex128)
    return leray_project(k, v)


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
    """Fixed-shape resonant triad k1+k2+k3=0 with amplitude amp on each pair."""
    k3 = (-k1[0] - k2[0], -k1[1] - k2[1], -k1[2] - k2[2])
    assert k1[0] + k2[0] + k3[0] == 0
    assert k1[1] + k2[1] + k3[1] == 0
    assert k1[2] + k2[2] + k3[2] == 0
    field: Field = {}
    for k, phase, seed in zip((k1, k2, k3), phases, pol_seeds):
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            # try alternate seed
            v = make_divfree_amp(k, (seed[1], seed[2], seed[0]))
            nrm = np.linalg.norm(v)
        v = (amp * np.exp(1j * phase) / nrm) * v
        field[k] = v
    return enforce_reality(field)


def random_field(
    rng: np.random.Generator,
    kmax: int = 4,
    n_modes: int = 12,
    amp: float = 1.0,
) -> Field:
    """Random real divergence-free field with modes in [-kmax,kmax]^3 \\ {0}."""
    candidates = [
        (i, j, k)
        for i in range(-kmax, kmax + 1)
        for j in range(-kmax, kmax + 1)
        for k in range(-kmax, kmax + 1)
        if (i, j, k) != (0, 0, 0) and (i > 0 or (i == 0 and j > 0) or (i == 0 and j == 0 and k > 0))
    ]
    rng.shuffle(candidates)
    chosen = candidates[:n_modes]
    field: Field = {}
    for k in chosen:
        seed = rng.normal(size=3)
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            continue
        phase = rng.uniform(0, 2 * np.pi)
        field[k] = (amp * np.exp(1j * phase) / nrm) * v * rng.uniform(0.3, 1.0)
    return enforce_reality(field)


def two_shell_field(
    amp_low: float,
    amp_high: float,
    k_low: ModeKey = (1, 0, 0),
    k_high: ModeKey = (8, 3, 2),
    phase: float = 0.4,
) -> Field:
    """Low + high shell pair for HH→L / scale-separation probes."""
    field: Field = {}
    for k, amp, ph in ((k_low, amp_low, 0.0), (k_high, amp_high, phase)):
        v = make_divfree_amp(k, (1.0, 0.3, -0.7))
        nrm = np.linalg.norm(v)
        field[k] = (amp * np.exp(1j * ph) / nrm) * v
    return enforce_reality(field)


def bony_channel_split(field: Field, k_cut: float) -> Dict[str, float]:
    """Split ⟨B, A u⟩-type transfer into HH, HL, LL by wavevector size of parents.

    For each triad contribution to B at k = p+q, classify by (|p|,|q|) vs k_cut.
    Returns absolute contributions to the N-inner-product sum |k|^2 ⟨B_k, u_k⟩
    partitioned by channel (signed sums).
    """
    keys = list(field.keys())
    channels = {"HH": 0.0 + 0.0j, "HL": 0.0 + 0.0j, "LL": 0.0 + 0.0j, "other": 0.0 + 0.0j}
    # Build B by channel
    B_chan: Dict[str, Field] = {c: {} for c in channels}

    def add(ch: str, k: ModeKey, vec: np.ndarray) -> None:
        B_chan[ch][k] = B_chan[ch].get(k, np.zeros(3, dtype=np.complex128)) + vec

    for p in keys:
        up = field[p]
        pn = np.sqrt(k_norm2(p))
        for q in keys:
            uq = field[q]
            qn = np.sqrt(k_norm2(q))
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            coeff = 1j * np.dot(np.array(q, dtype=np.float64), up)
            contrib = leray_project(k, coeff * uq)
            if pn >= k_cut and qn >= k_cut:
                ch = "HH"
            elif pn >= k_cut or qn >= k_cut:
                ch = "HL"
            else:
                ch = "LL"
            add(ch, k, contrib)

    for ch, Bf in B_chan.items():
        s = 0.0 + 0.0j
        for k, bk in Bf.items():
            kn2 = k_norm2(k)
            if kn2 == 0:
                continue
            uk = field.get(k, np.zeros(3, dtype=np.complex128))
            # contribution to N = −⟨B,Au⟩ and to M via |k|^2 / |k|^4 weights later
            s += kn2 * np.vdot(bk, uk)
        channels[ch] = -s  # match N sign
    return {c: float(v.real) if isinstance(v, complex) else float(v) for c, v in channels.items()}


def format_probe(r: ProbeResult) -> str:
    return (
        f"{r.label:28s} E={r.E:.4e} X={r.X:.4e} Λ={r.Lambda:.4f} Ds={r.Ds:.4e} "
        f"Tc={r.Tc:.4e} Rshape={r.ratio_R_star_shape:.4e} Rpost={r.ratio_star:.4e} "
        f"Rpre={r.ratio_preyoung:.4e} Rc*={r.ratio_cstar:.4e} Rk0={r.ratio_k0:.4e}"
    )


def almost_single_shell_field(
    rng: np.random.Generator,
    k_main: ModeKey = (3, 1, 0),
    n_pert: int = 3,
    eps: float = 1e-3,
    kmax_pert: int = 6,
) -> Field:
    """Nearly one Fourier shell + small multi-mode perturbation (live ★ kill attempt).

    Pure single shell: Ds=0 and typically Tc=0 (vacuous). Live kill needs Ds→0+ with
    stretching that keeps R_star_shape = Tc^2/(Ds E Y) from staying bounded.
    """
    field: Field = {}
    v = make_divfree_amp(k_main, (1.0, 0.2, -0.5))
    nrm = np.linalg.norm(v)
    if nrm < 1e-15:
        v = make_divfree_amp(k_main, (0.0, 1.0, 0.0))
        nrm = np.linalg.norm(v)
    field[k_main] = v / nrm

    candidates = [
        (i, j, k)
        for i in range(-kmax_pert, kmax_pert + 1)
        for j in range(-kmax_pert, kmax_pert + 1)
        for k in range(-kmax_pert, kmax_pert + 1)
        if (i, j, k) != (0, 0, 0)
        and (i, j, k) != k_main
        and (i, j, k) != (-k_main[0], -k_main[1], -k_main[2])
        and (i > 0 or (i == 0 and j > 0) or (i == 0 and j == 0 and k > 0))
    ]
    rng.shuffle(candidates)
    for k in candidates[:n_pert]:
        vp = make_divfree_amp(k, rng.normal(size=3))
        n = np.linalg.norm(vp)
        if n < 1e-15:
            continue
        phase = rng.uniform(0, 2 * np.pi)
        field[k] = (eps * np.exp(1j * phase) / n) * vp
    return enforce_reality(field)
