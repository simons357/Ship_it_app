# Fourier-triangle geometry — identities, then the missing arrow

20 September 2026.
**Reconstruction. Not a close.
Unrestricted ★ stays killed by \(v_n\).
B★ is not a universal \(C\).
Catalog B open stays 1.
NS not solved.**

Machine: `python3 scripts/fourier_triangle.py`.
Does not overwrite `stokes_moments.py`.
Identities already locked:
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Two-shell gap-cancel:
[`NEED-STAR-HH-L-DUAL.md`](NEED-STAR-HH-L-DUAL.md).
Pairing:
[`BSTAR-PROOF.md`](BSTAR-PROOF.md).
Time-dependent target:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
First lift (two-shell sits;
third eigenvalue dies;
\(K\sim\sqrt{E}\) dead):
[`TRIANGLE-LIFT.md`](TRIANGLE-LIFT.md).
Energy-class ladder (all
three amplitude-legal doors
die on \(v_n\)):
[`ENERGY-K.md`](ENERGY-K.md).
Pairing CS doors (tight is
★; LE dead; LX not a
universal \(C\)):
[`L-DOOR.md`](L-DOOR.md).
Instantaneous \(MN\)
(\(N=0\) on \(v_n\); no
uniform \(\theta<1\)):
[`MN-CANCEL.md`](MN-CANCEL.md).
First jet (Stokes keeps
\(N=0\); \(T_c\) grows):
[`PATHWISE.md`](PATHWISE.md).
Short interval (Stokes
keeps \(N=0\); NSE keeps
\(R_{mn}=1\)):
[`INTERVAL.md`](INTERVAL.md).
Incoming ledger (two-shell
product sits; \(\alpha+\beta=\Lambda\)
empty on two shells):
[`CENTERED-LEDGER.md`](CENTERED-LEDGER.md).
Chart reset:
[`RESET.md`](RESET.md).

Do not start leftover 1.
Do not weld \(\star\).
Do not cash B★ as G5.

---

## Three kinds of sentence

**Exact identities.** Algebra on a
mean-zero divergence-free field.
They sit on every admissible snapshot.
A machine residual at \(10^{-16}\) is
a check, not the reason.

**Numerical observations.** Printed
sizes on named triangles. They can
change with phase or seed. They are
not \(C\) and not a kill.

**Illustrative motion.** A phase of
one leg is rotated by hand. That is
not an NSE trajectory and not a
blowup.

Do not mix the three.

---

## The vertex (exact)

On \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\),

\[
v=\sum_{k\neq0}v_ke^{ik\cdot x},\qquad
k\cdot v_k=0,\qquad
v_{-k}=\overline{v_k}.
\]

A Fourier triangle is an ordered
lattice triple with \(p+q=k\), all
nonzero. The cubic vertex is

\[
I_3(p,q;k)
=
(q\cdot v_p)\,(v_q\cdot\overline{v_k}).
\]

Signed modal transfer (keep
\(\mathrm{Im}\); never replace by
\(\lvert\cdot\rvert\)):

\[
T_k
=
\sum_{p+q=k}
\mathrm{Im}\,I_3(p,q;k).
\]

Stokes bilinear, both orders, no
extra \(1/2\):

\[
\widehat B_k
=
i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q,
\qquad
P_k=I-\frac{k\otimes k}{\lvert k\rvert^2}.
\]

Because \(P_k\) is self-adjoint and
\(P_kv_k=v_k\), the energy pairing
drops Leray:

\[
T_k
=
-\mathrm{Re}\bigl(\widehat B_k\cdot\overline{v_k}\bigr)
=
-\mathrm{Re}\bigl(i\sum(q\cdot v_p)v_q\cdot\overline{v_k}\bigr).
\]

That is **Leray idle in \(T_k\)**.
Leray is *not* idle in
\(\|\Pi_\beta B\|_2\) (exact-shell
\(K\)). Two objects. Do not glue.

Energy of the bilinear:

\[
\sum_k T_k=0.
\]

On a conjugate-closed isolated
triangle the three shells (or the
three keys and their mates) satisfy
the cyclic sum \(T_p+T_q+T_k=0\).

Centered drift (one pairing):

\[
T_c
=
\sum_k\lambda_k(\lambda_k-\Lambda)T_k
=
\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\,I_3(p,q;k).
\]

\(\lambda_k=\lvert k\rvert^2\),
\(\Lambda=Y/X\). Do not split
\(M\) and \(\Lambda N\) as the
first move.

---

## Shell placement (exact)

A triangle occupies one, two, or
three Stokes eigenvalues.

