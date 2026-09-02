"""Small mechanism catalog used by translation and inverse design.

Entries are reusable mathematical mechanisms, not physical identities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .schema import FunctionalRole, MathType
from .signature import FunctionalSignature


@dataclass
class Mechanism:
    mechanism_id: str
    name: str
    domain: str
    signature: FunctionalSignature
    operator: str
    parameters: dict[str, str] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.mechanism_id,
            "name": self.name,
            "domain": self.domain,
            "signature": self.signature.to_dict(),
            "operator": self.operator,
            "parameters": dict(self.parameters),
            "notes": self.notes,
        }


def default_catalog() -> list[Mechanism]:
    return [
        Mechanism(
            "linear_damping",
            "linear damping",
            "mechanics",
            FunctionalSignature(
                FunctionalRole.DISSIPATION,
                MathType.OPERATOR,
                "velocity",
                "force_like",
                symmetry=frozenset({"linear", "time_invariant", "passive"}),
            ),
            "u = −γ ẋ",
            {"gamma": "damping coefficient"},
        ),
        Mechanism(
            "linear_restoring",
            "linear restoring",
            "mechanics",
            FunctionalSignature(
                FunctionalRole.INTERACTION,
                MathType.OPERATOR,
                "state",
                "force_like",
                symmetry=frozenset({"linear", "time_invariant"}),
            ),
            "u = −k x",
            {"k": "stiffness"},
        ),
        Mechanism(
            "inertia",
            "inertia",
            "mechanics",
            FunctionalSignature(
                FunctionalRole.STATE_TRANSITION,
                MathType.OPERATOR,
                "acceleration",
                "force_like",
                symmetry=frozenset({"linear"}),
            ),
            "u = m ẍ",
            {"m": "mass"},
        ),
        Mechanism(
            "resistance",
            "ohmic resistance",
            "electrical",
            FunctionalSignature(
                FunctionalRole.DISSIPATION,
                MathType.OPERATOR,
                "current",
                "voltage",
                symmetry=frozenset({"linear", "time_invariant", "passive"}),
            ),
            "v = R i",
            {"R": "resistance"},
        ),
        Mechanism(
            "pd_controller",
            "saturated PD controller",
            "control",
            FunctionalSignature(
                FunctionalRole.FEEDBACK,
                MathType.OPERATOR,
                "error × velocity",
                "input",
                constraints=frozenset({"box_constraint"}),
            ),
            "u = clip(Kp e − Kd ẋ, u_min, u_max)",
            {"Kp": "proportional gain", "Kd": "derivative gain"},
        ),
        Mechanism(
            "riblet_geometry",
            "riblet surface geometry",
            "fluid_surface",
            FunctionalSignature(
                FunctionalRole.CONSTRAINT,
                MathType.UNKNOWN,
                "near_wall_flow",
                "near_wall_flow",
                constraints=frozenset({"height_limit", "manufacturable"}),
            ),
            "boundary geometry θ_riblet",
            {"h": "height / h_max"},
            notes="Catalog entry for the drag-reduction workflow. Not a CFD result.",
        ),
        Mechanism(
            "navier_slip",
            "Navier slip length",
            "fluid_surface",
            FunctionalSignature(
                FunctionalRole.CONSTRAINT,
                MathType.UNKNOWN,
                "wall_tangent_velocity",
                "shear",
                constraints=frozenset({"boundary_condition"}),
            ),
            "u_slip = b ∂_n u",
            {"b": "slip length"},
        ),
        Mechanism(
            "compliant_wall",
            "compliant wall response",
            "fluid_structure",
            FunctionalSignature(
                FunctionalRole.FEEDBACK,
                MathType.UNKNOWN,
                "pressure",
                "wall_displacement",
                symmetry=frozenset({"causal"}),
            ),
            "wall impedance Z",
            {"c": "compliance"},
        ),
        Mechanism(
            "discrete_suction",
            "discrete wall suction",
            "fluid_surface",
            FunctionalSignature(
                FunctionalRole.FORCING,
                MathType.UNKNOWN,
                "wall_normal_mass_flux",
                "near_wall_flow",
                constraints=frozenset({"mass_flow_limit", "manufacturable"}),
            ),
            "v_wall = −v_suction",
            {"v_suction": "inward wall-normal speed"},
            notes="Existing HLFC / porous-panel hardware. Not a CFD result.",
        ),
    ]


def by_role(role: FunctionalRole) -> list[Mechanism]:
    return [m for m in default_catalog() if m.signature.role == role]


def drag_surrogate(h: float, slip: float, compliance: float) -> float:
    """Schematic D_R(θ) ∈ [0, 1). Not a fluid-mechanical prediction."""
    h = float(np_clip(h, 0.0, 1.0))
    slip = float(np_clip(slip, 0.0, 1.0))
    compliance = float(np_clip(compliance, 0.0, 1.0))
    return 0.12 * (1.0 - _exp(-4.0 * h)) * (0.5 + 0.5 * slip) * (0.7 + 0.3 * compliance)


def optimize_drag_surrogate(
    *,
    mass_max: float = 1.1,
    samples: int = 11,
) -> dict[str, float]:
    """Grid search of the schematic drag objective under mass ≤ mass_max."""
    best = {"D_R": -1.0, "h": 0.0, "slip": 0.0, "compliance": 0.0, "mass": 0.0}
    grid = [i / (samples - 1) for i in range(samples)]
    for h in grid:
        for slip in grid:
            for compliance in grid:
                mass = h + 0.3 * compliance
                if mass > mass_max:
                    continue
                score = drag_surrogate(h, slip, compliance)
                if score > best["D_R"]:
                    best = {
                        "D_R": score,
                        "h": h,
                        "slip": slip,
                        "compliance": compliance,
                        "mass": mass,
                    }
    return best


def np_clip(value: float, lo: float, hi: float) -> float:
    return lo if value < lo else hi if value > hi else value


def _exp(x: float) -> float:
    # local exp so catalog does not depend on numpy at import for this helper
    import math

    return math.exp(x)
