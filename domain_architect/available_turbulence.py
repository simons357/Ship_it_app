"""Available-tech turbulence-reduction stack with a 15% DA setpoint.

Desired state is the recognized setpoint x → 0.85 (15% below the
industry-standard no-actuation intensity). Hardware is off-the-shelf
sawtooth riblets plus discrete wall suction. Literature envelopes are
cited as ranges, not added, and not computed by Domain Architect.

The lumped analog can computationally *realize* 15%. The hardware stack
does not; that gate stays empirical[unverified].

Not 3D Navier–Stokes. Not a tank certificate. Clay is NOT CLAIMED.
"""

from __future__ import annotations

import re
from typing import Any

from .catalog import default_catalog
from .cycle import CycleReport
from .decompose import decompose
from .schema import CorrespondenceKind, ValidationGate
from .synthesize import Provenance, inverse_design_architecture, is_recognized_setpoint
from .turbulence_intensity import (
    BELOW_INDUSTRY_FRACTION,
    INDUSTRY_STANDARD_X,
    cycle_turbulence_intensity,
    turbulence_intensity_lab,
)


REFUSED = (
    "no 3D Navier–Stokes regularity claim",
    "no adding literature percentages as a proof",
    "no Clay / unaugmented smoothness",
    "no archived coating dump as this plant",
    "no lab-only slip as field hardware",
    "no phononic film as a DA-certified layer",
    "no licensing band as a tank result",
    "no 9–14% first-cycle lab as a DA result",
    "no provisional patent filing by Domain Architect",
)

# Synthesize of x → 0.85 stays the analog PD loop unless the caller
# actually asks for field hardware. "manufacturable" alone is not enough.
_HARDWARE_CONSTRAINT_MARKERS = (
    "hardware already available",
    "available-tech",
    "available-turbulence",
    "available stack",
    "available now",
    "field-ready hardware",
    "riblet",
    "discrete suction",
    "discrete-suction",
)

# Hardware catalog id → live DA mechanism id. Unselected rows may still
# point at a catalog entry so the refuse path is explicit.
HARDWARE_TO_CATALOG = {
    "sawtooth-riblets": "riblet_geometry",
    "discrete-suction": "discrete_suction",
    "superhydrophobic-slip": "navier_slip",
    "compliant-wall": "compliant_wall",
}


def available_mechanisms() -> tuple[dict[str, Any], ...]:
    """Hardware that already exists. Ranges are published envelopes, not DA CFD."""
    return (
        {
            "id": "sawtooth-riblets",
            "name": "sawtooth riblets",
            "available_now": True,
            "how": (
                "embossed or molded film; triangular or trapezoidal; "
                "spacing s+ about 12–16; height h+ about 8–12"
            ),
            "role": "constraint",
            "geometry": {"s_plus": [12, 16], "h_plus": [8, 12], "section": "triangular-or-trapezoidal"},
            "literature_cf_reduction": {"low": 0.04, "high": 0.10},
            "field_ready": True,
            "selected": True,
            "notes": (
                "Bechert-class riblets. Typical lab skin-friction cut 5–10%. "
                "Flight and marine installs usually sit in the lower half."
            ),
        },
        {
            "id": "discrete-suction",
            "name": "discrete wall suction",
            "available_now": True,
            "how": "porous insert or laser-drilled panel plus a vacuum pump",
            "role": "forcing",
            "literature_cf_reduction": {"low": 0.08, "high": 0.20},
            "field_ready": True,
            "selected": True,
            "notes": (
                "HLFC / discrete suction is existing aerospace hardware. "
                "Contamination and mass-flow are the real constraints."
            ),
        },
        {
            "id": "lebu-blades",
            "name": "outer-layer LEBU blades",
            "available_now": True,
            "how": "thin plates in the outer layer",
            "role": "constraint",
            "literature_cf_reduction": {"low": 0.05, "high": 0.10},
            "field_ready": True,
            "selected": False,
            "notes": "Available geometry. Parasitic drag; not in the default stack.",
        },
        {
            "id": "superhydrophobic-slip",
            "name": "superhydrophobic slip length",
            "available_now": False,
            "how": "lab coatings with trapped gas",
            "role": "constraint",
            "literature_cf_reduction": {"low": 0.10, "high": 0.40},
            "field_ready": False,
            "selected": False,
            "notes": "Lab-available. Not selected: durability is not field-ready.",
        },
        {
            "id": "compliant-wall",
            "name": "viscoelastic compliant wall",
            "available_now": True,
            "how": "elastomer sheet",
            "role": "feedback",
            "literature_cf_reduction": {"low": 0.00, "high": 0.07},
            "field_ready": False,
            "selected": False,
            "notes": "Kramer-class. Replication is mixed. Not selected.",
        },
        {
            "id": "locally-resonant-film",
            "name": "locally resonant polymer film",
            "available_now": False,
            "how": (
                "thin phononic / locally resonant polymer, 50–300 µm, "
                "optional sparse piezoelectric or plasma assist"
            ),
            "role": "constraint",
            "literature_cf_reduction": None,
            "field_ready": False,
            "selected": False,
            "notes": (
                "Licensing overlay, not field hardware. Not selected. "
                "No DA skin-friction envelope. Not an archived coating dump."
            ),
        },
    )


