#!/usr/bin/env python3
"""Generate AI Surgeon phone-UI mockup screens as SVG, render to PNG."""
import os, math, cairosvg

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 390, 844

_cos = math.cos


class _Rnd:
    """Tiny deterministic LCG so texture is reproducible build to build."""
    def __init__(self, seed):
        self.s = seed * 2654435761 % 2147483647

    def f(self):
        self.s = (self.s * 48271) % 2147483647
        return self.s / 2147483647

INK      = "#080D11"
PANEL    = "#111C23"
PANEL2   = "#17242C"
LINE     = "#22333D"
TEAL     = "#31B9A4"
TEAL_DIM = "#1B6A5F"
AMBER    = "#DFA33C"
RED      = "#D2454D"
TXT      = "#E9EFF1"
MUT      = "#7C9299"
MUT2     = "#546A72"
F        = "DejaVu Sans"


def head():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0A1218"/><stop offset="1" stop-color="#060A0D"/>
  </linearGradient>
  <linearGradient id="field" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2A1418"/><stop offset="1" stop-color="#140A0C"/>
  </linearGradient>
  <radialGradient id="lamp" cx="0.5" cy="0.32" r="0.62">
    <stop offset="0" stop-color="#3D2126" stop-opacity="0.95"/>
    <stop offset="1" stop-color="#0E0709" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="tissue1" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#B4736A"/><stop offset="1" stop-color="#7E4A46"/>
  </linearGradient>
  <linearGradient id="tissue2" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#C98F80"/><stop offset="1" stop-color="#8E5A50"/>
  </linearGradient>
  <linearGradient id="fat" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#D9B776"/><stop offset="1" stop-color="#9B7C46"/>
  </linearGradient>
  <linearGradient id="drape" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1E4750"/><stop offset="1" stop-color="#123037"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="0" fill="url(#bg)"/>
'''


def statusbar():
    return f'''<text x="22" y="26" font-family="{F}" font-size="11" font-weight="bold" fill="{TXT}">9:41</text>
<g fill="{TXT}"><rect x="330" y="18" width="3" height="7" rx="1"/><rect x="336" y="15" width="3" height="10" rx="1"/>
<rect x="342" y="12" width="3" height="13" rx="1"/><rect x="350" y="14" width="16" height="9" rx="2.5" opacity="0.5"/>
<rect x="352" y="16" width="10" height="5" rx="1"/></g>
'''


def header(module, sub, pts, coh):
    cw = 96
    fill = TEAL if coh >= 72 else (AMBER if coh >= 34 else RED)
    return f'''{statusbar()}
<path d="M22 62 l-8 8 l8 8" stroke="{MUT}" stroke-width="2" fill="none" stroke-linecap="round"/>
<text x="40" y="66" font-family="{F}" font-size="9" font-weight="bold" fill="{TEAL}" letter-spacing="1.4">{module}</text>
<text x="40" y="80" font-family="{F}" font-size="12.5" font-weight="bold" fill="{TXT}">{sub}</text>
<text x="368" y="68" text-anchor="end" font-family="{F}" font-size="15" font-weight="bold" fill="{TXT}">{pts}</text>
<text x="368" y="80" text-anchor="end" font-family="{F}" font-size="8" fill="{MUT2}" letter-spacing="0.8">POINTS</text>
<text x="22" y="99" font-family="{F}" font-size="8" fill="{MUT2}" letter-spacing="0.8">COHERENCE</text>
<rect x="86" y="92" width="{cw}" height="4" rx="2" fill="{LINE}"/>
<rect x="86" y="92" width="{cw*coh/100:.0f}" height="4" rx="2" fill="{fill}"/>
<text x="190" y="99" font-family="{F}" font-size="8" font-weight="bold" fill="{fill}">{coh}</text>
<line x1="0" y1="112" x2="390" y2="112" stroke="{LINE}" stroke-width="1"/>
'''


def attending(x, y, s=1.0, speaking=True):
    """Original armored attending silhouette — no borrowed likeness."""
    g = TEAL if speaking else MUT2
    return f'''<g transform="translate({x},{y}) scale({s})">
  <path d="M0 30 L0 10 L7 0 L25 0 L32 10 L32 30 Z" fill="#1C2B33" stroke="{LINE}" stroke-width="1"/>
  <path d="M4 12 L28 12 L26 20 L6 20 Z" fill="{INK}"/>
  <rect x="7" y="14.5" width="7" height="2.6" rx="1.3" fill="{g}"/>
  <rect x="18" y="14.5" width="7" height="2.6" rx="1.3" fill="{g}"/>
  <path d="M16 22 L16 27" stroke="{LINE}" stroke-width="1"/>
  <path d="M-5 30 L37 30 L34 44 L-2 44 Z" fill="#16232A" stroke="{LINE}" stroke-width="1"/>
  <path d="M16 32 L16 44" stroke="{LINE}" stroke-width="0.8"/>
