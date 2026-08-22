"""Auto-derived control-variable (tuning) export.

After Domain Architect assigns functional roles automatically, this module
lists which quantities are candidate *control parameters* for later
intervention experiments — the honest successor to informal “knob”
language used in older bridge/tuning apps.

Rules:
- Prefer roles that can vary independently without rewriting the PDE type.
- Mark structural constraints (e.g. Leray / div-free) as fixed unless the
  experiment explicitly changes the book.
- Never claim that exporting a control variable optimizes reality; it only
  names degrees of freedom for a frozen protocol.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .report import AuditReport


@dataclass
class ControlVariable:
    name: str
    role: str
    subtype: str
    status: str  # free | structural_fixed | derived | protocol_selector
    why: str
    default_intervention: str
    bridge_app_hint: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TuningExport:
    """Machine-readable handoff for tuning / bridge apps."""

    auto_assigned: bool
    domain_book: str
    controls: list[ControlVariable] = field(default_factory=list)
    fixed_structure: list[str] = field(default_factory=list)
    protocol_reminder: str = (
        "Freeze objective, training set, held-out tests, and controls "
        "before inspecting outcomes. Verify interventions on the original "
        "equations, not only inside the HB map."
    )
    statement: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "auto_assigned": self.auto_assigned,
            "domain_book": self.domain_book,
            "controls": [c.to_dict() for c in self.controls],
            "fixed_structure": self.fixed_structure,
            "protocol_reminder": self.protocol_reminder,
            "statement": self.statement,
        }

    def narrative(self) -> str:
        lines = [
            "Auto tuning export (control variables for intervention apps)",
            f"  domain_book: {self.domain_book}",
            f"  auto_assigned: {self.auto_assigned}",
            "",
            "Free / selector controls:",
        ]
        frees = [c for c in self.controls if c.status in {"free", "protocol_selector"}]
        if not frees:
            lines.append("  (none — map too unresolved for safe intervention list)")
        for c in frees:
            lines.append(
                f"  - {c.name} [{c.status}] role={c.role}/{c.subtype}: {c.why}"
            )
            lines.append(f"      intervene: {c.default_intervention}")
            if c.bridge_app_hint:
                lines.append(f"      bridge hint: {c.bridge_app_hint}")
        if self.fixed_structure:
            lines.append("")
            lines.append("Structural / fixed (do not casually retune):")
            for item in self.fixed_structure:
                lines.append(f"  - {item}")
        lines.append("")
        lines.append(self.statement)
        lines.append(self.protocol_reminder)
        return "\n".join(lines)


def _book(report: AuditReport) -> str:
    if report.hb_map and report.hb_map.get("domain_book"):
        return str(report.hb_map["domain_book"])
    joined = " ".join(report.notes + report.warnings).lower()
    if "ns-b" in joined:
        return "NS-B"
    if report.recovery_kind or report.poisson_compatibility is not None:
        return "gravity-poisson"
    return "generic"


def build_tuning_export(report: AuditReport) -> TuningExport:
    book = _book(report)
    roles = {
        str(a.get("candidate_role")): a for a in report.role_assignments
    }
    resolved = [
        a
        for a in report.role_assignments
        if not str(a.get("candidate_role", "")).startswith("unresolved")
    ]
    auto = bool(resolved) and book != "generic"
    controls: list[ControlVariable] = []
    fixed: list[str] = []

    if book == "gravity-poisson":
        controls.append(
            ControlVariable(
                name="P",
                role="admissibility",
                subtype="mode_permission",
                status="protocol_selector",
                why=(
                    "Mode permission / projector. Baseline P=I must recover "
                    "Newtonian Poisson; alternate masks are experiments."
                ),
                default_intervention=(
                    "Hold energy budget fixed; compare P=I vs prime/odd/"
                    "composite/random/optimized selectors on held-out sources."
                ),
                bridge_app_hint=(
                    "Maps to selector / mask controls in spectral gravity lab "
                    "and older bridge tuning UIs."
                ),
            )
        )
        if "coupling" in roles or any(
            a.get("symbol") in {"G", "H"} for a in report.role_assignments
        ):
            controls.append(
                ControlVariable(
                    name="H_g (=4πG)",
                    role="coupling",
                    subtype="coupling_constant",
                    status="free",
                    why="Gravitational coupling scale in the Poisson map.",
                    default_intervention="Scale H_g only under declared units; check Φ residual.",
                    bridge_app_hint="Scalar coupling dial in bridge-style tuners.",
                )
            )
        controls.append(
            ControlVariable(
                name="rho / S",
                role="source",
                subtype="density_or_amplitude",
                status="free",
                why="Source family is the primary experiment input.",
                default_intervention="Swap training vs held-out source distributions.",
                bridge_app_hint="Input field / drive amplitude in tuning apps.",
            )
        )
        fixed.append("Laplacian / inverse-Laplacian structure (R=1/κ², κ≠0)")
        fixed.append("Zero-mode compatibility policy (reject or subtract)")

    elif book == "NS-B":
        controls.append(
            ControlVariable(
                name="nu",
                role="scale_response",
                subtype="viscosity",
                status="free",
                why="Dissipative scale; classical viscosity parameter.",
                default_intervention=(
                    "Vary ν under fixed IC/BC; measure energy, enstrophy, "
                    "dissipation; verify on original NS, not only the map."
                ),
                bridge_app_hint="Primary continuous dial analogous to bridge gain.",
            )
        )
        controls.append(
            ControlVariable(
                name="u0 / omega0",
                role="state",
                subtype="initial_data",
                status="free",
                why="Initial state is an independent control for Cauchy runs.",
                default_intervention="Family of divergence-free ICs with matched energy.",
                bridge_app_hint="Initial-condition presets in experiment UIs.",
            )
        )
        controls.append(
            ControlVariable(
                name="F (optional body force)",
                role="forcing",
                subtype="external_forcing",
                status="free",
                why="External forcing lives in E when present.",
                default_intervention="On/off and amplitude sweeps with frozen protocol.",
                bridge_app_hint="Drive / forcing channel in tuning apps.",
            )
        )
        fixed.append("P ≈ Leray / div-free admissibility (structural for classical NS-B)")
        fixed.append("Nonlinear advection / stretching operator form")
        fixed.append("Do not bake λ_min(Q_N)>-1/2 or prime floors into unaugmented NS")

    else:
        for a in resolved:
            controls.append(
                ControlVariable(
                    name=str(a.get("symbol")),
                    role=str(a.get("candidate_role")),
                    subtype=str(a.get("subtype") or "unknown"),
                    status="free",
                    why="Resolved role without a frozen domain book; treat cautiously.",
                    default_intervention="Declare a book before intervention experiments.",
                )
            )
        if not resolved:
            fixed.append(
                "No auto book route; roles unresolved — computer refused name-only assignment"
            )

    statement = (
        "Computer auto-assigned functional roles for this input where a domain "
        "book matched. Tuning export lists candidate control variables for "
        "downstream bridge/tuning apps; it does not run the optimizer."
        if auto
        else (
            "Auto domain route incomplete. Domain Architect will not invent "
            "physical identities from letter names alone."
        )
    )
    return TuningExport(
        auto_assigned=auto,
        domain_book=book,
        controls=controls,
        fixed_structure=fixed,
        statement=statement,
    )
