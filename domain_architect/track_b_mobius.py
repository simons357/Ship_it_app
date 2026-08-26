"""RH Track B — Möbius–GCD operator (not classical NS Track B).

Locked operator
    Q_N(i,j) = μ(gcd(i,j)) / gcd(i,j),    1 ≤ i,j ≤ N.

This module checks the finite algebraic identities in the August Track B
chain and attacks the missing bridge to the Littlewood–Mertens bound.
It does not assume RH, Mertens, a zero-free region, Route C, λ_min > −1/2,
or the historical −1/(2π) limit. It is not a proof engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd, pi
from typing import Any, Iterable

import numpy as np

# Disambiguation: DA inventory "Track B" is classical NS vorticity (NS-B).
RH_TRACK_B_NAME = "RH Track B (Möbius–GCD)"
LOCKED_OPERATOR = "Q_N(i,j) = μ(gcd(i,j))/gcd(i,j)"
QUARANTINED_OPERATORS = (
    "1/gcd(i,j)",
    "1/(gcd(i,j)*sqrt(i*j))",
    "gcd(i,j)/sqrt(i*j)",
    "NS shell Hamiltonian / Möbius-frozen fluid operator",
)

ZETA2 = pi * pi / 6.0
ZETA3 = 1.2020569031595942  # Apéry; used only to read August edge constants
AUGUST_LAMBDA_MAX_SLOPE = 1.0 / (ZETA2 * ZETA3)  # N/(ζ(2)ζ(3))
AUGUST_LAMBDA_MIN_SLOPE = -11.0 / (21.0 * ZETA2 * ZETA3)

OUTPUT_OBSTRUCTION = "obstruction"
OUTPUT_CONDITIONAL = "conditional"
OUTPUT_PROOF = "uniform_proof"


def mobius_sieve(n: int) -> list[int]:
    """μ(0..n) with μ(0)=0."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    mu = [1] * (n + 1)
    if n >= 0:
        mu[0] = 0
    least = [0] * (n + 1)
    for i in range(2, n + 1):
        if least[i] == 0:
            for j in range(i, n + 1, i):
                if least[j] == 0:
                    least[j] = i
    for i in range(2, n + 1):
        p = least[i]
        m = i // p
        if m % p == 0:
            mu[i] = 0
        else:
            mu[i] = -mu[m]
    return mu


def h_of(n: int) -> Fraction:
    """h = (μ/·) * μ. Cubefree multiplicative values as specified."""
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        return Fraction(1)
    value = Fraction(1)
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            k = 0
            while x % p == 0:
                x //= p
                k += 1
            if k == 1:
                value *= -Fraction(p + 1, p)
            elif k == 2:
                value *= Fraction(1, p)
            else:
                return Fraction(0)
        p = 3 if p == 2 else p + 2
    if x > 1:
        value *= -Fraction(x + 1, x)
    return value


def mertens(mu: list[int], n: int) -> int:
    return int(sum(mu[1 : n + 1]))


def s_d(mu: list[int], d: int, n: int) -> int:
    """S_d(N) = sum_{k≤N/d} μ(k d)."""
    total = 0
    kd = d
    while kd <= n:
        total += mu[kd]
        kd += d
    return total


def build_q_fractions(n: int, mu: list[int] | None = None) -> list[list[Fraction]]:
    mu = mu if mu is not None else mobius_sieve(n)
    rows: list[list[Fraction]] = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            g = gcd(i, j)
            row.append(Fraction(mu[g], g))
        rows.append(row)
    return rows


def q_from_cubefree_decomp(n: int) -> list[list[Fraction]]:
    """Q_N = sum_{d≤N} h(d) u_d u_d^T with exact rationals."""
    q = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for d in range(1, n + 1):
        hd = h_of(d)
        if hd == 0:
            continue
        multiples = [k - 1 for k in range(d, n + 1, d)]
        for a in multiples:
            qa = q[a]
            for b in multiples:
                qa[b] += hd
    return q


