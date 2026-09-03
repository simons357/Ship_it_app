"""Geometric analysis of Track B — architecture, not a regularity proof.

Four geometries sit on the same NS object:
  1. physical space (torus, axis, tube, wall)
  2. frequency space (dyadic shells, 3-packet, CONC/SPREAD)
  3. vorticity geometry (strain frame, alignment, superlevel E_c)
  4. swirl tube (Γ, 1/r^4 source, angular 1/r² viscosity)

A lemma is geometric when it estimates one of these. Regularity would be
a closed bound on X after the tube and the packet are controlled. That
weld is open.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final


DIAGRAMS: Final[dict[str, str]] = {
    "physical": """
        z
        |
  off   |   off     r ≥ δ   (I_off: standard Sobolev)
 -------+-------    r = δ   wall  CLIP-B4-WALL = 2 h(δ)²
  TUBE  |  TUBE     r < δ   I_tube ~ Γ ∂_z Γ / r^4
        |                   δ ∼ 2^{-j*}
        r
""",
    "frequency": """
  ...  j*-1 |  j*  | j*+1  ...
       \\______ 3-shell packet ______/
              J = max X_j     X = Σ X_j
              σ = P_{j*}/X    CONC σ≥1/2 | SPREAD σ≤1/2
""",
    "vorticity": """
  strain  λ1 + λ2 + λ3 = 0
  stretching  ω·Sω = |ω|² Σ λ_i cos² α_i
  ξ = ω/|ω|
  E_c = { |ω| ≥ c ||ω||_rms }     Ring: |∇ξ|_∞ ≤ C 2^{j*} on E_c
  alignment cos α_3 → 0   NOT implied   CLIP-B3b-ALIGN
""",
    "swirl": """
  Γ = r u_θ     keep Γ
  1/r^4 ∂_z(Γ²) = ∂_z(Φ_θ²)   identity, not a cancel
  (Δu)_θ = Δu_θ − u_θ/r²      extra viscosity IN THE SAME TUBE
  Φ_θ = Γ/r² as unknown       refused   CLIP-PHI-LINFTY
