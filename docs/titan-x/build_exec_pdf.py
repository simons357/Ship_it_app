#!/usr/bin/env python3
"""Build TITAN-X Executive Business Plan PDF with full, uncropped images."""

from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.colors import Color, white, black
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    KeepTogether,
    ListFlowable,
    ListItem,
    HRFlowable,
)

ROOT = Path("/workspace")
RENDERS = ROOT / "docs/titan-x/renders"
OUT = ROOT / "TITAN-X-Executive-Business-Plan.pdf"

VOID = Color(7 / 255, 11 / 255, 18 / 255)
PANEL = Color(18 / 255, 28 / 255, 42 / 255)
FOAM = Color(232 / 255, 238 / 255, 246 / 255)
MIST = Color(154 / 255, 173 / 255, 194 / 255)
SKY = Color(91 / 255, 143 / 255, 184 / 255)
SOLAR = Color(201 / 255, 162 / 255, 74 / 255)
LINE = Color(0.55, 0.62, 0.70)


def fit_image(path: Path, max_w: float, max_h: float) -> Image:
    """Contain image fully inside max box — never crop."""
    with PILImage.open(path) as im:
        w, h = im.size
    aspect = w / h
    box_aspect = max_w / max_h
    if aspect > box_aspect:
        draw_w = max_w
        draw_h = max_w / aspect
    else:
        draw_h = max_h
        draw_w = max_h * aspect
    return Image(str(path), width=draw_w, height=draw_h)


def styles():
    ss = getSampleStyleSheet()
    ss.add(
        ParagraphStyle(
            name="Kicker",
            fontName="Helvetica",
            fontSize=8,
            textColor=SOLAR,
            leading=11,
            spaceAfter=8,
        )
    )
    ss.add(
        ParagraphStyle(
            name="Brand",
            fontName="Helvetica-Bold",
            fontSize=42,
            textColor=FOAM,
            leading=46,
            spaceAfter=6,
        )
    )
    ss.add(
        ParagraphStyle(
            name="Tag",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=FOAM,
            leading=18,
            spaceAfter=8,
        )
    )
    ss.add(
        ParagraphStyle(
            name="Lede",
            fontName="Helvetica",
            fontSize=10.5,
            textColor=MIST,
            leading=15,
            spaceAfter=14,
        )
    )
    ss.add(
        ParagraphStyle(
            name="H2",
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=FOAM,
            leading=20,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    ss.add(
        ParagraphStyle(
            name="H3",
            fontName="Helvetica-Bold",
            fontSize=11.5,
            textColor=FOAM,
            leading=15,
            spaceBefore=10,
            spaceAfter=4,
        )
    )
    ss.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=10,
            textColor=FOAM,
            leading=14,
            spaceAfter=7,
        )
    )
    ss.add(
        ParagraphStyle(
            name="Muted",
            fontName="Helvetica",
            fontSize=9,
            textColor=MIST,
            leading=12,
            spaceAfter=6,
        )
    )
    ss.add(
        ParagraphStyle(
            name="Cap",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=MIST,
            leading=11,
            spaceBefore=4,
            spaceAfter=10,
        )
    )
    ss.add(
        ParagraphStyle(
            name="Cell",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=FOAM,
            leading=11,
        )
    )
    ss.add(
        ParagraphStyle(
            name="CellHead",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            textColor=MIST,
            leading=10,
        )
    )
    ss.add(
        ParagraphStyle(
            name="TxBullet",
            fontName="Helvetica",
            fontSize=10,
            textColor=FOAM,
            leading=13,
            leftIndent=12,
            spaceAfter=3,
        )
    )
    return ss


def paint_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(VOID)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    canvas.setFillColor(MIST)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(0.6 * inch, 0.35 * inch, "Prime Field Technologies LLC · TITAN-X Executive Business Plan · August 2026")
    canvas.drawRightString(letter[0] - 0.6 * inch, 0.35 * inch, f"{doc.page}")
    canvas.restoreState()