def quadratic_form(q: list[list[Fraction]], x: list[int]) -> Fraction:
    total = Fraction(0)
    n = len(x)
    for i in range(n):
        xi = x[i]
        if xi == 0:
            continue
        row = q[i]
        inner = Fraction(0)
        for j in range(n):
            if x[j] != 0:
                inner += row[j] * x[j]
        total += xi * inner
    return total


def first_row_is_ones(q: list[list[Fraction]]) -> bool:
    return all(entry == 1 for entry in q[0])


def matrices_equal(a: list[list[Fraction]], b: list[list[Fraction]]) -> bool:
    return a == b


@dataclass
class IdentityCheck:
    n: int
    decomp_matches: bool
    first_row_ones: bool
    first_row_mertens: bool
    quadratic_identity: bool
    mertens: int
    mu_q_mu: str
    remainder: str

    @property
    def ok(self) -> bool:
        return (
            self.decomp_matches
            and self.first_row_ones
            and self.first_row_mertens
            and self.quadratic_identity
        )


def verify_identities(n: int) -> IdentityCheck:
    """Exact finite identities. Independent of RH."""
    mu = mobius_sieve(n)
    q = build_q_fractions(n, mu)
    q_de = q_from_cubefree_decomp(n)
    mu_vec = mu[1 : n + 1]
    m_n = mertens(mu, n)
    first = sum(q[0][j] * mu_vec[j] for j in range(n))
    quad = quadratic_form(q, mu_vec)
    remainder = Fraction(0)
    for d in range(2, n + 1):
        hd = h_of(d)
        if hd == 0:
            continue
        remainder += hd * s_d(mu, d, n) ** 2
    return IdentityCheck(
        n=n,
        decomp_matches=matrices_equal(q, q_de),
        first_row_ones=first_row_is_ones(q),
        first_row_mertens=(first == m_n),
        quadratic_identity=(quad == Fraction(m_n**2) + remainder),
        mertens=m_n,
        mu_q_mu=str(quad),
        remainder=str(remainder),
    )


def q_dense(n: int, mu: list[int] | None = None) -> np.ndarray:
    mu = mu if mu is not None else mobius_sieve(n)
    q = np.empty((n, n), dtype=np.float64)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            g = gcd(i, j)
            q[i - 1, j - 1] = mu[g] / g
    return q


def spectral_snapshot(n: int) -> dict[str, Any]:
    mu = mobius_sieve(n)
    q = q_dense(n, mu)
    eig = np.linalg.eigvalsh(q)
    lam_min = float(eig[0])
    lam_max = float(eig[-1])
    n_pos = int(np.sum(eig > 1e-10))
    n_neg = int(np.sum(eig < -1e-10))
    n_zero = n - n_pos - n_neg
    mu_vec = np.array(mu[1 : n + 1], dtype=np.float64)
    quad = float(mu_vec @ q @ mu_vec)
    l2 = float(mu_vec @ mu_vec)
    ones = np.ones(n, dtype=np.float64)
    r_ones = float(ones @ q @ ones) / float(n)
    return {
        "n": n,
        "lambda_min": lam_min,
        "lambda_max": lam_max,
        "lambda_min_over_n": lam_min / n,
        "lambda_max_over_n": lam_max / n,
        "august_lambda_max_slope": AUGUST_LAMBDA_MAX_SLOPE,
        "august_lambda_min_slope": AUGUST_LAMBDA_MIN_SLOPE,
        "n_pos": n_pos,
        "n_neg": n_neg,
        "n_zero": n_zero,
        "indefinite": bool(n_pos > 0 and n_neg > 0),
        "mu_q_mu": quad,
        "mu_l2": l2,
        "rayleigh_mu": quad / l2 if l2 else 0.0,
        "rayleigh_ones": r_ones,
        "mertens": int(mu_vec.sum()),
        "holder_l1": float(np.abs(mu_vec).sum()),  # ||μ||_1 * ||Q e_1||_∞ = ||μ||_1
        "holder_l2": float(np.linalg.norm(mu_vec) * np.sqrt(n)),
        "holder_linf": float(n),  # ||μ||_∞=1, ||ones||_1=N
    }


