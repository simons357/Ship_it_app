# Pairing CS remainder — L-doors

23 September 2026.
**The tight CS door is ★.
The useful loose doors are
\(\|L\|_2\le C\sqrt{EX}\) (dead)
and \(\|L\|_2\le C X\) (not a
universal \(C\)).
Not a close. ★ stays killed.
Catalog B open stays 1.**

Pairing:
[`BSTAR-PROOF.md`](BSTAR-PROOF.md).
Energy-class ladder:
[`ENERGY-K.md`](ENERGY-K.md).
Target:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
Machine: `python3 scripts/l_door.py`.
Does not overwrite `stokes_moments.py`.
This is **not**
[`CS-REMAINDER.md`](CS-REMAINDER.md)
(ABC evaluator).
Do not start leftover 1.
Do not weld \(\star\).
Do not cash B★ as G5.

---

## Three kinds of sentence

**Exact.** The pairing, CS,
AM-GM, and the identity that
the tight projection is ★.

**Numerical.** Printed
\(\|L\|_2\) ratios. Imag is a
reading, not a boxed kill of
the \(X\)-door.

**Illustrative.** None.
Amplitude is exact scaling.

---

## The pairing and the three CS packagings (exact)

\[
T_c
=
\bigl\langle L,\,(A-\Lambda)\omega\bigr\rangle,
\qquad
L=(\omega\cdot\nabla)u-(u\cdot\nabla)\omega.
\]

Cauchy–Schwarz:

\[
\lvert T_c\rvert
\le
\|L\|_2\,\mathcal D_s^{1/2}.
\]

AM-GM, \(\theta<1\):

\[
T_c
\le
\theta\nu\mathcal D_s
+\frac{\|L\|_2^2}{4\theta\nu},
\qquad
K=\frac{\|L\|_2^2}{4\theta\nu X}.
\]

Three ways to bound \(\|L\|_2\).
Only two would be useful.

**Tight.** Project \(L\) onto
\((A-\Lambda)\omega\):
\(\|PL\|_2=\lvert T_c\rvert/\sqrt{\mathcal D_s}\).
Then
\[
K\sim\frac{T_c^2}{\mathcal D_s X}
=\mathcal R_\star E\Lambda.
\]
That is unrestricted ★.
**DEAD.** Locked: the two
formulae match on \(v_n\) and
on the live triangle.

**\(R_L\).** \(\|L\|_2\le C\sqrt{XY}\).
This is the B★ CS door.
AM-GM remainder \(Y/\nu\).
Not useful even if \(C\) sat.
Already scored.

**LE.** \(\|L\|_2\le C\sqrt{EX}\).
Amplitude-legal (\(L\) is
degree 2). Then \(K\sim E\),
and \(\Lambda'\le 2C'E\).
Useful if \(C\) sat.

**LX.** \(\|L\|_2\le C X\).
Amplitude-legal. Then
\(K\sim X/\nu\), so
\((\log\Lambda)'\le C'E/\nu\).
Useful if \(C\) sat.

Locked on the live \(2,2,4\)
triangle: \(R_{LE}\), \(R_{LX}\),
and \(R_L\) stay flat from
amplitude \(0.05\) to \(4\).

---

## LE is dead

\(R_{LE}=\|L\|_2/\sqrt{EX}\):

| Family | \(R_{LE}\) | \(R_{LX}\) | \(R_L\) |
|---|---|---|---|
| \(v_1\) | \(0.543\) | \(0.258\) | \(0.115\) |
| \(v_4\) | \(3.51\) | \(0.430\) | \(0.049\) |
| \(v_8\) | \(9.56\) | \(0.588\) | \(0.034\) |
| \(v_{10}\) | \(13.3\) | \(0.654\) | \(0.030\) |
| imag \(K=4\) | \(4.07\) | \(1.98\) | \(0.569\) |
| imag \(K=6\) | \(8.71\) | \(3.53\) | \(0.718\) |
| imag \(K=8\) | \(15.0\) | \(5.30\) | \(0.835\) |
| sep \(m=1\) | \(0.690\) | \(0.598\) | — |
| sep \(m=8\) | \(4.53\) | \(0.688\) | — |

\(v_n\) kills LE
(\(0.543\to 9.56\)). Imag
climbs. Separated triads
climb too. Finite \(9.56\)
is not \(C\). Do not AM-GM
a false line.

\(R_L\) *falls* on \(v_n\).
That family does not kill
the B★ CS door. Different
box. Do not glue.

---

## LX is not a universal \(C\)

\(R_{LX}=\|L\|_2/X\) grows
on \(v_n\) (\(0.258\to 0.588\)
through \(n=8\), \(0.650\) at
\(n=10\)) and on imag
(\(1.98\to 5.30\)).

That is not a closed-form
kill. It is also not a
seated \(C\). Finite \(0.650\)
is not \(C\). Imag is the
same stall shape as B★,
now on a door that *would*
have been useful.

Do not seat LX. Do not
cash it as G5.

About half of \(\|L\|_2^2\)
leaks off the support of
\(v_n\) (\(\approx 0.576\),
flat in \(n\)). The on-support
piece grows at the same
rate. Leak is not the
escape.

---

## What remains

Energy-class \(K(E)\) is
dead. Tight CS is ★, dead.
LE is dead. LX is not
seated. \(R_L\) is not
useful.

G4 stays OPEN only for a
\(K\) that is not a uniform
function of
\((E,X,\|L\|_2)\) of this
scaling: a named dynamical
cancellation in
\(T_c=M-\Lambda N\) itself,
or a named death of G4
that is not this door.

Tautological \(K\) is still
forbidden.

---

## What this page is not

- A close. Catalog B open
  stays 1.
- A seating of B★ or of LX.
- A restoration of ★.
- The ABC page
  [`CS-REMAINDER.md`](CS-REMAINDER.md).
- A death of Attack-2 \(C_*\).
- Leftover 1. Do not start
  H1.
- An NSE trajectory.

---

## Lock

Tight CS is ★. LE dies on
\(v_n\). LX is not a
universal \(C\). \(R_L\) is
not a useful \(K\).
G4 stays OPEN.
★ stays killed.
NS not solved.