</g>'''


def surgical_field(y0, h, opened=2, labels=(), tool=None):
    """Abstract surgical field. Final art comes from sourced anatomy, not primitives."""
    s = f'<rect x="0" y="{y0}" width="390" height="{h}" fill="url(#field)"/>'
    s += f'<rect x="0" y="{y0}" width="390" height="{h}" fill="url(#lamp)"/>'
    s += f'<path d="M0 {y0} L390 {y0} L390 {y0+h} L0 {y0+h} Z" fill="none"/>'
    # drape with fenestration
    s += f'<rect x="0" y="{y0}" width="390" height="{h}" fill="url(#drape)" opacity="0.92"/>'
    cx, cy = 195, y0 + h * 0.5
    rx, ry = 132, h * 0.34
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx+9}" ry="{ry+9}" fill="#0B1C21"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#field)"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#lamp)"/>'
    if opened >= 1:
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*0.86:.0f}" ry="{ry*0.84:.0f}" fill="url(#fat)" opacity="0.55"/>'
    if opened >= 2:
        s += f'<ellipse cx="{cx-4}" cy="{cy+2}" rx="{rx*0.66:.0f}" ry="{ry*0.62:.0f}" fill="url(#tissue1)" opacity="0.9"/>'
    if opened >= 3:
        # cecum + appendix suggestion
        s += f'<ellipse cx="{cx-34}" cy="{cy+4}" rx="46" ry="{ry*0.5:.0f}" fill="url(#tissue2)"/>'
        s += f'<path d="M{cx-6} {cy+14} Q{cx+34} {cy+26} {cx+72} {cy+2}" stroke="#C0766C" stroke-width="9" fill="none" stroke-linecap="round"/>'
        s += f'<path d="M{cx-6} {cy+14} Q{cx+34} {cy+26} {cx+72} {cy+2}" stroke="#A3242B" stroke-width="2.2" fill="none" stroke-linecap="round" opacity="0.85"/>'
        s += f'<path d="M{cx-70} {cy-10} Q{cx-40} {cy-16} {cx-8} {cy-6}" stroke="#DED3BB" stroke-width="3" fill="none" opacity="0.75"/>'
    # texture pass: vessel tracery + grain, so the field does not read as flat vector shapes
    if opened >= 1:
        rnd = _Rnd(7 + opened)
        for _ in range(26):
            a = rnd.f() * 6.283
            r = 0.25 + rnd.f() * 0.62
            px, py = cx + rx * r * _cos(a), cy + ry * r * _cos(a + 1.57)
            dx, dy = (rnd.f() - .5) * 40, (rnd.f() - .5) * 18
            s += (f'<path d="M{px:.0f} {py:.0f} q{dx*.5:.0f} {dy:.0f} {dx:.0f} {dy*.4:.0f}" '
                  f'stroke="#9C4A48" stroke-width="{0.5+rnd.f():.1f}" fill="none" opacity="{0.10+rnd.f()*0.20:.2f}"/>')
        for _ in range(150):
            a = rnd.f() * 6.283
            r = rnd.f() ** 0.5 * 0.94
            px, py = cx + rx * r * _cos(a), cy + ry * r * _cos(a + 1.57)
            s += (f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{1+rnd.f()*4:.1f}" ry="{1+rnd.f()*3:.1f}" '
                  f'fill="{"#E3B9A8" if rnd.f()>0.55 else "#5C2B2C"}" opacity="{0.04+rnd.f()*0.10:.2f}"/>')
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#lamp)" opacity="0.5"/>'
    for (lx, ly, tx, ty, txt, hot) in labels:
        col = TEAL if hot else "#B9C9CE"
        s += f'<circle cx="{lx}" cy="{ly}" r="3.4" fill="none" stroke="{col}" stroke-width="1.4"/>'
        s += f'<circle cx="{lx}" cy="{ly}" r="1.2" fill="{col}"/>'
        anch = "start" if tx > lx else "end"
        # keep the label inside the screen: measured against an 5.4px/char estimate
        est = len(txt) * 5.4
        tx2 = tx
        if anch == "start" and tx2 + 5 + est > 372:
            tx2 = 372 - est - 5
        if anch == "end" and tx2 - 5 - est < 18:
            tx2 = 18 + est + 5
        s += f'<line x1="{lx}" y1="{ly}" x2="{tx2}" y2="{ty}" stroke="{col}" stroke-width="1" opacity="0.9"/>'
        s += (f'<text x="{tx2 + (5 if anch=="start" else -5)}" y="{ty+3.5}" text-anchor="{anch}" '
              f'font-family="{F}" font-size="9" font-weight="bold" fill="{col}">{txt}</text>')
    if tool:
        s += tool
    return s


def scalpel(x, y, rot=-28):
    return f'''<g transform="translate({x},{y}) rotate({rot})">
  <rect x="0" y="-2.6" width="52" height="5.2" rx="1" fill="#8E9DA4"/>
  <rect x="0" y="-2.6" width="52" height="2" rx="1" fill="#C3D0D6"/>
  <path d="M-18 -3 L0 -2.6 L0 2.6 L-18 3 Z" fill="#DDE7EB"/>
  <path d="M-18 -3 L0 -2.6 L0 0 L-18 0 Z" fill="#FFFFFF" opacity="0.6"/>