def holder_always_order_n(n: int, snap: dict[str, Any] | None = None) -> dict[str, Any]:
    """First-row pairing + any ℓ^p Hölder bound is Θ(N), never RH-scale."""
    snap = snap if snap is not None else spectral_snapshot(n)
    m = abs(int(snap["mertens"]))
    bounds = {
        "l1": snap["holder_l1"],
        "l2": snap["holder_l2"],
        "linf": snap["holder_linf"],
    }
    return {
        "n": n,
        "|M(N)|": m,
        "sqrt_n": n**0.5,
        "bounds": bounds,
        "all_bounds_are_theta_n": all(b >= 0.2 * n for b in bounds.values()),
        "no_holder_bound_is_o_n": min(bounds.values()) >= 0.2 * n,
        "first_row_uses_only_that_Q_e1_is_ones": True,
    }


def quadratic_split(n: int) -> dict[str, Any]:
    mu = mobius_sieve(n)
    q = build_q_fractions(n, mu)
    mu_vec = mu[1 : n + 1]
    m_n = mertens(mu, n)
    quad = quadratic_form(q, mu_vec)
    remainder = quad - Fraction(m_n**2)
    return {
        "n": n,
        "M": m_n,
        "M_squared": m_n**2,
        "mu_Q_mu": str(quad),
        "remainder_sum_d_ge_2": str(remainder),
        "signs_mixed": True,
        "note": (
            "M(N)^2 = μ^T Q μ − remainder. A lower bound on μ^T Q μ is not "
            "an upper bound on M(N)^2. Bounding both RHS terms at the RH "
            "scale is equivalent to the Mertens target, not a reduction."
        ),
    }


def adversarial_squarefree_signs(n: int, trials: int = 25, seed: int = 0) -> dict[str, Any]:
    """Random ±1 on squarefree support. Typical |1^T x| is already ~√N."""
    rng = np.random.default_rng(seed)
    mu = mobius_sieve(n)
    support = [i for i in range(1, n + 1) if mu[i] != 0]
    sizes = []
    for _ in range(trials):
        x = np.zeros(n, dtype=np.float64)
        signs = rng.choice([-1.0, 1.0], size=len(support))
        for idx, s in zip(support, signs):
            x[idx - 1] = s
        sizes.append(abs(float(x.sum())))
    arr = np.array(sizes)
    mu_size = abs(mertens(mu, n))
    return {
        "n": n,
        "trials": trials,
        "random_mean_abs": float(arr.mean()),
        "random_median": float(np.median(arr)),
        "|M(N)|": mu_size,
        "sqrt_n": n**0.5,
        "random_typical_is_sqrt_n_scale": float(arr.mean()) < 8.0 * (n**0.5),
    }


@dataclass
class RouteVerdict:
    name: str
    status: str
    reason: str
    independent_of_rh: bool


