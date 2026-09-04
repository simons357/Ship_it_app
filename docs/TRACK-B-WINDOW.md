# Climb sketch as an a priori

`python3 scripts/track_b_window.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B21: ODE and NS readable on \(T=0.064\). Prescribed
\(c=8\) has not reached the viscous room. The sitting
path is not the packet. This write asks whether
matching the sketch closes \(X\). It does not.

---

## The knob on this write

Tesla: the sitting of \(c=8\) is a long ODE. This
window is short. The field did not follow. Cashing
B11c on \(T=0.064\) is a knob.

No \(Q_1\). No \(\varepsilon\). No Biot–Savart slogan.
Do not spawn \(n=64\). Do not write \(c=8\) into the PDE.

---

## What the apparatus does

**B32, pass.** Window rates, missed viscous room, and
sketch-grows / field-falls are readable together.
Same caches as B21. No new FFT.

**B32a, fail** of “matching the sketch closes \(X\).”
ODE \(X\) grows \(2.5\to 2.67\). NS \(X\) falls
\(2.5\to 1.43\). A short window is not the sitting.

**B32b, fail** of “cashing B11c on \(T=0.064\) is
continuation.” Time to \(j=5\) is \(0.375\). This box
is \(0.064\). Do not cash a later save.

**B32c, fail** of “a typed ODE that climbs while the
packet falls is still an NS a priori.” Prescribed
\(\Delta j=0.512\). Field \(\approx-0.015\).

**B32d, fail** of “matching the sketch on this window
is \(\int\|\omega\|_\infty\).” A short-window sign is
not the max criterion.

**B32e, fail** of “a finer box closes \(X\).”
Scored as B22e / B33. A bigger FFT is not
continuation. Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity stays open. Do not spawn
\(n=64\).

**B32f, fail** of “this retunes the PDE.” The window
is a knob on the check.

**B21e, fail** of “matching the sketch closes \(X\).”
Scored here.

**B31e, fail** of “the sketch leftover closes \(X\).”
Leftover is now scored.

---

## They work it

**Tesla.** You typed a rate whose saving happens later
than the box. Detune the window. Do not cash B11c on
\(T=0.064\).

**Leray.** Viscosity pulled \(j_{\mathrm{bar}}\) down.
The sketch asked it to climb.

**Ladyzhenskaya.** Same weight, both sides, at the
scale you are actually on. On this window that scale
is still fat. I still will not give you \(\varepsilon\).

**Majda.** The packet stayed CONC. Occupation of CONC
is not a cascade to \(j=5\).

**Beale.** Nobody votes a growing sketch against a
falling packet into \(\int\|\omega\|_\infty\).

**Feynman.** Missable: \(j(T)\) versus \(5\), \(\Delta X\)
signs, and whether a short window is a bound. The
first two held. The a-priori slogan missed.

**Einstein.** The object stayed the classical field.
A long ODE is not a short path.

**Operator.** The window is scored. B21e is scored.
Next: regularity stays open. Do not spawn \(n=64\). B4c
stands. Do not cancel to \(\Phi\). Do not write
\(c=8\) into the PDE.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B21e | **fail** | matching the sketch closes \(X\) |
| B31e | **fail** | sketch leftover closes \(X\) |
| B32 | **pass** | window rates, missed room, sketch-grows / field-falls readable |
| B32a | **fail** | matching the sketch closes \(X\) |
| B32b | **fail** | cashing B11c on \(T=0.064\) is continuation |
| B32c | **fail** | growing sketch is an NS a priori |
| B32d | **fail** | matching the window is \(\int\|\omega\|_\infty\) |
| B32e | **fail** | a finer box closes \(X\) |
| B32f | **fail** | this retunes the PDE |
| domain B | **open** | regularity stays open |

Tesla’s line: the sitting of \(c=8\) is a long ODE.
This window is short. The field did not follow.
