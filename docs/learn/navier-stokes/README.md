# Navier–Stokes, in plain language

**For:** Jonathan Simons  
**What this is:** a teaching pack. Pictures plus short lessons.  
**What this is not:** a proof, a press release, or a claim that anyone here closed the equations.

You already know physiology under pressure. These notes use that same habit: name the law, name what it can do, name what it cannot pretend to be.

Read in this order. Twenty minutes if you only want the news and the “why bother.” Another ten if you sit with the pictures.

1. [What the OpenAI fuss actually is](01-the-news.md) — September 2026, searched, not invented.
2. [Why bother with these equations](02-why-these-equations.md) — what they are, what they can do, honest “is this a waste?”
3. [Pictures](03-pictures.md) — laminar vs turbulent, a control volume, a vortex, the energy cascade.

The same pictures live in [`figures/`](figures/). A small script can redraw the labeled plots: [`scripts/make_figures.py`](scripts/make_figures.py).

---

## How this workspace sits

Keep the split. This pack teaches the continuum law. It does not merge the books.

- **Live product** is Domain Architect: `DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE`.
- **DA-VC-01** (unaugmented Navier–Stokes as a lab challenge) is a **challenge, not PASS**.
- **Book B** leftover \(T_{j\leftarrow j}\) is still **OPEN**. That is the radial stretching \(u^r/r\) that energy does not control. Do not treat a rewrite as a close.
- **Paper2 SND** is **conditional**. Different book from swirl. Different book from Domain Architect.
- Swirl \(\Phi = u_\theta/r\) is **not** Domain Architect’s \(\Phi\). Same letter, different object. Do not glue them.

---

## One shelf note

A recovered equation dump from 14 September stays on the shelf. Unknown author. Not regular work. Not these lessons.

One remark in that dump is ordinary continuum bookkeeping: if a coefficient is constant, a pure gradient can be absorbed into pressure under the usual incompressible projection. That is the same move classical Navier–Stokes already makes. The same remark names an extra “resonance” term; that would be a **changed model**, not the classical law. Neither belongs here as canon.
