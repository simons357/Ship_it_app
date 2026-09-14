"""Pólya probe: feed every independently specifiable object into Domain Architect.

The core grammar is Φ = ℱ(P, H, ψ, λ; E). The number of recorded components
is not capped at five. Domain Architect expands E whenever hiding a structure
would lose information. This probe does that for Hilbert–Pólya plus proven
Pólya entire-function facts.

It does not construct H, prove RH, merge incompatible candidates, or derive
Navier–Stokes (or any other Millennium problem) from Pólya.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .audit import audit_expression
from .hilbert_polya import (
    GUE_NOT_IDENTITY_WARNING,
    PROGRAM_SCOPE,
    RH_STATUS,
    audit_candidate,
    extra_structures,
    gue_is_not_riemann_spectrum,
    historical_candidates,
    program_pieces,
    weyl_law_screen,
)
from .protocol import freeze_protocol
from .registry import EquationRegistry
from .schema import (
    CANONICAL_SFE_STATUS,
    EvidenceLevel,
    HILBERT_POLYA_STATUS,
)


PROBE_SCOPE: str = (
    "Pólya probe. Domain Architect chooses how many independently specifiable "
    "components to record. Core roles are an interface, not a cap. This is "
    "an exploratory classification of supplied Pólya / zeta objects, not a "
    "proof of the Riemann hypothesis and not a unification of Millennium problems."
)


@dataclass
class ComponentRecord:
    """One independently specifiable object in the probe."""

    component_id: str
    role: str
    occupant: str
    kind: str
    independently_specified: bool
    da_action: str
    verdict: str
    source: str = ""


@dataclass
class PolyaProbeReport:
    instance_name: str
    component_count: int
    core_role_count: int
    extension_count: int
    components: list[ComponentRecord]
    da_requests: list[str]
    findings: list[str]
    millennium_routing: list[dict[str, str]]
    candidate_scores: list[dict[str, Any]]
    expression_audits: list[dict[str, Any]]
    gue_laboratory: dict[str, Any]
    weyl_laboratory: dict[str, Any]
    registry_hp_ids: list[str]
    conflicts: list[str]
    nulls: list[str]
    highest_evidence_level: int
    hilbert_polya_status: str
    rh_status: str
    canonical_sfe_status: str
    complete: bool
    protocol_hash: str
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["components"] = [asdict(c) for c in self.components]
        return payload

    def narrative(self) -> str:
        lines = [
            "Domain Architect — Pólya probe",
            "",
            PROBE_SCOPE,
            "",
            PROGRAM_SCOPE,
            "",
            f"Instance: {self.instance_name}",
            f"Independently specifiable components recorded: {self.component_count} "
            f"({self.core_role_count} core roles + {self.extension_count} extension / E)",
            f"Hilbert–Pólya status: {self.hilbert_polya_status}.",
            f"Riemann hypothesis status: {self.rh_status}.",
            f"Canonical SFE status: {self.canonical_sfe_status}.",
            f"Program complete: {self.complete}",
            f"Highest evidence level actually supported: Level {self.highest_evidence_level}",
            "",
            "What Domain Architect did with the supplied objects:",
        ]
        for item in self.components:
            spec = "specified" if item.independently_specified else "not independently specified"
            lines.append(
                f"  [{item.component_id}] role={item.role} kind={item.kind} ({spec})"
            )
            lines.append(f"    occupant: {item.occupant}")
            lines.append(f"    DA action: {item.da_action}")
            lines.append(f"    verdict: {item.verdict}")
        lines.append("")
        lines.append("Findings (classification, not discovery of a Hamiltonian):")
        for finding in self.findings:
            lines.append(f"  - {finding}")
        lines.append("")
        lines.append("Domain Architect still needs (cannot invent these):")
        for req in self.da_requests:
            lines.append(f"  - {req}")
        lines.append("")
        lines.append("Millennium-problem routing (no silent glue):")
        for row in self.millennium_routing:
            lines.append(
                f"  {row['prize']}: {row['relation']} — {row['polya_object']} "
                f"[{row['status']}]"
            )
        lines.append("")
        lines.append("Candidate scores (unmerged):")
        for row in self.candidate_scores:
            lines.append(
                f"  {row['candidate_id']}: independent_H={row['independent_h']} "
                f"circular={row['circular']} complete={row['complete']} "
                f"missing={', '.join(row['missing'][:6])}"
                + ("…" if len(row["missing"]) > 6 else "")
            )
        if self.gue_laboratory:
            lines.append("")
            lines.append("GUE laboratory:")
            lines.append(
                f"  affine residual to first γ_n: "
                f"{self.gue_laboratory.get('affine_residual_to_first_gammas')}"
            )
            lines.append(
                f"  is Riemann spectrum: {self.gue_laboratory.get('is_riemann_spectrum')}"
            )
            lines.append(f"  {self.gue_laboratory.get('conclusion')}")
        if self.weyl_laboratory:
            lines.append("")
            lines.append("Weyl-law screen (usable filter on H, not a construction):")
            lines.append(
                f"  oscillator rejected: {self.weyl_laboratory.get('oscillator_rejected')}"
            )
            lines.append(
                f"  xp classical leading term compatible: "
                f"{self.weyl_laboratory.get('xp_classical_leading_term_compatible')}"
            )
            lines.append(
                f"  Riemann spacing ratio high/low T: "
                f"{self.weyl_laboratory.get('spacing_ratio_high_over_low_riemann')}"
            )
            lines.append(f"  {self.weyl_laboratory.get('conclusion')}")
        if self.expression_audits:
            lines.append("")
            lines.append("Expression audits (parser / role classifier, names are not physics):")
            for row in self.expression_audits:
                lines.append(
                    f"  {row['expression']!r}: evidence={row['evidence']} "
                    f"warnings={len(row['warnings'])} extra={row['extra']}"
                )
        if self.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
        if self.notes:
            lines.append("")
            for note in self.notes:
                lines.append(note)
        lines.append("")
        lines.append(f"Registry HP ids: {', '.join(self.registry_hp_ids)}")
        lines.append(f"Conflicts involving HP: {len(self.conflicts)}")
        lines.append(f"Nulls involving HP: {', '.join(self.nulls) or 'none'}")
        lines.append(f"Protocol hash: {self.protocol_hash}")
        return "\n".join(lines)


def briefing_components() -> list[ComponentRecord]:
    """Every object the probe is willing to record. DA does not merge them."""
    return [
        ComponentRecord(
            "C-P",
            "P",
            "domain / cutoff / self-adjoint extension of whatever H is chosen",
            "open",
            False,
            "recorded as admissibility; not filled from zeta zeros",
            "must be declared once H is chosen; xp cutoff is extra structure",
            "HP-U3 / Berry–Keating cutoff",
        ),
        ComponentRecord(
            "C-H",
            "H",
            "no unique independent Hamiltonian; several incompatible candidates exist",
            "missing",
            False,
            "refused to pick a winner by symbol overlap; kept candidates distinct",
            "load-bearing gap remains",
            "HP-S0",
        ),
        ComponentRecord(
            "C-psi",
            "ψ",
            "eigenfunctions of an independently specified H",
            "downstream",
            False,
            "kept downstream of H; not a free wavefunction to tune",
            "cannot be filled before H",
            "quantum state role",
        ),
        ComponentRecord(
            "C-lambda",
            "λ",
            "eigenvalue parameter E_n with subtype eigenvalue",
            "target",
            True,
            "declared scale subtype = eigenvalue, not a transfer function",
            "claim E_n = γ_n is identity, not a fill",
            "HP-H001",
        ),
        ComponentRecord(
            "C-Phi",
            "Φ",
            "spectral data of H (spectrum / det); target identity spec(H) = {γ_n}",
            "target",
            False,
            "recorded as claimed output, not as definition of H",
            "circular if Φ := zeros is used as the instance",
            "HP-H001 / HP-H007",
        ),
        ComponentRecord(
            "C-Hspace",
            "ℋ",
            "Hilbert space must be declared (L²(ℝ), adelic space, …)",
            "open",
            False,
            "promoted out of the five-role map into E / UHF",
            "quantum does not fit in five roles without ℋ",
            "UHF requirement",
        ),
        ComponentRecord(
            "C-inner",
            "⟨,⟩",
            "inner product / units / normalization on ℋ",
            "open",
            False,
            "recorded as a separate component (changes self-adjointness)",
            "missing until ℋ is chosen",
            "HP-U2",
        ),
        ComponentRecord(
            "C-B",
            "ℬ",
            "boundary conditions and deficiency indices of D(H)",
            "open",
            False,
            "recorded as boundary data, not hidden inside P",
            "xp is not essentially self-adjoint without this",
            "HP-U3",
        ),
        ComponentRecord(
            "C-D",
            "D",
            "evolution e^{-iHt} once H is self-adjoint; alternatively d/dt",
            "blocked",
            False,
            "DHFA layer exists only after HP-S1; not a route to construct H",
            "dynamics do not invent the operator",
            "HP-D1",
        ),
        ComponentRecord(
            "C-decoherence",
            "Ξ",
            "decoherence / damping = 0 for a closed Hamiltonian system",
            "implicit",
            True,
            "recorded as implicit unitary assumption (Ξ = 0)",
            "GUE statistics assume a closed chaotic system, not open dissipation",
            "quantum closed-system hypothesis",
        ),
        ComponentRecord(
            "C-completed-xi",
            "E-entire",
            "completed zeta ξ(s); entire; archimedean Gamma factor included",
            "theorem",
            True,
            "kept as analytic input, not as a Hamiltonian",
            "may become the left-hand side of a det identity after H exists",
            "HP-H006",
        ),
        ComponentRecord(
            "C-FE",
            "E-entire",
            "ξ(s) = ξ(1 − s)",
            "theorem",
            True,
            "recorded as functional equation; representation of a known identity",
            "does not specify H",
            "Riemann 1859 / HP-H006",
        ),
        ComponentRecord(
            "C-Euler",
            "E-arithmetic",
            "Euler product ζ(s) = ∏_p (1 − p^{-s})^{-1} for Re s > 1",
            "theorem",
            True,
            "recorded as the arithmetic source of primes; not a selector P_n",
            "primes enter as Euler factors, not as a physical prime mask",
            "Euler 1737",
        ),
        ComponentRecord(
            "C-Weil",
            "E-trace",
            "Weil explicit formula: zeros ↔ primes",
            "theorem",
            True,
            "recorded in E as the target trace identity; refused as H",
            "theorem about ζ, not a dynamical system",
            "HP-H002",
        ),
        ComponentRecord(
            "C-NT",
            "E-trace",
            "N(T) = (T/2π) log(T/2πe) + S(T) + O(1)  (von Mangoldt / Riemann–von Mangoldt)",
            "theorem",
            True,
            "recorded as Weyl-law target for a future H; not a spectrum",
            "necessary and far from sufficient",
            "HP-S3",
        ),
        ComponentRecord(
            "C-LP",
            "E-entire",
            "Laguerre–Pólya class: entire functions that are limits of real-rooted polynomials",
            "theorem",
            True,
            "recorded as Pólya’s proven entire-function calculus, parallel to Hilbert–Pólya",
            "ξ(1/2+iz) has only real zeros iff RH; LP membership is a sufficient packing of that claim, not a new H",
            "Pólya; Laguerre–Pólya class",
        ),
        ComponentRecord(
            "C-Jensen",
            "E-entire",
            "Jensen polynomials of ξ; Griffin–Ono–Rolen–Zagier: they approach Hermite polynomials",
            "theorem_plus_asymptotics",
            True,
            "recorded as a proven approximation to real-rooted polynomials, not RH",
            "Hermite limits are real-rooted; finite-N hyperbolicity is not RH",
            "GORZ 2019; Jensen / Pólya",
        ),
        ComponentRecord(
            "C-Hermite",
            "E-entire",
            "Hermite polynomials: oscillator eigenfunctions, GUE orthogonal polynomials, and GORZ limit of Jensen(ξ)",
            "collision",
            True,
            "recorded as a shared special function, then Weyl-screened against N(T)",
            "not a Hamiltonian. Equal spacing is rejected; Hermite-in-three-books is not identity of H",
            "oscillator / GUE / GORZ collision",
        ),
        ComponentRecord(
            "C-BK",
            "H-candidate",
            "H = xp (or (xp+px)/2) with phase-space cutoff",
            "candidate",
            True,
            "accepted as an independent classical symbol; not promoted to the unique H",
            "missing unique quantization, cutoff justification, spectral identity",
            "HP-H003 Berry–Keating",
        ),
        ComponentRecord(
            "C-Connes",
            "H-candidate",
            "adelic absorption spectrum (missing lines)",
            "candidate",
            True,
            "kept incompatible with Berry–Keating (absorption vs emission)",
            "not a compact point-spectrum Hamiltonian of {γ_n}",
            "HP-H004",
        ),
        ComponentRecord(
            "C-GUE",
            "E-statistics",
            "Montgomery–Odlyzko pair correlation matches GUE",
            "conjecture_plus_numerics",
            True,
            "recorded as universality class HP-G1; ran negative laboratory vs {γ_n}",
            "statistics ≠ spectral identity",
            "HP-H005",
        ),
        ComponentRecord(
            "C-diag",
            "forbidden",
            "H = diag(γ_n) on ℓ² or Φ := {γ_n} as a definition",
            "circular",
            False,
            "retired as a construction; kept as a null",
            "tautological or assumes RH",
            "HP-H007",
        ),
        ComponentRecord(
            "C-Tbreak",
            "E-symmetry",
            "time-reversal breaking if the statistics are GUE rather than GOE",
            "heuristic",
            True,
            "recorded as extra symmetry data any chaotic H would have to carry",
            "constraint on a future H, not a formula for H",
            "Berry; Bohigas–Giannoni–Schmit",
        ),
        ComponentRecord(
            "C-SFEHAM",
            "other-book",
            "retired inverse-GCD Fock Hamiltonian Ĥ_SFE",
            "other_book",
            True,
            "classified INCOMPATIBLE with Berry–Keating; not ingested as H",
            "different space and interaction; not Hilbert–Pólya",
            "SFE-H003",
        ),
        ComponentRecord(
            "C-NS",
            "other-book",
            "incompressible Navier–Stokes / vorticity form",
            "other_book",
            True,
            "no checked transformation to Weil, ξ, xp, or LP class",
            "INSUFFICIENT_INFORMATION as a Pólya-to-NS bridge; do not glue",
            "NS-B in inventory",
        ),
        ComponentRecord(
            "C-Polya1926",
            "E-entire",
            "Pólya 1926: sufficient conditions on Φ so ∫ Φ(t) cos(zt) dt has only real zeros",
            "theorem",
            True,
            "accepted as a proven sufficient criterion; refused as a fill of H",
            "relocates the gap to a kernel hypothesis; does not produce a Hamiltonian",
            "HP-H011",
        ),
        ComponentRecord(
            "C-RiemannPhi",
            "E-entire",
            "Ξ(z) = ∫_0^∞ Φ(t) cos(zt) dt with Riemann’s positive even kernel Φ",
            "theorem",
            True,
            "recorded as the shape that makes 1926 applicable in principle",
            "shape matches; 1926 hypotheses are not a checked theorem for this Φ",
            "HP-H012",
        ),
        ComponentRecord(
            "C-PolyaSzego",
            "other-book",
            "Pólya–Szegő inequalities (analysis / potential theory)",
            "other_book",
            True,
            "ingested because they sometimes appear in PDE estimates; no NS map checked",
            "INSUFFICIENT_INFORMATION as a Clay-NS solution",
            "Pólya–Szegő, Problems and Theorems in Analysis",
        ),
        ComponentRecord(
            "C-PolyaLiouville",
            "forbidden",
            "Pólya’s Liouville-sum conjecture L(x)≤0 (disproved)",
            "disproved",
            True,
            "recorded as a disproved Pólya claim so proven work is not confused with every Pólya sentence",
            "Pólya is not an oracle; this claim is false",
            "HP-H013",
        ),
    ]


def millennium_routing() -> list[dict[str, str]]:
    """Pólya objects versus Clay problems. Shared vocabulary is not a proof."""
    return [
        {
            "prize": "Riemann hypothesis",
            "polya_object": "Hilbert–Pólya; Laguerre–Pólya class; Pólya 1926 cosine-transform criterion",
            "relation": "direct open strategy",
            "status": "open; probe does not prove it",
        },
        {
            "prize": "Navier–Stokes existence and smoothness",
            "polya_object": "Pólya–Szegő inequalities ingested; no checked map to regularity",
            "relation": "INSUFFICIENT_INFORMATION",
            "status": "separate book; do not derive from ξ or xp",
        },
        {
            "prize": "Yang–Mills mass gap",
            "polya_object": "spectral language only (no checked operator map)",
            "relation": "INSUFFICIENT_INFORMATION",
            "status": "shared word “spectrum” is not a transformation",
        },
        {
            "prize": "Birch and Swinnerton-Dyer",
            "polya_object": "L-functions in the same arithmetic family as ζ",
            "relation": "COMPATIBLE_DISTINCT",
            "status": "same explicit-formula style; different L-function; not solved here",
        },
        {
            "prize": "Hodge conjecture",
            "polya_object": "none checked",
            "relation": "INSUFFICIENT_INFORMATION",
            "status": "no Pólya input ingested",
        },
        {
            "prize": "P versus NP",
            "polya_object": "none checked",
            "relation": "INSUFFICIENT_INFORMATION",
            "status": "no Pólya input ingested",
        },
    ]


def da_requests() -> list[str]:
    return [
        "One independent operator formula for H, with a declared Hilbert space, "
        "inner product, and domain — not a merge of xp, adeles, GUE, and diag(γ_n).",
        "A proof that that H is essentially self-adjoint (deficiency indices).",
        "A decision whether an xp cutoff is P, ℬ, or a separate regularization in E.",
        "A trace identity deriving Weil’s formula from Tr f(H), or a proven "
        "identification ξ(s) ∝ det((s−1/2)/i − H) times an entire factor of specified order.",
        "Multiplicity data: simple zeros versus possible multiple eigenvalues.",
        "If Laguerre–Pólya / Pólya 1926 is the route instead of a Hamiltonian: "
        "an independent verification that Riemann’s Φ meets the 1926 hypotheses, "
        "or that ξ(1/2+iz) lies in the LP class, not an appeal to RH.",
        "If a Navier–Stokes or other-prize bridge is claimed: an explicit checked "
        "transformation. Shared letters are not enough.",
    ]


def _findings() -> list[str]:
    return [
        "Quantum Hilbert–Pólya does not fit in five roles. DA expanded the "
        "record to Hilbert space, inner product, domain/boundary data, unitary "
        "evolution, implicit Ξ = 0, arithmetic (Euler/Weil), entire-function "
        "data (ξ, functional equation, Laguerre–Pólya, Jensen), statistics "
        "(GUE), and symmetry (time-reversal breaking).",
        "Two parallel Pólya routes exist and must not be merged: (1) Hilbert–Pólya "
        "— a self-adjoint H whose eigenvalues are the γ_n; (2) Laguerre–Pólya — "
        "ξ(1/2+iz) as an entire function of the LP class (all zeros real). Both "
        "imply RH if completed. Each is missing its independent object (H, or an "
        "LP-membership proof that does not assume RH).",
        "Feeding Pólya’s proven LP / Jensen calculus does not fill H. It restates "
        "the reality of zeros in entire-function language.",
        "Pólya 1926 is the actual attempt to solve H with proven Pólya analysis: "
        "a sufficient condition for cosine transforms to have only real zeros. "
        "Riemann Ξ has that shape. The hypotheses are not a checked theorem for "
        "Riemann’s Φ. So Pólya relocates the gap (kernel condition instead of H) "
        "and does not fill the H role. A disproved Pólya conjecture (Liouville "
        "sums) is recorded so proven theorems are not treated as an oracle.",
        "Berry–Keating xp is the only supplied emission-Hamiltonian candidate "
        "with an independent classical symbol. Connes is a different object. "
        "GUE is not an object of that type. diag(γ_n) is circular.",
        "A frozen GUE matrix is not the sequence γ_n after a best affine map. "
        "Random-matrix agreement cannot substitute for the spectral identity.",
        "Usable filter: N(T) rejects the harmonic oscillator and any equally "
        "spaced spectrum. Riemann mean gaps shrink like 1/log T; oscillator "
        "gaps do not. Hermite polynomials appearing in the oscillator, in GUE, "
        "and as the GORZ limit of Jensen(ξ) is a special-function collision, "
        "not a shared H. Classical xp matches the leading von Mangoldt term "
        "(compatibility, not identity).",
        "No checked transformation connects these objects to Navier–Stokes or to "
        "a canonical SFE. Other-book formulas were classified, not absorbed.",
        "A filled N-component map is still classification (Level 0) plus "
        "negative laboratories (Level 1). It is not a surprise Hamiltonian. "
        "The Weyl screen is a surprise *filter*: it can throw out the wrong H "
        "now, without proving RH.",
    ]


def _audit_expressions() -> list[dict[str, Any]]:
    expressions = [
        "H = xp",
        "xi(s) = xi(1-s)",
        "Hilbert-Polya Hamiltonian",
    ]
    rows = []
    for expr in expressions:
        report = audit_expression(expr)
        rows.append(
            {
                "expression": expr,
                "evidence": int(report.highest_evidence_level),
                "warnings": list(report.warnings),
                "extra": list(report.extra_structures),
                "sfe": report.canonical_sfe_status,
            }
        )
    return rows


def run_polya_probe() -> PolyaProbeReport:
    """Ingest the full briefing and return what Domain Architect can do with it."""
    components = briefing_components()
    core_roles = {"P", "H", "ψ", "λ", "Φ"}
    core_count = sum(1 for c in components if c.role in core_roles)
    extension_count = len(components) - core_count

    registry = EquationRegistry.load_default()
    hp_ids = sorted(
        eq_id for eq_id in registry.equations if eq_id.startswith("HP-")
    )
    conflicts = [
        f"{c.left_id}/{c.right_id}:{c.relation}"
        for c in registry.conflicts
        if c.left_id.startswith("HP-") or c.right_id.startswith("HP-")
    ]
    nulls = [n.null_id for n in registry.nulls if "HP" in n.null_id]

    scores = []
    for cand in historical_candidates():
        if cand.candidate_id in {"unspecified"}:
            continue
        audit = audit_candidate(cand.candidate_id)
        scores.append(
            {
                "candidate_id": cand.candidate_id,
                "independent_h": cand.hamiltonian_independent_of_zeros,
                "circular": audit.circular,
                "complete": audit.complete,
                "missing": list(audit.missing_piece_ids),
            }
        )

    gue = gue_is_not_riemann_spectrum()
    weyl = weyl_law_screen()
    warnings = [
        GUE_NOT_IDENTITY_WARNING,
        "N independently specifiable components were recorded. That count is "
        "not a universal physical equation and not a claim that every theory "
        "has this many parts.",
        "Exploratory ingestion is not a license to merge other-book formulas "
        "or to treat classification as a Millennium solution.",
    ]
    notes = [
        PROBE_SCOPE,
        "Pieces on the Hilbert–Pólya checklist: "
        + ", ".join(p.piece_id for p in program_pieces()),
        "UHF extras that remain required: " + "; ".join(extra_structures()),
    ]

    protocol = freeze_protocol(
        {
            "program": "polya-probe",
            "components": [c.component_id for c in components],
            "forbid_circular_fills": True,
            "forbid_millennium_glue": True,
            "gue_is_not_identity": True,
            "weyl_law_screen": True,
        }
    )

    complete = all(row["complete"] for row in scores)
    evidence = int(EvidenceLevel.MATHEMATICAL_COMPATIBILITY)
    if gue["is_riemann_spectrum"]:
        evidence = int(EvidenceLevel.COHERENT_CLASSIFICATION)

    return PolyaProbeReport(
        instance_name="polya-probe",
        component_count=len(components),
        core_role_count=core_count,
        extension_count=extension_count,
        components=components,
        da_requests=da_requests(),
        findings=_findings(),
        millennium_routing=millennium_routing(),
        candidate_scores=scores,
        expression_audits=_audit_expressions(),
        gue_laboratory=gue,
        weyl_laboratory=weyl,
        registry_hp_ids=hp_ids,
        conflicts=conflicts,
        nulls=nulls,
        highest_evidence_level=evidence,
        hilbert_polya_status=HILBERT_POLYA_STATUS,
        rh_status=RH_STATUS,
        canonical_sfe_status=CANONICAL_SFE_STATUS,
        complete=complete,
        protocol_hash=protocol.protocol_hash,
        warnings=warnings,
        notes=notes,
    )
