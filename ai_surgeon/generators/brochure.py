#!/usr/bin/env python3
"""AI Surgeon — concept brochure. Follows AI-Surgeon-Scoped-Concept.md as the script."""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader

OUT = os.path.dirname(os.path.abspath(__file__))
PW, PH = LETTER
M = 0.72 * inch

INK   = HexColor("#0B1319")
DEEP  = HexColor("#122029")
TEAL  = HexColor("#2FAE9A")
TEALD = HexColor("#1B6A5F")
PAPER = HexColor("#F7F5F0")
BODY  = HexColor("#232B2F")
MUT   = HexColor("#6C7B82")
RULE  = HexColor("#D6D2C8")
AMBER = HexColor("#B4802A")
RED   = HexColor("#A8353C")

H1, H2, BOLD, REG, IT = "Helvetica-Bold", "Helvetica-Bold", "Helvetica-Bold", "Helvetica", "Helvetica-Oblique"

c = canvas.Canvas(os.path.join(OUT, "AI-Surgeon-Brochure.pdf"), pagesize=LETTER)
c.setTitle("AI Surgeon — Concept Brochure")
c.setAuthor("Jonathan Simons, CRNA · Simons Medical Innovations, LLC")
c.setSubject("Phone-first surgical training. Concept and screen design.")

PAGE = [0]


def wrap_lines(text, font, size, width):
    out, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width:
            line = t
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def para(x, y, text, width, font=REG, size=10.2, lead=14.6, fill=BODY):
    c.setFont(font, size)
    c.setFillColor(fill)
    for ln in wrap_lines(text, font, size, width):
        c.drawString(x, y, ln)
        y -= lead
    return y


def bg(dark=False):
    c.setFillColor(INK if dark else PAPER)
    c.rect(0, 0, PW, PH, stroke=0, fill=1)


def footer(label, dark=False):
    PAGE[0] += 1
    c.setFont(REG, 7.4)
    c.setFillColor(HexColor("#5A6B72") if dark else MUT)
    c.drawString(M, 0.5 * inch, "AI SURGEON  ·  SIMONS MEDICAL INNOVATIONS, LLC  ·  CONFIDENTIAL")
    c.drawRightString(PW - M, 0.5 * inch, f"{label}   {PAGE[0]:02d}")


def kicker(x, y, s, fill=TEAL, size=7.8):
    c.setFont(BOLD, size)
    c.setFillColor(fill)
    c.drawString(x, y, s)


def rule(x, y, w, col=RULE, lw=0.7):
    c.setStrokeColor(col)
    c.setLineWidth(lw)
    c.line(x, y, x + w, y)


def phone(img, x, y, h, caption=None, cap_w=None):
    """Place a screen PNG as a phone with a hairline bezel."""
    w = h * 390 / 844
    c.setFillColor(HexColor("#1B262C"))
    c.roundRect(x - 3, y - 3, w + 6, h + 6, 10, stroke=0, fill=1)
    c.drawImage(ImageReader(img), x, y, w, h, mask=None)
    c.setStrokeColor(HexColor("#39474E"))
    c.setLineWidth(0.6)
    c.roundRect(x - 3, y - 3, w + 6, h + 6, 10, stroke=1, fill=0)
    if caption:
        c.setFont(REG, 7.6)
        c.setFillColor(MUT)
        yy = y - 13
        for ln in wrap_lines(caption, REG, 7.6, cap_w or w + 40):
            c.drawString(x - 2, yy, ln)
            yy -= 9.6
    return w


IMG = {k: os.path.join(OUT, f"screen-{k}.png") for k in
       ["01-study-one", "02-see-one", "03-do-one-decision",
        "04-scrub-tech", "05-trauma-vitals", "06-teach-one"]}

# ══════════════════════════════ 1 · COVER ══════════════════════════════
bg(dark=True)
c.setFillColor(DEEP)
c.rect(0, PH - 4.2 * inch, PW, 4.2 * inch, stroke=0, fill=1)
c.setStrokeColor(TEALD)
c.setLineWidth(1.2)
c.line(M, PH - 4.2 * inch, PW - M, PH - 4.2 * inch)

