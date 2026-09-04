# Low-\(j_*\) CONC: energy ceiling

`python3 scripts/track_b_low_j.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.

---

## We are not tuning Navier–Stokes

Classical field. Keep \(1/r^4\). No \(Q_1\). No \(\varepsilon\).
No \(\Phi\)-cancel. `nodes.json` stays frozen.

What turned is a knob on the **estimate**: \(j_*\), and
whether the B9b model remembered Leray’s energy. Tesla
detunes the apparatus. He does not retune the machine.
Olga will not slide \(\varepsilon\) into his equation.

---

## What B9b forgot

The glue ODE at frozen \(j_*=2\) lets \(X\) run to 40.
That path has no energy.

On a packet with support \(|k|\le K=2^{j_*+1}\),

\[
X=\|\omega\|_2^2\le K^2\|u\|_2^2=K^2 E.
\]

Leray: \(E(t)\le E(0)\). Frozen \(j_*\) freezes \(K\).
Then \(X\) is bounded by a number you already have.
A near-saturated packet has no room to run. Growing
without bound at frozen support is not an NS trajectory.

**B10, pass.** Measured on 3-shell fields. \(X/K^2E\le 1\).

**B10a, fail** of “B9b is NS-legal.” The model forgot \(E\).

---

## What the ceiling does not do

If \(j_*\) climbs, \(K\) climbs, the cap rises.

**B10b, fail** of “the ceiling saves a climbing packet.”

**B10c, open.** CONC with rising \(j_*\) is the remaining
cubic room. High \(j_*\) already sits on the glue ODE.
Getting from coarse to thin, while staying concentrated,
is not shown.

**B10d, fail** of “this is a retune of the PDE.”

---

## They work it

**Tesla.** You asked if we were tuning the equation.
No. I turned \(j_*\) and I turned whether \(E\) is in
the room. The model that died at 2 had forgotten the
battery. That is a knob. Do not call it a new machine.

**Ladyzhenskaya.** Same weight, both sides. Energy is
the other side of frozen support. I still will not
give you \(\varepsilon\).

**Leray.** You may use \(E\). You may not use \(\int X\)
to cap \(X\). We already failed that.

**Feynman.** Missable number: \(X/K^2E\). If that ratio
goes past 1, the ceiling is a paragraph.

**Majda.** The clock still says which line is on.
The ceiling only talks while \(j_*\) sits still.

**Beale.** Nobody votes a ceiling into \(X\in L^\infty\)
on a climbing packet.

**Einstein.** The object stayed the classical field.

**Operator.** Frozen low-\(j_*\) is hygiene. The live
room is climbing CONC.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B10 | **pass** | packet \(X\le K^2 E\) |
| B10a | **fail** | B9b unbounded path is NS-legal |
| B10b | **fail** | ceiling bounds a climbing \(j_*\) |
| B10c | **open** | climbing CONC closes \(X\) |
| B10d | **fail** | this retunes the PDE |
| domain B | **open** | climbing CONC is the room |

Tesla’s line: detune the apparatus. Do not retune
Navier–Stokes.
