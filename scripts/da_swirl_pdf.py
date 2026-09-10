#!/usr/bin/env python3
"""Build the swirl map PDF. A map, not a proof."""

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
            "Simons  —  Swirl leftover (a map, not a proof)",
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


def body(pdf: Paper, text: str, size: float = 11) -> None:
    pdf.set_font("Serif", "", size)
    _reset(pdf)
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
    pdf.set_x(pdf.l_margin + 8)
    pdf.multi_cell(pdf.epw - 16, 5.6, text, align="C")
    pdf.ln(2)
    _reset(pdf)


def build() -> Path:
    pdf = _pdf()

    def center(size: float, text: str, h: float, bold: bool = False) -> None:
        if bold:
            pdf.set_font("Serif", "B", size)
        else:
            pdf.set_font("Serif", "", size)
        _reset(pdf)
        pdf.multi_cell(pdf.epw, h, text, align="C")
        _reset(pdf)

    center(16, "Swirl, alignment, and the leftover in", 8, bold=True)
    center(16, "three-dimensional Navier–Stokes", 8, bold=True)
    pdf.ln(1)
    pdf.set_font("SerifI", "", 12)
    _reset(pdf)
    pdf.multi_cell(pdf.epw, 6, "A map, not a proof", align="C")
    _reset(pdf)
    pdf.ln(4)
    center(12, "Jonathan Robert Simons", 6)
    pdf.set_font("SerifI", "", 11)
    _reset(pdf)
    pdf.multi_cell(pdf.epw, 5.5, "Prime Field Technologies", align="C")
    _reset(pdf)
    pdf.multi_cell(pdf.epw, 5.5, "10 September 2026", align="C")
    _reset(pdf)
    pdf.ln(4)

    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.cell(0, 6, "Abstract", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    italic(
        pdf,
        "The geometric swirl leftover after Constantin–Fefferman (1993) and "
        "Beirão da Veiga–Berselli (2002) is recorded. Alignment of vorticity "
        "direction at Lipschitz scale, and then at Hölder exponent 1/2, is a "
        "theorem as an if. The pairs those papers refused remain. This note "
        "names the missing local bound WRITE (6) and does not prove it. A "
        "forced finite-time construction with a smooth external force, "
        "announced 8 September 2026, addresses a different official statement "
        "(Fefferman (C)/(D)) from unforced regularity ((A)/(B)). It is not "
        "WRITE (6). A separate note records global regularity for a "
        "Ladyzhenskaya / p-Laplacian augmentation; that is a different equation.",
    )

    heading(pdf, "1.  What swirl is, in this note")
    body(
        pdf,
        "Let u be a divergence-free velocity in three dimensions, ω = curl u, "
        "ξ = ω/|ω| off the zero set, and φ(x,y) the angle between ξ(x) and "
        "ξ(y). Vortex stretching is a principal-value integral of a geometric "
        "factor D times |ω(y)| / |x−y|³, with |D| at most a constant times "
        "|sin φ|. Local enstrophy on a cutoff supported in a ball of radius r "
        "has stretching on the right and ν ∫ |grad ω|² φ on the left. This is the "
        "classical unaugmented equation. No extra stress. No Φ-cancel of the "
        "axisymmetric tube source.",
    )

    heading(pdf, "2.  The cut that sits, as an if")
    body(
        pdf,
        "Constantin–Fefferman (1993): if |sin φ| is at most Lipschitz in "
        "|x−y| whenever both vorticities are large, the solution is strong. "
        "Beirão da Veiga–Berselli (2002): Hölder exponent 1/2 suffices. "
        "Alignment drops the kernel. Call those pairs Good. The complementary "
        "intense pairs, with |sin φ| larger than C_* |x−y|^{1/2}, are Bad. "
        "Good pairs are their theorem. Bad pairs are the pairs they refused. "
        "Grujić (2009) localizes the condition, not the bad-pair integral. "
        "Later papers weight coherence or assume sparseness. Those are still ifs.",
    )

    heading(pdf, "3.  WRITE (6)")
    body(
        pdf,
        "On a parabolic cylinder Q_r, Bad pairs only, both ends in the local ball:",
    )
    display(
        pdf,
        "A_bad(Q_r)  ≤  (ν/8) ∫∫ |grad ω|² φ  +  C r^{−2} ∫∫ |ω|² .",
    )
    body(
        pdf,
        "The kernel on Bad is still |z|^{−3}. Hardy–Littlewood–Sobolev returns "
        "local E³, the cubic wall. The Hölder cut changes the set, not the "
        "exponent. Assuming the Bad set is thin is the Good-pair theorem again. "
        "Morrey: W^{1,2} does not embed in Hölder 1/2 in three dimensions, so "
        "energy does not empty the Bad set. ν/8 is a conventional slice of "
        "local dissipation, not a sharp constant. Parabolic scaling of the "
        "three terms agrees. There is no dimensional obstruction. There is "
        "also no proof. Aimed leftover: yes. Theorem: no.",
    )

    heading(pdf, "4.  A cylinder still needs more than (6)")
    body(
        pdf,
        "Do not merge the pieces. Good pairs are an if; localizing them leaves "
        "a cutoff error on the annulus. Skin flux at energy level is "
        "Caffarelli–Kohn–Nirenberg as smallness, not as an a priori from finite "
        "energy. Exterior Biot–Savart is not absorbed as r → 0 from energy; "
        "that remainder is why a localization paper exists. If those bounds "
        "and (6) all sit, local Serrin (1962) gives smoothness on a smaller "
        "cylinder. That implication is not Caffarelli–Kohn–Nirenberg. If (6) "
        "sits and skin flux from energy does not, the cylinder is still open. "
        "If the cylinder is already small in the Caffarelli–Kohn–Nirenberg "
        "sense, (6) was not needed on that cylinder. Nečas–Růžička–Šverák "
        "(1996) rules out Leray backward self-similar profiles. It is not a "
        "blanket Type-I theorem.",
    )

    heading(pdf, "5.  A forced vortex is not this leftover")
    body(
        pdf,
        "Fefferman’s official statement has four alternatives. (A) and (B): "
        "unforced, smooth data stay smooth on R³ or on the torus. (C) and (D): "
        "a smooth force is allowed, and one asks for breakdown. On 8 September "
        "2026 a finite-time singularity with a smooth external force was "
        "announced, pictured as a vortex that spirals inward. If that write-up "
        "holds, its slot is (C) or (D). It does not decide (A) or (B). It does "
        "not bound WRITE (6). I did not write that construction. I do not "
        "claim it. This note is a map of the unforced geometric leftover. "
        "The problem those symbols name is 1993. The naming of WRITE (6) in "
        "this form is 10 September 2026.",
    )

    heading(pdf, "6.  What this author claims, and what he does not")
    body(
        pdf,
        "Claims: the map above; a separate write-up of global regularity for "
        "Navier–Stokes plus Ladyzhenskaya / p-Laplacian stress Q1 at ε > 0, "
        "β ≥ 1/2, on the three-torus (this PDE only; known class; cite "
        "Ladyzhenskaya 1968/1969 and Málek–Nečas–Růžička 1996); inverse-GCD "
        "matrix facts posted as Zenodo 22045478, not as the Riemann hypothesis. "
        "Does not claim: ordinary unforced Navier–Stokes; axisymmetric ordinary "
        "NS with swirl as finished; uniform H¹ as ε → 0 for the augmented "
        "equation; WRITE (6) as a theorem; the forced construction of "
        "8 September 2026. Axisymmetric swirl, keeping 1/r⁴: a localized Hardy "
        "inequality does not absorb all data. A Φ-cancel of the tube source "
        "was dropped; it was not the unforced path.",
    )

    heading(pdf, "References")
    refs = [
        "[1]  J. Leray, Acta Math. 63 (1934).",
        "[2]  J. Serrin, Arch. Rational Mech. Anal. 9 (1962).",
        "[3]  L. Caffarelli, R. Kohn, L. Nirenberg, Comm. Pure Appl. Math. 35 (1982), 771–831.",
        "[4]  P. Constantin, C. Fefferman, Indiana Univ. Math. J. 42 (1993), 775–789.",
        "[5]  H. Beirão da Veiga, L. C. Berselli, Diff. Int. Eq. 15 (2002), 345–356.",
        "[6]  J. Nečas, M. Růžička, V. Šverák, Acta Math. 176 (1996).",
        "[7]  L. Escauriaza, G. Seregin, V. Šverák, Uspekhi Mat. Nauk 58 (2003).",
        "[8]  Z. Grujić, Comm. Math. Phys. 290 (2009), 861–870.",
        "[9]  C. L. Fefferman, Existence and smoothness of the Navier–Stokes equation, Clay Mathematics Institute.",
        "[10] O. A. Ladyzhenskaya, The Mathematical Theory of Viscous Incompressible Flow, 1969.",
        "[11] J. Málek, J. Nečas, M. Růžička, Weak and Measure-valued Solutions to Evolutionary PDEs, 1996.",
    ]
    for r in refs:
        body(pdf, r, size=10)

    dest = ROOT / "docs" / "SWIRL-PAPER.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(dest)
    artifact = Path("/opt/cursor/artifacts/assets/swirl-paper.pdf")
    try:
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(dest.read_bytes())
    except OSError:
        pass
    return dest


if __name__ == "__main__":
    path = build()
    print(f"wrote {path}")
