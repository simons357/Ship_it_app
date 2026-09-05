#!/usr/bin/env python3
"""Print the unaugmented NS chain as a paper. WRITE (6) stays open."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"


class Paper(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("SerifI", "", 9)
        self.set_text_color(80, 80, 80)
        self.cell(
            0,
            8,
            "Simons  -  Track B chain  -  WRITE (6) open  -  not QED",
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


def bold_line(pdf: Paper, text: str) -> None:
    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.multi_cell(0, 6, text)
    _reset(pdf)


def build() -> Path:
    pdf = Paper(format="Letter", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.add_font("Serif", "", SERIF)
    pdf.add_font("Serif", "B", SERIFB)
    pdf.add_font("SerifI", "", SERIFI)
    pdf.add_page()
    pdf.set_left_margin(22)
    pdf.set_right_margin(22)

    pdf.set_font("Serif", "B", 16)
    _reset(pdf)
    pdf.multi_cell(
        pdf.epw,
        8,
        "Unaugmented 3D Navier-Stokes: the proof chain",
        align="C",
    )
    _reset(pdf)
    pdf.set_font("SerifI", "", 12)
    pdf.multi_cell(pdf.epw, 6, "Track B  -  WRITE (6) open  -  not QED", align="C")
    _reset(pdf)
    pdf.ln(3)
    pdf.set_font("Serif", "", 12)
    pdf.multi_cell(pdf.epw, 6, "Jonathan Robert Simons", align="C")
    _reset(pdf)
    pdf.set_font("SerifI", "", 11)
    pdf.multi_cell(pdf.epw, 5.5, "Prime Field Technologies", align="C")
    _reset(pdf)
    pdf.multi_cell(pdf.epw, 5.5, "5 September 2026", align="C")
    _reset(pdf)
    pdf.ln(3)

    pdf.set_font("Serif", "B", 11)
    _reset(pdf)
    pdf.cell(0, 6, "Abstract", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    italic(
        pdf,
        "This is the written chain for classical three-dimensional "
        "incompressible Navier-Stokes: no Q1, keep 1/r^4. Lines (1)-(5) "
        "sit. Line (6) does not. Lines (7)-(9) wait on (6). Emitting this "
        "paper is not a close. Theorem A (the Q1-augmented PDE) is a "
        "different equation and is not used here. Check B stays open.",
    )

    heading(pdf, "1.  Aimed theorem  (does not sit)")
    body(
        pdf,
        "Let u be a smooth solution of three-dimensional incompressible "
        "Navier-Stokes (periodic or whole space), viscosity nu > 0, no Q1, "
        "keep 1/r^4. Let X = ||omega||_2^2. Then X stays finite on [0, T] "
        "for arbitrary T, and u remains smooth.",
    )
    italic(
        pdf,
        "That statement is the leftover. It is not a theorem of this desk.",
    )

    heading(pdf, "2.  The leftover form")
    display(
        pdf,
        "d/dt X + nu ||grad omega||_2^2  <=  eps nu ||grad omega||_2^2 "
        "+ C_eps X R(t),     integral_0^T R < infinity.",
    )
    body(
        pdf,
        "The only term that can beat viscosity is the stretching leftover. "
        "F is not this object. The extra Q1 stress is not on this equation.",
    )

    heading(pdf, "3.  Proof chain")
    bold_line(pdf, "(1)  HAVE  -  Energy.")
    body(
        pdf,
        "Leray: integral_0^T X(t) dt < infinity on these packets, and the "
        "energy inequality holds.",
    )
    bold_line(pdf, "(2)  HAVE  -  Enstrophy identity.")
    display(
        pdf,
        "d/dt X + nu ||grad omega||_2^2  =  - integral omega · S omega",
    )
    body(pdf, "up to lower-order terms already controlled.")
    bold_line(pdf, "(3)  HAVE  -  Leftover form.")
    body(
        pdf,
        "Absorb a slice of dissipation to obtain the display in section 2. "
        "The stretching leftover is the only term that can beat viscosity.",
    )
    bold_line(pdf, "(4)  HAVE  -  Split.")
    body(
        pdf,
        "integral omega · S omega = hole 1 (aligned P+ on E_c) + hole 2 "
        "(unaligned P+ on E_c) + hole 3 (off E_c). Scored on the n=32 box "
        "as B37.",
    )
    bold_line(pdf, "(5)  HAVE  -  Named blanks.")
    body(
        pdf,
        "A1 = alignment in time for all data (hole 1). A2 = integral "
        "||lambda_2^+|| for all data (live cubic; Miller cut B38). On this "
        "box A1 is off and A2 is live and did not blow on the B15 path "
        "(B40, B41). Neither integral is known for all data.",
    )
    bold_line(pdf, "(6)  WRITE  -  the leftover.  NOT DONE.")
    italic(
        pdf,
        "One all-data integrable residual: integral_0^T R(t) dt < infinity, "
        "or all-data A1, or all-data A2, or a field that kills the stretching "
        "leftover.",
    )
    bold_line(pdf, "(7)  THEN  -  Gronwall.  Waits on (6).")
    body(pdf, "From (3) and (6), X(t) stays finite on [0, T].")
    bold_line(pdf, "(8)  THEN  -  Continuation.  Waits on (6).")
    body(
        pdf,
        "Beale-Kato-Majda: if integral_0^T ||omega||_infty dt < infinity "
        "then the solution continues. L^2 is not the max.",
    )
    bold_line(pdf, "(9)  THEN  -  Bootstrap.  Waits on (6).")
    body(
        pdf,
        "A bound on X and no blowup of ||omega||_infty upgrades to smoothness "
        "on [0, T]. If T is arbitrary, the solution is globally regular.",
    )
    italic(pdf, "If (6) sits, (7)-(9) close the aimed theorem. (6) does not sit.")

    heading(pdf, "4.  Completion ledger")
    body(pdf, "(1)-(5)  done.")
    body(pdf, "(6)  all-data R / A1 / A2 / killing field  -  not done.")
    body(pdf, "(7)-(9)  Gronwall / continuation / bootstrap  -  waiting on (6).")
    italic(
        pdf,
        "Printing this paper does not change that table. Please-finish-bad "
        "does not change that table. Theorem A does not change that table.",
    )

    heading(pdf, "5.  Candidates for (6)")
    body(pdf, "Classify one:")
    body(pdf, "- all-data alignment in time (A1)")
    body(pdf, "- all-data integral ||lambda_2^+|| (A2)")
    body(pdf, "- a different integrable residual")
    body(pdf, "- a killing field for the stretching leftover")
    body(
        pdf,
        "Do not use Q1, Phi-cancel, a Q-floor, or leftover-close B42. "
        "Do not spawn n=64. Do not cash an n=32 reading as an a priori.",
    )

    dest = ROOT / "docs" / "TRACK-B-CHAIN.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(dest)
    artifact = Path("/opt/cursor/artifacts/assets/track-b-chain.pdf")
    try:
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(dest.read_bytes())
    except OSError:
        pass
    return dest


if __name__ == "__main__":
    print(f"wrote {build()}")