kicker(M, PH - 1.15 * inch, "SIMONS MEDICAL INNOVATIONS, LLC", TEAL, 8.4)
c.setFont(H1, 54)
c.setFillColor(HexColor("#EDF3F4"))
c.drawString(M, PH - 1.95 * inch, "AI SURGEON")
c.setFont(REG, 15.5)
c.setFillColor(HexColor("#9FB3B9"))
c.drawString(M, PH - 2.38 * inch, "See one. Do one. Teach one.")
c.setFont(BOLD, 11.6)
c.setFillColor(TEAL)
c.drawString(M, PH - 2.85 * inch, "A phone-first surgical training product where you")
c.drawString(M, PH - 3.05 * inch, "cannot cut something you cannot name.")
c.setFont(REG, 9.6)
c.setFillColor(HexColor("#7C9299"))
c.drawString(M, PH - 3.62 * inch, "Concept and screen design  ·  August 2026")
c.drawString(M, PH - 3.82 * inch, "Companion to the business plan  ·  Prepared for development partners")

y = PH - 5.0 * inch
c.setFillColor(HexColor("#C9D6DA"))
y = para(M, y, "An AI attending performs the operation, names every structure as it appears, then hands "
               "over the instruments and supervises. It asks questions mid-case and points ride on the "
               "answer. Before a learner is allowed to scrub in, they have to study the anatomy and the "
               "pathophysiology and get it right.",
         PW - 2 * M, REG, 11.6, 17, HexColor("#C9D6DA"))

y -= 22
rule(M, y, PW - 2 * M, HexColor("#22333D"))
y -= 30
cols = [("PHASE 1", "Phone. Browser-based.\nNo install. Touch gestures."),
        ("PHASE 2", "VR. Same codebase.\nWebXR, already wired."),
        ("PHASE 3", "ProVR Bluetooth instruments.\nOptional, like a stylus.")]
cx = M
for k, v in cols:
    kicker(cx, y, k, TEAL, 8)
    c.setFont(REG, 9.2)
    c.setFillColor(HexColor("#9FB3B9"))
    yy = y - 15
    for ln in v.split("\n"):
        c.drawString(cx, yy, ln)
        yy -= 12.4
    cx += (PW - 2 * M) / 3

# cover hero: three screens
hy = 1.06 * inch
hh = 2.62 * inch
hw = hh * 390 / 844
hx = PW - M - hw
for k in ["06-teach-one", "05-trauma-vitals", "03-do-one-decision"]:
    phone(IMG[k], hx, hy, hh)
    hx -= hw + 0.16 * inch
kicker(M, hy + hh - 6, "THE PRODUCT, ON A PHONE", TEAL)
c.setFont(REG, 9.4)
c.setFillColor(HexColor("#8FA5AC"))
yy = hy + hh - 26
for ln in wrap_lines("Identify before you cut. Call for your instruments by name. Answer the "
                     "attending mid-case. Then teach it to someone junior to you — the phase "
                     "worth the most points, and the one nothing else on the market tests.",
                     REG, 9.4, 2.0 * inch):
    c.drawString(M, yy, ln)
    yy -= 13
footer("COVER", dark=True)
c.showPage()

# ══════════════════════════════ 2 · THE OPENING ══════════════════════════════
bg()
kicker(M, PH - M, "WHY THIS EXISTS")
c.setFont(H1, 25)
c.setFillColor(INK)
c.drawString(M, PH - M - 32, "The incumbents already bought")
c.drawString(M, PH - M - 60, "the expensive ground.")
rule(M, PH - M - 78, 2.1 * inch, TEAL, 1.6)

colw = (PW - 2 * M - 0.42 * inch) / 2
y1 = PH - M - 108
y = para(M, y1, "Osso VR owns headset-based institutional procedural training. Level Ex owns "
                "pharma-funded gamified specialty content. Touch Surgery, owned by Medtronic, "
                "already puts procedural rehearsal on a phone and gives it away.", colw)
y -= 8
y = para(M, y, "None of them owns the layer beneath the procedure, which is anatomy a learner "
               "actually has to know rather than click through. That is the opening, and it is "
               "the only ground worth entering on.", colw)
y -= 8
y = para(M, y, "This document is not a request for $500M to build a AAA title. The phone version "
               "with four to six modules is a small-team build — one developer, one anatomy "
               "artist, one surgical content reviewer, nine to twelve months.", colw, BOLD)

