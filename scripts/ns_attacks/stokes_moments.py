"""Stokes-moment / centered-drift calculus on T^3 Fourier Galerkin fields.

Truth-only numerics for Lemma★ / Route N spectral drift attacks.
Does NOT claim a proof. NS is not solved.

Notation (Foias–Temam / Constantin–Foias style on T^3):
  E = ||u||_2^2
  X = ||A^{1/2} u||_2^2 = sum |k|^2 |û(k)|^2
  Y = ||A u||_2^2       = sum |k|^4 |û(k)|^2
  Z = ||A^{3/2} u||_2^2 = sum |k|^6 |û(k)|^2
  Λ = Y/X
  Ds = Z − Λ Y = X · Var_μ(|k|^2) ≥ 0
  B(u,u) = P((u·∇)u)
  N = −⟨B(u,u), A u⟩
  M = −⟨A B(u,u), A u⟩   (= −⟨B(u,u), A^2 u⟩ by self-adjointness of A)
  Tc = M − Λ N

Lemma★ (energy remainder; OPEN):
  Tc ≤ θ ν Ds + C0 ν^{-1} E X Λ
with C0 geometric only (independent of amplitude / viscosity scale).

Survivor bound from Attack 2 (K=0 killed; NOT Lemma★):
  Tc ≤ θ ν Ds + C* X^{3/2} Λ
That C* is not the trilinear C_star in
  [Tc]_+ ≤ C_star ||v||_2 ||Av||_2 ||(A-Λ)A^{1/2} v||_2
  with C_star^2 = 4 θ C0. The latter is the exact ★ form.
  ratio_box is (Tc_+)^2 / (Ds E Y) = R_star.
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


def moments(field: Field) -> Dict[str, float]:
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


def nonlinear_B(field: Field) -> Field:
    """B(u,u) = P((u·∇)u) in Fourier: i sum_{p+q=k} (û(p)·q) û(q), then Leray."""
    keys = list(field.keys())
    raw: Field = {}
    for p in keys:
        up = field[p]
        for q in keys:
            uq = field[q]
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            # (u·∇) contribution: i (û(p)·q) û(q)
            coeff = 1j * np.dot(up, np.array(q, dtype=np.float64))
            contrib = coeff * uq
            raw[k] = raw.get(k, np.zeros(3, dtype=np.complex128)) + contrib
    out: Field = {}
    for k, v in raw.items():
        out[k] = leray_project(k, v)
    return out


def N_and_M(field: Field) -> Tuple[float, float, Field]:
    """Return N, M, B(u,u) with
    N = −⟨B, A u⟩ = − sum |k|^2 ⟨B_k, û_k⟩
    M = −⟨B, A^2 u⟩ = − sum |k|^4 ⟨B_k, û_k⟩
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
        ip = np.vdot(bk, uk)
        N -= kn2 * ip
        M -= (kn2 * kn2) * ip
    return float(N.real), float(M.real), Buu


@dataclass
class ProbeResult:
    E: float
    X: float
    Y: float
    Z: float
    Lambda: float
    Ds: float
    N: float
    M: float
    Tc: float
    # Post-Young Lemma★ ratio: Tc / (E X Λ) — scales as 1/B on fixed shape (degree 3/4)
    ratio_star: float
    # Pre-Young geometric ratio: Tc / (√E · X · Λ) — amplitude-invariant; true C0 candidate
    ratio_preyoung: float
    # Survivor C* form: Tc / (X^{3/2} Λ) — amplitude-invariant
    ratio_cstar: float
    # K=0 form: Tc / Ds  (blows ~B with amplitude)
    ratio_k0: float
    # Exact ★ reduction: (Tc_+)^2 / (Ds E Y). Amplitude-invariant. Decisive.
    ratio_box: float
    B_L2: float
    label: str = ""


