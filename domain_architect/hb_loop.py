"""HB loop helpers: map → reconstruct → compare (not solve).

These stages match the Domain Architect product definition:

1. Map — functional role inventory for one equation
2. Reconstruct — can the inventory reassemble the known target?
3. Solve/predict — numerical baseline (existing gravity lab / future fluids)
4. Discover — fair experiments only after protocol freeze

Reconstruction here is an inventory / recombination check. It does not
prove Millennium regularity, derive NS from an SFE, or declare new physics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .report import AuditReport
from .schema import EvidenceLevel


STAGE_LABELS = (
    "map",
    "reconstruct",
    "solve_predict",
    "discover",
)

ACHIEVEMENT_LADDER = (
    "classification",  # Level 0
    "compatibility",  # Level 1–2
    "advantage",  # Level 3+
    "new_physics",  # external evidence only
)


@dataclass
class HBMap:
    """Organizational representation H(eq) as role/domain inventory."""

    source_expression: str
    domain_book: str
    roles: dict[str, dict[str, Any]] = field(default_factory=dict)
    extras: list[str] = field(default_factory=list)
    evidence_level: int = 0
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReconstructionCheck:
    """First proof-of-correctness for the mapper: inventory completeness."""

    passed: bool
    kind: str  # inventory | representation_recovery | incomplete
    required_roles: list[str]
    present_roles: list[str]
    missing_roles: list[str]
    missing_extras: list[str]
    recomposed_summary: str
    statement: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CompareReport:
    left: HBMap
    right: HBMap
    shared_roles: list[str]
    only_left: list[str]
    only_right: list[str]
    shared_extras: list[str]
    only_left_extras: list[str]
    only_right_extras: list[str]
    why_not_working: list[str]
    statement: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
            "shared_roles": self.shared_roles,
            "only_left": self.only_left,
            "only_right": self.only_right,
            "shared_extras": self.shared_extras,
            "only_left_extras": self.only_left_extras,
            "only_right_extras": self.only_right_extras,
            "why_not_working": self.why_not_working,
            "statement": self.statement,
        }

    def narrative(self) -> str:
        lines = [
            "Domain Architect — side-by-side HB map compare",
            "",
            "Loop: INPUT → MAP → RECONSTRUCT → EXPERIMENT (discover).",
            "This report is structural comparison only; it does not declare new physics.",
            "",
            f"Left:  {self.left.source_expression}",
            f"  book={self.left.domain_book}  roles={sorted(self.left.roles)}",
            f"Right: {self.right.source_expression}",
            f"  book={self.right.domain_book}  roles={sorted(self.right.roles)}",
            "",
            f"Shared roles: {', '.join(self.shared_roles) or '(none)'}",
            f"Only left:    {', '.join(self.only_left) or '(none)'}",
            f"Only right:   {', '.join(self.only_right) or '(none)'}",
            "",
            f"Shared E: {', '.join(self.shared_extras) or '(none)'}",
            f"Only left E: {', '.join(self.only_left_extras) or '(none)'}",
            f"Only right E: {', '.join(self.only_right_extras) or '(none)'}",
            "",
            self.statement,
        ]
        if self.why_not_working:
            lines.append("")
            lines.append("Why this may not be working / what is missing:")
            for item in self.why_not_working:
                lines.append(f"  - {item}")
        return "\n".join(lines)


# Required organizational inventory by book (Level 0 reconstruction).
BOOK_REQUIREMENTS: dict[str, dict[str, Any]] = {
    "NS-B": {
        "roles": {
            "admissibility",
            "interaction",
            "state",
            "scale_response",
            "realized_output",
            "environment",
        },
        "extras": {
            "incompressibility constraint",
            "initial_conditions",
            "boundary_conditions",
        },
        "recompose": (
            "NS' ≈ {P≈Leray/div-free, H≈advection/stretch, ψ≈u|ω, λ≈ν, "
            "Φ≈p/response; E⊃R³, IC/BC, Biot–Savart}"
        ),
    },
    "gravity-poisson": {
        "roles": {"realized_output", "source", "scale_response"},
        "extras": {"geometry", "boundary"},
        "recompose": "∇²Φ = 4πGρ with spectral R(κ)=1/κ² (κ≠0); P=I recovers Newtonian",
    },
    "generic": {
        "roles": set(),
        "extras": set(),
        "recompose": "No frozen book target; reconstruction withheld",
    },
}


def infer_book(report: AuditReport) -> str:
    joined = " ".join(report.notes + report.warnings).lower()
    if "ns-b" in joined or "navier" in joined:
        return "NS-B"
    if report.recovery_kind or (
        report.poisson_compatibility is not None
    ) or "poisson" in joined:
        return "gravity-poisson"
    return "generic"


def build_hb_map(report: AuditReport) -> HBMap:
    roles: dict[str, dict[str, Any]] = {}
    for item in report.role_assignments:
        role = str(item.get("candidate_role") or "unresolved")
        roles[role] = {
            "symbol": item.get("symbol"),
            "subtype": item.get("subtype"),
            "confidence": item.get("confidence"),
        }
    return HBMap(
        source_expression=report.input_expression,
        domain_book=infer_book(report),
        roles=roles,
        extras=list(report.extra_structures),
        evidence_level=int(report.highest_evidence_level),
        notes=[
            "HB map is an organizational representation, not a solved PDE.",
            "Reconstruction checks inventory fidelity; it does not solve NS.",
        ],
    )


def check_reconstruction(report: AuditReport) -> ReconstructionCheck:
    hb = build_hb_map(report)
    req = BOOK_REQUIREMENTS.get(hb.domain_book, BOOK_REQUIREMENTS["generic"])
    present = set(hb.roles)
    # Treat unresolved-only maps as empty for required roles.
    present_effective = {r for r in present if not r.startswith("unresolved")}
    required = set(req["roles"])
    missing_roles = sorted(required - present_effective)
    extras_l = {e.lower() for e in hb.extras}
    missing_extras = sorted(
        e for e in req["extras"] if e.lower() not in extras_l
    )

    if hb.domain_book == "generic":
        return ReconstructionCheck(
            passed=False,
            kind="incomplete",
            required_roles=sorted(required),
            present_roles=sorted(present_effective),
            missing_roles=missing_roles,
            missing_extras=missing_extras,
            recomposed_summary=req["recompose"],
            statement=(
                "No domain book frozen for this input; cannot run "
                "eq → H(eq) → eq' reconstruction."
            ),
        )

    # Gravity with representation recovery is a stronger reconstruct signal.
    if hb.domain_book == "gravity-poisson" and report.recovery_kind:
        passed = not missing_roles
        return ReconstructionCheck(
            passed=passed,
            kind="representation_recovery" if passed else "incomplete",
            required_roles=sorted(required),
            present_roles=sorted(present_effective),
            missing_roles=missing_roles,
            missing_extras=missing_extras,
            recomposed_summary=req["recompose"],
            statement=(
                "Reconstruction (compatibility): FRA inventory recovers the "
                "known Poisson target as representation, not derivation."
                if passed
                else "Reconstruction incomplete: required gravity roles missing."
            ),
        )

    passed = not missing_roles
    return ReconstructionCheck(
        passed=passed,
        kind="inventory" if passed else "incomplete",
        required_roles=sorted(required),
        present_roles=sorted(present_effective),
        missing_roles=missing_roles,
        missing_extras=missing_extras,
        recomposed_summary=req["recompose"],
        statement=(
            f"Reconstruction inventory check for {hb.domain_book}: "
            + (
                "required roles present. This shows H(eq) faithfully labels "
                "the equation; it does not solve the PDE or prove regularity."
                if passed
                else "missing roles "
                + ", ".join(missing_roles)
                + ". Mapper lost or never assigned structure."
            )
        ),
    )


# Back-compat alias for older imports.
_BOOK_REQUIREMENTS = BOOK_REQUIREMENTS


def compare_reports(left: AuditReport, right: AuditReport) -> CompareReport:
    a = build_hb_map(left)
    b = build_hb_map(right)
    left_roles = {r for r in a.roles if not r.startswith("unresolved")}
    right_roles = {r for r in b.roles if not r.startswith("unresolved")}
    shared = sorted(left_roles & right_roles)
    only_l = sorted(left_roles - right_roles)
    only_r = sorted(right_roles - left_roles)
    left_e = set(a.extras)
    right_e = set(b.extras)
    shared_e = sorted(left_e & right_e)
    only_le = sorted(left_e - right_e)
    only_re = sorted(right_e - left_e)

    why: list[str] = []
    if a.domain_book != b.domain_book:
        why.append(
            f"Different domain books ({a.domain_book} vs {b.domain_book}); "
            "shared letters do not imply shared physics."
        )
    if only_l:
        why.append(f"Left has roles right lacks: {', '.join(only_l)}")
    if only_r:
        why.append(f"Right has roles left lacks: {', '.join(only_r)}")
    if only_le:
        why.append(f"Left records E-structures right lacks: {', '.join(only_le)}")
    if only_re:
        why.append(f"Right records E-structures left lacks: {', '.join(only_re)}")
    if not shared and (left_roles or right_roles):
        why.append(
            "No shared resolved roles — side-by-side compare finds unlike "
            "functional inventories; do not merge by symbol names."
        )
    if not why:
        why.append(
            "Role inventories align at the organizational level; still run "
            "reconstruction and held-out numerical tests before claiming advantage."
        )

    statement = (
        f"Compared H(left) and H(right) under books {a.domain_book} / "
        f"{b.domain_book}. Shared roles={len(shared)}. "
        "This is structural compare (stages map/reconstruct aid), not discovery."
    )
    return CompareReport(
        left=a,
        right=b,
        shared_roles=shared,
        only_left=only_l,
        only_right=only_r,
        shared_extras=shared_e,
        only_left_extras=only_le,
        only_right_extras=only_re,
        why_not_working=why,
        statement=statement,
    )


def attach_loop_to_report(report: AuditReport) -> AuditReport:
    """Populate reconstruction fields on an existing audit report."""
    hb = build_hb_map(report)
    recon = check_reconstruction(report)
    report.hb_map = hb.to_dict()
    report.reconstruction = recon.to_dict()
    report.notes = list(
        dict.fromkeys(
            list(report.notes)
            + [
                "HB loop stages: map → reconstruct → solve/predict → discover.",
                recon.statement,
                f"Recomposed summary: {recon.recomposed_summary}",
                "App assists classification / compatibility / advantage tests; "
                "it cannot declare new physics without external evidence.",
            ]
        )
    )
    if not recon.passed and report.highest_evidence_level > EvidenceLevel.COHERENT_CLASSIFICATION:
        # Do not inflate evidence when reconstruction inventory fails.
        pass
    return report
