# SND to regularity — the implication, written out

15 September 2026.
Unaugmented NS on \(\mathbb{T}^3\).
This page is the implication, not a bound.
Ordinary NS is not solved.
Closing SND-C does not close ordinary NS.
No more \(K\)-sweeps for this hole.
Exact-shell 9D is a different statement
([`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md)).

**Limitation / assumption (read this first).**
A shell condition is an instantaneous
statement about enstrophy mass across
Littlewood–Paley shells. It is not a
law for how the peak scale moves, and
it is not an a priori bound on
\(X=\|\omega\|_2^2\).

Dictionary and regime split:
[`UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md)
§8–9. Closing SND is not ordinary NS:
[`SND-H-PLAIN.md`](SND-H-PLAIN.md).
Scored lemmas:
[`TRACK-B-LEMMAS.md`](TRACK-B-LEMMAS.md).

---

## The three answers

**What the shell condition controls.**
The instantaneous partition of
enstrophy among LP shells, hence which
regime you are in at that time, and
(if SND-C sits) the size of the flux
into the peak shell while you are in
SPREAD.

**What frequency drift is still needed.**
A law for \(j_*=\mathrm{argmax}_j X_j\)
or for \(\Lambda=Y/X\). Frozen support,
a prescribed climb, an occupation
clock, and a \(t=0\) reading are not
that law.

**Does the proof assume the desired
bound?**
Yes, in named places. T2 Lemma 2 takes
an \(H^{2.3}\) ball as input. Theorem F
assumes a dissipation lower bound that
is not a theorem. Theorem G needs a
uniform \(C_*\) as \(\rho\to 0\).
Theorem E is already-smooth.
Lemma★ is an implication, not a proof
of its hypothesis. SND-C’s floor
\(X\ge\delta_*/4\) is **not** an upper
bound on \(X\).

---

## Do not use one word

Five statements were all called SND.
Use the names.

| Name | Formula | Job |
|---|---|---|
| **CONC** / **3-CONC** | \(\inf J/X\ge c_*\), or packet mass \(\sigma\ge 1/2\) | Dominant shell or triad. Ring / Bernstein at scale \(2^{j_*}\). |
| **SPREAD** | \(\rho=J/X\le\rho_0\), or \(\sigma\le 1/2\) | No triad holds half. T2 Lemma 1. Attempted SND-C. |
| **SND-C** | bound on \(\lvert\Pi_{j_*}\rvert\) in SPREAD, with \(X\ge\delta_*/4\) | Shell flux while spread. Fluids Theorem H. |
| **T2-ODE** | quantitative SPREAD ODE | Rebuild without \(H^{2.3}\). |
| **SIMPLEX** | \(\|a-\mu\|_{\ell^1}\le 0.039\) | PARK. GCD arithmetic. Not used. |

August CONC and June SPREAD are
opposites. That is useful once they
have two names. Do not add them and
call the sum a close.

Shell language (sits as bookkeeping):

\[
X_j=2^{2j}\|\Delta_j u\|_2^2,\qquad
X=\sum_j X_j=\|\nabla u\|_2^2=\|\omega\|_2^2,
\]

\[
J=\max_j X_j,\qquad
\rho=J/X,\qquad
j_*=\mathrm{argmax}_j X_j,
\]

\[
P_{j_*}=X_{j_*-1}+X_{j_*}+X_{j_*+1},\qquad
\sigma=P_{j_*}/X.
\]

Flux into the peak shell:

\[
\Pi_{j_*}=\int_{\mathbb{T}^3}
\Delta_{j_*}\bigl[(u\cdot\nabla)u\bigr]
\cdot\Delta_{j_*}u\,dx.
\]

**(SND-C).** There is \(C_*<\infty\)
such that whenever \(X\ge\delta_*/4\)
and \(\rho=J/X\le\rho_0\) (spread),

\[
\lvert\Pi_{j_*}\rvert
\le
C_*\bigl(\nu\,2^{2j_*}X_{j_*}
+X^{1/2}\mathcal{D}^{1/2}\bigr),
\qquad
\mathcal{D}=\nu\|\Delta u\|_2^2.
\]

That is the shell condition people
meant when they said “SND implies
regularity.” It is a bound on
\(\Pi_{j_*}\) in one regime, under a
floor on \(X\). It is not a bound on
\(X\).

---

## What the shell condition controls

At each fixed time the numbers
\(\rho\) and \(\sigma\) say where the
enstrophy sits.

**In 3-CONC** (\(\sigma\ge 1/2\)).
A triad around \(j_*\) holds at least
half of \(X\). Bernstein on three
shells gives a Lipschitz bound for
direction on \(\{|\omega|\ge c\|\omega\|_2\}\)
at scale \(2^{j_*}\) (B3). That is
what Ring is. It controls geometry
**at the current scale**. It does not
force \(\cos\alpha_3\to 0\) for all
data (B3b). It does not freeze \(j_*\).

**In SPREAD** (\(\sigma\le 1/2\)).
No three consecutive shells hold half
of \(X\). T2 Lemma 1 kills low
self-flux into each \(\Delta_j\) by
\(\nabla\cdot u=0\) (B1). SND-C, if it
sits, bounds the remaining flux
\(\lvert\Pi_{j_*}\rvert\) while you
stay in this regime. Energy-class
low \(T\) sits without a \(\rho\)
upgrade (B7b). Uniform
\(\rho^{1/2}\) as \(\rho\to 0\) fails
(B7c). So even the flux bound is not
finished.

**The occupation clock**
\(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\)
(B8) only records which of those two
regimes you occupied. A cover of
mass fractions is not dynamics (B2).
A clock is not a bound on \(X\)
(B8c).

### What it does not control

The shell condition does **not**
control:

- how \(j_*\) or \(\Lambda\) moves
- continuation of \(X\)
- alignment of vorticity with strain
- the axisymmetric remainder
  \(T_{j\leftarrow j}\)
- whether Fourier support stays frozen
- the cubic \(\omega\cdot S\omega\)
  on a general CONC field

T2 Lemma 1 is unconditional and does
**not** imply regularity.

---

## What frequency-drift information is still needed

Centroid and peak:

\[
\Lambda=\frac{Y}{X},\qquad
Y=\|Au\|_2^2,\qquad
\mathcal{D}_s=Z-\Lambda Y\ge 0.
\]

The identities that sit
([`DA-NS-2.md`](DA-NS-2.md)):

\[
(\log\Lambda)'=\frac{2}{Y}(T_c-\nu\mathcal{D}_s),
\qquad
\Lambda'=\frac{2}{X}(T_c-\nu\mathcal{D}_s).
\]

Those are bookkeeping. They name the
leftover \(T_c\). They are not a law
that keeps \(\Lambda\) or \(j_*\)
from climbing.

What was tried, and what it actually
does:

| Candidate | What it controls | Why it is not the drift law |
|---|---|---|
| Frozen support \(X\le K^2 E\), \(K=2^{j_*+1}\) | Enstrophy while the packet cannot leave \(\lvert k\rvert\le K\) (B10) | If \(j_*\) climbs, \(K\) climbs, the cap rises (B10b). |
| Prescribed climb \(c=\mathrm{d}j_*/\mathrm{d}t\) | A knob on a model ODE. \(c=1\) still blows; \(c=8\) reaches the viscous room on that ODE (B11b, B11c) | NS did not force \(c=8\) (B11d). The sketch is not an a priori (B11e). |
| \(t=0\) reading of \(j_{\mathrm{bar}}\) | A number on a packet (B12) | A reading is not a law (B12e). Viscosity pulled \(j_{\mathrm{bar}}\) down, not up (B12c). |
| Occupation clock \(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\) | Time spent in each regime (B8) | Not a bound on \(X\) (B8c). Leray \(\int X<\infty\) does not make CONC short (B8b, B6). |
| Lemma★ energy budget | Would freeze \(\Lambda\) **if** the geometric inequality sat | Unrestricted \(\sup\mathcal{R}_\star<\infty\) is killed by \(v_n\). Replacement closure OPEN. |

A bounded peak scale is necessary
for a bounded \(X\) in the packet
class (B11a). Necessary is not a
close. Unbounded \(X\) in that class
needs unbounded \(j_*\). So the
missing information is a bound on
the climb, or a bound on \(\Lambda\),
coming from the field — not from a
typed \(c\).

### What remains even if SND-C and Ring both sit

Suppose SND-C is true in SPREAD with
\(C_*\) uniform in \(\rho\), and
3-shell Ring is true in 3-CONC.
You still have:

- the peak can walk to high \(j_*\)
  while concentrated
- then \(K\sim 2^{j_*}\) rises
- the frozen ceiling \(X\le K(j_*)^2 E\)
  blows
- occupation of CONC does not stop
  that walk
- a spike \(X\sim(T_*-t)^{-1/2}\) is
  compatible with integrable \(X\)
  (B6)

Without a drift law, true SND-C plus
true Ring do not give
\(X\in L^\infty([0,T])\).

---

## Whether the proof assumes the desired bound

Yes. Named places, already scored.
Do not rebuild the same circle under
a new name.

**1. T2 Lemma 2, circular as input.**
The June flux decay used an
\(H^{2.3}\) absorbing ball as a
hypothesis. That is already a
regularity assumption. For the
large-data a priori it is circular.
Dropped (B1b). Rebuild from Bony plus
energy class only.

**2. SND-C’s floor is not the circle.**
\(X\ge\delta_*/4\) is an enstrophy
*floor*: the bound is only claimed
when there is enough \(X\) to talk
about a peak shell. It is not an
upper bound on \(X\). Using it does
not assume \(X\in L^\infty\).
Theorem G, however, leans on
Theorem F to force you out of deep
SPREAD. That is a different, and
broken, step.

**3. Theorem F, too strong.**
The claimed dissipation

\[
\mathcal{D}\ge\nu\cdot 4^{N-1}\rho X,
\qquad
N=\lceil X/J\rceil
\]

treats “\(N\) active shells” as if
they sat at exponentially higher
frequency. They can be \(N\)
consecutive low shells.
Super-exponential dissipation as
\(\rho\to 0\) is not a theorem.
The diagonal step that writes

\[
2^{j_*}\le\bigl(\mathcal{D}/(\nu X_{j_*})\bigr)^{1/2}
\]

from F inherits this. Using F as a
lemma assumes a lower bound on
\(\mathcal{D}\) that would already
control high-frequency mass. That is
assuming a form of the bound you
wanted.

**4. Old \(\Phi\)-glue.**
The May chain put \(\Phi=\Gamma/r^2\)
in front of H. The cancel is free
only if \(\|\Phi\|_\infty\) is already
controlled. That bound is the swirl
barrier you do not have. Assuming it
to reach SND-C on an unaugmented
limit is circular. Cut B, C, and I
from the H track. State SND-C only
for classical velocity on
\(\mathbb{T}^3\), spread class, no
\(\varepsilon\), no \(\Phi\).

**5. Theorem E, already smooth.**
“SND on smooth intervals” is true
for an already-smooth \(u\). It does
not start the a priori. It assumes
the regularity the implication is
supposed to produce.

**6. Lemma★, honest implication,
dishonest converse.**
If the energy-budget inequality
sits, then \(\Lambda\) Gronwalls in
that packaging, hence
\(X\le\|u_0\|_2^2\Lambda\) stays
finite. One direction. These files
have no converse that global
regularity would force the uniform
inequality on every smooth field.
Do not write “★ equivalent to global
regularity.” Claiming the implication
proves its hypothesis is circular.
The unrestricted box is **killed**
by \(v_n\) anyway
([`LEMMA-STAR.md`](LEMMA-STAR.md)).

**7. Theorem G, needs the uniform
bound it concludes from.**
G says SND-C \(\Rightarrow\) CONC,
because if \(\rho(t_k)\to 0\) then F
makes \(\mathcal{D}\) explode and
SND-C forces \(\dot\rho>0\). If
\(C_*\) blows up as \(\rho\to 0\),
the contradiction fails. Uniform
\(\rho^{1/2}\) on the low sum in
\(L^\infty\) **fails** (B7c). G is
dead. It assumed a uniform SND-C
down to \(\rho\to 0\).

The two-regime glue sketch is a
further, separate circle: it used a
model ODE, not NS. Typed \(j_*=2\)
grows; the NS packet falls (B9d,
B19a). Matching the sketch is not
continuation.

---

## Honest non-circular skeleton

All three conjuncts are needed.
None closes NS alone.

\[
\bigl[\text{SND-C in SPREAD, }C_*
\text{ uniform in }\rho\bigr]
+\bigl[\text{Ring in 3-CONC}\bigr]
+\bigl[\text{drift law for }j_*
\text{ or }\Lambda\bigr]
\ \Rightarrow\ X\text{ bounded}.
\]

| Conjunct | Status |
|---|---|
| SND-C in SPREAD, \(C_*\) uniform in \(\rho\) | **OPEN.** Low Bony \(T\). Energy-class bound sits (B7b); uniformity as \(\rho\to 0\) fails (B7c). |
| Ring in 3-CONC | **Regime hypothesis** plus Bernstein. Bernstein sits (B3). All-data depletion from Ring fails (B3b). |
| Drift law for \(j_*\) or \(\Lambda\) | **MISSING.** Frozen ceiling does not follow a climb (B10b). NS did not force a saving \(c\) (B11d). \(t=0\) drift is not a law (B12e). Lemma★ replacement closure OPEN. |

The target estimate, if those three
sat, is the usual Gronwall form
(plan §G): something integrable
controlling \(\dot X\), then
\(X\in L^\infty([0,T])\), then
continuation in \(H^1\). That form
is a skeleton. It is not a theorem.

G, if it could be made uniform, would
only say you cannot stay in deep
SPREAD. That is optional. The
unaugmented bound needs **each**
regime controlled while you are in
it, **and** a law for the scale you
are on.

T2 Lemma 1 sits and stops there.

---

## What this page is not

- Not a regularity close.
- Not Clay Statement B.
- Not a claim that SND-C sits.
- Not a claim that Ring depletes
  alignment.
- Not more exact-shell \(K\) sweeps.
- Not a repair of unrestricted ★.
- Not the axisymmetric remainder
  \(T_{j\leftarrow j}\).

If a later sentence says “SND implies
regularity,” this page wins until a
named error is added with a date.

NS not solved.
Replacement closure OPEN.
Drift law MISSING.
SND-C OPEN at low \(T\).
