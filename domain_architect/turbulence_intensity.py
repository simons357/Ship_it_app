"""Lumped turbulence-intensity cycle: desired state against a no-actuation control.

This is a Domain Architect *use* of inverse design. The state x is a scalar
intensity analog. Desired: x → x★ with x★ below the uncontrolled equilibrium.
Control arm: u = 0, same plant, same initial condition.

Not 3D Navier–Stokes. Not a coating. Not a regularity proof.
Slogans such as "decrease turbulence" still refuse A13 unless written as
a recognized setpoint ``x → x★``.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .cycle import CycleReport
from .decompose import decompose
from .dynamics import ControllerSpec, produced_intensity_field, simulate
from .schema import CorrespondenceKind, ValidationGate
from .synthesize import inverse_design_architecture, is_recognized_setpoint


REFUSED = (
    "no 3D Navier–Stokes regularity claim",
    "no coating / surface as this plant",
    "no Clay / unaugmented smoothness",
    "no identifying x with enstrophy of a field",
)

# Industry-standard operating intensity on this analog is the no-actuation
# equilibrium. The desired endpoint is 15% below that.
INDUSTRY_STANDARD_X = 1.0
BELOW_INDUSTRY_FRACTION = 0.15


def turbulence_intensity_lab(
    *,
    x_eq: float = INDUSTRY_STANDARD_X,
    reduction: float = BELOW_INDUSTRY_FRACTION,
    omega: float = 1.5,
    zeta: float = 0.8,
    u_max: float = 6.0,
    t_final: float = 8.0,
) -> dict[str, Any]:
    """Compare no-actuation industry baseline vs PD to 15% below it."""
    if not 0.0 < reduction < 1.0:
        raise ValueError("reduction must be in (0, 1)")
    x_star = round((1.0 - reduction) * x_eq, 4)
    target = f"x → {x_star}"
    if not is_recognized_setpoint(target):
        raise RuntimeError(f"lab setpoint {target!r} is not recognized")

    plant = f"xdd + a*xd + k*x = k*{x_eq} + u"
    field = produced_intensity_field(omega, zeta, x_eq)
    x0 = np.array([x_eq, 0.0])

    control = simulate(
        field,
        x0=x0,
        controller=ControllerSpec(
            target=x_eq,
            kp=0.0,
            kd=0.0,
            u_min=-u_max,
            u_max=u_max,
            feedforward=0.0,
        ),
        t_final=t_final,
    )
    treated = simulate(
        field,
        x0=x0,
        controller=ControllerSpec(
            target=x_star,
            kp=8.0,
            kd=3.0,
            u_min=-u_max,
            u_max=u_max,
            feedforward=(omega**2) * (x_star - x_eq),
        ),
        t_final=t_final,
    )

    x_c = float(control.trajectory.x[-1])
    x_t = float(treated.trajectory.x[-1])
    relative = 1.0 - (x_t / x_c) if abs(x_c) > 1e-12 else 0.0
    reduced = bool(
        treated.settled
        and x_t < 0.9 * x_c
        and treated.trajectory.max_control() <= u_max + 1e-9
    )
    return {
        "protocol": "turbulence-intensity",
        "definition": (
            "x is a lumped intensity analog. Industry-standard intensity on "
            f"this plant is the no-actuation equilibrium x_eq = {x_eq}. "
            f"Desired endpoint is {reduction:.0%} below that: x★ = {x_star}."
        ),
        "plant": plant,
        "industry_standard": {
            "meaning": "no-actuation equilibrium on this analog",
            "x": x_eq,
        },
        "desired": {
            "symbol": "x★",
            "value": x_star,
            "as_setpoint": target,
            "below_industry_fraction": reduction,
        },
        "control_arm": {
            "actuation": "u = 0",
            "terminal_x": x_c,
            "max_control": control.trajectory.max_control(),
            "settled": control.settled,
            "constraint_violations": control.constraint_violations,
        },
        "treated_arm": {
            "actuation": "saturated PD + feedforward to x★",
            "terminal_x": x_t,
            "max_control": treated.trajectory.max_control(),
            "settled": treated.settled,
            "constraint_violations": treated.constraint_violations,
        },
        "relative_reduction": relative,
        "reduced_vs_control": reduced,
        "constraints": [f"|u| ≤ {u_max}"],
        "refused": list(REFUSED),
        "kind": CorrespondenceKind.ANALOGY.value,
        "validation_gate": (
            ValidationGate.COMPUTATIONAL.value
            if reduced
            else ValidationGate.MATHEMATICAL.value
        ),
    }


def cycle_turbulence_intensity(**kwargs: Any) -> CycleReport:
    payload = turbulence_intensity_lab(**kwargs)
    candidate = inverse_design_architecture(
        payload["desired"]["as_setpoint"],
        payload["constraints"],
    )
    plant = decompose(payload["plant"], name="lumped_intensity")
    gate = (
        ValidationGate.COMPUTATIONAL
        if payload["reduced_vs_control"]
        else ValidationGate.MATHEMATICAL
    )
    return CycleReport(
        mode="turbulence-intensity",
        target=payload["desired"]["as_setpoint"],
        constraints=list(payload["constraints"]),
        decomposition=plant,
        translation=None,
        candidate=candidate,
        prediction=payload,
        residual=None,
        validation_gate=gate,
        notes=[
            payload["definition"],
            (
                f"Control terminal x = {payload['control_arm']['terminal_x']:.4f}; "
                f"treated terminal x = {payload['treated_arm']['terminal_x']:.4f}; "
                f"relative reduction = {payload['relative_reduction']:.3f}."
            ),
            "Computational gate is on this lumped analog only.",
            "Not a coating. Not 3D Navier–Stokes. Clay is NOT CLAIMED.",
            (
                f"Endpoint is {payload['desired']['below_industry_fraction']:.0%} "
                "below the industry-standard no-actuation intensity."
            ),
            "A13 still refuses the slogan 'decrease turbulence' without x → x★.",
            f"Synthesize of the setpoint is {candidate.name}.",
        ],
        method_credits=["RK4", "saturated PD", "no-actuation control arm"],
    )
