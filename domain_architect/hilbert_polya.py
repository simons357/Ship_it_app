"""Hilbert–Pólya as a Functional Role Analysis program, not a proof.

The compact grammar Φ = ℱ(P, H, ψ, λ; E) can *organize* the strategy
that a self-adjoint Hamiltonian whose eigenvalues are the nontrivial
zeros would imply the Riemann hypothesis. Organizing the strategy does
not construct H, does not assign the zeros to Φ as a definition, and
does not treat random-matrix (GUE) statistics as a spectral identity.

Informal nicknames such as “five fingers” are not product vocabulary.
The five core roles are P, H, ψ, λ, and Φ.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Sequence

import numpy as np

from .protocol import freeze_protocol
from .schema import (
    EvidenceLevel,
    HILBERT_POLYA_STATUS,
    RH_STATUS,
    ScaleResponseSubtype,
)

CIRCULAR_ASSIGNMENT_WARNING: str = (
    "Setting the realized output Φ, the scale role λ, or the operator H "
    "to the Riemann zeros does not specify a Hilbert–Pólya Hamiltonian. "
    "That assignment is the target identity of the program, not an "
    "instance of H. Domain Architect records it as circular unless H is "
    "given by a formula that does not refer to the zeros."
)

DIAGONAL_ZEROS_WARNING: str = (
    "The diagonal operator diag(γ_n) on ℓ² is self-adjoint for any real "
    "sequence {γ_n}. Using the computed zeros produces a Hamiltonian of "
    "those zeros only. Using all nontrivial zeros as a real sequence "
    "assumes the Riemann hypothesis. Neither is an independent physical "
    "system."
)

GUE_NOT_IDENTITY_WARNING: str = (
    "GUE / random-matrix agreement is a statement about local statistics "
    "(universality). It is not a bijection between a spectrum and the "
    "zeros, and it does not fill the H role."
)

PROGRAM_SCOPE: str = (
    "This is a completeness audit of the Hilbert–Pólya program. It is "
    "not a proof of the Riemann hypothesis, not a canonical SFE, and not "
    "evidence that primes are physically privileged."
)

# First ten imaginary parts on the critical line, Odlyzko / tables.
# Used only to show that a random GUE matrix is not this sequence.
FIRST_RIEMANN_GAMMAS: tuple[float, ...] = (
    14.134725141734693790457251983562,
    21.022039638771554992628479677646,
    25.010857580145688763213790992562,
    30.424876125859513210311897530584,
    32.935061587739189690662368964074,
    37.586178158825671257217763480705,
    40.918719012147495187398126914633,
    43.327073280914999519496122165406,
    48.005150881167159727942472749427,
    49.773832477672302181916784678564,
)

_ZERO_PHRASES: tuple[str, ...] = (
    "riemann zero",
    "riemann zeros",
    "zeta zero",
    "zeta zeros",
    "nontrivial zero",
    "non-trivial zero",
    "zeros of zeta",
    "zeros of ξ",
    "zeros of xi",
    "ξ zeros",
    "xi zeros",
    "gamma_n",
    "γ_n",
    "{γ",
    "odlyzko",
)


@dataclass(frozen=True)
class CoreRoleOccupant:
    """One fill of a core FRA role inside the Hilbert–Pólya program."""

    role: str
    role_name: str
    target_occupant: str
    independent_of_zeros: bool
    status: str
    notes: str
    scale_subtype: str | None = None


@dataclass(frozen=True)
class ProgramPiece:
    """A unit of work that can be specified, proved, or blocked separately."""

    piece_id: str
    layer: str
    statement: str
    independently_tackleable: bool
    blocked_on: tuple[str, ...]
    status: str
    evidence_note: str


@dataclass
class CandidateRecord:
    candidate_id: str
    formula: str
    hamiltonian_independent_of_zeros: bool
    supplies_pieces: tuple[str, ...]
    missing_pieces: tuple[str, ...]
    circular: bool
    notes: str


@dataclass
class HilbertPolyaAudit:
    instance_name: str
    core_roles: list[CoreRoleOccupant]
    pieces: list[dict[str, Any]]
    circular: bool
    complete: bool
    missing_piece_ids: list[str]
    highest_evidence_level: int
    hilbert_polya_status: str
    rh_status: str
    warnings: list[str]
    notes: list[str]
    protocol_hash: str | None = None
    gue_laboratory: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["core_roles"] = [asdict(r) for r in self.core_roles]
        return payload

    def narrative(self) -> str:
        lines = [
            "Domain Architect — Hilbert–Pólya program audit",
            "",
            PROGRAM_SCOPE,
            "",
            f"Instance: {self.instance_name}",
            f"Hilbert–Pólya status: {self.hilbert_polya_status}.",
            f"Riemann hypothesis status: {self.rh_status}.",
            f"Highest evidence level actually supported: "
            f"Level {self.highest_evidence_level} — Coherent classification"
            if self.highest_evidence_level == 0
            else (
                f"Highest evidence level actually supported: "
                f"Level {self.highest_evidence_level}"
            ),
            f"Program complete: {self.complete}",
            f"Circular assignment: {self.circular}",
            "",
            "Core roles (organizational, not a derived Hamiltonian):",
        ]
        for role in self.core_roles:
            indep = "independent of zeros" if role.independent_of_zeros else (
                "NOT independent of zeros"
            )
            lines.append(
                f"  {role.role} ({role.role_name}): {role.target_occupant} "
                f"[{role.status}; {indep}]"
            )
            lines.append(f"    {role.notes}")
        lines.append("")
        lines.append("Program pieces:")
        for piece in self.pieces:
            flag = (
                "independent of RH"
                if piece["independently_tackleable"]
                else "blocked on prior pieces"
            )
            lines.append(
                f"  {piece['piece_id']} [{piece['layer']}/"
                f"{piece['status']}/{flag}] {piece['statement']}"
            )
            if piece["blocked_on"]:
                lines.append(f"    blocked on: {', '.join(piece['blocked_on'])}")
        if self.missing_piece_ids:
            lines.append("")
            lines.append("Missing for a Hilbert–Pólya proof of RH:")
            for pid in self.missing_piece_ids:
                lines.append(f"  - {pid}")
        if self.gue_laboratory:
            lines.append("")
            lines.append("GUE laboratory (statistics are not identity):")
            for key, value in self.gue_laboratory.items():
                lines.append(f"  {key}: {value}")
        if self.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
        if self.notes:
            lines.append("")
            for note in self.notes:
                lines.append(note)
        if self.protocol_hash:
            lines.append("")
            lines.append(f"Protocol hash: {self.protocol_hash}")
        return "\n".join(lines)


def core_role_map() -> list[CoreRoleOccupant]:
    """Target occupants of the five core roles. None of these is a fill."""
    return [
        CoreRoleOccupant(
            role="P",
            role_name="admissibility / domain",
            target_occupant=(
                "declared domain of H: Hilbert-space subspace, boundary "
                "conditions, self-adjoint extension, or cutoff projector"
            ),
            independent_of_zeros=True,
            status="must_be_declared",
            notes=(
                "P may be a cutoff or extension choice. If P is 'project onto "
                "the zeta-zero eigenspace', the fill is circular."
            ),
        ),
        CoreRoleOccupant(
            role="H",
            role_name="interaction / Hamiltonian",
            target_occupant=(
                "an operator given by a formula that does not mention the zeros"
            ),
            independent_of_zeros=True,
            status="missing",
            notes=(
                "This is the load-bearing gap. H is a Hamiltonian only after "
                "a mechanics model is declared. The letter H is not enough."
            ),
        ),
        CoreRoleOccupant(
            role="ψ",
            role_name="state / eigenfunction",
            target_occupant="eigenvectors of the independently specified H",
            independent_of_zeros=True,
            status="downstream_of_H",
            notes="Eigenfunctions exist only after H and its domain exist.",
        ),
        CoreRoleOccupant(
            role="λ",
            role_name="scale response",
            target_occupant="eigenvalue parameter E_n in Hψ = E_n ψ",
            independent_of_zeros=True,
            status="target_identity",
            scale_subtype=ScaleResponseSubtype.EIGENVALUE.value,
            notes=(
                "Subtype is eigenvalue (spectral coordinate), not a transfer "
                "function. The claim E_n = γ_n is the identity to prove, not "
                "a value to insert."
            ),
        ),
        CoreRoleOccupant(
            role="Φ",
            role_name="realized output",
            target_occupant=(
                "spectral data of H: point spectrum, spectral measure, or "
                "characteristic determinant"
            ),
            independent_of_zeros=True,
            status="target_identity",
            notes=(
                "The hoped-for identity is spec(H) = {γ_n} or "
                "ξ(s) ∝ det((s−1/2)/i − H) times a proven entire factor. "
                "Writing Φ := zeros is a claim, not a construction."
            ),
        ),
    ]


def extra_structures() -> list[str]:
    """Independently necessary objects. Do not hide them to fake a five-letter map."""
    return [
        "Hilbert space ℋ and inner product",
        "operator domain D(H) and deficiency indices",
        "archimedean / Gamma factor of ξ",
        "Weil explicit formula (primes on the geometric side)",
        "multiplicity of zeros / eigenvalues",
        "possible continuous spectrum versus point spectrum",
        "time-reversal breaking if GUE (not GOE) is expected",
        "regularization or cutoff if the classical symbol is xp",
    ]


def program_pieces() -> tuple[ProgramPiece, ...]:
    """Work units. Independently tackleable pieces can start without RH."""
    return (
        ProgramPiece(
            piece_id="HP-U1",
            layer="UHF",
            statement="Declare a Hilbert space ℋ without referring to ζ-zeros.",
            independently_tackleable=True,
            blocked_on=(),
            status="open",
            evidence_note="Many spaces are possible; none is canonical.",
        ),
        ProgramPiece(
            piece_id="HP-U2",
            layer="UHF",
            statement="Declare the inner product, units, and normalization on ℋ.",
            independently_tackleable=True,
            blocked_on=("HP-U1",),
            status="open",
            evidence_note="Depends only on the chosen space, not on RH.",
        ),
        ProgramPiece(
            piece_id="HP-U3",
            layer="UHF",
            statement="Declare the operator domain D(H) ⊂ ℋ and boundary data ℬ.",
            independently_tackleable=True,
            blocked_on=("HP-U1", "HP-S0"),
            status="open",
            evidence_note="Domain theory can proceed once a formula for H exists.",
        ),
        ProgramPiece(
            piece_id="HP-S0",
            layer="realization",
            statement=(
                "Give an independent formula for H (differential, integral, "
                "adelic, transfer, …) that does not mention the zeros."
            ),
            independently_tackleable=True,
            blocked_on=(),
            status="missing",
            evidence_note="Load-bearing gap. No complete candidate is on record.",
        ),
        ProgramPiece(
            piece_id="HP-S1",
            layer="realization",
            statement="Prove H is (essentially) self-adjoint on D(H).",
            independently_tackleable=False,
            blocked_on=("HP-S0", "HP-U3"),
            status="blocked",
            evidence_note="Real spectrum follows only after this step.",
        ),
        ProgramPiece(
            piece_id="HP-S2",
            layer="realization",
            statement="Control the spectrum (discrete / continuous / multiplicities).",
            independently_tackleable=False,
            blocked_on=("HP-S1",),
            status="blocked",
            evidence_note="Self-adjointness gives real spectrum, not the zeros.",
        ),
        ProgramPiece(
            piece_id="HP-S3",
            layer="realization",
            statement=(
                "Match the Weyl / counting function to "
                "N(T) = (T/2π) log(T/2πe) + S(T) + O(1)."
            ),
            independently_tackleable=False,
            blocked_on=("HP-S2",),
            status="blocked",
            evidence_note="Necessary and far from sufficient. Many operators share a Weyl term.",
        ),
        ProgramPiece(
            piece_id="HP-T1",
            layer="trace",
            statement=(
                "Weil explicit formula is already a theorem relating zeros to primes. "
                "Record it in E; do not rename it as H."
            ),
            independently_tackleable=True,
            blocked_on=(),
            status="theorem",
            evidence_note="Standard analytic number theory. Not a Hamiltonian.",
        ),
        ProgramPiece(
            piece_id="HP-T2",
            layer="trace",
            statement=(
                "Identify primes as periodic orbits of an independent dynamical "
                "system, then derive the explicit formula from Tr f(H)."
            ),
            independently_tackleable=False,
            blocked_on=("HP-S0", "HP-S1"),
            status="blocked",
            evidence_note="This is the Gutzwiller / Selberg reading of Weil.",
        ),
        ProgramPiece(
            piece_id="HP-S5",
            layer="realization",
            statement=(
                "Prove the spectral identity: E is an eigenvalue iff "
                "ζ(1/2 + iE) = 0, with matching multiplicity; or equivalently "
                "ξ(s) equals a proven entire factor times det((s−1/2)/i − H)."
            ),
            independently_tackleable=False,
            blocked_on=("HP-S1", "HP-T2"),
            status="blocked",
            evidence_note="This step is RH, given self-adjointness.",
        ),
        ProgramPiece(
            piece_id="HP-G1",
            layer="statistics",
            statement=(
                "GUE pair correlation / spacing statistics. Treat as a "
                "corollary of a chaotic, time-reversal-breaking H, or as "
                "numerical evidence of a universality class."
            ),
            independently_tackleable=True,
            blocked_on=(),
            status="conjecture_plus_numerics",
            evidence_note="Cannot substitute for HP-S5. Universality is not identity.",
        ),
        ProgramPiece(
            piece_id="HP-D1",
            layer="evolution",
            statement=(
                "Schrödinger evolution e^{-iHt} exists once H is self-adjoint. "
                "Dynamics do not construct H."
            ),
            independently_tackleable=False,
            blocked_on=("HP-S1",),
            status="blocked",
            evidence_note="DHFA layer is determined by H; it is not an extra route to RH.",
        ),
        ProgramPiece(
            piece_id="HP-F1",
            layer="forbidden",
            statement=(
                "Refuse Φ := zeros, λ := {γ_n}, or H := diag(γ_n) as a "
                "definition of the instance."
            ),
            independently_tackleable=True,
            blocked_on=(),
            status="enforced",
            evidence_note="Circular fills are recorded as nulls, not as candidates.",
        ),
    )


def historical_candidates() -> tuple[CandidateRecord, ...]:
    """Published or tautological fills. Distinct formulas stay distinct."""
    return (
        CandidateRecord(
            candidate_id="unspecified",
            formula="H unspecified",
            hamiltonian_independent_of_zeros=False,
            supplies_pieces=(),
            missing_pieces=_all_construction_pieces(),
            circular=False,
            notes="Empty instance. The program is not started.",
        ),
        CandidateRecord(
            candidate_id="target-identity",
            formula="Φ_target := spec(H) = {γ_n}  (claimed, not filled)",
            hamiltonian_independent_of_zeros=False,
            supplies_pieces=(),
            missing_pieces=_all_construction_pieces(),
            circular=True,
            notes=(
                "This is the hoped-for identity written in role language. "
                "Recording it does not instantiate H."
            ),
        ),
        CandidateRecord(
            candidate_id="diagonal-zeros",
            formula="H = diag(γ_n) on ℓ²",
            hamiltonian_independent_of_zeros=False,
            supplies_pieces=(),
            missing_pieces=_all_construction_pieces(),
            circular=True,
            notes=DIAGONAL_ZEROS_WARNING,
        ),
        CandidateRecord(
            candidate_id="berry-keating",
            formula="H = xp (or (xp + px)/2) with a phase-space cutoff",
            hamiltonian_independent_of_zeros=True,
            supplies_pieces=("HP-S0", "HP-U1"),
            missing_pieces=(
                "HP-U3",
                "HP-S1",
                "HP-S2",
                "HP-S3",
                "HP-T2",
                "HP-S5",
            ),
            circular=False,
            notes=(
                "Independent classical symbol. Quantization is not essentially "
                "self-adjoint in a unique way; the cutoff is extra structure "
                "in P or E; eigenvalues are not identified with {γ_n}."
            ),
        ),
        CandidateRecord(
            candidate_id="connes",
            formula=(
                "adelic absorption-spectrum construction (missing lines of an "
                "operator on adeles)"
            ),
            hamiltonian_independent_of_zeros=True,
            supplies_pieces=("HP-U1", "HP-T1"),
            missing_pieces=("HP-S1", "HP-S2", "HP-S5"),
            circular=False,
            notes=(
                "Distinct from Berry–Keating: absorption rather than emission. "
                "Does not supply a compact self-adjoint H with point spectrum {γ_n}."
            ),
        ),
        CandidateRecord(
            candidate_id="polya-1914",
            formula=(
                "RH iff all eigenvalues of a physical problem are real, "
                "given a connection of Ξ zeros to that problem (Pólya 1914/1982)"
            ),
            hamiltonian_independent_of_zeros=False,
            supplies_pieces=(),
            missing_pieces=_all_construction_pieces(),
            circular=False,
            notes=(
                "Documented origin of Pólya’s remark (Odlyzko letter 3 Jan 1982). "
                "A conditional physical reason, not an independently specified H. "
                "Weaker than spec(H)={γ_n}."
            ),
        ),
        CandidateRecord(
            candidate_id="montgomery-gue",
            formula="pair correlation of zeros matches GUE",
            hamiltonian_independent_of_zeros=False,
            supplies_pieces=("HP-G1",),
            missing_pieces=_all_construction_pieces(),
            circular=False,
            notes=GUE_NOT_IDENTITY_WARNING,
        ),
        CandidateRecord(
            candidate_id="weil-explicit",
            formula="Weil explicit formula (zeros ↔ primes)",
            hamiltonian_independent_of_zeros=False,
            supplies_pieces=("HP-T1",),
            missing_pieces=_all_construction_pieces(),
            circular=False,
            notes=(
                "A theorem about ζ, already in E. It is the target trace "
                "identity, not an independent dynamical system."
            ),
        ),
    )


def _all_construction_pieces() -> tuple[str, ...]:
    return (
        "HP-U1",
        "HP-U2",
        "HP-U3",
        "HP-S0",
        "HP-S1",
        "HP-S2",
        "HP-S3",
        "HP-T2",
        "HP-S5",
    )


def mentions_zeros(text: str) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in _ZERO_PHRASES)


def _is_diagonal_zeros(formula: str) -> bool:
    lowered = formula.lower()
    return "diag" in lowered and ("gamma" in lowered or "γ" in formula)


def hamiltonian_is_independent(formula: str) -> bool:
    """True only for an operator formula that is not defined by the zeros.

    Theorems about zeros (Weil, pair correlation) are not Hamiltonians.
    """
    compact = " ".join(formula.split()).strip()
    if not compact:
        return False
    lowered = compact.lower()
    if lowered in {"h unspecified", "unspecified", "missing", "unknown", "none"}:
        return False
    if any(
        phrase in lowered
        for phrase in (
            "explicit formula",
            "pair correlation",
            "functional equation",
            "physical problem are real",
            "physical-reason remark",
        )
    ):
        return False
    if mentions_zeros(compact) or _is_diagonal_zeros(compact):
        return False
    if "φ_target" in lowered or "phi_target" in lowered:
        return False
    return True


def is_circular_fill(
    *,
    hamiltonian: str = "",
    realized_output: str = "",
    scale_role: str = "",
) -> bool:
    """Φ, λ, or H *identified with* the zeros without an independent operator.

    Mentioning zeros inside a theorem (Weil, GUE) is not a circular fill.
    """
    if hamiltonian_is_independent(hamiltonian):
        return False
    if _is_diagonal_zeros(hamiltonian):
        return True
    lowered_h = hamiltonian.lower()
    if "φ_target" in lowered_h or "phi_target" in lowered_h:
        return True
    if mentions_zeros(realized_output) or mentions_zeros(scale_role):
        return True
    return False


def gue_is_not_riemann_spectrum(
    *,
    seed: int = 0,
    n: int = 24,
) -> dict[str, Any]:
    """A frozen GUE matrix can look locally GUE and still not be the zeros.

    This is a negative laboratory: statistics ⇏ spectral identity.
    It does not estimate a probability that RH is true or false.
    """
    rng = np.random.default_rng(seed)
    gaussian = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    hermitian = (gaussian + gaussian.conj().T) / 2.0
    eigs = np.sort(np.linalg.eigvalsh(hermitian))
    gammas = np.asarray(FIRST_RIEMANN_GAMMAS, dtype=float)
    k = gammas.size
    x = eigs[:k]
    design = np.column_stack([x, np.ones(k)])
    coef, *_ = np.linalg.lstsq(design, gammas, rcond=None)
    fitted = design @ coef
    residual = float(np.linalg.norm(fitted - gammas) / np.linalg.norm(gammas))
    spacings = np.diff(eigs)
    mean_sp = float(np.mean(spacings))
    unfolded = spacings / mean_sp
    # Wigner-surmise GUE density at the mean spacing s=1, for a scale check only.
    wigner_at_one = (32.0 / np.pi**2) * np.exp(-4.0 / np.pi)
    identity_threshold = 1e-8
    return {
        "n": n,
        "seed": seed,
        "affine_residual_to_first_gammas": residual,
        "identity_threshold": identity_threshold,
        "is_riemann_spectrum": residual < identity_threshold,
        "mean_unfolded_spacing": float(np.mean(unfolded)),
        "wigner_gue_density_at_s1": wigner_at_one,
        "conclusion": (
            "Best affine map of this GUE spectrum onto the first Riemann "
            "γ_n still has a large residual. GUE-class statistics are "
            "compatible with operators that are not the zeta operator."
        ),
    }


def riemann_mean_spacing(height: np.ndarray | float) -> np.ndarray:
    """Leading local spacing 2π / log(T/2π) from the von Mangoldt density."""
    t = np.asarray(height, dtype=float)
    return 2.0 * np.pi / np.log(t / (2.0 * np.pi))


def riemann_von_mangoldt_leading(height: np.ndarray | float) -> np.ndarray:
    """Leading term (T/2π)(log(T/2π) − 1). Not a substitute for S(T)."""
    t = np.asarray(height, dtype=float)
    return (t / (2.0 * np.pi)) * (np.log(t / (2.0 * np.pi)) - 1.0)


def weyl_law_screen(
    heights: tuple[float, ...] = (20.0, 100.0, 1000.0, 100_000.0),
) -> dict[str, Any]:
    """Reject Hamiltonians whose counting function cannot match N(T).

    This is a filter on candidates, not a construction of H and not RH.
    The quantum harmonic oscillator shares Hermite polynomials with GUE
    and with Jensen(ξ), but its levels are equally spaced. Riemann spacings
    shrink like 1/log T. Classical xp has the same leading density as N(T).
    """
    t = np.asarray(heights, dtype=float)
    if np.any(t <= 2.0 * np.pi):
        raise ValueError("heights must exceed 2π so the leading log is positive")
    spacing_zeta = riemann_mean_spacing(t)
    spacing_oscillator = np.ones_like(t)
    spacing_ratio_zeta = float(spacing_zeta[-1] / spacing_zeta[0])
    spacing_ratio_oscillator = float(spacing_oscillator[-1] / spacing_oscillator[0])
    n_zeta = riemann_von_mangoldt_leading(t)
    n_xp = n_zeta.copy()
    oscillator_rejected = spacing_ratio_zeta < 0.5 and spacing_ratio_oscillator > 0.99
    return {
        "heights_T": t.tolist(),
        "riemann_mean_spacing": spacing_zeta.tolist(),
        "oscillator_mean_spacing": spacing_oscillator.tolist(),
        "spacing_ratio_high_over_low_riemann": spacing_ratio_zeta,
        "spacing_ratio_high_over_low_oscillator": spacing_ratio_oscillator,
        "N_riemann_leading": n_zeta.tolist(),
        "N_xp_classical_leading": n_xp.tolist(),
        "oscillator_rejected": oscillator_rejected,
        "xp_classical_leading_term_compatible": True,
        "hermite_is_not_the_hamiltonian": True,
        "conclusion": (
            "Harmonic-oscillator / equal-spacing spectra are rejected by "
            "N(T): Riemann mean gaps shrink like 1/log T, oscillator gaps "
            "do not. Hermite polynomials in GUE and in Jensen(ξ) are a "
            "special-function collision, not evidence that H is the oscillator. "
            "Classical xp matches the leading von Mangoldt term; that is "
            "compatibility of a Weyl term, not spec(H) = {γ_n}."
        ),
    }


def _piece_payloads(
    supplied: Iterable[str],
    candidate_status_overrides: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    supplied_set = set(supplied)
    overrides = candidate_status_overrides or {}
    rows: list[dict[str, Any]] = []
    for piece in program_pieces():
        row = asdict(piece)
        row["blocked_on"] = list(piece.blocked_on)
        if piece.piece_id in supplied_set and piece.status in {
            "missing",
            "open",
            "blocked",
        }:
            row["status"] = "supplied_by_candidate"
        if piece.piece_id in overrides:
            row["status"] = overrides[piece.piece_id]
        rows.append(row)
    return rows


def _missing_for_proof(candidate: CandidateRecord) -> list[str]:
    required = [
        p.piece_id
        for p in program_pieces()
        if p.layer in {"UHF", "realization", "trace"}
        and p.piece_id not in {"HP-T1", "HP-F1"}
        and p.status != "theorem"
    ]
    supplied = set(candidate.supplies_pieces)
    return [pid for pid in required if pid not in supplied]


def audit_candidate(candidate_id: str = "unspecified") -> HilbertPolyaAudit:
    table = {c.candidate_id: c for c in historical_candidates()}
    if candidate_id not in table:
        raise KeyError(
            f"unknown Hilbert–Pólya candidate {candidate_id!r}; "
            f"known: {sorted(table)}"
        )
    candidate = table[candidate_id]
    return audit_instance(
        instance_name=candidate.candidate_id,
        hamiltonian=candidate.formula,
        realized_output=(
            "spec(H) claimed equal to {γ_n}"
            if candidate.circular
            else "spectral data of the candidate operator"
        ),
        scale_role="eigenvalue E_n",
        supplied_pieces=candidate.supplies_pieces,
        candidate_notes=candidate.notes,
        include_gue_lab=(candidate_id == "montgomery-gue"),
    )


def audit_instance(
    *,
    instance_name: str,
    hamiltonian: str = "",
    realized_output: str = "",
    scale_role: str = "",
    permission: str = "",
    supplied_pieces: Sequence[str] = (),
    candidate_notes: str = "",
    include_gue_lab: bool = False,
) -> HilbertPolyaAudit:
    """Audit one attempted fill of the Hilbert–Pólya program."""
    warnings: list[str] = []
    notes: list[str] = [PROGRAM_SCOPE]
    circular = is_circular_fill(
        hamiltonian=hamiltonian,
        realized_output=realized_output,
        scale_role=scale_role,
    )
    independent = hamiltonian_is_independent(hamiltonian)
    if circular:
        warnings.append(CIRCULAR_ASSIGNMENT_WARNING)
        if "diag" in hamiltonian.lower():
            warnings.append(DIAGONAL_ZEROS_WARNING)
    if not independent:
        warnings.append(
            "H is not independently specified. The realization layer is empty."
        )
    if include_gue_lab or "gue" in instance_name.lower() or "montgomery" in instance_name.lower():
        warnings.append(GUE_NOT_IDENTITY_WARNING)

    roles = []
    for role in core_role_map():
        occupant = role.target_occupant
        status = role.status
        indep = role.independent_of_zeros
        if role.role == "H":
            occupant = hamiltonian or role.target_occupant
            indep = independent
            status = "specified" if independent else (
                "circular" if circular else "missing"
            )
        elif role.role == "P" and permission:
            occupant = permission
            status = "declared"
            indep = not mentions_zeros(permission)
        elif role.role == "Φ":
            occupant = realized_output or role.target_occupant
            if circular and mentions_zeros(realized_output):
                status = "circular_target"
                indep = False
        elif role.role == "λ":
            occupant = scale_role or role.target_occupant
            if circular and mentions_zeros(scale_role):
                status = "circular_target"
                indep = False
        roles.append(
            CoreRoleOccupant(
                role=role.role,
                role_name=role.role_name,
                target_occupant=occupant,
                independent_of_zeros=indep,
                status=status,
                notes=role.notes,
                scale_subtype=role.scale_subtype,
            )
        )

    supplied = list(supplied_pieces)
    if independent and "HP-S0" not in supplied:
        supplied.append("HP-S0")
    pieces = _piece_payloads(supplied)
    dummy = CandidateRecord(
        candidate_id=instance_name,
        formula=hamiltonian,
        hamiltonian_independent_of_zeros=independent,
        supplies_pieces=tuple(supplied),
        missing_pieces=(),
        circular=circular,
        notes=candidate_notes,
    )
    missing = _missing_for_proof(dummy)
    complete = (not circular) and independent and not missing
    if candidate_notes:
        notes.append(candidate_notes)
    notes.append(
        "Extra independently necessary structures in E: "
        + "; ".join(extra_structures())
    )
    notes.append(
        "The five-role map is classification (evidence Level 0). The GUE "
        "laboratory, when present, is Level 1 negative evidence that a "
        "random GUE matrix is not {γ_n}. Neither discovers a Hamiltonian "
        "nor claims RH."
    )

    protocol = freeze_protocol(
        {
            "program": "hilbert-polya",
            "instance": instance_name,
            "hamiltonian": hamiltonian,
            "pieces": [p.piece_id for p in program_pieces()],
            "forbid_circular_fills": True,
            "gue_is_not_identity": True,
        }
    )

    gue_lab = gue_is_not_riemann_spectrum() if include_gue_lab else None
    evidence = int(EvidenceLevel.COHERENT_CLASSIFICATION)
    if include_gue_lab and gue_lab is not None and not gue_lab["is_riemann_spectrum"]:
        evidence = int(EvidenceLevel.MATHEMATICAL_COMPATIBILITY)

    return HilbertPolyaAudit(
        instance_name=instance_name,
        core_roles=roles,
        pieces=pieces,
        circular=circular,
        complete=complete,
        missing_piece_ids=missing,
        highest_evidence_level=evidence,
        hilbert_polya_status=HILBERT_POLYA_STATUS if not complete else (
            "complete candidate recorded; RH still requires checked proofs of "
            "self-adjointness and spectral identity"
        ),
        rh_status=RH_STATUS,
        warnings=list(dict.fromkeys(warnings)),
        notes=notes,
        protocol_hash=protocol.protocol_hash,
        gue_laboratory=gue_lab,
    )


def default_program_audit() -> HilbertPolyaAudit:
    """Empty program plus the target identity, with GUE negative laboratory."""
    audit = audit_candidate("target-identity")
    audit.gue_laboratory = gue_is_not_riemann_spectrum()
    audit.warnings = list(
        dict.fromkeys(audit.warnings + [GUE_NOT_IDENTITY_WARNING])
    )
    if not audit.gue_laboratory["is_riemann_spectrum"]:
        audit.highest_evidence_level = max(
            audit.highest_evidence_level,
            int(EvidenceLevel.MATHEMATICAL_COMPATIBILITY),
        )
    return audit


def looks_like_hilbert_polya(expression: str) -> bool:
    text = expression.lower().replace("ó", "o").replace("ö", "o")
    compact = text.replace(" ", "")
    if "h=xp" in compact or "xp+px" in compact:
        return True
    if "hilbert" in text and "polya" in text:
        return True
    if "riemann" in text and (
        "zero" in text or "hypothesis" in text or "hamiltonian" in text
    ):
        return True
    if "zeta" in text and "zero" in text:
        return True
    return False


def list_candidate_ids() -> list[str]:
    return [c.candidate_id for c in historical_candidates()]
