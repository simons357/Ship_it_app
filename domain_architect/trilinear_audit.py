"""Independent Functional Role Analysis of the Gate B trilinear claim.

This module does not invent a proof. It classifies each claimed step,
records the hypothesis it actually uses, and marks unjustified
Cauchy–Schwarz or counting-to-norm leaps as failed tests.

Not (17). NS is not solved. Canonical SFE status remains unresolved.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .schema import (
    CANONICAL_SFE_STATUS,
    EvidenceLevel,
    MathValidationStatus,
    ROLE_GLOSSARY,
)


@dataclass
class InequalityStep:
    step_id: str
    claim: str
    hypotheses: list[str]
    cauchy_schwarz: str | None
    functional_roles: dict[str, str]
    verdict: str
    reason: str
    math_status: str


@dataclass
class TrilinearAudit:
    object_audited: str
    steps: list[InequalityStep]
    board: dict[str, str]
    highest_evidence_level: int
    canonical_sfe_status: str
    theorem_17_proved: bool
    ns_solved: bool
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "object_audited": self.object_audited,
            "steps": [asdict(s) for s in self.steps],
            "board": self.board,
            "highest_evidence_level": self.highest_evidence_level,
            "canonical_sfe_status": self.canonical_sfe_status,
            "theorem_17_proved": self.theorem_17_proved,
            "ns_solved": self.ns_solved,
            "notes": list(self.notes),
        }

    def narrative(self) -> str:
        lines = [
            "Domain Architect — Gate B trilinear inequality audit",
            f"Object: {self.object_audited}",
            "",
        ]
        for step in self.steps:
            lines.append(f"[{step.step_id}] {step.verdict.upper()} — {step.claim}")
            lines.append(f"    {step.reason}")
            if step.cauchy_schwarz:
                lines.append(f"    Cauchy–Schwarz: {step.cauchy_schwarz}")
            lines.append("")
        lines.append("Board:")
        for key, val in self.board.items():
            lines.append(f"  {key}: {val}")
        lines.append("")
        lines.append(f"Canonical SFE status: {self.canonical_sfe_status}.")
        lines.append("Theorem (17) is not claimed. NS is not solved.")
        return "\n".join(lines)


def _roles(**kwargs: str) -> dict[str, str]:
    out = dict(kwargs)
    for key in out:
        if key in ROLE_GLOSSARY and key not in kwargs:
            out[key] = ROLE_GLOSSARY[key]
    return out


def audit_gate_b_trilinear() -> TrilinearAudit:
    """Independent audit of counting, distinct-shell, and every CS use."""
    steps = [
        InequalityStep(
            step_id="G1",
            claim=(
                "Two linearly independent affine planes and a sphere in R^3 "
                "meet in at most two points, at every radius."
            ),
            hypotheses=[
                "normals n1, n2 linearly independent",
                "ambient space R^3 (then Z^3 by restriction)",
            ],
            cauchy_schwarz=None,
            functional_roles=_roles(
                P="admissibility: independent plane constraints",
                g="geometry: Euclidean R^3 / integer lattice",
                λ="scale-response: radius R is a spectral coordinate; the count is radius-independent",
                Φ="realized output: at most two candidate points",
            ),
            verdict="pass",
            reason=(
                "The two planes cut out an affine line. A line meets a "
                "sphere in a quadratic, hence in at most two real points. "
                "No Cauchy–Schwarz is used. This is Euclidean geometry, "
                "not a Navier–Stokes estimate."
            ),
            math_status=MathValidationStatus.PASSED.value,
        ),
        InequalityStep(
            step_id="H-shell",
            claim=(
                "The distinct-shell hypothesis |p|² ≠ |q|² makes the two "
                "plane normals independent."
            ),
            hypotheses=["|p|² ≠ |q|²"],
            cauchy_schwarz=None,
            functional_roles=_roles(
                P="admissibility: distinct squared radii",
                ψ="state: two input wavevectors",
            ),
            verdict="fail",
            reason=(
                "Distinct shells do not imply linear independence. "
                "Counterexample: p=(1,0,0), q=(2,0,0) have |p|²=1 ≠ 4=|q|² "
                "but p ∥ q, so the two radical planes are parallel. The "
                "intersection is then empty, a plane, or inconsistent — "
                "not a uniformly two-point set. The correct extra "
                "hypothesis is linear independence of the wavevectors."
            ),
            math_status=MathValidationStatus.FAILED.value,
        ),
        InequalityStep(
            step_id="G2",
            claim=(
                "For one fixed input vector and two prescribed partner "
                "shells, there are at most two closing lattice vectors, "
                "at arbitrarily large frequency."
            ),
            hypotheses=[
                "p fixed",
                "|q|² = β",
                "|p+q|² = γ",
            ],
            cauchy_schwarz=None,
            functional_roles=_roles(
                P="admissibility: two sphere constraints on q",
                g="geometry: radical plane of two spheres, residual sphere",
                Φ="locus is a circle, not two points",
            ),
            verdict="fail",
            reason=(
                "Two spheres in R^3 intersect in a circle (one radical "
                "plane plus a sphere). Lattice occupancy can exceed two. "
                "Explicit counterexample: p=(0,0,2), β=γ=5 yields four "
                "partners {(±2,0,-1),(0,±2,-1)}. Finite-radius scans "
                "reproduce occupancy well above two. The two-point count "
                "requires a second independent linear constraint, which "
                "this one-input geometry does not supply."
            ),
            math_status=MathValidationStatus.FAILED.value,
        ),
        InequalityStep(
            step_id="G3",
            claim=(
                "For two linearly independent input wavevectors, a common "
                "closer of prescribed radii satisfies two independent "
                "planes and a sphere, hence at most two candidates."
            ),
            hypotheses=[
                "p, q linearly independent (not merely distinct shells)",
                "|r|², |r+p|², |r+q|² prescribed",
            ],
            cauchy_schwarz=None,
            functional_roles=_roles(
                P="admissibility: two radical planes from three spheres",
                g="two-input / two-output common-closer geometry",
                Φ="at most two common closers",
            ),
            verdict="pass",
            reason=(
                "This is G1 applied to the two-input common-closer system. "
                "Finite-radius lattice scans with independent p, q did not "
                "exceed two. This is a counting statement about a different "
                "incidence geometry than Dish #3's one-output Q_x sum."
            ),
            math_status=MathValidationStatus.PASSED.value,
        ),
        InequalityStep(
            step_id="CS-1",
            claim=(
                "Dish #3 energy sharing: ∑_x f_x Q_x ≤ √E (∑_x Q_x²)^{1/2}."
            ),
            hypotheses=[
                "E = ∑_x f_x² < ∞",
                "Q ∈ ℓ²",
                "no sign restriction required for this inequality",
            ],
            cauchy_schwarz=(
                "ℓ² inner product ⟨f, Q⟩ ≤ ||f||_2 ||Q||_2 with "
                "||f||_2 = √E. Used once, on the low index. No inner "
                "sum over partners."
            ),
            functional_roles=_roles(
                ψ="state: shell amplitudes f_x",
                H="interaction: already-assembled Q_x",
                λ="scale-response: none introduced by this step",
                Φ="realized output: T_sc⁺ bound √E ||Q||_2",
            ),
            verdict="pass",
            reason=(
                "Standard Cauchy–Schwarz on ℓ². It is valid for every "
                "real f, Q. It does not use distinct shells, multiplicity, "
                "or nonnegativity. It also does not bound ||Q||_2."
            ),
            math_status=MathValidationStatus.PASSED.value,
        ),
        InequalityStep(
            step_id="CS-2",
            claim=(
                "Inner Cauchy–Schwarz on partners, with Y-charge "
                "f_b ≤ √Y/b, f_c ≤ √Y/c, produces Q_x ≤ (Y/c) "
                "(∑_b C_{xbc}² / b²)^{1/2} and the ρ-face T⁺ ≤ 2 S √E Y."
            ),
            hypotheses=[
                "C_abc ≥ 0 is an upper majorant, not a coercive cost",
                "Y-charge on middle and high legs",
                "diagnostic 1/(2c) factor is not a general-c lemma",
            ],
            cauchy_schwarz=(
                "Second, inner CS: |∑_b C_{xbc} f_b f_c| ≤ f_c "
                "(∑ C²/b²)^{1/2} (∑ b² f_b²)^{1/2} after the Y-weight. "
                "This CS is applied to a different object than CS-1."
            ),
            functional_roles=_roles(
                H="interaction: C-majorant",
                λ="scale-response: Y-charge is a high-frequency weight, not energy",
                Φ="ρ-face remainder S, not ||Q||_2 of Dish #3",
            ),
            verdict="pass_as_upper_bound_on_a_different_object",
            reason=(
                "The inner CS is algebraically valid under the Y-charge. "
                "It changes the object: the resulting S is not ||Q||_2 of "
                "the explicit nonnegative assembly. Reading θ ≈ 0 from S "
                "does not control the Dish #3 power. Equation (16) of the "
                "September 20 note remains an upper bound, not a cost."
            ),
            math_status=MathValidationStatus.PASSED.value,
        ),
        InequalityStep(
            step_id="CS-3",
            claim=(
                "A uniform two-point counting bound on closing vectors "
                "implies a weighted trilinear (or ||Q||_2) inequality "
                "for the nonnegative assembly."
            ),
            hypotheses=[
                "μ ≤ 2 at all radii",
                "the counted incidence graph is the same graph summed in Q_x",
            ],
            cauchy_schwarz=(
                "Would have to be a third CS / Schur bound of the form "
                "||Q||_2² = ∑_x (∑_{yz} C_{xyz} f_y f_z)² ≤ μ ∑ C² f_y² f_z² "
                "or an operator-norm estimate on the incidence graph. "
                "No such identification is supplied."
            ),
            functional_roles=_roles(
                H="interaction: C-weighted triads of Dish #3",
                P="admissibility: would require the Q-sum to run over G3 pairs",
                Φ="claimed: a radius-independent trilinear norm bound",
            ),
            verdict="fail",
            reason=(
                "Counting possible outputs is not a trilinear estimate. "
                "Dish #3 groups by the low shell x, summing C_xyz f_y f_z "
                "over partner shells, not over two-input common closers. "
                "The one-input two-shell locus that does appear in a "
                "single triad is a circle (G2 failed). Even if some other "
                "incidence graph had μ ≤ 2, converting that into "
                "||Q(f)||_2 ≤ K Λ^θ Ω(f) still requires a Cauchy–Schwarz "
                "or Schur step on that graph with the C-weights, and a "
                "proof that C does not reintroduce a positive power of Λ. "
                "That step is missing. Status of the full multiplicity "
                "inequality: gap."
            ),
            math_status=MathValidationStatus.FAILED.value,
        ),
        InequalityStep(
            step_id="LB",
            claim=(
                "For the specified nonnegative Q_x, any uniform power bound "
                "||Q(f)||_2 ≤ K Λ^θ Ω(f) requires θ ≥ 1/2."
            ),
            hypotheses=[
                "Q_x = ∑ C_xyz f_y f_z with C the September 20 majorant ≥ 0",
                "f ≥ 0",
                "similar-triad family: one lattice triad dilated by t, "
                "equal-energy split f_a = f_b = f_c = 1/√3",
            ],
            cauchy_schwarz=(
                "None. Homogeneity: C(t²a, t²b, t²c) = t³ C(a,b,c), "
                "Ω ↦ t² Ω, so ||Q||_2 / Ω scales as t = Λ^{1/2}."
            ),
            functional_roles=_roles(
                H="interaction: nonnegative C-majorant",
                ψ="state: nonnegative shell amplitudes",
                λ="scale-response: dilation t, Λ = t² Λ_0",
                Φ="lower bound θ ≥ 1/2 on every uniform power",
            ),
            verdict="pass",
            reason=(
                "This lower bound does not use all-radii counting, "
                "distinct shells as a two-point theorem, or CS-3. "
                "It is a homogeneity identity on an explicit family, "
                "checked on n = 4, 8, 16, 32 to machine precision and "
                "holding for every dilation t because C is homogeneous "
                "of degree three in t. Optimal θ remains open: the "
                "family saturates 1/2 as a lower bound, not as a uniform "
                "upper bound on overlapping assemblies."
            ),
            math_status=MathValidationStatus.PASSED.value,
        ),
        InequalityStep(
            step_id="PROMOTE",
            claim=(
                "If the all-radii / trilinear audit passes, promote the "
                "Gate B exponent obstruction to a proved result for the "
                "specified nonnegative Q."
            ),
            hypotheses=["CS-3 passes", "G2 or G3 identified with Q_x"],
            cauchy_schwarz="CS-3 is the missing step; it failed.",
            functional_roles=_roles(
                P="admissibility of promotion",
                Φ="program status of Gate B",
            ),
            verdict="split",
            reason=(
                "Promote the obstruction θ ≥ 1/2 by LB (dilation), which "
                "already passed and does not depend on the failed "
                "counting-to-norm link. Do not promote a new all-radii "
                "trilinear upper bound: CS-3 failed. Do not condition LB "
                "on G1. Signed transfer control remains open. (17) remains "
                "open. NS is not solved."
            ),
            math_status=MathValidationStatus.INCONCLUSIVE.value,
        ),
    ]

    board = {
        "Finite-radius multiplicity checks": (
            "Verified, with a circle counterexample: one-input two-shell "
            "occupancy can exceed two"
        ),
        "All-radii geometric counting": (
            "Pass as Euclidean two-plane+sphere; does not bind generic triads"
        ),
        "Distinct-shell hypothesis": (
            "Insufficient; linear independence of wavevectors is required"
        ),
        "Full multiplicity / trilinear inequality": (
            "Gap — counting does not yield the weighted ||Q||_2 bound"
        ),
        "Gate B lower bound (nonnegative Q)": (
            "Proved by similar-triad dilation: θ ≥ 1/2. Not conditional on CS-3"
        ),
        "Optimal exponent": "Open",
        "Signed transfer control": "Open",
        "Gate D dynamical budget": "Measurement campaign; cutoff-independent budget open",
        "Theorem (17)": "Open",
        "Classical unforced 3-D Navier–Stokes": "Open",
    }
    notes = [
        "Agreement between previous agents is not independent validation.",
        "C_abc remains an upper majorant, not a coercive cost.",
        "Gate A remains UNRESOLVED / DIAGNOSTIC ONLY.",
        "This audit is Functional Role Analysis plus explicit geometry. "
        "It is not a Clay / Millennium claim.",
    ]
    return TrilinearAudit(
        object_audited=(
            "Gate B nonnegative Q_x: all-radii counting, distinct-shell "
            "hypothesis, Cauchy–Schwarz chain, and the exponent obstruction"
        ),
        steps=steps,
        board=board,
        highest_evidence_level=int(EvidenceLevel.MATHEMATICAL_COMPATIBILITY),
        canonical_sfe_status=CANONICAL_SFE_STATUS,
        theorem_17_proved=False,
        ns_solved=False,
        notes=notes,
    )