def _catalog_by_id() -> dict[str, Any]:
    return {m.mechanism_id: m for m in default_catalog()}


def _bind_catalog(row: dict[str, Any]) -> dict[str, Any]:
    bound = dict(row)
    mid = HARDWARE_TO_CATALOG.get(row["id"])
    bound["catalog_id"] = mid
    if mid is None:
        bound["catalog"] = None
        return bound
    mech = _catalog_by_id()[mid]
    bound["catalog"] = mech.to_dict()
    return bound


def _envelope(selected: list[dict[str, Any]]) -> dict[str, Any]:
    ranged = [m for m in selected if m.get("literature_cf_reduction")]
    highs = [m["literature_cf_reduction"]["high"] for m in ranged]
    lows = [m["literature_cf_reduction"]["low"] for m in ranged]
    selected_high = max(highs) if highs else 0.0
    selected_low = min(lows) if lows else 0.0
    target_cut = BELOW_INDUSTRY_FRACTION
    return {
        "selected_low": selected_low,
        "selected_high": selected_high,
        "target_cut": target_cut,
        "envelope_can_contain_target": selected_high >= target_cut - 1e-12,
        "percentages_were_added": False,
        "sum_of_highs_not_used": sum(highs),
    }


def _stack_candidate(
    setpoint: str,
    constraints: list[str],
    selected: list[dict[str, Any]],
    notes: list[str],
):
    loop = inverse_design_architecture(setpoint, constraints)
    catalog = _catalog_by_id()
    for row in selected:
        mid = HARDWARE_TO_CATALOG[row["id"]]
        mech = catalog[mid]
        label = f"{mech.mechanism_id} ({mech.operator})"
        if label not in loop.components:
            loop.components.append(label)
        loop.provenance.append(
            Provenance(
                source=mech.mechanism_id,
                original_domain=mech.domain,
                functional_role=mech.signature.role.value,
                translation=None,
                assumptions=[
                    "hardware already available",
                    "literature envelope is not a Domain Architect CFD result",
                ],
                compatibility_checks=["field_ready", "available_now", "selected"],
                modifications=[],
                evidence=[mech.notes or row["notes"]],
                validation_status=ValidationGate.MATHEMATICAL.value,
            )
        )
    loop.name = "available_turbulence_stack"
    loop.hypothesis = (
        f"Target {setpoint!r} is the desired intensity state. Compatible "
        "field-ready mechanisms: sawtooth riblets (constraint) and discrete "
        "wall suction (forcing). Correspondence is analogy, not a declared T. "
        "Literature envelopes are not added. Hardware 15% is not certified."
    )
    loop.notes = list(loop.notes) + list(notes)
    return loop


def wants_available_hardware(constraints: list[str]) -> bool:
    """True when inverse design should assemble the field-ready stack."""
    blob = " ".join(str(c) for c in constraints).lower()
    return any(marker in blob for marker in _HARDWARE_CONSTRAINT_MARKERS)


def is_desired_intensity_setpoint(target: str) -> bool:
    """The DA 15% plug-in: recognized x★ = 0.85, not a drag slogan."""
    if not is_recognized_setpoint(target):
        return False
    match = re.search(r"(?:=|→|->)\s*([0-9]*\.?[0-9]+)", target or "")
    if match is None:
        return False
    try:
        value = float(match.group(1))
    except ValueError:
        return False
    return abs(value - (1.0 - BELOW_INDUSTRY_FRACTION)) < 1e-9


def maybe_available_stack(
    target: str,
    constraints: list[str],
) -> dict[str, Any] | None:
    """Inverse-design payload for the available-tech stack, or None.

    A13 still refuses slogans. Bare ``x → 0.85`` with only a saturation
    constraint stays the analog PD loop. Hardware language selects this
    stack. The analog can realize 15%; hardware stays unverified.
    """
    if not is_desired_intensity_setpoint(target):
        return None
    if not wants_available_hardware(constraints):
        return None
    payload = available_turbulence_system()
    out = dict(payload["candidate"])
    out["board"] = payload["board"]
    out["protocol"] = "available-turbulence"
    out["realized_or_desired"] = payload["realized_or_desired"]
    return out


