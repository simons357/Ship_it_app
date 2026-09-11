"""Recursive module decomposition (drill-down) and recompose checks.

Style: H → (H1, H2, …) as first-class structures for NS-B and/or gravity.
Each module records children until a stop rule fires:

  Stop when remaining objects are defined / measurable / standard operators.

Closure/recompose: children inventories must cover the parent's declared
parts. This is structural bookkeeping — not a PDE solve, not Clay, not ToE.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .hb_loop import infer_book
from .report import AuditReport
from .schema import CANONICAL_SFE_STATUS


@dataclass
class ModuleNode:
    """One node in a recursive FRA module tree."""

    module_id: str
    label: str
    role: str
    kind: str  # composite | terminal
    stop_reason: str = ""
    definition: str = ""
    children: list["ModuleNode"] = field(default_factory=list)
    recompose_ok: bool | None = None
    recompose_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "module_id": self.module_id,
            "label": self.label,
            "role": self.role,
            "kind": self.kind,
            "stop_reason": self.stop_reason,
            "definition": self.definition,
            "children": [c.to_dict() for c in self.children],
            "recompose_ok": self.recompose_ok,
            "recompose_note": self.recompose_note,
        }


@dataclass
class DecompositionReport:
    domain_book: str
    root: ModuleNode
    depth: int
    terminal_count: int
    all_recompose_ok: bool
    statement: str
    canonical_sfe_status: str = CANONICAL_SFE_STATUS

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain_book": self.domain_book,
            "root": self.root.to_dict(),
            "depth": self.depth,
            "terminal_count": self.terminal_count,
            "all_recompose_ok": self.all_recompose_ok,
            "statement": self.statement,
            "canonical_sfe_status": self.canonical_sfe_status,
        }

    def narrative(self) -> str:
        lines = [
            "Drill-down + recompose",
            f"  book: {self.domain_book}",
            f"  depth: {self.depth}",
            f"  terminals: {self.terminal_count}",
            f"  all modules recompose: {self.all_recompose_ok}",
            f"  {self.statement}",
            f"  Canonical SFE status: {self.canonical_sfe_status}.",
            "",
            "Module tree:",
        ]
        lines.extend(_format_tree(self.root, indent=0))
        return "\n".join(lines)


def _format_tree(node: ModuleNode, indent: int) -> list[str]:
    pad = "  " * indent
    flag = ""
    if node.kind == "composite" and node.recompose_ok is not None:
        flag = " ✓" if node.recompose_ok else " ✗"
    stop = f" [{node.stop_reason}]" if node.stop_reason else ""
    lines = [f"{pad}- {node.module_id}: {node.label} ({node.kind}){flag}{stop}"]
    if node.definition:
        lines.append(f"{pad}    def: {node.definition}")
    if node.recompose_note:
        lines.append(f"{pad}    recompose: {node.recompose_note}")
    for child in node.children:
        lines.extend(_format_tree(child, indent + 1))
    return lines


def _terminal(
    module_id: str,
    label: str,
    role: str,
    *,
    stop_reason: str,
    definition: str,
) -> ModuleNode:
    return ModuleNode(
        module_id=module_id,
        label=label,
        role=role,
        kind="terminal",
        stop_reason=stop_reason,
        definition=definition,
        recompose_ok=True,
        recompose_note="Terminal leaf — stop rule satisfied.",
    )


def _compose(
    module_id: str,
    label: str,
    role: str,
    children: list[ModuleNode],
    *,
    definition: str,
    expected_child_ids: list[str],
) -> ModuleNode:
    have = {c.module_id for c in children}
    missing = [eid for eid in expected_child_ids if eid not in have]
    ok = not missing and all(
        c.recompose_ok is not False for c in children
    )
    note = (
        "Children cover parent inventory; organizational recompose OK."
        if ok
        else f"Recompose gap — missing child modules: {', '.join(missing)}"
    )
    return ModuleNode(
        module_id=module_id,
        label=label,
        role=role,
        kind="composite",
        definition=definition,
        children=children,
        recompose_ok=ok,
        recompose_note=note,
    )


def _ns_b_tree() -> ModuleNode:
    """Classical NS-B five-finger drill-down with stop rules."""
    # P → Helmholtz / Leray pieces → standard ops
    p_helmholtz = _terminal(
        "P1",
        "Helmholtz decomposition",
        "admissibility",
        stop_reason="standard_operator",
        definition="u = ∇×A − ∇φ style split; curl/grad are standard",
    )
    p_leray = _terminal(
        "P2",
        "Leray / divergence-free projector",
        "admissibility",
        stop_reason="defined_operator",
        definition="P = I − ∇(Δ^{-1})∇· on suitable spaces (classical)",
    )
    p_div = _terminal(
        "P3",
        "Incompressibility constraint ∇·u = 0",
        "admissibility",
        stop_reason="measurable_constraint",
        definition="divergence-free condition on velocity",
    )
    p = _compose(
        "P",
        "Admissibility / Leray",
        "admissibility",
        [p_helmholtz, p_leray, p_div],
        definition="Select divergence-free admissible states",
        expected_child_ids=["P1", "P2", "P3"],
    )

    h_adv = _terminal(
        "H1",
        "Advection / transport (u·∇)u or (ω·∇)u piece",
        "interaction",
        stop_reason="standard_operator",
        definition="(u·∇) acting on fields — standard differential operator",
    )
    h_stretch = _terminal(
        "H2",
        "Vortex stretching / nonlinear self-interaction",
        "interaction",
        stop_reason="defined_operator",
        definition="Stretching term in vorticity form; classical NS nonlinearity",
    )
    h = _compose(
        "H",
        "Interaction / coupling",
        "interaction",
        [h_adv, h_stretch],
        definition="Nonlinear advection / stretch H(ψ)",
        expected_child_ids=["H1", "H2"],
    )

    psi_u = _terminal(
        "psi1",
        "Velocity field u",
        "state",
        stop_reason="measurable_field",
        definition="Velocity is the primary NS state in velocity form",
    )
    psi_w = _terminal(
        "psi2",
        "Vorticity ω = ∇×u",
        "state",
        stop_reason="defined_from_measurable",
        definition="Vorticity derived from velocity via curl",
    )
    psi = _compose(
        "psi",
        "State / coherence",
        "state",
        [psi_u, psi_w],
        definition="ψ ≈ u | ω",
        expected_child_ids=["psi1", "psi2"],
    )

    lam_nu = _terminal(
        "lambda1",
        "Kinematic viscosity ν",
        "scale_response",
        stop_reason="measurable_scalar",
        definition="Material viscosity — laboratory / protocol parameter",
    )
    lam_lap = _terminal(
        "lambda2",
        "Laplacian dissipation Δ",
        "scale_response",
        stop_reason="standard_operator",
        definition="Standard Laplacian on the domain",
    )
    lam = _compose(
        "lambda",
        "Scale response / dissipation",
        "scale_response",
        [lam_nu, lam_lap],
        definition="λ ≈ ν with dissipative operator Δ",
        expected_child_ids=["lambda1", "lambda2"],
    )

    phi_p = _terminal(
        "Phi1",
        "Pressure (or Lagrange multiplier for div-free)",
        "realized_output",
        stop_reason="defined_field",
        definition="Pressure enforces incompressibility / observed force balance",
    )
    phi_obs = _terminal(
        "Phi2",
        "Observed response (strain, enstrophy production, …)",
        "realized_output",
        stop_reason="measurable_output",
        definition="Diagnostics derived from (u,ω,p)",
    )
    phi = _compose(
        "Phi",
        "Realized output",
        "realized_output",
        [phi_p, phi_obs],
        definition="Φ ≈ p / observed response",
        expected_child_ids=["Phi1", "Phi2"],
    )

    e_dom = _terminal(
        "E1",
        "Domain R³ (or bounded Ω)",
        "environment",
        stop_reason="defined_geometry",
        definition="Spatial domain for the PDE",
    )
    e_icbc = _terminal(
        "E2",
        "Initial and boundary conditions",
        "environment",
        stop_reason="protocol_data",
        definition="IC/BC required for well-posed classical formulation",
    )
    e_bs = _terminal(
        "E3",
        "Biot–Savart reconstruction u from ω",
        "environment",
        stop_reason="standard_operator",
        definition="u = K * ω (Biot–Savart kernel) — classical",
    )
    e = _compose(
        "E",
        "Environment / extras",
        "environment",
        [e_dom, e_icbc, e_bs],
        definition="E ⊃ domain, IC/BC, Biot–Savart",
        expected_child_ids=["E1", "E2", "E3"],
    )

    return _compose(
        "NS-B",
        "Classical Navier–Stokes book (five-finger root)",
        "root",
        [p, h, psi, lam, phi, e],
        definition=(
            "Organizational Φ≈ℱ(P,H,ψ,λ;E) for classical NS — not Clay, "
            "not SFE derivation"
        ),
        expected_child_ids=["P", "H", "psi", "lambda", "Phi", "E"],
    )


def _gravity_tree() -> ModuleNode:
    """Newtonian Poisson gravity drill-down."""
    phi = _terminal(
        "Phi",
        "Newtonian potential Φ",
        "realized_output",
        stop_reason="defined_field",
        definition="Gravitational potential in Poisson form",
    )
    src = _terminal(
        "S",
        "Mass density ρ",
        "source",
        stop_reason="measurable_field",
        definition="Source density — measurable / prescribed",
    )
    r_kappa = _terminal(
        "R1",
        "Spectral coordinate κ (wavevector)",
        "scale_response",
        stop_reason="standard_coordinate",
        definition="Fourier wavevector; coordinate-like, not the response",
    )
    r_resp = _terminal(
        "R2",
        "Transfer R(κ)=1/κ² (κ≠0)",
        "scale_response",
        stop_reason="standard_operator",
        definition="Green/Fourier multiplier for Laplacian inverse",
    )
    scale = _compose(
        "R",
        "Scale response",
        "scale_response",
        [r_kappa, r_resp],
        definition="Keep κ vs R(κ) distinct",
        expected_child_ids=["R1", "R2"],
    )
    g_geom = _terminal(
        "g1",
        "Flat Euclidean geometry / torus for periodic lab",
        "environment",
        stop_reason="defined_geometry",
        definition="Domain geometry for Poisson solve",
    )
    g_bc = _terminal(
        "g2",
        "Boundary / mean-zero solvability",
        "environment",
        stop_reason="defined_constraint",
        definition="Zero-mode / BC policy for ∇²",
    )
    env = _compose(
        "E",
        "Geometry + boundary",
        "environment",
        [g_geom, g_bc],
        definition="E ⊃ geometry, boundary",
        expected_child_ids=["g1", "g2"],
    )
    return _compose(
        "gravity-poisson",
        "Newtonian Poisson book",
        "root",
        [phi, src, scale, env],
        definition="∇²Φ = 4πGρ as representation target — not SFE-derived",
        expected_child_ids=["Phi", "S", "R", "E"],
    )


def _generic_tree(expression: str) -> ModuleNode:
    return ModuleNode(
        module_id="generic",
        label="Unresolved / no frozen book",
        role="root",
        kind="terminal",
        stop_reason="no_book",
        definition=f"Input {expression!r} has no drill-down book",
        recompose_ok=False,
        recompose_note="Withhold decomposition rather than invent modules.",
    )


def _depth(node: ModuleNode) -> int:
    if not node.children:
        return 1
    return 1 + max(_depth(c) for c in node.children)


def _count_terminals(node: ModuleNode) -> int:
    if node.kind == "terminal":
        return 1
    return sum(_count_terminals(c) for c in node.children)


def _all_recompose(node: ModuleNode) -> bool:
    if node.recompose_ok is False:
        return False
    return all(_all_recompose(c) for c in node.children)


def decompose_report(report: AuditReport) -> DecompositionReport:
    """Build recursive module tree for the inferred domain book."""
    book = infer_book(report)
    if book == "NS-B":
        root = _ns_b_tree()
    elif book == "gravity-poisson":
        root = _gravity_tree()
    else:
        root = _generic_tree(report.input_expression)

    ok = _all_recompose(root) if book != "generic" else False
    statement = (
        f"Drill-down for {book}: stop when objects are defined, measurable, "
        "or standard operators. Recompose checks are inventory closure only "
        "— not a PDE solve, Clay claim, or canonical SFE."
        if book != "generic"
        else "No domain book; recursive decomposition withheld."
    )
    return DecompositionReport(
        domain_book=book,
        root=root,
        depth=_depth(root),
        terminal_count=_count_terminals(root),
        all_recompose_ok=ok,
        statement=statement,
    )


def attach_decomposition(report: AuditReport) -> AuditReport:
    dec = decompose_report(report)
    report.decomposition = dec.to_dict()
    report.notes = list(
        dict.fromkeys(
            list(report.notes)
            + [
                dec.statement,
                f"Drill-down depth={dec.depth}, terminals={dec.terminal_count}, "
                f"recompose_ok={dec.all_recompose_ok}.",
            ]
        )
    )
    return report