""",
}


OBJECTS: Final[tuple[dict[str, str], ...]] = (
    {
        "id": "T3",
        "geometry": "physical",
        "what": "periodic box T^3, div-free, Leray projector P",
        "status": "given",
    },
    {
        "id": "AXIS-TUBE",
        "geometry": "physical",
        "what": "r < δ(t) around the axis; δ ∼ 2^{-j*} in concentration",
        "status": "architecture",
    },
    {
        "id": "WALL",
        "geometry": "physical",
        "what": "r = δ interface; Hardy wall remainder 2 h(δ)²",
        "status": "pass as identity (B4); not absorbed",
    },
    {
        "id": "OFF-AXIS",
        "geometry": "physical",
        "what": "r ≥ δ; 1/r^4 is bounded; I_off is Sobolev",
        "status": "standard; not the live difficulty",
    },
    {
        "id": "SHELLS",
        "geometry": "frequency",
        "what": "X_j = 2^{2j} ||Δ_j u||_2^2,  X = ||ω||_2^2,  J = max X_j",
        "status": "given Littlewood–Paley",
    },
    {
        "id": "PACKET",
        "geometry": "frequency",
        "what": "3-shell around j*: P_{j*} = X_{j*-1}+X_{j*}+X_{j*+1}",
        "status": "pass as Bernstein (B3), not depletion",
    },
    {
        "id": "COVER",
        "geometry": "frequency",
        "what": "CONC σ≥1/2 vs SPREAD σ≤1/2; August vs June SND renamed",
        "status": "pass as a cover (B2), not dynamics",
    },
    {
        "id": "STRAIN",
        "geometry": "vorticity",
        "what": "eigenframe of S; Σ λ_i = 0; stretching Σ λ_i cos² α_i",
        "status": "identity; depletion open",
    },
    {
        "id": "SUPERLEVEL",
        "geometry": "vorticity",
        "what": "E_c superlevel of |ω|; Ring bound on |∇ξ|",
        "status": "pass on a 3-shell field (B3)",
    },
    {
        "id": "GAMMA",
        "geometry": "swirl",
        "what": "Γ = r u_θ; source 2Γ ∂_z Γ / r^4 kept",
        "status": "kept; Φ_θ cancel refused",
    },
    {
        "id": "ANGULAR-VISC",
        "geometry": "swirl",
        "what": "extra −u_θ/r² in (Δu)_θ, same tube as the source",
        "status": "identity pass (B5); domination open (B5b)",
    },
)


@dataclass(frozen=True)
class GeoStep:
    step: str
    uses: tuple[str, ...]
    geometric_picture: str
    proved: str
    remainder: str
    remainder_id: str

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["uses"] = list(self.uses)
        return d


GEO_STEPS: Final[tuple[GeoStep, ...]] = (
    GeoStep(
        step="B0",
        uses=("T3", "STRAIN", "SHELLS"),
        geometric_picture="A divergence-free field on a torus. Stretching is geometry of the strain frame. No tube yet.",
        proved="the PDE and the stretching identity",
        remainder="X has no geometric bound",
        remainder_id="CLIP-B-REG",
    ),
    GeoStep(
        step="B1",
        uses=("T3", "SHELLS"),
        geometric_picture="Low-frequency velocity is a large-scale, incompressible flow. It cannot pump its own high-frequency block.",
        proved="low self-flux vanishes (geometry of div-free + parts)",
        remainder="high-high and high-low fluxes still live",
        remainder_id="CLIP-B1-HIGHFLUX",
    ),
    GeoStep(
        step="B2",
        uses=("SHELLS", "COVER", "PACKET"),
        geometric_picture="Enstrophy is a pile of shells. Either one packet holds half the mass, or it does not.",
        proved="the two regimes cover all mass fractions",
        remainder="which regime the solution occupies, and for how long",
        remainder_id="CLIP-B2-OCCUPATION",
    ),
    GeoStep(
        step="B3",
        uses=("PACKET", "SUPERLEVEL", "STRAIN"),
        geometric_picture="A triad packet is almost a single scale. On the superlevel, direction cannot oscillate faster than 2^{j*}.",
        proved="Bernstein / Ring on a 3-shell field",
        remainder="alignment in the strain frame (cos α_3)",
        remainder_id="CLIP-B3b-ALIGN",
    ),
    GeoStep(
        step="B4",
        uses=("AXIS-TUBE", "WALL", "GAMMA"),
        geometric_picture="A radial Hardy inequality on a finite tube. Axis vanishing + a wall at δ.",
        proved="∫ h²/r ≤ 4∫ (h')² r + 2 h(δ)²",
        remainder="the wall term, and whether this eats I_tube",
        remainder_id="CLIP-B4-WALL",
    ),
    GeoStep(
        step="B4b",
        uses=("AXIS-TUBE", "WALL", "GAMMA", "OFF-AXIS"),
        geometric_picture="Split the swirl source: I_off(δ) + I_tube(δ). Off-axis is cheap. Tube is the geometric contest.",
        proved="nothing yet (open)",
        remainder="I_tube vs viscosity at δ ∼ 2^{-j*}",
        remainder_id="CLIP-B4b-ITUBE",
    ),
    GeoStep(
        step="B5",
        uses=("ANGULAR-VISC", "AXIS-TUBE", "GAMMA"),
        geometric_picture="Stokes in cylindrical components puts extra 1/r² damping where the 1/r^4 source lives.",
        proved="the identity (Δu)_θ = Δu_θ − u_θ/r²",
        remainder="whether that extra damping wins",
        remainder_id="CLIP-B5b-VS-VISC",
    ),
    GeoStep(
        step="B6",
        uses=("T3",),
        geometric_picture="A spike in time can have finite area and infinite height. Integrable enstrophy is not a geometric bound.",
        proved="the attempted close is false (counterexample spike)",
        remainder="X ∼ (T*−t)^{-1/2}",
        remainder_id="CLIP-B6-SPIKE",
    ),
)


def ns_geometry() -> dict[str, Any]:
    return {
        "book": "B",
        "title": "Geometric analysis of Track B",
        "not_a_regularity_proof": True,
        "claim": (
            "This is a geometric analysis of the architecture: which "
            "manifolds, packets, tubes, and frames each lemma uses. "
            "It is not a geometric proof of global regularity."
        ),
        "split": "I = I_off(δ) + I_tube(δ),  δ ∼ 2^{-j*} under concentration",
        "diagrams": dict(DIAGRAMS),
        "objects": [dict(o) for o in OBJECTS],
        "steps": [s.to_dict() for s in GEO_STEPS],
        "closed_geometrically": [
            "div-free low flux (B1)",
            "regime cover (B2)",
            "3-shell Bernstein / Ring on E_c (B3)",
            "tube Hardy with wall (B4)",
            "cylindrical extra viscosity identity (B5)",
            "energy-to-L^∞ close is false (B6)",
        ],
        "open_geometrically": [
            "occupation time of CONC vs SPREAD",
            "all-data alignment / depletion",
            "I_tube absorbed at δ ∼ 2^{-j*}",
            "angular viscosity dominates I_tube",
            "closed bound on X",
        ],
        "next_geometric_write": (
            "STOP at T3b. Missing piece GAP-T3 sits between T3a and T5. "
            "T5 is a candidate after, not a step. python -m domain_architect --gap B"
        ),
    }


def format_ns_geometry(report: dict[str, Any] | None = None) -> str:
    data = report or ns_geometry()
    lines = [
        data["title"],
        data["claim"],
        "",
        "Source split: " + data["split"],
        "",
        "Physical space" + data["diagrams"]["physical"],
        "Frequency space" + data["diagrams"]["frequency"],
        "Vorticity geometry" + data["diagrams"]["vorticity"],
        "Swirl tube" + data["diagrams"]["swirl"],
        "Objects",
    ]
    for obj in data["objects"]:
        lines.append(f"  {obj['id']} [{obj['geometry']}] {obj['what']}")
        lines.append(f"      {obj['status']}")
    lines.append("")
    lines.append("Each lemma as geometry")
    for step in data["steps"]:
        lines.append(f"── {step['step']}  uses {', '.join(step['uses'])}")
        lines.append(f"   picture: {step['geometric_picture']}")
        lines.append(f"   proved:  {step['proved']}")
        lines.append(f"   remainder {step['remainder_id']}: {step['remainder']}")
        lines.append("")
    lines.append("Closed geometrically")
    for item in data["closed_geometrically"]:
        lines.append(f"  - {item}")
    lines.append("Open geometrically")
    for item in data["open_geometrically"]:
        lines.append(f"  - {item}")
    lines.append("")
    lines.append("Next: " + data["next_geometric_write"])
    return "\n".join(lines)
