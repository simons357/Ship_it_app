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

Survivor bound from Attack 2 (K=0 killed):
  Tc ≤ θ ν Ds + C* X^{3/2} Λ
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
        f"Rc*={r.ratio_cstar:.4e} Rk0={r.ratio_k0:.4e}"
    )