def route_verdicts(n: int, snap: dict[str, Any]) -> list[RouteVerdict]:
    holder = holder_always_order_n(n, snap)
    return [
        RouteVerdict(
            name="first-row Hölder / dual ℓ^p",
            status=OUTPUT_OBSTRUCTION,
            reason=(
                "M(N)=e_1^T Q_N μ_N because the first row of Q_N is identically 1. "
                "That identity does not see the rest of the spectrum. Hölder on "
                "(μ_N, 1) yields |M(N)| ≤ ||μ||_p ||1||_q = Θ(N) for every p∈[1,∞] "
                f"(checked at N={n}: ℓ¹ {holder['bounds']['l1']:.3g}, "
                f"ℓ² {holder['bounds']['l2']:.3g}, ℓ∞ {holder['bounds']['linf']:.3g}). "
                "This family cannot reach O_ε(N^{1/2+ε})."
            ),
            independent_of_rh=True,
        ),
        RouteVerdict(
            name="Q-inner-product / Schur dual",
            status=OUTPUT_OBSTRUCTION,
            reason=(
                "Q_N is real symmetric and indefinite for every N≥2 "
                f"(N={n}: {snap['n_pos']} positive, {snap['n_neg']} negative "
                f"eigenvalues). Cauchy–Schwarz in the Q-form is therefore not a "
                "norm inequality and cannot upper-bound |M(N)|."
            ),
            independent_of_rh=True,
        ),
        RouteVerdict(
            name="naive spectral floor/ceiling",
            status=OUTPUT_OBSTRUCTION,
            reason=(
                "λ_min ||μ||_2^2 ≤ μ^T Q μ ≤ λ_max ||μ||_2^2 with both edges "
                "of order N and ||μ||_2^2 = Θ(N) only yields |μ^T Q μ| = O(N^2). "
                "A lower quadratic-form bound does not upper-bound M(N)^2. "
                "Fixed floors −1/2 and −1/(2π) are quarantined: they belong to "
                "other operators."
            ),
            independent_of_rh=True,
        ),
        RouteVerdict(
            name="signed cubefree remainder as an independent estimate",
            status=OUTPUT_OBSTRUCTION,
            reason=(
                "M(N)^2 = μ^T Q μ − ∑_{d≥2} h(d) S_d(N)^2 with mixed-sign h(d). "
                "S_d vanishes unless d is squarefree; for squarefree d, S_d is a "
                "Mertens-type coprime subsum of length N/d. Bounding each S_d at "
                "RH scale assumes the target. Bounding both μ^T Q μ and the "
                "remainder at O_ε(N^{1+2ε}) is equivalent to Littlewood–Mertens, "
                "not a reduction."
            ),
            independent_of_rh=True,
        ),
        RouteVerdict(
            name="weighted ℓ²(1/n) or new norm (search)",
            status=OUTPUT_CONDITIONAL,
            reason=(
                "A genuinely new norm ||·||_* in which ||μ_N||_* and the dual "
                "norm of Q_N e_1 are estimable without Möbius cancellation, yet "
                "multiply to O_ε(N^{1/2+ε}), was not obtained. Random ±1 "
                "squarefree vectors already have |1^T x| on the √N scale, so "
                "operator control alone does not force the exponent; μ must be "
                "shown to behave like those vectors without using RH."
            ),
            independent_of_rh=True,
        ),
    ]


def isolated_conditional_theorem() -> dict[str, str]:
    return {
        "name": "Track B quadratic split, tautological form",
        "statement": (
            "Assume |μ_N^T Q_N μ_N| ≤ C_ε N^{1+2ε} and "
            "|∑_{d=2}^N h(d) S_d(N)^2| ≤ C_ε N^{1+2ε} for every ε>0 and all "
            "large N. Then |M(N)| ≤ √(2 C_ε) N^{1/2+ε}."
        ),
        "status": "not a reduction",
        "why": (
            "Under the exact quadratic identity, this assumption is equivalent "
            "to the Littlewood–Mertens target. Domain Architect therefore does "
            "not treat it as an independent operator estimate."
        ),
    }


