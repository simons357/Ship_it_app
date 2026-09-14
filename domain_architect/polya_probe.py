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
from .millennium_overlap import closest_rhymes, overlap_looks
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

COUNT_POLICY: str = (
    "P, H, ψ, λ, Φ are an interface, not a cap. The count can be 7, 8, 15, "
    "or whatever the subject requires. DA decides. Five is what we started "
    "with, not what quantum Hilbert–Pólya fitted into."
)

QUANTUM_FIT_IDS: tuple[str, ...] = (
    "C-Hspace",
    "C-inner",
    "C-B",
    "C-D",
    "C-decoherence",
    "C-Tbreak",
)


def how_quantum_fitted(components: list[ComponentRecord] | None = None) -> list[str]:
    """What DA added because a quantum Hamiltonian does not fit in five letters."""
    items = components if components is not None else briefing_components()
    lines = [
        "A quantum Hamiltonian is not five letters. DA kept P, H, ψ, λ, Φ "
        "as the interface and recorded every extra object the subject needed.",
    ]
    for item in items:
        if item.component_id in QUANTUM_FIT_IDS:
            lines.append(
                f"{item.role}: {item.occupant} — {item.verdict}"
            )
    lines.append(
        "Those extras are how quantum fitted. Hiding them to keep a count of "
        "five would lose the theory."
    )
    return lines


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
    filter_pops: list[str]
    filter_scoreboard: list[dict[str, str]]
    how_quantum_fitted: list[str]
    count_policy: str
    millennium_looks: list[dict[str, str]]
    closest_rhymes: list[str]
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
            f"DA decided the component count for this subject: {self.component_count}",
            f"Independently specifiable components recorded: {self.component_count} "
            f"({self.core_role_count} core interface letters + {self.extension_count} extension / E)",
            self.count_policy,
            f"Interface letters recorded: {self.core_role_count} "
            f"(P, H, ψ, λ, Φ). Extra independently specifiable objects: "
            f"{self.extension_count}.",
            f"Hilbert–Pólya status: {self.hilbert_polya_status}.",
            f"Riemann hypothesis status: {self.rh_status}.",
            f"Canonical SFE status: {self.canonical_sfe_status}.",
            f"Program complete: {self.complete}",
            f"Highest evidence level actually supported: Level {self.highest_evidence_level}",
            "",
            "How quantum fitted (DA expanded; it did not squeeze into five):",
        ]
        for line in self.how_quantum_fitted:
            lines.append(f"  * {line}")
        lines.append("")
        lines.append("Who survived the filter (RH-attack sources):")
        for row in self.filter_scoreboard:
            lines.append(f"  [{row['result']}] {row['source']}")
            lines.append(f"    {row['objects']}")
            lines.append(f"    {row['notes']}")
        lines.append("")
        lines.append("What popped through the DA filter:")
        for pop in self.filter_pops:
            lines.append(f"  * {pop}")
        lines.append("")
        lines.append("What Domain Architect did with the supplied objects:")
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
        lines.append("What rhymed when we looked across prizes (not a unification):")
        for rhyme in self.closest_rhymes:
            lines.append(f"  * {rhyme}")
        lines.append("")
        lines.append("Looks (parts of Pólya vs each prize):")
        for look in self.millennium_looks:
            lines.append(f"  [{look['look_id']}] {look['prize']}  match={look['match_level']}")
            lines.append(f"    Pólya part: {look['polya_part']}")
            lines.append(f"    other: {look['other_object']}")
            lines.append(f"    matched: {look['what_matched']}")
            lines.append(f"    did not: {look['what_did_not']}")
            lines.append(f"    {look['status']}")
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
            "promoted into E; quantum needed ℋ as its own component",
            "quantum does not fit in five letters without ℋ",
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
        ComponentRecord(
            "C-BN",
            "λ-alt",
            "de Bruijn–Newman constant Λ; Ξ_t has only real zeros iff t ≥ Λ; Λ ≥ 0 theorem; RH ⇔ Λ = 0",
            "theorem_plus_open",
            True,
            "promoted to a second scale occupant, not merged with {γ_n} and not called H",
            "pop through the DA filter: one real number instead of an infinite spectrum. Λ = 0 is still RH",
            "HP-H014",
        ),
        ComponentRecord(
            "C-PolyaSchur",
            "E-entire",
            "Pólya–Schur multiplier sequences (preserve real-rooted polynomials)",
            "theorem",
            True,
            "accepted as the algebraic filter of the LP class; γ_k multipliers ≠ Riemann γ_n",
            "proven; does not fill H; notation collision on γ",
            "HP-H015",
        ),
        ComponentRecord(
            "C-XiIntegral",
            "E-entire",
            "Pólya 1926 Acta: integral representation of Riemann’s ξ",
            "theorem",
            True,
            "ingested as the 1926 ξ-representation paper, kept distinct from the cosine-zero criterion",
            "representation of ξ, not H",
            "HP-H016",
        ),
        ComponentRecord(
            "C-PF",
            "E-entire",
            "Pólya frequency functions / variation-diminishing convolutions (totally positive kernels)",
            "theorem",
            True,
            "ingested as the analytic engine behind cosine-transform real-zero criteria",
            "a PF / variation-diminishing check on Riemann’s Φ is a possible fill of the 1926 hypotheses, not a Hamiltonian",
            "HP-H017",
        ),
        ComponentRecord(
            "C-Turan",
            "E-entire",
            "Turán inequalities on Taylor coefficients of LP-class entire functions",
            "theorem",
            True,
            "ingested as coefficient tests for the LP class / Jensen hyperbolicity",
            "necessary for LP membership; not RH unless checked for ξ without assuming RH",
            "HP-H018",
        ),
        ComponentRecord(
            "C-EntireZeros",
            "E-entire",
            "Pólya 1918 / 1923: distribution of zeros of certain entire functions",
            "theorem",
            True,
            "ingested as Pólya’s earlier zero-distribution calculus",
            "general entire-function zeros; not spec(H) = {γ_n}",
            "HP-H023",
        ),
        ComponentRecord(
            "C-IntegerEntire",
            "E-entire",
            "Pólya 1915: integer-valued entire functions (ganzwertige ganze Funktionen)",
            "theorem",
            True,
            "ingested because it is proven Pólya entire-function work",
            "different book from ξ; no checked map to Riemann zeros",
            "HP-H024",
        ),
        ComponentRecord(
            "C-Isoperimetric",
            "other-book",
            "Pólya–Szegő 1951 Isoperimetric Inequalities in Mathematical Physics",
            "other_book",
            True,
            "ingested as the mathematical-physics book (eigenvalues, torsion, capacity)",
            "spectral geometry / isoperimetric estimates; no checked map to Clay NS regularity",
            "HP-H019",
        ),
        ComponentRecord(
            "C-Membrane",
            "other-book",
            "Pólya 1954: eigenvalues of vibrating membranes (Weyl-type counts for domains)",
            "other_book",
            True,
            "ingested as a second Weyl-law book, kept unmerged with N(T)",
            "domain eigenvalue asymptotics are not the Riemann–von Mangoldt law",
            "HP-H020",
        ),
        ComponentRecord(
            "C-Enumeration",
            "other-book",
            "Pólya 1937 enumeration theorem (cycle index of group actions)",
            "other_book",
            True,
            "ingested as proven Pólya combinatorics",
            "no checked map to ξ, H, or Navier–Stokes",
            "HP-H021",
        ),
        ComponentRecord(
            "C-RandomWalk",
            "other-book",
            "Pólya 1921: simple random walk is recurrent in d=1,2 and transient in d≥3",
            "other_book",
            True,
            "ingested as proven Pólya probability; compared with 3D Biot–Savart",
            "LOOK-NS-GREEN: d≥3 transience shares the Green/Newtonian family with 3D NS; not regularity",
            "HP-H022 / HP-H027",
        ),
        ComponentRecord(
            "C-Rearrange",
            "other-book",
            "Pólya–Szegő rearrangement: Dirichlet integral does not increase under Schwarz symmetrization",
            "other_book",
            True,
            "looked at as a PDE estimate tool next to NS energy methods",
            "shared-tool with Sobolev / Ladyzhenskaya; not Clay NS smoothness",
            "HP-H025",
        ),
        ComponentRecord(
            "C-StokesOp",
            "other-book",
            "Stokes operator A = −ℙΔ on divergence-free fields (spectral sibling of membrane Laplacian)",
            "other_book",
            True,
            "looked at next to Pólya 1954 membrane eigenvalues",
            "spectral sibling of HP-H020; not Hilbert–Pólya H; not Clay NS",
            "NS-H003",
        ),
        ComponentRecord(
            "C-NSPhi",
            "other-book",
            "this-repo swirl algebra: Γ=r u_θ, Φ=u_θ/r, r^{-4}∂_z(Γ²)=∂_z(Φ²)",
            "other_book",
            True,
            "ingested because it is the kept NS identity in this repo; Φ here is not FRA Φ and not Riemann’s kernel Φ",
            "KEEP algebra; open barrier ‖u^r/r‖_∞; notation collision with Riemann Φ",
            "NS-H002",
        ),
    ]


