"""Track B proof chain: each step as a shape, not a regularity close.

Classical Navier–Stokes, keep 1/r^4. A lemma pass is not continuation.
The domain shape stays open unless a closed estimate for X = ||ω||_2^2 exists.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final


NS_SHAPE: Final[dict[str, str]] = {
    "object": "classical 3D NS vorticity",
    "P": "Leray / div-free projector",
    "H": "advection + stretching (ω·∇)u",
    "psi": "ω (vorticity); swirl uses Γ = r u_θ, not Φ=Γ/r² as the unknown",
    "lam": "ν plus dyadic scale j / tube radius δ",
    "Phi": "X = ||ω||_2^2 — no closed bound",
    "E": "T^3 or axisymmetric tube; keep 1/r^4; no Q1",
}


@dataclass(frozen=True)
class ChainStep:
    step: str
    statement: str
    looks_like: str
    verdict: str
    shape_delta: str
    clip_id: str
    clip: str
    what_changes: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


STEPS: Final[tuple[ChainStep, ...]] = (
    ChainStep(
        step="B0 setup",
        statement="∂_t ω + (u·∇)ω = (ω·∇)u + ν Δω,  ∇·u = 0",
        looks_like="The object. Six-role skeleton. Φ is X, still unbounded a priori.",
        verdict="given",
        shape_delta="none — this IS the shape",
        clip_id="—",
        clip="none",
        what_changes="Nothing yet. Every later pass is judged against this skeleton.",
    ),
    ChainStep(
        step="B1",
        statement="∫ (u_≤j ·∇) u_j · u_j = 0  (periodic, div-free)",
        looks_like="Low self-flux into one dyadic block vanishes by parts.",
        verdict="pass",
        shape_delta="none",
        clip_id="—",
        clip="none",
        what_changes="Texture on H: low Bony piece is zero. Same object. T2 Lemma 1 only.",
    ),
    ChainStep(
        step="B1b",
        statement="Use an H^{2.3} absorbing ball as an input to the a priori estimate",
        looks_like="Assume already-regular data to get regularity.",
        verdict="fail",
        shape_delta="would add a hidden hypothesis into E (already small/smooth)",
        clip_id="CLIP-B1b-H23",
        clip="extra assumption: start inside an H^{2.3} ball",
        what_changes="Shape would become a different, conditional PDE problem. Clipped off. Not used.",
    ),
    ChainStep(
        step="B2",
        statement="σ = P_{j*}/X;  σ≥1/2 (3-CONC) or σ≤1/2 (SPREAD) covers (0,1]",
        looks_like="A partition of mass. Two regimes, no gap.",
        verdict="pass",
        shape_delta="none",
        clip_id="—",
        clip="none",
        what_changes="Texture on λ: a selector of scales. Not dynamics. Cover ≠ solution lives there.",
    ),
    ChainStep(
        step="B3",
        statement="3-shell support ⇒ Bernstein + |∇ξ|_∞ ≤ C 2^{j*} on E_c",
        looks_like="One packet of three octaves. Ring bound on direction gradient.",
        verdict="pass",
        shape_delta="none",
        clip_id="—",
        clip="none",
        what_changes="Texture on λ / local geometry. Still not stretching depletion.",
    ),
    ChainStep(
        step="B3b",
        statement="Ring ⇒ cos α_3 → 0 for all data",
        looks_like="Biot–Savart slogan: alignment for free.",
        verdict="fail",
        shape_delta="would insert depletion into H as if it were already in the object",
        clip_id="CLIP-B3b-ALIGN",
        clip="unjustified all-data alignment / stretching shutdown",
        what_changes="Fake upgrade of H. Clipped. Alignment is the open problem, not a lemma.",
    ),
    ChainStep(
        step="B4",
        statement="h(0)=0 ⇒ ∫ h²/r dr ≤ 4∫ (h')² r dr + 2 h(δ)²",
        looks_like="Localized Hardy on a tube, with a wall term at r=δ.",
        verdict="pass",
        shape_delta="none on the PDE; a tool appears in E",
        clip_id="CLIP-B4-WALL",
        clip="wall remainder 2 h(δ)² — ID'd, not absorbed yet",
        what_changes="New measured piece in E (geometry of the tube). Hardy is a tool, not I_tube.",
    ),
    ChainStep(
        step="B4b",
        statement="tube Hardy absorbs |I_tube| into ν‖∇ω‖_2² for all data",
        looks_like="The live weld: Hardy + wall ⇒ the 1/r^4 swirl source is controlled.",
        verdict="open",
        shape_delta="would tighten Φ (X controlled by viscosity) IF it closed",
        clip_id="CLIP-B4b-ITUBE",
        clip="I_tube itself — still unmeasured as a bound",
        what_changes="This is the first step that could actually change Φ. Not done.",
    ),
    ChainStep(
        step="B5",
        statement="axisymmetric (Δu)_θ = Δu_θ − u_θ/r²",
        looks_like="Angular viscosity identity. Extra 1/r² sits in the same tube as 1/r^4.",
        verdict="pass",
        shape_delta="none",
        clip_id="—",
        clip="none",
        what_changes="Texture on λ: the viscous operator has a cylindrical extra piece. Identity only.",
    ),
    ChainStep(
        step="B5b",
        statement="angular 1/r² viscosity dominates I_tube at δ ∼ 2^{-j*}",
        looks_like="Why we kept 1/r^4. Viscosity vs swirl source, same tube.",
        verdict="open",
        shape_delta="would identify CLIP-B4b with the B5 extra viscosity",
        clip_id="CLIP-B5b-VS-VISC",
        clip="same I_tube, now asked to lose to angular viscosity",
        what_changes="Shape of Φ still open. Canceling to Φ=Γ/r² is refused (moves work to ‖Φ‖_∞).",
    ),
    ChainStep(
        step="B6",
        statement="∫ X dt < ∞  ⇒  X ∈ L^∞",
        looks_like="Leray energy closes the cubic enstrophy ODE by itself.",
        verdict="fail",
        shape_delta="would upgrade Φ from integrable to bounded — a fake promotion",
        clip_id="CLIP-B6-SPIKE",
        clip="X ∼ (T*−t)^{-1/2}: integrable and unbounded",
        what_changes="The clip shows the shape of Φ does NOT upgrade. Energy is not L^∞.",
    ),
    ChainStep(
        step="B-Φ",
        statement="Switch the unknown to Φ_θ = Γ/r²",
        looks_like="Algebra 1/r^4 ∂_z(Γ²) = ∂_z(Φ_θ²). Looks cleaner.",
        verdict="fail",
        shape_delta="would change ψ from Γ to Φ_θ",
        clip_id="CLIP-PHI-LINFTY",
        clip="the estimate is dumped onto ‖Φ_θ‖_∞",
        what_changes="Same object, worse unknown. Keep Γ. Clip the change of unknown.",
    ),
    ChainStep(
        step="B-reg",
        statement="classical 3D NS is globally regular (this chain, no Q1)",
        looks_like="Continuation: X stays finite.",
        verdict="open",
        shape_delta="would fill Φ with a closed bound — the only domain-level shape change",
        clip_id="CLIP-B-REG",
        clip="the missing closed estimate for X",
        what_changes="Domain B stays the same shape: Φ is still open. Lemma passes did not finish it.",
    ),
)


def ns_chain() -> dict[str, Any]:
    return {
        "book": "B",
        "not_a_regularity_proof": True,
        "domain_verdict": "open",
        "skeleton": dict(NS_SHAPE),
        "rule": (
            "A pass adds texture or a named clip. It does not change the NS object "
            "unless Φ gets a closed bound. Failures are clipped hypotheses or fake upgrades."
        ),
        "steps": [s.to_dict() for s in STEPS],
        "counts": {
            "pass": sum(1 for s in STEPS if s.verdict == "pass"),
            "fail": sum(1 for s in STEPS if s.verdict == "fail"),
            "open": sum(1 for s in STEPS if s.verdict == "open"),
            "given": sum(1 for s in STEPS if s.verdict == "given"),
        },
        "how_shape_moves": [
            "B0: skeleton frozen.",
            "B1–B3, B5: same shape, new textures (flux identity, cover, Bernstein, cylindrical Laplacian).",
            "B1b, B3b, B6, B-Φ: attempted shape hacks. Clipped and failed.",
            "B4: tool + wall clip CLIP-B4-WALL. PDE shape unchanged.",
            "B4b / B5b: live welds. These are the only pending shape-tightening of Φ.",
            "B-reg: still open. Φ not filled. Domain shape unchanged.",
        ],
        "next": "T3a Young trace is in. Write T5 I_tube carrying CLIP-T3-WELD. Then energy-class low Bony T. Do not pass regularity.",
    }


def format_ns_chain(report: dict[str, Any] | None = None) -> str:
    data = report or ns_chain()
    sk = data["skeleton"]
    lines = [
        "Track B chain — classical NS (not a regularity proof)",
        f"Domain verdict: {data['domain_verdict']}.",
        "",
        "Frozen skeleton (the shape that almost never changes)",
        f"  object: {sk['object']}",
        f"  P: {sk['P']}",
        f"  H: {sk['H']}",
        f"  ψ: {sk['psi']}",
        f"  λ: {sk['lam']}",
        f"  Φ: {sk['Phi']}",
        f"  E: {sk['E']}",
        "",
        data["rule"],
        "",
    ]
    for step in data["steps"]:
        lines.append(f"── {step['step']}  [{step['verdict']}]")
        lines.append(f"   {step['statement']}")
        lines.append(f"   looks like: {step['looks_like']}")
        lines.append(f"   shape delta: {step['shape_delta']}")
        lines.append(f"   clip: {step['clip_id']}  {step['clip']}")
        lines.append(f"   {step['what_changes']}")
        lines.append("")
    lines.append("How the shape moved")
    for line in data["how_shape_moves"]:
        lines.append(f"  - {line}")
    lines.append("")
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
