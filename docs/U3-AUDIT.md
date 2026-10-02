# \(\|u\|_3\) audit — three gates

2 October 2026.
**The derivation is
[`U3-DERIV.md`](U3-DERIV.md).
Owned interpolation sits.
NSE \(L^3\) does not close.
Not beyond ESS.
Not a useful \(K\).
Not a close. ★ stays killed.
Catalog B open stays 1.**

Sign run:
[`SIGN-RUN.md`](SIGN-RUN.md).
The gate:
[`SIGN-GATE.md`](SIGN-GATE.md).
Press spectral L3
(not this object):
[`PRESS.md`](PRESS.md).
SBP / \(H_{1/2}\) charge:
[`SBP.md`](SBP.md).
Energy class:
[`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md).
Target:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
Machine: `python3 scripts/u3_audit.py`.
Does not overwrite `stokes_moments.py`.
Do not start leftover 1.
Do not weld \(\star\).
Do not invent a new mechanism.
Do not invent a bridge.
Do not run Taylor–Green.
Do not alter Lemma A.
No more potentials.

Attack the implication
chain on the derivation
page, not only the
algebra.

---

## Three kinds of sentence

**Exact.**
Serrin index
\(2/p+3/q\).
Energy owns
\(L^4_t L^3\)
(index \(3/2\)).
ESS is
\(L^\infty_t L^3\)
(index \(1\)).
\(\dot H^{1/2}\hookrightarrow L^3\)
one way.
(D1)–(D3) cutoff-uniform.
(D4) while smooth.
(D5) Galerkin commutator.

**Named comparison.**
The three gates.
The interesting
outcome: a
cutoff-uniform NSE
budget on the
growth-capable
portion of \(L^3\),
without first
assuming a
Serrin / ESS
quantity is finite.
That outcome
does not sit.

**Not on this desk.**
A new regularity
mechanism.
ESS as an a priori
on \(X\). Lemma B.
A paid pressure
remainder.

---

## Three gates

**Derivation.**
(D1)–(D3) sit,
cutoff-uniformly,
with named constants
and no hidden higher
norm. (D4) sits as
an identity on the
smooth interval.
A closed Galerkin
inequality paying
the pressure does
not sit. (D5).

**Regularity value.**
The owned time-space
condition is
\(L^4_t L^3\), index
\(3/2>1\), or the
high piece in
\(L^2_t L^3\), index \(2\).
Neither is weaker
than Prodi–Serrin
in the useful
direction. Neither
is beyond
\(u\in L^\infty_t L^3_x\)
of Escauriaza–Seregin–Šverák
(Uspekhi 58, 2003).
Finite-\(p\) \(L^3\)
stays above the line.

**Novelty.**
(D1) is Ladyzhenskaya
interpolation.
(D2) is Sobolev plus
CS. A \(\Lambda\)-weighted
form is \(H_{1/2}\) again.
(D4) is the standard
\(L^p\) testing identity,
closed in the
literature for
\(p>3\), not at \(p=3\).
No exact a priori
\(\|u\|_3\) budget from
NSE was found that
is not one of these.

---

## The key comparison
is scaling

Prodi–Serrin:

\[
u\in L^p_t L^q_x,
\qquad
\frac2p+\frac3q\le 1,
\quad q>3.
\]

The critical endpoint
\(q=3\) forces \(p=\infty\).
That is ESS. A criterion.
Not an a priori on \(X\).
Tao 2019 quantifies ESS.
It still assumes the
\(L^3\) bound.

Energy already owns

\[
u\in L^\infty_t L^2\cap L^2_t L^6
\;\Longrightarrow\;
u\in L^4_t L^3.
\]

Index \(3/2>1\). Owned.
Not Serrin.

Any \(L^p_t L^3\) with
finite \(p\) is still
above the line
(\(1+2/p>1\)).

If a new budget
requires something
already strong enough
to imply Serrin or
ESS, that is a useful
reformulation, not a
new regularity
mechanism.

---

## Microscope

The interesting
outcome is a
cutoff-uniform
NSE-derived budget
that controls only
the growth-capable
portion of the
\(L^3\) behavior
without first
assuming a
Serrin / ESS-class
quantity is finite.

(D3) names that
portion:
\(u_{\ge\kappa_e}\),
\(\|u_{\ge\kappa_e}\|_3\le C_*\kappa_e^{-1/2}X^{1/2}\).
Energy pays it in
\(L^2_t L^3\). Energy
does not pay it in
\(L^4_t L^3\) or
\(L^\infty_t L^3\).
(D4) does not pay
it. The interesting
outcome does not sit.

Common reductions
already scored:

- Energy interpolation
  to \(L^4_t L^3\).
  Already owned. (D1).
- Assume
  \(\|u\|_{L^\infty_t L^3}<\infty\).
  That is ESS.
- Replace the SBP
  charge \(H_{1/2}\)
  by \(\|u\|_3\) using
  a converse Sobolev.
  \(\dot H^{1/2}\hookrightarrow L^3\)
  is one way.
  \(L^3\hookrightarrow\dot H^{1/2}\)
  is false.
- A \(\Lambda\)-weighted
  writing that is
  \(H_{1/2}\) again.
  Already named.
  [`SBP.md`](SBP.md).
- A hidden \(X\),
  \(\|\nabla u\|_\infty\),
  or other higher norm
  inside the constant.
  That is how (D4)
  fails to close.
- PRESS “sharp L3” is
  \(\Phi_e\le W_{\lambda_e}\)
  on the unit torus.
  It is **not**
  \(\|u\|_3\).
  Do not weld.

---

## Literature

- Prodi, *Ann. Mat. Pura Appl.*
  1959. Criterion.
- Serrin, *Arch. Rational
  Mech. Anal.* 9 (1962).
  Criterion.
- Ladyzhenskaya, *The
  Mathematical Theory of
  Viscous Incompressible
  Flow*, 1969.
  Interpolation and
  uniqueness in the
  Serrin class.
- Escauriaza–Seregin–Šverák,
  *Uspekhi Mat. Nauk* 58
  (2003) / *Russian Math.
  Surveys* 58:2 (2003),
  211–250. \(L^\infty_t L^3\)
  criterion. Backward
  uniqueness. Not an
  a priori on \(X\).
- Tao, arXiv:1908.09845.
  Quantitative ESS.
  Still assumes the
  \(L^3\) bound.
- Giga, *J. Differential
  Equations* 62 (1986).
  Local \(L^p\), \(p>3\).
- Robinson–Sadowski–Silva,
  *Rend. Sem. Mat. Univ.
  Padova* 131 (2014).
  \(L^p\) energy identity
  closes for \(p>3\).
  Pressure by CZ.
  von Wahl \(C_t L^3\)
  is a criterion.
- Berselli–Galdi: \(L^3\)
  energy estimates fail
  on bounded domains
  for the same pressure
  reason.

No seated a priori
\(\|u\|_3\) budget from
unaugmented NSE was
found that is not
(D1), (D2), or a
criterion.

---

## What this page is not

- A close. Catalog B
  open stays 1.
- A seating of a new
  \(\|u\|_3\) mechanism.
- A seating of DA-NS-2.
- A restoration of ★.
- Leftover 1.
- A Taylor–Green run.
- [`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md).

---

## Lock

Three gates. Owned interpolation sits.
NSE \(L^3\) remainder not paid.
If it implies Serrin or ESS, it is a reformulation.
G4 stays OPEN. ★ stays killed.
NS not solved.
