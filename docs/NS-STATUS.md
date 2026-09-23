# Final NS / SND status — 16 September 2026

Jonathan R. Simons.
**Single handoff for Cursor / other
reviewers and the next phase.**
Ordinary Navier–Stokes is not solved.
Catalog B open stays 1 (`B_regularity`).
Not leftover 1. Do not start H1.
Do not weld \(\star\). Soft X silent.

This page scores the 16 September
orders. It does not close a leftover.
Incoming reports scored:
[`REPORT-AUDIT.md`](REPORT-AUDIT.md).
How this desk moves:
[`MASTER-PLAN.md`](MASTER-PLAN.md).
Operator close-report (not a close):
[`NS-CLOSE-REPORT.md`](NS-CLOSE-REPORT.md).
Path to a close (gates; not a close):
[`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md).
Route A write (A-pair; not \(L^\infty\)):
[`ROUTE-A-WRITE.md`](ROUTE-A-WRITE.md).
B★ (no universal \(C\); imag cutoff
grows \(R_B\); not a useful \(K\);
★ stays killed):
[`BSTAR.md`](BSTAR.md),
[`BSTAR-PROOF.md`](BSTAR-PROOF.md).
Fourier-triangle geometry
(identities sit; first missing
arrow to a useful \(K\); not a
close):
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).
First lift (same two shells
keep the gap; third eigenvalue
dies; \(K\sim\sqrt{E}\) dead):
[`TRIANGLE-LIFT.md`](TRIANGLE-LIFT.md).
Energy-class ladder (X, mid,
and Y doors die on \(v_n\);
G4 still OPEN):
[`ENERGY-K.md`](ENERGY-K.md).
Pairing CS doors (tight is
★; LE dead; LX not a
universal \(C\)):
[`L-DOOR.md`](L-DOOR.md).
Instantaneous \(MN\)
(\(N=0\) on \(v_n\); no
uniform \(\theta<1\)):
[`MN-CANCEL.md`](MN-CANCEL.md).
Enough for that plan. Not a close.
This desk is unaugmented. A is not B.

Phone pack: [`TINY.txt`](TINY.txt).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).
C10: [`C10-CHAIN.md`](C10-CHAIN.md).
Centered drift:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
SND instrument:
[`SND-INSTRUMENT.md`](SND-INSTRUMENT.md).

---

## Executive status

The program is in a better position
than when Theorem H was carrying too
much weight. The live question is
localized:

> Can the nonlinear term drive
> high-frequency concentration faster
> than viscosity can control it?

Several shortcuts are eliminated.
We are no longer trying to make a
false or insufficient inequality work.

Three research lanes sit **beside**
each other, not in series through H:

1. **C10 / near-scale depletion** —
   leftover-5 candidate. (A) not seated.
2. **Centered spectral drift** —
   \(T_c=M-\Lambda N\) versus
   \(\mathcal D_s=Z-\Lambda Y\).
   Unrestricted \(\star\) stays killed.
3. **SND spectral diagnostics** —
   instrument first. No persistence.

One mathematically interesting but
separate result:

> Exact-shell bound \(C=4/3\)
> (\(K\le 16/9\)) — **CLAIMED.**
> Independent verification pending.
> Designed \(\Theta(m^2)\) 9D is **NO.**
> Do not write “9D is claimed.”

Strategic change that stays:

> Stop trying to prove persistence of
> SND first. Attack the nonlinear
> high-frequency transfer mechanism
> directly.

---

## I. What has survived

### A. Exact spectral bookkeeping

The global quantities

\[
X=\|A^{1/2}u\|_2^2,\qquad
Y=\|Au\|_2^2,\qquad
Z=\|A^{3/2}u\|_2^2,\qquad
\Lambda=\frac{Y}{X}
\]

and the centered pair

\[
N=-\langle B(u,u),Au\rangle,\qquad
M=-\langle AB(u,u),Au\rangle,
\]

\[
T_c=M-\Lambda N,\qquad
\mathcal D_s=Z-\Lambda Y
\]

remain one of the strongest conceptual
pieces. \(T_c\) measures nonlinear
motion relative to the instantaneous
spectral center. \(\mathcal D_s\)
measures the corresponding dissipative
spread.

That decomposition is independent of
SND. Identities sit
([`LEMMA-STAR.md`](LEMMA-STAR.md),
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md)).
The uniform geometric remainder that
turned this into unrestricted \(\star\)
is **KILLED** by \(v_n\).

---

## II. Theorem H — freeze

The displayed version of Theorem H is
not a proof bridge. The audit found
independent obstructions: viscous-tail
bookkeeping, invalid 3-D Sobolev
embeddings, amplitude-scaling
incompatibility, and explicit
high-tail / shear counterexamples.

A universal initial SND floor does
not follow from the old hypotheses.

> Do not repair old Theorem H.

Keep it as historical material.
[`SND-H-REVIEW.md`](SND-H-REVIEW.md),
[`SND-H-REPAIR.md`](SND-H-REPAIR.md).
\(A.2\) sits. \(A.3\) is a Dini
ceiling, not a floor. Propagation
unwritten. The original extract stays
an extract.

---

## III. What SND is now

SND survives as a **diagnostic
language**, not as a regularity
theorem.

Frozen shells \(X_j\),

\[
J=\max_j X_j,\qquad
\rho=\frac{J}{X},\qquad
j_*\in\operatorname{argmax}_j X_j.
\]

These tell concentration, peak
location, peak migration, mass
outside the dominant region, and
shape change.

But \(\rho\ge\rho_*\) alone does not
control regularity. Even
\(\rho\ge\rho_*\) and \(j_*\le J_0\)
is insufficient: the remaining
\(1-\rho\) can occupy arbitrarily
high frequencies. That is an audit
result, not a slogan.

A sufficient spectral description
needs something like
\(\rho\) + peak location + tail shape.
A candidate envelope

\[
X_j\le J\,2^{-\gamma(j-j_*)},\qquad j>j_*,
\]

may later give a BKM-type conditional
by Bernstein summation. That is
**not** the primary attack: assuming
enough tail decay risks repackaging
a known regularity condition.

> SND: instrument first; theorem only
> when dynamics justify it.

Implemented, no persistence claim:
[`SND-INSTRUMENT.md`](SND-INSTRUMENT.md).

---

## IV. Exact-shell bound — freeze

Current status:

> Exact-shell \(C=4/3\)
> (\(K\le 16/9\)) — **CLAIMED.**
> Independent specialist reproduction
> pending. Designed \(\Theta(m^2)\) 9D
> is **NO.** Do not write “9D is
> claimed.”

The claimed projected estimate has
the form written on
[`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md).
Sweeps and the three-shear value
\(K_{1,2}=2/3\) are consistency /
falsification tests. They do not
establish \(16/9\).