def probe(field: Field, label: str = "") -> ProbeResult:
    field = enforce_reality(field)
    m = moments(field)
    N, M, Buu = N_and_M(field)
    Lam = m["Lambda"]
    Tc = M - Lam * N
    E, X, Ds = m["E"], m["X"], m["Ds"]
    B_L2 = 0.0
    for v in Buu.values():
        B_L2 += float(np.vdot(v, v).real)
    B_L2 = np.sqrt(max(B_L2, 0.0))
    denom_star = E * X * Lam if E > 0 and X > 0 and Lam > 0 else float("nan")
    denom_pre = (np.sqrt(E) * X * Lam) if E > 0 and X > 0 and Lam > 0 else float("nan")
    denom_cstar = (X ** 1.5) * Lam if X > 0 and Lam > 0 else float("nan")
    Y = m["Y"]
    tc_plus = max(Tc, 0.0)
    denom_box = Ds * E * Y if Ds > 0 and E > 0 and Y > 0 else float("nan")

    def div(num: float, den: float) -> float:
        return num / den if den and den == den and abs(den) > 0 else float("nan")

    return ProbeResult(
        E=E,
        X=X,
        Y=m["Y"],
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
        ratio_box=div(tc_plus ** 2, denom_box),
        B_L2=B_L2,
        label=label,
    )


def make_divfree_amp(k: ModeKey, seed_vec: Sequence[float]) -> np.ndarray:
    """Project a real seed vector to the divergence-free plane at k."""
    v = np.array(seed_vec, dtype=np.complex128)
    return leray_project(k, v)


def add_modes(a: ModeKey, b: ModeKey) -> ModeKey:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def three_shell_keys(k0: ModeKey, e: ModeKey) -> Tuple[ModeKey, ModeKey, ModeKey]:
    """Closing triad: k0 + (k0+e) = 2k0+e."""
    k1 = add_modes(k0, e)
    k2 = add_modes(add_modes(k0, k0), e)
    return k0, k1, k2


def three_shell_field(
    k0: ModeKey,
    e: ModeKey,
    amp0: float = 1.0,
    amp1: float = 0.2,
    amp2: float = 0.2,
    phases: Tuple[float, float, float] = (0.0, 0.3, -0.2),
    pol_seeds: Tuple[Sequence[float], Sequence[float], Sequence[float]] = (
        (0.0, 1.0, 0.2),
        (1.0, 0.0, 0.3),
        (0.2, 0.5, 1.0),
    ),
) -> Field:
    """On-shell k0 plus off-shell k0+e and 2k0+e. Two Fourier keys is not this."""
    k0, k1, k2 = three_shell_keys(k0, e)
    if k0 == (0, 0, 0) or k1 == (0, 0, 0) or k2 == (0, 0, 0):
        raise ValueError("three-shell keys must be nonzero")
    if len({k0, k1, k2}) < 3:
        raise ValueError("three-shell keys must be distinct (need e ≠ 0 and e ≠ -k0)")
    field: Field = {}
    for k, amp, phase, seed in zip((k0, k1, k2), (amp0, amp1, amp2), phases, pol_seeds):
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            v = make_divfree_amp(k, (seed[1], seed[2], seed[0]))
            nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            continue
        field[k] = (amp * np.exp(1j * phase) / nrm) * v
    return enforce_reality(field)


def two_shell_shift_field(
    k0: ModeKey,
    e: ModeKey,
    amp0: float = 1.0,
    amp1: float = 0.2,
    phases: Tuple[float, float] = (0.0, 0.3),
    pol_seeds: Tuple[Sequence[float], Sequence[float]] = (
        (0.0, 1.0, 0.2),
        (1.0, 0.0, 0.3),
    ),
) -> Field:
    """k0 and k0+e only: two Fourier keys, no closing third mode.
    Two *shells* can still support a live triad; this control is two keys.
    """
    k1 = add_modes(k0, e)
    field: Field = {}
    for k, amp, phase, seed in zip((k0, k1), (amp0, amp1), phases, pol_seeds):
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            v = make_divfree_amp(k, (seed[1], seed[2], seed[0]))
            nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            continue
        field[k] = (amp * np.exp(1j * phase) / nrm) * v
    return enforce_reality(field)


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