y2 = y1
x2 = M + colw + 0.42 * inch
c.setFillColor(HexColor("#EFEBE2"))
c.roundRect(x2, y2 - 3.05 * inch, colw, 3.05 * inch, 8, stroke=0, fill=1)
c.setStrokeColor(RULE)
c.setLineWidth(0.7)
c.roundRect(x2, y2 - 3.05 * inch, colw, 3.05 * inch, 8, stroke=1, fill=0)
kicker(x2 + 16, y2 - 22, "THE ONE DESIGN DECISION")
yy = para(x2 + 16, y2 - 46, "The loop does not open on a scalpel. It opens on the appendix — what it is, "
                            "what it does, why this one has to come out.", colw - 32, BOLD, 11.4, 15.4, INK)
yy -= 6
yy = para(x2 + 16, yy, "Then the pathophysiology. The lumen obstructs, mucus keeps being secreted, "
                       "pressure passes venous before arterial, so congestion precedes ischaemia. "
                       "Then bacterial translocation, gangrene, perforation.", colw - 32, REG, 9.6, 13.4)
yy -= 6
yy = para(x2 + 16, yy, "Four cards. Four questions. Ten points each. You cannot scrub in until you "
                       "have done them.", colw - 32, REG, 9.6, 13.4)
yy -= 4
c.setFillColor(TEALD)
c.setFont(BOLD, 9.8)
for ln in wrap_lines("The game will not let you cut something you have not studied.",
                     BOLD, 9.8, colw - 32):
    c.drawString(x2 + 16, yy, ln)
    yy -= 13.4

# strip of all six screens
ys = 1.06 * inch
kicker(M, ys + 2.24 * inch, "THE LOOP, IN SIX SCREENS")
xs = M
for k in IMG:
    w = phone(IMG[k], xs, ys, 2.0 * inch)
    xs += w + 0.19 * inch
c.setFont(REG, 7.4)
c.setFillColor(MUT)
c.drawString(M, ys - 15, "Screen design is final-intent. Anatomy shown is placeholder — see the note on sourced anatomy, page 7.")
footer("THE OPENING")
c.showPage()

# ══════════════════════════════ 3 · STUDY ONE / SEE ONE ══════════════════════
bg()
kicker(M, PH - M, "PHASES 1 AND 2")
c.setFont(H1, 25)
c.setFillColor(INK)
c.drawString(M, PH - M - 32, "First you study. Then you watch")
c.drawString(M, PH - M - 60, "an attending do it properly.")
rule(M, PH - M - 78, 2.1 * inch, TEAL, 1.6)

ph_h = 4.35 * inch
py = PH - M - 100 - ph_h
w1 = phone(IMG["01-study-one"], M, py, ph_h)
tx = M + w1 + 0.34 * inch
tw = PW - M - tx
kicker(tx, py + ph_h - 6, "STUDY ONE  ·  10 POINTS A CARD")
y = para(tx, py + ph_h - 26, "Pre-op anatomy and physiology, gated. The card above is the one every "
                             "examiner asks about: pressure rises past venous before arterial, so venous "
                             "congestion precedes arterial ischaemia. Get it wrong and you review it. "
                             "Get it right and the attending will still ask you again mid-case.", tw)
y -= 10
kicker(tx, y, "SEE ONE  ·  5 POINTS A STEP")
y = para(tx, y - 20, "Not a cutscene. The attending performs the procedure and names every structure as "
                     "it appears. The learner can stop at any moment, tap anything on screen, and be "
                     "told what it is and why it matters clinically.", tw)
y -= 6
y = para(tx, y, "Nothing here is skippable and nothing here is graded. The phase exists so the learner "
                "arrives at the next one having already seen the anatomy in the order it appears.", tw, IT)
y -= 12
c.setFillColor(HexColor("#EFEBE2"))
c.roundRect(tx, py + 6, tw, y - py - 14, 8, stroke=0, fill=1)
kicker(tx + 14, y - 18, "ANATOMICAL CONTENT STANDARD", AMBER)
para(tx + 14, y - 38, "Every structure carries a name, a line on what it is, and a line on why it "
                      "matters clinically. Every step sequence has to match an accepted operative "
                      "technique and be reviewable against a standard text. Where technique is "
                      "genuinely contested — stump inversion, for instance — the module says so "
                      "rather than picking a side silently. This is the part that cannot be "
                      "outsourced. It is also the moat: a competitor can copy the gesture system "
                      "in a quarter.", tw - 28, REG, 9.2, 12.8)