def _stack_board(payload: dict[str, Any]) -> dict[str, Any]:
    """Human-readable keep/refuse board. Not a tank certificate."""
    analog = payload.get("analog") or {}
    overlay = payload.get("licensing_overlay") or {}
    lines = [
        "AVAILABLE-TECH TURBULENCE STACK",
        payload.get("headline") or "",
        (
            "desired {setpoint}  analog relative reduction={red:.3f}  "
            "hardware_realized={hw}  envelope_contains_15%={env}"
        ).format(
            setpoint=(payload.get("desired") or {}).get("as_setpoint"),
            red=float(analog.get("relative_reduction") or 0.0),
            hw=(payload.get("states") or {}).get("hardware_realized", {}).get("value"),
            env=payload.get("envelope_can_contain_target"),
        ),
        (
            "commercial band 8–12% is a licensing target inside the selected "
            "envelope, not a tank number. Percentages were not added."
        ),
        "",
        "SELECTED",
    ]
    for row in payload.get("stack") or []:
        lit = row.get("literature_cf_reduction") or {}
        low = 100.0 * float(lit.get("low") or 0.0)
        high = 100.0 * float(lit.get("high") or 0.0)
        lines.append(
            f"  {row['id']}  {row['role']}  literature {low:.0f}–{high:.0f}%"
        )
    lines.append("NOT SELECTED")
    for row in payload.get("catalog") or []:
        if row.get("selected"):
            continue
        lines.append(f"  {row['id']}  {row.get('notes') or 'not selected'}")
    lines.append("GROK HYBRID SKETCH")
    for piece in overlay.get("pieces") or []:
        mark = "kept" if piece.get("kept") else "refused"
        lines.append(f"  {mark}  {piece.get('id')}  {piece.get('note')}")
    lines.extend(
        [
            "Clay is NOT CLAIMED.",
            "Not 3D Navier–Stokes. Not a tank certificate.",
        ]
    )
    return {
        "kind": "available-turbulence",
        "text": "\n".join(lines),
        "selected": [m["id"] for m in payload.get("stack") or []],
        "refused_overlay": [
            p["id"] for p in overlay.get("pieces") or [] if not p.get("kept")
        ],
    }


def _licensing_overlay(envelope: dict[str, Any]) -> dict[str, Any]:
    """External hybrid-film sketch. DA keeps geometry/regime; refuses the rest."""
    commercial_high = 0.12
    return {
        "name": "hybrid riblet + locally resonant film",
        "source": "external licensing sketch, not a Domain Architect CFD result",
        "da_verdict": (
            "partial — riblet geometry and cruise regime kept; "
            "resonant film not selected; 9–14% lab not awarded; "
            "patent filing is attorney-owned"
        ),
        "commercial_target": {"low": 0.08, "high": commercial_high},
        "claimed_first_cycle_lab": {
            "low": 0.09,
            "high": 0.14,
            "da_status": "refused",
            "reason": "not a Domain Architect measurement or simulation",
        },
        "inside_selected_envelope": envelope["selected_high"] >= commercial_high - 1e-12,
        "pieces": [
            {
                "id": "cruise-regime",
                "kept": True,
                "role": "constraint",
                "note": "application context only; not LES",
            },
            {
                "id": "riblet-geometry",
                "kept": True,
                "role": "constraint",
                "note": "s+ 12–16, h+ 8–12, embossed/molded film",
            },
            {
                "id": "resonant-film",
                "kept": False,
                "role": "constraint",
                "note": "not field-ready; no DA skin-friction envelope",
            },
            {
                "id": "piezo-plasma-assist",
                "kept": False,
                "role": "forcing",
                "note": "optional overlay; not in the default stack",
            },
            {
                "id": "first-cycle-9-14-lab",
                "kept": False,
                "role": "output",
                "note": "expected lab band is not a DA result",
            },
            {
                "id": "provisional-patent",
                "kept": False,
                "role": "constraint",
                "note": "attorney-owned; DA does not file claims",
            },
        ],
        "licensing_package_owed": [
            "wind-tunnel and simulation performance data",
            "manufacturing specification",
            "application process",
            "durability and maintenance data",
            "cost / payback model",
            "field-of-use options",
        ],
        "da_does_not_file": True,
    }