| Placement | Shells | What the weight does |
|---|---|---|
| Equal-length | \(\lambda_p=\lambda_q=\lambda_k\) | \(\Lambda=\lambda\), so \(\lambda(\lambda-\Lambda)=0\). \(T_c=0=\mathcal D_s\). Vacuous. |
| Isosceles / two-shell | \(\lambda_p=\lambda_q=\alpha\neq\beta=\lambda_k\) | One gap. \(T_\alpha+T_\beta=0\). |
| Unequal-length | three distinct \(\lambda\) | Two independent signed transfers. No single-gap reduction. |

**Equal-length cancellation (exact).**
One Fourier shell \(\Rightarrow
\mathcal D_s=0\Rightarrow T_c=0\).
Not a kill. Locked on a two-mode
shell in the machine.

**Two-shell gap-cancel (exact).**
Energies \(e_\alpha,e_\beta\),
\(E=e_\alpha+e_\beta\),
\(X=\alpha e_\alpha+\beta e_\beta\):

\[
T_c
=
(\alpha-\beta)\frac{\alpha\beta E}{X}\,T_\alpha
=
-(\alpha-\beta)\frac{\alpha\beta E}{X}\,T_\beta,
\]

\[
\mathcal D_s
=
\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{X}.
\]

The gap \((\alpha-\beta)\) drops
out of \(\mathcal R_\star\). That
identity sits. It is not Need★.

Locked on
\(p=(1,1,0)\), \(q=(1,-1,0)\),
\(k=(2,0,0)\):
\(\alpha=2\), \(\beta=4\),
\(T_\alpha+T_\beta=0\) at
\(10^{-16}\),
\(T_c\) matches the gap formula
at \(10^{-15}\).

**Unequal-length defect (exact).**
Three distinct \(\lambda\) give
three weights
\(\lambda(\lambda-\Lambda)\).
Energy conservation removes one
degree of freedom, not two.
\(T_c\) is not a single \(T_\lambda\)
times one gap.

Locked on
\(k_0=(2,0,0)\), \(e=(0,1,0)\):
shells \(4,5,17\).
\(T_c/T_\lambda\) prints three
different numbers
(\(\approx-199\), \(-1710\), \(178\)).
That is the defect.

---

## Polarizations (exact, then a reading)

Each \(v_k\) lives in the complex
plane \(k^\perp\). That is the
divergence-free restriction.
Independent complex amplitudes
in that plane are legal.

**Vertex-idle polarization (exact
on a named triangle).** Pure-\(z\)
on both inputs of
\((1,1,0)+(1,-1,0)=(2,0,0)\)
makes \(q\cdot v_p=0\). Then
\(I_3=0\) and \(T_c=0\). The
triangle is present. The vertex
is not. LEMMA-STAR-E already
named a parallel-\(e\) zero as
accidental, not a bound.

**Live in-plane polarization
(numerical).** The same keys
with seeds \((1,-1,0.4)\),
\((1,1,0.4)\), \((0,1,0.7)\)
give \(\mathrm{Im}\,I_3\neq 0\)
and \(T_c\approx 3.657\) at
phase \(0.5\). Finite. Not \(C\).

Helical polarization of a
power-law spectrum makes
\(T_c\approx 0\). Imag of the
same spectrum does not
([`BSTAR.md`](BSTAR.md)).
Polarization is the content.
A bound that forgets it is
unsigned CS.

---

## Phase-dependent signed transfer

**Exact.** \(I_3\) is complex.
\(T_c\) is odd under
\(v\mapsto -v\). A relative
phase on one leg can flip the
sign of \(\mathrm{Im}\,I_3\).

**Numerical (illustrative motion,
not NSE).** Rotate the mid-leg
phase through a period.

| Triangle | \(\min T_c\) | \(\max T_c\) | Changes sign |
|---|---|---|---|
| Isosceles \(2,2,4\) | \(-5.08\) | \(+5.08\) | yes |
| Unequal \(4,5,17\) | \(-25.6\) | \(+25.4\) | yes |

Same keys, same amplitudes, both
signs. The geometry does not pick
the stretching orientation. The
viscous remainder fights only
\((T_c)_+\). Reverse the field and
the same triangle stretches.

---

## Where the geometry is lost

The identities are per triangle,
per snapshot.

**Lost at the sum.**
The living \(T_c\) is the *signed*
sum over every lattice triangle.
Replacing \(\mathrm{Im}\) by
\(\lvert\mathrm{Im}\rvert\) hides
occupancy \(s\) (same hole as
\(K\le 16s\)). Mixing HH→L,
HL→H, and LL→H lets weights of
opposite sign cancel or add.
A bound that estimates each
channel by its size, then adds,
throws the only cancellation the
vertex has.

**Lost at the evolution.**
\(\Lambda(t)\) is itself moved by
\(T_c\):

\[
\Lambda'=\frac{2}{X}(T_c-\nu\mathcal D_s).
\]