# four-phase loop band
by = 1.06 * inch
c.setFillColor(DEEP)
c.roundRect(M, by, PW - 2 * M, 1.42 * inch, 8, stroke=0, fill=1)
kicker(M + 18, by + 1.42 * inch - 20, "THE LOOP, AND THE GATE THAT RUNS IT", TEAL)
phases = [("STUDY ONE", "Anatomy and pathophysiology.\nGated. 10 a card."),
          ("SEE ONE", "The attending operates and\nnames everything. 5 a step."),
          ("DO ONE", "You identify, then you act.\n25 a step, alone."),
          ("TEACH ONE", "A junior asks. You answer.\n40 a step.")]
px = M + 18
for i, (k, v) in enumerate(phases):
    c.setFont(BOLD, 9.2)
    c.setFillColor(HexColor("#EDF3F4"))
    c.drawString(px, by + 60, k)
    c.setFont(REG, 7.8)
    c.setFillColor(HexColor("#8FA5AC"))
    yy = by + 46
    for ln in v.split("\n"):
        c.drawString(px, yy, ln)
        yy -= 10.4
    if i < 3:
        c.setFillColor(TEAL)
        c.setFont(H1, 12)
        c.drawString(px + 1.52 * inch, by + 58, "→")
    px += 1.72 * inch
c.setFont(REG, 7.6)
c.setFillColor(TEAL)
c.drawString(M + 18, by + 24, "COHERENCE GATE   Above 72, the next module opens at the difficulty you left off at.")
c.setFillColor(HexColor("#8FA5AC"))
c.drawString(M + 18, by + 13, "34 to 72 repeats Do One. Below 34 sends you back to the specific structures you missed, then back to See One.")
footer("STUDY · SEE")
c.showPage()

# ══════════════════════════════ 4 · DO ONE ══════════════════════════════
bg()
kicker(M, PH - M, "PHASE 3  ·  THE CORE MECHANIC")
c.setFont(H1, 25)
c.setFillColor(INK)
c.drawString(M, PH - M - 32, "You do not get to cut something")
c.drawString(M, PH - M - 60, "you cannot name.")
rule(M, PH - M - 78, 2.1 * inch, TEAL, 1.6)

ph_h = 4.35 * inch
py = PH - M - 100 - ph_h
tw = PW - 2 * M - 2 * (ph_h * 390 / 844) - 0.68 * inch
w1 = phone(IMG["03-do-one-decision"], M, py, ph_h)
w2 = phone(IMG["04-scrub-tech"], PW - M - ph_h * 390 / 844, py, ph_h)
tx = M + w1 + 0.34 * inch
kicker(tx, py + ph_h - 6, "IDENTIFY, THEN ACT")
y = para(tx, py + ph_h - 26, "The attending calls the step. The learner must identify the correct "
                             "structure before the maneuver unlocks. Then the gesture: swipe to "
                             "incise, two-finger spread to split bluntly or retract, pinch to clamp, "
                             "press-and-hold to ligate.", tw, REG, 9.8, 13.8)
y -= 8
y = para(tx, y, "Wrong structure, wrong maneuver, and wrong-place-right-maneuver are three "
                "different errors and are scored differently, because they are three different "
                "kinds of not knowing.", tw, BOLD, 9.8, 13.8)
y -= 10
kicker(tx, y, "THE SCRUB TECH", AMBER)
y = para(tx, y - 20, "You do not have instruments. You ask for them, by name, and the scrub hands "
                     "them over.", tw, BOLD, 9.8, 13.8)
y -= 6
y = para(tx, y, "Knowing the peritoneum is opened between two hemostats, that the external oblique "
                "aponeurosis is taken with Metzenbaums, that the cecum is delivered with a Babcock "
                "and not a Kelly — that is real operative fluency, and no other product makes you "
                "produce it from memory.", tw, REG, 9.8, 13.8)
y -= 6
y = para(tx, y, "It also teaches the social choreography of an OR, which students are terrified of "
                "and no simulator addresses. Wrong instrument costs points and the scrub says so. "
                "Nobody hands you the wrong thing silently.", tw, REG, 9.8, 13.8)
y -= 8
c.setFillColor(TEALD)
c.setFont(BOLD, 9.4)
for ln in wrap_lines("Nearly free to build. Among the highest-value mechanics in the design.", BOLD, 9.4, tw):
    c.drawString(tx, y, ln)
    y -= 13