def mul_mode(k: ModeKey, n: int) -> ModeKey:
    return (k[0] * n, k[1] * n, k[2] * n)


def ap_line(origin: ModeKey, step: ModeKey, count: int) -> List[ModeKey]:
    return [add_modes(origin, mul_mode(step, i)) for i in range(count)]


def l2_normalize(field: Field) -> Field:
    e = 0.0
    for v in field.values():
        e += float(np.vdot(v, v).real)
    if e <= 1e-30:
        return field
    s = 1.0 / float(np.sqrt(e))
    return {k: s * v for k, v in field.items()}


def integer_shell(N: int) -> List[ModeKey]:
    """All nonzero k in Z^3 with |k|^2 = N."""
    if N <= 0:
        return []
    kmax = int(N ** 0.5) + 1
    out: List[ModeKey] = []
    for i in range(-kmax, kmax + 1):
        for j in range(-kmax, kmax + 1):
            for k in range(-kmax, kmax + 1):
                if i * i + j * j + k * k == N and (i, j, k) != (0, 0, 0):
                    out.append((i, j, k))
    return out


def shell_closing_pairs(
    P: List[ModeKey],
    Q: List[ModeKey] | None = None,
    *,
    forbid: Iterable[int] | None = None,
) -> Tuple[int, List[Tuple[ModeKey, ModeKey, ModeKey]]]:
    """Pairs p in P, q in Q with p+q nonzero. Return the most popular |p+q|^2 and those triads.

    *forbid* drops sum-shells (so the third leg can be forced off the
    P/Q eigenvalue: otherwise a one-shell packet has Ds=0 and is not
    a test of the O(1)-denominator heuristic).
    """
    if Q is None:
        Q = P
    banned = set(forbid) if forbid is not None else set()
    buckets: Dict[int, List[Tuple[ModeKey, ModeKey, ModeKey]]] = {}
    for p in P:
        for q in Q:
            r = add_modes(p, q)
            if r == (0, 0, 0):
                continue
            t = int(k_norm2(r))
            if t in banned:
                continue
            buckets.setdefault(t, []).append((p, q, r))
    if not buckets:
        raise ValueError("no closing pairs")
    T, pairs = max(buckets.items(), key=lambda kv: len(kv[1]))
    return T, pairs


def _edge_preserving_subset(
    keys: List[ModeKey],
    pairs: Sequence[Tuple[ModeKey, ModeKey, ModeKey]],
    m: int,
) -> List[ModeKey]:
    """Keep *m* vertices that still carry actual closing pairs.

    Degree-ranking the global graph then dropping vertices can leave a
    subset with *zero* remaining edges on the original best T
    (seen at N=14, m=8). Walk the pair list and take both endpoints
    until the budget is spent, so a small packet is still two-shell.
    """
    if m <= 0 or len(keys) <= m:
        return list(keys)
    used: List[ModeKey] = []
    seen = set()
    for p, q, _r in pairs:
        for k in (p, q):
            if k in seen:
                continue
            seen.add(k)
            used.append(k)
            if len(used) >= m:
                return used
    for k in keys:
        if k in seen:
            continue
        seen.add(k)
        used.append(k)
        if len(used) >= m:
            break
    return used


def _aligned_pol_seed(k: ModeKey) -> Tuple[float, float, float]:
    """Deterministic swirl k × e_z (or k × e_x if k is vertical)."""
    kx, ky, kz = float(k[0]), float(k[1]), float(k[2])
    if abs(kx) + abs(ky) > 0:
        return (ky, -kx, 0.0)
    return (0.0, kz, 0.0)