Remaining job: independently
reproduce the complex-polarization /
projected identity and the
weighted-incidence argument, with
every multiplicity, normalization,
and ordered / unordered convention
explicit.

Until then:

> exact-shell bound
> \(\neq\) unrestricted \(\star\)
> \(\neq\) regularity closure.

Do not run another thousand sweeps.

---

## V. The live obstruction: near-scale transfer

Exact same-shell internal energy
transfer at \(b=0\) vanishes through
the relevant bookkeeping /
cancellation. The problem is not
simply “same-scale energy transfer.”

The live obstruction is closer to
near-scale \(b\ge 1\) interactions /
enstrophy-side transfer. That is
where stretching can potentially
beat spectral spreading and
viscosity.

---

## VI. TASK 1 — C10 chain (done as a write)

Estimate (A), verbatim from
[`C10-CHAIN.md`](C10-CHAIN.md):

\[
(T_{j\leftarrow j})_+
\le
\varepsilon\nu D_j
+C\,a_+ Z_j
+\mathrm{Rem}_j,
\]

with \(\mathrm{Rem}_j\) absorbed into
\(\varepsilon\nu D_j\) or estimated
from the energy inequality, **or** a
named proof that \(\mathrm{Rem}_j=0\).

\(a_+:=\|(\alpha_{\mathrm{loc},j})_+\|_\infty\),
\(\alpha_{\mathrm{loc},j}=\xi_j\cdot S(u_{\mathrm{loc}})\,\xi_j\).

Every arrow marked EXACT / STANDARD
LEMMA / NEW CLAIM / NUMERICAL ONLY.
Dependency graph written. Circularity
tested against \(H^1\), \(L^\infty\),
BKM, spectral-tail control, and the
desired conclusion.

**C10 did not survive as seated (A).**
That is not the same as “the lane is
dead.” The identities sit. The two
new arrows do not.

---

## VII. TASK 2 — which implication failed

