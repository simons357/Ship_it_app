"""Look across Pólya objects and the open Millennium prizes.

Exploration, not glue. Shared tools and kernel families are recorded so they
can be inspected. They are not a unification and not a Clay solution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


LOOK_SCOPE: str = (
    "Millennium look. Parts of Pólya were compared with Navier–Stokes and the "
    "other open Clay prizes. A match of tool or kernel family is not a proof. "
    "A notation collision is not a match."
)


@dataclass
class OverlapLook:
    look_id: str
    prize: str
    polya_part: str
    other_object: str
    match_level: str
    what_matched: str
    what_did_not: str
    status: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def overlap_looks() -> list[OverlapLook]:
    """Every look the probe is willing to record. DA does not merge prizes."""
    return [
        OverlapLook(
            "LOOK-NS-GREEN",
            "Navier–Stokes existence and smoothness",
            "Pólya 1921: simple random walk is transient in d≥3; discrete Green ~ 1/|x|^{d-2}",
            "3D Biot–Savart: u = ∇×(−Δ)^{-1}ω, Newtonian kernel 1/|x|",
            "shared-kernel-family",
            "d=3 is the dimension where Pólya transience and the Newtonian potential used by NS both live",
            "Transience is not regularity. Biot–Savart is already standard NS, not a Pólya derivation of Clay NS",
            "LOOKED; closest structural rhyme; not a bridge",
        ),
        OverlapLook(
            "LOOK-NS-REARRANGE",
            "Navier–Stokes existence and smoothness",
            "Pólya–Szegő rearrangement: Dirichlet integral does not increase under Schwarz symmetrization",
            "Sobolev / Ladyzhenskaya estimates used in NS energy methods",
            "shared-tool",
            "Same isoperimetric / rearrangement family that feeds Sobolev constants in PDE estimates",
            "An estimate tool is not 3D global smoothness",
            "LOOKED; tool overlap; not a solution",
        ),
        OverlapLook(
            "LOOK-NS-STOKES-OP",
            "Navier–Stokes existence and smoothness",
            "Pólya 1954 membrane eigenvalues (scalar Laplacian Weyl law on a domain)",
            "Stokes operator A = −ℙΔ on divergence-free fields",
            "spectral-sibling",
            "Self-adjoint Laplacian-type operators on domains, both with Weyl-type counts",
            "Scalar membrane ≠ vector Stokes. Neither is Hilbert–Pólya H. Neither solves Clay NS",
            "LOOKED; sibling spectra; not identity",
        ),
        OverlapLook(
            "LOOK-NS-HEAT",
            "Navier–Stokes existence and smoothness",
            "de Bruijn–Newman heat flow on Ξ (continuation of Pólya 1926)",
            "viscous term νΔu in Navier–Stokes",
            "shared-pde-name",
            "Both deform by a heat/diffusion operator",
            "Ξ_t is a deformation of an entire function. NS is a vector PDE. Heat is not a unifier",
            "LOOKED; name-rhyme; not a transformation",
        ),
        OverlapLook(
            "LOOK-NS-PHI-LETTER",
            "Navier–Stokes (this repo, NS-Φ swirl algebra)",
            "Riemann kernel Φ in Ξ(z) = ∫ Φ(t) cos(zt) dt",
            "swirl Φ = u_θ/r and r^{-4}∂_z(Γ²) = ∂_z(Φ²)",
            "notation-collision",
            "The same letter Φ",
            "Riemann’s Fourier kernel is not swirl angular rate. Do not merge",
            "LOOKED; collision only; keep both books",
        ),
        OverlapLook(
            "LOOK-YM-LAPLACE",
            "Yang–Mills mass gap",
            "Pólya membrane / Laplacian eigenvalues",
            "spectrum of a gauge Hamiltonian / Hodge Laplacian on connections",
            "shared-word-spectrum",
            "The word spectrum and a Laplacian-type operator",
            "No checked map from a vibrating membrane to a mass gap",
            "LOOKED; vocabulary only",
        ),
        OverlapLook(
            "LOOK-BSD-L",
            "Birch and Swinnerton-Dyer",
            "Riemann ξ, Weil explicit formula, Pólya 1926 cosine representation",
            "L-functions of elliptic curves; rank vs order of vanishing",
            "same-analytic-family",
            "Completed L-functions and explicit formulae live in one analytic book",
            "Pólya 1926 is about Riemann ξ, not L(E,s). Different L-function, different prize",
            "LOOKED; family resemblance; not BSD",
        ),
        OverlapLook(
            "LOOK-HODGE",
            "Hodge conjecture",
            "none of the ingested Pólya theorems",
            "algebraic cycles vs Hodge classes",
            "none",
            "nothing checked",
            "No Pólya object in this briefing is a Hodge-class statement",
            "LOOKED; empty",
        ),
        OverlapLook(
            "LOOK-PNP",
            "P versus NP",
            "Pólya 1937 enumeration (cycle index / orbit counting)",
            "Turing-machine complexity classes",
            "none",
            "both involve counting, at a slogan level",
            "Orbit counting of group actions is not P vs NP",
            "LOOKED; slogan only",
        ),
        OverlapLook(
            "LOOK-RH",
            "Riemann hypothesis",
            "Hilbert–Pólya; Laguerre–Pólya; Pólya 1926; de Bruijn–Newman Λ",
            "nontrivial zeros of ζ on Re s = 1/2",
            "direct-open-strategy",
            "This is the prize Pólya’s surviving theorems actually address",
            "Those theorems do not prove RH. Λ = 0 is still RH. H is still missing",
            "LOOKED; this is the live prize for the surviving Pólya objects",
        ),
    ]


def closest_rhymes() -> list[str]:
    """What survived the look as a rhyme, not as a Clay solution."""
    return [
        "Closest NS rhyme: Pólya 1921 transience in d≥3 and the 3D Newtonian / "
        "Biot–Savart kernel. Same dimension, same Green-function family. Not regularity.",
        "NS tool overlap: Pólya–Szegő rearrangement sits in the isoperimetric book "
        "that feeds Sobolev / Ladyzhenskaya estimates. A tool, not Clay NS.",
        "Spectral sibling: membrane Laplacian (Pólya 1954) versus Stokes operator "
        "A = −ℙΔ. Sibling Weyl laws. Not Hilbert–Pólya H.",
        "Notation collision: Riemann kernel Φ versus swirl Φ = u_θ/r in this repo. "
        "Keep both; do not merge.",
        "No Pólya object in this briefing unifies the Clay prizes. The live prize "
        "for the theorems that survived the RH-attack filter is still RH.",
    ]


def millennium_look_narrative() -> str:
    looks = overlap_looks()
    lines = [
        "Domain Architect — Millennium look",
        "",
        LOOK_SCOPE,
        "",
        "What rhymed when we looked (not a unification):",
    ]
    for line in closest_rhymes():
        lines.append(f"  * {line}")
    lines.append("")
    lines.append("Looks (parts of Pólya vs each prize):")
    for look in looks:
        lines.append(f"  [{look.look_id}] {look.prize}")
        lines.append(f"    Pólya part: {look.polya_part}")
        lines.append(f"    other object: {look.other_object}")
        lines.append(f"    match level: {look.match_level}")
        lines.append(f"    matched: {look.what_matched}")
        lines.append(f"    did not: {look.what_did_not}")
        lines.append(f"    status: {look.status}")
    return "\n".join(lines)


PAIRS: dict[str, dict[str, str]] = {
    "green-biot": {
        "left_id": "HP-H027",
        "right_id": "NS-H004",
        "left_parse": "laplacian(G) = -delta",
        "right_parse": "u = curl(invLap * omega)",
        "finding": (
            "The Laplacian classifier put G in the realized-output seat of "
            "ΔG = −δ and recorded R(κ)=1/κ² in E. Biot–Savart is curl of that "
            "inverse Laplacian applied to ω. Shared scale response, different "
            "outputs (Green kernel vs velocity). COMPATIBLE_DISTINCT. Not Clay NS."
        ),
    },
    "phi": {
        "left_id": "HP-H012",
        "right_id": "NS-H002",
        "left_parse": "Xi = I(Phi)",
        "right_parse": "partial_z(Gamma^2)/r^4 = partial_z(Phi^2)",
        "finding": (
            "Both parses contain a symbol Phi. The auditor warns that Φ is an "
            "identifier, not automatically a gravitational potential. Registry "
            "relation is INCOMPATIBLE: Riemann’s cosine-transform kernel is not "
            "swirl u_θ/r. Keep both books."
        ),
    },
}


def list_pair_ids() -> list[str]:
    return list(PAIRS)


def run_equation_pair(pair_id: str = "green-biot") -> str:
    """Audit both registered equations of a look pair. Does not merge them."""
    from .audit import audit_expression
    from .registry import EquationRegistry
    from .schema import CANONICAL_SFE_STATUS, RH_STATUS

    if pair_id not in PAIRS:
        known = ", ".join(list_pair_ids())
        raise KeyError(f"unknown pair {pair_id!r}; known={known}")
    spec = PAIRS[pair_id]
    registry = EquationRegistry.load_default()
    left = registry.equations[spec["left_id"]]
    right = registry.equations[spec["right_id"]]
    left_report = audit_expression(spec["left_parse"])
    right_report = audit_expression(spec["right_parse"])
    relation = "unrecorded"
    evidence = ""
    for conflict in registry.conflicts:
        if {conflict.left_id, conflict.right_id} == {left.equation_id, right.equation_id}:
            relation = conflict.relation
            evidence = conflict.evidence
            break

    def _roles(report) -> list[str]:
        rows = []
        for item in report.role_assignments:
            rows.append(
                f"{item.get('symbol')}: role={item.get('candidate_role')} "
                f"subtype={item.get('subtype')}"
            )
        return rows

    lines = [
        f"Domain Architect — pair run ({pair_id})",
        "",
        "Both equations were run through the auditor. They were not merged.",
        f"Riemann hypothesis status: {RH_STATUS}.",
        f"Canonical SFE status: {CANONICAL_SFE_STATUS}.",
        "",
        f"[{left.equation_id}] {left.original_expression}",
        f"  book/family: {left.family}  disposition: {left.audit_disposition}",
        f"  parse used: {spec['left_parse']}",
        f"  evidence: Level {int(left_report.highest_evidence_level)}",
        f"  extra E: {left_report.extra_structures or 'none'}",
    ]
    for row in _roles(left_report):
        lines.append(f"  {row}")
    lines.extend(
        [
            "",
            f"[{right.equation_id}] {right.original_expression}",
            f"  book/family: {right.family}  disposition: {right.audit_disposition}",
            f"  parse used: {spec['right_parse']}",
            f"  evidence: Level {int(right_report.highest_evidence_level)}",
            f"  extra E: {right_report.extra_structures or 'none'}",
        ]
    )
    for row in _roles(right_report):
        lines.append(f"  {row}")
    lines.extend(
        [
            "",
            f"Recorded relation: {relation}",
            f"  {evidence}" if evidence else "  (no conflict row)",
            "",
            "What DA did with the pair:",
            f"  {spec['finding']}",
        ]
    )
    return "\n".join(lines)


def run_default_pairs() -> str:
    """Run the two look-pairs that were on the table: Green/Biot–Savart and the Φs."""
    blocks = [run_equation_pair("green-biot"), "", run_equation_pair("phi")]
    return "\n".join(blocks)
