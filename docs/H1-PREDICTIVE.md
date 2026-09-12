# H1 — shape 3, predictive

12 September 2026. Dynamics door. **Not a theorem.
H1 is not proved. NS is not solved.**

Started H1 here. Not from ABC_λ.
Do not glue to Lemma★. Do not emit H1.

Probe: `python3 scripts/h1_predictive.py`

---

## What “predictive” is

The Constantin–Fefferman direction law
\[
D_t\xi=S\xi-(\xi\cdot S\xi)\xi
\]
forecasts whether a Bad pair stays Bad.
Waiting is the viscous core time \(\tau=\rho^2/\nu\),
not an imposed Burgers lock.

Shape 3 claims NSE *forbids* persistent sheets
and gaps on that scale. This file tests the
reduced ODE (Rosenhead Biot–Savart two-blob
+ viscous core), not NSE.

Pictures: fold, sheet, gap. Not ABC.

Bad cut (conventional, not the CF paper
constant): holder
\(|\sin\varphi|/\sqrt{\mathrm{sep}/\rho}\)
above \(C_\star=0.35\).

---

## What ran

\(\rho=0.25\), \(\Gamma=1\), \(\nu=0.02\),
\(\tau=3.125\), horizon \(4\tau\).

| picture | holder \(0\to 4\tau\) | stayed Bad | amp end |
|---|---|---|---|
| fold | \(1.00\to 0.964\) | yes | \(0.27\) |
| sheet | \(0.707\to 0.707\) | yes | \(0.34\) |
| gap | \(0.408\to 0.408\) | yes | \(0.34\) |

Alignment is frozen. Viscosity lowers
circulation. The Hölder ratio does not drop
through the cut. The ODE does not forbid
sheets or gaps on \(4\tau\).

---

## Score

| claim | verdict |
|---|---|
| \(\lvert\xi\rvert=1\) along the ODE | **pass** (identity) |
| not started from ABC_λ | **pass** |
| waiting is \(\rho^2/\nu\), not Burgers \(\gamma\) | **pass** (still not a derived NSE time) |
| ODE forbids a persistent Bad gap | **fail** |
| ODE forbids a persistent Bad sheet | **fail** |
| shape 3 sits | **fail** |
| this closes H1 / WRITE (6) | **fail** |
| glue to Lemma★ | **fail** |

Shape 3 remains a miss. H1 is still the leftover.

A later NSE run on the same three pictures
would be a different test. This ODE is not
that run. Do not cash frozen alignment as
a kill of NS. Do not cash viscous amp drop
as depletion of \(\xi\).

---

## Honesty

- H1 not proved.
- WRITE (6) open.
- Do not start H1 from ABC screenshots.
- Do not add \(K(t)\).
- If H1 sits and H2-from-energy does not,
  the cylinder is still open.

Object: [`H1-OBJECT.md`](H1-OBJECT.md).
Shapes: [`H1-SHAPES.md`](H1-SHAPES.md).
Tube snapshots (other door): [`H1-TUBE.md`](H1-TUBE.md).

NS not solved.
