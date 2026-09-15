"""The kept Navier–Stokes model as a Domain Architect instance.

The good model in this repo is classical unaugmented NS on the
axisymmetric-with-swirl class, plus the KEEP swirl algebra (NS-Φ) and the
open barrier ‖u^r/r‖_∞. It is not Track A augmentation, not SFE, not Clay.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .audit import audit_expression
from .protocol import freeze_protocol
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, NS_CLAY_STATUS, RH_STATUS


NS_MODEL_SCOPE: str = (
    "Kept NS model. Axisymmetric-with-swirl classical Navier–Stokes plus the "
    "KEEP swirl identity. Domain Architect expands E from the subject. "
    "Swirl Φ is not FRA Φ and not Riemann’s kernel Φ. Clay NS is not claimed."
)


@dataclass
class NSComponent:
    component_id: str
    role: str
    occupant: str
    kind: str
    independently_specified: bool
    da_action: str
    verdict: str
    source: str = ""


def ns_components() -> list[NSComponent]:
    return [
        NSComponent(
            "NS-P",
            "P",
            "axisymmetric-with-swirl class: ∂_θ = 0, u_θ ≠ 0, ∇·u = 0, smooth on the axis r=0",
            "admissibility",
            True,
            "recorded as the function class, not a prime selector and not Leray ℙ as permission",
            "the class is specified; global regularity inside the class is not",
            "NS-H001 / KEEP card",
        ),
        NSComponent(
            "NS-H",
            "H",
            "nonlinear coupling: convection (u·∇)ω and stretching (ω·∇)u; linear part νΔ / Stokes A=−ℙΔ",
            "pde-coupling",
            True,
            "seated as fluids interaction, not as a Hilbert–Pólya Hamiltonian",
            "specified as a PDE; stretching is the 3D obstruction; this H is not spec(H)={γ_n}",
            "NS-H001 / NS-H003",
        ),
        NSComponent(
            "NS-psi",
            "ψ",
            "state: velocity u, or vorticity ω=∇×u, or intensive swirl Φ_swirl=u_θ/r",
            "field",
            True,
            "three presentations of one state; Φ_swirl is the near-axis variable",
            "specified. Intensive swirl stays finite on a smooth axis; Γ=r u_θ is the wrong near-axis variable",
            "KEEP card §1",
        ),
        NSComponent(
            "NS-lambda",
            "λ",
            "viscosity ν; axis scale r; Sobolev / Ḣ^{1.3} packaging after the Ḣ relabel",
            "scale",
            True,
            "ν is the dissipative scale; r is geometric scale; Ḣ^{1.3} is the corrected energy label (not Ḣ^{2.6})",
            "specified as parameters. Relabel was bookkeeping, not a repair of the barrier",
            "PHI-RENORM-AUDIT-2026-08-22",
        ),
        NSComponent(
            "NS-Phi-FRA",
            "Φ",
            "target realized output: globally regular u(t) on the class (Clay Statement B, restricted to swirl)",
            "target",
            False,
            "recorded as the prize output, not filled by the KEEP identity",
            "open. The algebra does not occupy this seat. Do not write Φ_FRA := Φ_swirl",
            "Clay / KEEP card honest scope",
        ),
        NSComponent(
            "NS-geom",
            "g",
            "cylindrical (r,θ,z); axis r=0 is a coordinate singularity, not necessarily a physical one",
            "geometry",
            True,
            "promoted out of five letters; quantum-style expansion for a PDE with an axis",
            "specified. 1/r^4 in Γ-variables is often the wrong variable, not a catastrophe",
            "KEEP card §1–2",
        ),
        NSComponent(
            "NS-Baxis",
            "ℬ",
            "axis regularity: u_θ → 0 as r→0; Φ_swirl|_{r=0}=∂_r u_θ",
            "boundary",
            True,
            "recorded as axis data, not hidden inside P",
            "class requirement. The open estimate is ‖u^r/r‖_∞, not this vanishing",
            "KEEP card §1",
        ),
        NSComponent(
            "NS-D",
            "D",
            "evolution: vorticity transport / NS in time",
            "evolution",
            True,
            "DHFA-like seat occupied by the PDE itself; dynamics are the model, not a route to invent H",
            "specified as the NS Cauchy problem",
            "NS-H001",
        ),
        NSComponent(
            "NS-Xi",
            "Ξ",
            "viscous dissipation νΔω (damping of enstrophy)",
            "damping",
            True,
            "recorded as NS viscosity, not de Bruijn–Newman heat on Ξ",
            "specified. You cannot identify this with Ξ_t on Riemann’s cosine transform",
            "LOOK-NS-HEAT",
        ),
        NSComponent(
            "NS-N",
            "N",
            "stretching (ω·∇)u — the genuinely 3D nonlinear term",
            "nonlinearity",
            True,
            "promoted as its own component; 2D has no stretching",
            "this is the obstruction. Dropping it leaves 2D NS (already regular)",
            "NS-B.2 child",
        ),
        NSComponent(
            "NS-keep",
            "E-algebra",
            "KEEP identity r^{-4}∂_z(Γ²)=∂_z(Φ_swirl²) with Γ=r u_θ, Φ_swirl=u_θ/r",
            "theorem",
            True,
            "accepted as algebra; lem:Phieq left as written",
            "KEEP. Algebraic identity. Not Clay. Not cosmology",
            "NS-H002",
        ),
        NSComponent(
            "NS-barrier",
            "E-open",
            "uniform-in-ε control of ‖u^r/r‖_∞ (op:gronwall / eq:B1)",
            "open-barrier",
            False,
            "recorded as the remaining condition; equivalent in difficulty to swirl GR",
            "OPEN. Conditional reduction only. This is the load-bearing gap of the good model",
            "PHI-RENORM-AUDIT-2026-08-22",
        ),
        NSComponent(
            "NS-lions",
            "E-estimate",
            "Lions bookkeeping β=0.6 ⇒ dissipation order 1.3 > 5/4; Ḣ^{1.3} after relabel",
            "theorem-bookkeeping",
            True,
            "accepted as correct bookkeeping; Ḣ^{2.6} was a mislabel of the energy norm",
            "KEEP as calculation. Does not close the barrier",
            "audit KEEP findings 2–3",
        ),
        NSComponent(
            "NS-BS",
            "E-kernel",
            "Biot–Savart u=∇×(−Δ)^{-1}ω; Green ΔG=−δ; shared R(κ)=1/κ²",
            "theorem",
            True,
            "recovered velocity from vorticity; pair-run with HP-H027",
            "specified reconstruction. Shared inverse-Laplacian tool. Not smoothness",
            "NS-H004",
        ),
        NSComponent(
            "NS-div",
            "E-constraint",
            "∇·u=0 (and curl reconstruction implies it)",
            "constraint",
            True,
            "incompressibility is admissibility and a constraint, not FRA P-as-primes",
            "specified",
            "NS-H001",
        ),
        NSComponent(
            "NS-park",
            "forbidden",
            "PARK: SFE→NS, CMB Axis of Evil as proof, Triple Lock, Lemma★ collapse, Track A as this PDE, Riemann Φ as swirl Φ",
            "parked",
            True,
            "classified and refused as glue",
            "DA does not ingest PARK items as the good model",
            "KEEP card §3 / C-GLUE-1 / C-GLUE-4",
        ),
    ]


def ns_da_requests() -> list[str]:
    return [
        "Uniform-in-ε control of ‖u^r/r‖_∞ — the open barrier of the kept model.",
        "A bound on stretching (ω·∇)u on this class, or a reduction of Clay Statement B "
        "that does not assume the barrier.",
        "If Track A (augmented NS) is used: say so; it is a different PDE from this instance.",
        "If a map to RH is claimed: an explicit transformation, not the letter Φ and not the word spectrum.",
        "A name other than Φ for swirl u_θ/r when this instance sits next to FRA output or Riemann’s kernel.",
    ]


def ns_path_guides() -> list[str]:
    return [
        "You cannot fill FRA Φ with swirl Φ_swirl. The KEEP identity is algebra in E, not the prize output.",
        "You cannot call this Clay NS closed. The barrier ‖u^r/r‖_∞ is equivalent to swirl global regularity.",
        "You cannot derive this PDE from SFE/UHF/DHFA. Route between books; do not glue.",
        "You cannot identify viscous νΔω with de Bruijn–Newman heat on Ξ.",
        "You cannot treat Track A’s extra projector term as this model.",
        "You cannot use CMB / Saturn / cosmic lattice as a proof of the identity.",
        "You can keep the algebra and the Phi equation (lem:Phieq). That is what KEEP means.",
        "You can work the barrier as the live NS-side piece. That is the path.",
        "You can use Biot–Savart / R(κ)=1/κ² as a reconstruction tool without claiming regularity.",
    ]


def ns_parse_runs() -> list[dict[str, str]]:
    expressions = [
        ("KEEP identity", "partial_z(Gamma^2)/r^4 = partial_z(Phi^2)"),
        ("incompressibility", "div(u) = 0"),
        ("Biot–Savart", "u = curl(invLap * omega)"),
        ("vorticity NS", "partial_t(omega) + (u * nabla)*omega = (omega * nabla)*u + nu * laplacian(omega)"),
    ]
    rows = []
    for label, expr in expressions:
        report = audit_expression(expr)
        rows.append(
            {
                "label": label,
                "expression": expr,
                "evidence": str(int(report.highest_evidence_level)),
                "roles": ", ".join(
                    f"{a.get('symbol')}={a.get('candidate_role')}"
                    for a in report.role_assignments
                )
                or "none",
                "warnings": str(len(report.warnings)),
            }
        )
    return rows


@dataclass
class NSModelReport:
    instance_name: str
    component_count: int
    core_role_count: int
    extension_count: int
    components: list[NSComponent]
    filled: list[str]
    open_gaps: list[str]
    path_guides: list[str]
    da_requests: list[str]
    parse_runs: list[dict[str, str]]
    registry_ids: list[str]
    ns_clay_status: str
    rh_status: str
    canonical_sfe_status: str
    protocol_hash: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["components"] = [asdict(c) for c in self.components]
        return payload

    def narrative(self) -> str:
        lines = [
            "Domain Architect — kept NS model",
            "",
            NS_MODEL_SCOPE,
            "",
            f"Instance: {self.instance_name}",
            f"DA decided the component count for this subject: {self.component_count}",
            f"Interface letters: {self.core_role_count} (P, H, ψ, λ, Φ). "
            f"Extras: {self.extension_count}.",
            f"Clay NS status: {self.ns_clay_status}.",
            f"Riemann hypothesis status: {self.rh_status}.",
            f"Canonical SFE status: {self.canonical_sfe_status}.",
            "",
            "What happens when this model is entered:",
            "  DA accepts it as a fluids book. It does not turn it into SFE or RH.",
            "  Swirl Φ is renamed Φ_swirl in the role map so it cannot occupy FRA Φ.",
            "  The KEEP identity is seated in E as algebra. The prize output stays empty.",
            "  The load-bearing gap is ‖u^r/r‖_∞, not a missing Hamiltonian.",
            "",
            "What is already filled (KEEP):",
        ]
        for item in self.filled:
            lines.append(f"  * {item}")
        lines.append("")
        lines.append("What stays open:")
        for item in self.open_gaps:
            lines.append(f"  * {item}")
        lines.append("")
        lines.append("Path guidance:")
        for item in self.path_guides:
            lines.append(f"  - {item}")
        lines.append("")
        lines.append("Components:")
        for item in self.components:
            spec = "specified" if item.independently_specified else "not independently specified"
            lines.append(
                f"  [{item.component_id}] role={item.role} kind={item.kind} ({spec})"
            )
            lines.append(f"    occupant: {item.occupant}")
            lines.append(f"    DA action: {item.da_action}")
            lines.append(f"    verdict: {item.verdict}")
        lines.append("")
        lines.append("Parseable pieces run through the auditor:")
        for row in self.parse_runs:
            lines.append(
                f"  {row['label']}: {row['expression']!r} "
                f"evidence={row['evidence']} roles={row['roles']} "
                f"warnings={row['warnings']}"
            )
        lines.append("")
        lines.append("Domain Architect still needs:")
        for req in self.da_requests:
            lines.append(f"  - {req}")
        lines.append("")
        lines.append(f"Registry ids: {', '.join(self.registry_ids)}")
        lines.append(f"Protocol hash: {self.protocol_hash}")
        for note in self.notes:
            lines.append(note)
        return "\n".join(lines)


def run_ns_model() -> NSModelReport:
    components = ns_components()
    core = {"P", "H", "ψ", "λ", "Φ"}
    core_count = sum(1 for c in components if c.role in core)
    registry = EquationRegistry.load_default()
    ns_ids = sorted(eq_id for eq_id in registry.equations if eq_id.startswith("NS-"))
    protocol = freeze_protocol(
        {
            "program": "ns-kept-model",
            "components": [c.component_id for c in components],
            "keep_algebra": True,
            "forbid_sfe_glue": True,
            "forbid_phi_letter_merge": True,
            "clay_not_claimed": True,
        }
    )
    filled = [
        "KEEP swirl identity (NS-H002) — algebra",
        "Phi equation lem:Phieq — no spurious −Φ/r²",
        "Lions β=0.6 dissipation order 1.3>5/4; Ḣ^{1.3} relabel",
        "Biot–Savart reconstruction and ∇·u=0",
        "Axisymmetric-with-swirl class and cylindrical geometry",
        "PARK list refused (not ingested as this instance)",
    ]
    open_gaps = [
        "‖u^r/r‖_∞ uniform in ε (load-bearing barrier)",
        "3D stretching control on this class",
        "FRA realized output (global regularity) — not filled",
        "Unaugmented classical swirl GR / Clay Statement B",
    ]
    return NSModelReport(
        instance_name="kept-ns-swirl",
        component_count=len(components),
        core_role_count=core_count,
        extension_count=len(components) - core_count,
        components=components,
        filled=filled,
        open_gaps=open_gaps,
        path_guides=ns_path_guides(),
        da_requests=ns_da_requests(),
        parse_runs=ns_parse_runs(),
        registry_ids=ns_ids,
        ns_clay_status=NS_CLAY_STATUS,
        rh_status=RH_STATUS,
        canonical_sfe_status=CANONICAL_SFE_STATUS,
        protocol_hash=protocol.protocol_hash,
        notes=[
            "Live command: python -m domain_architect --ns-model",
            "Source: docs/ns-review/PHI-RENORM-WHAT-IS-KEPT.md",
        ],
    )


def render_ns_model(report: NSModelReport | None = None) -> str:
    if report is None:
        report = run_ns_model()
    return report.narrative()
