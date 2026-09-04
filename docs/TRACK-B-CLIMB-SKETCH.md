# Climb sketch

`python3 scripts/track_b_climb_sketch.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B11c typed \(c=8\) and the long ODE sat. This write asks
the working-box field.

---

## The knob on this write

The B11 model sits if \(c=8\) on a long run (B11c). NS
did not pick that \(c\) (B11d). Tesla: the sitting is a
*time*. Put the ODE on the same window the field was
read (\(T=0.064\)). If the viscous room has not arrived,
you do not have B11c on this box.

\[
j_*(t)=2+8t,\qquad
\dot X=\alpha_c(j_*)X^3-\nu\,2^{2j_*}X.
\]

Time to \(j_*=5\): \(0.375\). The NS window is \(0.064\).
Prescribed \(\Delta j=0.512\). Packet \(\Delta j_{\mathrm{bar}}\approx-0.015\).

No \(Q_1\). No \(\varepsilon\). Do not write \(c=8\) into
the PDE.

---

## What the apparatus does

**B21, pass.** Both readable. Long ODE still sits
(\(j_{\mathrm{final}}\approx 8.5\), \(T\approx 0.81\)).
Window \(T=0.064\) matches B18.

**B21a, fail** of “on this window, \(c=8\) has reached
the viscous room.” \(j\colon 2\to 2.51\). The sitting
of B11c has not arrived.

**B21b, fail** of “the B11c sitting path is the NS
packet.” Climb ODE \(X\) grows \(2.5\to 2.67\). NS \(X\)
falls \(2.5\to 1.43\).

**B21c, fail** of “NS \(\Delta j_{\mathrm{bar}}=c\,T\).”
Prescribed \(+0.512\). Field \(\approx-0.015\).

**B21d, fail** of “the sketch already sits on this
window.” Model \(X\) still grows. \(t=0\) \(\dot X=+2.25\),
same fat cubic as frozen \(j_*=2\).

**B21e, fail** of “matching the sketch closes \(X\).”
Scored as B32. A short window is not the sitting of
B11c. The sketch grew. The field fell.

**B21f, fail** of “this retunes the PDE.” \(c\) is a
knob on the estimate.

**B11e, fail** of “the climbing model is a closed a
priori for classical \(X\).” Prescribed \(c=8\) sits on
the ODE. NS did not pick that \(c\). On the readable
window the climb has not reached the room, and the
sketch grows while the field falls.

---

## They work it

**Tesla.** You typed a rate whose saving happens later
than the box. Detune the window. Do not cash B11c on
\(T=0.064\). Do not type the rate into the equation.

**Ladyzhenskaya.** Same weight, both sides, at the scale
you are actually on. On this window that scale is still
fat. I still will not give you \(\varepsilon\).

**Leray.** Viscosity pulled \(j_{\mathrm{bar}}\) down.
The sketch asked it to climb.

**Majda.** The packet stayed CONC. Occupation of CONC
is not a cascade to \(j=5\).

**Kato.** High \(j_*\) short was a scale on the long ODE.
This window did not get there.

**Beale.** Nobody votes a growing sketch against a
falling packet into \(X\in L^\infty\).

**Feynman.** Missable: \(j(T)\) versus \(5\), \(\Delta X\)
signs, and \(\Delta j\) versus \(cT\). All readable. The
a-priori slogan missed.

**Einstein.** The object stayed the classical field.
A long ODE is not a short path.

**Operator.** Climb sketch is scored. B11e is scored.
B21e is scored. Next: regularity stays open. Do not spawn
\(n=64\). B4c stands. Do not cancel to \(\Phi\). Do not
write \(c=8\) into the PDE.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B11e | **fail** | climb sketch is an NS a priori |
| B21 | **pass** | ODE and NS readable on the window |
| B21a | **fail** | \(c=8\) reached the viscous room here |
| B21b | **fail** | B11c sitting path is the NS packet |
| B21c | **fail** | NS \(\Delta j_{\mathrm{bar}}=cT\) |
| B21d | **fail** | the sketch already sits on this window |
| B21e | **fail** | matching the sketch closes \(X\) |
| B21f | **fail** | this retunes the PDE |
| domain B | **open** | regularity stays open |

Tesla’s line: the sitting of \(c=8\) is a long ODE.
This window is short. The field did not follow.