# economy band
by = 1.02 * inch
c.setFillColor(DEEP)
c.roundRect(M, by, PW - 2 * M, 1.38 * inch, 8, stroke=0, fill=1)
kicker(M + 18, by + 1.38 * inch - 20, "THE ECONOMY IS DELIBERATELY LOPSIDED", TEAL)
items = [("10", "study, per card"), ("5", "observing, per step"),
         ("25", "operating alone"), ("40", "teaching a step back")]
ix = M + 18
for n, lab in items:
    c.setFont(H1, 21)
    c.setFillColor(HexColor("#EDF3F4"))
    c.drawString(ix, by + 44, n)
    c.setFont(REG, 8)
    c.setFillColor(HexColor("#8FA5AC"))
    c.drawString(ix, by + 30, lab)
    ix += 1.12 * inch
c.setFont(REG, 8.4)
c.setFillColor(HexColor("#9FB3B9"))
yy = by + 1.38 * inch - 42
for ln in wrap_lines("Acuity multiplies reward and penalty together. A routine nineteen-year-old is "
                     "×1.0. A perforated appendix with an abscess in a diabetic is ×1.8. A septic "
                     "seventy-year-old on anticoagulation is ×2.5. Taking a hard case is a real "
                     "gamble, not a free points grab.", REG, 8.4, 2.62 * inch):
    c.drawString(M + 5.05 * inch, yy, ln)
    yy -= 11
footer("DO ONE")
c.showPage()

# ══════════════════════════════ 5 · TRAUMA / ACUITY ══════════════════════════
bg()
kicker(M, PH - M, "ACUITY, PHYSIOLOGY, AND LOSING THE PATIENT")
c.setFont(H1, 25)
c.setFillColor(INK)
c.drawString(M, PH - M - 32, "Trauma is a mode, not a module.")
rule(M, PH - M - 50, 2.1 * inch, TEAL, 1.6)

ph_h = 4.35 * inch
py = PH - M - 74 - ph_h
w1 = phone(IMG["05-trauma-vitals"], M, py, ph_h)
tx = M + w1 + 0.34 * inch
tw = PW - M - tx
y = para(tx, py + ph_h - 4, "A randomized case, a clock, incomplete information, and an anatomy you have "
                            "to identify under time pressure with the field partly obscured.", tw, BOLD, 10.6, 14.6)
y -= 10
kicker(tx, y, "LIVE PHYSIOLOGY, NOT A TIMER")
y = para(tx, y - 20, "The monitor is driven by a deterioration model, not a countdown. In the built "
                     "tension pneumothorax module, doing nothing arrests the patient in 56 to 78 "
                     "seconds. A needle buys 67 to 110. The tube has to be in within 63 to 103. "
                     "The spread depends on how well the learner is doing.", tw)
y -= 10
kicker(tx, y, "COHERENCE MONITORING")
y = para(tx, y - 20, "The system tracks accuracy and hesitation continuously and moves difficulty in "
                     "both directions during play, not between sessions. High coherence and the "
                     "labels stop appearing, gesture tolerance tightens, the attending stops "
                     "narrating, the teaching questions get harder — and the clock runs faster. "
                     "Low coherence and the scaffolding quietly comes back.", tw)
y -= 6
y = para(tx, y, "A learner who is struggling should not be failed out. A learner who is ahead of the "
                "module should feel it get harder within thirty seconds, not at the next unlock.", tw, IT)
y -= 12
c.setFillColor(HexColor("#F1E7E7"))
c.roundRect(tx, y - 1.42 * inch, tw, 1.42 * inch, 8, stroke=0, fill=1)
kicker(tx + 14, y - 20, "AND YOU CAN LOSE THE PATIENT", RED)
para(tx + 14, y - 40, "A death voids the case score and takes a fixed penalty off rank. It must be rare, "
                      "always traceable to specific decisions the learner made, and followed by a "
                      "debrief that walks through exactly where it went wrong. Handled well it is the "
                      "most powerful teaching moment in the product. Handled badly it is cruel and "
                      "people quit. It is not possible at all in the entry modules.", tw - 28, REG, 9.2, 12.6)

# ladder
by = 1.02 * inch
kicker(M, by + 1.34 * inch, "THE RESIDENCY LADDER  ·  ORDERED BY ANATOMICAL DEMAND, NOT BY DRAMA")
rungs = [("01", "Open appendectomy", "built"), ("02", "Tube thoracostomy", "built"),
         ("03", "Lap cholecystectomy", "Calot's triangle"), ("04", "Inguinal hernia", "next"),
         ("05", "Bowel anastomosis", "next"), ("06", "Trauma / ortho / vascular", "branch"),
         ("07", "Cardiac and neuro", "top of ladder")]
