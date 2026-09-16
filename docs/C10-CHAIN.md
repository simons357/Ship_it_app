# C10 chain — depletion via \(a_+\) to (A)

16 September 2026.
**Named candidate for leftover 5 / the
local block. Not a theorem. Not leftover 1.
Do not work on Theorem H. Do not extend
9D sweeps. NS not solved.**

Exact-shell 9D stays **CLAIMED**:
[`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md).
Firewall:
exact-shell 9D \(\neq\) unrestricted \(\star\)
\(\neq\) regularity closure.

Three probes of the high-frequency
obstruction sit **beside** each other,
not in series through Theorem H:

1. SND / spectral shape → conditional
   criteria. [`SND-H-REVIEW.md`](SND-H-REVIEW.md),
   [`SND-H-REPAIR.md`](SND-H-REPAIR.md).
2. Near-scale depletion / C10 → (A)?
   This page.
3. Centered spectral drift
   \(T_c=M-\Lambda N\),
   \(\mathcal D_s=Z-\Lambda Y\)
   → \(T_c\le\theta\nu\mathcal D_s+K(t)X\).
   [`CENTERED-DRIFT.md`](CENTERED-DRIFT.md),
   [`LEMMA-STAR.md`](LEMMA-STAR.md).
   Unrestricted \(\star\) is already
   killed by \(v_n\).

Handoff and four-bucket score:
[`NS-STATUS.md`](NS-STATUS.md).
SND instrument (no persistence):
[`SND-INSTRUMENT.md`](SND-INSTRUMENT.md).
Master plan (Route A):
[`MASTER-PLAN.md`](MASTER-PLAN.md).
GPT board vs tape:
[`REPORT-AUDIT.md`](REPORT-AUDIT.md).

Do not merge (2) and (3) unless an
explicit inequality connects them.
BKM from assumed spectral decay is a
useful conditional. It is not the
primary target.

Identities used from the \(T_{j\leftarrow j}\)
write on PR 64 / branch
`cursor/tjj-estimate-chain-e5c5`
([`docs/TJJ-ESTIMATE.md`](https://github.com/simons357/Ship_it_app/blob/cursor/tjj-estimate-chain-e5c5/docs/TJJ-ESTIMATE.md)
on that branch). This page does not
merge that PR. Arithmetic:
`python3 scripts/c10_chain.py`.

Not leftover 1. Do not start H1.
Do not weld \(\star\). Catalog B open
stays 1 (`B_regularity`).

---

## Definitions

Class: smooth divergence-free \(u\) on
a fixed torus or on \(\mathbb{R}^3\),
unforced NS, \(\nu>0\). The
axisymmetric-with-swirl restriction is
the leftover-5 class; the same local
block is the near-scale piece in
unrestricted 3-D. Scope is named at
each claim.

Littlewood–Paley as on
[`AXISYM-SHELL.md`](AXISYM-SHELL.md).
\(u_{\mathrm{loc}}=(\Delta_{j-1}+\Delta_j+\Delta_{j+1})u\),
\(Z_j=\|\Delta_j\omega\|_2^2\),
\(D_j=\|\nabla\Delta_j\omega\|_2^2\),
\[
T_{j\leftarrow j}
=\langle\Delta_j B(u_{\mathrm{loc}}),\Delta_j\omega\rangle,
\qquad
B(\omega,u)=\omega\cdot\nabla u-u\cdot\nabla\omega.
\]

On \(\{\Delta_j\omega\neq 0\}\) set
\(\xi_j=\Delta_j\omega/\lvert\Delta_j\omega\rvert\)
and
\[
\alpha_{\mathrm{loc},j}
=\xi_j\cdot S(u_{\mathrm{loc}})\,\xi_j,
\qquad
a_+
:=\bigl\|(\alpha_{\mathrm{loc},j})_+\bigr\|_\infty.
\]
\(S=\tfrac12(\nabla u+(\nabla u)^{\mathsf T})\).
This \(a_+\) is a direction-weighted
positive strain of the **local**
velocity. It is not \(A_{\mathrm{bad}}\)
and not \(P_+\).

**Estimate (A), the target of C10.**
A bound of the local block that does
not use \(\dot Z_j\) or \(\Lambda'\) as
a majorant, and whose remainder is
controlled without assuming the
desired \(H^1\) ceiling, \(L^\infty\),
or BKM:

\[
(T_{j\leftarrow j})_+
\le
\varepsilon\nu D_j
+C\,a_+ Z_j
+\mathrm{Rem}_j,
\]
with \(\mathrm{Rem}_j\) either absorbed
into \(\varepsilon\nu D_j\) or estimated
by quantities already controlled from
the energy inequality, **or** a named
proof that \(\mathrm{Rem}_j=0\).

If (A) sits with \(\int a_+\,dt<\infty\),
then leftover 5’s [ρ] is implied on
\(\{Z_j>0\}\) up to the infrared sums
already in Lemma AS-IR. That implication
is one direction. It is not a bound on
global \(X\).

---

## Shortlist (what C10 is not)

These were already scored on the local
block. They are not C10.

| id | Sentence | Status |
|---|---|---|
| C1 | \(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu D_j+C\,\mathcal E\,Z_j\) | **DEAD.** TJJ-E-false: \(\lambda^{1/2}\to\infty\). |
| C2 | Bound \(T_{j\leftarrow j}\) by \(\dot Z_j\) | **DISCARD.** Restates AS-Id. |
| C3 | Bound \(T_{j\leftarrow j}\) by \(\Lambda'\) | **DISCARD.** \(\Lambda'\) already contains the leftover. |
| C4 | Only \(T^{\mathrm{ss}}\) remains (no-swirl regularity) | **DEAD.** Mixed samples: \(T^{\mathrm{mm}}\) is the bulk. |
| C5 | Bernstein \(\|u_{\mathrm{loc}}\|_\infty\) / \(\|\nabla u_{\mathrm{loc}}\|_\infty\) into energy | **Circular / cubic wall.** \(W^{1,2}\not\subset L^\infty\). |
| C6 | Assume [ρ] | **Conditional.** Not an a priori. |
| C7 | Tube Hardy on \(T^{\mathrm{ss}}\) | **Not enough.** \(T^{\mathrm{mm}}\) remains. Fat swirl fails localized Hardy. |
| C8 | Theorem H / SND-C | **Withdrawn** even under \(X\le M\). |
| C9 | Assume enough decay that \(\int\|\nabla u\|_\infty\,dt<\infty\) | **BKM sufficient.** Does not attack the dynamics. |
| **C10** | Hypotheses \(\Rightarrow a_+\) estimate \(\Rightarrow\) depletion \(\Rightarrow\) (A), no circular Gronwall | **Named candidate.** Chain below. Not seated. |

---

## The chain, every arrow marked

### Arrow 0 — identities (no (A) yet)

**TJJ-Trans.** EXACT.
\[
\int(u_{\mathrm{loc}}\cdot\nabla)\Delta_j\omega\cdot\Delta_j\omega=0.
\]
Main transport vanishes. The transport
commutator \([\Delta_j,u_{\mathrm{loc}}\cdot\nabla]\)
remains.

**TJJ-α.** EXACT.
\[
\int\bigl((\Delta_j\omega)\cdot\nabla u_{\mathrm{loc}}\bigr)\cdot\Delta_j\omega
=\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2.
\]
Antisymmetric \(\nabla u\) drops.

Hence EXACT:
\[
T_{j\leftarrow j}
=\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2
+T_{j\leftarrow j}^{\mathrm{comm}}.
\]

### Arrow 1 — hypotheses \(\Rightarrow a_+\) estimate

**One-sided stretch.** EXACT.
\[
\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2
\le a_+ Z_j.
\]
This is the definition of \(a_+\). It
does not use \(H^1\), \(L^\infty\) of
\(u\), or BKM. It also does not bound
\(a_+\).

**Brutal question.** Is the right-hand
side secretly \(H^1\) control? **No.**
It is \(a_+ Z_j\). Controlling \(a_+\)
is the next arrow.

### Arrow 2 — \(a_+\) estimate \(\Rightarrow\) depletion

**C10 depletion (the NEW CLAIM).**
The NS dynamics produce
\[
\int_0^T a_+(t)\,dt<\infty
\]
(or a stronger pointwise bound that
can be absorbed into \(\varepsilon\nu D_j\))
from the equation, **without** assuming
\(X\in L^\infty_t\), \(\|u\|_\infty\),
\(\|\nabla u\|_\infty\), BKM, [ρ], or
(A).

**Status: unwritten.** All-data
geometric depletion of
\(\lvert\cos\alpha_3\rvert\) already
**failed** as an a priori (B25a).
Constantin–Fefferman is a criterion:
*if* alignment is depleted, stretching
is weaker. That is the converse of
C10’s arrow. A printed \(\alpha\) on
samples is Door 3, not this claim.

**Brutal question.** Is “depletion”
here equivalent to, stronger than, or
dependent on the desired \(H^1\)
control? **As usually written, yes it
depends.** Bounding
\(\|(\xi\cdot S\xi)_+\|_\infty\) by
Sobolev uses \(\|\nabla u\|_\infty\) or
a supercritical norm. That is BKM-adjacent
or circular for continuation. A
non-circular C10 must bound \(a_+\)
from the *dynamics* (vortex stretching
structure, local cancellation, or a
monotone quantity), not from an
embedding of the unknown field.

### Arrow 3 — depletion \(\Rightarrow\) (A)

**TJJ-template.** STANDARD LEMMA
(Young + Bernstein remainder).
\[
T_{j\leftarrow j}
\le
\varepsilon\nu D_j
+a_+ Z_j
+C_\varepsilon[\varphi]\,\nu^{-1}\|u_{\mathrm{loc}}\|_\infty^2 Z_j
+C[\varphi]\,\|\nabla u_{\mathrm{loc}}\|_\infty\sum_{|k-j|\le 1}Z_k.
\]
This inequality **sits**. Its last two
terms are **not** in (A) as stated.
They are \(L^\infty\) of local velocity
and strain.

**C10 remainder claim (NEW CLAIM).**
Those two terms are absorbed without
\(L^\infty\), or vanish, or are
estimated from energy / \(Z\) only.

**Status: false as energy-only**
(C1 / TJJ-E-false). **Unwritten** as a
dynamical estimate. Completing (A)
from the template by Bernstein puts
\(2^{3j}\) or \(X^{3/2}\) back in, which
is the cubic wall: Gronwall then wants
the \(H^1\) ceiling one is proving.

**Brutal question.** Does this arrow
use the desired conclusion? **If the
commutators are estimated in \(L^\infty\),
yes (BKM / continuation).** If they are
left in (A), then (A) is not closed.
If they are claimed to vanish, that is
a separate exact identity and must be
stated (TJJ-Trans kills only the
*main* transport, not the commutator).

---

## Dependency graph

```
smooth NSE, Δ_j, u_loc          EXACT defs
        |
        v
TJJ-Trans + TJJ-α               EXACT
        |
        v
stretch ≤ a_+ Z_j               EXACT (def of a_+)
        |
        +---- TJJ-template commutators     STANDARD; L^∞ remainder
        |
        v
C10 depletion of a_+            NEW CLAIM; unwritten
        |
        v
(A)                             NEW CLAIM; not seated
        |
        v
[ρ] / leftover 5                FOLLOWS from (A)+∫a_+  (one direction)
        |
        x  not  x
        v
global X / leftover 1 / ★       NOT IMPLIED. Do not weld.
```

Gronwall on \(Z_j\) or on \(X\) sits
**after** (A). Using Gronwall to get
the coefficients in (A) is the circular
step C10 is required to avoid.

---

## Adversarial families

No new 9D sweeps. These are the
families already on the desk.

### 1. High-tail shears (SND audit)

\(u=f(y)\,e_1\), \((u\cdot\nabla)u\equiv 0\).
Vorticity is in \(e_3\), strain is
off-diagonal in the \(xy\)-plane, so
\(\xi\cdot S\xi=0\) on the support of
\(\omega\). Thus \(a_+=0\) and
\(T_{j\leftarrow j}=0\). C10 holds as
\(0\le 0\). Same verdict as the
repaired \(F_j\) bound: it no longer
answers the question that killed
Theorem H. Locked in
`scripts/c10_chain.py`.

### 2. Amplitude \(u=Aw\)

\(Z\to A^2 Z\), \(T\to A^3 T\),
\(a_+\to A a_+\), so \(a_+ Z\to A^3\).
The \(a_+ Z_j\) majorant matches the
cubic. Energy-linear \(C\,\mathcal E Z_j\)
is quadratic in \(A\) and **fails**
(C1). C10 passes this family only if
it keeps \(a_+\) in the majorant and
does not replace it by energy.

### 3. Equal-enstrophy shells / \(v_L\)

\(\rho(0)=1/L\) arbitrarily small.
A bound on the *rate* of \(a_+\) does
not create a universal floor at \(t=0\).
Consistent, not a kill of Arrow 1.
A later theorem from C10 must be
conditioned on the initial local
block, not asserted uniformly.

### 4. Growing-layer \(v_n\) (unrestricted ★)

Admissible. \(\mathcal R_\star(v_n)\to\infty\).
C10 does not resurrect unrestricted
\(\star\). If \(a_+(v_n)\) stays bounded
while \(T_c/\mathcal D_s\) blows, C10
cannot imply the centered estimate
without an extra inequality. Do not
merge. [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).

### 5. Compact mixed swirl (leftover 5 samples)

\(T^{\mathrm{mm}}\) is the bulk.
Pure-swirl vanishing is not this
class. Occupancy \(55/56\) on the
peak remainder shell did not fall
with \(n\). Not [ρ]. Not a close of
C10. [`AXISYM-SWIRL-PROBE.md`](AXISYM-SWIRL-PROBE.md).

---

## Can C10 bound \(T_c\)?

\(T_c=M-\Lambda N\) is a **centered**
pairing against \((A-\Lambda)u\).
\(a_+ Z_j\) is an \(L^\infty\) strain
times one shell’s enstrophy. There is
no seated inequality
\(T_c\le C\sum_j a_+ Z_j\).
Do not write one. If a later estimate
connects them, display it and re-test
\(v_n\) and the shears. Until then the
two probes stay separate.

---

## Verdict

| Claim | Status |
|---|---|
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Freeze. No more sweeps. Independent reproduction of the projected identity and weighted incidence is the remaining job. |
| Designed 9D \(\Theta(m^2)\) | **NO.** |
| Unrestricted \(\star\) | **KILLED** by \(v_n\). |
| Theorem H | **Withdrawn.** Do not work it. |
| TJJ-Trans / TJJ-α / one-sided \(a_+ Z_j\) | **Sits.** EXACT. |
| TJJ-template | **Sits.** Remainder is \(L^\infty\). |
| C1 energy-linear \(R\) | **DEAD.** |
| C10 depletion of \(a_+\) | **OPEN / NEW CLAIM.** |
| (A) as stated | **Not seated.** Commutators or embeddings reintroduce \(L^\infty\) or the cubic wall. |
| C10 \(\Rightarrow\) leftover 5 | **Not implied** until (A) and \(\int a_+\) sit. |
| C10 \(\Rightarrow\) leftover 1 or \(\star\) | **NO.** Do not weld. |
| Merge C10 with \(T_c\) | **NO** without an explicit inequality. |
| BKM-from-spectral-decay as primary | **NO.** Conditional only. |

If C10 dies, that is cheap: the
non-circular depletion of \(a_+\) is
the only new arrow, and it is the
same obstruction B25a already named
for all-data geometry. If a later
write bounds \(a_+\) from the
equation without \(H^1\), \(L^\infty\),
or BKM, that write is the candidate
mechanism. It is not on this page.

---

## What this does not do

It does not restore Theorem H.
It does not unclaim \(4/3\).
It does not run a 9D sweep.
It does not close leftover 1, 4, or 5.
It does not make Ring a theorem.
It does not add \(K(t)\) to the PDE.
It does not put \(\Phi\)-cancel on B.

NS not solved.

---

## Lock

Exact-shell 9D = CLAIMED. Freeze.
exact-shell 9D ≠ unrestricted ★ ≠ regularity.
Do not work on Theorem H.
C10: a_+ := ||(α_loc,j)_+||_∞.
stretch ≤ a_+ Z_j EXACT.
depletion of a_+ NEW CLAIM, unwritten.
(A) not seated: commutators are L^∞.
C1 energy-linear R DEAD (λ^{1/2}).
Shears: a_+=0 and T=0.
Do not merge T_c.
BKM-from-decay is not the primary.
Leftover 5 stays OPEN.
Handoff: NS-STATUS.md.
NS not solved.
