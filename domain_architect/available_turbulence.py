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

SEAWATER_NU_15C = 1.2e-6  # m²/s, order of magnitude for 15 °C seawater


def shear_velocity(U: float, cf: float) -> float:
    """u_τ = U √(C_f / 2). First-order station estimate, not a CFD profile."""
    if U <= 0.0 or cf <= 0.0:
        raise ValueError("U and cf must be positive")
    return float(U) * (float(cf) / 2.0) ** 0.5


def riblet_spacing_m(*, s_plus: float, nu: float, u_tau: float) -> float:
    """s = s+ ν / u_τ. Wall units, not a manufactured tolerance."""
    if s_plus <= 0.0 or nu <= 0.0 or u_tau <= 0.0:
        raise ValueError("s_plus, nu, and u_tau must be positive")
    return float(s_plus) * float(nu) / float(u_tau)


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
                "embossed or molded film in a fouling-release carrier; "
                "trapezoidal preferred; s+ about 15–17; h/s = 0.5"
            ),
            "role": "constraint",
            "geometry": {
                "s_plus": [15, 17],
                "h_over_s": 0.5,
                "h_plus": [7.5, 8.5],
                "section": "trapezoidal-durable",
            },
            "literature_cf_reduction": {"low": 0.04, "high": 0.10},
            "field_ready": True,
            "selected": True,
            "notes": (
                "Bechert 1997 oil-channel: trapezoid about 8.2% at s+≈17, "
                "h/s=0.5; thin blades 9.9% are not field-durable. "
                "Marine fouling-release riblets: about 6% in Couette (Bressy 2018)."
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
    lines.append("SHIP PRODUCT (MAERSK-CLASS)")
    ship = payload.get("ship_package") or {}
    cf = ship.get("cf_reduction_target") or {}
    lines.append(
        "  desired Cf {lo:.0f}–{hi:.0f}%  durable lab ceiling {lab:.1f}%  "
        "contains_8%={c8}  contains_12%={c12}".format(
            lo=100.0 * float(cf.get("low") or 0.0),
            hi=100.0 * float(cf.get("high") or 0.0),
            lab=100.0 * float(cf.get("durable_lab_high") or 0.0),
            c8=cf.get("contains_8pct"),
            c12=cf.get("contains_12pct"),
        )
    )
    lines.append("  selected: trapezoidal riblets in fouling-release carrier")
    lines.append("  not selected: hull suction, resonant film, thin blades")
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
            "partial — riblet geometry kept; ship hull is now the primary regime; "
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
                "id": "ship-regime",
                "kept": True,
                "role": "constraint",
                "note": "primary market: large cargo / container hull; not a towing-tank result",
            },
            {
                "id": "cruise-regime",
                "kept": True,
                "role": "constraint",
                "note": "secondary application context only; not LES",
            },
            {
                "id": "riblet-geometry",
                "kept": True,
                "role": "constraint",
                "note": "s+ 15–17, h/s = 0.5, trapezoidal, embossed fouling-release film",
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


def _ship_stations() -> list[dict[str, Any]]:
    """First-order s from s+ ν / u_τ at two cargo speeds. Not a hull map."""
    stations = (
        {"id": "slow-steamer", "speed_kn": 15.0, "U": 7.72, "cf": 0.002},
        {"id": "container-cruise", "speed_kn": 22.0, "U": 11.32, "cf": 0.002},
    )
    out = []
    for row in stations:
        u_tau = shear_velocity(row["U"], row["cf"])
        s16 = riblet_spacing_m(s_plus=16.0, nu=SEAWATER_NU_15C, u_tau=u_tau)
        s17 = riblet_spacing_m(s_plus=17.0, nu=SEAWATER_NU_15C, u_tau=u_tau)
        h = 0.5 * s16
        out.append(
            {
                **row,
                "u_tau": u_tau,
                "s_m_at_splus_16": s16,
                "s_m_at_splus_17": s17,
                "h_m_at_hs_0_5": h,
                "s_um_band": [round(1e6 * s16, 1), round(1e6 * s17, 1)],
            }
        )
    return out


def _ship_package() -> dict[str, Any]:
    """Maersk-class hull product spec. Resonant film stays unselected."""
    stations = _ship_stations()
    durable_lab_high = 0.082  # Bechert trapezoid, not blades
    marine_couette = 0.06  # Bressy 2018 Intersleek-class riblets
    cf_lo, cf_hi = 0.08, 0.12
    fuel_lo, fuel_hi = 0.04, 0.08
    return {
        "name": "ship-hull riblet film",
        "primary_market": "large cargo / container ships",
        "customer": "Maersk-class liner and similar",
        "realized_or_desired": "desired",
        "cf_reduction_target": {
            "low": cf_lo,
            "high": cf_hi,
            "plug_in": "desired",
            "durable_lab_high": durable_lab_high,
            "marine_couette_high": marine_couette,
            "contains_8pct": durable_lab_high >= cf_lo - 1e-12,
            "contains_12pct": durable_lab_high >= cf_hi - 1e-12,
            "notes": (
                "8% sits at the Bechert trapezoid lab ceiling. "
                "12% is not contained by established marine-durable riblets. "
                "In-service net is usually lower because of fouling."
            ),
        },
        "fuel_translation": {
            "low": fuel_lo,
            "high": fuel_hi,
            "basis": (
                "frictional resistance is about 70–90% of calm-water RT for "
                "low-speed bulkers/tankers and about 50–65% for faster "
                "container ships (Wärtsilä / standard split). "
                "4–8% fuel is consistent with 6–10% Cf only if that Cf is "
                "actually achieved on a clean hull. Not a DA measurement."
            ),
            "da_status": "hypothesis",
        },
        "product_stack": [
            {
                "id": "trapezoidal-riblets",
                "selected": True,
                "role": "constraint",
                "geometry": {
                    "s_plus": [15, 17],
                    "h_over_s": 0.5,
                    "section": "trapezoidal",
                    "physical_s_um": "about 50–90 µm at cargo u_τ",
                },
                "carrier": "fouling-release fluoropolymer or silicone, embossed",
                "literature": "Bechert 1997 JFM 338:59; Bressy et al. 2018 Biofouling",
            }
        ],
        "not_selected_for_hull": [
            {
                "id": "discrete-suction",
                "reason": "HLFC hardware; pumps and seawater fouling are not a Maersk film product",
            },
            {
                "id": "locally-resonant-film",
                "reason": (
                    "no established skin-friction envelope at ship Re. "
                    "Kramer-class compliant walls have mixed replication. "
                    "Not an archived coating dump."
                ),
            },
            {
                "id": "thin-blade-riblets",
                "reason": "Bechert 9.9% is real in oil channel and not field-durable",
            },
        ],
        "stations": stations,
        "coating_approaches": [
            {
                "id": "embossed-fouling-release",
                "established": True,
                "what": (
                    "emboss trapezoidal riblets into a fouling-release system "
                    "already used on commercial hulls"
                ),
                "evidence": "Bressy 2018: up to 6% vs smooth in Taylor–Couette; fouling still the limiter",
            },
            {
                "id": "molded-film",
                "established": True,
                "what": "pre-molded riblet film applied as sheets, aligned with local streamlines",
                "evidence": "3M-class riblet films; yaw and application alignment are known failure modes",
            },
            {
                "id": "phononic-overlay",
                "established": False,
                "what": "50–300 µm locally resonant polymer over or co-molded with riblets",
                "evidence": "not selected; no DA Cf envelope; must be physically tested before any claim",
            },
        ],
        "validation_plan": [
            "wall-resolved LES of trapezoid s+=15–17 at Re_τ about 1000–2000 (not Re_L 1e9)",
            "Taylor–Couette or oil-film Cf on 10–30 cm coupons vs smooth FR control",
            "towing-tank panels at the highest reachable Re, same control",
            "static plus dynamic seawater fouling; confirm grooves do not fill",
            "abrasion, UV, temperature, and dry-dock handling coupons",
            "ISO 19030 in-service comparison is later; it is not this first cycle",
        ],
        "durability": [
            "survive dry-dock blasting/handling and fender abrasion",
            "keep s and h after biofilm and slime; fouling-release is mandatory",
            "no biocide requirement beyond the carrier's existing approval path",
            "target life aligned with a coating interval, not a DA number",
        ],
        "must_physically_test": [
            "clean-hull Cf vs smooth FR control at the same Re_τ band",
            "fouled-hull Cf; static biofilm is expected to hurt riblets",
            "yaw / cross-flow; misaligned riblets can increase Cf",
            "full-scale application tolerance on a curved hull",
            "any phononic overlay, separately, against a riblet-only control",
        ],
        "risks": [
            "12% net Cf at ship Re is outside the durable riblet literature",
            "fouling can erase a lab Cf gain (Bressy: more biofilm at rest)",
            "tunnel Re does not equal ship Re_L ~ 1e9",
            "yawed flow on a real hull",
            "phononic / locally resonant layers are not an established Cf mechanism at ship Re",
        ],
        "requested_roadmap": {
            "horizon": "6–12 months",
            "da_status": "requested plan, not a Domain Architect schedule certificate",
            "gates": [
                "geometry freeze: trapezoid s+=15–17, h/s=0.5, two physical s from cargo u_τ",
                "coupon manufacture in an existing FR system",
                "clean Cf (Couette or tunnel) vs smooth FR",
                "fouling exposure and re-test",
                "one towing-tank campaign",
                "data room for a coatings partner; no ISO 19030 claim yet",
            ],
        },
        "patent_ideas_attorney_owned": [
            "method of embossing trapezoidal s+=15–17 riblets into a specified fouling-release chemistry",
            "shipyard application process that preserves local streamline alignment",
            "do not claim an unproven phononic burst-frequency mechanism as the invention",
        ],
        "da_does_not_file": True,
        "maersk_note": (
            "Domain Architect can offer a fouling-release trapezoidal riblet "
            "film sized in wall units to cargo-ship shear, aimed at a desired "
            "6–8% clean-hull Cf cut (lab ceiling about 8%). An 8–12% net Cf "
            "target at full scale is a commercial stretch, not a measured result. "
            "A resonant overlay is a separate experiment, not part of the "
            "field-ready stack. Next evidence: coupon Cf and fouling, then a "
            "partner towing-tank. DA does not file patents."
        ),
        "kind": CorrespondenceKind.ANALOGY.value,
        "validation_gate": "empirical[unverified]",
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
        "Commercial 8–12% is a licensing band. Durable trapezoid riblets contain 8%, not 12%.",
        "Ship-primary product is a fouling-release riblet film. Suction and resonant film are not the hull stack.",
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
            "primary": "large cargo / container ship hull",
            "customer": "Maersk-class liner and similar",
            "speed_kn": [12, 22],
            "re_L_full_scale": "O(1e9)",
            "re_tau_panel": [1000, 5000],
            "secondary": ["aircraft cruise", "submarine hull", "internal duct"],
            "aircraft_cruise": {
                "mach": [0.75, 0.85],
                "altitude_ft": [30000, 40000],
            },
            "notes": "Application context. DA did not run LES or a towing tank.",
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
        "ship_package": _ship_package(),
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