| Arrow | Status | Why |
|---|---|---|
| NS \(\Rightarrow\) stretch \(\le a_+ Z_j\) | **EXACT.** Sits. | Definition of \(a_+\). Not secretly \(H^1\). |
| \(a_+\) estimate \(\Rightarrow\) depletion \(\int a_+<\infty\) | **NEW CLAIM. Unwritten.** | All-data geometric depletion already failed (B25a). Constantin–Fefferman is the converse. Sobolev control of \(a_+\) is BKM-adjacent. |
| depletion \(\Rightarrow\) (A) | **Failed to seat.** | TJJ-template sits, but the remainder is \(L^\infty\) of local velocity and strain. Energy-only remainder is **DEAD** (C1 / TJJ-E-false, \(\lambda^{1/2}\)). Bernstein reintroduces the cubic wall / circular Gronwall. |
| (A) \(\Rightarrow\) leftover 5 | **Not implied.** | (A) and \(\int a_+\) do not sit. |
| C10 \(\Rightarrow\) leftover 1 or \(\star\) | **NO.** | Do not weld. |

Adversarial families (no new 9D
sweeps):

1. **High-tail shears.** \(a_+=0\) and
   \(T_{j\leftarrow j}=0\). Holds as
   \(0\le 0\). Does not test depletion.
2. **Amplitude \(u=Aw\).** \(a_+ Z\)
   matches the cubic. Energy-linear
   \(R\) fails. C10 passes only if it
   keeps \(a_+\) in the majorant.
3. **Equal-enstrophy \(v_L\).**
   \(\rho(0)=1/L\). No universal
   \(t=0\) floor. Not a kill of
   Arrow 1.
4. **Growing-layer \(v_n\).** Kills
   unrestricted \(\star\). Does not
   resurrect it. Not a C10 close.
5. **Compact mixed swirl.**
   \(T^{\mathrm{mm}}\) is the bulk.
   Occupancy \(55/56\) did not fall.
   Not [ρ].

Do not repair a failure by
strengthening the hypothesis until
the theorem becomes tautological.
The failed seat is recorded above.
The lane stays a **named candidate**,
not a theorem.

---

## VIII. TASK 3 — centered drift (independent)

Target, preserved centering:

\[
T_c
\le
\theta\nu\mathcal D_s
+K(t)X,
\qquad
0\le\theta<1,
\qquad
K\in L^1_{\mathrm{loc}}(0,T).
\]

This is **not** unrestricted \(\star\).
The killed box used a uniform
geometric remainder
\(C_0\nu^{-1}\|u\|_2^2 X\Lambda\).
\(v_n\) kills that uniform remainder.
A pathwise \(K(t)\) is a different
sentence. It is also not automatic:
if \(K=(T_c-\theta\nu\mathcal D_s)_+/X\),
the estimate is tautological and the
content is only \(\int K<\infty\).

Work \(T_c-\theta\nu\mathcal D_s\).
Do not split \(M\) and \(\Lambda N\)
if that destroys cancellation.

Formal implication if the estimate
sits with a useful \(K\):
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
Replacement leftover 4 stays OPEN.

---

## IX. TASK 4 — crossover

C10 did **not** seat (A).
No conceptual arrow is drawn.

There is no seated inequality

\[
T_c\le C\sum_j a_+ Z_j
\]

and none of the form
near-scale depletion \(\Rightarrow\)
\(\lvert T_c\rvert\le\theta\nu\mathcal D_s+K(t)X\).

If a later write produces an actual
inequality, display it and re-test
\(v_n\) and the shears. Until then
the two lanes stay separate.

---

## X. TASK 5 — SND instrument

Frozen partition, exact diagnostics,
no persistence claim:
[`SND-INSTRUMENT.md`](SND-INSTRUMENT.md),
`python3 scripts/snd_instrument.py`.

Quantities: \(X_j\), \(J\), \(\rho\),
\(j_*\), packet \(P_{j_*}\), \(\sigma\),
tail profile, \(F_j\), \(\bar j\),
peak migration. Not a theorem.

---

## XI. What not to prioritize

For this phase, stop spending primary
effort on:

- Theorem H resurrection.
- Universal \(\rho\)-persistence.
- More exact-shell sweeps.
- A BKM criterion obtained by
  assuming strong spectral decay.
- SFE, \(Q\) operators, Harmonic
  Blueprint, or modified viscosity.
  They are not classical unforced 3-D
  Navier–Stokes.
- Beautiful numerics without a
  theorem-sized inequality.

---

## XII. TASK 6 — four-bucket score

Every object on this desk for the
classical unforced problem sits in
exactly one bucket.

### PROVED