def millennium_routing() -> list[dict[str, str]]:
    """Pólya objects versus Clay problems. Shared vocabulary is not a proof."""
    return [
        {
            "prize": "Riemann hypothesis",
            "polya_object": "Hilbert–Pólya; LP class; Pólya 1926; de Bruijn–Newman Λ (RH ⇔ Λ=0)",
            "relation": "direct open strategy",
            "status": "open; probe does not prove it",
        },
        {
            "prize": "Navier–Stokes existence and smoothness",
            "polya_object": (
                "LOOKED: 1921 Green/Biot–Savart rhyme; rearrangement as PDE tool; "
                "membrane vs Stokes operator; heat-name rhyme; Φ-letter collision. "
                "No regularity map."
            ),
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


def filter_scoreboard() -> list[dict[str, str]]:
    """RH-attack sources only. Classical input theorems (Euler, Riemann, Weil) are not scored here."""
    return [
        {
            "source": "George Pólya (proven entire-function / Fourier / multiplier / frequency)",
            "result": "survived",
            "objects": (
                "Laguerre–Pólya class; Pólya–Schur multipliers; 1926 cosine-zero "
                "criterion; 1926 Acta ξ integral; Pólya frequency kernels; "
                "1918/1923 zero distribution"
            ),
            "notes": (
                "Only RH-attack source whose theorems remain as usable objects. "
                "Does not fill H. Does not prove RH. Heat-flow continuation is Λ."
            ),
        },
        {
            "source": "de Bruijn–Newman–Rodgers–Tao (continuation of Pólya 1926)",
            "result": "survived-as-continuation",
            "objects": "de Bruijn–Newman Λ; Λ ≥ 0 theorem; RH ⇔ Λ = 0",
            "notes": "They extended Pólya’s win to one real number. Still not RH.",
        },
        {
            "source": "Hilbert–Pólya program",
            "result": "incomplete",
            "objects": "strategy: self-adjoint H with spec(H) = {γ_n}",
            "notes": "No independent Hamiltonian on record. Strategy, not a theorem.",
        },
        {
            "source": "Berry–Keating xp",
            "result": "incomplete",
            "objects": "classical symbol xp with cutoff",
            "notes": "Independent emission candidate. Missing quantization, cutoff, spectral identity.",
        },
        {
            "source": "Connes adelic absorption",
            "result": "incomplete",
            "objects": "missing lines / absorption spectrum",
            "notes": "Incompatible with Berry–Keating. Not a compact point spectrum of {γ_n}.",
        },
        {
            "source": "Montgomery–Odlyzko GUE",
            "result": "not-identity",
            "objects": "pair correlation / universality class",
            "notes": "Statistics survive as HP-G1. A frozen GUE matrix is not {γ_n}.",
        },
        {
            "source": "H = diag(γ_n) / Φ := zeros",
            "result": "retired",
            "objects": "circular FRA fill",
            "notes": "Tautological or assumes RH.",
        },
        {
            "source": "harmonic oscillator / equal spacing as H",
            "result": "rejected",
            "objects": "Hermite eigenfunctions; equal gaps",
            "notes": "N(T) kills equal spacing. Hermite-in-three-books is not H.",
        },
        {
            "source": "retired SFE-HAM",
            "result": "incompatible",
            "objects": "inverse-GCD Fock Hamiltonian",
            "notes": "Different book. Not Hilbert–Pólya.",
        },
        {
            "source": "Pólya Liouville-sum conjecture",
            "result": "false",
            "objects": "L(x) ≤ 0",
            "notes": "The Pólya claim that does not survive. Proven Pólya is not every Pólya sentence.",
        },
        {
            "source": "Pólya–Szegő 1951 / membrane 1954 / enumeration / random walk as Clay NS",
            "result": "insufficient",
            "objects": "isoperimetric physics; membrane Weyl law; combinatorics; lattice walk",
            "notes": "Proven Pólya, other books. No checked map to Clay NS or to spec(H) = {γ_n}.",
        },
    ]


def filter_pops() -> list[str]:
    """What survives DA’s filter as a distinct, usable object — not a Hamiltonian."""
    return [
        "Among RH-attack sources, Pólya is the only one whose theorems survive "
        "as usable objects. Hilbert–Pólya is still a strategy with no H. "
        "Berry–Keating, Connes, GUE-as-identity, diag(γ_n), the oscillator, "
        "and SFE-HAM do not survive as a filled Hamiltonian. Pólya also lost "
        "one: the Liouville-sum conjecture is false.",
        "N(T) rejects equal-spaced H (the oscillator). Hermite polynomials in "
        "the oscillator, GUE, and Jensen(ξ) are a special-function collision, not H.",
        "Two Pólya routes stay unmerged: a self-adjoint Hamiltonian versus "
        "Laguerre–Pólya / Pólya 1926 kernel conditions.",
        "Pólya 1926 plus heat flow contracts the missing object to one real "
        "number Λ (de Bruijn–Newman). Rodgers–Tao: Λ ≥ 0 is a theorem. "
        "RH ⇔ Λ = 0. This is a second scale occupant, not H and not {γ_n}.",
        "Pólya–Schur multiplier sequences are a proven algebraic filter on "
        "real-rooted polynomials. Their γ_k are not the Riemann heights γ_n.",
        "Pólya frequency / variation-diminishing kernels are the analytic "
        "engine of the 1926 cosine criterion. Checking that Riemann’s Φ is "
        "PF of sufficient order would be a kernel fill, not H.",
        "Two Weyl laws stay unmerged: Riemann–von Mangoldt N(T) versus "
        "Pólya membrane eigenvalue counts for domains.",
        "Turán inequalities are coefficient tests for the LP class. They "
        "are not RH unless they are checked for ξ without assuming RH.",
        "Pólya 1937 enumeration and 1921 random-walk recurrence ingest as "
        "proven work. The 1921 d≥3 transience rhymes with the 3D Newtonian "
        "kernel in Biot–Savart; that is not Clay NS.",
        "Pólya’s Liouville-sum conjecture does not survive the filter (false).",
        "Looked across Clay prizes: tool/kernel rhymes with NS, family "
        "resemblance with BSD L-functions, vocabulary with Yang–Mills. "
        "No Pólya object unifies the prizes. Live prize for the surviving "
        "theorems is still RH.",
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
        "If the de Bruijn–Newman route is chosen: a proof of Λ ≤ 0 that does "
        "not assume RH. Λ ≥ 0 is already a theorem.",
        "If a Navier–Stokes or other-prize bridge is claimed: an explicit checked "
        "transformation. Shared letters are not enough.",
        "A check whether Riemann’s Φ is a Pólya frequency function "
        "(variation-diminishing of sufficient order). That would address the "
        "1926 hypotheses; it would still not be an operator H.",
        "Turán / Jensen hyperbolicity inequalities for ξ that do not assume RH.",
        "If vibrating-membrane or 1951 isoperimetric estimates are claimed for "
        "Navier–Stokes: an explicit regularity map from those inequalities to "
        "smoothness of 3D incompressible flow.",
    ]


def _findings() -> list[str]:
    return [
        "Quantum Hilbert–Pólya does not fit in five letters. DA decided "
        "the count from the subject and expanded to Hilbert space, inner "
        "product, domain/boundary data, unitary evolution, implicit Ξ = 0, "
        "arithmetic (Euler/Weil), entire-function data (ξ, functional "
        "equation, Laguerre–Pólya, Jensen), statistics (GUE), and symmetry "
        "(time-reversal breaking). Another subject can land at 7 or 8. "
        "This one did not.",
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
        "Riemann’s Φ. Pólya relocates the gap, then heat flow contracts it to Λ. "
        "DA’s pop: one real number with target Λ = 0, distinct from the H role "
        "and from {γ_n}.",
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
        "a canonical SFE. Other-book formulas were classified, not absorbed. "
        "Dumping the 1951 isoperimetric book, 1954 membrane eigenvalues, 1937 "
        "enumeration theorem, and 1921 random walk does not create a bridge. "
        "Looking at rearrangement, Biot–Savart/Green, and the Stokes operator "
        "found rhymes, not a Clay solution.",
        "Pólya frequency / variation-diminishing structure is the natural "
        "language of the 1926 kernel hypotheses. DA recorded it as a possible "
        "fill of those hypotheses, not as H and not as a proof that Riemann’s "
        "Φ is PF.",
        "A filled N-component map is still classification (Level 0) plus "
        "negative laboratories (Level 1). It is not a surprise Hamiltonian. "
        "The Weyl screen is a surprise *filter*: it can throw out the wrong H "
        "now, without proving RH.",
        "Filter scoreboard: Pólya is the only RH-attack source whose theorems "
        "survive as usable objects. That is a win for entire-function / Fourier "
        "calculus, not a Hamiltonian and not RH. Everyone else in the attack "
        "column is incomplete, not-identity, retired, rejected, incompatible, "
        "false, or insufficient.",
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
            "filter_scoreboard": True,
            "da_decides_component_count": True,
            "millennium_look": True,
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
        filter_pops=filter_pops(),
        filter_scoreboard=filter_scoreboard(),
        how_quantum_fitted=how_quantum_fitted(components),
        count_policy=COUNT_POLICY,
        millennium_looks=[look.to_dict() for look in overlap_looks()],
        closest_rhymes=closest_rhymes(),
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
