# Longer path

`python3 scripts/track_b_longer.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B13 stopped at \(T\sim 0.06\). The \(c=8\) sketch reaches
the viscous room at \(T=0.375\). This write lets the
field run to \(T=0.384\). Same \(n=32\). Not a bigger FFT.

---

## The knob on this write

Tesla: you said longer. Lengthen \(T\) at the working
box until it passes the sketch’s room time. If \(c\)
still does not reach 8, “just let it run” has failed
on this apparatus.

\[
T=0.384=48\times 0.008>0.375=\frac{5-2}{8}.
\]

Finer (\(n>32\)) is a different knob. \(n=64\) is not
this write.

No \(Q_1\). No \(\varepsilon\). Do not write \(c=8\)
into the PDE.

---

## What the apparatus does

**B22, pass.** Packet and blob stay readable. \(X>0\).
Still CONC.

**B22a, fail** of “a longer \(n=32\) run produces
\(c\ge 8\).” Packet visc \(c_{\mathrm{mean}}\approx-0.48\).
Blob \(\approx-1.87\). Euler \(\approx 0.001\). No step
increment reaches 8.

**B22b, fail** of “longer is a ladder.” Packet
\(j_{\mathrm{bar}}\colon 2.97\to 2.79\). Blob
\(2.57\to 1.85\). More time pulled the barycenter down.

**B22c, fail** of “longer fills resolved high shells.”
Mass above \(j_*+1\) stays \(\sim 0\).

**B22d, fail** of “the clock left CONC and that is why
\(X\) sat.” Zero switches. Packet \(X\colon 2.5\to 0.15\)
by viscosity.

**B22e, fail** of “a finer box produces a saving
climb.” Scored as B33. A bigger FFT is not
continuation. DNS leftover is B23e. Do not spawn
\(n=64\).

**B22f, fail** of “this retunes the PDE.” \(T\) is a
knob on the check.

**B13e, fail** of “a finer / longer run produces a
saving climb.” Longer past the sketch’s room time did
not. Finer is B22e, not a close.

---

## They work it

**Tesla.** You asked for time. You got past the sitting
of \(c=8\). The field went the other way. Do not buy
a bigger box to hide that. Do not type the rate into
the equation.

**Ladyzhenskaya.** Same weight, both sides, at the
scale you are actually on. Length did not move that
scale up. I still will not give you \(\varepsilon\).

**Leray.** Viscosity owned \(X\) harder, not less.
That is my dissipation.

**Majda.** Still CONC at \(T=0.384\). Occupation of
CONC is not a cascade.

**Kato.** High \(j_*\) short was a scale on the ODE.
This path went down.

**Beale.** Nobody votes a decaying packet into
\(\int\|\omega\|_\infty\).

**Feynman.** Missable: \(T\) versus \(0.375\),
\(c_{\mathrm{mean}}\), and \(\Delta j_{\mathrm{bar}}\).
All readable. The “just let it run” slogan missed.

**Einstein.** The object stayed the classical field.
A longer path is not a finer metric.

**Operator.** Longer is scored. B13e is scored.
Climb and DNS knobs at \(n=32\) are scored. Finer is B22e. B4c stands. Do not
write \(c=8\) into the PDE. Do not spawn \(n=64\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B13e | **fail** | finer / longer produces a saving climb |
| B22 | **pass** | longer paths readable past room time |
| B22a | **fail** | longer run produces \(c\ge 8\) |
| B22b | **fail** | longer visc is a ladder |
| B22c | **fail** | longer fills high shells |
| B22d | **fail** | the clock left CONC and saved \(X\) |
| B22e | **fail** | finer (\(n>32\)) produces a saving climb |
| B22f | **fail** | this retunes the PDE |
| domain B | **open** | DNS leftover is B23e |

Tesla’s line: you said longer. \(T\) passed the
sketch’s room time. The field still did not climb.