def available_turbulence_system() -> dict[str, Any]:
    """Assemble the stack and attach the 15% analog check."""
    analog = turbulence_intensity_lab()
    catalog = [_bind_catalog(m) for m in available_mechanisms()]
    selected = [m for m in catalog if m["selected"]]
    envelope = _envelope(selected)
    setpoint = analog["desired"]["as_setpoint"]
    constraints = [
        f"|u| ≤ 6",
        "manufacturable",
        "hardware already available",
        "no lab-only slip",
        "no phononic film as certified layer",
    ]
    notes = [
        (
            "Industry standard is the smooth-wall / no-actuation intensity "
            f"x = {INDUSTRY_STANDARD_X}. Desired state is {setpoint} "
            f"({BELOW_INDUSTRY_FRACTION:.0%} below that)."
        ),
        "Default stack: sawtooth riblets (passive) plus discrete suction (active).",
        "Literature ranges are not added. DA does not certify a tank result.",
        "Commercial 8–12% is a licensing band inside the selected envelope, not a hardware certificate.",
        "Hybrid resonant-film overlay is catalogued and not selected. 9–14% lab is refused.",
        "Patent filing is attorney-owned. DA does not file claims.",
        "The computational gate is the lumped analog, not the hardware.",
        "Clay is NOT CLAIMED.",
    ]
    candidate = _stack_candidate(setpoint, constraints, selected, notes)
    analog_realized = bool(analog["reduced_vs_control"])
    payload = {
        "protocol": "available-turbulence",
        "headline": (
            "desired x → 0.85 (15% below industry); analog realized; "
            "hardware empirical[unverified]"
        ),
        "industry_standard": analog["industry_standard"],
        "desired": analog["desired"],
        "realized_or_desired": "desired",
        "states": {
            "desired": {
                "setpoint": setpoint,
                "below_industry_fraction": BELOW_INDUSTRY_FRACTION,
                "plug_in": "desired",
            },
            "analog_realized": {
                "value": analog_realized,
                "relative_reduction": analog["relative_reduction"],
                "gate": analog["validation_gate"],
                "plant": "lumped intensity analog",
            },
            "hardware_realized": {
                "value": False,
                "gate": "empirical[unverified]",
                "reason": (
                    "selected literature high envelope can contain 15% "
                    "(suction); DA does not award a tank or DNS certificate"
                ),
            },
        },
        "target_cut": BELOW_INDUSTRY_FRACTION,
        "operating_regime": {
            "primary": "aircraft cruise boundary layer",
            "mach": [0.75, 0.85],
            "altitude_ft": [30000, 40000],
            "re_tau_panel": [1000, 5000],
            "secondary": ["ship hull", "submarine hull", "internal duct"],
            "notes": "Application context. DA did not run LES or a wind tunnel.",
        },
        "commercial_band": {
            "low": 0.08,
            "high": 0.12,
            "source": "licensing target, not a Domain Architect CFD result",
            "inside_selected_envelope": envelope["selected_high"] >= 0.12 - 1e-12,
            "relation_to_desired": (
                "8–12% is a commercial band inside the selected literature "
                "envelope. DA desired remains 15%."
            ),
        },
        "licensing_overlay": _licensing_overlay(envelope),
        "empirical_next": [
            "wall-resolved LES of the selected riblet geometry",
            "down-select two or three geometries",
            "modular test panels 10–30 cm",
            "direct drag measurement (balance or oil-film interferometry)",
            "durability coupons (abrasion, UV, temperature, fluid)",
        ],
        "stack": selected,
        "catalog": catalog,
        **envelope,
        "analog": {
            "control_x": analog["control_arm"]["terminal_x"],
            "treated_x": analog["treated_arm"]["terminal_x"],
            "relative_reduction": analog["relative_reduction"],
            "reduced_vs_control": analog["reduced_vs_control"],
        },
        "candidate": candidate.to_dict(),
        "refused": list(REFUSED),
        "kind": CorrespondenceKind.ANALOGY.value,
        "validation_gate": analog["validation_gate"],
        "notes": notes,
    }
    payload["board"] = _stack_board(payload)
    return payload


def cycle_available_turbulence() -> CycleReport:
    payload = available_turbulence_system()
    analog_report = cycle_turbulence_intensity()
    plant = decompose(
        "xdd + a*xd + k*x = k*1.0 + u",
        name="available_turbulence_plant",
    )
    selected = [m for m in payload["stack"]]
    candidate = _stack_candidate(
        payload["desired"]["as_setpoint"],
        [
            "|u| ≤ 6",
            "manufacturable",
            "hardware already available",
        ],
        selected,
        list(payload["notes"]),
    )
    return CycleReport(
        mode="available-turbulence",
        target=payload["desired"]["as_setpoint"],
        constraints=[
            "|u| ≤ 6",
            "manufacturable",
            "hardware already available",
            "15% below industry-standard intensity",
        ],
        decomposition=plant,
        translation=None,
        candidate=candidate,
        prediction=payload,
        residual=None,
        validation_gate=analog_report.validation_gate,
        notes=list(payload["notes"])
        + analog_report.notes[:2]
        + ["Clay is NOT CLAIMED."],
        method_credits=[
            "available riblet geometry",
            "available discrete suction",
            "RK4 analog vs no-actuation control",
        ],
    )
