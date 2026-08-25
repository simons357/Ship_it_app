"""The Domain Architect cycle.

TARGET + CONSTRAINTS
        ↓
    DECOMPOSE
        ↓
FUNCTIONAL ARCHITECTURE
        ↓
CROSS-DOMAIN TRANSLATION
        ↓
COMPATIBLE MECHANISMS
        ↓
    SYNTHESIZE
        ↓
CANDIDATE ARCHITECTURE
        ↓
     PREDICT → TEST → RESIDUAL ↺
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .catalog import default_catalog, optimize_drag_surrogate
from .decompose import Decomposition, decompose
from .dynamics import (
    ControllerSpec,
    SimulationReport,
    free_oscillator_trajectory,
    second_order_field,
    simulate,
)
from .cycle import CycleReport
from .residual import recover_missing_damping
from .schema import ValidationGate
from .synthesize import CandidateArchitecture, Provenance, inverse_design_architecture, synthesize
from .translate import TranslationRecord, mechanical_electrical_translation


def cycle_missing_damping(
    *,
    omega: float = 2.0,
    zeta: float = 0.15,
    t_final: float = 8.0,
    dt: float = 0.002,
) -> CycleReport:
    """Paper §16 benchmark: delete dissipation and ask DA to recover it."""
    incomplete = decompose("xdd + k*x = 0", name="incomplete_oscillator")
    observed = free_oscillator_trajectory(
        omega=omega, zeta=zeta, t_final=t_final, dt=dt
    )
    acc = np.gradient(observed.v, dt)
    analysis = recover_missing_damping(
        observed.x, observed.v, omega=omega, acc=acc
    )
    recovered = analysis.recovered_parameter.get("zeta")
    ok = recovered is not None and abs(recovered - zeta) < 0.03
    notes = [
        "True model: ẍ + 2ζω ẋ + ω² x = 0.",
        "Incomplete model: ẍ + ω² x = 0 (dissipation removed).",
        analysis.rationale,
    ]
    if ok:
        notes.append(
            f"Recovered ζ̂ = {recovered:.4f} against true ζ = {zeta:.4f} "
            "(computational gate passed)."
        )
        gate = ValidationGate.COMPUTATIONAL
    else:
        notes.append(
            f"Recovery missed the true damping: ζ̂ = {recovered} vs ζ = {zeta}."
        )
        gate = ValidationGate.MATHEMATICAL
    candidate = CandidateArchitecture(
        name="completed_oscillator",
        components=["state x", "inertia", "restoring", "linear_damping"],
        replaced={"missing": "linear_damping"},
        hypothesis="Insert γ ẋ with γ̂ from the role-restricted least-squares fit.",
        provenance=[
            Provenance(
                source="equation-error OLS on {1, x, ẋ}",
                original_domain="second_order_ode",
                functional_role="dissipation",
                translation=None,
                assumptions=["linear constant-coefficient plant", "role-restricted library"],
                compatibility_checks=["role_restricted_least_squares"],
                modifications=["insert linear_damping"],
                evidence=[analysis.rationale],
                validation_status=gate.value,
            )
        ],
        validation_gate=gate,
        notes=[
            "The fit is ordinary least squares on a three-term library. "
            "That method is equation-error identification, not Domain Architect itself."
        ],
    )
    return CycleReport(
        mode="analysis",
        target="recover missing dissipation",
        constraints=["linear second-order plant", "constant coefficients"],
        decomposition=incomplete,
        translation=None,
        candidate=candidate,
        prediction={"true_zeta": zeta, "recovered": analysis.recovered_parameter},
        residual=analysis,
        validation_gate=gate,
        notes=notes,
    )


def cycle_inverse_control(
    *,
    omega: float = 1.5,
    zeta: float = 0.1,
    target: float = 1.0,
    u_max: float = 6.0,
) -> tuple[CycleReport, SimulationReport]:
    plant = decompose("xdd + a*xd + k*x = u", name="controlled_oscillator")
    candidate = inverse_design_architecture(
        f"x → {target}",
        constraints=[f"|u| ≤ {u_max}"],
    )
    sim = simulate(
        second_order_field(omega, zeta),
        x0=np.array([0.0, 0.0]),
        controller=ControllerSpec(
            target=target,
            kp=8.0,
            kd=3.0,
            u_min=-u_max,
            u_max=u_max,
            feedforward=omega**2 * target,
        ),
    )
    gate = ValidationGate.COMPUTATIONAL if sim.settled else ValidationGate.MATHEMATICAL
    report = CycleReport(
        mode="synthesis",
        target=f"x★ = {target}",
        constraints=[f"|u| ≤ {u_max}"],
        decomposition=plant,
        translation=None,
        candidate=candidate,
        prediction=sim.to_dict(),
        residual=None,
        validation_gate=gate,
        notes=list(sim.notes)
        + [
            "Required roles: state, measurement, feedback, forcing, "
            "state_transition, constraint."
        ],
    )
    return report, sim


def cycle_mechanical_electrical() -> CycleReport:
    translation = mechanical_electrical_translation()
    left = decompose("m*xdd + c*xd + k*x = f", name="mechanical_oscillator")
    candidate = synthesize(
        left,
        replacements={"c": "R"},
        compatibility=translation.compatibility,
        name="mech_with_electrical_damper",
    )
    return CycleReport(
        mode="translation",
        target="legal substitution of dissipation across domains",
        constraints=["explicit T required", "SI dimensions need not match"],
        decomposition=left,
        translation=translation,
        candidate=candidate,
        prediction={"mapping": dict(translation.mapping)},
        residual=None,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "Mechanical damper c and electrical resistance R perform the same "
            "functional role and share LTI structure. They are TRANSFORMABLE, "
            "not DIRECTLY COMPATIBLE."
        ],
    )


def cycle_drag_reduction() -> CycleReport:
    """Paper §14 workflow on a schematic surrogate. Not a CFD claim."""
    target = "max D_R(θ) inside the operating envelope"
    constraints = ["h ≤ h_max", "mass ≤ mass_max", "manufacturable"]
    dec = decompose("D_R = D_R(h, slip, compliance)", name="drag_reduction_objective")
    # Role declarations for an objective that is not a differential equation.
    catalog_ids = [m.mechanism_id for m in default_catalog() if m.domain in {"fluid_surface", "fluid_structure"}]
    optimum = optimize_drag_surrogate()
    candidate = CandidateArchitecture(
        name="surface_architecture_surrogate",
        components=catalog_ids,
        replaced={},
        hypothesis=(
            "Candidate surface architecture assembled from compatible catalog "
            "mechanisms (riblets, slip, compliant wall). The score is a "
            "schematic surrogate, not a Navier–Stokes result."
        ),
        provenance=[],
        validation_gate=ValidationGate.MATHEMATICAL,
    )
    return CycleReport(
        mode="synthesis",
        target=target,
        constraints=constraints,
        decomposition=dec,
        translation=None,
        candidate=candidate,
        prediction=optimum,
        residual=None,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=[
            "TARGET → DECOMPOSE → TRANSLATE → SYNTHESIZE → SIMULATE → OPTIMIZE.",
            "DA does not need to solve Navier–Stokes regularity to run this workflow.",
            f"Surrogate optimum D_R = {optimum['D_R']:.4f} at h={optimum['h']}, "
            f"slip={optimum['slip']}, compliance={optimum['compliance']}.",
            "The score is a schematic surrogate (constrained grid search), "
            "not a computational validation of Domain Architect.",
        ],
        method_credits=["constrained grid search on an invented surrogate"],
    )


def run_named_cycle(name: str, **kwargs: Any) -> CycleReport:
    name = name.replace("_", "-")
    chain = kwargs.get("chain")
    excise = kwargs.get("excise")
    if name in {"missing-damping", "damping", "benchmark"}:
        return cycle_missing_damping()
    if name in {"control", "inverse", "controller"}:
        return cycle_inverse_control()[0]
    if name in {"translate", "mechanical-electrical", "rlc"}:
        return cycle_mechanical_electrical()
    if name in {"drag", "drag-reduction"}:
        return cycle_drag_reduction()
    if name in {"leftover-repair", "leftover", "snd-vs-h"}:
        from .leftover_repair import cycle_leftover_repair

        return cycle_leftover_repair()
    if name in {"excise-2", "surgery-2", "step-2"}:
        # Hidden/test alias. User-facing command is localized-repair --excise K.
        from .localized_repair import cycle_localized_repair

        return cycle_localized_repair(chain=chain or "paper2", excise=2)
    if name in {"localized-repair", "surgery", "paper2-surgery"}:
        from .localized_repair import cycle_localized_repair

        return cycle_localized_repair(chain=chain, excise=excise)
    if name in {"open-board", "openboard", "close-open"}:
        from .open_board import cycle_open_board

        return cycle_open_board()
    if name in {
        "turbulence-intensity",
        "turbulence",
        "intensity",
        "reduced-turbulence",
    }:
        from .turbulence_intensity import cycle_turbulence_intensity

        return cycle_turbulence_intensity()
    raise ValueError(
        f"unknown cycle {name!r}; expected missing-damping, control, "
        "mechanical-electrical, drag, leftover-repair, localized-repair "
        "(use --excise K to cut a single step), open-board, or "
        "turbulence-intensity"
    )


def run_benchmarks() -> dict[str, Any]:
    damping = cycle_missing_damping()
    control, _sim = cycle_inverse_control()
    analog = cycle_mechanical_electrical()
    drag = cycle_drag_reduction()
    recovered = (damping.residual.to_dict() if damping.residual else {})
    return {
        "missing_damping": {
            "passed": damping.validation_gate == ValidationGate.COMPUTATIONAL,
            "missing_role": recovered.get("missing_role"),
            "recovered": recovered.get("recovered_parameter"),
        },
        "inverse_control": {
            "passed": bool((control.prediction or {}).get("settled")),
            "prediction": control.prediction,
        },
        "mechanical_electrical": {
            "kind": None if analog.translation is None else analog.translation.kind.value,
            "mapping": None if analog.translation is None else analog.translation.mapping,
            "verdicts": [
                c.verdict.value for c in (analog.translation.compatibility if analog.translation else [])
            ],
        },
        "drag_surrogate": drag.prediction,
    }
