"""Tube estimate: the live geometric write on Track B.

Split the swirl source, apply localized Hardy with a wall, choose δ from
the dominant shell. The wall is a two-sided cylinder: Hardy dumps 2h(δ)²
from inside; Young can buy the same number from outside IF swirl vanishes
at an outer radius. That trace is not I_off. Domination of I_tube is OPEN.

Not a regularity proof. Not A⇒B. Keep 1/r^4. Keep Γ.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Final

import numpy as np


WALL_DIAGRAM: Final[str] = """
        z                         the wall r=δ is a cylinder
        |                         Hardy (inside) dumps  2 h(δ)²
  off   |   off     r ≥ δ         Young  (outside) can buy the
 -------+-------    r = δ         same number IFF h→0 at some R
  TUBE  |  TUBE     r < δ         I_off is a different monomial
        |                         (Γ ∂_z Γ) ω^r / r³, not h²/r
        r                         T^3 has no outer vanishing
"""

# h = Γ/r. Weights after the r dr measure is already in the 1-D Hardy line.
MONOMIALS: Final[tuple[dict[str, str], ...]] = (
    {
        "id": "HARDY-WEIGHT",
        "expression": "h²/r  with h=Γ/r  →  Γ²/r³",
        "lives": "radial 1-D, inside or outside the wall",
        "status": "controlled by T2 inside, T3a outside (if h(R)=0)",
    },
    {
        "id": "WALL",
        "expression": "2 h(δ)² = 2 (Γ/δ)²  on the cylinder r=δ",
        "lives": "surface, shared face of tube and off-axis",
        "status": "ID'd CLIP-B4-WALL; T3a buys it from outside under extra E",
    },
    {
        "id": "I-OFF",
        "expression": "r^{-4} ∂_z(Γ²) ω^r · (r dr dz)  →  (Γ ∂_z Γ) ω^r / r³",
        "lives": "volume r≥δ, needs a z-derivative and ω^r",
        "status": "same r-weight as Hardy, different fields — CLIP-T3-WELD",
    },
    {
        "id": "I-TUBE",
        "expression": "2 Γ ∂_z Γ / r^4  on r<δ",
        "lives": "volume inside the cylinder",
        "status": "open vs viscosity  CLIP-B4b-ITUBE",
    },
    {
        "id": "ANGULAR-VISC",
        "expression": "(u_θ/r)² = (Γ/r²)²",
        "lives": "same tube as I_tube",
        "status": "identity B5; domination open CLIP-B5b-VS-VISC",
    },
)


@dataclass(frozen=True)
class TubeStep:
    step: str
    inequality: str
    status: str
    geometry: str
    clip_id: str
    remainder: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


TUBE_STEPS: Final[tuple[TubeStep, ...]] = (
    TubeStep(
        step="T0",
        inequality="I = ∫ r^{-4} ∂_z(Γ²) ω^r r dr dz = I_off(δ) + I_tube(δ)",
        status="setup",
        geometry="physical split at the wall r=δ",
        clip_id="—",
        remainder="choice of δ still free",
    ),
    TubeStep(
        step="T1",
        inequality="r≥δ  ⇒  |r^{-4} ∂_z(Γ²)| ≤ δ^{-4} |∂_z(Γ²)|",
        status="pass",
        geometry="off-axis: the weight is bounded, I_off is Sobolev",
        clip_id="CLIP-T1-DELTA",
        remainder="negative powers of δ, to be paid by the tube scale",
    ),
    TubeStep(
        step="T2",
        inequality="h(0)=0 ⇒ ∫_0^δ h²/r dr ≤ 4 ∫_0^δ (h')² r dr + 2 h(δ)²",
        status="pass",
        geometry="localized Hardy on the tube; wall term at r=δ from the INSIDE",
        clip_id="CLIP-B4-WALL",
        remainder="2 h(δ)² is ID'd; T3a tries to buy it from the outside",
    ),
    TubeStep(
        step="T3a",
        inequality="h(R)=0 ⇒ h(δ)² ≤ ε ∫_δ^R (h')² r dr + ε^{-1} ∫_δ^R h²/r dr",
        status="pass",
        geometry="Young from the OUTSIDE: the cylinder is a two-sided face",
        clip_id="CLIP-T3-OUTER",
        remainder="needs an outer radius where swirl vanishes — extra E, not T^3",
    ),
    TubeStep(
        step="T3b",
        inequality="off-axis Hardy integrals control I_off  (same r-weight, different fields)",
        status="open",
        geometry="h²/r is Γ²/r³; I_off is (Γ ∂_z Γ) ω^r / r³. Not the same shape.",
        clip_id="CLIP-T3-WELD",
        remainder="the weld of the wall/trace to the swirl source — unmeasured",
    ),
    TubeStep(
        step="T4",
        inequality="δ(t) ∼ 2^{-j_*(t)}  when σ = P_{j*}/X ≥ 1/2",
        status="architecture",
        geometry="tube radius = viscous scale of the concentrated packet",
        clip_id="CLIP-T4-SPREAD",
        remainder="spread regime uses T2/Bony, not this δ",
    ),
    TubeStep(
        step="T5",
        inequality="|I_tube| ≤ ε ν ‖∇ω‖_2² + C_{ε,δ} ‖Γ/r‖_{L^2(tube)}² X^β",
        status="open",
        geometry="Hardy+viscosity contest inside the tube; keep 1/r^4",
        clip_id="CLIP-B4b-ITUBE",
        remainder="the bound itself — this is the live estimate",
    ),
    TubeStep(
        step="T6",
        inequality="angular 1/r² viscosity vs I_tube at the same δ",
        status="open",
        geometry="danger and dissipation occupy the same tube (B5 identity)",
        clip_id="CLIP-B5b-VS-VISC",
        remainder="whether extra Stokes damping wins; ratio is diagnostic, not a close",
    ),
    TubeStep(
        step="T7",
        inequality="dX/dt + ν‖∇ω‖_2² ≤ ε ν‖∇ω‖_2² + C_ε X R(t),  R∈L^1",
        status="open",
        geometry="Gronwall form that would close X in L^∞; R from tube and/or Ring and/or spread",
        clip_id="CLIP-B-REG",
        remainder="integrable R(t) is not constructed",
    ),
)


def hardy_wall_ratio(h: np.ndarray, r: np.ndarray) -> float:
    """Return LHS / RHS of the tube Hardy+wall inequality. Must be ≤ 1 + tol."""
    dr = r[1] - r[0]
    hp = np.gradient(h, dr)
    lhs = float(np.sum((h**2) / np.maximum(r, dr)) * dr)
    rhs = float(4.0 * np.sum((hp**2) * r) * dr + 2.0 * h[-1] ** 2)
    if rhs <= 0.0:
        return float("inf")
    return lhs / rhs


def hardy_wall_probe(
    delta: float = 1.0,
    n: int = 400,
    profiles: tuple[str, ...] = ("r", "r2", "r*(delta-r)", "sin"),
) -> dict[str, Any]:
    """Check B4 on manufactured axis-vanishing profiles."""
    r = np.linspace(delta / n, delta, n)
    makers: dict[str, Callable[[np.ndarray], np.ndarray]] = {
        "r": lambda x: x,
        "r2": lambda x: x**2,
        "r*(delta-r)": lambda x: x * (delta - x),
        "sin": lambda x: np.sin(np.pi * x / delta) * x,
    }
    rows: list[dict[str, Any]] = []
    worst = 0.0
    for name in profiles:
        h = makers[name](r)
        h[0] = 0.0
        ratio = hardy_wall_ratio(h, r)
        rows.append({"profile": name, "lhs_over_rhs": ratio, "holds": ratio <= 1.05})
        worst = max(worst, ratio)
    return {
        "delta": delta,
        "n": n,
        "worst_lhs_over_rhs": worst,
        "holds": worst <= 1.05,
        "profiles": rows,
        "identity": "∫ h²/r ≤ 4∫ (h')² r + 2 h(δ)²",
        "verdict": "pass" if worst <= 1.05 else "fail",
        "notes": "Numeric check of B4 from INSIDE the tube. Does not absorb I_tube.",
    }


def wall_trace_ratio(h: np.ndarray, r: np.ndarray, eps: float = 1.0) -> float:
    """Young from the outside: h(δ)² / (ε∫ r(h')² + ε^{-1}∫ h²/r + h(R)²)."""
    dr = r[1] - r[0]
    hp = np.gradient(h, dr)
    lhs = float(h[0] ** 2)
    rhs = float(
        eps * np.sum((hp**2) * r) * dr
        + (1.0 / eps) * np.sum((h**2) / np.maximum(r, dr)) * dr
        + h[-1] ** 2
    )
    if rhs <= 0.0:
        return float("inf")
    return lhs / rhs


def wall_trace_probe(
    delta: float = 0.25,
    outer: float = 1.0,
    n: int = 400,
    eps: float = 1.0,
) -> dict[str, Any]:
    """T3a: buy the wall from the outside when swirl vanishes at r=R."""
    r = np.linspace(delta, outer, n)
    span = outer - delta
    makers: dict[str, Callable[[np.ndarray], np.ndarray]] = {
        "linear-to-zero": lambda x: (outer - x),
        "quad-to-zero": lambda x: (outer - x) ** 2,
        "sine-to-zero": lambda x: np.sin(0.5 * np.pi * (outer - x) / span),
        "r*(R-r)": lambda x: x * (outer - x),
    }
    rows: list[dict[str, Any]] = []
    worst = 0.0
    for name, maker in makers.items():
        h = maker(r)
        h[-1] = 0.0
        ratio = wall_trace_ratio(h, r, eps=eps)
        rows.append(
            {
                "profile": name,
                "lhs_over_rhs": ratio,
                "holds": ratio <= 1.05,
                "h_at_wall": float(h[0]),
                "h_at_outer": float(h[-1]),
            }
        )
        worst = max(worst, ratio)
    return {
        "delta": delta,
        "outer": outer,
        "n": n,
        "eps": eps,
        "worst_lhs_over_rhs": worst,
        "holds": worst <= 1.05,
        "profiles": rows,
        "identity": "h(R)=0 ⇒ h(δ)² ≤ ε∫ r(h')² + ε^{-1}∫ h²/r",
        "verdict": "pass" if worst <= 1.05 else "fail",
        "notes": (
            "Numeric check of T3a. Extra environment: an outer radius where "
            "h vanishes. Periodic T^3 does not supply that (CLIP-T3-OUTER)."
        ),
        "torus_obstruction": (
            "On T^3 the off-axis is not a half-line. There is no R with "
            "Γ(R)=0 forced by the domain. T3a is a cylinder identity, not "
            "a torus identity."
        ),
    }


def monomial_mismatch_probe(
    delta: float = 0.3,
    outer: float = 1.2,
    nr: int = 120,
    nz: int = 64,
) -> dict[str, Any]:
    """Show T3b: wall/Hardy weights are not the swirl source I_off."""
    r = np.linspace(delta, outer, nr)
    z = np.linspace(0.0, 2.0 * np.pi, nz, endpoint=False)
    R, Z = np.meshgrid(r, z, indexing="ij")
    # Smooth off-axis swirl; Γ = r u_θ with u_θ decaying in r.
    uth = (R**2) * np.exp(-((R / 0.5) ** 2)) * np.sin(Z)
    gamma = R * uth
    h = gamma / np.maximum(R, delta)
    dr = r[1] - r[0]
    dz = z[1] - z[0]
    weight = R  # r dr dz, θ absorbed
    hardy = float(np.sum((h**2) / np.maximum(R, dr) * weight) * dr * dz)
    dgz = np.gradient(gamma, dz, axis=1)
    # I_off density ~ r^{-4} ∂_z(Γ²) ω^r, ω^r unknown; use |∂_z(Γ²)| as proxy.
    i_off_proxy = float(np.sum(np.abs(2.0 * gamma * dgz) / (R**4) * weight) * dr * dz)
    wall = float(np.sum((h[0, :] ** 2) * dz) * 2.0)
    return {
        "verdict": "open",
        "clip_id": "CLIP-T3-WELD",
        "hardy_off_axis": hardy,
        "i_off_proxy_abs": i_off_proxy,
        "wall_2h2": wall,
        "same_r_weight": "both Hardy and I_off scale as 1/r³ after r dr",
        "different_fields": "Hardy sees Γ²; I_off sees (Γ ∂_z Γ) ω^r",
        "notes": (
            "Ratios are diagnostic on one manufactured field. They do not "
            "weld the wall to I_off. T3b stays open."
        ),
    }


def swirl_source_vs_angular_probe(nr: int = 96, nz: int = 64) -> dict[str, Any]:
    """B5/T6 diagnostic: |I_source| / angular mass on one field. Not a close."""
    r0, r1 = 1e-3, 1.5
    r = np.linspace(r0, r1, nr)
    z = np.linspace(0.0, 2.0 * np.pi, nz, endpoint=False)
    R, Z = np.meshgrid(r, z, indexing="ij")
    uth = (R**2) * np.exp(-((R / 0.4) ** 2)) * np.sin(Z)
    gamma = R * uth
    dr = r[1] - r[0]
    dz = z[1] - z[0]
    weight = R
    ang = float(np.sum((uth / R) ** 2 * weight) * dr * dz)
    source = 2.0 * gamma * np.gradient(gamma, dz, axis=1) / (R**4)
    i_abs = float(np.sum(np.abs(source) * weight) * dr * dz)
    ratio = i_abs / max(ang, 1e-30)
    return {
        "verdict": "open",
        "clip_id": "CLIP-B5b-VS-VISC",
        "angular_mass": ang,
        "abs_source_mass": i_abs,
        "source_over_angular": ratio,
        "notes": (
            "Identity (Δu)_θ = Δu_θ − u_θ/r² is already B5. This ratio on "
            "one manufactured field is not domination at δ ∼ 2^{-j*}."
        ),
    }


def scaling_ledger() -> dict[str, Any]:
    """Architecture scalings at δ ∼ 2^{-j*}. Two charts, neither is a proof."""
    return {
        "delta": "δ ∼ 2^{-j*} under CONC",
        "l2_chart": (
            "Packet L²: ‖Δ_j u‖_2 ∼ 2^{-j} √X_j so |u| ∼ δ √X. "
            "Then h(δ) ∼ u_θ ∼ δ √X and wall ∼ δ² X, which looks small."
        ),
        "linfty_chart": (
            "3D Bernstein: ‖Δ_j u‖_∞ ≲ 2^{j/2} √X_j. "
            "Then wall ∼ 2^{j} X = X/δ, which looks large."
        ),
        "why_open": (
            "L² and L∞ charts disagree on the wall. That disagreement is "
            "CLIP-T3-WELD / CLIP-B4b-ITUBE, not a close. Do not pick the "
            "optimistic chart."
        ),
        "status": "architecture, UNMEASURED as an estimate",
    }


def tube_estimate() -> dict[str, Any]:
    from .gap import gap_tube

    hardy = hardy_wall_probe()
    trace = wall_trace_probe()
    mismatch = monomial_mismatch_probe()
    swirl = swirl_source_vs_angular_probe()
    steps = [s.to_dict() for s in TUBE_STEPS]
    return {
        "book": "B",
        "title": "Tube estimate — live geometric write",
        "not_a_regularity_proof": True,
        "keep": "1/r^4 and Γ = r u_θ. Do not pass to Φ_θ as the unknown.",
        "split": "I = I_off(δ) + I_tube(δ)",
        "delta": "δ ∼ 2^{-j*} under CONC; spread uses Bony, not this tube",
        "wall_diagram": WALL_DIAGRAM,
        "monomials": [dict(m) for m in MONOMIALS],
        "steps": steps,
        "gap": gap_tube(steps),
        "hardy_probe": hardy,
        "wall_trace_probe": trace,
        "monomial_mismatch": mismatch,
        "swirl_vs_angular": swirl,
        "scaling": scaling_ledger(),
        "closed": [
            "T1 off-axis weight bound (geometric, r≥δ)",
            "T2 Hardy+wall identity from inside (B4, numeric probe holds)",
            "T3a Young trace from outside when h(R)=0 (numeric probe holds)",
        ],
        "open": [
            "T3b wall/trace welded to I_off (different fields; T^3 has no outer vanishing)",
            "T5 I_tube absorbed by viscosity",
            "T6 angular 1/r² wins in the same tube",
            "T7 integrable R(t) for Gronwall on X",
        ],
        "target": (
            "dX/dt + ν||∇ω||_2^2 ≤ ε ν||∇ω||_2^2 + C_ε X R(t) "
            "with R integrable from tube Hardy and/or Ring and/or spread Poincaré"
        ),
        "next": (
            "STOP at T3b. Fill GAP-T3 (CLIP-T3-WELD, CLIP-T3-OUTER). "
            "T5 is the first candidate after, not a step. Leave T7 open. "
            "Do not pass regularity. Do not glue Cartesian Bony T onto this tube."
        ),
    }


def format_tube_estimate(report: dict[str, Any] | None = None) -> str:
    data = report or tube_estimate()
    lines = [
        data["title"],
        "Not a regularity proof. " + data["keep"],
        "",
        "Split: " + data["split"],
        "Scale: " + data["delta"],
        "Wall as a two-sided cylinder" + data["wall_diagram"],
        "Monomials (do not silent-merge)",
    ]
    for mon in data["monomials"]:
        lines.append(f"  {mon['id']}: {mon['expression']}")
        lines.append(f"      {mon['lives']}")
        lines.append(f"      {mon['status']}")
    lines.append("")
    from .gap import format_gap

    lines.append(format_gap(data.get("gap")))
    lines.append("")
    lines.append("Walked inequalities (detail; stop at the wall)")
    wall_name = (data.get("gap") or {}).get("wall", {}).get("step")
    hit_wall = False
    for step in data["steps"]:
        if hit_wall:
            break
        if step["step"] == wall_name:
            hit_wall = True
        lines.append(f"── {step['step']}  [{step['status']}]")
        lines.append(f"   {step['inequality']}")
        lines.append(f"   geometry: {step['geometry']}")
        lines.append(f"   remainder {step['clip_id']}: {step['remainder']}")
        lines.append("")
    hardy = data["hardy_probe"]
    lines.append(
        f"Hardy+wall (inside) probe: {hardy['verdict']}  "
        f"worst LHS/RHS = {hardy['worst_lhs_over_rhs']:.4f}"
    )
    for row in hardy["profiles"]:
        flag = "ok" if row["holds"] else "FAIL"
        lines.append(f"  {row['profile']}: {row['lhs_over_rhs']:.4f} [{flag}]")
    trace = data["wall_trace_probe"]
    lines.append(
        f"Young trace (outside) probe: {trace['verdict']}  "
        f"worst LHS/RHS = {trace['worst_lhs_over_rhs']:.4f}"
    )
    for row in trace["profiles"]:
        flag = "ok" if row["holds"] else "FAIL"
        lines.append(f"  {row['profile']}: {row['lhs_over_rhs']:.4f} [{flag}]")
    lines.append("  " + trace["torus_obstruction"])
    weld = data["monomial_mismatch"]
    lines.append(
        f"T3b monomial probe [{weld['verdict']}] wall={weld['wall_2h2']:.4g}  "
        f"Hardy_off={weld['hardy_off_axis']:.4g}  "
        f"I_off_proxy={weld['i_off_proxy_abs']:.4g}"
    )
    lines.append("  " + weld["different_fields"])
    swirl = data["swirl_vs_angular"]
    lines.append(
        f"T6 diagnostic [{swirl['verdict']}] |I_source|/angular = "
        f"{swirl['source_over_angular']:.4g} (not a close)"
    )
    scale = data["scaling"]
    lines.append("Scaling ledger: " + scale["why_open"])
    lines.append("")
    lines.append("Closed: " + "; ".join(data["closed"]))
    lines.append("Open: " + "; ".join(data["open"]))
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
