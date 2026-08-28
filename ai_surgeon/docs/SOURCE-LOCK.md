# AI Surgeon — what the final docs locked

Desk map of the 28 Aug 2026 user drop. Independent of ChatVault, Domain Architect, RH, and NS. **Not a medical-device claim.**

## Files in this tree

| File | Role |
|---|---|
| `bible/AI-Surgeon-Final-Final.pdf` | Canonical **“AI surgeon final final”** (Pages → PDF, 11 pages, 19 Feb 2025). Investor / education-gaming plan. |
| `bible/AI-Surgeon-Final-Final.pages` | Same document as Apple Pages. |
| `bible/AI-Surgeon-Final-Final.extracted.txt` | `pdftotext` of the canonical PDF. |
| `bible/AI-Surgeon-Final-Final.pages.extracted.txt` | Readable extract from the `.pages` zip/IWA (same body). |
| `bible/AI-Surgeon-Final-With-Citations.txt` | “Final with citations” — same plan plus Section 11 sources. |
| `bible/AI-Surgeon-VR-Business-Plan.pages` | **bigbiz** — longer investor draft (“AI Surgeon VR Business Plan”). |
| `bible/AI-Surgeon-VR-Business-Plan.extracted.txt` | IWA extract of bigbiz. |
| `bible/claude_ai.pdf` | Screenshot of a Claude chat, 14 Mar 2025. |
| `CITATIONS.md` | Named sources only. |
| `AI-Surgeon-Storyboard.pdf` | August 2026 product storyboard (sibling ingest). **Supersedes VR-first framing for what to build.** |
| `AI-Surgeon-Systems-and-Progression.md` | Scoring, coherence, teach-one, handover (sibling ingest). |

The 2025 “final final” PDF is the **business bible**. The August 2026 storyboard is the **product bible** for modules, phases, and hardware order. Where they conflict, the hub follows the storyboard for *what ships*, and archives the 2025 plan without pretending it is the current raise.

## Voice

**2025 plans:** investor-hype. “Fortnite of VR education,” “kids addicted to being smart,” $500M (bigbiz also floats $1B then $500M) AAA raise, esports scholarships, BlueTools.

**August 2026 desk (storyboard / systems / brochure):** OR-literate, specific, small-team. “The game will not let you cut something you cannot name.” Phone first. Four to six modules. Identify before you cut. Teaching is worth the most points. Anatomy sourced, not modelled.

**Hub copy uses the 2026 desk voice.** The 2025 voice stays in `bible/`.

## Claims the 2025 plans make (archived, not repeated as current facts)

- AAA VR surgical game with AI attendings, haptics, multiplayer, scholarships.
- Markets: $5.1B VR medical training (2024), $50.3B VR gaming, etc.
- Revenue years 2024–2027 totalling up to $200M; break-even Q3 2026.
- Hardware sales, institutional licensing, microtransactions, government funding, merchandise.
- Possible CEUs / certification; military and space-medicine licensing.

## Non-claims (hub and this desk must not say)

- **Not a medical device.** No FDA/510(k)/CE-mark language. The 2025 risk slide mentions “medical device regulations”; that is a risk, not a clearance.
- **Not a clinical reference** and not a substitute for supervised training.
- **Not awarding scholarships, CEUs, or certifications** from this prototype.
- **Not a $500M / Stripe launch.** No checkout. The storyboard says nothing here requires a nine-figure raise.
- **Not a metaverse.** Claude was told “deliver everything in pdf except metaverse stuff.” Surgery Verse on the hub means **two seats on one case**, not a second world.
- **Not claiming we measured** 60% engagement, 230% skill retention, or 37% laparoscopic improvement. Those numbers are *named in the plans*; the 2026 brochure says several of them need re-verification.
- **Do not steal credit.** Clinical content and design: Jonathan Simons, CRNA. Named papers stay attributed to the publishers listed in `CITATIONS.md`.

## Module list and progression

Four phases on every case: **Study one → See one → Do one → Teach one.**

Residency ladder as already on the hub (sibling curriculum numbering — not rewritten):

