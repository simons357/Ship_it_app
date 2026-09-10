"""ns_lemma_star_core.py

Self-contained, exact implementation of the canonical Lemma* shape
quantities directly from LEMMA_STAR_SHAPE_FORM.md / LEMMA_STAR_EXACT_FORMULAS.md.

Independent of scripts/ns_attacks/stokes_moments.py. That live Stokes
file is not replaced. This module is a second writing of the same
boxed objects, for cross-check. A match on a sample is not a proof.
NS is not solved. sup R_star remains OPEN.

    A = -P Delta,           lambda_k = |k|^2
    E     = ||v||_2^2       = sum_k |v_k|^2
    X     = ||A^{1/2}v||_2^2 = sum_k lambda_k |v_k|^2
    Y     = ||Av||_2^2       = sum_k lambda_k^2 |v_k|^2
    Z     = ||A^{3/2}v||_2^2 = sum_k lambda_k^3 |v_k|^2
    Lambda = Y / X
    D_s   = Z - Y^2/X = sum_k lambda_k (lambda_k - Lambda)^2 |v_k|^2
    B(v,v)_hat_k = i P_k sum_{p+q=k} (q . v_p) v_q,   P_k = I - k k^T/|k|^2
    T_k   = -Re( B_hat_k . conj(v_k) ) = sum_{p+q=k} Im[(q.v_p)(v_q . conj(v_k))]
    T_c   = sum_k lambda_k (lambda_k - Lambda) T_k
    R_star(v) = (T_c)_+^2 / (D_s * E * Y)

No external Stokes/eigenbasis code is used. A field is a finite set of
Fourier modes on Z^3 \\ {0}, with v_{-k} = conj(v_k) enforced by
construction (never assumed silently) and k . v_k = 0 (divergence-free)
enforced by projection at the point of setting a mode.

Two independent D_s formulas (moment form Z - Y^2/X, and the direct
sum sum_k lambda_k(lambda_k-Lambda)^2|v_k|^2) are cross-checked on
every call to R_star; a mismatch raises, rather than silently returning
a number that might be wrong.

T_c is computed by DIRECT triad summation (exact, no aliasing) --
for each k in the field's support, B_hat_k is computed by summing over
p in support(v), q = k - p, using only terms where q is also in the
support (v_q = 0 elsewhere kills the term). This is exact for any
finite-support field; no FFT/grid truncation is involved.

Engineering locks (same math, not a second claim):
  * scale(a) requires real a. A complex factor breaks v_{-k}=conj(v_k).
  * Shell enumeration uses integer isqrt, not float round(sqrt).
  * T_c is also checked against M - Lambda N when verify=True.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple

import numpy as np

ModeKey = Tuple[int, int, int]


def lam(k) -> float:
    """lambda_k = |k|^2 for integer wavevector k (tuple or array)."""
    k = np.asarray(k, dtype=float)
    return float(np.dot(k, k))


def project_perp(k, w):
    """Project complex 3-vector w onto the plane perpendicular to real k."""
    k = np.asarray(k, dtype=float)
    k2 = float(np.dot(k, k))
    if k2 == 0:
        raise ValueError("k=0 has no perpendicular plane (mean-zero excludes k=0).")
    kw = np.dot(k, w)  # k real, w complex -> complex scalar
    return w - (kw / k2) * k


class Field:
    """
    A finite-support, divergence-free, mean-zero field on T^3.
    Internally stores Fourier coefficients v_k for every k in the
    support (both +k and -k explicitly), with v_{-k} = conj(v_k)
    guaranteed by construction.
    """

    def __init__(self):
        self.modes = {}  # tuple(int,int,int) -> np.array shape (3,), complex

    def set_mode(self, k, w):
        """
        Set v_k = P_k(w) (projected divergence-free), and automatically
        v_{-k} = conj(v_k). k must be a nonzero integer 3-tuple.
        If a mode already exists at k or -k it is overwritten (not added).
        """
        k = tuple(int(x) for x in k)
        if k == (0, 0, 0):
            raise ValueError("mean-zero: cannot set the k=0 mode.")
        w = np.asarray(w, dtype=complex)
        vk = project_perp(k, w)
        self.modes[k] = vk
        nk = tuple(-x for x in k)
        self.modes[nk] = np.conj(vk)

    def add_mode(self, k, w):
        """Like set_mode, but adds to any existing coefficient at k (and -k) instead of overwriting."""
        k = tuple(int(x) for x in k)
        existing = self.modes.get(k, np.zeros(3, dtype=complex))
        w = np.asarray(w, dtype=complex)
        vk_new = project_perp(k, w)
        self.set_mode(k, existing + vk_new)

    def scale(self, a):
        """Return a new Field equal to a * self. a must be real (reality condition)."""
        a = np.asarray(a)
        if abs(float(np.asarray(a).imag)) > 1e-15:
            raise ValueError(
                "scale(a) requires real a. A complex factor breaks v_{-k}=conj(v_k)."
            )
        a = float(np.real(a))
        out = Field()
        for k, vk in self.modes.items():
            out.modes[k] = a * vk
        return out

    def add(self, other):
        """Return a new Field equal to self + other (disjoint or overlapping supports)."""
        out = Field()
        keys = set(self.modes.keys()) | set(other.modes.keys())
        for k in keys:
            out.modes[k] = self.modes.get(k, 0) + other.modes.get(k, 0)
        return out

    def support(self):
        return list(self.modes.keys())

    def get(self, k):
        return self.modes.get(tuple(int(x) for x in k), np.zeros(3, dtype=complex))

    def energy(self):
        """E = sum_k |v_k|^2."""
        return sum(float(np.vdot(vk, vk).real) for vk in self.modes.values())

    def normalize(self, target_E=1.0):
        """Return a new Field scaled so E = target_E."""
        E = self.energy()
        if E <= 0:
            raise ValueError("Cannot normalize a zero field.")
        return self.scale(np.sqrt(target_E / E))


def from_mode_dict(d: Dict[ModeKey, np.ndarray]) -> Field:
    """Build a Field from a live stokes_moments-style dict (k -> C^3)."""
    f = Field()
    seen = set()
    for k, w in d.items():
        k = tuple(int(x) for x in k)
        if k == (0, 0, 0) or k in seen:
            continue
        f.set_mode(k, w)
        seen.add(k)
        seen.add(tuple(-x for x in k))
    return f


def to_mode_dict(field: Field) -> Dict[ModeKey, np.ndarray]:
    """Export modes as a live stokes_moments-style dict."""
    return {k: np.array(v, copy=True) for k, v in field.modes.items()}


def dilate(field: Field, n: int) -> Field:
    """Uniform Fourier dilation v(n·): mode k moves to n k, amplitude unchanged."""
    if int(n) < 1:
        raise ValueError("dilation factor n must be a positive integer.")
    n = int(n)
    out = Field()
    for k, vk in field.modes.items():
        nk = (n * k[0], n * k[1], n * k[2])
        out.modes[nk] = np.array(vk, copy=True)
    return out


def moments(field: Field):
    """Return (E, X, Y, Z, Lambda)."""
    E = X = Y = Z = 0.0
    for k, vk in field.modes.items():
        l = lam(k)
        e = float(np.vdot(vk, vk).real)
        E += e
        X += l * e
        Y += l * l * e
        Z += l * l * l * e
    Lambda = Y / X if X > 0 else 0.0
    return E, X, Y, Z, Lambda


def D_s_moment_form(X, Y, Z):
    return Z - (Y * Y) / X if X > 0 else 0.0


def D_s_direct_form(field: Field, Lambda):
    total = 0.0
    for k, vk in field.modes.items():
        l = lam(k)
        e = float(np.vdot(vk, vk).real)
        total += l * (l - Lambda) ** 2 * e
    return total


def D_s_double_sum(field: Field, X: float) -> float:
    """Third identity: (1/(2X)) sum_{k,ℓ} λ_k λ_ℓ (λ_k-λ_ℓ)^2 |v_k|^2 |v_ℓ|^2."""
    if X <= 0:
        return 0.0
    items = list(field.modes.items())
    total = 0.0
    for k, vk in items:
        lk = lam(k)
        ek = float(np.vdot(vk, vk).real)
        for ell, vl in items:
            ll = lam(ell)
            el = float(np.vdot(vl, vl).real)
            total += lk * ll * (lk - ll) ** 2 * ek * el
    return total / (2.0 * X)


def B_hat_at(field: Field, k):
    """
    B_hat_k = i * P_k * sum_{p+q=k, p in support(v), q in support(v)} (q . v_p) v_q

    Exact direct summation: only pairs (p, q) with BOTH p and q in the
    field's support contribute (v is exactly zero outside its support,
    no truncation/aliasing involved). k need not be in the support.
    """
    k = tuple(int(x) for x in k)
    S = field.modes  # dict k -> vk
    total = np.zeros(3, dtype=complex)
    for p, vp in S.items():
        q = tuple(k[i] - p[i] for i in range(3))
        if q == (0, 0, 0):
            continue
        vq = S.get(q)
        if vq is None:
            continue
        qf = np.array(q, dtype=float)
        qdotvp = np.dot(qf, vp)  # complex scalar
        total += qdotvp * vq
    total = 1j * total
    if k != (0, 0, 0):
        total = project_perp(k, total)
    return total


def T_k_map(field: Field) -> Dict[ModeKey, float]:
    """T_k = -Re(B_hat_k · conj(v_k)) on the support."""
    out: Dict[ModeKey, float] = {}
    for k, vk in field.modes.items():
        Bk = B_hat_at(field, k)
        out[k] = -float(np.real(np.dot(Bk, np.conj(vk))))
    return out


def sum_Tk(field: Field) -> float:
    """Σ_k T_k. Energy identity: this is 0 on mean-zero divergence-free fields."""
    return float(sum(T_k_map(field).values()))


def T_c_direct(field: Field, Lambda):
    """
    T_c = sum_{k in support(v)} lambda_k (lambda_k - Lambda) * T_k,
    T_k = -Re(B_hat_k . conj(v_k)).
    Terms with k outside support(v) vanish automatically (v_k=0 there),
    so summing only over support(v) is exact, not an approximation.
    """
    total = 0.0
    for k, vk in field.modes.items():
        Bk = B_hat_at(field, k)
        Tk = -float(np.real(np.dot(Bk, np.conj(vk))))
        l = lam(k)
        total += l * (l - Lambda) * Tk
    return total


def T_c_from_MN(field: Field, Lambda) -> Tuple[float, float, float]:
    """T_c = M - Lambda N with N = sum λ T_k, M = sum λ^2 T_k."""
    N = M = 0.0
    for k, Tk in T_k_map(field).items():
        l = lam(k)
        N += l * Tk
        M += (l * l) * Tk
    return N, M, M - Lambda * N


def R_star(field: Field, verify=True, tol=1e-6):
    """
    Compute R_star(v) = (T_c)_+^2 / (D_s * E * Y), with the two D_s
    formulas cross-checked (moment form vs direct spectral-sum form).
    Raises RuntimeError if they disagree beyond `tol` relative error --
    this is a correctness guard, not a formality.
    """
    E, X, Y, Z, Lambda = moments(field)
    if X <= 0:
        raise ValueError("X=0: zero or empty field.")

    Ds_m = D_s_moment_form(X, Y, Z)
    Ds_d = D_s_direct_form(field, Lambda)
    if verify:
        # Relative check is meaningless when both sides are cancellation
        # noise (single-shell Ds theoretically 0; Z - Y^2/X loses digits).
        # A true bug (O(1) disagreement) still raises.
        ds_floor = 1e-9 * max(abs(Z), 1.0)
        if abs(Ds_m - Ds_d) > max(tol * max(abs(Ds_m), abs(Ds_d), ds_floor), ds_floor):
            rel_err = abs(Ds_m - Ds_d) / max(abs(Ds_m), abs(Ds_d), 1e-300)
            raise RuntimeError(
                f"D_s cross-check FAILED: moment form={Ds_m!r}, "
                f"direct form={Ds_d!r}, relative error={rel_err!r}. "
                f"Do not trust this R_star value -- there is a bug."
            )
        _N, _M, Tc_mn = T_c_from_MN(field, Lambda)
        Tc_dir = T_c_direct(field, Lambda)
        tc_floor = 1e-10 * max(abs(Y) ** 1.5, 1.0)
        if abs(Tc_mn - Tc_dir) > max(
            tol * max(abs(Tc_mn), abs(Tc_dir), tc_floor), tc_floor
        ):
            raise RuntimeError(
                f"T_c cross-check FAILED: M-Lambda N={Tc_mn!r}, "
                f"direct={Tc_dir!r}. Do not trust this R_star value."
            )
    else:
        Tc_dir = T_c_direct(field, Lambda)

    Tc = Tc_dir
    Tc_plus = max(Tc, 0.0)

    # Spectral sum has no cancellation on a single shell; use it for vacuous.
    if Ds_d <= 1e-14:
        # Single-shell (or numerically single-shell) field: vacuous case.
        return dict(
            E=E,
            X=X,
            Y=Y,
            Z=Z,
            Lambda=Lambda,
            D_s=Ds_d,
            T_c=Tc,
            R_star=(0.0 if Tc_plus == 0.0 else float("inf")),
            vacuous_single_shell=True,
        )

    Rs = (Tc_plus ** 2) / (Ds_d * E * Y)
    return dict(
        E=E,
        X=X,
        Y=Y,
        Z=Z,
        Lambda=Lambda,
        D_s=Ds_d,
        T_c=Tc,
        R_star=Rs,
        vacuous_single_shell=False,
    )


# ---------------------------------------------------------------------------
# Shell generation (pure number theory: sum-of-three-squares lattice points)
# ---------------------------------------------------------------------------


def shell_wavevectors(n, canonical_only=True):
    """
    Integer 3-vectors k with |k|^2 = n (n > 0). If canonical_only, return
    one representative per {k, -k} pair (the one whose first nonzero
    coordinate is positive) -- enough to build a basis of the real
    eigenspace, since v_{-k}=conj(v_k) is automatic in Field.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer (nonzero eigenvalue).")
    n = int(n)
    R = int(math.isqrt(n))
    pts = []
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            rem = n - a * a - b * b
            if rem < 0:
                continue
            c = int(math.isqrt(rem))
            if c * c != rem:
                continue
            pts.append((a, b, c))
            if c != 0:
                pts.append((a, b, -c))
    pts = list(set(pts))
    pts = [p for p in pts if p != (0, 0, 0)]
    if not canonical_only:
        return pts

    seen = set()
    out = []
    for p in pts:
        if p in seen:
            continue
        neg = tuple(-x for x in p)
        seen.add(p)
        seen.add(neg)
        # canonical: first nonzero coordinate positive
        for coord in p:
            if coord != 0:
                out.append(p if coord > 0 else neg)
                break
    return out


