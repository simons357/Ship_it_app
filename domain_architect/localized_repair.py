"""Localized reparation: excise step k of an n-step chain and graft an honest hook.

This is surgical leftover-split on a numbered chain. If a proof has n steps
and some step k is not working, Domain Architect excises that step, keeps
the tissue on both sides of the cut, searches a finite catalog for the most
logical hook, and re-inserts a graft at the same slot. k is an index, not
a product. The graft may be an OPEN hypothesis. It is not a closed theorem.

Default dataset: the classical unaugmented NS chain (9 program steps).
Controlling face: August repaired TeX. Named protocol (no --excise) cuts
the OPEN dynamical leftover 7–8 (simplex + dynamic SND). Step 2 is the
Ring Lemma and is already PROVED. Any other k is ``localized_repair(excise=k)``.

This does not close Navier–Stokes. It does not call inverse design.
It does not glue Ring-book fluids SND (J/X) with Paper2 operator SND.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from .cycle import CycleReport
from .decompose import decompose
from .lab_cases import RING_SND_LAB, SIMPLEX_LEFTOVER_LAB
from .schema import CorrespondenceKind, ValidationGate
from .synthesize import CandidateArchitecture, Provenance
from .translate import translate_refuse_glue


# Paper safety margin in the manuscript. Not an all-N theorem.
DELTA_0 = 0.20
# August 1 audit: local existence gives 2; the target quoted there is 0.039.
# That is δ_0 / C_N with C_N ≈ 5.13, not a certified Lipschitz bound.
ETA_STAR_AUDIT = 0.039
LOCAL_EXISTENCE_L1 = 2.0
SIMPLEX_N = 32
SIMPLEX_SAMPLES = 400
SIMPLEX_SEED = 20260825

REFUSED = (
    "no letter map J→H / urad→J / a→HN",
    "no TRANSFORMABLE stamp",
    "no structure_preserving_equivalence",
    "no PD / inverse-design control loop",
    "no Clay / unaugmented regularity claim",
    "no treating local existence ||a-μ||_1 ≤ 2 as the 0.039 bound",
    "no treating energy as simplex smallness",
    "no glue of Ring J/X or Q6 H_N into Paper2 H_N[a]",
    "no identifying NS-6 ring geometry with Ring-book inf J/X",
    "no treating Ring Lemma (NS-6) as Clay Statement B",
    "no accepting §7 T2 Closed",
    "no claiming Lemma 6.1 is proved by this graft",
)


@dataclass
class ProofStep:
    """One numbered step in a proof chain."""

    index: int
    id: str
    status: str  # healthy | diseased | open | not_claimed
    claim: str
    provides: str
    requires: str
    source: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "id": self.id,
            "status": self.status,
            "claim": self.claim,
            "provides": self.provides,
            "requires": self.requires,
            "source": self.source,
            "notes": self.notes,
        }


@dataclass
class GraftCandidate:
    """A possible hook into the cut. Ranking is interface fit, not a proof."""

    id: str
    name: str
    kind: str  # hypothesis | estimate | diagnostic | refused
    provides: str
    score: float
    accepted: bool
    closed: bool
    reason: str
    computation: dict[str, Any] | None = None
    refused_because: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "provides": self.provides,
            "score": self.score,
            "accepted": self.accepted,
            "closed": self.closed,
            "reason": self.reason,
        }
        if self.computation is not None:
            payload["computation"] = self.computation
        if self.refused_because is not None:
            payload["refused_because"] = self.refused_because
        return payload


# ---------------------------------------------------------------------------
# Classical unaugmented NS chain (9 program steps). Controlling face:
# August repaired TeX. Not the June FIXED PDF compile. Named protocol
# cuts leftover 7–8. Step 2 is Ring Lemma (NS-6), already PROVED.
# NS-11 / Clay Statement B is not a program step; it is not claimed.
# ---------------------------------------------------------------------------

PAPER2_CHAIN: tuple[ProofStep, ...] = (
    ProofStep(
        index=1,
        id="leray-energy",
        status="healthy",
        claim=(
            "Leray–Hopf energy inequality: a(t) exists on the simplex "
            "(boundedness, not smallness)."
        ),
        provides="a(t) ∈ Δ_{N-1}",
        requires="periodic 3D NS on T^3",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 1",
        notes="STANDARD / INHERITED. Boundedness is not closeness to μ.",
    ),
    ProofStep(
        index=2,
        id="ring-lemma-ns6",
        status="healthy",
        claim=(
            "Ring Lemma (NS-6): static three-shell lower bound for "
            "Q_N / H_N geometry."
        ),
        provides="static three-shell lower bound on Q_N / H_N geometry",
        requires="GCD / shell operator geometry",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 2",
        notes=(
            "PROVED standalone; not Clay alone. This is not Ring-book "
            "fluids inf J/X ≥ c_* unless the source says so."
        ),
    ),
    ProofStep(
        index=3,
        id="lemma-3-1-continuity",
        status="healthy",
        claim=(
            "Finite-N operator continuity (Lemma 3.1): "
            "||H_N[a]-H_N[b]||_op ≤ C_N ||a-b||_1."
        ),
        provides="C_N Lipschitz constant (finite N, triangle inequality)",
        requires="finite-N shell operator H_N[a]",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 3",
        notes="PROVED Lipschitz. Paper2 H_N[a] is not Q6 H_N.",
    ),
    ProofStep(
        index=4,
        id="frozen-gap-route-j",
        status="open",
        claim=(
            "Frozen gap (Route J): λ_min(Ĥ_N^μ) > -1/2 + δ_0 for tested "
            "N ≤ 800. No analytic all-N claim."
        ),
        provides="δ_0 > 0 frozen at μ (numerical / under audit)",
        requires="equidistributed μ_j = 1/N",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 4",
        notes="NUMERICAL / UNDER AUDIT. Frozen gap is step 4, not step 2.",
    ),
    ProofStep(
        index=5,
        id="weyl-master",
        status="healthy",
        claim=(
            "Weyl master implication (Paper2 Thm): quantitative SND + "
            "frozen gap ⇒ dynamic spectral gap "
            "inf_t λ_min(H_N[u(t)]) > -1/2."
        ),
        provides="conditional dynamic spectral gap",
        requires="FG and quantitative operator-norm SND",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 5",
        notes="PROVED conditional on SND + FG. Not a proof that SND holds.",
    ),
    ProofStep(
        index=6,
        id="conditional-h1",
        status="healthy",
        claim=(
            "Global summation / conditional H^1 bound (NS-7, NS-8): if "
            "[SND] holds for all t, then dangerous-regime time is finite "
            "and global H^1 follows."
        ),
        provides="conditional global H^1",
        requires="[SND] for all t",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 6",
        notes="PROVED conditional on [SND]. Not unconditional regularity.",
    ),
    ProofStep(
        index=7,
        id="lemma-6-1-simplex",
        status="open",
        claim=(
            "SND simplex stability (Lemma 6.1): ||a(t)-μ||_1 ≤ η_N "
            "uniform in t for classical Leray–Hopf."
        ),
        provides="the smallness Weyl actually needs",
        requires="NS dynamics of a(t), not energy",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 7",
        notes="OPEN leftover. Do not treat as proved.",
    ),
    ProofStep(
        index=8,
        id="dynamic-snd-ns10",
        status="open",
        claim=(
            "Dynamic [SND] preservation (NS-10): unaugmented classical "
            "flow keeps ||H_N[u(t)]-Ĥ_N^μ||_op < δ_0 for all t ≥ 0."
        ),
        provides="uniform quantitative operator-norm SND",
        requires="classical unaugmented Leray–Hopf dynamics",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 8",
        notes="OPEN leftover. Not implied by energy or by ε→0.",
    ),
    ProofStep(
        index=9,
        id="continuation",
        status="open",
        claim=(
            "Continuation: spectral gap / non-concentration ⇒ smooth "
            "Leray–Hopf continuation (must be supplied explicitly)."
        ),
        provides="classical smoothness, if supplied",
        requires="uniform spectral gap plus an explicit continuation theorem",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md step 9",
        notes="OPEN / INCOMPLETE in repaired Paper2. Default surgery does not cut this.",
    ),
)

NOT_CLAIMED: tuple[ProofStep, ...] = (
    ProofStep(
        index=11,
        id="classical-ns-11",
        status="not_claimed",
        claim="Classical global regularity (NS-11 / Clay Statement B).",
        provides="Clay / Millennium",
        requires="the whole chain closed",
        source="NS_UNAUGMENTED_PROOF_CHAIN.md conclusion",
        notes="NOT CLAIMED. DA must not synthesize a PD loop to fill this.",
    ),
)

DEFAULT_CUT_IDS = {
    "lemma-6-1-simplex",
    "dynamic-snd-ns10",
    "lemma-6-1",
    "local-existence-as-target",
    "t2-closed",
    "toy-energy-implies-smallness",
}

LEFTOVER_IDS = {
    "lemma-6-1-simplex",
    "dynamic-snd-ns10",
    "lemma-6-1",
    "t2-closed",
    "local-existence-as-target",
}

RING_LEMMA_IDS = {"ring-lemma-ns6", "ring-lemma"}
FROZEN_GAP_IDS = {"frozen-gap-route-j", "frozen-gap"}


TOY_CHAIN: tuple[ProofStep, ...] = (
    ProofStep(
        index=1,
        id="toy-energy",
        status="healthy",
        claim="Coercive energy bound E(t) ≤ E(0).",
        provides="energy bound",
        requires="",
        source="toy chain for the n-step API",
        notes="Keep.",
    ),
    ProofStep(
        index=2,
        id="toy-energy-implies-smallness",
        status="diseased",
        claim="Energy implies the needed smallness σ.",
        provides="σ small",
        requires="energy bound",
        source="toy chain",
        notes="Example of a diseased step (here k=2 on the toy chain).",
    ),
    ProofStep(
        index=3,
        id="toy-continuation",
        status="healthy",
        claim="If σ is small then continuation closes.",
        provides="conditional continuation",
        requires="σ small",
        source="toy chain",
        notes="Keep. Hook an independent σ, do not derive it from energy.",
    ),
)


CHAINS: dict[str, tuple[ProofStep, ...]] = {
    "paper2": PAPER2_CHAIN,
    "classical": PAPER2_CHAIN,
    "unaugmented": PAPER2_CHAIN,
    "toy": TOY_CHAIN,
    "toy-excise-2": TOY_CHAIN,
}


def _simplex_l1_to_barycenter(weights: list[float]) -> float:
    n = len(weights)
    mu = 1.0 / n
    return sum(abs(x - mu) for x in weights)


def _uniform_simplex_point(n: int, rng: random.Random) -> list[float]:
    """Dirichlet(1,…,1) via exponential spacings. Stdlib only."""
    xs = [rng.expovariate(1.0) for _ in range(n)]
    total = sum(xs)
    return [x / total for x in xs]


def simplex_concentration_diagnostic(
    n: int = SIMPLEX_N,
    samples: int = SIMPLEX_SAMPLES,
    seed: int = SIMPLEX_SEED,
    eta_star: float = ETA_STAR_AUDIT,
) -> dict[str, Any]:
    """Finite Monte Carlo: a typical simplex point is not η_*-close to μ.

    This is a diagnostic computation, not a proof of Lemma 6.1 and not a
    disproof. It shows the leftover is not ‘what random a already satisfy.’
    """
    rng = random.Random(seed)
    distances = [
        _simplex_l1_to_barycenter(_uniform_simplex_point(n, rng))
        for _ in range(samples)
    ]
    mean = sum(distances) / samples
    hits = sum(1 for d in distances if d <= eta_star)
    return {
        "n": n,
        "samples": samples,
        "seed": seed,
        "eta_star": eta_star,
        "mean_l1": mean,
        "min_l1": min(distances),
        "max_l1": max(distances),
        "fraction_within_eta_star": hits / samples,
        "local_existence_bound": LOCAL_EXISTENCE_L1,
        "local_existence_over_eta_star": LOCAL_EXISTENCE_L1 / eta_star,
        "reading": (
            "Random a on Δ_{N-1} have ||a-μ||_1 of order 1, not ≤ η_*. "
            "Local existence bound 2 is the simplex diameter scale, not the "
            "Weyl target. This computation does not prove Lemma 6.1."
        ),
    }


def _simplex_catalog(computation: dict[str, Any]) -> list[GraftCandidate]:
    eta = ETA_STAR_AUDIT
    gap = LOCAL_EXISTENCE_L1 / eta
    return [
        GraftCandidate(
            id="independent-simplex-hypothesis",
            name="Lemma 6.1 as an independent OPEN hypothesis",
            kind="hypothesis",
            provides=f"||a(t)-μ||_1 ≤ {eta} uniformly in t (assumed, not proved)",
            score=1.0,
            accepted=True,
            closed=False,
            reason=(
                "This is the interface Weyl actually needs after Lipschitz. "
                "It is the honest hook: keep Lemma 3.1 and Theorem 4.1, "
                "re-insert 6.1 as a hypothesis, leave it OPEN."
            ),
        ),
        GraftCandidate(
            id="local-existence-bound-2",
            name="Local existence ||a-μ||_1 ≤ 2",
            kind="estimate",
            provides=f"||a-μ||_1 ≤ {LOCAL_EXISTENCE_L1}",
            score=0.0,
            accepted=False,
            closed=False,
            reason=(
                f"Interface fail: {LOCAL_EXISTENCE_L1} is about {gap:.1f}× "
                f"the audit target {eta}. Local existence is a diameter bound, "
                "not simplex smallness."
            ),
            computation={
                "bound": LOCAL_EXISTENCE_L1,
                "eta_star_audit": eta,
                "ratio": gap,
            },
        ),
        GraftCandidate(
            id="leray-energy",
            name="Leray energy / enstrophy boundedness",
            kind="estimate",
            provides="a(t) ∈ Δ_{N-1}",
            score=0.0,
            accepted=False,
            closed=False,
            reason=(
                "Energy puts a on the simplex. It does not put a near μ. "
                "Same leftover *shape* as swirl ∫||u^r/r||_∞ dt; not the "
                "same estimate."
            ),
        ),
        GraftCandidate(
            id="dirichlet-random-samples",
            name="Dirichlet(1,…,1) samples on the simplex",
            kind="diagnostic",
            provides="typical ||a-μ||_1 (order 1, not ≤ η_*)",
            score=0.15,
            accepted=False,
            closed=False,
            reason=(
                "A bounded search over random simplex points. They are not "
                "inside the Weyl ball. Useful as a negative diagnostic, not "
                "as a graft."
            ),
            computation=computation,
        ),
        GraftCandidate(
            id="ring-snd-glue",
            name="Glue Ring SND inf J/X ≥ c_*",
            kind="refused",
            provides="J/X (different book)",
            score=0.0,
            accepted=False,
            closed=False,
            reason="Different book. Ring SND is not Paper2 operator-norm SND.",
            refused_because="different_books",
        ),
        GraftCandidate(
            id="q6-hn-floor",
            name="Glue withdrawn Q6 floor λ_min(H_N) > -1/2",
            kind="refused",
            provides="arithmetic H_N (different object)",
            score=0.0,
            accepted=False,
            closed=False,
            reason=(
                "Q6 H_N = D^{-1/2} Q̃_N D^{-1/2} is not Paper2 H_N[a]. "
                "The all-N floor is withdrawn."
            ),
            refused_because="different_books_and_withdrawn",
        ),
        GraftCandidate(
            id="pd-inverse-design",
            name="Inverse-design a PD loop to force smallness",
            kind="refused",
            provides="refused PD loop (A13 closed)",
            score=0.0,
            accepted=False,
            closed=False,
            reason="A13: inverse design of NS regularity is fail-closed. Do not emit a PD loop as a repair.",
            refused_because="a13_fail_closed",
        ),
    ]


def _ring_geometry_catalog() -> list[GraftCandidate]:
    return [
        GraftCandidate(
            id="independent-ring-geometry-hypothesis",
            name="NS-6 Ring Lemma as an independent OPEN hypothesis",
            kind="hypothesis",
            provides=(
                "static three-shell lower bound for Q_N / H_N geometry "
                "(assumed after the cut, not used as Clay)"
            ),
            score=1.0,
            accepted=True,
            closed=False,
            reason=(
                "Generic excise-k at slot 2. On this chain step 2 is the "
                "Ring Lemma (NS-6), already PROVED. Cutting it re-inserts "
                "an OPEN ring-geometry hypothesis. Neighbors are Leray "
                "energy (1) and Lemma 3.1 (3). This does not prove Clay "
                "Statement B. This is not Ring-book fluids inf J/X ≥ c_*."
            ),
        ),
        GraftCandidate(
            id="ring-snd-glue",
            name="Glue Ring SND inf J/X ≥ c_*",
            kind="refused",
            provides="J/X (different book)",
            score=0.0,
            accepted=False,
            closed=False,
            reason="Different book. Ring-book fluids SND is not NS-6 operator geometry.",
            refused_because="different_books",
        ),
        GraftCandidate(
            id="clay-from-ring-lemma",
            name="Treat NS-6 as a Clay proof",
            kind="refused",
            provides="nothing (standalone geometry is not Statement B)",
            score=0.0,
            accepted=False,
            closed=False,
            reason="Standalone Ring Lemma is not Clay Statement B.",
            refused_because="not_clay",
        ),
        GraftCandidate(
            id="pd-inverse-design",
            name="Inverse-design a PD loop",
            kind="refused",
            provides="vacuous controller",
            score=0.0,
            accepted=False,
            closed=False,
            reason="A13 fail-closed. Not a proof of the excised step.",
            refused_because="a13_fail_closed",
        ),
    ]


def _frozen_gap_catalog() -> list[GraftCandidate]:
    return [
        GraftCandidate(
            id="independent-frozen-gap-hypothesis",
            name="Frozen gap as an independent OPEN hypothesis",
            kind="hypothesis",
            provides="δ_0 > 0 at μ (assumed, not proved for all N)",
            score=1.0,
            accepted=True,
            closed=False,
            reason=(
                "On the classical chain, frozen gap / Route J is step 4, "
                "not step 2. The honest hook is to keep it as a hypothesis "
                "feeding Weyl, not to stamp it a theorem."
            ),
        ),
        GraftCandidate(
            id="route-j-numerics",
            name="Route J numerics N ≤ 800",
            kind="diagnostic",
            provides="numerical λ_min near -0.30 for tested N",
            score=0.25,
            accepted=False,
            closed=False,
            reason="Finite-N numerics are not an all-N frozen-gap theorem.",
        ),
        GraftCandidate(
            id="q6-hn-floor",
            name="Withdrawn Q6 all-N floor",
            kind="refused",
            provides="wrong H_N",
            score=0.0,
            accepted=False,
            closed=False,
            reason="Different matrix, withdrawn claim.",
            refused_because="different_books_and_withdrawn",
        ),
        GraftCandidate(
            id="pd-inverse-design",
            name="Inverse-design a PD loop",
            kind="refused",
            provides="vacuous controller",
            score=0.0,
            accepted=False,
            closed=False,
            reason="A13 fail-closed. Not a spectral-gap proof.",
            refused_because="a13_fail_closed",
        ),
    ]


def _toy_catalog() -> list[GraftCandidate]:
    return [
        GraftCandidate(
            id="independent-smallness-hypothesis",
            name="Independent smallness σ (OPEN hypothesis)",
            kind="hypothesis",
            provides="σ small, not derived from energy",
            score=1.0,
            accepted=True,
            closed=False,
            reason="Keep energy. Hook σ independently. Continuation still needs σ.",
        ),
        GraftCandidate(
            id="energy-implies-smallness",
            name="Derive σ from energy",
            kind="estimate",
            provides="nothing (this was the diseased step)",
            score=0.0,
            accepted=False,
            closed=False,
            reason="That implication is what was excised.",
        ),
        GraftCandidate(
            id="pd-inverse-design",
            name="PD loop",
            kind="refused",
            provides="vacuous controller",
            score=0.0,
            accepted=False,
            closed=False,
            reason="A13 fail-closed.",
            refused_because="a13_fail_closed",
        ),
    ]


def _generic_interface_catalog(excised: list[ProofStep]) -> list[GraftCandidate]:
    labels = ", ".join(s.id for s in excised) or "cut"
    return [
        GraftCandidate(
            id="independent-interface-hypothesis",
            name=f"Independent OPEN hypothesis at the {labels} interface",
            kind="hypothesis",
            provides="whatever the distal step requires (assumed, not proved)",
            score=1.0,
            accepted=True,
            closed=False,
            reason=(
                "Honest hook for an arbitrary cut: re-state the missing "
                "interface as a hypothesis. This is not a proof of the "
                "excised claim."
            ),
        ),
        GraftCandidate(
            id="pd-inverse-design",
            name="Inverse-design a PD loop",
            kind="refused",
            provides="vacuous controller",
            score=0.0,
            accepted=False,
            closed=False,
            reason="A13 fail-closed. Not a proof of the excised step.",
            refused_because="a13_fail_closed",
        ),
    ]


def _catalog_for(chain_name: str, excised: list[ProofStep]) -> list[GraftCandidate]:
    ids = {s.id for s in excised}
    if chain_name.startswith("toy"):
        return _toy_catalog()
    if ids & RING_LEMMA_IDS and not (ids & LEFTOVER_IDS):
        return _ring_geometry_catalog()
    if ids & FROZEN_GAP_IDS and not (ids & LEFTOVER_IDS):
        return _frozen_gap_catalog()
    if ids & LEFTOVER_IDS:
        return _simplex_catalog(simplex_concentration_diagnostic())
    return _generic_interface_catalog(excised)


def _normalize_excise(
    steps: tuple[ProofStep, ...],
    excise: list[int] | int | None,
) -> list[int]:
    if excise is None:
        return [
            s.index
            for s in steps
            if s.status in {"diseased", "open"} and s.id in DEFAULT_CUT_IDS
        ]
    if isinstance(excise, int):
        excise = [excise]
    indices = [int(i) for i in excise]
    valid = {s.index for s in steps}
    bad = [i for i in indices if i not in valid]
    if bad:
        raise ValueError(f"excise indices {bad} are not in the chain 1..{max(valid)}")
    return indices


def _neighbors(
    steps: tuple[ProofStep, ...],
    excised_indices: set[int],
) -> tuple[ProofStep | None, ProofStep | None]:
    """Last remaining step before the first cut, first remaining step after the last cut."""
    if not excised_indices:
        return None, None
    lo, hi = min(excised_indices), max(excised_indices)
    proximal = None
    distal = None
    for step in steps:
        if step.index < lo:
            proximal = step
        elif step.index > hi and distal is None:
            distal = step
    return proximal, distal


def _graft_step(chosen: GraftCandidate, index: int) -> ProofStep:
    return ProofStep(
        index=index,
        id=f"{chosen.id}-graft",
        status="open",
        claim=chosen.name,
        provides=chosen.provides,
        requires="independent of energy / local-existence diameter",
        source="localized reparation (graft)",
        notes=chosen.reason + " Status OPEN. Not a theorem.",
    )


def _mark_line(step: ProofStep, mark: str) -> str:
    return f"{step.index:>2}  {mark:<8}  {step.id}  [{step.status}]"


def chain_board(
    original: tuple[ProofStep, ...] | list[ProofStep],
    excised: list[ProofStep],
    repaired: list[ProofStep],
) -> dict[str, Any]:
    """Human-readable before/after of the numbered chain."""
    cut_ids = {s.id for s in excised}
    before = [
        _mark_line(step, "EXCISE" if step.id in cut_ids else "keep")
        for step in original
    ]
    after = [
        _mark_line(step, "GRAFT" if step.id.endswith("-graft") else "keep")
        for step in repaired
    ]
    text = "BEFORE\n" + "\n".join(before) + "\n\nAFTER\n" + "\n".join(after)
    return {"before": before, "after": after, "text": text}


def run_surgery(
    steps: tuple[ProofStep, ...],
    *,
    chain_name: str,
    excise: list[int] | int | None = None,
) -> dict[str, Any]:
    """Cut the named steps, rank hooks, re-insert the best honest graft."""
    excised_indices = set(_normalize_excise(steps, excise))
    excised = [s for s in steps if s.index in excised_indices]
    remaining = [s for s in steps if s.index not in excised_indices]
    proximal, distal = _neighbors(steps, excised_indices)
    candidates = _catalog_for(chain_name, excised)
    ranked = sorted(candidates, key=lambda c: (-c.score, c.id))
    chosen = next((c for c in ranked if c.accepted), None)
    if chosen is None:
        raise RuntimeError("localized reparation found no accepted graft")

    insert_at = min(excised_indices) if excised_indices else 0
    graft = _graft_step(chosen, insert_at)
    repaired: list[ProofStep] = []
    inserted = False
    for step in remaining:
        if not inserted and step.index > insert_at:
            repaired.append(graft)
            inserted = True
        repaired.append(step)
    if not inserted:
        repaired.append(graft)

    board = chain_board(steps, excised, repaired)
    slots = sorted(excised_indices)
    operation = {
        "excise": slots,
        "fix": (
            "Restore the cut interface with the best catalog hook. "
            "That hook is an OPEN hypothesis unless a real estimate fits. "
            "DA does not invent a proof of the excised claim."
        ),
        "fix_kind": "interface_graft",
        "fix_is_a_proof": False,
        "reinsert": insert_at,
        "neighbors": {
            "proximal_index": None if proximal is None else proximal.index,
            "distal_index": None if distal is None else distal.index,
        },
        "order_preserved": [s.index for s in repaired] == sorted(s.index for s in repaired),
    }
    answer = (
        f"Yes. DA excised step(s) {slots}, kept the healthy neighbors, "
        f"ranked a finite catalog, and re-inserted {chosen.id} at slot "
        f"{insert_at}. The graft is OPEN. Fix means restore the interface, "
        "not close the theorem."
    )

    return {
        "answer": answer,
        "protocol": "localized-reparation",
        "operation": operation,
        "board": board,
        "metaphor": (
            "Surgery: keep healthy tissue on both sides of the cut, "
            "excise the diseased step, hook the best logical graft to "
            "each end. The graft may be OPEN. This is not a closed proof."
        ),
        "chain_name": chain_name,
        "source_faces": [
            "docs/papers/ns-snd/NS_UNAUGMENTED_PROOF_CHAIN.md",
            "docs/papers/ns-snd/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex",
            "docs/papers/ns-snd/NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md",
            "docs/papers/ns-snd/FACES.md",
        ]
        if chain_name in {"paper2", "classical", "unaugmented"}
        else ["toy chain"],
        "controlling_face": (
            "docs/papers/ns-snd/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex"
            if chain_name in {"paper2", "classical", "unaugmented"}
            else None
        ),
        "not_june_fixed_compile": (
            "This chain is not the June FIXED PDF compile."
            if chain_name in {"paper2", "classical", "unaugmented"}
            else None
        ),
        "original_chain": [s.to_dict() for s in steps],
        "excised": [s.to_dict() for s in excised],
        "proximal": None if proximal is None else proximal.to_dict(),
        "distal": None if distal is None else distal.to_dict(),
        "not_claimed": [s.to_dict() for s in NOT_CLAIMED]
        if chain_name in {"paper2", "classical", "unaugmented"}
        else [],
        "interface": {
            "delta_0": DELTA_0,
            "eta_star_audit": ETA_STAR_AUDIT,
            "local_existence_l1": LOCAL_EXISTENCE_L1,
            "needed": (
                proximal.provides if proximal else ""
            )
            + "  →  graft  →  "
            + (distal.requires if distal else ""),
        },
        "candidates": [c.to_dict() for c in ranked],
        "chosen": chosen.to_dict(),
        "repaired_chain": [s.to_dict() for s in repaired],
        "closed": False,
        "refused": list(REFUSED),
        "validation_gate": ValidationGate.MATHEMATICAL.value,
        "kind": CorrespondenceKind.ANALOGY.value,
        "notes": [
            "Localized reparation does not prove Navier–Stokes regularity.",
            "Step 2 Ring Lemma (NS-6) is PROVED. Default surgery does not cut it.",
            "Lemma 3.1, Weyl master, and conditional H^1 stay.",
            "Default leftover cut is steps 7–8 (simplex + dynamic SND).",
            "Continuation (step 9) stays OPEN / INCOMPLETE.",
            "NS-11 / Clay Statement B is not claimed.",
            "A13: synthesize of NS regularity is fail-closed (no PD loop).",
            board["text"],
        ],
    }


def localized_repair(
    *,
    chain: str | None = None,
    excise: list[int] | int | None = None,
) -> dict[str, Any]:
    """Public entry: default classical leftover cut 7–8, or ``excise=k``."""
    name = (chain or "paper2").replace("_", "-")
    if name not in CHAINS:
        raise ValueError(
            f"unknown chain {name!r}; expected paper2, classical, unaugmented, toy"
        )
    if isinstance(excise, str):
        excise = [int(part) for part in excise.replace(" ", "").split(",") if part]
        if len(excise) == 1:
            excise = excise[0]
    if isinstance(excise, float) and excise == int(excise):
        excise = int(excise)
    if excise == []:
        excise = None
    return run_surgery(CHAINS[name], chain_name=name, excise=excise)


def cycle_localized_repair(
    *,
    chain: str | None = None,
    excise: list[int] | int | None = None,
) -> CycleReport:
    """Named cycle: surgical excision of step k on an n-step chain."""
    payload = localized_repair(chain=chain, excise=excise)
    simplex = decompose(SIMPLEX_LEFTOVER_LAB, name="paper2-simplex")
    ring = decompose(RING_SND_LAB, name="ring_snd")
    translation = translate_refuse_glue(
        simplex,
        ring,
        notes=[
            "Paper2 simplex leftover vs Ring SND",
            "Surgery does not glue these books.",
        ],
    )
    chosen = payload["chosen"]
    slots = payload["operation"]["excise"]
    insert_at = payload["operation"]["reinsert"]
    if len(slots) == 1:
        hypothesis = (
            f"Step {slots[0]} of an n-step chain is not working. "
            "Excise it. Restore the interface. Re-insert the best honest "
            f"catalog hook at slot {insert_at} as an OPEN hypothesis. "
            "This does not prove the excised claim."
        )
    else:
        hypothesis = (
            "Classical unaugmented surgery: cut the OPEN dynamical leftover "
            "7–8 (simplex + dynamic SND). Keep Ring Lemma (PROVED), Lipschitz, "
            "Weyl, and conditional H^1. Re-insert Lemma 6.1 / dynamic SND as "
            "an independent hypothesis. Continuation and Clay stay unclaimed."
        )
    candidate = CandidateArchitecture(
        name="localized_reparation_open",
        components=[
            "healthy proximal tissue (keep)",
            f"graft: {chosen['name']} (OPEN)",
            "healthy distal tissue (keep)",
        ],
        replaced={
            step["id"]: "excised"
            for step in payload["excised"]
        },
        hypothesis=hypothesis,
        provenance=[
            Provenance(
                source="localized reparation / surgery",
                original_domain="classical-unaugmented-ns",
                functional_role="constraint",
                translation=None,
                assumptions=[
                    "do not identify leftovers",
                    "do not glue J/X with operator SND",
                    "graft remains OPEN",
                ],
                compatibility_checks=["glue refused", "no executable T", "no PD"],
                modifications=[f"excised {step['id']}" for step in payload["excised"]],
                evidence=[chosen["id"]],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        ],
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "Not a PD controller. Inverse design is not used.",
            "Not TRANSFORMABLE. Not Clay.",
            "August repaired TeX is the controlling face. Not the June FIXED PDF compile.",
        ],
    )
    return CycleReport(
        mode="localized-repair",
        target=(
            "excise failing step(s) on a numbered chain, graft the honest "
            "OPEN hook, re-insert into the same chain"
        ),
        constraints=[
            "keep Ring Lemma (PROVED), Lemma 3.1, Weyl master, conditional H^1",
            "cut leftover 7–8, not step 2",
            "do not emit a PD loop",
            "do not glue books",
            "no Clay claim",
        ],
        decomposition=simplex,
        translation=translation,
        candidate=candidate,
        prediction=payload,
        residual=None,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            payload["answer"],
            payload["board"]["text"],
            payload["metaphor"],
            "Not a PD controller. Inverse design is not used.",
        ],
        method_credits=["localized reparation", "leftover-split protocol"],
    )