bw = (PW - 2 * M - 6 * 6) / 7
bx = M
for n, name, note in rungs:
    built = note == "built"
    c.setFillColor(DEEP if built else HexColor("#EFEBE2"))
    c.roundRect(bx, by, bw, 1.06 * inch, 6, stroke=0, fill=1)
    if not built:
        c.setStrokeColor(RULE); c.setLineWidth(0.7)
        c.roundRect(bx, by, bw, 1.06 * inch, 6, stroke=1, fill=0)
    c.setFont(H1, 13)
    c.setFillColor(TEAL if built else HexColor("#B6BEC2"))
    c.drawString(bx + 9, by + 1.06 * inch - 20, n)
    c.setFont(BOLD, 7.4)
    c.setFillColor(HexColor("#EDF3F4") if built else INK)
    yy = by + 40
    for ln in wrap_lines(name, BOLD, 7.4, bw - 18):
        c.drawString(bx + 9, yy, ln); yy -= 9
    c.setFont(REG, 6.6)
    c.setFillColor(TEAL if built else MUT)
    c.drawString(bx + 9, by + 11, note.upper())
    bx += bw + 6
footer("TRAUMA · LADDER")
c.showPage()

# ══════════════════════════════ 6 · TEACH ONE / COMPETITION ══════════════════
bg()
kicker(M, PH - M, "PHASE 4  ·  THE DIFFERENTIATED MECHANIC")
c.setFont(H1, 25)
c.setFillColor(INK)
c.drawString(M, PH - M - 32, "Teach one is the phase that makes")
c.drawString(M, PH - M - 60, "the whole thing worth building.")
rule(M, PH - M - 78, 2.1 * inch, TEAL, 1.6)

ph_h = 4.35 * inch
py = PH - M - 100 - ph_h
w1 = phone(IMG["06-teach-one"], PW - M - ph_h * 390 / 844, py, ph_h)
tw = PW - 2 * M - w1 - 0.34 * inch
y = para(M, py + ph_h - 4, "A junior asks a question and the learner has to answer it. Not “what is the "
                            "next step” but “why is the incision oblique,” “trace this artery back to the "
                            "aorta,” “your junior cannot find the appendix, what is the landmark.”", tw, BOLD, 10.6, 14.8)
y -= 10
y = para(M, y, "Being able to perform a procedure and being able to be responsible for someone else "
               "performing it are different competencies. Almost nothing on the market tests the "
               "second one. It is worth the most points in the game — forty a step, against "
               "twenty-five for operating alone — because it is the harder thing.", tw)
y -= 14
kicker(M, y, "COMPETITION  ·  THREE FORMATS ON ONE CASE SEED")
y -= 20
for head_, body in [
    ("Same team, same case",
     "Two to four players in one OR with real roles — primary surgeon, first assist, scrub, and "
     "someone running the anaesthetic. The surgeon calls for an instrument and a human being has "
     "to hand it over. This is the format that will actually get played, because it recreates the "
     "thing that makes an OR interesting: a team performing under pressure."),
    ("Head to head",
     "Same patient, same seed, separate runs. Fewest errors wins; time breaks the tie. Errors "
     "first and time second, always, in that order. If speed wins outright you have built a game "
     "that teaches people to rush, which is the exact opposite of the intent."),
    ("Ladder",
     "Seasonal ranking across a school or a program, acuity-weighted so the leaderboard rewards "
     "people taking hard cases well rather than farming easy ones fast."),
]:
    c.setFont(BOLD, 9.8)
    c.setFillColor(INK)
    c.drawString(M, y, head_)
    y = para(M, y - 14, body, tw, REG, 9.2, 12.8)
    y -= 10

y -= 4
c.setFillColor(HexColor("#EFEBE2"))
c.roundRect(M, y - 1.46 * inch, tw, 1.46 * inch, 8, stroke=0, fill=1)
kicker(M + 14, y - 20, "THE AI ATTENDING IS A CHARACTER")
para(M + 14, y - 40, "It should read as imposing, precise, and worth impressing — armored, mechanical, "
                     "deliberate in how it moves and speaks. One practical caution: build it as an "
                     "original design. A character that reads as a specific existing film robot is a "
                     "trademark and copyright exposure that would follow the product into every "
                     "funding conversation and every app store review, and it is entirely avoidable "
                     "at the concept-art stage. The silhouette can carry the same weight without "
                     "borrowing anyone's.", tw - 28, REG, 9.2, 12.6)
