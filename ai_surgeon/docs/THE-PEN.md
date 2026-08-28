# THE PEN — one object in the hand

**THEIRS. Medical big picture.** Not Harrison’s Lady of the Lake. Not Camelot.
Not ChatVault, not Domain Architect, not RH. **Not a medical device.**

This is the instrument language for AI Surgeon. A pen. A min-movement stylus.
It is the knife. It is the clamp. It is the retractor. Mapped by gesture —
not a tray of toy-size fake instruments that feel silly and would never feel
like the real thing.

A pen already lives in the hand. You can twist it. You can click the top.
You can squeeze it. That is a whole language. Phone ships first. Vision
commands watch the pen and the hand. Mechanical twist / click / squeeze stay
cheap. The camera is a phone-tier extra, not a radio-heavy stylus and not
cleared tracking.

> Software cannot make a phone stylus feel like a Kelly clamp. The Pen is
> the *language*. Life-size steel is the tablet / VR ladder later. v1 is
> min-movement plus vision, not fake mini-tools.

Full lock on voice split: [`VOICE-LOCK.md`](VOICE-LOCK.md). Playable product
voice: [`THEIRS-medical-big-picture.md`](THEIRS-medical-big-picture.md).

---

## Why a pen, not a tray of toys

Everyone is trying to win. The studying is serious. Anatomy is a gate —
study your anatomy. High stakes when it counts. Scores high enough can
unlock “this is medical education.” The product is completely **benign**:
you program it any way you want. It is meant to be entertaining. Always
fun. It still monitors coherence and movement, because fun without a
read on how you are moving is just a cartoon.

Tiny replica instruments fail both tests. They look like toys and they
do not feel like steel. A pen does not pretend. It is one object. The
role changes. The hand does not.

| What you are doing | What the Pen is | Gesture |
|---|---|---|
| Incise / fire / next | Knife | **Click the top** |
| Clamp / retract / ligate | Clamp or retractor | **Squeeze** (hold-to-ligate) |
| Choose / plunger / tray | Selector | **Twist** |

No double-tap menus. No long-press hunting. Three gestures. That is the
whole language.

The anaesthesia still (`screens.html#anesthesia`) is the **same object**:
twist is the plunger, click commits the airway. Module 04 is not a second
pen. It is the Pen at the head of the bed.

---

## Anatomy of the object

Four zones. Nothing else. No radio, no battery, no firmware required for v1.

```
        ┌──── click cap ────┐
        │   COMMIT / FIRE   │   Click the top.
        │   next / incise   │   Detent. One shot.
        └────────┬──────────┘
                 │
        ┌────────┴──────────┐
        │    twist grip     │   Knurled ring.
        │  choose / plunger │   Twist to cycle the tray,
        │   tray summon     │   the dose, the airway.
        ├───────────────────┤
        │   squeeze zone    │   Compliant barrel.
        │ clamp / retract   │   Squeeze to clamp.
        │  hold-to-ligate   │   Hold the squeeze to ligate.
        └────────┬──────────┘
                 │
        ┌────────┴──────────┐
        │        nib        │   Where it points.
        │  the field index  │   Vision sees this first.
        └───────────────────┘
```

**Nib** — the point. The camera (and the player) treat this as where the
instrument is aimed. On a phone without a physical nib, the on-screen
reticle is the stand-in. The still `stills/11-the-nib.png` is this zone.

**Twist grip** — a detent ring you roll with thumb and first finger.
Twist chooses: instrument on the tray, MASK / LMA / ETT, propofol rate.
Twist summons the tray. Eyes stay on the field. The still
`stills/10-twist-stylus.png` is this zone.

**Top click** — a cap you click, like a ballpoint. Commit. Fire. Next.
Incise. You already know this motion. That is the point.

**Squeeze zone** — a slightly soft barrel. Squeeze is clamp. Squeeze is
retract (hold the field). Squeeze and hold is ligate. One pressure
language instead of a handful of toy hemostats.

Phone v1 stand-ins (no physical pen in the box): on-screen Twist / Click /
Squeeze, `Q` `E` for twist, `Enter` / space for click, `F` for squeeze.
The physical pen is the same three events when it exists.

---

## Gesture map

Locked. Do not add a fourth family in v1.

| Gesture | Event name | Means | Maps onto existing actions |
|---|---|---|---|
| **TWIST** | `twist` | Choose. Plunger. Tray summon. | Cycle the legal tray. Propofol rate. Airway MASK/LMA/ETT. |
| **CLICK THE TOP** | `click` | Commit. Fire. Next. Incise. | `swipe` (incise / transect) and `tap` (deliver / confirm). |
| **SQUEEZE** | `squeeze` | Clamp. Retract. Hold-to-ligate. | `pinch` (clamp), `spread` (retract / split), `hold` (ligate). |

On-screen swipe / pinch / spread / hold still work. They are the fallback
for a finger on glass. The Pen language is the one we teach. The fallback
does not get a menu.

**Illegal in v1**

- Double-tap to open a menu.
- Long-press to hunt a tool.
- A drawer of miniature scalpels, Kellys, and Army-Navys you pinch like
  dolls.
- A requirement for VR, a steel mat, or Bluetooth replicas before the
  phone loop works.

---

## See one, then do one

This one teaches you scenarios. You see one first. Then you do one.

