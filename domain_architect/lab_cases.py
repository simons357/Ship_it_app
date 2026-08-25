"""Lab strings and leftover pieces DA may look at. Not a structure map.

Ring SND is the usable Spectral Non-Dispersal criterion (still claimed
as conditional). Q6 ``H_N`` is the standing arithmetic definition.
The three NS leftovers are the parts that still fail. These are
different books. Live DA must not glue them.
"""

from __future__ import annotations

from typing import TypedDict


# Parser-safe threshold form of inf_t J(t)/X(t) ≥ c_* > 0.
# The infimum and the time argument are in the warning, not in the AST.
RING_SND_LAB = "J/X >= cstar"

# Parser-safe form of H_N = D^{-1/2} Q̃_N D^{-1/2}.
# D^((-1)/2) is required: D^(-1/2) would parse as (D^{-1})/2.
Q6_HN_LAB = "HN = D^((-1)/2)*Qtilde*D^((-1)/2)"

SWIRL_IDENTITY_LAB = "(1/r^4)*dz(Gamma^2) = dz(Phi^2)"
SWIRL_LEFTOVER_LAB = "Istrain = urad/r"
SIMPLEX_LEFTOVER_LAB = "ell1(a - mu) = 0"


def tokens_look_like_ring_snd(tokens: list[str]) -> bool:
    s = set(tokens)
    return "cstar" in s and "J" in s and "X" in s


def tokens_look_like_q6_hn(tokens: list[str]) -> bool:
    s = set(tokens)
    return "Qtilde" in s or "HN" in s


def tokens_look_like_swirl_leftover(tokens: list[str]) -> bool:
    return "urad" in set(tokens)


def tokens_look_like_simplex_leftover(tokens: list[str]) -> bool:
    return "ell1" in set(tokens)


def leftover_family(tokens: list[str]) -> str | None:
    """Which leftover book a token list belongs to, if any."""
    if tokens_look_like_ring_snd(tokens):
        return "ring"
    if tokens_look_like_q6_hn(tokens):
        return "q6"
    if tokens_look_like_swirl_leftover(tokens):
        return "swirl"
    if tokens_look_like_simplex_leftover(tokens):
        return "simplex"
    return None


RING_SND_WARNINGS = (
    "This is Ring-book SND: inf J/X ≥ c_*. It is not Paper2 "
    "operator-norm SND, not GNC, and not Bridge. Unconditional "
    "SND for large H¹ data is still open.",
)

Q6_HN_WARNINGS = (
    "This is the Q6 definition of H_N = D^{-1/2} Q̃_N D^{-1/2}. "
    "It is not FRA coupling H, not Paper2 H_N[a] = Σ a_j B_j, and "
    "not a fluids Theorem H. The all-N floor λ_min(H_N) > -1/2 "
    "is withdrawn.",
    "D here is the degree matrix of the inverse-GCD graph, not a "
    "wave operator and not a dissipation coefficient.",
)

SWIRL_LEFTOVER_WARNINGS = (
    "This is the swirl leftover I_strain = u^r/r. Energy does not "
    "bound ∫||u^r/r||_∞ dt. Classical unaugmented swirl is still "
    "open. Not Ring SND and not Paper2 simplex.",
)

SIMPLEX_LEFTOVER_WARNINGS = (
    "This is Paper2 leftover ||a-μ||_ℓ¹. Leray boundedness is not "
    "simplex smallness. The simplex lemma is still open. Not Ring "
    "SND and not swirl strain.",
)

BOTH_BOOKS_WARNING = (
    "Ring SND and Q6 H_N are in different books. Do not glue them. "
    "A shared 'spectrum concentration' shape is not a structure map T."
)

DIFFERENT_LEFTOVER_WARNING = (
    "These leftovers share a role (independent concentration / "
    "smallness) but not an estimate. Do not identify them. DA "
    "refuses a letter map."
)