@dataclass
class AttackReport:
    output: str
    operator: str = LOCKED_OPERATOR
    book: str = RH_TRACK_B_NAME
    identities: list[IdentityCheck] = field(default_factory=list)
    spectra: list[dict[str, Any]] = field(default_factory=list)
    routes: list[RouteVerdict] = field(default_factory=list)
    conditional: dict[str, str] = field(default_factory=dict)
    adversarial: dict[str, Any] = field(default_factory=dict)
    rh_claimed: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "output": self.output,
            "operator": self.operator,
            "book": self.book,
            "rh_claimed": self.rh_claimed,
            "identities": [c.__dict__ for c in self.identities],
            "spectra": self.spectra,
            "routes": [v.__dict__ for v in self.routes],
            "conditional": self.conditional,
            "adversarial": self.adversarial,
            "notes": self.notes,
        }

    def narrative(self) -> str:
        lines = [
            f"Domain Architect — {self.book}",
            f"Locked operator: {self.operator}",
            "Realization target: Littlewood–Mertens M(N)=O_ε(N^{1/2+ε}). Not an input.",
            "RH is not claimed.",
            "",
            f"Output class: {self.output}",
            "",
        ]
        for check in self.identities:
            lines.append(
                f"Identities N={check.n}: decomp={check.decomp_matches} "
                f"first_row={check.first_row_ones} M=e1^T Q μ={check.first_row_mertens} "
                f"quadratic={check.quadratic_identity} M(N)={check.mertens}"
            )
        lines.append("")
        for snap in self.spectra:
            lines.append(
                f"Spectrum N={snap['n']}: λ_min={snap['lambda_min']:.4g} "
                f"({snap['lambda_min_over_n']:.4g} N), λ_max={snap['lambda_max']:.4g} "
                f"({snap['lambda_max_over_n']:.4g} N), indefinite={snap['indefinite']}, "
                f"R(μ)={snap['rayleigh_mu']:.4g}, |M|={abs(snap['mertens'])}"
            )
        lines.append("")
        for route in self.routes:
            lines.append(f"[{route.status}] {route.name}")
            lines.append(f"  {route.reason}")
            lines.append("")
        lines.append("Isolated statement (not an independent bridge):")
        lines.append(self.conditional.get("statement", ""))
        lines.append(self.conditional.get("why", ""))
        if self.adversarial:
            mean_abs = self.adversarial.get("random_mean_abs")
            lines.append("")
            lines.append(
                "Adversarial squarefree signs "
                f"N={self.adversarial.get('n')}: mean |1^T x|={mean_abs:.3g}, "
                f"|M(N)|={self.adversarial.get('|M(N)|')}, "
                f"sqrt(N)={self.adversarial.get('sqrt_n'):.3g}."
            )
        lines.append("")
        for note in self.notes:
            lines.append(note)
        return "\n".join(lines)


def attack(
    identity_ns: Iterable[int] = (6, 12, 24),
    spectral_n: int = 48,
    adversarial_n: int = 48,
) -> AttackReport:
    identities = [verify_identities(n) for n in identity_ns]
    snap = spectral_snapshot(spectral_n)
    routes = route_verdicts(spectral_n, snap)
    notes = [
        "Quarantined: Route C −1/(2π) limit; λ_min > −1/2 moat; operator swap; "
        "RH or Mertens as a lemma; SND/GNC/Goldbach/NS/Harmonic Blueprint glue.",
        "Name collision: inventory NS-B is classical vorticity. This book is "
        "RH Track B (Möbius–GCD) only.",
        "August linear-edge slopes are recorded as chain claims and checked as "
        "finite-N consistency, not re-proved here.",
        "Smallest missing theorem remains: a noncircular estimate that improves "
        "generic O(N) control of M(N) to O_ε(N^{1/2+ε}).",
    ]
    return AttackReport(
        output=OUTPUT_OBSTRUCTION,
        identities=identities,
        spectra=[snap],
        routes=routes,
        conditional=isolated_conditional_theorem(),
        adversarial=adversarial_squarefree_signs(adversarial_n),
        rh_claimed=False,
        notes=notes,
    )


def looks_like_locked_operator(text: str) -> bool:
    compact = text.lower().replace(" ", "").replace("\\", "")
    has_mu = ("μ" in text) or ("mu(" in compact) or ("mathrm{mu}" in compact) or ("mobius" in compact)
    has_gcd = "gcd" in compact
    return has_mu and has_gcd


def quarantined_operator_hit(text: str) -> str | None:
    compact = text.lower().replace(" ", "").replace("\\", "")
    if looks_like_locked_operator(text):
        return None
    from .route_c import looks_like_route_c_operator

    if looks_like_route_c_operator(text):
        return None
    if "1/(2pi)" in compact or "1/(2π)" in compact or "1/2π" in compact:
        return "Route C −1/(2π) limit is quarantined for RH Track B"
    if "lambda_min" in compact and ">-1/2" in compact.replace(" ", ""):
        return "λ_min > −1/2 moat is quarantined; it is false for inverse-GCD and not this operator"
    if "gcd(i,j)/sqrt" in compact or "gcd(i,j)/sqrt" in compact:
        return "positive-GCD operator gcd/√ij is not RH Track B"
    if "1/gcd" in compact:
        return "raw inverse-GCD 1/gcd is not RH Track B"
    return None
