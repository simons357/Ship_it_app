"""Children of the Hilbert–Pólya / NS / pair-run breakdowns.

Each parent piece splits into independently specifiable children. Refusals
and blocked steps are path guidance for the NS/RH chase, not leftover noise.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


LOOK_SCOPE: str = (
    "Breakdown children. DA splits each parent piece and runs the parseable "
    "ones. What you cannot do is recorded as a guide, not as a dead end."
)


@dataclass(frozen=True)
class ChildPiece:
    child_id: str
    parent_id: str
    chase: str
    statement: str
    status: str
    path_guide: str
    independently_tackleable: bool
    parse: str = ""

    def to_dict(self) -> dict[str, str | bool]:
        return asdict(self)


def breakdown_children() -> list[ChildPiece]:
    return [
        # --- HP-U1 Hilbert space ---
        ChildPiece(
            "HP-U1.a", "HP-U1", "RH",
            "Candidate ℋ = L²(ℝ).",
            "open",
            "You can declare this space without RH. You cannot make it canonical by naming it.",
            True,
        ),
        ChildPiece(
            "HP-U1.b", "HP-U1", "RH",
            "Candidate ℋ for xp with a cutoff (half-line / phase-space window).",
            "open",
            "Cutoff is extra structure. Do not hide it inside H.",
            True,
        ),
        ChildPiece(
            "HP-U1.c", "HP-U1", "RH",
            "Adelic / Connes space (absorption spectrum).",
            "open",
            "A different ℋ from L²(ℝ). Do not merge with Berry–Keating by the letter H.",
            True,
        ),
        ChildPiece(
            "HP-U1.d", "HP-U1", "RH",
            "ℋ = ℓ² with basis labeled by zeros.",
            "forbidden",
            "You cannot choose the space from the zeros. That is a circular fill (HP-F1).",
            True,
        ),
        # --- HP-U2 inner product ---
        ChildPiece(
            "HP-U2.a", "HP-U2", "RH",
            "Inner product / Hilbert-space metric.",
            "open",
            "Changes which operators are self-adjoint. Declare it; do not infer it from GUE.",
            True,
        ),
        ChildPiece(
            "HP-U2.b", "HP-U2", "RH",
            "Units and eigenfunction normalization.",
            "open",
            "Normalization is not a Hamiltonian. Keep it in E.",
            True,
        ),
        # --- HP-U3 domain ---
        ChildPiece(
            "HP-U3.a", "HP-U3", "RH",
            "Deficiency indices of the chosen formula for H.",
            "blocked",
            "You cannot prove essential self-adjointness before HP-S0. Path: pick H first.",
            False,
        ),
        ChildPiece(
            "HP-U3.b", "HP-U3", "RH",
            "Decide whether an xp cutoff is P, ℬ, or extra regularization in E.",
            "open",
            "Three different seats. Do not leave the cutoff unnamed.",
            True,
        ),
        # --- HP-S0 formula for H ---
        ChildPiece(
            "HP-S0.a", "HP-S0", "RH",
            "Berry–Keating candidate H = xp.",
            "incomplete",
            "Independent classical symbol. You can keep searching here. You cannot call it done.",
            True,
            "H = xp",
        ),
        ChildPiece(
            "HP-S0.b", "HP-S0", "RH",
            "Connes adelic absorption spectrum.",
            "incomplete",
            "Different object from xp. You cannot merge HP-S0.a with HP-S0.b.",
            True,
        ),
        ChildPiece(
            "HP-S0.c", "HP-S0", "RH",
            "H = diag(γ_n).",
            "forbidden",
            "You cannot define H from the zeros. Path: drop this fill; it is a null.",
            True,
            "H = diag(gamma)",
        ),
        ChildPiece(
            "HP-S0.d", "HP-S0", "RH",
            "Retired SFE-HAM as Hilbert–Pólya H.",
            "forbidden",
            "You cannot import the inverse-GCD Fock operator as this H. Different book.",
            True,
        ),
        # --- HP-S1 / S2 / S3 / S5 ---
        ChildPiece(
            "HP-S1.a", "HP-S1", "RH",
            "Essential self-adjointness vs a family of extensions.",
            "blocked",
            "You cannot skip this and still claim a unique real spectrum.",
            False,
        ),
        ChildPiece(
            "HP-S2.a", "HP-S2", "RH",
            "Discrete vs continuous spectrum.",
            "blocked",
            "Self-adjointness gives real spectrum, not {γ_n}. Path: do not treat realness as RH.",
            False,
        ),
        ChildPiece(
            "HP-S2.b", "HP-S2", "RH",
            "Multiplicities vs simple zeros.",
            "blocked",
            "You cannot ignore multiplicity. A multiple eigenvalue is not a simple zero.",
            False,
        ),
        ChildPiece(
            "HP-S3.a", "HP-S3", "RH",
            "Leading Weyl term vs N(T).",
            "blocked",
            "Necessary, not sufficient. Path: use it as a filter, not as a proof.",
            False,
            "N = (T/2pi)*log(T)",
        ),
        ChildPiece(
            "HP-S3.b", "HP-S3", "RH",
            "Harmonic oscillator / equal spacing as H.",
            "rejected",
            "You cannot use the oscillator: N(T) kills equal gaps. Path: throw this H out now.",
            True,
        ),
        ChildPiece(
            "HP-S3.c", "HP-S3", "RH",
            "Classical xp leading term vs von Mangoldt.",
            "compatible-not-identity",
            "You may keep xp on the Weyl screen. You cannot promote a leading-term match to spec(H)={γ_n}.",
            True,
        ),
        ChildPiece(
            "HP-S5.a", "HP-S5", "RH",
            "Eigenvalue identity E in spec(H) iff ζ(1/2+iE)=0.",
            "blocked",
            "This child is RH given self-adjointness. You cannot skip it or replace it by GUE.",
            False,
        ),
        ChildPiece(
            "HP-S5.b", "HP-S5", "RH",
            "det identity ξ(s) ∝ det((s−1/2)/i − H) times an entire factor.",
            "blocked",
            "Same prize as HP-S5.a, different packaging. You cannot treat a hoped-for det as H.",
            False,
        ),
        # --- trace / GUE / evolution / forbidden ---
        ChildPiece(
            "HP-T1.a", "HP-T1", "RH",
            "Zeros side of the Weil explicit formula.",
            "theorem",
            "Already proved. Record in E. You cannot rename this side as H.",
            True,
        ),
        ChildPiece(
            "HP-T1.b", "HP-T1", "RH",
            "Primes / geometric side of the Weil explicit formula.",
            "theorem",
            "Already proved. You cannot treat primes as a physical selector P_n.",
            True,
        ),
        ChildPiece(
            "HP-T2.a", "HP-T2", "RH",
            "Primes as periodic orbits of an independent dynamical system.",
            "blocked",
            "Gutzwiller/Selberg reading. You cannot derive this from GUE statistics.",
            False,
        ),
        ChildPiece(
            "HP-G1.a", "HP-G1", "RH",
            "GUE pair correlation as universality class.",
            "conjecture_plus_numerics",
            "You can keep this as HP-G1. You cannot substitute it for HP-S5.",
            True,
        ),
        ChildPiece(
            "HP-D1.a", "HP-D1", "RH",
            "e^{-iHt} once self-adjoint.",
            "blocked",
            "You cannot construct H from dynamics. DHFA is downstream.",
            False,
        ),
        ChildPiece(
            "HP-F1.a", "HP-F1", "RH",
            "Refuse Φ := zeros as a definition.",
            "enforced",
            "Path: keep Φ_target as a claim, never as the instance.",
            True,
        ),
        # --- Laguerre–Pólya / 1926 / Λ route ---
        ChildPiece(
            "LP-0", "HP-H008", "RH",
            "ξ(1/2+iz) in the Laguerre–Pólya class.",
            "open-equivalent-to-RH",
            "Parallel route to Hilbert–Pólya. You cannot prove LP membership by assuming RH.",
            True,
            "xi(s) = xi(1-s)",
        ),
        ChildPiece(
            "LP-1", "HP-H011", "RH",
            "Pólya 1926 hypotheses on Riemann’s Φ.",
            "open",
            "Relocates the gap to a kernel check. You cannot skip the hypotheses.",
            True,
        ),
        ChildPiece(
            "LP-2", "HP-H017", "RH",
            "Is Riemann’s Φ a Pólya frequency function of sufficient order?",
            "open",
            "This is a possible fill of LP-1. It is still not an operator H.",
            True,
        ),
        ChildPiece(
            "LP-3", "HP-H018", "RH",
            "Turán / Jensen hyperbolicity inequalities for ξ without assuming RH.",
            "open",
            "Coefficient tests. Finite-N hyperbolicity is not RH.",
            True,
        ),
        ChildPiece(
            "LP-4", "HP-H014", "RH",
            "Λ ≥ 0 (Rodgers–Tao).",
            "theorem",
            "Done. Path: the remaining inequality is Λ ≤ 0.",
            True,
        ),
        ChildPiece(
            "LP-5", "HP-H014", "RH",
            "Λ ≤ 0 without assuming RH.",
            "open-equivalent-to-RH",
            "You cannot close this by quoting RH. Λ = 0 is the prize.",
            True,
        ),
        ChildPiece(
            "LP-F", "HP-H013", "RH",
            "Pólya Liouville-sum conjecture.",
            "false",
            "You cannot treat every Pólya sentence as a theorem. Drop this from the chase.",
            True,
        ),
        # --- Green / Biot–Savart pair children ---
        ChildPiece(
            "GB-1", "HP-H027", "NS/RH",
            "ΔG = −δ (3D Green kernel).",
            "ran",
            "DA seated G as realized output of a Laplacian and recorded R(κ)=1/κ². Tool, not RH, not Clay NS.",
            True,
            "laplacian(G) = -delta",
        ),
        ChildPiece(
            "GB-2", "NS-H004", "NS/RH",
            "u = ∇ × (−Δ)^{-1} ω (Biot–Savart).",
            "ran",
            "Curl of the inverse Laplacian on vorticity. Shared R(κ) with GB-1. Not smoothness.",
            True,
            "u = curl(invLap * omega)",
        ),
        ChildPiece(
            "GB-3", "NS-H004", "NS",
            "∇·u = 0 follows from u = curl(something).",
            "theorem",
            "Incompressibility is downstream of Biot–Savart. You cannot skip the stretching term by citing this.",
            True,
            "div(u) = 0",
        ),
        ChildPiece(
            "GB-4", "HP-H022", "NS",
            "Pólya walk is recurrent in d=1,2 and transient in d≥3.",
            "theorem",
            "Clay NS is 3D (transient side). 2D NS is globally regular (recurrent side). Dimensional rhyme, not a proof.",
            True,
        ),
        ChildPiece(
            "GB-5", "HP-H027", "NS/RH",
            "Shared scale response R(κ)=1/κ² of Green and Biot–Savart.",
            "looked",
            "You may use this as a common inverse-Laplacian tool. You cannot glue NS to RH with it.",
            True,
        ),
        # --- NS vorticity / KEEP swirl ---
        ChildPiece(
            "NS-B.1", "NS-H001", "NS",
            "Vorticity transport ∂_t ω + (u·∇)ω = (ω·∇)u + νΔω.",
            "open-prize",
            "The Clay PDE. You cannot derive it from ξ or xp.",
            True,
            "partial_t(omega) + (u * nabla)*omega = (omega * nabla)*u + nu * laplacian(omega)",
        ),
        ChildPiece(
            "NS-B.2", "NS-H001", "NS",
            "Stretching term (ω·∇)u.",
            "open",
            "This is the 3D obstruction. You cannot drop it and still be Clay NS.",
            True,
        ),
        ChildPiece(
            "NS-B.3", "NS-H001", "NS",
            "Diffusion νΔω.",
            "theorem-as-term",
            "Heat on vorticity. You cannot identify this with de Bruijn–Newman heat on Ξ.",
            True,
        ),
        ChildPiece(
            "NS-B.4", "NS-H003", "NS",
            "Stokes operator A = −ℙΔ.",
            "open",
            "Spectral sibling of Pólya membranes. You cannot call it Hilbert–Pólya H.",
            True,
        ),
        ChildPiece(
            "NS-Φ.1", "NS-H002", "NS",
            "KEEP algebra r^{-4}∂_z(Γ²)=∂_z(Φ²).",
            "theorem-algebra",
            "You can keep this identity. You cannot call it Clay NS.",
            True,
            "partial_z(Gamma^2)/r^4 = partial_z(Phi^2)",
        ),
        ChildPiece(
            "NS-Φ.2", "NS-H002", "NS",
            "Open barrier ‖u^r/r‖_∞.",
            "open",
            "This is the remaining NS-side condition in the swirl book. Path: estimates here, not RH glue.",
            True,
        ),
        ChildPiece(
            "NS-Φ.3", "NS-H002", "NS/RH",
            "Swirl Φ vs Riemann kernel Φ vs FRA output Φ.",
            "forbidden-merge",
            "You cannot reuse the letter Φ across these three seats. Path: keep three names.",
            True,
        ),
        ChildPiece(
            "NS-T.1", "HP-H025", "NS",
            "Pólya–Szegő rearrangement as a PDE estimate.",
            "tool",
            "You may use it in energy estimates. You cannot quote it as 3D smoothness.",
            True,
        ),
        ChildPiece(
            "NS-F.1", "NS-H001", "NS/RH",
            "Glue NS to RH because both have a spectrum.",
            "forbidden",
            "Shared word ‘spectrum’ is not a transformation. Path: stop this glue.",
            True,
        ),
        ChildPiece(
            "NS-F.2", "NS-H001", "NS",
            "Derive unaugmented NS from SFE / UHF / DHFA.",
            "forbidden",
            "Domain Architect may route between books. It may not derive NS from SFE.",
            True,
        ),
    ]


def path_guides() -> list[str]:
    """Refusals and blocked steps, written as guidance for the NS/RH chase."""
    kids = breakdown_children()
    guides = []
    for child in kids:
        if child.status in {
            "forbidden",
            "rejected",
            "false",
            "forbidden-merge",
            "enforced",
        } or child.path_guide.lower().startswith("you cannot"):
            guides.append(f"{child.child_id}: {child.path_guide}")
    return guides


def runnable_children() -> list[ChildPiece]:
    return [c for c in breakdown_children() if c.parse]


def run_breakdown_children() -> str:
    """Split parent pieces, run parseable children, list path guides."""
    from .audit import audit_expression
    from .schema import CANONICAL_SFE_STATUS, RH_STATUS

    children = breakdown_children()
    by_parent: dict[str, list[ChildPiece]] = {}
    for child in children:
        by_parent.setdefault(child.parent_id, []).append(child)

    lines = [
        "Domain Architect — breakdown children",
        "",
        LOOK_SCOPE,
        f"Parents split: {len(by_parent)}. Children recorded: {len(children)}. "
        f"Parseable children run: {len(runnable_children())}.",
        f"Riemann hypothesis status: {RH_STATUS}.",
        f"Canonical SFE status: {CANONICAL_SFE_STATUS}.",
        "",
        "Path guidance (what you cannot do, and what that points at):",
    ]
    for guide in path_guides():
        lines.append(f"  - {guide}")
    lines.append("")
    lines.append("Children by parent:")
    for parent, kids in by_parent.items():
        lines.append(f"  [{parent}]")
        for child in kids:
            tackle = "now" if child.independently_tackleable else "blocked"
            lines.append(
                f"    {child.child_id} [{child.status}/{tackle}] chase={child.chase}"
            )
            lines.append(f"      {child.statement}")
            lines.append(f"      guide: {child.path_guide}")
    lines.append("")
    lines.append("Parseable children run through the auditor:")
    for child in runnable_children():
        report = audit_expression(child.parse)
        roles = [
            f"{a.get('symbol')}={a.get('candidate_role')}"
            for a in report.role_assignments
        ]
        lines.append(
            f"  {child.child_id}  {child.parse!r}  "
            f"evidence={int(report.highest_evidence_level)}  "
            f"roles={roles or ['none']}  extra={report.extra_structures or 'none'}"
        )
    return "\n".join(lines)
