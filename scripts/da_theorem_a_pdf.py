#!/usr/bin/env python3
"""Build a regular-paper PDF of sitting Theorem A. This PDE only."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIFBI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"


class Paper(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("SerifI", "", 9)
        self.set_text_color(80, 80, 80)
        self.cell(
            0,
            8,
            "Simons  —  Theorem A, Q1-augmented Navier–Stokes (this PDE only)",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("SerifI", "", 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, str(self.page_no()), align="C")
        self.set_text_color(0, 0, 0)


def _pdf() -> Paper:
    pdf = Paper(format="Letter", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.add_font("Serif", "", SERIF)
    pdf.add_font("Serif", "B", SERIFB)
    pdf.add_font("SerifI", "", SERIFI)
    pdf.add_font("SerifBI", "", SERIFBI)
    pdf.add_page()
    pdf.set_left_margin(22)
    pdf.set_right_margin(22)
    return pdf


def _reset(pdf: Paper) -> None:
    pdf.set_x(pdf.l_margin)


def body(pdf: Paper, text: str, size: float = 11, indent: float = 0) -> None:
    pdf.set_font("Serif", "", size)
    _reset(pdf)
    pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(0, 5.4, text)
    pdf.ln(1.2)
    _reset(pdf)


def italic(pdf: Paper, text: str, size: float = 11) -> None:
    pdf.set_font("SerifI", "", size)
    _reset(pdf)
    pdf.multi_cell(0, 5.4, text)
    pdf.ln(1.2)
    _reset(pdf)


def heading(pdf: Paper, text: str) -> None:
    pdf.ln(3)
    pdf.set_font("Serif", "B", 12.5)
    _reset(pdf)
    pdf.multi_cell(0, 7, text)
    pdf.ln(1.5)
    _reset(pdf)


def display(pdf: Paper, text: str) -> None:
    pdf.ln(1)
    pdf.set_font("Serif", "", 11)
    _reset(pdf)
    pdf.set_x(pdf.l_margin + 10)
    pdf.multi_cell(pdf.epw - 20, 5.6, text, align="C")
    pdf.ln(2)
    _reset(pdf)


def build() -> Path:
    pdf = _pdf()

    def center(family: str, size: float, text: str, h: float) -> None:
        pdf.set_font(family, "B" if family == "Serif" and size >= 16 else "", size)
        if family == "SerifI":
            pdf.set_font("SerifI", "", size)
        elif size >= 16:
            pdf.set_font("Serif", "B", size)
        else:
            pdf.set_font("Serif", "", size)
        _reset(pdf)
        pdf.multi_cell(pdf.epw, h, text, align="C")
        _reset(pdf)

    center("Serif", 16, "Global regularity for the Q1-augmented Navier-Stokes system", 8)
    pdf.ln(1)
    pdf.set_font("SerifI", "", 12)
    _reset(pdf)
    pdf.multi_cell(pdf.epw, 6, "Track A  -  this PDE only", align="C")
    _reset(pdf)
    pdf.ln(4)
    pdf.set_font("Serif", "", 12)
    _reset(pdf)
    pdf.multi_cell(pdf.epw, 6, "Jonathan Robert Simons", align="C")
    _reset(pdf)
    pdf.set_font("SerifI", "", 11)
    _reset(pdf)
    pdf.multi_cell(pdf.epw, 5.5, "Prime Field Technologies", align="C")
    _reset(pdf)
    pdf.multi_cell(pdf.epw, 5.5, "5 September 2026", align="C")
    _reset(pdf)
    pdf.ln(4)

    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.cell(0, 6, "Abstract", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    italic(
        pdf,
        "On the three-torus, the Navier–Stokes equations with an extra "
        "Ladyzhenskaya / p-Laplacian stress (Q1-augmentation, ε > 0, β ≥ 1/2) "
        "admit a unique global smooth solution. This is Theorem A on the "
        "Domain Architect desk. It is a theorem about this equation. It is "
        "not classical three-dimensional Navier–Stokes. The extra dissipation "
        "may be sent to zero only after a separate uniform H¹ bound, which "
        "remains open; even then classical regularity is a further argument "
        "(Track B). The chain records a standard class (Ladyzhenskaya 1968; "
        "Málek–Nečas–Růžička) in Q1 notation.",
    )

    heading(pdf, "1.  The system")
    body(
        pdf,
        "Let ν > 0, ε > 0, α > 0, and β ≥ 1/2. On T³ × [0, ∞) consider",
    )
    display(
        pdf,
        "dt u + (u · grad)u  =  -grad p + ν Δu  +  ε^α  P div( |grad u|^β grad u ) ,    div u = 0,",
    )
    body(
        pdf,
        "with u0 in H¹(T³) divergence-free. Here P is the Leray projector. "
        "Write p = β + 2, so β ≥ 1/2 is p ≥ 5/2. The extra term is the "
        "variational derivative of (1/p) ∫ |grad u|^p. It is not the scalar "
        "-ε^α |grad u|^β Δu.",
    )

    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.multi_cell(0, 6, "Theorem A.")
    _reset(pdf)
    italic(
        pdf,
        "Let ν > 0, ε > 0, α > 0, β ≥ 1/2, and let u0 in H¹(T³) be "
        "divergence-free. The Q1 system has a unique solution",
    )
    display(pdf, "u in C^∞(T³ × (0, ∞))  ∩  L^∞(0, ∞; H¹).")
    italic(
        pdf,
        "No finite-time singularity occurs for this PDE. The data need not "
        "be axisymmetric.",
    )

    heading(pdf, "2.  Proof")
    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.multi_cell(0, 6, "Lemma 1 (Energy).")
    _reset(pdf)
    italic(
        pdf,
        "For a smooth solution,",
    )
    display(
        pdf,
        "½ d/dt ||u||₂²  +  ν ||grad u||₂²  +  ε^α ||grad u||_{L^{β+2}}^{β+2}  =  0.",
    )
    italic(
        pdf,
        "Hence for every T > 0,",
    )
    display(
        pdf,
        "½ ||u(T)||₂² + ν ∫ ||grad u||₂² dt + ε^α ∫ ||grad u||_{L^{β+2}}^{β+2} dt  =  ½ ||u0||₂².",
    )
    body(
        pdf,
        "Proof. Test the equation against u. The convective term and the "
        "pressure vanish: ∫ (u·grad)u · u = ½ ∫ u · grad(|u|²) = 0. The extra "
        "stress gives ∫ P div(|grad u|^β grad u) · u = -∫ |grad u|^{β+2}. The Stokes "
        "term is -ν ||grad u||₂².",
    )

    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.multi_cell(0, 6, "Lemma 2 (Galerkin).")
    _reset(pdf)
    italic(
        pdf,
        "The Galerkin projections onto the first n Stokes eigenfunctions "
        "exist globally. The energy bounds are uniform in n. A subsequence "
        "converges weakly to a weak solution",
    )
    display(
        pdf,
        "u in L^∞(0, ∞; L²) ∩ L²(0, ∞; H¹),    grad u in L^{β+2}(0, ∞; L^{β+2}).",
    )
    body(
        pdf,
        "Proof. Finite-dimensional ODE; the same energy identity holds. "
        "No finite-time blowup of ‖un‖₂. Banach–Alaoglu and Aubin–Lions "
        "pass to the limit. Monotonicity of v |-> div(|grad v|^β grad v) is "
        "Minty–Browder. Details: Málek–Nečas–Růžička, Weak and "
        "Measure-valued Solutions to Evolutionary PDEs, Chapter 5.",
    )

    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.multi_cell(0, 6, "Lemma 3 (Strong solutions, β ≥ 1/2).")
    _reset(pdf)
    italic(
        pdf,
        "The weak solution is unique and lies in L^∞(0, ∞; H¹) ∩ L²(0, ∞; H²). "
        "The constant depends on ε, α, β, ν, ‖u0‖_{H¹} and blows up as ε → 0.",
    )
    body(
        pdf,
        "Proof. For β ≥ 1/2 one has β + 2 ≥ 5/2. Extra integrability of grad u "
        "meets the Ladyzhenskaya p ≥ 5/2 criterion (equivalently a "
        "Ladyzhenskaya–Prodi–Serrin pair built from that integrability). "
        "The extra term produces a monotone remainder that absorbs the "
        "convective difference of two solutions. See Ladyzhenskaya (1968) "
        "and Málek–Nečas–Růžička. This is extra integrability of grad u, not a "
        "geometric cancel, and not a Φ identity.",
    )

    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.multi_cell(0, 6, "Lemma 4 (Bootstrap).")
    _reset(pdf)
    italic(
        pdf,
        "The unique strong solution is C^∞(T³ × (0, ∞)).",
    )
    body(
        pdf,
        "Proof. Frozen ε > 0, the linearized operator is a uniformly elliptic "
        "Stokes operator. Difference quotients give H^k for all k. Sobolev "
        "embedding yields spatial smoothness; time regularity follows from "
        "the equation.",
    )

    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.multi_cell(0, 6, "Proof of Theorem A.")
    _reset(pdf)
    body(
        pdf,
        "Galerkin existence, weak limit, strong uniqueness at β ≥ 1/2, "
        "then the bootstrap.",
    )

    heading(pdf, "3.  What this does not prove")
    body(
        pdf,
        "Uniform H¹ as ε → 0 is not claimed. A decaying Q1 integral is not "
        "that bound. Classical unaugmented Navier–Stokes (Track B: keep 1/r⁴, "
        "no Q1) is not claimed. A => B remains false on this desk. Riemann "
        "zeros, Birch–Swinnerton-Dyer, Hodge, Yang–Mills, and P vs NP are "
        "different objects.",
    )

    heading(pdf, "References")
    body(
        pdf,
        "[1]  O. A. Ladyzhenskaya, The Mathematical Theory of Viscous "
        "Incompressible Flow, Gordon and Breach, 1969 (modified NS: extra "
        "p-Laplacian stress).",
    )
    body(
        pdf,
        "[2]  J. Málek, J. Nečas, M. Růžička, Weak and Measure-valued "
        "Solutions to Evolutionary PDEs, Chapman & Hall, 1996.",
    )

    dest = ROOT / "docs" / "THEOREM-A-Q1.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(dest)
    artifact = Path("/opt/cursor/artifacts/assets/theorem-a-q1.pdf")
    try:
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(dest.read_bytes())
    except OSError:
        pass
    return dest


if __name__ == "__main__":
    path = build()
    print(f"wrote {path}")
