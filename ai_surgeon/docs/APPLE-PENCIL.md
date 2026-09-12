# Apple Pencil — until the custom Pen exists

**THEIRS.** Same instrument language as [`THE-PEN.md`](THE-PEN.md).
Not a second product. Not a tray of toys. **Not a medical device.**

You asked for a design of an Apple Pencil, unless that *is* all of the
surgical instruments. It is. One object. Knife, clamp, retractor,
plunger — by gesture. Use Apple’s hardware until the Chronogate pen
(click cap, knurled twist, squeeze barrel) is in the hand.

---

## The answer

**Yes. Apple Pencil Pro is every instrument until yours is ready.**

Do not ship miniature Kellys, scalpels, or Army-Navys that feel silly
and do not feel like steel. A pencil already lives in a student’s hand.
It will not feel like a clamp. We do not say it does. It will feel like
a pen, which is the whole point of the language.

| Your gesture | What it is in the OR language | Apple Pencil Pro | Until then, on the web |
|---|---|---|---|
| **Twist** | Choose / tray / propofol plunger / MASK·LMA·ETT | **Barrel roll** | Tilt / azimuth change (`pointerType === 'pen'`) |
| **Click the top** | Commit / fire / incise / next | Apple Pencil has **no clicker cap**. Map to **nib tap** (touch to commit). Pencil 2 **double-tap** on the flat is the native stand-in | Short pen tap, low travel |
| **Squeeze** | Clamp / retract / hold-to-ligate | **Squeeze** (Pencil Pro, haptic) | High `pressure` while the nib is down (honest approximation) |
| *(look, don’t cut)* | Identify before you cut | **Hover** over the structure | `pointerType === 'pen'` + hover if the browser reports it |

No fourth gesture family. No double-tap **menus**. Pencil 2’s double-tap
is *click*, not a drawer.

---

## What Apple actually sells (do not invent buttons)

| Hardware | Twist | Squeeze | Click-cap | Hover | Pairs with |
|---|---|---|---|---|---|
| Apple Pencil (1st) | No | No | No | No | Older iPad |
| Apple Pencil USB-C | No | No | No | Hover on supported iPad | iPad (USB-C) |
| Apple Pencil (2nd) | No | No | No — **double-tap** on the flat | Hover on supported iPad | iPad Pro / Air with magnet |
| **Apple Pencil Pro** | **Barrel roll** | **Squeeze** | No — nib tap / squeeze | **Hover** | Current iPad Pro / Air |
| **iPhone** | — | — | — | — | **Does not take Apple Pencil.** Phone v1 stays finger on glass or a cheap capacitive stylus + camera. |

Desk tier ships on **iPad + Apple Pencil Pro**. Phone still ships first
without waiting for Apple or for the custom pen.

Native iPadOS (`UIPencilInteraction`, barrel roll, squeeze haptics) is
the full mapping. Safari on iPad gives `PointerEvent` with
`pointerType === 'pen'`, `pressure`, and sometimes tilt / azimuth.
This repo maps those three. It does **not** pretend Safari exposes
Pencil Pro squeeze as a named Web API.

---

## Custom Pen vs Apple (same three events)

```
  YOURS (later)              APPLE (now)
  click cap          ←→      nib tap  (touch to commit)
  knurled twist      ←→      barrel roll
  squeeze zone       ←→      Pencil Pro squeeze
  nib                ←→      nib
```

Software talks `twist` | `click` | `squeeze` either way.
When your pen exists, swap the hardware. Do not swap the language.

---

## Where it lives

| Path | Role |
|---|---|
| This file | Apple stand-in lock |
| [`THE-PEN.md`](THE-PEN.md) | The language (yours) |
| [`../pen.html`](../pen.html) `#apple-pencil` | Design plate + pointer field |
| [`../art/apple-pencil-pro-instrument.png`](../art/apple-pencil-pro-instrument.png) | Annotated Pencil Pro |
| `AISS.ApplePencil` in [`../ai-surgeon-systems.js`](../ai-surgeon-systems.js) | Web pointer → Pen events |

Not ChatVault. Not Domain Architect. Not a cleared tracker.
Apple, Apple Pencil, and iPad are Apple’s marks. This desk is not
an Apple product and does not claim partnership.