def table(data, col_widths):
    sty = styles()
    rows = []
    for i, row in enumerate(data):
        style = sty["CellHead"] if i == 0 else sty["Cell"]
        rows.append([Paragraph(str(c), style) for c in row])
    t = Table(rows, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PANEL),
                ("TEXTCOLOR", (0, 0), (-1, -1), FOAM),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def kpi_row(items):
    sty = styles()
    cells = []
    for value, label in items:
        cells.append(
            [
                Paragraph(f"<b>{value}</b>", ParagraphStyle("KpiV", parent=sty["Body"], fontSize=12, textColor=white, leading=14)),
                Paragraph(label, ParagraphStyle("KpiL", parent=sty["Muted"], fontSize=7.5, leading=9)),
            ]
        )
    # flatten to one row of stacked mini tables
    boxes = []
    for value, label in items:
        inner = Table(
            [
                [Paragraph(f"<b>{value}</b>", ParagraphStyle("kv", fontName="Helvetica-Bold", fontSize=11, textColor=white, leading=13))],
                [Paragraph(label, ParagraphStyle("kl", fontName="Helvetica", fontSize=7, textColor=MIST, leading=9))],
            ],
            colWidths=[1.15 * inch],
        )
        inner.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                    ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        boxes.append(inner)
    row = Table([boxes], colWidths=[1.2 * inch] * len(boxes))
    row.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2)]))
    return row


