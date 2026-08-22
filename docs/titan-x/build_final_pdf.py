#!/usr/bin/env python3
"""TITAN-X FINAL Investor Plan — full synthesis of all available source versions + pictures."""

from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.colors import Color, white
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
)

ROOT = Path("/workspace")
RENDERS = ROOT / "docs/titan-x/renders"
OUT = ROOT / "TITAN-X-FINAL-Investor-Plan.pdf"
WEB = ROOT / "titan-x-web"

VOID = Color(7 / 255, 11 / 255, 18 / 255)
PANEL = Color(18 / 255, 28 / 255, 42 / 255)
FOAM = Color(232 / 255, 238 / 255, 246 / 255)
MIST = Color(154 / 255, 173 / 255, 194 / 255)
SOLAR = Color(201 / 255, 162 / 255, 74 / 255)
LINE = Color(0.55, 0.62, 0.70)


def fit_image(path: Path, max_w: float, max_h: float) -> Image:
    with PILImage.open(path) as im:
        w, h = im.size
    aspect = w / h
    box_aspect = max_w / max_h
    if aspect > box_aspect:
        draw_w, draw_h = max_w, max_w / aspect
    else:
        draw_h, draw_w = max_h, max_h * aspect
    return Image(str(path), width=draw_w, height=draw_h)


def crop_to_aspect(src: Path, dest: Path, target_aspect: float) -> Path:
    """Center-crop to a taller frame so cover plates fill the page."""
    with PILImage.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        aspect = w / h
        if aspect > target_aspect:
            new_w = int(h * target_aspect)
            left = (w - new_w) // 2
            im = im.crop((left, 0, left + new_w, h))
        elif aspect < target_aspect:
            new_h = int(w / target_aspect)
            top = max(0, (h - new_h) // 5)
            im = im.crop((0, top, w, min(h, top + new_h)))
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, quality=92)
    return dest


def styles():
    ss = getSampleStyleSheet()

    def add(name, **kw):
        ss.add(ParagraphStyle(name=name, **kw))

    add("Kicker", fontName="Helvetica", fontSize=8, textColor=SOLAR, leading=11, spaceAfter=6)
    add("Brand", fontName="Helvetica-Bold", fontSize=36, textColor=FOAM, leading=40, spaceAfter=4)
    add("Tag", fontName="Helvetica-Bold", fontSize=12, textColor=FOAM, leading=15, spaceAfter=6)
    add("Lede", fontName="Helvetica", fontSize=10, textColor=MIST, leading=14, spaceAfter=8)
    add("H2", fontName="Helvetica-Bold", fontSize=13, textColor=FOAM, leading=16, spaceBefore=8, spaceAfter=5)
    add("H3", fontName="Helvetica-Bold", fontSize=10.5, textColor=FOAM, leading=13, spaceBefore=6, spaceAfter=3)
    add("Body", fontName="Helvetica", fontSize=9, textColor=FOAM, leading=12, spaceAfter=4)
    add("Muted", fontName="Helvetica", fontSize=8, textColor=MIST, leading=10, spaceAfter=4)
    add("Cap", fontName="Helvetica", fontSize=7.5, textColor=MIST, leading=9, spaceBefore=2, spaceAfter=6)
    add("Cell", fontName="Helvetica", fontSize=7.5, textColor=FOAM, leading=9.5)
    add("CellHead", fontName="Helvetica-Bold", fontSize=7, textColor=MIST, leading=9)
    add("TxBullet", fontName="Helvetica", fontSize=9, textColor=FOAM, leading=11.5, leftIndent=10, spaceAfter=1)
    return ss


def paint(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(VOID)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    canvas.setFillColor(MIST)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(0.55 * inch, 0.32 * inch, "Prime Field Technologies LLC · TITAN-X FINAL Investor Plan · August 2026")
    canvas.drawRightString(letter[0] - 0.55 * inch, 0.32 * inch, str(doc.page))
    canvas.restoreState()


def table(data, widths):
    sty = styles()
    rows = []
    for i, row in enumerate(data):
        s = sty["CellHead"] if i == 0 else sty["Cell"]
        rows.append([Paragraph(str(c), s) for c in row])
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PANEL),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def kpi_grid(items, cols=3):
    usable = letter[0] - 1.1 * inch
    gap = 0.06 * inch
    col_w = (usable - gap * (cols - 1)) / cols
    boxes = []
    for value, label in items:
        inner = Table(
            [
                [Paragraph(f"<b>{value}</b>", ParagraphStyle("kv", fontName="Helvetica-Bold", fontSize=10.5, textColor=white, leading=12))],
                [Paragraph(label, ParagraphStyle("kl", fontName="Helvetica", fontSize=7, textColor=MIST, leading=8.5))],
            ],
            colWidths=[col_w - 4],
        )
        inner.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                    ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        boxes.append(inner)
    rows = []
    for i in range(0, len(boxes), cols):
        chunk = boxes[i : i + cols]
        while len(chunk) < cols:
            chunk.append("")
        rows.append(chunk)
    g = Table(rows, colWidths=[col_w] * cols, hAlign="LEFT", spaceBefore=2, spaceAfter=6)
    g.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return g


