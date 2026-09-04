# Occupation time

`python3 scripts/track_b_occupation.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The two-regime clock, broken out.

B4c sits on 3-CONC. Energy-class \(T\) sits on SPREAD.
This write is the time each side is allowed to own.

---

## The clock (B8)

One threshold, the same one as B2:

\[
\sigma=\frac{P_{j_*}}{X},\qquad
\tau_{\mathrm{C}}=\mathrm{meas}\{\sigma\ge\tfrac12\},\qquad
\tau_{\mathrm{S}}=\mathrm{meas}\{\sigma<\tfrac12\}.
\]

Then \(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\). Switching is
free. The threshold sits on CONC so the clock partitions; a
cover that double-counts is not a clock.

**Pass.** Paths that stay, switch, or wander all add to \(T\).

---

## High \(j_*\) (B8a)

On a packet, B4c’s scale is \(\delta\sim 2^{-j_*}\). The model
budget is

\[
\dot X=X^3-\nu\,2^{2j_*}X.
\]

Hot occupation (time with \(X\ge 1\)) falls as \(j_*\) rises:

| \(j_*\) | \(\tau_{\mathrm{hot}}\) |
|---|---|
| 2 | 0.53 |
| 3 | 0.035 |
| 4 | 0.0075 |
| 5 | 0.0018 |
| 6 | 0.0005 |

**Pass** as a packet ODE. High CONC cannot sit hot for long
on that budget.

---

## Leray is not a clock (B8b)

The hope: \(\int X\,dt<\infty\) makes CONC short.

Killer: stay in CONC (\(\sigma=0.8\)) with
\(X=(T_*-t)^{-1/2}\). The integral is \(\approx 2\). The clock
runs the whole interval. \(X\) is unbounded.

Same spike as B6, now wearing a regime label. **Fail.**

---

**B8c, fail** of “occupation-time bookkeeping closes a
bound for \(X\).” B8b sits in CONC the whole interval
with unbounded \(X\). Short NS paths occupy CONC fully;
the bound, when it sits, is viscosity. Field occupation
is [`TRACK-B-FIELD-OCC.md`](TRACK-B-FIELD-OCC.md).

---

## They work it

**Leray.** My integral is a budget on \(\int X\), not on
which hat \(\sigma\) wears. Do not ask it to shorten CONC.

**Kato.** High \(j_*\) dies because viscosity has a scale,
not because we renamed a criterion.

**Majda.** The clock is the glue. It does not bound \(X\).
It says which column is on.

**Ladyzhenskaya.** High \(j_*\) short is the same-weight
instinct. Low \(j_*\) CONC is a fat, slow room. I still will
not lend you \(\varepsilon\).

**Tesla.** \(j_*\) is a knob. Turn it up, hot time collapses.
Sit in CONC with a mild spike, the clock does not blink.
Two knobs, two moves.

**Feynman.** Missable numbers: \(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}-T\),
and \(\tau_{\mathrm{hot}}(j_*)\). You can get both wrong.

**Caffarelli.** Occupation is measure. Small time is not
empty singular set.

**Fefferman.** Do not call a short high-\(j_*\) visit
alignment.

**Beale.** The clock does not vote \(X\in L^\infty\).

**Einstein.** Two columns, one time axis. Name which object
is on.

**Operator.** Clock is scored. B8c is a fail of the close.
The glue that talks to \(X\) is written in
[`TRACK-B-GLUE.md`](TRACK-B-GLUE.md). Field occupation is
[`TRACK-B-FIELD-OCC.md`](TRACK-B-FIELD-OCC.md). Next: finer/longer
climb (B13e).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B8 | **pass** | \(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\) |
| B8a | **pass** | high \(j_*\) hot time falls |
| B8b | **fail** | Leray \(\Rightarrow\) short CONC |
| B8c | **fail** | occupation closes a bound for \(X\) |
| domain B | **open** | finer/longer (B13e) is next |

The unicorn, broken out: a clock you can read, not a close.
