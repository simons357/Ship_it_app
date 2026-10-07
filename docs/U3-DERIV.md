# \(\|u\|_3\) derivation

2 October 2026.
Corrected 3 October 2026
from the historical audit
screenshots. Not a fresh
verification of the full
source, constants, or
domain hypotheses.
**D1–D3 retained at
stated scope.
\(L^4_t L^3\) is not Serrin.
\(\int X^2\) supplies
\(L^4_t L^6\).
D4 pressure unpaid.
D5 remainder unnamed.
No budget derived here.
Not an impossibility
theorem. Not a close.
★ stays killed.
Catalog B open stays 1.**

Three-gate score:
[`U3-AUDIT.md`](U3-AUDIT.md).
Press spectral L3
(not this object):
[`PRESS.md`](PRESS.md).
SBP / \(H_{1/2}\):
[`SBP.md`](SBP.md).
Energy class:
[`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md).
Target:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
Share-gates (not Track A/B):
[`SHARE-GATES.md`](SHARE-GATES.md).
Machine: `python3 scripts/u3_audit.py`.
Does not overwrite `stokes_moments.py`.
Do not start leftover 1.
Do not weld \(\star\).
Do not invent a new mechanism.
Do not invent a bridge.
Do not run Taylor–Green.
Do not alter Lemma A.
Do not alter \(L_{1,N}\).
No more potentials.

The implication chain is
below. Attack that, not
only the algebra.

---

## Correction — 3 October 2026

Recorded from the
screenshots. Not a
re-derivation.

**Serrin.** The sentence
that the high piece
“is Serrin in
\(L^4_t L^3\) only after
\(\int X^2<\infty\)”
is withdrawn. For
\(L^4_t L^3\),
\(2/4+3/3=3/2>1\).
That space stays
outside the classical
Serrin range no matter
how the bound is
obtained. If
\(X=\|\nabla u\|_2^2\),
the extra assumption
\(\int X^2<\infty\),
with the energy bound
and Sobolev, gives
\(u\in L^4_t L^6\),
and \(2/4+3/6=1\).
Serrin arrives through
that different space.
Deriving the extra
control from the
unaugmented equations
stays the unresolved
task.

**Scope.** D1, D2, D3
stay as reusable
estimates at the
stated scope, subject
to verification of the
full source, constants,
and domain assumptions.
Do not reverse
\(\dot H^{1/2}\hookrightarrow L^3\).
An \(L^3\) bound alone
does not give
\(\dot H^{1/2}\).

**Obstacles.** D4 is
an unresolved pressure
contribution in the
\(L^3\) testing identity.
D5 is a projection
remainder when the
spectral Galerkin
equation is tested
with \(\lvert u^N\rvert u^N\).
The remainder must be
estimated uniformly
in the cutoff. Its
appearance alone does
not prove that every
possible estimate
requires a higher
norm.

**Negative conclusion.**
The estimates reviewed
here do not establish
the missing
cutoff-uniform a priori
budget. No such budget
was derived in this
audit. “No new
mechanism was found”
is a search result,
not an impossibility
theorem. A
reformulation may
still be useful. A
new regularity
conclusion requires
an independently
established estimate.

This correction does
not close the remaining
gap and does not
revive a previously
rejected estimate.
Historical OPEN and
KILLED labels keep
their statements,
hypotheses, and
evidence.

---

## Setup and letters

Unit torus, mean-zero,
divergence-free. Spectral
Galerkin field \(u^N\),
cutoff \(N\). Drop \(N\)
where the bound is uniform
in \(N\). Viscosity \(\nu>0\).
Force zero.

SBP letters, not the
chain’s enstrophy \(E\):

\[
E=\|u\|_2^2=\sum_k\lvert a_k\rvert^2,
\qquad
X=\|\nabla u\|_2^2=\sum_k\lvert k\rvert^2\lvert a_k\rvert^2,
\]

\[
H_{1/2}=\sum_k\lvert k\rvert\lvert a_k\rvert^2,
\qquad
\Lambda=X/E.
\]

Energy, while smooth:

\[
\tfrac12 E'+ \nu X=0
\qquad\Rightarrow\qquad
\int_0^T X\le E(0)/(2\nu),\quad
E(t)\le E(0).
\]

Named constants:
\(C_S\) Sobolev \(\dot H^1\hookrightarrow L^6\),
\(C_*\) Sobolev \(\dot H^{1/2}\hookrightarrow L^3\),
\(C_B\) Bernstein \(L^2\to L^3\) on
frequencies \(\lvert k\rvert<\kappa\),
\(C_{\mathrm{CZ}}\) Calderón–Zygmund
for the torus pressure.
Absolute on this torus.
No hidden \(X\), no
\(\|\nabla u\|_\infty\).

---

## D1 — interpolation
(cutoff-uniform)

Hölder, then Sobolev:

\[
\|u\|_3
\le
\|u\|_2^{1/2}\|u\|_6^{1/2}
\le
C_S^{1/2} E^{1/4} X^{1/4}.
\tag{D1}
\]

Fourth power and the
energy identity:

\[
\int_0^T\|u\|_3^4\,dt
\le
C_S^2(\sup E)\int_0^T X\,dt
\le
\frac{C_S^2 E(0)^2}{2\nu}.
\tag{D1t}
\]

Galerkin: \(P_N\) is an
\(L^2\) and \(\dot H^1\)
contraction. \(C_S\) does
not see \(N\). Cutoff-uniform.

Serrin index
\(2/4+3/3=3/2>1\).
Owned. Not Serrin.

---

## D2 — one-way Sobolev
and CS on \(H_{1/2}\)

\[
\|u\|_3
\le
C_* H_{1/2}^{1/2}.
\tag{D2}
\]

Cauchy–Schwarz on the
modes:

\[
H_{1/2}
\le
E^{1/2}X^{1/2}.
\tag{D2cs}
\]

Equality on a single
shell. Therefore

\[
\|u\|_3
\le
C_*(EX)^{1/4},
\]

the same scaling as (D1).
A \(\Lambda\)-weighted
writing \(H_{1/2}\le E\sqrt{\Lambda}\)
is (D2cs). It is not a
new budget.

\(\dot H^{1/2}\hookrightarrow L^3\)
is one way.
\(L^3\hookrightarrow\dot H^{1/2}\)
is false. Do not replace
the SBP charge by
\(\|u\|_3\).

---

## D3 — frozen-cutoff split
(growth-capable piece)

Fix \(\kappa\ge 1\). Write
\(u=u_{<\kappa}+u_{\ge\kappa}\).

Bernstein, \(L^2\to L^3\),
exponent \(3(1/2-1/3)=1/2\):

\[
\|u_{<\kappa}\|_3
\le
C_B\kappa^{1/2}E^{1/2}.
\tag{D3lo}
\]

High modes,
\(\lvert k\rvert^{1/2}\le\kappa^{-1/2}\lvert k\rvert\):

\[
\|u_{\ge\kappa}\|_3
\le
C_*\kappa^{-1/2}X^{1/2}.
\tag{D3hi}
\]

Optimize \(\kappa^2=X/E=\Lambda\).
Both pieces become
\(C E^{1/4}X^{1/4}\). That is (D1)
again.

Freeze \(\kappa=\kappa_e\),
the epoch center. Then
the low piece is

\[
\sup_t\|u_{<\kappa_e}\|_3
\le
C_B\kappa_e^{1/2}E(0)^{1/2}.
\]

Owned. Not growth-capable
while \(\kappa_e\) is fixed.

The high piece is the
growth-capable portion:

\[
\|u_{\ge\kappa_e}\|_3
\le
C_*\kappa_e^{-1/2}X^{1/2}.
\]

Time integrability of
that piece alone:

- \(L^2_t L^3\):
  \(\int\|u_{\ge\kappa_e}\|_3^2\le C_*^{2}\kappa_e^{-1}\int X\).
  Energy. Index \(2/2+3/3=2>1\).
- \(L^4_t L^3\):
  \(\int\|u_{\ge\kappa_e}\|_3^4\le C_*^{4}\kappa_e^{-2}\int X^2\).
  Index \(2/4+3/3=3/2>1\).
  Still not Serrin,
  however the bound is
  obtained.
- The same extra
  assumption
  \(\int X^2<\infty\),
  with energy and
  Sobolev
  \(\|u\|_6\lesssim X^{1/2}\),
  gives
  \(u\in L^4_t L^6\).
  Index \(2/4+3/6=1\).
  That is Serrin, in a
  different space.
  Deriving \(\int X^2\)
  from the unaugmented
  equations is the
  unresolved task.
- \(L^\infty_t L^3\):
  needs \(\sup X/\kappa_e<\infty\).
  Enstrophy bound, or ESS
  on the high piece.

Cutoff-uniform. Constants
named. No hidden higher
norm inside (D3lo)–(D3hi).
The interesting control
is not in those two lines.
It is in a time-space
budget on \(u_{\ge\kappa_e}\)
that energy does not give.

---

## D4 — NSE \(L^3\) identity
(while smooth)

On the torus, test the
smooth NSE with \(\lvert u\rvert u\).
Divergence-free kills
convection:

\[
\int(u\cdot\nabla)u\cdot\lvert u\rvert u
=
\tfrac13\int(u\cdot\nabla)\lvert u\rvert^3
=
0.
\]

Viscosity is exact:

\[
-\nu\int\Delta u\cdot\lvert u\rvert u
=
\nu\int\lvert u\rvert\lvert\nabla u\rvert^2
+
\nu\int\lvert u\rvert\lvert\nabla\lvert u\rvert\rvert^2.
\]

Pressure remains:

\[
\int\nabla p\cdot\lvert u\rvert u
=
-\int p\,(u\cdot\nabla\lvert u\rvert).
\]

Calderón–Zygmund
(\(1<q<\infty\)):

\[
\|p\|_{3/2}
\le
C_{\mathrm{CZ}}\|u\|_3^2.
\]

Therefore, while smooth,

\[
\tfrac13\frac{d}{dt}\|u\|_3^3
+
\nu\int\lvert u\rvert\lvert\nabla u\rvert^2
+
\nu\int\lvert u\rvert\lvert\nabla\lvert u\rvert\rvert^2
=
\int p\,(u\cdot\nabla\lvert u\rvert).
\tag{D4}
\]

The left viscous form
does not absorb the
right-hand side from
energy-class quantities
alone. D4 therefore
identifies an
unresolved pressure
contribution in the
\(L^3\) testing identity.
Robinson–Sadowski–Silva
close a related
identity for \(p>3\),
not at \(p=3\).
Giga local existence is
\(L^p\), \(p>3\). von Wahl
is continuity in \(L^3\),
a criterion.

No hidden higher norm
was put in (D4). Paying
the pressure was not
derived here. That is
not a theorem that
every closing attempt
inserts a hidden
higher norm.

---

## D5 — Galerkin commutator
(projection remainder)

The Galerkin equation
is tested in the finite
mode space. \(\lvert u^N\rvert u^N\)
is not in that space.

\[
\langle P_N((u^N\cdot\nabla)u^N),\lvert u^N\rvert u^N\rangle
=
\langle(u^N\cdot\nabla)u^N,P_N(\lvert u^N\rvert u^N)\rangle.
\]

The convection identity
of D4 is then replaced
by a commutator

\[
R_N
=
\langle(u^N\cdot\nabla)u^N,P_N(\varphi)-\varphi\rangle,
\qquad
\varphi=\lvert u^N\rvert u^N.
\]

\(P_N\) is bounded on \(L^3\)
uniformly in \(N\) (Mihlin,
\(1<p<\infty\)). The
remainder \(R_N\) must
be estimated uniformly
in the cutoff. Its
appearance alone does
not prove that every
possible estimate
requires a higher
norm.

So: (D1)–(D3) are
written as
cutoff-uniform
comparisons at the
stated scope, subject
to source, constant,
and domain checks.
(D4) is an identity on
the smooth interval.
A closed Galerkin
\(L^3\) inequality with
constants independent
of \(N\) and with the
pressure paid was
**not derived** in
this audit.

---

## Implication chain
(attack this)

**I1.** Energy \(\Rightarrow\)
\(u\in L^4_t L^3\). (D1).
Index \(3/2\). Owned.
Not regularity.

**I2.** \(\dot H^{1/2}\hookrightarrow L^3\)
and \(H_{1/2}\le\sqrt{EX}\)
recover the same
\(L^4_t L^3\). (D2).
A \(\Lambda\)-weighted
writing is the same
comparison. Converse
Sobolev is false.

**I3.** Split at \(\kappa\).
Optimize \(\kappa^2=\Lambda\):
back to I1.
Freeze \(\kappa=\kappa_e\):
the low piece is owned
in \(L^\infty_t L^3\);
the high piece is owned
in \(L^2_t L^3\) (index \(2\)).
A bound of that piece
in \(L^4_t L^3\) still has
index \(3/2>1\). It is
not Serrin. The extra
assumption
\(\int X^2<\infty\)
supplies Serrin through
\(L^4_t L^6\), not through
\(L^4_t L^3\). Deriving
that extra control
from the unaugmented
equations is open.
The growth-capable
portion is named.
It is not paid by
energy alone.

**I4.** NSE \(L^3\) identity:
convection dies,
pressure is an
unresolved
contribution.
A cutoff-uniform
payment of that
contribution was not
derived. The Galerkin
remainder in D5 must
be estimated uniformly
in \(N\). Its appearance
alone is not a proof
that every estimate
needs a higher norm.

**I5.** ESS: if
\(u\in L^\infty_t L^3\),
then regular.
Escauriaza–Seregin–Šverák,
Uspekhi 58 (2003).
A criterion. Tao 2019
quantifies the same
hypothesis. Neither
is an a priori on \(X\).

**I6.** The estimates
reviewed here do not
establish the missing
cutoff-uniform a priori
budget. No such budget
was derived in this
audit. That is not an
impossibility theorem
for the \(L^3\)
direction.

**I7.** PRESS “sharp L3”
is \(\Phi_e\le W_{\lambda_e}\),
not \(\|u\|_3\). Do not weld.

If a later writing
already assumes a
Serrin or ESS
quantity, it is a
reformulation of a
known criterion, not
by itself a new
regularity conclusion.
A reformulation may
still be useful. A
new regularity
conclusion requires
an independently
established estimate.
“No new mechanism
was found” is a
search result, not
an impossibility
theorem.

---

## What this page is not

- A close. Catalog B
  open stays 1.
- A seating of ESS
  as an a priori.
- A useful \(K\) in
  \(T_c\le\theta\nu\mathcal D_s+K(t)X\).
- A seating of Lemma B
  or DA-NS-2.
- A restoration of ★.
- Leftover 1.
- A Taylor–Green run.
- [`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md).

---

## Lock

D1–D3 retained at stated scope.
\(L^4_t L^3\) is not Serrin. \(\int X^2\) supplies \(L^4_t L^6\).
No cutoff-uniform a priori budget was derived in this audit.
Not an impossibility theorem. G4 stays OPEN. ★ stays killed.
NS not solved.