def random_shell_field(n, rng, target_E=1.0):
    """
    Sample a random field supported on shell n (|k|^2=n), with each
    canonical k assigned an isotropic complex-Gaussian vector in the
    2D plane perpendicular to k, then normalized to energy target_E.
    This is a reasonable (not claimed-uniform) sampling distribution
    over the eigenspace, suitable for Monte-Carlo maximization of R_star.
    """
    reps = shell_wavevectors(n)
    if not reps:
        raise ValueError(f"No lattice points with |k|^2={n} (not a sum of three squares).")
    f = Field()
    for k in reps:
        kf = np.array(k, dtype=float)
        # build 2 real orthonormal vectors spanning the plane perp to k
        a = np.array([1.0, 0.0, 0.0])
        if abs(np.dot(a, kf)) > 0.9 * np.linalg.norm(kf):
            a = np.array([0.0, 1.0, 0.0])
        e1 = a - (np.dot(a, kf) / np.dot(kf, kf)) * kf
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(kf, e1)
        e2 /= np.linalg.norm(e2)
        c1 = rng.normal() + 1j * rng.normal()
        c2 = rng.normal() + 1j * rng.normal()
        w = c1 * e1 + c2 * e2
        f.set_mode(k, w)
    return f.normalize(target_E)


def build_closing_direction(w_field: Field, beta):
    """
    Build z_beta proportional to Pi_beta B(w,w): for every k on shell
    beta, evaluate B_hat_k(w,w) directly (exact triad sum, w's support
    only), assemble as a Field on shell beta, normalize to unit energy.
    Returns (z_beta_field, raw_norm) where raw_norm = ||Pi_beta B(w,w)||_2
    before normalization (needed for the closed-form K comparison).

    The displayed R_star → K limit holds only for this aligned closer
    (sign-selected so (T_c)_+ > 0). A misaligned z_beta sees the
    squared projection against B(w,w), not K.
    """
    beta_ks = shell_wavevectors(beta)
    z = Field()
    for k in beta_ks:
        Bk = B_hat_at(w_field, k)
        z.set_mode(k, Bk)
    raw_norm_sq = z.energy()
    if raw_norm_sq <= 0:
        return None, 0.0
    return z.normalize(1.0), float(np.sqrt(raw_norm_sq))


def K_of_w(w_field: Field, alpha: float, beta: float) -> dict:
    """K_{α,β}(w) = β ||Π_β B(w,w)||_2^2 / (α^2 ||w||_2^4). Restricted family. Not ★."""
    _z, raw = build_closing_direction(w_field, beta)
    e = w_field.energy()
    denom = (alpha ** 2) * (e ** 2)
    K = (beta * (raw ** 2) / denom) if denom > 0 else float("nan")
    return {
        "K": float(K),
        "PiB_L2": float(raw),
        "E_w": float(e),
        "alpha": float(alpha),
        "beta": float(beta),
    }