| Object | What sits |
|---|---|
| Spectral identities \(X,Y,Z,\Lambda,T_c,\mathcal D_s\) | Algebra. \(\mathcal D_s\ge 0\). \(X\le\|u\|_2^2\Lambda\). \((\log\Lambda)'=2(T_c-\nu\mathcal D_s)/Y\). |
| TJJ-Trans, TJJ-α, stretch \(\le a_+ Z_j\) | Exact. |
| TJJ-template | Standard lemma. Remainder is \(L^\infty\). |
| \(A.2\) bound on \(F_j\) under \(X\le M\) | Hölder \(6,2,3\) and Poincaré. Not Theorem H. |
| Unrestricted \(\sup\mathcal R_\star<\infty\) is false | Growing-layer \(v_n\). Instantaneous admissible class, not a trajectory. |
| Displayed Theorem H / SND-C as written | Fails even under \(X\le M\). Shear ratio \(\to\infty\). |
| C1 energy-linear \(R\) | TJJ-E-false, \(\lambda^{1/2}\). |
| Designed Attack 9D \(\Theta(m^2)\) | Freiman-AP. |
| \(K=0\); \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\); uniform pre-Young \(C\) | Amplitude / scaling. |
| Theorem G; universal \(t=0\) SND floor | B7c; equal-shell \(v_L\). |
| Theorem A | Extra-stress / \(Q_1\)-NS, this PDE. Not ordinary NS. |

### CLAIMED

| Object | Remaining job |
|---|---|
| Exact-shell \(C=4/3\), \(K\le 16/9\) | Independent reproduction of the projected identity and weighted incidence. Freeze sweeps. |

### OPEN

| Object | What would move it |
|---|---|
| C10 depletion of \(a_+\) | A bound from the dynamics without \(H^1\), \(L^\infty\), or BKM. |
| Estimate (A) as stated | Remainder controlled without the cubic wall. |
| Leftover 5, \(\int\rho_j\) | Class bound, or a field with \(\int\rho_j=\infty\). C10 is the named candidate, not this close. |
| Centered drift \(T_c\le\theta\nu\mathcal D_s+K(t)X\) with useful \(K\in L^1_{\mathrm{loc}}\) | An estimate that is not tautological and that \(v_n\) does not turn into a hidden \(H^1\) ceiling. |
| Replacement energy-budget closure (leftover 4) | A different estimate that \(v_n\) does not kill. Need★ cannot repair the dead box. |
| Leftover 1 = H1 = WRITE (6) | Shape 1, 2, or 3, or \(\mathcal G\to\infty\). Do not start from ABC_λ. |
| SND-to-regularity implication | Frequency drift from the field, plus a non-circular tail. Not a bound on \(X\) today. |
| Hyp-Lat★ | Lattice transfer, or drop the route. |

### DEAD

| Object | Why it stays dead |
|---|---|
| Ordinary NS solved | A ≠ B. Killing ★ is not a blowup. |
| Unrestricted \(\star\) as a bound | \(v_n\). Do not resurrect. |
| Displayed Theorem H as a bridge | Audit. Do not repair. |
| C10 as a seated theorem / leftover 1 | (A) not seated. Named leftover-5 candidate only. |
| Merge C10 with \(T_c\) or with ★ | No explicit inequality. |
| Universal \(\rho\)-persistence | Adversarial families. |
| BKM-from-assumed-decay as the primary | Conditional only. |
| SFE / Q / HB / \(K(t)\) in the PDE | Not classical unforced NS. |
| \(\Phi\)-cancel on Track B | Dropped. |
| Detector occupation decay | Withdrawn. |
| “9D is claimed” as a sentence | Designed 9D is NO. The claimed object is the exact-shell bound. |

---

## What this does not do

It does not restore Theorem H.
It does not unclaim \(4/3\).
It does not run a 9D sweep.
It does not close leftover 1, 4, or 5.
It does not make Ring a theorem.
It does not add \(K(t)\) to the PDE.
It does not put \(\Phi\)-cancel on B.
It does not mail a panel.

NS not solved.

---

## Lock

Primary attack = nonlinear
high-frequency transfer, not SND
persistence.
C10: identities sit; depletion
unwritten; (A) not seated.
Centered drift: identities sit;
estimate OPEN; unrestricted ★ stays
killed.
SND: instrument, not a theorem.
Exact-shell \(K\le 16/9\) = CLAIMED.
Freeze. No more sweeps.
Do not write “9D is claimed.”
Do not work Theorem H.
Do not merge lanes without an
inequality.
Catalog B open stays 1.
NS not solved.