</g>'''


def bar(x, y, w, h, r, fill, stroke=None, sw=1, op=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st} opacity="{op}"/>'


def txt(x, y, s, size=11, fill=TXT, w="normal", anchor="start", ls=0, fam=F):
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" '
            f'font-weight="{w}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def wrap(x, y, s, size=11, fill=TXT, lh=15, width=44, w="normal"):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if len(t) > width:
            lines.append(cur); cur = wd
        else:
            cur = t
    lines.append(cur)
    return "".join(txt(x, y + i * lh, l, size, fill, w) for i, l in enumerate(lines))


# ─────────────────────────── SCREEN 1 · STUDY ONE ───────────────────────────
def s1():
    s = head() + header("PHASE 1 OF 4 &#183; STUDY ONE", "Acute appendicitis", "40", 61)
    s += bar(22, 130, 346, 22, 11, "#12262B", TEAL_DIM)
    s += txt(34, 145, "LOCKED &#183; You cannot scrub in until 4 of 4 cards are complete", 8.5, TEAL)
    s += bar(22, 164, 346, 176, 14, PANEL, LINE)
    s += txt(40, 190, "CARD 3 OF 4 &#183; PATHOPHYSIOLOGY", 8.5, TEAL, "bold", ls=1.2)
    s += wrap(40, 212, "The lumen obstructs. Mucus keeps being secreted, so intraluminal pressure rises — past venous pressure before it passes arterial.", 11.5, TXT, 16, 46)
    s += bar(40, 270, 310, 1, 0, LINE)
    s += txt(40, 292, "So which comes first?", 12, TXT, "bold")
    s += txt(40, 312, "Points ride on the answer. The attending asks this again mid-case.", 9, MUT)
    opts = [("A", "Arterial ischaemia, then venous congestion", False),
            ("B", "Venous congestion, then arterial ischaemia", True),
            ("C", "Simultaneous — the wall fails all at once", False)]
    y = 352
    for k, t, sel in opts:
        c = TEAL if sel else LINE
        f = "#0F2C2B" if sel else PANEL2
        s += bar(22, y, 346, 46, 12, f, c, 1.4 if sel else 1)
        s += f'<circle cx="46" cy="{y+23}" r="11" fill="none" stroke="{c}" stroke-width="1.4"/>'
        s += txt(46, y + 27, k, 11, TEAL if sel else MUT, "bold", "middle")
        s += txt(68, y + 21, t, 10.5, TXT if sel else "#C3D2D7", "bold" if sel else "normal")
        if sel:
            s += txt(68, y + 35, "Correct. Congestion precedes ischaemia. +10", 8.5, TEAL)
        y += 54
    s += bar(22, 528, 346, 74, 14, "#101A20", LINE)
    s += txt(40, 552, "REMAINING", 8.5, MUT2, "bold", ls=1.2)
    s += txt(40, 573, "Card 4 — Referred pain: why periumbilical first,", 10, TXT)
    s += txt(40, 588, "then right lower quadrant", 10, TXT)
    s += bar(22, 620, 346, 52, 26, TEAL_DIM, TEAL, 1.4)
    s += txt(195, 651, "CONTINUE  →", 12.5, "#DFF7F2", "bold", "middle", 1.4)
    s += txt(195, 700, "Studying: 10 pts/card  ·  Observing: 5/step", 9, MUT2, anchor="middle")
    s += txt(195, 716, "Operating alone: 25/step  ·  Teaching: 40/step", 9, MUT2, anchor="middle")
    return s + "</svg>"


# ─────────────────────────── SCREEN 2 · SEE ONE ───────────────────────────
def s2():
    s = head() + header("PHASE 2 OF 4 &#183; SEE ONE", "The attending operates", "85", 66)
    labels = [(120, 300, 44, 250, "External oblique", False),
              (250, 330, 330, 268, "Internal oblique", False),
              (196, 372, 300, 410, "Transversalis fascia", True)]
    s += surgical_field(112, 330, opened=2, labels=labels, tool=scalpel(150, 288))
    s += bar(22, 460, 346, 96, 14, PANEL, TEAL_DIM, 1.4)
    s += attending(40, 476, 0.72)
    s += txt(74, 490, "AI ATTENDING", 8, TEAL, "bold", ls=1.4)
    s += wrap(74, 508, "Transversalis fascia. Under it, preperitoneal fat, then peritoneum. I am splitting muscle, not cutting it.", 10, TXT, 14, 40)
    s += bar(22, 570, 346, 40, 12, "#12262B", TEAL_DIM)
    s += txt(38, 595, "Tap any structure to be told what it is and why it matters", 9.5, TEAL)
    s += bar(22, 626, 346, 118, 14, "#101A20", LINE)
    s += txt(40, 650, "NOTHING HERE IS SKIPPABLE. NOTHING IS GRADED.", 8.5, MUT2, "bold", ls=0.9)
    s += wrap(40, 672, "This phase exists so you arrive at Do One having already seen the anatomy in the order it appears.", 10, "#C3D2D7", 15, 45)
    s += bar(22, 762, 168, 46, 23, PANEL2, LINE)
    s += txt(106, 790, "PAUSE &#183; ASK", 11, TXT, "bold", "middle")
    s += bar(200, 762, 168, 46, 23, TEAL_DIM, TEAL, 1.4)
    s += txt(284, 790, "SCRUB IN  →", 11, "#DFF7F2", "bold", "middle")
    return s + "</svg>"


# ─────────────────────────── SCREEN 3 · DO ONE / DECISION ───────────────────
def s3():
    s = head() + header("PHASE 3 OF 4 &#183; DO ONE", "You are operating", "310", 78)
    labels = [(150, 300, 40, 246, "Cecum", False),
              (268, 322, 344, 262, "Appendix", False),
              (214, 352, 306, 400, "Mesoappendix", True)]
    s += surgical_field(112, 300, opened=3, labels=labels)
    s += bar(22, 428, 346, 78, 14, PANEL, TEAL, 1.6)
    s += attending(38, 442, 0.66)
    s += txt(70, 456, "AI ATTENDING ASKS", 8, TEAL, "bold", ls=1.4)
    s += txt(70, 476, "“What are you about to divide?”", 13, TXT, "bold")
    s += txt(70, 494, "Answer before the instrument unlocks.", 9, MUT)
    s += f'<rect x="300" y="440" width="54" height="22" rx="11" fill="#2A1518" stroke="{RED}" stroke-width="1"/>'
    s += txt(327, 455, "0:14", 10, RED, "bold", "middle")
    y = 520
    opts = [("Mesoappendix, carrying the appendicular artery", "+25", TEAL, True),
            ("Taenia libera", "–10", MUT, False),
            ("Ileocolic artery", "–25  wrong structure", MUT, False),
            ("Peritoneal reflection", "–10", MUT, False)]
    for t, pts, col, sel in opts:
        f = "#0F2C2B" if sel else PANEL2
        c = TEAL if sel else LINE
        s += bar(22, y, 346, 44, 12, f, c, 1.4 if sel else 1)
        s += txt(38, y + 27, t, 10.5, TXT if sel else "#AEBEC4", "bold" if sel else "normal")
        s += txt(354, y + 27, pts, 9.5, col, "bold", "end")
        y += 51
    s += bar(22, 732, 346, 1, 0, LINE)
    s += txt(22, 754, "THEN THE GESTURE", 8.5, MUT2, "bold", ls=1.2)
    ge = [("swipe", "incise"), ("2-finger", "split / retract"), ("pinch", "clamp"), ("hold", "ligate")]
    x = 22
    for g, m in ge:
        s += bar(x, 766, 82, 44, 11, "#101A20", LINE)
        s += txt(x + 41, 784, g, 9.5, TEAL, "bold", "middle")
        s += txt(x + 41, 799, m, 8, MUT, anchor="middle")
        x += 87
    return s + "</svg>"


# ─────────────────────────── SCREEN 4 · SCRUB TECH ───────────────────────────
def s4():
    s = head() + header("PHASE 3 OF 4 &#183; DO ONE", "Call for the instrument", "335", 81)
    s += bar(22, 130, 346, 74, 14, PANEL, TEAL, 1.5)
    s += attending(38, 142, 0.62)
    s += txt(68, 156, "AI ATTENDING", 8, TEAL, "bold", ls=1.4)
    s += txt(68, 176, "“Open the peritoneum between two of", 11.5, TXT, "bold")
    s += txt(68, 192, "these. Ask the scrub. By name.”", 11.5, TXT, "bold")
    s += txt(22, 228, "STERILE BACK TABLE", 8.5, MUT2, "bold", ls=1.2)
    s += txt(368, 228, "you have no instruments until you ask", 8.5, MUT2, anchor="end")
    # instrument tray
    s += bar(22, 240, 346, 300, 14, "#0D171C", LINE)
    items = [("Hemostat", "Kelly / mosquito", True),
             ("Metzenbaum scissors", "sharp dissection", False),
             ("Babcock clamp", "delivers the cecum", False),
             ("Army-Navy retractor", "wound edge", False),
             ("0-Vicryl on driver", "fascial closure", False),
             ("Bovie", "electrocautery", False)]
    y = 258
    for name, note, sel in items:
        c = TEAL if sel else LINE
        f = "#0F2C2B" if sel else PANEL2
        s += bar(36, y, 318, 42, 10, f, c, 1.4 if sel else 1)
        s += f'<rect x="50" y="{y+16}" width="34" height="3" rx="1.5" fill="{"#C3D0D6" if sel else MUT2}"/>'
        s += f'<rect x="50" y="{y+22}" width="26" height="2.4" rx="1.2" fill="{"#8E9DA4" if sel else MUT2}" opacity="0.7"/>'
        s += txt(96, y + 20, name, 10.5, TXT if sel else "#AEBEC4", "bold" if sel else "normal")
        s += txt(96, y + 33, note, 8.5, TEAL if sel else MUT2)
        if sel:
            s += txt(340, y + 26, "✓", 14, TEAL, "bold", "end")
        y += 47
    s += bar(22, 556, 346, 62, 14, "#12262B", TEAL_DIM)
    s += txt(38, 578, "SCRUB TECH", 8, TEAL, "bold", ls=1.4)
    s += txt(38, 598, "“Two hemostats. Careful, they're loaded.”", 10.5, TXT)
    s += bar(22, 634, 346, 70, 14, "#241A10", AMBER, 1)
    s += txt(38, 656, "WRONG INSTRUMENT COSTS POINTS", 8.5, AMBER, "bold", ls=0.9)
    s += wrap(38, 676, "And the scrub says so. Nobody hands you the wrong thing silently.", 9.5, "#D9C9A8", 14, 46)
    s += bar(22, 722, 346, 52, 26, TEAL_DIM, TEAL, 1.4)
    s += txt(195, 753, "CALL FOR IT", 12, "#DFF7F2", "bold", "middle", 1.4)
    s += txt(195, 796, "Voice or tap. Spoken aloud scores higher.", 9, MUT2, anchor="middle")
    return s + "</svg>"


# ─────────────────────────── SCREEN 5 · TRAUMA / VITALS ─────────────────────
def s5():
    s = head() + header("TRAUMA MODE &#183; CASE 07", "Tension pneumothorax", "590", 44)
    # acuity chip
    s += bar(22, 126, 122, 26, 13, "#2A1518", RED, 1.2)
    s += txt(83, 144, "ACUITY  ×2.5", 9.5, RED, "bold", "middle")
    s += bar(152, 126, 216, 26, 13, "#241A10", AMBER, 1)
    s += txt(260, 144, "PATIENT DEATH ENABLED", 9, AMBER, "bold", "middle")
    # monitor
    s += bar(22, 164, 346, 158, 14, "#04090C", LINE)
    s += txt(38, 186, "ECG  II", 8.5, TEAL, "bold", ls=1.2)
    ecg = "M38 250"
    x = 38
    import math
    while x < 350:
        ecg += f" L{x+7} 250 L{x+9} 244 L{x+11} 262 L{x+13} 226 L{x+16} 258 L{x+19} 250 L{x+26} 250"
        x += 34
    s += f'<path d="{ecg}" stroke="{TEAL}" stroke-width="1.7" fill="none" opacity="0.95"/>'
    s += f'<line x1="38" y1="204" x2="352" y2="204" stroke="{LINE}" stroke-width="0.6"/>'
    vit = [("HR", "138", RED, 60), ("BP", "72/44", RED, 150), ("SpO2", "81", RED, 250)]
    for lab, val, col, vx in vit:
        s += txt(vx, 292, lab, 8.5, MUT2, "bold", "middle", 1)
        s += txt(vx, 312, val, 18, col, "bold", "middle")
    s += bar(22, 334, 346, 76, 14, PANEL, TEAL_DIM, 1.2)
    s += attending(38, 346, 0.6)
    s += txt(66, 360, "ANAESTHESIA", 8, TEAL, "bold", ls=1.4)
    s += wrap(66, 378, "Pressure is falling and I cannot ventilate him. This is obstructive, not hypovolaemic. Move.", 10, TXT, 14, 42)
    s += bar(22, 424, 346, 58, 14, "#2A1518", RED, 1.5)
    s += txt(38, 446, "TIME TO DECOMPRESSION", 8.5, RED, "bold", ls=1)
    s += txt(38, 468, "Arrest at current trajectory", 11, TXT, "bold")
    s += bar(258, 434, 94, 32, 16, "#3A1B20", RED, 1.2)
    s += txt(305, 455, "00:41", 15, RED, "bold", "middle")
    y = 498
    for t, note in [("Needle decompression, 2nd ICS", "buys time, does not fix it"),
                    ("Tube thoracostomy, 5th ICS", "definitive"),
                    ("Fluid bolus", "wrong physiology")]:
        s += bar(22, y, 346, 46, 12, PANEL2, LINE)
        s += txt(38, y + 22, t, 10.5, TXT, "bold")
        s += txt(38, y + 36, note, 8.5, MUT)
        y += 53
    s += bar(22, 664, 346, 84, 14, "#101A20", LINE)
    s += txt(40, 688, "COHERENCE IS RUNNING THE CLOCK", 8.5, AMBER, "bold", ls=0.9)
    s += wrap(40, 708, "You are ahead of this module, so the deterioration model is running faster than baseline.", 9.5, "#C3D2D7", 14, 46)
    s += txt(195, 786, "Errors first. Time only breaks ties.", 9.5, MUT2, anchor="middle")
    return s + "</svg>"


# ─────────────────────────── SCREEN 6 · TEACH ONE / DEBRIEF ─────────────────
def s6():
    s = head() + header("PHASE 4 OF 4 &#183; TEACH ONE", "A junior is asking", "1,240", 88)
    s += bar(22, 130, 346, 96, 14, PANEL, AMBER, 1.4)
    s += f'<circle cx="52" cy="164" r="15" fill="{PANEL2}" stroke="{AMBER}" stroke-width="1.2"/>'
    s += txt(52, 169, "M3", 9, AMBER, "bold", "middle")
    s += txt(78, 152, "JUNIOR &#183; THIRD-YEAR STUDENT", 8, AMBER, "bold", ls=1.2)
    s += txt(78, 174, "“I can't find the appendix.", 12.5, TXT, "bold")
    s += txt(78, 191, "What's the landmark?”", 12.5, TXT, "bold")
    s += txt(78, 212, "Worth 40 points — the most in the game.", 9, MUT)
    s += bar(22, 240, 346, 108, 14, PANEL2, LINE)
    s += txt(38, 262, "YOUR ANSWER", 8.5, MUT2, "bold", ls=1.2)
    s += wrap(38, 284, "Follow the taenia libera down the anterior cecum. All three taeniae converge on the base of the appendix. That's the landmark — not the tip.", 10, TXT, 15, 44)
    s += bar(22, 362, 346, 34, 12, "#0F2C2B", TEAL, 1.4)
    s += txt(38, 384, "Attending: “That is the answer. +40”", 10, TEAL, "bold")
    s += bar(22, 414, 346, 1, 0, LINE)
    s += txt(22, 438, "CASE DEBRIEF", 9, TEAL, "bold", ls=1.4)
    rows = [("Study One · 4 cards", "+40"), ("See One · 11 steps", "+55"),
            ("Do One · 11 steps solo", "+275"), ("Teach One · 3 questions", "+120"),
            ("Wrong instrument ×2", "–20"), ("Acuity multiplier", "×1.8")]
    y = 456
    for k, v in rows:
        neg = v.startswith("–")
        s += txt(38, y, k, 10, "#C3D2D7")
        s += txt(352, y, v, 10, RED if neg else TXT, "bold", "end")
        s += bar(38, y + 8, 314, 1, 0, "#182630")
        y += 26
    s += bar(22, 620, 346, 60, 14, "#0F2C2B", TEAL, 1.6)
    s += txt(38, 645, "CASE TOTAL", 9, TEAL, "bold", ls=1.2)
    s += txt(38, 666, "Coherence 88 — next module unlocked", 9, MUT)
    s += txt(352, 658, "+846", 22, TEAL, "bold", "end")
    s += bar(22, 694, 346, 66, 14, "#101A20", LINE)
    s += txt(40, 718, "NEXT ON THE LADDER", 8.5, MUT2, "bold", ls=1.2)
    s += txt(40, 740, "Laparoscopic cholecystectomy — Calot's triangle", 10, TXT)
    s += txt(195, 800, "Being able to operate and being able to be", 9, MUT2, anchor="middle")
    s += txt(195, 814, "responsible for someone else operating are", 9, MUT2, anchor="middle")
    s += txt(195, 828, "different competencies. Only one is tested elsewhere.", 9, MUT2, anchor="middle")
    return s + "</svg>"


NAMES = ["01-study-one", "02-see-one", "03-do-one-decision",
         "04-scrub-tech", "05-trauma-vitals", "06-teach-one"]
for fn, name in zip([s1, s2, s3, s4, s5, s6], NAMES):
    svg = fn()
    p = os.path.join(OUT, f"screen-{name}.svg")
    open(p, "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, f"screen-{name}.png"),
                     output_width=W * 3, output_height=H * 3)
    print("rendered", name)
