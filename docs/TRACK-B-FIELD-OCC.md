# Field occupation

`python3 scripts/track_b_field_occ.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B8 typed \(\sigma\) and partitioned \(T\). This write
samples the clock on a path.

---

## The knob on this write

Same threshold as B2 / B8:

\[
\sigma=\frac{P_{j_*}}{X},\qquad
\tau_{\mathrm{C}}=\mathrm{meas}\{\sigma\ge\tfrac12\}.
\]

Now \(\sigma=\sigma(t)\) along a short IF-RK2 trajectory.
Two paths, B13 box: \(n=32\), \(X_0=2.5\), \(\nu=0.1\),
\(dt=0.008\), eight steps (\(T=0.064\)).

1. Random 3-shell packet, \(j_*=2\).
2. Signed-strain blob (B17).

Tesla: occupation is a number on a path. If the path
never leaves CONC, the clock did not do the bound.
Cubic-live time (\(\lvert P\rvert/D\ge 0.05\)) is a
different number.

No \(Q_1\). No \(\varepsilon\). No BKM-from-\(L^2\).

---

## What the apparatus does

**B18, pass.** \(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\)
on both paths. Clock residual at roundoff. The B8
identity, read on a field.

**B18a, pass.** Both paths occupy CONC the whole
interval. \(\sigma\) stays \(\ge 0.5\) (packet \(\sigma=1\);
blob \(\sigma\approx 0.85\to 0.81\)). Zero switches.

**B18b, fail** of “the clock left CONC and that is why
\(X\) sat.” Packet \(X\): \(2.5\to 1.43\). Blob:
\(2.5\to 1.87\). Viscosity. The clock did not flip them
into SPREAD.

**B18c, fail** of “CONC occupation is short on these
runs.” \(\tau_{\mathrm{C}}=T\). B8a’s collapsing hot time
is a packet ODE at high \(j_*\). These fields did not
make a short visit.

**B18d, fail** of “the cubic is live on a nonempty set
of samples.” Zero samples with \(\lvert P\rvert/D\ge 0.05\).
Occupation of CONC is not occupation of a live cubic.
The blob’s one-sided \(P\) is still \(\sim 0.8\%\) of \(D\).

**B18e, fail** of “field occupation closes \(X\).”
Scored as B29. Occupation of CONC is not
continuation. The clock did not leave.

**B18f, fail** of “this retunes the PDE.” Sampling
\(\sigma(t)\) is a knob on the check.

**B8c, fail** of “occupation-time bookkeeping closes
\(X\).” B8b already sits in CONC the whole interval with
unbounded \(X\). These NS paths occupy CONC fully; the
bound, when it sits, is viscosity. The placeholder close
is scored.

---

## They work it

**Leray.** My integral still does not choose the hat.
Jean, they occupied CONC and \(X\) fell because of me,
not because of \(\tau_{\mathrm{C}}\).

**Kato.** High \(j_*\) short was a scale. These paths
did not climb, and they did not leave.

**Majda.** The clock says which column is on. One
column was on. That is not a bound.

**Ladyzhenskaya.** I still will not give you
\(\varepsilon\). A short visit you did not get is not
my same-weight gift.

**Tesla.** Two knobs. Did it switch? No. Was the cubic
live in time? No. You can miss the second if you stop
at “they stayed CONC.”

**Feynman.** Missable: \(\tau_{\mathrm{C}}/T\), switches,
and live samples. All readable. The save-by-leaving
slogan missed.

**Caffarelli.** Occupation is still measure. Full
occupation of a decaying packet is not a singular set.

**Beale.** Nobody votes \(\tau_{\mathrm{C}}=T\) into
\(\int\|\omega\|_\infty\).

**Einstein.** The object stayed the classical field.
Same PDE, now with a clock along the path.

**Operator.** Field occupation is scored. B8c is scored.
B18e is scored. Field glue is not an a priori (B19e). Next: NS climb (B20e). Finer is B22e.
B4c stands. Do not cancel to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B8c | **fail** | occupation bookkeeping closes \(X\) |
| B18 | **pass** | clock identity on a path |
| B18a | **pass** | both paths occupy CONC fully |
| B18b | **fail** | the clock left CONC and saved \(X\) |
| B18c | **fail** | CONC occupation is short on these runs |
| B18d | **fail** | cubic-live time is nonempty |
| B18e | **fail** | field occupation closes \(X\) |
| B18f | **fail** | this retunes the PDE |
| domain B | **open** | NS-climb leftover is B20e |

Tesla’s line: occupation is a number on a path. If the
path never leaves CONC, the clock did not do the bound.
