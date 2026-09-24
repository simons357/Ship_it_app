# Recovered Gate 1–7 record

24 September 2026.
Seated on the NS close plan.
**Recovery, not a reopen. Not a close.
NS not solved.**

This page is the fullest recoverable
answer from the earlier Gate material,
as recovered by ChatGPT on
24 September 2026 and sent to
[`docs/NS-CLOSE-PLAN.md`](NS-CLOSE-PLAN.md).

Gaps are **not** filled by
re-deriving definitions. Where the
earlier record does not preserve the
exact definition, it is marked
**MISSING**. Later quantities that
look similar are **not** spliced
into this older Gate system.

ChatGPT’s own status warning,
preserved:

> this old Gate-5–7 roadmap was
> subsequently treated as
> superseded / obsolete in later
> work. Recovering it is worthwhile
> for auditing mathematical lineage,
> but it should not automatically
> overwrite the current board or
> resurrect a branch. Under our
> present rule, **REOPEN = recompute**.

Machine lock:
`data/ns_close_plan/gates_recovered_2026-09-24.json`.
Picture of this older board:
[`docs/ns-close-plan/roadmap.svg`](ns-close-plan/roadmap.svg).

---

## What is left (from that board)

Concrete leftover, as recorded after
the recovery — not a new derivation:

1. **Finish Gate 5.** Obtain an
   exact real-algebra certificate
   that the bad \(++\) set is empty,
   or an exact counterexample. This
   is the immediate target.
2. **Gate 6.** Close the remaining
   sign chambers for the three
   centered shell positions. Several
   should collapse into each other
   by permutation, so this is not
   necessarily six completely new
   proofs.
3. **Gate 7.** Sum the remaining
   pointwise triad toward the
   broadband estimate.

The living close-plan order remains
Route A then Route B on
[`NS-CLOSE-PLAN.md`](NS-CLOSE-PLAN.md).
This leftover list does not replace
that order.

---

## GATE 5 — most important

### 1. Exact \(C_0,C_1,C_2,D_+\)

The exact Gate-5 polynomial
previously recorded was

\[
P_0(z)=C_0(u,m)+C_1(u,m)\,z+C_2(u,m)\,z^2,
\qquad z=d^2.
\]

**Screenshot-visible coefficients**
(do not complete the truncated
polynomials):

\[
C_0(u,m)=2(m+1)(u+1)\bigl[
m^4+2m^3u+4m^3+m^2u^2
+4m^2u+m^2+2mu^3+2mu^2+2u^3
+\cdots\bigr]
\]

\[
C_1(u,m)=(u+1)\bigl[
-20m^3+4m^2u-32m^2+6mu^2+\cdots
\bigr]
\]

\[
C_2(u,m)=16m^2+2mu+18m-4u^2-10u-2.
\]

\(C_0\) and \(C_1\) arrived
**truncated** in the recovered
screenshots. \(C_2\) is the only
coefficient that looks complete.
Until a source artifact supplies
the rest, Gate 5 is **not**
independently reproducible.

The recorded definition of \(D_+\)
was

\[
D_+(u,m)=4C_0C_2-C_1^2.
\]

So no: in that Gate-5 notation
\(D_+\) was **not**
\(C_1^2-4C_0C_2\). It was its
negative:

\[
D_+=-\mathrm{disc}(P_0).
\]

The dangerous chamber was recorded
as

\[
C_2>0,\qquad C_1<0,\qquad D_+<0,
\qquad 0<z^*<z_{\max},
\]

where

\[
z^*=-\frac{C_1}{2C_2}.
\]

This is consistent algebraically
because

\[
P_0(z^*)
=C_0-\frac{C_1^2}{4C_2}
=\frac{4C_0C_2-C_1^2}{4C_2}
=\frac{D_+}{4C_2}.
\]

Thus the chamber \(C_2>0\),
\(D_+<0\) means the quadratic’s
interior minimum is negative.

### 2. Exact meanings of \(u,m,d,z\)

The original exact definitions of
\(u,m,d\) are **MISSING**.

What is preserved exactly is

\[
z=d^2.
\]

The Gate-3 convention also
survives:

\[
r=\lvert q\rvert,\qquad
t=\lvert p\rvert,\qquad
s=\lvert k\rvert,
\]

with the triad wavevectors
satisfying the Fourier-triad
relation used in the construction.

Do **not** reverse-engineer
\(u,m,d\) from the polynomial.
Those would be a fresh
reconstruction, not the
definitions actually used earlier.

### 3. Derivation of \(P_0(z)\) from
Gates 2–3; what is \(c\)?

The complete step-by-step
derivation is **MISSING**.

Notation discrepancy: the exact
polynomial recovered is labeled
\(P_0(z)\), rather than \(P_c(z)\).
No reliable earlier definition of
the parameter \(c\) is preserved.
Do not invent one.

What survives upstream is the
Gate-2 centered function

\[
f(x)=x(x-\Lambda)
\]

and the Gate-3 geometric factor

\[
\psi_\Lambda(r,t,s)
=\frac{\sqrt{\Delta}}{2\sqrt{r}}
\bigl\lvert(s-t)(s+t-\Lambda)\bigr\rvert.
\]

That is **not** enough to reproduce
the historical Gate-2/3 → Gate-5
reduction without a new derivation.

### 4. What exactly is \(D_+\)?

Definitively, in the recovered
Gate-5 record,

\[
D_+=4C_0C_2-C_1^2.
\]

Therefore

\[
D_+=-\bigl(C_1^2-4C_0C_2\bigr)
\]

and

\[
P_0(z^*)=\frac{D_+}{4C_2}.
\]