def same_shell_packet_field(
    N: int,
    m: int | None = None,
    phase_p: float = 0.0,
    phase_q: float = 0.0,
    phase_r_shift: float = 0.5 * np.pi,
    pol_seed: Sequence[float] = (0.2, 1.0, -0.3),
    random_phases: bool = False,
    aligned_pol: bool = True,
    rng: np.random.Generator | None = None,
) -> Tuple[Field, dict]:
    """Coherent packet on one Fourier shell, partner on a second eigenvalue.

    Keys of P and Q sit on shell N. The third leg is the most popular
    sum-shell T ≠ N among closing pairs, so Ds is a shell gap, not an
    AP-width sum. Eigenvalues do not spread with m. Amplitudes are
    equal after L2 normalization. Phases are one value per shell
    unless random_phases. Polarizations default to aligned swirl.

    If m is not None, keep m vertices that still carry closing pairs
    on that fixed T (edge-preserving subset).
    """
    S = integer_shell(N)
    if len(S) < 3:
        raise ValueError(f"shell {N} too thin")
    T, pairs = shell_closing_pairs(S, forbid={N})
    if m is not None:
        keys_p = _edge_preserving_subset(S, pairs, m)
        keyset = set(keys_p)
        pairs = [tr for tr in pairs if tr[0] in keyset and tr[1] in keyset]
    if not pairs:
        raise ValueError(f"shell {N} m={m}: no remaining T-pairs")
    Pkeys = sorted(set(p for p, _q, _r in pairs))
    Qkeys = sorted(set(q for _p, q, _r in pairs))
    Rkeys = sorted(set(r for _p, _q, r in pairs))
    field: Field = {}

    def put(k: ModeKey, phase: float) -> None:
        if k == (0, 0, 0):
            return
        mk = (-k[0], -k[1], -k[2])
        if k in field or mk in field:
            return
        if aligned_pol and not random_phases:
            seed: Sequence[float] = _aligned_pol_seed(k)
        elif rng is not None and random_phases:
            seed = tuple(float(x) for x in rng.normal(size=3))
        else:
            seed = pol_seed
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            v = make_divfree_amp(k, (seed[1], seed[2], seed[0]))
            nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            return
        if random_phases and rng is not None:
            phase = float(rng.uniform(0, 2 * np.pi))
        field[k] = (np.exp(1j * phase) / nrm) * v

    n_phase = phase_p
    t_phase = phase_p + phase_q + phase_r_shift
    for k in Pkeys:
        put(k, n_phase)
    for k in Qkeys:
        put(k, n_phase)
    for k in Rkeys:
        put(k, t_phase)
    field = l2_normalize(enforce_reality(field))
    shells = sorted({int(k_norm2(k)) for k in field})
    meta = {
        "N": N,
        "T": T,
        "m_requested": m,
        "n_P": len(Pkeys),
        "n_Q": len(Qkeys),
        "n_R": len(Rkeys),
        "n_pairs": len(pairs),
        "n_modes": len(field),
        "shells": shells,
        "n_shells": len(shells),
    }
    return field, meta


def two_eigenvalue_closed_triad(
    phases: Tuple[float, float, float] = (0.0, 0.3, -0.2),
    pol_seeds: Tuple[Sequence[float], Sequence[float], Sequence[float]] = (
        (0.0, 1.0, 0.2),
        (1.0, 0.0, 0.3),
        (0.2, 0.5, 1.0),
    ),
) -> Field:
    """Live two-*shell* triad on three keys: p=(1,1,0), q=(1,-1,0), p+q=(2,0,0).

    |p|^2 = |q|^2 = 2, |p+q|^2 = 4. Two shells can support a closed triad.
    Two Fourier keys cannot.
    """
    return three_shell_field(
        (1, 1, 0),
        (0, -2, 0),
        amp0=1.0,
        amp1=1.0,
        amp2=1.0,
        phases=phases,
        pol_seeds=pol_seeds,
    )


