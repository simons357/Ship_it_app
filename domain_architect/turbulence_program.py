"""Turbulence-reduction program: four applications under one DA project.

Program
    turbulence-reduction
Applications
    ships       ACTIVE   (Maersk-class hull; ship_package)
    missiles    QUEUED   (high-speed external flow)
    submarines  QUEUED
    drones      QUEUED

Correspondence is analogy, not a declared T across platforms.
Not 3D Navier–Stokes. Clay is NOT CLAIMED. DA does not file patents.
"""

from __future__ import annotations

from typing import Any

from .available_turbulence import available_turbulence_system
from .cycle import CycleReport
from .decompose import decompose
from .schema import CorrespondenceKind, ValidationGate
from .synthesize import CandidateArchitecture, Provenance


APPLICATION_ORDER = ("ships", "missiles", "submarines", "drones")

REFUSED = (
    "no 3D Navier–Stokes regularity claim",
    "no Clay / unaugmented smoothness",
    "no adding literature percentages as a proof",
    "no one stack copied across platforms without a new study",
    "no phononic film as a DA-certified layer",
    "no 9–14% lab as a DA result",
    "no provisional patent filing by Domain Architect",
)


def _queued_application(
    *,
    id: str,
    title: str,
    regime: str,
    why_separate: str,
    next_study: str,
    spec: str,
    **extra: Any,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "id": id,
        "title": title,
        "status": "QUEUED",
        "realized_or_desired": "desired",
        "cycle": None,
        "spec": spec,
        "stack_selected": [],
        "envelope_awarded": False,
        "operating_regime": regime,
        "why_separate": why_separate,
        "next_study": next_study,
        "validation_gate": ValidationGate.MATHEMATICAL.value,
        "notes": [
            "Queued. DA has not run a study on this application.",
            "Do not copy the ship riblet envelope here.",
            "Clay is NOT CLAIMED.",
        ],
    }
    row.update(extra)
    return row


def applications() -> tuple[dict[str, Any], ...]:
    ships = available_turbulence_system()
    ship_pkg = ships.get("ship_package") or {}
    return (
        {
            "id": "ships",
            "title": "large cargo / container ships",
            "status": "ACTIVE",
            "customer": ship_pkg.get("customer"),
            "realized_or_desired": "desired",
            "cycle": "available-turbulence",
            "spec": "docs/projects/turbulence-reduction/ships.md",
            "operating_regime": "large cargo / container ship hull (Maersk-class)",
            "envelope_awarded": False,
            "cf_reduction_target": ship_pkg.get("cf_reduction_target"),
            "fuel_translation": ship_pkg.get("fuel_translation"),
            "product_stack": ship_pkg.get("product_stack"),
            "not_selected_for_hull": ship_pkg.get("not_selected_for_hull"),
            "contains_8pct": (ship_pkg.get("cf_reduction_target") or {}).get(
                "contains_8pct"
            ),
            "contains_12pct": (ship_pkg.get("cf_reduction_target") or {}).get(
                "contains_12pct"
            ),
            "validation_gate": ship_pkg.get("validation_gate"),
        },
        _queued_application(
            id="missiles",
            title="high-speed missiles",
            regime=(
                "high-Re external flow; compressibility and heat may dominate "
                "skin friction. Not a hull coating study."
            ),
            why_separate=(
                "Ship wall units and fouling-release chemistry do not transfer. "
                "Need a new decompose of the compressible near-wall layer."
            ),
            spec="docs/projects/turbulence-reduction/missiles.md",
            next_study="new DA application study after ships; do not copy ship_package",
            not_a_weapon_design=True,
        ),
        _queued_application(
            id="submarines",
            title="submarines",
            regime=(
                "submerged high-pressure seawater; quiet operation; "
                "biofouling and coating acoustic impedance matter."
            ),
            why_separate=(
                "Cargo-ship riblets are sized to a different u_τ and a "
                "fouling-release interval. Submarine quieting is a new constraint."
            ),
            spec="docs/projects/turbulence-reduction/submarines.md",
            next_study="new DA application study; do not copy ship_package",
        ),
        _queued_application(
            id="drones",
            title="drones",
            regime=(
                "low-to-moderate Re; mixed laminar/turbulent patches; "
                "mass and power budgets dominate."
            ),
            why_separate=(
                "A 50–90 µm ship riblet is the wrong scale and the wrong "
                "weight budget. Need a new decompose."
            ),
            spec="docs/projects/turbulence-reduction/drones.md",
            next_study="new DA application study after ships and/or missiles",
        ),
    )