Those three quantities are related
but are **not** identically the
same object.

### 5. Allowed \((u,m)\) range and
\(z_{\max}\)

The recovered Gate material
explicitly gives

\[
u>0,\qquad m>0
\]

and

\[
z_{\max}
=\min\left\{
m^2,\;
\frac{(1+u)(3+4m-u)}{4}
\right\}.
\]

The original derivation of those
two upper bounds on \(d^2=z\) is
**MISSING**.

Therefore this is **not** certified
as the complete admissible
\((u,m)\) domain beyond the
recorded \(u,m>0\), and the origin
of the second constraint is not
reconstructed here.

### 6. Meaning of the \(++\) chamber

The exact prior definition of
\(++\) is **MISSING**.

In particular, the earlier record
does **not** certify that it meant

\[
r>\Lambda,\qquad s>\Lambda,\qquad t>\Lambda.
\]

That needs the original Gate-5
derivation or source artifact.

### 7. Numerical evidence

The exact numerical protocol —
grid bounds, grid resolution,
random-sampling distribution, seed,
and number of tested points — is
**MISSING**.

Those numbers are not supplied
here.

---

## GATE 1

The surviving Gate-1 roadmap
statement is

\[
\lVert\Pi_\beta B(w,w)\rVert_2
\le\sqrt{3\beta}\,\lVert w\rVert_2^2
\]

together with

\[
\lvert\mathcal S_\star\rvert
\le\sqrt{3}\,\frac{\alpha}{\sqrt{\beta}}
\,e_\alpha\sqrt{e_\beta}.
\]

The exact earlier definitions of
\(\mathcal S_\star\), \(c_\alpha\),
\(e_\beta\) are **MISSING**.

Do not reconstruct them from
standard shell notation and
present that as the original
definition.

Recorded roadmap status: **CLAIMED**
(equal-shell HH → L).

---

## GATE 2

What survives exactly is the
centered function

\[
f(x)=x(x-\Lambda)
\]

and the compressed triad identity

\[
\mathcal T_{pqk}
=[f(s)-f(t)]X
+[f(r)-f(s)]Y
+[f(t)-f(r)]Z.
\]

The requested full six-permutation
identity before compression into
\(X,Y,Z\) is **MISSING**.

This is one of the important
missing pieces.

Recorded roadmap status: **CLOSED**
for the compressed identity only.

---

## GATE 3

### Are \(r,s,t\) lengths or squared
lengths?

The earlier roadmap is unambiguous:

\[
r=\lvert q\rvert,\qquad
t=\lvert p\rvert,\qquad
s=\lvert k\rvert.
\]

They are **lengths**, not squared
lengths.

The recorded triangle quantity was

\[
\Delta
=2(r^2t^2+t^2s^2+s^2r^2)
-(r^4+t^4+s^4).
\]

And the Gate-3 expression was

\[
\psi_\Lambda(r,t,s)
=\frac{\sqrt{\Delta}}{2\sqrt{r}}
\bigl\lvert(s-t)(s+t-\Lambda)\bigr\rvert.
\]

### Origin of \(\sqrt{\Delta}/(2\sqrt{r})\)

The exact historical derivation of
that factor is **MISSING**.

There is a reason not to casually
reconstruct it: with \(r\)
explicitly recorded as a
**length**, the denominator
\(2\sqrt{r}\) deserves checking
against the underlying geometric
normalization. Do not silently
“fix” or reinterpret it.

Status: formula recovered;
derivation not recovered.

Recorded roadmap status: **CLOSED**
for the recorded formula.

---

## GATE 4

The roadmap records the target

\[
L\le A
\]

and its status as **PARTIAL**
(not yet global).

The precise original formulas
defining \(L\) and \(A\) are
**MISSING**.

Safe historical statement: some
portion of the comparison had been
established, but the global
\(L\le A\) result had **not** been
completed.

---

## GATE 6

Recorded status: **NOT YET STARTED**.

The roadmap describes remaining
sign chambers for the three
centered shell positions. Several
should collapse by permutation.

No chamber list, no sign table,
and no permutation dictionary
were preserved in the recovered
record. Do not invent them.

---

## GATE 7

The surviving Gate-7 target is

\[
(T_c)_+\lesssim\sqrt{D_s\,E\,Y}.
\]

The roadmap describes this as
involving occupancy control /
global summation and marks the
Gate-7 status: **NOT YET STARTED**.

The exact Gate-7 definitions of
\(T_c\), \(D_s\), \(E\), \(Y\)
are **not** preserved in that
Gate record.

There is later work in this
program using similarly named
quantities. Those later
definitions are **not** spliced
into this older Gate system
without establishing that the
notation is identical.

---

## Bottom line

The strongest recoverable piece
is Gate 5’s exact quadratic

\[
P_0(z)=C_0+C_1z+C_2z^2,\qquad z=d^2,
\]

with

\[
D_+=4C_0C_2-C_1^2,\qquad
z^*=-\frac{C_1}{2C_2},\qquad
P_0(z^*)=\frac{D_+}{4C_2}.
\]

The recorded dangerous conditions
were

\[
u,m>0,\quad
C_2>0,\quad
C_1<0,\quad
D_+<0,\quad
0<z^*<z_{\max}.
\]

The historical definitions of
\(u,m,d,++\), the parameter \(c\),
the six-permutation expansion, and
the numerical protocol are
**MISSING**. Those are exactly the
pieces required before treating
Gate 5 as independently
reproducible.

Do not automatically overwrite
the current close-plan board.
Do not resurrect this branch as
the living line.
**REOPEN = recompute.**