def coherent_packet_field(
    m: int,
    p0: ModeKey = (5, 2, 1),
    q0: ModeKey = (-3, 1, 1),
    step: ModeKey = (0, 1, 0),
    phase_p: float = 0.0,
    phase_q: float = 0.0,
    phase_r_shift: float = 0.5 * np.pi,
    pol_seed: Sequence[float] = (0.2, 1.0, -0.3),
    random_phases: bool = False,
    random_pol: bool = False,
    rng: np.random.Generator | None = None,
) -> Field:
    """Arithmetic-progression packets P, Q, R=P+Q.

    |P|=m, |Q|=m, |R|=2m-1. Every (p,q) in P×Q closes onto R: O(m^2) triads.
    Energy-normalized. Coherent phases unless random_phases=True.
    """
    if m < 1:
        raise ValueError("m >= 1")
    P = ap_line(p0, step, m)
    Q = ap_line(q0, step, m)
    R = ap_line(add_modes(p0, q0), step, 2 * m - 1)
    field: Field = {}

    def put(k: ModeKey, phase: float) -> None:
        if k == (0, 0, 0):
            return
        if random_pol and rng is not None:
            seed: Sequence[float] = tuple(float(x) for x in rng.normal(size=3))
        else:
            seed = pol_seed
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            v = make_divfree_amp(k, (seed[1], seed[2], seed[0]))
            nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            return
        if random_phases and rng is not None:
            phase = float(rng.uniform(0, 2 * np.pi))
        field[k] = (np.exp(1j * phase) / nrm) * v

    for k in P:
        put(k, phase_p)
    for k in Q:
        put(k, phase_q)
    for k in R:
        put(k, phase_p + phase_q + phase_r_shift)
    return l2_normalize(enforce_reality(field))


def hh_l_fan_field(
    n_pairs: int,
    k_low: ModeKey = (2, 0, 0),
    rng: np.random.Generator | None = None,
    randomize: bool = True,
) -> Field:
    """n_pairs high pairs with p+q = k_low, plus mass on k_low. Not frozen."""
    field: Field = {}
    used = 0
    n = 3
    while used < n_pairs and n < 120:
        p = (n, n, 1)
        q = (k_low[0] - p[0], k_low[1] - p[1], k_low[2] - p[2])
        n += 1
        if p == (0, 0, 0) or q == (0, 0, 0) or p == q:
            continue
        if p == tuple(-x for x in q):
            continue
        if rng is not None and randomize:
            sp = tuple(float(x) for x in rng.normal(size=3))
            sq = tuple(float(x) for x in rng.normal(size=3))
            php = float(rng.uniform(0, 2 * np.pi))
            phq = float(rng.uniform(0, 2 * np.pi))
        else:
            sp, sq = (1.0, 0.3, -0.4), (0.2, 1.0, 0.1)
            php = phq = 0.0
        vp = make_divfree_amp(p, sp)
        vq = make_divfree_amp(q, sq)
        np_ = np.linalg.norm(vp)
        nq_ = np.linalg.norm(vq)
        if np_ < 1e-14 or nq_ < 1e-14:
            continue
        field[p] = (np.exp(1j * php) / np_) * vp
        field[q] = (np.exp(1j * phq) / nq_) * vq
        used += 1
    sl = (0.0, 1.0, 0.2) if rng is None else tuple(float(x) for x in rng.normal(size=3))
    vl = make_divfree_amp(k_low, sl)
    nl = np.linalg.norm(vl)
    if nl > 1e-14:
        phl = 0.0 if rng is None else float(rng.uniform(0, 2 * np.pi))
        field[k_low] = (np.exp(1j * phl) / nl) * vl
    return l2_normalize(enforce_reality(field))


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
            coeff = 1j * np.dot(up, np.array(q, dtype=np.float64))
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
        f"Tc={r.Tc:.4e} R★={r.ratio_star:.4e} Rpre={r.ratio_preyoung:.4e} "
        f"Rc*={r.ratio_cstar:.4e} Rk0={r.ratio_k0:.4e} Rbox={r.ratio_box:.4e}"
    )