1. **Study your anatomy.** The Lab. Layers on, layers off, name the
   structure. Curriculum will not let you skip this. Exploration will,
   because exploration is allowed to be reckless.
2. **See One.** The attending performs the maneuver with the Pen. You
   watch the twist, the click, the squeeze. You name what you are
   looking at while you watch. You do not operate yet.
3. **Do One.** Same scenario. Your Pen. Identify, then gesture. The
   knife is not unlocked until the structure is named.
4. **Teach One** stays the existing phase (placeholder quiz now; real
   supervise-a-junior later). The Pen does not replace it.

High-stakes when it counts. Competitive. Errors first; time only breaks
ties. Always fun — the attending still talks like an attending, the
scrub still refuses the wrong name, and the product never stops being
a game you would actually open.

---

## Two modes

Toggleable on the hub Pen screen and restored from `aiss.mode`.

### Exploration — anything goes, zero penalty

Program it any way you want. Skip the Lab. Skip See One. Mash squeeze
on a click step. The meter still moves. The camera can still watch.
Wrong maneuvers cost **zero**. Death is not enabled here. This is how
you learn the language without being punished for learning it.

Fun is the point. Coherence is still on the screen so you can see what
your hands are doing. It just cannot dock you.

### Curriculum — it counts

You must study in the Lab first. Then you See One. Then you Do One.
Clock, score, and coherence matter. Acuity multiplies reward *and*
penalty. From trauma onward, patient loss is enabled — that is a
teaching rule, not a gore setting. Scores high enough can read as
medical education. The product is still completely benign: a training
simulation, not a cleared device, not a clinical reference, not a
substitute for supervised training.

| Gate | Exploration | Curriculum |
|---|---|---|
| Lab | Optional | **Required** before Do One |
| See One | Optional | **Required** before Do One |
| Penalty on miss | **0** | Full (profile × acuity) |
| Clock | Display only | Runs the case |
| Coherence | Shown, no dock | Tightens gestures / speeds the sick patient |
| Death-enabled | Off | Follows the module (off in entry, on from trauma) |

---

## Coherence and movement

Coherence already measures how right you are and how long you hesitate.
The Pen adds **movement**: tremor from the squeeze, smoothness of the
twist, whether the click was a panic mash.

Two axes, same as the systems note:

| | Settled | Overloaded |
|---|---|---|
| **Accurate** | Push. | Hold. Do not add load. |
| **Struggling** | Push. This is boredom. | Back off. |

In exploration the axes are visible and inert. In curriculum they
change the case. Load is estimated from input timing, path tremor, and
optional phone sensors — derived on device, band only retained. See
`AISS.RETENTION`.

---

## Vision commands

The camera sees the **pen and the hand**. That is the cheap path. It is
not a radio-heavy active stylus. It is not 6-DoF surgical navigation.
It is not FDA-cleared tracking. The code stub (`AISS.Vision`) may open
`getUserMedia` and show the feed. It must not claim pose, tool identity,
or millimetre accuracy.

What vision is allowed to mean in v1:

- The nib is in frame.
- A twist / click / squeeze was seen *or* the mechanical switch fired
  (either source is enough).
- “I lost the pen” — a coaching line, not a clinical alarm.

What vision is **not** allowed to mean:

- “Tracking lock, 0.3 mm.”
- Instrument recognition as a medical claim.
- Anything a school counsel would read as a device function.

Phone-tier cheap: mechanical twist / click / squeeze plus a camera.
If the camera is denied, the Pen still works.

---

## Hardware ladder (honest)

| Tier | What your hands do | Ships |
|---|---|---|
| **Phone** | The Pen language on glass, or a cheap mechanical pen the camera can see. | **v1. First.** |
| **Tablet + mat** | Larger field. Optional life-size steel (the 2025 BlueTools idea). Like a stylus: later, never required. | Not shipped. |
| **VR** | Same codebase, headset. Same score ledger. | Later phase of this build, not a second product. |

v1 does not require VR. v1 does not require a mat of steel toys.

---

## Where it lives in the repo

| Path | Role |
|---|---|
| This file | Design lock |
| [`../pen.html`](../pen.html) | Hub screen: anatomy, mode toggle, See One / Do One / Lab, coherence, vision stub |
| [`../index.html`](../index.html) `#the-pen` | Hub card |
| [`../ai-surgeon-systems.js`](../ai-surgeon-systems.js) | `AISS.Mode`, `AISS.Pen`, `AISS.Coherence`, `AISS.Vision` |
| [`../ai-surgeon-prototype.html`](../ai-surgeon-prototype.html) | Appendectomy — Pen gestures map onto incise / clamp / ligate / retract |
| [`../ai-surgeon-module02-trauma.html`](../ai-surgeon-module02-trauma.html) | Trauma — same mapping, sibling case not rewritten |
| `../stills/10-twist-stylus.png`, `../stills/11-the-nib.png`, `../stills/01-anesthesia-pen.png` | Existing stills. No toy tray invented. |

Engine flags: `exploration` \| `curriculum`. Gesture events: `twist` \|
`click` \| `squeeze`.

---

## Non-claims

- Not a medical device. Not cleared. Not a tracker.
- Not a clinical reference. Not supervised training.
- The Pen does not feel like a Kelly. We do not say it does.
- Harrison’s quotations are not invented here. Lake / mist stay on
  Harrison’s file.
- Not ChatVault, not Domain Architect, not RH, not NS.