| Status | Module | Notes |
|---|---|---|
| Pitch / stub | 00.1–00.5 Skills lab | Knots, suturing, sterile technique, the tray, local blocks. |
| Pitch / stub | 01 I&D of a finger | Next real case to build (hub). Storyboard’s “Module 01” is the appendectomy *as a vertical slice* — different numbering; do not clobber. |
| **Playable** | 12 Open appendectomy | McBurney gridiron. Patient loss **disabled**. |
| Pitch / stub | Lap cholecystectomy, inguinal hernia, bowel anastomosis | Named on the brochure ladder; not built. |
| **Playable** | 21 Tube thoracostomy | Trauma. Live vitals. Patient loss **enabled**. |
| Pitch / stub | 22 Cricothyroidotomy | Two seats on the airway. |
| Pitch / stub | 24 Damage-control laparotomy | |
| Pitch / stub | 41 CABG, 43 Craniotomy | Chief / top of ladder. |
| Pitch / stub | Anaesthesia track (“Blame Anesthesia”) | Parallel ladder, head of the bed. |

Brochure also orders 01 appendectomy → 02 tube → 03 lap chole → 04 hernia → 05 anastomosis → 06 trauma/ortho/vascular → 07 cardiac/neuro. Hub keeps sibling year numbers and adds the missing brochure names as **honest stubs**.

## Scoring, coherence, death-enabled

Locked in storyboard + systems (and already on the hub):

- Study 10 / card (gated). See 5 / step. Do 25 / step. Teach 40 / step.
- Identify before you cut: gesture stays locked until the structure is named.
- **Twist to choose, touch to commit** (screens catalog / phone stills). Swipe, two-finger spread, pinch, press-and-hold to act on the playable HTML modules.
- Acuity multiplies reward **and** penalty (routine ×1.0 … septic ×2.5; trauma ×2.0).
- Coherence = accuracy + hesitation; high coherence removes hints, tightens gestures, speeds deterioration. Load is a second axis: accurate-and-overloaded is held, not pushed.
- Patient death voids the case. **Disabled in entry modules. Enabled from trauma onward.**
- Handover inside the window beats staying and getting away with it.
- Current Teach One in HTML is still a placeholder quiz; the real “supervise a junior” version is specified, not shipped.

## Hardware ladder

**Locked for the desk:** phone → tablet + mat → VR.

- **Phone:** browser, no install. Storyboard: “this is a phone product.” 2025 plan already lists a non-VR mobile version.
- **Tablet + mat:** larger field plus optional Bluetooth instrument replicas (2025 “BlueTools” / haptic toolkit $299–$999). Not shipped. Optional, like a stylus.
- **VR:** same codebase (WebXR), later phase, not a second raise.

## Surgery Verse seats

The phrase **“Surgery Verse”** is on the August 2026 stills catalog (`stills/07-surgery-verse.png`) and in `screens_engine.py`. It does **not** appear in the 2025 PDF / citations txt / bigbiz / Claude screenshot.

Locked seats: **surgeon, anaesthesia, scrub** — two (or three) seats on one case seed, not two products, not a metaverse. Claude: **do not deliver a metaverse.** Hub treats Verse as the seat name.

Catalog line: “Surgery and anaesthesia are two seats of the same case, not two products.”

## Who pays, what ships first (bigbiz + 2026 brochure — hub copy only)

**Who pays (plans):** institutional subscriptions (schools, hospitals), government/STEM grants, hardware, software licensing, optional consumer subscription, advertiser-funded prizes, esports sponsorships. Brochure correction: *schools / nursing programs / hospital systems / STEM grants fund incentives; the platform licenses.* Do not fund scholarships out of a vanity raise.

**What ships first:** the phone hub with a handful of modules. Not a store, not Stripe, not pre-orders, not a 2024 “full product launch” date that has already passed.

## Claude PDF — constraints and mistakes to avoid

`bible/claude_ai.pdf` is **not** a generated business plan. It is a screenshot of Claude saying it cannot export a PDF, plus Jon’s instruction:

> deliver everything in pdf except metaverse stuff

Constraints taken from that:

1. Do not ship metaverse / second-world copy.
2. Do not treat “I am generating the PDF now” as a delivered spec — that chat **failed to produce the file**.
3. Do not claim Claude authored the canonical plan; the canonical file is the Pages/PDF bible above.

## What this agent changed vs left alone

**Changed:** `index.html` copy (voice, identify-before-you-cut, hardware ladder, two seats, cite strip, who-pays, extra honest stubs). Docs bible + `CITATIONS.md`. Tests for those invariants.

**Left as sibling playable cases:** `ai-surgeon-prototype.html`, `ai-surgeon-module02-trauma.html`, `ai-surgeon-systems.js` — labels/copy on the hub only, not a game rewrite.

**Left as stubs:** skills lab, finger I&D, lap chole, hernia, anastomosis, cric, DCL, CABG, craniotomy, anaesthesia track, tablet+mat, Surgery Verse seats.