SND_VS_H_NOTES = (
    "Ring SND and Q6 H_N are in different books. This lab does not glue them.",
    "Usable SND (Ring, still claimed as a conditional criterion): "
    "inf_t J(t)/X(t) ≥ c_* > 0, with X = ||∇u||_{L²}² total enstrophy "
    "and J the dominant Littlewood–Paley shell. Unconditional SND for "
    "large H¹ data is open. This is not Paper2 operator-norm SND, not "
    "GNC, and not Bridge.",
    "Usable theory H (Q6 definition stands): "
    "H_N = D^{-1/2} Q̃_N D^{-1/2}. The all-N floor λ_min(H_N) > -1/2 "
    "is withdrawn. Dark-state ⇔ Goldbach is withdrawn. Navier–Stokes "
    "from these matrices is withdrawn. This is not FRA coupling H, not "
    "Paper2 H_N[a] = Σ a_j B_j, and not a fluids Theorem H.",
    "Human shape observation, not a structure map T: both talk about "
    "whether a spectrum is concentrated or mixed (enstrophy shells vs "
    "an arithmetic matrix spectrum). DA has no executable T, so the "
    "correspondence stays analogy.",
    "They can coexist without being multiplied: Ring SND is a fluids "
    "shell-mass diagnostic; H_N is an arithmetic mixing matrix. The "
    "shared protocol is leftover-split, not a joint operator.",
)


class LeftoverSpec(TypedDict):
    id: str
    book: str
    name: str
    works: str
    works_lab: str
    fails: str
    fails_lab: str
    missing_role: str
    put_back: str
    status: str


# The three NS pieces that still fail. Keep this list at three.
NS_LEFTOVERS: tuple[LeftoverSpec, ...] = (
    {
        "id": "swirl-strain",
        "book": "B — axisymmetric swirl",
        "name": "strain leftover",
        "works": (
            "Algebraic identity (1/r^4)∂_z(Γ²)=∂_z(Φ²) and the Γ "
            "maximum principle."
        ),
        "works_lab": SWIRL_IDENTITY_LAB,
        "fails": (
            "∫||u^r/r||_∞ dt is not bounded by energy. The strain "
            "pairing is not absorbed uniformly."
        ),
        "fails_lab": SWIRL_LEFTOVER_LAB,
        "missing_role": "independent smallness of the intensive strain u^r/r",
        "put_back": (
            "If ∫||u^r/r||_∞ dt < ∞ then continuation of the unaugmented "
            "swirl class closes. Keep the identity. Leave the integral OPEN."
        ),
        "status": "OPEN",
    },
    {
        "id": "ring-snd",
        "book": "Ring lemma + SND",
        "name": "unconditional SND leftover",
        "works": (
            "Ring lemma as a *conditional* criterion: if inf J/X ≥ c_* "
            "then the dominant-shell estimates run."
        ),
        "works_lab": RING_SND_LAB,
        "fails": (
            "Energy / enstrophy boundedness does not give inf J/X ≥ c_* "
            "for arbitrary large H¹ data."
        ),
        "fails_lab": RING_SND_LAB,
        "missing_role": "independent spectral non-dispersal of enstrophy",
        "put_back": (
            "If inf J/X ≥ c_* then the Ring/T2-conditional estimates run. "
            "Unconditional SND stays OPEN. Do not glue this to Paper2 "
            "operator-norm SND."
        ),
        "status": "OPEN",
    },
    {
        "id": "paper2-simplex",
        "book": "D — Paper2 SND/GNC",
        "name": "simplex leftover",
        "works": (
            "Lipschitz continuity of a ↦ H_N[a] and Weyl as a "
            "*conditional* perturbation fact."
        ),
        "works_lab": "",
        "fails": (
            "Leray energy boundedness does not give ||a(t)-μ||_ℓ¹ small. "
            "T2 Closed Gronwall is withdrawn."
        ),
        "fails_lab": SIMPLEX_LEFTOVER_LAB,
        "missing_role": "independent simplex closeness of shell weights to μ",
        "put_back": (
            "If ||a-μ||_ℓ¹ is small enough then the frozen-gap Weyl "
            "perturbation keeps evolving λ_min above -1/2. That is "
            "Paper2 Lemma 6.1 (simplex / SND stability), still OPEN. "
            "Do not accept §7 'T2 Closed'. This H_N[a] is not Q6 H_N."
        ),
        "status": "OPEN",
    },
)

LEFTOVER_SPLIT_STEPS = (
    "Isolate the leftover: the smallness that energy / coercivity does not give.",
    "Decompose that leftover as its own system. Do not decompose the whole theorem as if the leftover were already closed.",
    "Name the missing role (independent concentration / smallness constraint) without naming a shared estimate.",
    "Reconstruct the main problem as: coercive part (keep) + independent diagnostic (hypothesis) ⇒ the rest of the estimates close.",
    "Put that conditional theorem back into each original book separately. Leave each diagnostic OPEN. Do not set σ_swirl = σ_ring = σ_simplex = σ_H.",
)