The weights \(\lambda(\lambda-\Lambda)\)
are dynamical. New keys light.
An isolated-triangle identity
does not close the cascade. A
phase that cancels at \(t=0\)
is not a phase that stays
cancelled. Snapshot \(I_3\) is
not a pathwise \(K(t)\).

That is the precise loss: the
mechanism that sits on one
triangle does not survive as a
majorant of the *summed, evolved*
pairing.

---

## \(I_3\) prime restrictions

\(I_3\) is the cubic Fourier
vertex. It is **not** leftover 3
(H3 absorb as \(r\to 0\)). It is
**not** the Q-matrix prime block.
Those are other books. Do not
weld.

**Prime** here means: an
irreducible restriction that
sits as an identity on every
admissible field. Drop it and
you are not computing NS \(B\).

| Restriction | Verdict |
|---|---|
| Lattice triangle \(p+q=k\) in \(\mathbb{Z}^3\setminus\{0\}\) | **Prime.** Support of \(I_3\). |
| Transverse polarizations \(k\cdot v_k=0\) | **Prime.** Divergence-free. |
| Leray idle in the energy pairing | **Prime.** \(P_k\) drops from \(T_k\). Not from \(\|\Pi_\beta B\|_2\). |
| Reality \(v_{-k}=\overline{v_k}\) | **Prime.** Real fields. |
| Cyclic energy \(T_p+T_q+T_k=0\) | **Prime.** On each conjugate-closed triad, and globally \(\sum T_k=0\). |
| Equal-length kills the \(T_c\) weight | **Prime.** One shell is vacuous. |
| Two-shell gap-cancel of \((\alpha-\beta)\) in \(\mathcal R_\star\) | **Prime** as an identity. Not Need★. |
| Prime \(\lvert k\rvert^2\) shells only | **Not prime.** Composite shells carry the same vertex. |
| Primitive \(\gcd=1\) triangles as a bound | **Not prime.** Dilation already leaves \(\mathcal R_\star\) invariant. |
| Leftover 3 / H3 | **Not this \(I_3\).** Local ball absorb. |
| Q-matrix prime block | **Not this book.** |
| Unsigned \(\lvert I_3\rvert\) | **Not prime.** Kills the sign that is the content. |
| HH→L only | **Not prime.** Incomplete \(T_c\). |

The prime list is the mechanism.
The not-prime list is how people
lose it, or weld another leftover.

---

## First missing implication

Preserve every identity above.
The time-dependent bound already
written as the close-shaped
target is Route B
([`CENTERED-DRIFT.md`](CENTERED-DRIFT.md),
[`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md)):

\[
T_c
\le
\theta\nu\mathcal D_s
+K(t)X,
\qquad
\theta<1,
\]

with \(K\) useful (energy-class,
or a named dynamical cancellation
that does not assume the \(H^1\)
ceiling, \(L^\infty\), or BKM).
If that sits,
\(\Lambda'\le 2K\), and
\(X\le\|u\|_2^2\Lambda\) stays
finite on the torus.

**First missing arrow.**

From

\[
T_c
=
\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\,I_3(p,q;k)
\]

together with Leray-idle pairing,
cyclic energy, equal-length
cancel, and two-shell gap-cancel,
one does **not** obtain a useful
majorant of the summed \(T_c\).
The identities name the pairing.
They do not bound it after the
sum and the evolution.

That is the first missing
implication to the full
time-dependent bound. It is G4.
It is not G5. B★ was a candidate
majorant and does not sit as a
universal \(C\). Unrestricted ★
was a uniform geometric remainder
and is killed by \(v_n\).
Need★ cannot repair that box.
Tautological
\(K=(T_c-\theta\nu\mathcal D_s)_+/X\)
is not this arrow.

A later write may kill G4 with a
named family, or seat a different
useful \(K\). The energy-class
ladder is now dead
([`ENERGY-K.md`](ENERGY-K.md)).
This page does not seat a
replacement.

---

## What this page is not

- A close. Catalog B open stays 1.
- A restoration of ★.
- A seating of B★.
- Need★. The signed dual on HH→L
  is still MISSING.
- Exact-shell \(C=4/3\). That
  bound stays CLAIMED on one
  input shell.
- Leftover 1. Do not start H1.
- An NSE trajectory. The phase
  scan is illustrative motion.

---

## Lock

Exact: triangle, polarizations,
Leray idle in \(T_k\), cyclic
energy, equal-length cancel,
two-shell gap-cancel,
unequal-length defect.
Numerical: live \(T_c\) on named
triangles; phase flips the sign.
Illustrative: a rotated phase is
not a path.
\(I_3\) prime restrictions sit
as identities, not as a bound.
First missing implication: those
identities do not give a useful
\(K\) in
\(T_c\le\theta\nu\mathcal D_s+K(t)X\).
★ stays killed.
NS not solved.