def bullets(sty, items):
    return [Paragraph(f"• {x}", sty["TxBullet"]) for x in items]


def kt(*items):
    return KeepTogether(list(items))


def plate(path: Path, usable_w: float, max_h: float, caption: str, sty):
    return kt(fit_image(path, usable_w, max_h), Paragraph(caption, sty["Cap"]))


def build():
    sty = styles()
    usable_w = letter[0] - 1.1 * inch
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.48 * inch,
        title="TITAN-X FINAL Investor Plan",
        author="Prime Field Technologies LLC",
    )
    s = []

    # —— COVER ——
    s.append(Paragraph("PRIME FIELD TECHNOLOGIES LLC · FINAL INVESTOR PLAN · AUGUST 2026", sty["Kicker"]))
    s.append(Paragraph("TITAN-X", sty["Brand"]))
    s.append(Paragraph("Stratospheric Persistent Aerial Platform", sty["Tag"]))
    s.append(
        Paragraph(
            "Indefinite-endurance free-flight aerostat. 20,000 lb modular payload. California firefighting first; metro disaster and infrastructure nodes next. Planning estimates for qualified parties. Not an offer to sell securities.",
            sty["Lede"],
        )
    )
    cover = crop_to_aspect(
        RENDERS / "titan-x-wildfire-suppress.jpg",
        Path("/tmp/titan-x-cover-crop.jpg"),
        target_aspect=1.22,
    )
    s.append(plate(cover, usable_w, 6.6 * inch, "California firefighting configuration — retardant + water delivery.", sty))
    s.append(PageBreak())

    # —— 1 EXEC SUMMARY ——
    s.append(Paragraph("1. Executive summary", sty["H2"]))
    s.append(
        Paragraph(
            "TITAN-X is a free-flight stratospheric aerostat in the altitude band between conventional aircraft and satellites. Helium buoyancy plus solar power keep it aloft indefinitely. Gondolas and underbelly modules swap so one hull family serves firefighting, disaster, communications, observation, rockoon loft, and selected dual-use missions.",
            sty["Body"],
        )
    )
    s.append(
        Paragraph(
            "<b>Investment thesis:</b> pathfinder validation → first full-scale hull → California firefighting concentration + metro pre-positioning → planning <b>12-unit</b> fleet by 2030. Pre-positioning converts response from days into hours. Civil utilization underwrites year-round availability; dual-use configurations share the same hull and cost base.",
            sty["Body"],
        )
    )
    s.append(
        kpi_grid(
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

    # —— 2 PLATFORM (technical only — money lives in §1 and §7) ——
    s.append(
        kt(
            Paragraph("2. Platform at a glance", sty["H2"]),
            table(
                [
                    ["Parameter", "Value", "Notes"],
                    ["Size", "480 ft × 200 ft", "Swept manta planform"],
                    ["Net payload", "20,000 lbs", "≈ school-bus weight"],
                    ["Altitude range", "500 – 130,000 ft", "Tree-top to lower stratosphere"],
                    ["Endurance", "Indefinite", "Solar + buoyancy; no combustion for loiter"],
                    ["Architecture", "Fully modular", "Gondola / underbelly module swap"],
                    ["Rockoon loft", "~100,000 ft", "Propellant savings; platform recovers"],
                ],
                [2.1 * inch, 1.7 * inch, 3.0 * inch],
            ),
        )
    )

    s.append(
        kt(
            Paragraph("2.1 Core advantages", sty["H3"]),
            *bullets(
                sty,
                [
                    "Indefinite endurance — solar power is sufficient for continuous station-keeping",
                    "School-bus-class payload with rapid mission-module swap on one hull family",
                    "Near-zero operational carbon for persistent missions",
                    "Rockoon loft plus selected dual-use configs share the civil cost base",
                ],
            ),
        )
    )

    s.append(
        kt(
            Paragraph("2.2 How the system works", sty["H3"]),
            Paragraph(
                "Lift is helium; electric/solar energy covers station-keeping, sensors, and modules. Firefighting tanks one week, communications the next — without a second fleet. The 500–130,000 ft band sits between aircraft sortie economics and satellite persistence.",
                sty["Body"],
            ),
        )
    )

    # —— 3 PROBLEM / MARKET ——
    s.append(
        kt(
            Paragraph("3. Problem and market context", sty["H2"]),
            Paragraph(
                "Wildfire and disaster response still depends on scarce surge aircraft. Assets arrive late; coverage collapses with weather, tanker availability, or basing. Satellites persist but cannot deliver mass. Aircraft deliver mass but cannot loiter indefinitely. Cities need <b>hours-scale</b> airborne nodes — not ad-hoc charter after the event.",
                sty["Body"],
            ),
            Paragraph(
                "<b>Gap:</b> nothing practical today combines indefinite loiter, 20,000 lb modular payload, rapid mission swap, and near-zero persistent ops carbon in the aircraft–satellite band. TITAN-X is persistent aerial <b>infrastructure</b>, not a surge novelty.",
                sty["Body"],
            ),
        )
    )
    s.append(
        kt(
            Paragraph("3.1 Customer / payer segments", sty["H3"]),
            table(
                [
                    ["Segment", "Primary use", "Why TITAN-X"],
                    ["State / regional wildfire authorities", "CA firefighting concentration", "Sensors + retardant/water + incident command on station"],
                    ["Metro / high-value regions", "Disaster &amp; communications nodes", "Hours-scale response vs days"],
                    ["Critical infrastructure operators", "Pipelines, grids, ports, campuses", "Continuous observation + logistics"],
                    ["Maritime / shipping", "Domain awareness, ship support", "Persistent coverage without ship sortie cost"],
                    ["Public safety", "Low-cost drone threat awareness", "Wide-area airborne node"],
                    ["Science / weather", "High-altitude observation", "Long dwell, recoverable platform"],
                    ["Rockoon / launch customers", "Stratospheric loft", "Propellant savings + recovery"],
                    ["Dual-use / defense (selected)", "ISR, relay, forward logistics", "Shared civil cost base"],
                ],
                [2.2 * inch, 2.2 * inch, 2.4 * inch],
            ),
        )
    )

    # —— 4 DEPLOYMENT ——
    s.append(
        kt(
            Paragraph("4. Regional deployment concept", sty["H2"]),
            Paragraph(
                "Preferred model: <b>pre-positioned regional coverage</b>, not centralized surge. Response time drops from days to hours. Civil utilization pays for year-round availability. One modular hull shifts among firefighting, disaster, and infrastructure without separate fleets.",
                sty["Body"],
            ),
            Paragraph("4.1 Major cities and high-value regions", sty["H3"]),
            Paragraph(
                "Each major metro or high-risk region is assigned one TITAN-X (or a small pair), loaded with modular response packages and able to be on station in hours — disaster response, communications restoration, observation, and logistics.",
                sty["Body"],
            ),
        )
    )
    s.append(
        kt(
            Paragraph("4.2 California firefighting concentration", sty["H3"]),
            Paragraph(
                "California is the natural first stack: fire-behavior / thermal / smoke sensors, retardant or water modules, incident-command comms, and decision-support for commanders. Off-season the same hull swaps to metro, infrastructure, or communications packages so the asset is not stranded on a single mission.",
                sty["Body"],
            ),
            Paragraph("4.3 Smaller complementary platforms", sty["H3"]),
            Paragraph(
                "Smaller aerostats cover local observation, relay, weather, and lower-cost regional coverage. Full-size TITAN-X is the primary node; smaller platforms take specialized or lower-intensity tasks.",
                sty["Body"],
            ),
        )
    )

    # —— 5 ROCKOON (missions already listed in 3.1; firefighting CONOPS is 4.2) ——
    s.append(
        kt(
            Paragraph("5. Rockoon and dual-use", sty["H2"]),
            Paragraph(
                "Rockoon loft to ~100,000 ft targets propellant savings for responsive access, with platform recovery after launch. Dual-use defense options (ISR, relay, forward logistics) are selected configurations on the civil hull — not a separate product line — so civil utilization helps carry the cost base.",
                sty["Body"],
            ),
        )
    )

    # —— 6 TECH PATH ——
    s.append(
        kt(
            Paragraph("6. Development path and capital staging", sty["H2"]),
            Paragraph(
                "Capital is staged: <b>pathfinder → first full-scale hull → initial operational units → fleet scale-up</b>. Gate heavy fleet CAPEX on endurance demo, modular swap demo, and first paid availability or mission contract.",
                sty["Body"],
            ),
            table(
                [
                    ["Phase", "Years", "Milestone / exit"],
                    ["A. Pathfinder", "2026", "Endurance, station-keeping, modular swap demonstrated"],
                    ["B. First full-scale hull", "2026–2027", "Operational unit class"],
                    ["C. Initial nodes", "2027–2028", "CA firefighting layer + first metro nodes"],
                    ["D. Fleet scale-up", "2028–2030", "Toward planning 12-unit fleet + complementary platforms"],
                ],
                [1.8 * inch, 1.3 * inch, 3.7 * inch],
            ),
        )
    )

    s.append(Spacer(1, 6))
    s.append(plate(RENDERS / "titan-x-formation.jpg", usable_w, 2.55 * inch, "Regional pre-positioning — one modular hull family, persistent high-altitude operations.", sty))

    # —— 7 UNIT ECONOMICS ——
    s.append(
        kt(
            Paragraph("7. Unit economics", sty["H2"]),
            table(
                [
                    ["Item", "Planning value"],
                    ["Unit CAPEX (fleet volume)", "$13.0M"],
                    ["12-unit fleet CAPEX", "$156M"],
                    ["Annual OPEX per unit", "$2.4M"],
                    ["Break-even utilization", "~$200K / month (covers OPEX)"],
                    ["Mature utilization target (base)", "$8–12M / unit / year"],
                    ["Contribution at $10M rev / $2.4M opex", "~$7.6M / unit / year"],
                ],
                [4.0 * inch, 2.8 * inch],
            ),
        )
    )
    s.append(
        kt(
            Paragraph("7.1 Illustrative mature revenue mix", sty["H3"]),
            table(
                [
                    ["Stream", "Share of unit revenue", "Role"],
                    ["Regional standby / availability", "35–45%", "Underwrites year-round presence"],
                    ["Wildfire / disaster mission fees", "20–30%", "High intensity, seasonal"],
                    ["Infrastructure / maritime / public safety", "15–25%", "Steady civil utilization"],
                    ["Rockoon / science / specialty", "5–15%", "High-margin spikes"],
                    ["Dual-use / defense options", "0–20%", "Selected configs; shared hull"],
                ],
                [2.6 * inch, 1.8 * inch, 2.4 * inch],
            ),
        )
    )

    # —— 8 FINANCIALS ——
    s.append(
        kt(
            Paragraph("8. Financial plan 2026–2030", sty["H2"]),
            Paragraph(
                "USD millions. The planning <b>17.8 : 1</b> ten-year fleet ROI is a long-horizon target on the stood-up fleet — not a 2030 cash guarantee. Early hulls cost more than the $13M volume target; the model includes learning-curve premium.",
                sty["Muted"],
            ),
        )
    )
    s.append(
        kt(
            Paragraph("8.1 Fleet build (base)", sty["H3"]),
            table(
                [
                    ["", "2026", "2027", "2028", "2029", "2030"],
                    ["Full-size units EOY", "0*", "1", "3", "6", "12"],
                    ["CA firefighting-primary", "—", "1", "2", "3", "4"],
                    ["Metro / regional nodes", "—", "0", "1", "3", "8"],
                ],
                [2.0 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch],
            ),
            Paragraph("*Pathfinder year — endurance, station-keeping, modular swap validation.", sty["Muted"]),
        )
    )
    s.append(
        kt(
            Paragraph("8.2 Capital expenditure (base, $M)", sty["H3"]),
            table(
                [
                    ["", "2026", "2027", "2028", "2029", "2030", "Total"],
                    ["Pathfinder + engineering", "18", "6", "4", "3", "2", "33"],
                    ["Hull production (learning curve)", "—", "18", "30", "42", "78", "168"],
                    ["Ground / ops infrastructure", "4", "6", "8", "10", "12", "40"],
                    ["Total CAPEX", "22", "30", "42", "55", "92", "241"],
                ],
                [2.0 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch, 0.75 * inch],
            ),
        )
    )
    s.append(
        kt(
            Paragraph("8.3 Operating model (base, $M)", sty["H3"]),
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
            ),
            Paragraph(
                "2030 check: ~$90M revenue on ~9 average units ≈ <b>$10M per unit-year</b>, above the $2.4M OPEX break-even. Cumulative CAPEX 2026–2030 ≈ $241M; cumulative revenue ≈ $154.5M during build years.",
                sty["Body"],
            ),
        )
    )
    s.append(
        kt(
            Paragraph("8.4 Scenario fan — 2030", sty["H3"]),
            table(
                [
                    ["Case", "Units", "Revenue", "EBITDA", "Note"],
                    ["Conservative", "6", "$45M", "$18M", "Slower production; CA + few metros"],
                    ["Base", "12", "$90M", "$55M", "Matches summary fleet target"],
                    ["Upside", "12+", "$130M", "$85M", "Strong dual-use + rockoon + multi-state wildfire"],
                ],
                [1.3 * inch, 0.9 * inch, 1.1 * inch, 1.1 * inch, 2.4 * inch],
            ),
        )
    )

    # —— 9 COMPETITION ——
    s.append(
        kt(
            Paragraph("9. Competition and differentiation", sty["H2"]),
            table(
                [
                    ["Alternative", "Strength", "Limitation vs TITAN-X"],
                    ["Tanker / scooping aircraft", "Proven mass delivery", "No indefinite loiter; weather &amp; basing limits"],
                    ["Helicopters", "Precision", "Low payload-hours; expensive persistence"],
                    ["LEO / GEO satellites", "Persistent eyes", "No mass delivery; limited logistics"],
                    ["Tethered aerostats", "Persistent local", "Site-bound; lower payload / mobility"],
                    ["HAPS aircraft concepts", "High altitude", "Rarely combine 20k-lb modularity + rockoon + dual-use"],
                ],
                [1.9 * inch, 2.0 * inch, 2.9 * inch],
            ),
            Paragraph(
                "<b>Differentiation:</b> indefinite solar/buoyancy endurance × 20,000 lb modularity × regional pre-positioning × shared civil–defense cost base.",
                sty["Body"],
            ),
        )
    )

    # —— 10 USE OF FUNDS ——
    s.append(
        kt(
            Paragraph("10. Use of funds and milestones", sty["H2"]),
            table(
                [
                    ["Use", "Share", "Purpose"],
                    ["Pathfinder + first full-scale hull", "35–45%", "Technical de-risk"],
                    ["CA firefighting + first metro modules", "20–30%", "Revenue-bearing configurations"],
                    ["Production tooling / learning-curve", "15–20%", "Drive unit cost toward $13M volume"],
                    ["Ops bases, helium, insurance, crew", "10–15%", "Year-round readiness"],
                    ["Corporate / BD / compliance", "5–10%", "Contracting with public &amp; private buyers"],
                ],
                [2.8 * inch, 1.2 * inch, 2.8 * inch],
            ),
        )
    )

    # —— 11 RISKS ——
    s.append(
        kt(
            Paragraph("11. Risks and guardrails", sty["H2"]),
            table(
                [
                    ["Risk", "Guardrail"],
                    ["Airworthiness / airspace", "Pathfinder before fleet claims"],
                    ["Helium &amp; ground logistics", "OPEX includes top-off; dual-sourcing plan"],
                    ["Early unit cost &gt; $13M", "Learning-curve premium modeled; volume target explicit"],
                    ["Public contracting cycles", "Civil commercial utilization underwrites standby"],
                    ["Over-claiming ROI", "17.8:1 is planning 10-year fleet figure — not a 2026–2030 cash guarantee"],
                    ["Defense narrative crowding civil", "Lead with regional civil utility; dual-use as selected configs"],
                ],
                [2.6 * inch, 4.2 * inch],
            ),
        )
    )

    # —— 12 ASK ——
    s.append(
        kt(
            Paragraph("12. The ask", sty["H2"]),
            Paragraph("We are engaging venture capitalists and business owners to fund or co-develop:", sty["Body"]),
            *bullets(
                sty,
                [
                    "Pathfinder validation and first full-scale hull",
                    "California firefighting concentration as the first revenue-bearing mission stack",
                    "Metro pre-positioning nodes that turn TITAN-X into practical infrastructure",
                ],
            ),
            Paragraph(
                "Return thesis: stand up the planning 12-unit fleet, clear ~$200K/month per-unit break-even via availability + mission mix, and pursue the long-horizon 17.8 : 1 planning ROI from persistent dual-use utilization — not from a single surge event.",
                sty["Body"],
            ),
        )
    )

    doc.build(s, onFirstPage=paint, onLaterPages=paint)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    return OUT


if __name__ == "__main__":
    build()