footer("TEACH ONE")
c.showPage()

# ══════════════════════════════ 7 · BUILD NOTES ══════════════════════════════
bg()
kicker(M, PH - M, "FOR WHOEVER BUILDS THIS")
c.setFont(H1, 25)
c.setFillColor(INK)
c.drawString(M, PH - M - 32, "Build notes and honest costs.")
rule(M, PH - M - 50, 2.1 * inch, TEAL, 1.6)

colw = (PW - 2 * M - 0.42 * inch) / 2
yL = PH - M - 82
kicker(M, yL, "SOURCED ANATOMY, NOT MODELLED ANATOMY", AMBER)
yL = para(M, yL - 20, "This is the single most important production decision in the project, and the "
                      "first prototype got it wrong. Anatomy built from geometric primitives — a "
                      "sphere for a cecum, a torus for a taenia — fails on sight with the exact "
                      "audience the product needs, and no engine choice fixes it.", colw)
yL -= 8
yL = para(M, yL, "Anatomy must be sourced, not authored. Three viable routes:", colw, BOLD)
yL -= 4
for t in [
    "Z-Anatomy / BodyParts3D — an open 3D atlas of over 7,000 labelled structures derived from "
    "real scan data, exportable to glTF. Licensed CC BY-SA, which is copyleft; whether share-alike "
    "encumbers a commercial product built around it is a question for counsel before committing.",
    "NLM Visible Human Project — public-domain cryosection, CT and MRI data. No license required "
    "since 2019. Photographs of an actual human, which is why nothing rendered competes with it "
    "for the study cards.",
    "Real operative video for See One — surgeons already learn this way, so it is the format the "
    "audience trusts by default. SURGhub, the UN's surgery learning hub, publishes a free acute "
    "appendicitis course with appendectomy footage.",
]:
    c.setFillColor(TEAL)
    c.circle(M + 3, yL - 3.4, 1.9, stroke=0, fill=1)
    yL = para(M + 12, yL, t, colw - 12, REG, 9.2, 12.8)
    yL -= 7

yL -= 6
kicker(M, yL, "PLATFORM")
yL = para(M, yL - 18, "Phase 1 is one web build running in the browser on iOS and Android with no "
                      "install. It has to be genuinely good on its own; it is not a demo for a VR "
                      "product. Phase 2 is the same codebase with WebXR — short trigger pull "
                      "identifies, long pull performs. Phase 3 is Bluetooth instrument replicas: "
                      "optional, like a stylus, and last because it is hardest.", colw, REG, 9.4, 13.2)

xR = M + colw + 0.42 * inch
yR = PH - M - 82
kicker(xR, yR, "WHAT EXISTS TODAY")
yR = para(xR, yR - 20, "Two working browser modules — an open appendectomy via McBurney gridiron "
                       "incision, and a tube thoracostomy for tension pneumothorax. The second "
                       "adds a live vitals monitor driven by an obstructive-shock model, an "
                       "anaesthesia character who calls out physiology, and patient death as a "
                       "real fail state. Both are anatomy-fact-checked and both have been driven "
                       "headlessly by a test harness that checks for softlocks, exact scoring and "
                       "arrest timing.", colw, REG, 9.8, 13.8)
yR -= 6
yR = para(xR, yR, "Modules are data — layers, structures, brief, steps, tray — sitting on a shared "
                  "engine, but the engine is copy-pasted per module rather than extracted. Extract "
                  "it before module four.", colw, IT, 9.8, 13.8)
yR -= 10

PROVE = [("1", "Does identify-before-you-cut teach anatomy better than a labelled diagram? "
               "Testable with a pre/post quiz and forty students, for almost nothing."),
         ("2", "Does Teach One retain people? It is the differentiated mechanic and the "
               "untested one."),
         ("3", "Will a surgical educator put their name on the content? One named academic "
               "surgeon reviewing the general surgery track is worth more than the entire "
               "market-size section of the old plan.")]
