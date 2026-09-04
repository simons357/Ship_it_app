# Short CONC evolution

`python3 scripts/track_b_evolve.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
We did not stop at \(t=0\).

---

## The knob on this write

Let the packet run. Same classical field. No \(Q_1\).
No \(\varepsilon\). Integrating-factor RK2 on \(\mathbb{T}^3\),
\(n=32\), \(j_*=2\), \(X_0=2.5\), \(T\approx 0.064\).

Tesla: \(t=0\) was a reading. Time is the next dial.
If \(j_{\mathrm{bar}}\) still does not climb toward 8,
do not type a cascade into the estimate.

---

## What the apparatus does

**B13, pass.** The short run stays finite. Viscous \(X\)
does not grow.

**B13a, fail** of “a short evolution produces \(c\ge 8\).”
Viscous mean \(c\) is negative. Euler is \(\sim 0\).

**B13b, fail** of “resolved shells above the triad fill.”
Mass above \(j_*+1\) stays \(\sim 0\). \(n=32\) dealias
cannot host a fat \(j=4\). Still a reading.

**B13c, pass.** They stayed 3-CONC. The clock did not
sneak into SPREAD to survive.

**B13d, fail** of “evolution is a ladder.” \(j_{\mathrm{bar}}\)
falls along the trajectory. Same direction as \(t=0\).

**B13e, open.** Finer / longer. Unresolved shells are
another check, not a stop forever.

**B13f, open.** A few steps are not an a priori for \(X\).
Do not sit “DNS did not climb” as regularity.

---

## They work it

**Tesla.** You asked if we had to stop at \(t=0\).
No. I turned time. The field still did not give you
\(c=8\). That is a knob.

**Ladyzhenskaya.** Viscosity ate \(X\) and pulled the
peak down. It is not a hoist. I still will not give
you \(\varepsilon\).

**Feynman.** Missable numbers: \(c_{\mathrm{mean}}\)
versus 8, and whether \(\sigma\) stayed \(\ge 1/2\).

**Majda.** CONC the whole way. No cheat.

**Beale.** A short decaying packet is not
\(\|\omega\|_\infty\in L^1\).

**Einstein.** The object stayed the classical field.

**Operator.** The short run is on the desk. Next is
either a bigger box or the tube viscosity that was
already open (B5b).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B13 | **pass** | short run finite; viscous \(X\) falls |
| B13a | **fail** | short run produces \(c\ge 8\) |
| B13b | **fail** | resolved high shells fill |
| B13c | **pass** | stays CONC |
| B13d | **fail** | evolution is a ladder |
| B13e | **open** | finer / longer saving climb |
| B13f | **open** | short DNS is an a priori |
| domain B | **open** | B5b or a bigger box |

Tesla’s line: let it run. Then read. Do not type the cascade.
