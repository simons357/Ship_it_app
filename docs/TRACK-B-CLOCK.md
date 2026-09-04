# Field occupation as an a priori

`python3 scripts/track_b_clock.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B18: \(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\) on a
path. Both paths stay CONC. The clock did not save
\(X\). This write asks whether that reading closes
\(X\). It does not.

---

## The knob on this write

Tesla: occupation is a number on a path. If the path
never leaves CONC, the clock did not do the bound.
Cubic-live time is a different number. It was empty.

No \(Q_1\). No \(\varepsilon\). No Biot–Savart slogan.
Do not spawn \(n=64\).

---

## What the apparatus does

**B29, pass.** Clock, full CONC occupation, and
visc-owned \(X\) are readable together. Same caches
as B18. No new FFT.

**B29a, fail** of “occupying CONC the whole interval
closes \(X\).” Both paths stay CONC and \(X\) falls.
Viscosity did the work. The clock did not leave.

**B29b, fail** of “\(\tau_{\mathrm{C}}=T\) is a short
visit that bounds \(X\).” B18c already missed. B8a’s
collapsing hot time is a packet ODE at high \(j_*\).

**B29c, fail** of “occupation of CONC is occupation
of a live cubic.” Zero live samples.
\(\lvert P\rvert/D\) stays below \(0.05\).

**B29d, fail** of “\(\tau_{\mathrm{C}}=T\) is an
integral bound on the max vorticity.” A clock column
is not \(\int\|\omega\|_\infty\).

**B29e, open.** Field-glue leftover is B19e. The
sketch versus the field. Not a bigger FFT.

**B29f, fail** of “this retunes the PDE.” The clock
is a knob on the estimate.

**B18e, fail** of “field occupation closes \(X\).”
Scored here.

**B28e, fail** of “the occupation leftover closes
\(X\).” Leftover is now scored.

---

## They work it

**Tesla.** Did it switch? No. Was the cubic live in
time? No. Do not sit a clock column as a bound.

**Leray.** They occupied CONC and \(X\) fell because
of me, not because of \(\tau_{\mathrm{C}}\).

**Majda.** The clock says which column is on. One
column was on. That is not a class.

**Beale.** Nobody votes \(\tau_{\mathrm{C}}=T\) into
\(\int\|\omega\|_\infty\).

**Ladyzhenskaya.** A short visit you did not get is
not my same-weight gift. I still will not give you
\(\varepsilon\).

**Feynman.** Missable: \(\tau_{\mathrm{C}}/T\),
switches, and live samples. All readable. The
save-by-leaving slogan missed.

**Einstein.** The object stayed the classical field.
A clock is not a closed estimate.

**Operator.** The clock is scored. B18e is scored.
Next: field glue (B19e). Finer stays B22e. Do not
spawn \(n=64\). B4c stands. Do not cancel to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B18e | **fail** | field occupation closes \(X\) |
| B28e | **fail** | occupation leftover closes \(X\) |
| B29 | **pass** | clock, full CONC, visc-owned \(X\) readable |
| B29a | **fail** | staying CONC closes \(X\) |
| B29b | **fail** | \(\tau_{\mathrm{C}}=T\) is a short visit |
| B29c | **fail** | CONC occupation is a live cubic |
| B29d | **fail** | \(\tau_{\mathrm{C}}=T\) is \(\int\|\omega\|_\infty\) |
| B29e | **open** | matching the sketch closes \(X\) |
| B29f | **fail** | this retunes the PDE |
| domain B | **open** | field-glue leftover is B19e |

Tesla’s line: occupation is a number on a path. If
the path never leaves CONC, the clock did not do
the bound.