_wrapped = [(n, wrap_lines(t, REG, 8.8, colw - 46)) for n, t in PROVE]
_need = 46 + sum(len(l) * 11.8 + 9 for _, l in _wrapped)
c.setFillColor(DEEP)
c.roundRect(xR, yR - _need, colw, _need, 8, stroke=0, fill=1)
kicker(xR + 16, yR - 22, "WHAT THIS HAS TO PROVE FIRST", TEAL)
yy = yR - 44
for n, lns in _wrapped:
    c.setFont(H1, 12)
    c.setFillColor(TEAL)
    c.drawString(xR + 16, yy, n)
    c.setFont(REG, 8.8)
    c.setFillColor(HexColor("#C9D6DA"))
    for ln in lns:
        c.drawString(xR + 32, yy, ln)
        yy -= 11.8
    yy -= 9

by = 1.02 * inch
c.setFillColor(HexColor("#EFEBE2"))
c.roundRect(M, by, PW - 2 * M, 1.5 * inch, 8, stroke=0, fill=1)
kicker(M + 18, by + 1.5 * inch - 22, "WHERE THE REWARDS COME FROM")
para(M + 18, by + 1.5 * inch - 42,
     "The endpoint — real merchandise, real scholarships — stays. Who funds it changes. The company "
     "funding scholarships out of a raise makes the rewards a cost centre and the whole thing a "
     "liability. Turn it around: schools, nursing programs, hospital systems, and state or federal "
     "STEM grant programs fund the incentives; the platform administers them and takes a licensing "
     "fee. A nursing school that will pay for a leaderboard prize pool for its own cohort is a far "
     "easier first customer than a sovereign wealth fund, and it is reachable next semester rather "
     "than in five years. Start concrete: a hospital system sponsors a set of loupes for the top "
     "resident in a quarter. A nursing program funds a $500 award. None of that requires a raise, "
     "and all of it builds the evidence the scholarship argument needs at scale.",
     PW - 2 * M - 36, REG, 9.2, 12.8)
footer("BUILD NOTES")
c.showPage()

# ══════════════════════════════ 8 · BACK ══════════════════════════════
bg(dark=True)
c.setFillColor(DEEP)
c.rect(0, PH - 3.1 * inch, PW, 3.1 * inch, stroke=0, fill=1)
kicker(M, PH - 1.0 * inch, "AI SURGEON", TEAL, 8.4)
c.setFont(H1, 30)
c.setFillColor(HexColor("#EDF3F4"))
c.drawString(M, PH - 1.62 * inch, "The game will not let you cut")
c.drawString(M, PH - 2.02 * inch, "something you have not studied.")
c.setFont(REG, 11)
c.setFillColor(HexColor("#9FB3B9"))
c.drawString(M, PH - 2.52 * inch, "Everything else in the design follows from that one sentence.")

y = PH - 3.8 * inch
kicker(M, y, "CONTACT")
c.setFont(BOLD, 13)
c.setFillColor(HexColor("#EDF3F4"))
c.drawString(M, y - 24, "Jonathan Simons, CRNA")
c.setFont(REG, 10.4)
c.setFillColor(HexColor("#9FB3B9"))
c.drawString(M, y - 42, "Founder, Simons Medical Innovations, LLC")
c.drawString(M, y - 58, "simonsmedical@icloud.com")

y -= 96
rule(M, y, PW - 2 * M, HexColor("#22333D"))
y -= 26
kicker(M, y, "A NOTE ON THIS DOCUMENT", HexColor("#7C9299"))
y = para(M, y - 20, "This brochure follows the August 2026 scoped concept, which supersedes the earlier "
                    "master business plan. Screen designs are final-intent; the anatomy shown in them "
                    "is placeholder, and the production art must come from the sourced datasets named "
                    "on the previous page rather than be modelled from scratch.",
         PW - 2 * M, REG, 9.6, 13.6, HexColor("#8FA5AC"))
y -= 8
y = para(M, y, "Market figures from the original business plan are deliberately absent here. Several of "
               "them — the VR-medical-training market size, the “37% better” laparoscopic claim, and the "
               "2025 to 2027 revenue projections — need re-verification against primary sources or "
               "removal before any version of this goes to an outside reader. Nothing in this document "
               "depends on them.",
         PW - 2 * M, REG, 9.6, 13.6, HexColor("#8FA5AC"))
footer("BACK", dark=True)
c.showPage()

c.save()
print("wrote AI-Surgeon-Brochure.pdf")