def turbulence_reduction_program() -> dict[str, Any]:
    apps = list(applications())
    by_id = {row["id"]: row for row in apps}
    active = [row["id"] for row in apps if row["status"] == "ACTIVE"]
    queued = [row["id"] for row in apps if row["status"] == "QUEUED"]
    lines = [
        "TURBULENCE REDUCTION PROGRAM",
        "four applications under one project. Ships is ACTIVE. The rest are QUEUED.",
        "Correspondence is analogy. Do not copy one envelope onto another platform.",
        "",
        "ACTIVE",
    ]
    for row in apps:
        if row["status"] != "ACTIVE":
            continue
        lines.append(
            f"  {row['id']}  {row['title']}  8% contained={row.get('contains_8pct')}  "
            f"12% contained={row.get('contains_12pct')}"
        )
    lines.append("QUEUED")
    for row in apps:
        if row["status"] != "QUEUED":
            continue
        lines.append(f"  {row['id']}  {row['title']}  envelope not awarded")
    lines.extend(
        [
            "Clay is NOT CLAIMED.",
            "Not 3D Navier–Stokes. DA does not file patents.",
        ]
    )
    board = {"kind": "turbulence-reduction", "text": "\n".join(lines)}
    return {
        "protocol": "turbulence-reduction",
        "headline": (
            "turbulence-reduction program: ships ACTIVE; "
            "missiles, submarines, drones QUEUED"
        ),
        "project": "turbulence-reduction",
        "home": "docs/projects/turbulence-reduction/README.md",
        "application_order": list(APPLICATION_ORDER),
        "applications": apps,
        "by_id": by_id,
        "active": active,
        "queued": queued,
        "board": board,
        "refused": list(REFUSED),
        "kind": CorrespondenceKind.ANALOGY.value,
        "validation_gate": ValidationGate.MATHEMATICAL.value,
        "notes": [
            "This is a program, not a single plant.",
            "Ships (Maersk-class) is the live application. See ship_package.",
            "Missiles, submarines, and drones are queued slots for later DA studies.",
            "Do not copy the ship riblet envelope onto those platforms.",
            "Clay is NOT CLAIMED.",
        ],
    }


def cycle_turbulence_reduction() -> CycleReport:
    payload = turbulence_reduction_program()
    plant = decompose(
        "Cf_net = Cf_net(application, geometry, coating, Re)",
        name="turbulence_reduction_program",
    )
    candidate = CandidateArchitecture(
        name="turbulence_reduction_program",
        components=[
            "program: turbulence-reduction",
            "application ships (ACTIVE)",
            "application missiles (QUEUED)",
            "application submarines (QUEUED)",
            "application drones (QUEUED)",
        ],
        replaced={},
        hypothesis=(
            "Skin-friction reduction is a program of four applications. "
            "Only ships has a candidate stack. The others are queued. "
            "Correspondence across platforms is analogy, not a declared T."
        ),
        provenance=[
            Provenance(
                source="turbulence-reduction program",
                original_domain="program",
                functional_role="constraint",
                translation=None,
                assumptions=[
                    "four named applications",
                    "do not copy envelopes across platforms",
                ],
                compatibility_checks=["application slots named"],
                modifications=[],
                evidence=["ships ACTIVE; missiles/submarines/drones QUEUED"],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        ],
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=list(payload["notes"]),
    )
    return CycleReport(
        mode="turbulence-reduction",
        target="four-application turbulent skin-friction program",
        constraints=[
            "available technology",
            "no unproven physics",
            "one application at a time",
            "ships first",
        ],
        decomposition=plant,
        translation=None,
        candidate=candidate,
        prediction=payload,
        residual=None,
        validation_gate=ValidationGate.MATHEMATICAL,
        notes=list(payload["notes"]),
        method_credits=["program decompose", "ship_package for the active slot"],
    )
