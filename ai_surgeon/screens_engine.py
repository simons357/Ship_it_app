"""Scoring and interaction rules for the phone stills screens.

Independent of the ingested appendectomy / Module 21 trauma prototypes.
Those modules keep their own engine (`ai-surgeon-systems.js`,
`trauma_physiology.js`). This file is the testable source of truth for
identify-before-cut, Study/See/Do One, The Lab, The Pen, The Nib, Verse,
and the Case 07 phone still.

Not a medical device. Not a claim of regulatory clearance.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Iterable

IDENTIFY_HIT = 15
IDENTIFY_MISS = -5
STUDY_PER_CARD = 10
SEE_PER_STEP = 5
DO_PER_STEP = 25
TEACH_PER_STEP = 40
WRONG_INSTRUMENT = -10
WRONG_PHYSIOLOGY = -25
FLUID_BOLUS_PENALTY = -25

AIRWAY_TOOLS = ("MASK", "LMA", "ETT")
NIB_TRAY = ("SCALPEL", "FORCEPS", "CLAMP", "DRIVER", "SPONGE")
LAB_LAYERS = (
    "peritoneum",
    "bowel_wall",
    "mesoappendix",
    "arteries",
    "lymphatics",
    "nerves",
)
FIELD_LAYERS = frozenset({"peritoneum", "bowel_wall", "mesoappendix"})
ADD_LAYERS = frozenset({"peritoneum", "bowel_wall", "mesoappendix", "arteries"})
SUBTRACT_LAYERS = frozenset({"bowel_wall", "arteries"})

VERSE_SEATS = ("surgeon", "anaesthesia", "scrub")
VERSE_CASES = (
    "Appendectomy",
    "Lap chole",
    "Bowel obstruction",
    "Tension pneumo",
    "C-section",
    "Trauma lap",
    "CABG",
    "Ruptured AAA",
)

# Normalized ellipses on stills/06-cecum-appendix-b.png (760×900).
# First match wins, so the appendix is listed before the cecum.
IDENTIFY_REGIONS: tuple[dict[str, Any], ...] = (
    {"id": "appendix", "cx": 0.64, "cy": 0.74, "rx": 0.20, "ry": 0.18},
    {"id": "mesoappendix", "cx": 0.48, "cy": 0.60, "rx": 0.15, "ry": 0.13},
    {"id": "ileum", "cx": 0.22, "cy": 0.36, "rx": 0.18, "ry": 0.16},
    {"id": "cecum", "cx": 0.50, "cy": 0.36, "rx": 0.32, "ry": 0.30},
)

IDENTIFY_COPY = {
    "appendix": {
        "label": "Appendix",
        "sub": "CONFIRMED",
        "footer": "Appendix. Base at the taenia. Scalpel unlocked.",
    },
    "cecum": {
        "label": "Cecum",
        "sub": "NOT THE TARGET",
        "footer": "That is the cecum. Follow the taenia down: -5",
    },
    "mesoappendix": {
        "label": "Mesoappendix",
        "sub": "NOT THE TARGET",
        "footer": "That is the mesoappendix. The appendix is the tube: -5",
    },
    "ileum": {
        "label": "Terminal ileum",
        "sub": "NOT THE TARGET",
        "footer": "That is the ileum. The appendix hangs off the cecum: -5",
    },
    "field": {
        "label": "Field",
        "sub": "NOT A STRUCTURE",
        "footer": "Touch the organ, not the drape: -5",
    },
}

STUDY_CARDS: tuple[dict[str, Any], ...] = (
    {
        "id": 1,
        "title": "Anatomy",
        "prompt": "Where do the three taeniae of the cecum converge?",
        "options": (
            {"id": "A", "text": "At the ileocecal valve", "correct": False},
            {"id": "B", "text": "At the base of the appendix", "correct": True},
            {"id": "C", "text": "At the hepatic flexure", "correct": False},
        ),
        "explain": "All three taeniae meet at the appendiceal base. That is the landmark.",
    },
    {
        "id": 2,
        "title": "McBurney",
        "prompt": "A gridiron incision splits which layers?",
        "options": (
            {"id": "A", "text": "External oblique, internal oblique, transversus — split, not cut", "correct": True},
            {"id": "B", "text": "Rectus sheath, then peritoneum in the midline", "correct": False},
            {"id": "C", "text": "Skin, then a muscle-cutting Kocher", "correct": False},
        ),
        "explain": "McBurney is split, not cut. Cutting the muscle is a different operation.",
    },
    {
        "id": 3,
        "title": "Pathophysiology",
        "prompt": "The lumen obstructs. Pressure rises past venous before arterial. So which comes first?",
        "options": (
            {"id": "A", "text": "Arterial ischaemia, then venous congestion", "correct": False},
            {"id": "B", "text": "Venous congestion, then arterial ischaemia", "correct": True},
            {"id": "C", "text": "Simultaneous — the wall fails all at once", "correct": False},
        ),
        "explain": "Correct. Congestion precedes ischaemia.",
    },
    {
        "id": 4,
        "title": "Referred pain",
        "prompt": "Why periumbilical first, then right lower quadrant?",
        "options": (
            {"id": "A", "text": "The appendix migrates during the attack", "correct": False},
            {"id": "B", "text": "Visceral afferents first (midgut / T10), then parietal peritoneum", "correct": True},
            {"id": "C", "text": "The ileocolic artery spasms, then the lumbar nerves", "correct": False},
        ),
        "explain": "Visceral midgut pain is periumbilical. Once the parietal peritoneum is involved it localises to the RLQ.",
    },
)

DO_ONE_OPTIONS: tuple[dict[str, Any], ...] = (
    {"id": "mesoappendix", "text": "Mesoappendix, carrying the appendicular artery", "points": 25, "correct": True},
    {"id": "taenia", "text": "Taenia libera", "points": -10, "correct": False},
    {"id": "ileocolic", "text": "Ileocolic artery", "points": -25, "correct": False, "wrong_structure": True},
    {"id": "peritoneum", "text": "Peritoneal reflection", "points": -10, "correct": False},
)

STERILE_TABLE: tuple[dict[str, Any], ...] = (
    {"id": "hemostat", "name": "Hemostat", "note": "Kelly / mosquito", "correct_for": "open_peritoneum"},
    {"id": "metz", "name": "Metzenbaum scissors", "note": "sharp dissection", "correct_for": "aponeurosis"},
    {"id": "babcock", "name": "Babcock clamp", "note": "delivers the cecum", "correct_for": "deliver_cecum"},
    {"id": "retractor", "name": "Army-Navy retractor", "note": "wound edge", "correct_for": "retract"},
    {"id": "vicryl", "name": "0-Vicryl on driver", "note": "fascial closure", "correct_for": "close"},
    {"id": "bovie", "name": "Bovie", "note": "electrocautery", "correct_for": "hemostasis"},
)

SEE_STRUCTURES: tuple[dict[str, str], ...] = (
    {
        "id": "external_oblique",
        "name": "External oblique",
        "why": "Outermost flat muscle. Split with the fibres, not across them.",
    },
    {
        "id": "internal_oblique",
        "name": "Internal oblique",
        "why": "Middle layer. Fibres run opposite the external. Still split.",
    },
    {
        "id": "transversalis",
        "name": "Transversalis fascia",
        "why": "Under it, preperitoneal fat, then peritoneum. Split muscle, do not cut it.",
    },
)

GESTURES = {
    "swipe": "incise",
    "two-finger": "split / retract",
    "pinch": "clamp",
    "hold": "ligate",
}

LEGAL_TRAY_BY_STEP = {
    "ligate_the_base": ("SCALPEL", "CLAMP", "DRIVER"),
    "identify": (),
    "open_peritoneum": ("CLAMP",),
}


def _in_ellipse(nx: float, ny: float, region: dict[str, Any]) -> bool:
    dx = (nx - region["cx"]) / region["rx"]
    dy = (ny - region["cy"]) / region["ry"]
    return dx * dx + dy * dy <= 1.0


def hit_structure(nx: float, ny: float, regions: Iterable[dict[str, Any]] | None = None) -> str:
    """Map a normalized (0–1) touch to a named structure. Misses the field."""
    if not (0.0 <= nx <= 1.0 and 0.0 <= ny <= 1.0):
        return "field"
    for region in regions or IDENTIFY_REGIONS:
        if _in_ellipse(nx, ny, region):
            return str(region["id"])
    return "field"


def identify_touch(nx: float, ny: float, target: str = "appendix") -> dict[str, Any]:
    grabbed = hit_structure(nx, ny)
    hit = grabbed == target
    copy = IDENTIFY_COPY.get(grabbed, IDENTIFY_COPY["field"])
    return {
        "state": "HIT" if hit else "MISS",
        "grabbed": grabbed,
        "target": target,
        "points": IDENTIFY_HIT if hit else IDENTIFY_MISS,
        "label": copy["label"],
        "sub": copy["sub"],
        "footer": copy["footer"],
        "unlocks": ("SCALPEL",) if hit else (),
        "advance": hit,
    }


def grade_study_card(card_id: int, choice: str) -> dict[str, Any]:
    card = next(c for c in STUDY_CARDS if c["id"] == card_id)
    option = next(o for o in card["options"] if o["id"] == choice)
    return {
        "card_id": card_id,
        "choice": choice,
        "correct": bool(option["correct"]),
        "points": STUDY_PER_CARD if option["correct"] else 0,
        "explain": card["explain"] if option["correct"] else "Review it. The attending will ask again mid-case.",
        "text": option["text"],
    }


def study_gate(completed_correct: int, total: int = 4) -> dict[str, Any]:
    done = completed_correct >= total
    return {
        "completed": completed_correct,
        "total": total,
        "scrub_unlocked": done,
        "banner": (
            "SCRUB UNLOCKED · 4 of 4 cards complete"
            if done
            else f"LOCKED · You cannot scrub in until {total} of {total} cards are complete."
        ),
    }


def name_before_divide(choice_id: str) -> dict[str, Any]:
    option = next(o for o in DO_ONE_OPTIONS if o["id"] == choice_id)
    return {
        "choice": choice_id,
        "correct": bool(option["correct"]),
        "points": int(option["points"]),
        "unlock_gesture": bool(option["correct"]),
        "wrong_structure": bool(option.get("wrong_structure")),
        "text": option["text"],
    }


def apply_gesture(named: bool, gesture: str, required: str = "hold") -> dict[str, Any]:
    if not named:
        return {"ok": False, "points": 0, "reason": "Name it before the instrument unlocks."}
    if gesture != required:
        return {"ok": False, "points": 0, "reason": f"Wrong maneuver. This step is {GESTURES[required]} ({required})."}
    return {"ok": True, "points": DO_PER_STEP, "reason": "Hold until the knot seats."}


def call_for_instrument(step: str, instrument_id: str) -> dict[str, Any]:
    item = next(i for i in STERILE_TABLE if i["id"] == instrument_id)
    correct = item["correct_for"] == step
    return {
        "instrument": item["name"],
        "correct": correct,
        "points": DO_PER_STEP if correct else WRONG_INSTRUMENT,
        "scrub": (
            "Two hemostats. Careful, they're loaded."
            if correct and instrument_id == "hemostat"
            else (
                f"{item['name']}. That is not what was asked."
                if not correct
                else f"{item['name']} up."
            )
        ),
    }


def lab_preset(name: str) -> frozenset[str]:
    key = name.strip().upper()
    if key == "FIELD":
        return FIELD_LAYERS
    if key == "ADD":
        return ADD_LAYERS
    if key == "SUBTRACT":
        return SUBTRACT_LAYERS
    raise ValueError(f"unknown lab preset: {name}")


def toggle_layer(active: Iterable[str], layer: str) -> frozenset[str]:
    if layer not in LAB_LAYERS:
        raise ValueError(f"unknown layer: {layer}")
    cur = set(active)
    if layer in cur:
        cur.remove(layer)
    else:
        cur.add(layer)
    return frozenset(cur)


def classify_lab(active: Iterable[str]) -> str:
    s = frozenset(active)
    if s == FIELD_LAYERS:
        return "FIELD"
    if s == ADD_LAYERS:
        return "ADD"
    if s == SUBTRACT_LAYERS:
        return "SUBTRACT"
    return "CUSTOM"


def twist_index(current: int, delta: int, n: int) -> int:
    if n <= 0:
        raise ValueError("empty tray")
    return (current + delta) % n


def touch_commit(options: tuple[str, ...], index: int) -> str:
    if not options:
        raise ValueError("nothing to commit")
    return options[index % len(options)]


def legal_tray(step: str) -> tuple[str, ...]:
    legal = LEGAL_TRAY_BY_STEP.get(step)
    if legal is None:
        return NIB_TRAY
    if not legal:
        return ()
    return tuple(t for t in NIB_TRAY if t in legal)


def verse_view(seat: str) -> dict[str, Any]:
    if seat not in VERSE_SEATS:
        raise ValueError(f"unknown seat: {seat}")
    return {
        "surgeon": {
            "sees_field": True,
            "sees_numbers": False,
            "sees_both": False,
            "prompt": "You cannot see the pressure.",
            "action": "Call for the 2-0 tie.",
        },
        "anaesthesia": {
            "sees_field": False,
            "sees_numbers": True,
            "sees_both": False,
            "prompt": "You cannot see the bleeder.",
            "action": "Tell him. Do not just treat it.",
        },
        "scrub": {
            "sees_field": True,
            "sees_numbers": True,
            "sees_both": True,
            "prompt": "You can see both of them.",
            "action": "Slap it in his hand.",
        },
    }[seat]


def verse_spin(index: int, delta: int = 1) -> str:
    return VERSE_CASES[twist_index(index, delta, len(VERSE_CASES))]


def propofol_rate(twist: float) -> dict[str, Any]:
    """Twist is the plunger. Values are mg/kg push rate, not a menu."""
    rate = max(0.2, min(4.0, round(2.0 + twist, 1)))
    too_fast = rate >= 3.2
    return {
        "dose": f"PROPOFOL {rate:.1f} mg/kg",
        "rate": rate,
        "too_fast": too_fast,
        "pressure": "Push it too fast and the pressure answers you." if too_fast else "Twist = push. Speed is your decision.",
    }


def airway_select(index: int) -> str:
    return AIRWAY_TOOLS[index % len(AIRWAY_TOOLS)]


@dataclass
class TraumaCase07:
    """Phone-still tension pneumothorax. Sibling Module 21 keeps TraumaPhys.

    Brochure numbers: do-nothing arrests in 56–78s (coherence runs the
    clock). Needle buys 67–110s. Tube is definitive. Fluid is the wrong
    physiology. Death is enabled.
    """

    coherence: float = 44.0
    acuity: float = 2.5
    elapsed: float = 0.0
    needle: bool = False
    tube: bool = False
    fluid: bool = False
    dead: bool = False
    points: int = 590
    notes: list[str] = field(default_factory=list)

    def arrest_deadline(self) -> float:
        c = max(0.0, min(100.0, self.coherence))
        return 78.0 - 22.0 * (c / 100.0)

    def needle_buy(self) -> float:
        c = max(0.0, min(100.0, self.coherence))
        return 110.0 - 43.0 * (c / 100.0)

    def remaining(self) -> float:
        if self.dead:
            return 0.0
        if self.tube:
            return self.needle_buy()
        base = self.arrest_deadline()
        if self.needle:
            base += self.needle_buy()
        return max(0.0, base - self.elapsed)

    def vitals(self) -> dict[str, Any]:
        t = 1.0 - (self.remaining() / max(self.arrest_deadline(), 1e-6))
        t = max(0.0, min(1.4, t))
        if self.tube:
            return {"hr": 92, "sbp": 118, "dbp": 72, "spo2": 97, "band": "holding"}
        if self.fluid:
            t += 0.15
        hr = int(118 + 40 * t)
        sbp = int(92 - 38 * t)
        dbp = int(58 - 22 * t)
        spo2 = int(94 - 22 * t)
        if self.needle and not self.tube:
            sbp += 8
            spo2 += 4
            hr -= 8
        return {
            "hr": hr,
            "sbp": sbp,
            "dbp": dbp,
            "spo2": max(40, spo2),
            "band": "crashing" if sbp < 80 or spo2 < 85 else "tight",
        }

    def step(self, dt: float) -> "TraumaCase07":
        if self.dead or self.tube:
            return self
        nxt = replace(self, elapsed=self.elapsed + dt, notes=list(self.notes))
        if nxt.remaining() <= 0:
            nxt.dead = True
            nxt.points = 0
            nxt.notes.append("Arrest. Death voids the case score.")
        return nxt

    def act(self, action: str) -> "TraumaCase07":
        if self.dead:
            return self
        nxt = replace(self, notes=list(self.notes))
        if action == "needle":
            if nxt.needle:
                nxt.points += WRONG_INSTRUMENT
                nxt.notes.append("Needle already in. It only buys time.")
                return nxt
            nxt.needle = True
            nxt.points += 10
            nxt.notes.append("Needle decompression, 2nd ICS. Buys time, does not fix it.")
            return nxt
        if action == "tube":
            nxt.tube = True
            nxt.points += int(DO_PER_STEP * nxt.acuity)
            nxt.notes.append("Tube thoracostomy, 5th ICS. Definitive.")
            return nxt
        if action == "fluid":
            nxt.fluid = True
            nxt.points += int(FLUID_BOLUS_PENALTY * nxt.acuity)
            nxt.notes.append("Fluid bolus. Wrong physiology. This is obstructive, not hypovolaemic.")
            return nxt
        raise ValueError(f"unknown action: {action}")


def errors_first(errors_a: int, time_a: float, errors_b: int, time_b: float) -> str:
    """Head-to-head: fewer errors wins; time only breaks ties."""
    if errors_a < errors_b:
        return "a"
    if errors_b < errors_a:
        return "b"
    if time_a < time_b:
        return "a"
    if time_b < time_a:
        return "b"
    return "tie"