def build():
    sty = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title="TITAN-X Executive Business Plan",
        author="Prime Field Technologies LLC",
    )
    story = []
    usable_w = letter[0] - 1.2 * inch

    # Cover
    story.append(Paragraph("PRIME FIELD TECHNOLOGIES LLC · CONFIDENTIAL DISCUSSION MATERIALS · AUGUST 2026", sty["Kicker"]))
    story.append(Paragraph("TITAN-X", sty["Brand"]))
    story.append(Paragraph("Executive Business Plan · 2026–2030", sty["Tag"]))
    story.append(
        Paragraph(
            "Stratospheric persistent aerial platform for venture capitalists and business owners — regional infrastructure between aircraft and satellites.",
            sty["Lede"],
        )
    )
    story.append(fit_image(RENDERS / "titan-x-wildfire-suppress.jpg", usable_w, 4.55 * inch))
    story.append(
        Paragraph(
            "Firefighting configuration — retardant and water delivery. California is the planning early concentration.",
            sty["Cap"],
        )
    )
    story.append(PageBreak())

    # Disclaimer + summary
    story.append(
        Paragraph(
            "Planning estimates for discussion with qualified parties. Not guarantees of future performance. Not an offer to sell securities.",
            sty["Muted"],
        )
    )
    story.append(Paragraph("1. Executive summary", sty["H2"]))
    story.append(
        Paragraph(
            "<b>TITAN-X</b> is a free-flight stratospheric aerostat with a <b>20,000 lb</b> modular payload, indefinite endurance on helium buoyancy and solar power, and mission reconfiguration by swapping gondolas and underbelly modules.",
            sty["Body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Investment thesis:</b> fund pathfinder → first full-scale hull → California firefighting + metro nodes → planning <b>12-unit</b> fleet by 2030. Pre-positioning converts response from days to hours; civil and commercial utilization underwrites year-round availability; dual-use configs share one cost base.",
            sty["Body"],
        )
    )
    story.append(
        kpi_row(
            [
                ("$13M", "Unit CAPEX (fleet volume)"),
                ("$156M", "12-unit fleet CAPEX"),
                ("$2.4M", "Annual OPEX / unit"),
                ("$200K", "Monthly break-even / unit"),
                ("17.8 : 1", "Planning 10-yr fleet ROI"),
                ("20,000 lb", "Net modular payload"),
            ]
        )
    )

    story.append(Paragraph("2. Platform at a glance", sty["H2"]))
    story.append(
        table(
            [
                ["Parameter", "Value", "Notes"],
                ["Size", "480 ft × 200 ft", "Swept manta planform"],
                ["Net payload", "20,000 lbs", "≈ school-bus weight"],
                ["Altitude range", "500 – 130,000 ft", "Tree-top to lower stratosphere"],
                ["Endurance", "Indefinite", "Solar + buoyancy"],
                ["Ops carbon (persistent)", "Near-zero", "No combustion for loiter"],
                ["Architecture", "Fully modular", "Gondola / underbelly swap"],
            ],
            [2.0 * inch, 1.7 * inch, 2.8 * inch],
        )
    )
    story.append(Paragraph("• Rockoon loft to ~100,000 ft for propellant savings, then recover the platform", sty["TxBullet"]))
    story.append(Paragraph("• Civil, commercial, and defense requirements share the same platform and cost base", sty["TxBullet"]))
    story.append(Spacer(1, 8))
    story.append(fit_image(RENDERS / "titan-x-formation.jpg", usable_w, 3.6 * inch))
    story.append(
        Paragraph(
            "Formation / persistent high-altitude operations — regional pre-positioning on one modular hull family.",
            sty["Cap"],
        )
    )
    story.append(PageBreak())

    story.append(Paragraph("3. Problem &amp; solution", sty["H2"]))
    story.append(
        Paragraph(
            "Wildfire and disaster response still depends on scarce surge aircraft. Satellites persist but cannot deliver mass. Cities need hours-scale airborne nodes for observation, temporary communications, and logistics.",
            sty["Body"],
        )
    )
    story.append(
        Paragraph(
            "<b>TITAN-X fills the band between aircraft and satellites:</b> indefinite loiter, school-bus-class modular payload, near-zero persistent ops carbon, and pre-positioned regional coverage instead of surge-only response.",
            sty["Body"],
        )
    )

    story.append(Paragraph("4. Regional deployment", sty["H2"]))
    story.append(Paragraph("Major cities &amp; high-value regions", sty["H3"]))
    story.append(
        Paragraph(
            "One TITAN-X (or a pair) per region, loaded with modular response packages, on station in hours — disaster response, communications restoration, observation, logistics.",
            sty["Body"],
        )
    )
    story.append(Paragraph("California firefighting concentration", sty["H3"]))
    for b in [
        "Fire-behavior, thermal, and smoke-plume sensors",
        "Retardant or water delivery modules",
        "Incident command and communications packages",
        "Decision-support for incident commanders",
    ]:
        story.append(Paragraph(f"• {b}", sty["TxBullet"]))
    story.append(Paragraph("Modules shift to other missions in lower-risk periods to preserve utilization.", sty["Muted"]))
    story.append(Paragraph("Smaller complementary platforms", sty["H3"]))
    story.append(
        Paragraph(
            "Secondary observation, relay, weather, and lower-cost coverage under full-size regional nodes.",
            sty["Body"],
        )
    )

    story.append(Paragraph("5. Customers &amp; missions", sty["H2"]))
    story.append(
        table(
            [
                ["Segment", "Use"],
                ["State / regional wildfire authorities", "CA firefighting concentration"],
                ["Metro &amp; high-value regions", "Persistent disaster &amp; comms nodes"],
                ["Critical infrastructure", "Monitoring and logistics support"],
                ["Maritime / shipping", "Domain awareness and ship support"],
                ["Public safety", "Airborne threat awareness (low-cost drones)"],
                ["Science / weather", "High-altitude observation"],
                ["Rockoon / launch customers", "Stratospheric loft + recover"],
                ["Dual-use / defense (selected)", "ISR, relay, forward logistics, responsive access"],
            ],
            [3.0 * inch, 3.5 * inch],
        )
    )
    story.append(PageBreak())

    story.append(Paragraph("6. Unit economics", sty["H2"]))
    story.append(
        table(
            [
                ["Item", "Planning value"],
                ["Unit CAPEX (fleet volume)", "$13.0M"],
                ["12-unit fleet CAPEX", "$156M"],
                ["Annual OPEX per unit", "$2.4M"],
                ["Break-even utilization", "~$200K / month"],
                ["Mature utilization target (base)", "$8–12M / unit / year"],
                ["Contribution at $10M rev / $2.4M opex", "~$7.6M / unit / year"],
            ],
            [4.2 * inch, 2.3 * inch],
        )
    )
    story.append(Paragraph("Illustrative mature revenue mix", sty["H3"]))
    story.append(
        table(
            [
                ["Stream", "Share"],
                ["Regional standby / availability", "35–45%"],
                ["Wildfire / disaster mission fees", "20–30%"],
                ["Infrastructure / maritime / public safety", "15–25%"],
                ["Rockoon / science / specialty", "5–15%"],
                ["Dual-use / defense options", "0–20%"],
            ],
            [4.2 * inch, 2.3 * inch],
        )
    )

    story.append(Paragraph("7. Financial plan 2026–2030", sty["H2"]))
    story.append(
        Paragraph(
            "USD millions. Anchored to consolidated summary CAPEX / OPEX / break-even. The planning 17.8 : 1 ten-year fleet ROI is a long-horizon target on the stood-up fleet — not a 2030 cash guarantee.",
            sty["Muted"],
        )
    )
    story.append(Paragraph("Fleet build (base)", sty["H3"]))
    story.append(
        table(
            [
                ["", "2026", "2027", "2028", "2029", "2030"],
                ["Full-size units EOY", "0*", "1", "3", "6", "12"],
                ["CA firefighting-primary", "—", "1", "2", "3", "4"],
                ["Metro / regional nodes", "—", "0", "1", "3", "8"],
            ],
            [2.0 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch],
        )
    )
    story.append(Paragraph("*Pathfinder year — endurance, station-keeping, modular swap validation.", sty["Muted"]))

    story.append(Paragraph("Capital expenditure (base, $M)", sty["H3"]))
    story.append(
        table(
            [
                ["", "2026", "2027", "2028", "2029", "2030", "Total"],
                ["Pathfinder + engineering", "18", "6", "4", "3", "2", "33"],
                ["Hull production (learning curve)", "—", "18", "30", "42", "78", "168"],
                ["Ground / ops infrastructure", "4", "6", "8", "10", "12", "40"],
                ["Total CAPEX", "22", "30", "42", "55", "92", "241"],
            ],
            [2.0 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch],
        )
    )

    story.append(Paragraph("Operating model (base, $M)", sty["H3"]))
    story.append(
        table(
            [
                ["", "2026", "2027", "2028", "2029", "2030"],
                ["Avg units in service", "0", "0.5", "2.0", "4.5", "9.0"],
                ["Revenue", "0.5", "4", "18", "42", "90"],
                ["Direct OPEX", "1.5", "3.5", "7", "13", "24"],
                ["Program / G&amp;A", "4", "5", "7", "9", "11"],
                ["EBITDA (planning)", "(5.0)", "(4.5)", "4", "20", "55"],
            ],
            [2.0 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch],
        )
    )
    story.append(
        Paragraph(
            "2030 check: ~$90M revenue on ~9 average units ≈ <b>$10M per unit-year</b>, above the $2.4M OPEX break-even.",
            sty["Body"],
        )
    )
    story.append(PageBreak())

    story.append(Paragraph("Scenario fan — 2030", sty["H3"]))
    story.append(
        table(
            [
                ["Case", "Units", "Revenue", "EBITDA"],
                ["Conservative", "6", "$45M", "$18M"],
                ["Base", "12", "$90M", "$55M"],
                ["Upside", "12+", "$130M", "$85M"],
            ],
            [1.8 * inch, 1.4 * inch, 1.6 * inch, 1.6 * inch],
        )
    )

    story.append(Paragraph("8. Use of funds &amp; milestones", sty["H2"]))
    story.append(
        table(
            [
                ["Use", "Share"],
                ["Pathfinder + first full-scale hull", "35–45%"],
                ["CA firefighting + first metro modules", "20–30%"],
                ["Production tooling / learning-curve", "15–20%"],
                ["Ops bases, helium, insurance, crew", "10–15%"],
                ["Corporate / BD / compliance", "5–10%"],
            ],
            [4.5 * inch, 2.0 * inch],
        )
    )
    story.append(
        Paragraph(
            "Gate heavy fleet CAPEX on endurance demo, modular swap demo, and first paid availability or mission contract.",
            sty["Body"],
        )
    )

    story.append(Paragraph("9. Risks", sty["H2"]))
    for b in [
        "Airworthiness / airspace — pathfinder before fleet claims",
        "Early unit cost above $13M volume target — learning-curve modeled explicitly",
        "Public contracting cycles — civil commercial utilization underwrites standby",
        "17.8 : 1 ROI is a planning ten-year fleet figure, not a 2026–2030 guarantee",
    ]:
        story.append(Paragraph(f"• {b}", sty["TxBullet"]))

    story.append(Paragraph("10. The ask", sty["H2"]))
    story.append(Paragraph("We are engaging venture capitalists and business owners to fund or co-develop:", sty["Body"]))
    for b in [
        "Pathfinder validation and first full-scale hull",
        "California firefighting concentration as the first revenue-bearing mission stack",
        "Metro pre-positioning nodes that turn TITAN-X into infrastructure",
    ]:
        story.append(Paragraph(f"• {b}", sty["TxBullet"]))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "<font color='#c9a24a'><b>Bottom line.</b></font> Indefinite endurance. 20,000 lb modular payload. Near-zero persistent ops carbon. Pre-positioned regional coverage with a California firefighting emphasis. Dual-use economics on one hull family. <b>2026–2030 builds the twelve-unit base; utilization after that is where the summary ROI lives.</b>",
            sty["Body"],
        )
    )

    doc.build(story, onFirstPage=paint_page, onLaterPages=paint_page)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
