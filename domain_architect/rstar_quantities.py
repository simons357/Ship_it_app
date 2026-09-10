"""Exact Fourier / R_★ spectral quantities for Lemma★ (USER lock-in).

Canonical full shape SoT: docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md

    T_c = -⟨B(v,v), A(A−Λ)v⟩
    (equivalent to M − Λ N when those triad moments exist)

Full lemma (viscosity cancelled under u=av):

    ∃ C_geom < ∞ ∀ v ≠ 0:  (T_c(v)_+)^2 ≤ C_geom D_s(v) ‖v‖₂² Y(v)
    R_★(v) = (T_c_+)^2 / (D_s ‖v‖₂² Y)   (D_s>0)

Viscosity packaging: C_geom = 4 θ C_0(θ).

Hard rules:
- NEVER absolute-value the triad sum.
- HH→L-restricted partial sums ≠ complete T_c for kill decisions.
- Finite small R_★ samples ≠ uniform bound.
- K_{α,β} ≠ full ★ — near-shell tests only a restricted limiting family.
- NS NOT SOLVED. No SFE glue.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Mapping, Sequence

# Wavevector key: (kx, ky, kz) ints, or shell eigenvalue λ=|k|² as int/float.
WaveKey = tuple[int, int, int] | int | float
EnergyMap = Mapping[Any, float]


HARD_RULES: tuple[str, ...] = (
    "NEVER abs the triad sum — T_k / T_c stay signed",
    "HH→L restricted ≠ complete T_c for kill decision",
    "Finite small R_★ samples ≠ uniform bound",
    "K_{α,β} ≠ full ★ — near-shell restricted family only",
    "Only complete T_c decides failure; NS NOT SOLVED; no SFE",
)

DOC_PATH = "docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md"


def _as_lambda(key: Any) -> float:
    """Extract λ_k = |k|² from a mode key or shell label."""
    if isinstance(key, (tuple, list)) and len(key) == 3:
        kx, ky, kz = (float(key[0]), float(key[1]), float(key[2]))
        return kx * kx + ky * ky + kz * kz
    return float(key)


def _energy_items(energies: EnergyMap) -> list[tuple[float, float]]:
    """Return list of (λ, |v|²) pairs; skip nonpositive energy."""
    out: list[tuple[float, float]] = []
    for key, e in energies.items():
        ee = float(e)
        if ee < 0:
            raise ValueError(f"negative shell/mode energy for key={key!r}: {ee}")
        if ee == 0.0:
            continue
        out.append((_as_lambda(key), ee))
    return out


@dataclass(frozen=True)
class SpectralMoments:
    """Linear spectral moments on T³ Fourier data."""

    energy_l2: float  # ‖v‖₂²
    X: float
    Y: float
    Z: float
    Lambda: float  # Y/X when X>0 else 0
    D_s_form1: float  # Z - Λ Y = Z - Y²/X
    D_s_form2: float  # Σ λ(λ-Λ)² |v|²
    D_s_form3: float  # (1/(2X)) Σ_{k,ℓ} λ_k λ_ℓ (λ_k-λ_ℓ)² |v_k|²|v_ℓ|²
    n_modes: int = 0

    @property
    def D_s(self) -> float:
        return self.D_s_form1

    @property
    def Lambda_symbol(self) -> float:
        return self.Lambda

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["D_s"] = self.D_s
        d["forms_agree"] = self.forms_agree()
        return d

    def forms_agree(self, rtol: float = 1e-9, atol: float = 1e-12) -> bool:
        a, b, c = self.D_s_form1, self.D_s_form2, self.D_s_form3
        return (
            abs(a - b) <= atol + rtol * max(abs(a), abs(b), 1.0)
            and abs(a - c) <= atol + rtol * max(abs(a), abs(c), 1.0)
        )


def spectral_moments(energies: EnergyMap) -> SpectralMoments:
    """Compute X, Y, Z, Λ, and all three D_s forms from |v_k|² (or shell) energies.

    ``energies`` maps either:
      - wavevector (kx,ky,kz) → |v_k|², or
      - shell eigenvalue λ=|k|² → shell energy e_λ.
    """
    items = _energy_items(energies)
    energy_l2 = sum(e for _, e in items)
    X = sum(lam * e for lam, e in items)
    Y = sum(lam * lam * e for lam, e in items)
    Z = sum(lam ** 3 * e for lam, e in items)

    if X <= 0.0:
        return SpectralMoments(
            energy_l2=energy_l2,
            X=0.0,
            Y=0.0,
            Z=0.0,
            Lambda=0.0,
            D_s_form1=0.0,
            D_s_form2=0.0,
            D_s_form3=0.0,
            n_modes=len(items),
        )

    Lambda = Y / X
    form1 = Z - Lambda * Y  # = Z - Y²/X
    form2 = sum(lam * (lam - Lambda) ** 2 * e for lam, e in items)

    # Pairwise form: (1/(2X)) Σ_{k,ℓ} λ_k λ_ℓ (λ_k-λ_ℓ)² e_k e_ℓ
    form3_acc = 0.0
    n = len(items)
    for i in range(n):
        lam_i, e_i = items[i]
        for j in range(n):
            lam_j, e_j = items[j]
            dlam = lam_i - lam_j
            form3_acc += lam_i * lam_j * dlam * dlam * e_i * e_j
    form3 = form3_acc / (2.0 * X)

    return SpectralMoments(
        energy_l2=energy_l2,
        X=X,
        Y=Y,
        Z=Z,
        Lambda=Lambda,
        D_s_form1=form1,
        D_s_form2=form2,
        D_s_form3=form3,
        n_modes=len(items),
    )


def D_s_moment(energies: EnergyMap) -> float:
    """D_s = Z − Λ Y (Form 1)."""
    return spectral_moments(energies).D_s_form1


def D_s_variance(energies: EnergyMap) -> float:
    """D_s = Σ λ(λ−Λ)² |v|² (Form 2)."""
    return spectral_moments(energies).D_s_form2


def D_s_pairwise(energies: EnergyMap) -> float:
    """D_s pairwise Form 3 ≥ 0."""
    return spectral_moments(energies).D_s_form3


def two_shell_D_s(alpha: float, beta: float, e_alpha: float, e_beta: float) -> float:
    """Closed form: D_s = α β (α−β)² e_α e_β / (α e_α + β e_β).

    Requires α≠β or zero energies; denominator is X = α e_α + β e_β.
    """
    a = float(alpha)
    b = float(beta)
    ea = float(e_alpha)
    eb = float(e_beta)
    if ea < 0 or eb < 0:
        raise ValueError("shell energies must be nonnegative")
    if ea == 0.0 and eb == 0.0:
        return 0.0
    denom = a * ea + b * eb
    if denom <= 0.0:
        return 0.0
    return (a * b * (a - b) ** 2 * ea * eb) / denom


def verify_two_shell_vs_sum(
    alpha: float,
    beta: float,
    e_alpha: float,
    e_beta: float,
    *,
    rtol: float = 1e-9,
    atol: float = 1e-12,
) -> dict[str, Any]:
    """Compare two-shell closed form against Form 1–3 on the same support."""
    closed = two_shell_D_s(alpha, beta, e_alpha, e_beta)
    moments = spectral_moments({alpha: e_alpha, beta: e_beta})
    ok = (
        abs(closed - moments.D_s_form1) <= atol + rtol * max(abs(closed), 1.0)
        and moments.forms_agree(rtol=rtol, atol=atol)
    )
    return {
        "ok": ok,
        "two_shell_closed": closed,
        "D_s_form1": moments.D_s_form1,
        "D_s_form2": moments.D_s_form2,
        "D_s_form3": moments.D_s_form3,
        "moments": moments.to_dict(),
    }


@dataclass(frozen=True)
class TriadContribution:
    """One signed triad contribution to some T_k (never abs'd)."""

    p: Any
    q: Any
    k: Any
    value: float  # signed Im[(q·v_p)(v_q·conj(v_k))]
    channel: str = "complete"  # e.g. "complete", "HH->L" (restricted ≠ kill)


@dataclass
class TcResult:
    """T_c from signed triad contributions — complete sum only for kill.

    Canonical definition:
        T_c = -⟨B(v,v), A(A−Λ)v⟩
    Equivalent (when M,N exist): T_c = M − Λ N = Σ λ(λ−Λ) T_k.
    """

    T_c: float
    N: float
    M: float
    Lambda: float
    n_contributions: int
    used_restricted_channel: bool
    complete: bool
    note: str = ""
    hard_rules: list[str] = field(default_factory=lambda: list(HARD_RULES))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def T_c_from_signed_triads(
    contributions: Sequence[TriadContribution] | Iterable[float],
    *,
    lambdas: Mapping[Any, float] | None = None,
    Lambda: float | None = None,
    X: float | None = None,
    Y: float | None = None,
    allow_restricted: bool = False,
) -> TcResult:
    """Assemble T_c from **signed** triad contributions (no abs).

    Canonical: T_c = -⟨B(v,v), A(A−Λ)v⟩.
    When triad moments exist this equals M − Λ N.

    Two call styles:

    1. Iterable of floats already weighted as λ(λ−Λ) T_k pieces → summed as T_c.
       Pass ``Lambda`` (and optionally mark restricted via TriadContribution).

    2. Sequence of ``TriadContribution`` with ``lambdas[k]=λ_k`` and either
       ``Lambda`` or ``X,Y`` so Λ=Y/X. Then
         T_k pieces summed per k, N=Σ λ T_k, M=Σ λ² T_k, T_c=M−Λ N.

    HH→L-restricted inputs raise unless ``allow_restricted=True`` (still marked
    incomplete — never used as a kill decision).
    """
    contrib_list = list(contributions)
    if not contrib_list:
        return TcResult(
            T_c=0.0,
            N=0.0,
            M=0.0,
            Lambda=float(Lambda or 0.0),
            n_contributions=0,
            used_restricted_channel=False,
            complete=True,
            note="empty triad list → T_c=0 (not a kill by itself)",
        )

    # Plain floats: already signed λ(λ−Λ)T_k pieces
    if all(isinstance(c, (int, float)) for c in contrib_list):
        if Lambda is None:
            raise ValueError("Lambda required when passing raw signed T_c pieces")
        total = float(sum(float(c) for c in contrib_list))
        return TcResult(
            T_c=total,
            N=float("nan"),
            M=float("nan"),
            Lambda=float(Lambda),
            n_contributions=len(contrib_list),
            used_restricted_channel=False,
            complete=True,
            note="summed pre-weighted signed λ(λ−Λ)T_k pieces (no abs)",
        )

    triads = [c if isinstance(c, TriadContribution) else TriadContribution(
        p=None, q=None, k=None, value=float(c)
    ) for c in contrib_list]

    restricted = any(
        str(t.channel).upper().replace("→", "->") in {"HH->L", "HH_TO_L", "RESTRICTED"}
        or "hh" in str(t.channel).lower()
        for t in triads
    )
    if restricted and not allow_restricted:
        raise ValueError(
            "HH→L restricted triad list is not complete T_c — "
            "refuse kill decision (pass allow_restricted=True only for diagnostics)"
        )

    if lambdas is None:
        # Treat each contribution value as already a full signed T_c piece
        if Lambda is None:
            raise ValueError("Lambda or lambdas required")
        total = sum(float(t.value) for t in triads)
        return TcResult(
            T_c=total,
            N=float("nan"),
            M=float("nan"),
            Lambda=float(Lambda),
            n_contributions=len(triads),
            used_restricted_channel=restricted,
            complete=not restricted,
            note=(
                "signed sum without per-mode λ map; "
                + ("INCOMPLETE (restricted channel)" if restricted else "treated as complete pieces")
            ),
        )

    # Aggregate T_k = Σ contributions targeting mode k (signed)
    T_by_k: dict[Any, float] = {}
    for t in triads:
        if t.k is None:
            raise ValueError("TriadContribution.k required when lambdas provided")
        T_by_k[t.k] = T_by_k.get(t.k, 0.0) + float(t.value)

    if Lambda is None:
        if X is None or Y is None:
            # derive from lambdas weights if energies not given — require X,Y
            raise ValueError("provide Lambda or both X and Y")
        if X <= 0:
            raise ValueError("X must be positive to form Lambda=Y/X")
        Lambda = Y / X
    Lam = float(Lambda)

    N = 0.0
    M = 0.0
    for k, Tk in T_by_k.items():
        if k not in lambdas:
            raise KeyError(f"missing λ for mode/shell key={k!r}")
        lam = float(lambdas[k])
        N += lam * Tk
        M += lam * lam * Tk
    Tc = M - Lam * N  # ≡ -⟨B, A(A−Λ)v⟩ = Σ λ(λ−Λ) T_k when moments exist

    return TcResult(
        T_c=Tc,
        N=N,
        M=M,
        Lambda=Lam,
        n_contributions=len(triads),
        used_restricted_channel=restricted,
        complete=not restricted,
        note=(
            "T_c=-⟨B,A(A−Λ)v⟩ ≡ M−ΛN from signed T_k (no abs); "
            + ("INCOMPLETE HH→L proxy — do not use for kill" if restricted else "complete T_c")
        ),
    )


def T_c_plus(T_c: float) -> float:
    """Positive part [T_c]_+ = max(T_c, 0)."""
    return max(float(T_c), 0.0)


def R_star(
    T_c: float,
    D_s: float,
    energy_l2: float,
    Y: float,
    *,
    complete_T_c: bool = True,
) -> dict[str, Any]:
    """R_★(v) = (T_c_+)^2 / (D_s ‖v‖₂² Y) with complete [T_c]_+ only.

    Kill diagnostics:
      - D_s=0 and T_c>0 → dead
      - pure single shell both vanish → not a kill
      - finite sample value ≠ uniform bound
    """
    if not complete_T_c:
        return {
            "R_star": None,
            "ok": False,
            "kill": None,
            "reason": (
                "REFUSE: incomplete / HH→L-restricted T_c cannot decide "
                "R_★ kill — only complete T_c"
            ),
            "hard_rules": list(HARD_RULES),
            "doc": DOC_PATH,
        }

    tc = float(T_c)
    ds = float(D_s)
    e2 = float(energy_l2)
    y = float(Y)
    tcp = T_c_plus(tc)
    denom = ds * e2 * y

    kill: str | None = None
    if ds == 0.0 and tc > 0.0:
        kill = "DEAD: D_s=0 and T_c>0 (almost-single-shell stretch / live kill lane)"
    elif ds == 0.0 and tcp == 0.0:
        kill = "NOT_KILL: pure single shell — both sides vanish"
    elif denom <= 0.0:
        kill = "UNDEFINED_DENOM: cannot form R_★ (check D_s, ‖v‖₂², Y)"

    r_val: float | None
    if denom > 0.0:
        r_val = (tcp * tcp) / denom
    else:
        r_val = None

    return {
        "R_star": r_val,
        "T_c": tc,
        "T_c_plus": tcp,
        "D_s": ds,
        "energy_l2": e2,
        "Y": y,
        "denominator": denom if denom > 0 else 0.0,
        "ok": r_val is not None,
        "kill": kill,
        "uniform_bound": False,  # finite sample ≠ uniform
        "note": (
            "Finite sample R_★ is evidence only — not a uniform bound; "
            "sup R_★=∞ would kill ★"
        ),
        "shape_form": "(T_c_+)^2 <= C_geom * D_s * ||v||_2^2 * Y",
        "hard_rules": list(HARD_RULES),
        "doc": DOC_PATH,
        "ns_solved": False,
    }


def lambda_prime(T_c: float, nu: float, D_s: float, X: float) -> float:
    """Sign-check identity: Λ' = (2/X)(T_c − ν D_s)."""
    if X <= 0.0:
        raise ValueError("X must be positive for Lambda'")
    return (2.0 / float(X)) * (float(T_c) - float(nu) * float(D_s))


def shape_form_holds(
    T_c: float,
    D_s: float,
    energy_l2: float,
    Y: float,
    theta: float,
    C_0: float,
) -> dict[str, Any]:
    """Check boxed shape inequality for one field (evidence, not proof)."""
    left = T_c_plus(T_c) ** 2
    right = 4.0 * float(theta) * float(C_0) * float(D_s) * float(energy_l2) * float(Y)
    return {
        "left": left,
        "right": right,
        "holds": left <= right + 1e-12,
        "evidence_only": True,
        "proof": False,
        "ns_solved": False,
        "boxed": "(T_c(v)_+)^2 <= C_geom * D_s(v) * ||v||_2^2 * Y(v)",
        "C_geom": "4*theta*C_0(theta)",
    }


def exact_formula_inventory() -> dict[str, Any]:
    """Machine-readable inventory of locked exact formulas (no SFE)."""
    return {
        "doc": DOC_PATH,
        "shape_statement": True,
        "viscosity_cancelled_under_u_av": True,
        "ns_solved": False,
        "sfe": False,
        "boxed_shape_form": "(T_c(v)_+)^2 <= C_geom * D_s(v) * ||v||_2^2 * Y(v)",
        "C_geom": "4*theta*C_0(theta)",
        "R_star": "R_star(v) = (T_c_+)^2 / (D_s * ||v||_2^2 * Y)",
        "linear_moments": ["||v||_2^2", "X", "Y", "Z", "Lambda=Y/X"],
        "D_s_forms": [
            "Z - Lambda*Y = Z - Y^2/X",
            "||(A-Lambda)A^{1/2}v||_2^2",
            "sum_k lambda*(lambda-Lambda)^2 |v_k|^2",
            "(1/(2X)) sum_{k,l} lambda_k lambda_l (lambda_k-lambda_l)^2 |v_k|^2|v_l|^2",
        ],
        "two_shell": "D_s = alpha*beta*(alpha-beta)^2*e_alpha*e_beta / (alpha*e_alpha+beta*e_beta)",
        "nonlinear": {
            "B": "P[(v·∇)v]",
            "T_k": "sum_{p+q=k} Im[(q·v_p)(v_q·conj(v_k))]  (SIGNED — never abs)",
            "N": "sum lambda T_k",
            "M": "sum lambda^2 T_k",
            "T_c": "-<B(v,v), A(A-Lambda)v>  ≡  M - Lambda*N = sum lambda(lambda-Lambda) T_k",
            "ordered_triad_pq_k": "sum_k sum_{p+q=k} lambda_k(lambda_k-Lambda) Im[...]",
            "ordered_triad_pqr_0": "sum_{p+q+r=0} lambda_r(lambda_r-Lambda) Im[(q·v_p)(v_q·conj(v_r))]",
        },
        "sign_check": "Lambda' = (2/X)(T_c - nu*D_s)",
        "kill_rules": [
            "sup R_star = infinity → dead",
            "D_s=0 and T_c>0 → dead",
            "pure single shell both vanish → not a kill",
            "almost-single-shell that stretches → live kill",
            "finite small R_star samples ≠ uniform bound",
            "K_{α,β} ≠ full ★ (restricted near-shell family only)",
        ],
        "hard_rules": list(HARD_RULES),
        "proof_needed": "triadic reason; HH→L dangerous channel; only complete T_c decides failure",
        "full_lemma": True,
        "K_alpha_beta_is_full_star": False,
    }
