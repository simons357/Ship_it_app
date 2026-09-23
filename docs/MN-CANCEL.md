# Instantaneous \(M-\Lambda N\) cancellation

23 September 2026.
**On \(v_n\), \(N=0\) so \(T_c=M\).
\(R_{mn}=1\). \(R_{ab}=1\).
No uniform instantaneous \(\theta<1\).
Signed vertices stay \(\sim 0.31\),
not a useful \(K\).
Not a close. ★ stays killed.
Catalog B open stays 1.**

Pairing:
[`BSTAR-PROOF.md`](BSTAR-PROOF.md).
Energy-class:
[`ENERGY-K.md`](ENERGY-K.md).
L-doors:
[`L-DOOR.md`](L-DOOR.md).
Target:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
First jet:
[`PATHWISE.md`](PATHWISE.md).
Short interval:
[`INTERVAL.md`](INTERVAL.md).
Machine: `python3 scripts/mn_cancel.py`.
Does not overwrite `stokes_moments.py`.
Do not start leftover 1.
Do not weld \(\star\).
Do not cash B★ as G5.
Do not split \(M\) and \(\Lambda N\)
by Sobolev as the first move.

---

## Three kinds of sentence

**Exact.** \(T_c=M-\Lambda N\),
the \(T_k\) rebuild, \(N=0\) on
\(v_n\), and \(R_{mn}=R_{ab}=1\)
on that family.

**Numerical.** Printed
\(R_{\mathrm{sign}}\) and imag /
sep \(R_{mn}\). Finite is not
\(C\) and not a remainder.

**Illustrative.** None.
Amplitude is exact scaling.

---

## The identities (exact)

\[
N=\sum_k\lambda_k T_k,\qquad
M=\sum_k\lambda_k^2 T_k,\qquad
T_c=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

Locked: the \(T_k\) rebuild
matches `probe()` on the live
triangle and on \(v_n\).

On the growing-layer family,
already locked,

\[
N=0,\qquad
T_c=M=3n^5(3n^2+3n+1).
\]

Two snapshot ratios:

\[
R_{mn}
=\frac{\lvert T_c\rvert}{\lvert M\rvert+\Lambda\lvert N\rvert}
\le 1,
\]

\[
R_{ab}
=\frac{\lvert T_c\rvert}{\lvert T_{>}\rvert+\lvert T_{<}\rvert}
\le 1,
\]

where \(T_{>}\) (resp. \(T_{<}\))
is the sum of
\(\lambda(\lambda-\Lambda)T_k\)
over \(\lambda>\Lambda\)
(resp. \(\lambda<\Lambda\)).

A uniform \(\theta<1\) in either
ratio would be instantaneous
cancellation. It would still
leave \(\lvert M\rvert+\Lambda\lvert N\rvert\)
to bound. That is the same
cubic problem.

---

## Instantaneous \(MN\) is dead

\(R_{mn}\) on \(v_n\) is \(1\)
by the closed form \(N=0\).
No \(\theta<1\).

| Family | \(R_{mn}\) | \(R_{ab}\) | \(R_{\mathrm{sign}}\) |
|---|---|---|---|
| \(v_1\) | \(1\) | \(1\) | \(0.273\) |
| \(v_4\) | \(1\) | \(1\) | \(0.303\) |
| \(v_8\) | \(1\) | \(1\) | \(0.308\) |
| \(v_{10}\) | \(1\) | \(1\) | \(0.309\) |
| live \(2,2,4\) | \(1/3\) | \(1\) | \(0.568\) |
| sep \(m=1\) | \(0.333\) | \(1\) | \(1\) |
| sep \(m=8\) | \(0.111\) | \(1\) | \(1\) |
| imag \(K=4\) | \(0.377\) | — | — |
| imag \(K=6\) | \(0.386\) | — | — |
| imag \(K=8\) | \(0.391\) | — | — |

Locked on the live triangle:
\(R_{mn}\), \(R_{ab}\), and
\(R_{\mathrm{sign}}\) stay flat
from amplitude \(0.05\) to \(4\).

Imag has partial \(MN\) cancel
and climbs. That is not a
universal \(\theta\). Separated
triads *lower* \(R_{mn}\).
Different family. That family
did **not** kill ★. Different
box. Do not glue.

---

## Above / below \(\Lambda\) is dead

On \(v_n\), \(T_{>}\) and
\(T_{<}\) have the **same
sign**. \(R_{ab}=1\).
The center does not cancel
the two sides against each
other on the family that
already killed ★.

Same on the live triangle
and on separated triads.
The split that keeps
centering still adds.

---

## Signed vertices are not a useful \(K\)

\[
R_{\mathrm{sign}}
=\frac{\lvert T_c\rvert}{\sum_k\lvert\lambda_k(\lambda_k-\Lambda)T_k\rvert}.
\]

On \(v_n\) this is
\(0.273\to 0.309\). Vertices
do cancel in sign. The
ratio saturates. A finite
\(0.31\) is not a remainder:

\[
\lvert T_c\rvert
\le
R_{\mathrm{sign}}
\sum_k\lvert\lambda_k(\lambda_k-\Lambda)T_k\rvert
\]

still needs a bound on the
absolute vertex sum. That
is cheap CS with the signs
stripped. It does not give
a useful \(K\).

Separated triads have
\(R_{\mathrm{sign}}=1\):
no vertex-sign cancel, and
they *do* cancel in \(M\)
versus \(\Lambda N\).
Opposite of \(v_n\).
Do not glue the two ratios.

---

## What remains

Energy-class \(K(E)\) is
dead. Tight CS is ★, dead.
LE is dead. LX is not
seated. Instantaneous
\(MN\) and above/below
\(\Lambda\) are dead as
uniform \(\theta<1\).
Signed vertices are not
a useful \(K\).

G4 stays OPEN only for a
\(K\) that is not a snapshot
function of
\((E,X,\|L\|_2,M,N,T_k)\)
of this scaling. The
\(t=0\) jet is scored
separately:
[`PATHWISE.md`](PATHWISE.md).
The short interval is
scored separately:
[`INTERVAL.md`](INTERVAL.md).

Snapshots cannot seat that
pathwise sentence. They
killed the instantaneous
one. \(v_n\) is an
admissible class, not a
trajectory.

Tautological \(K\) is still
forbidden.

---

## What this page is not

- A close. Catalog B open
  stays 1.
- A seating of B★ or of LX.
- A restoration of ★.
- A Sobolev split of
  \(M\) and \(\Lambda N\).
- A death of Attack-2 \(C_*\).
- Leftover 1. Do not start
  H1.
- An NSE trajectory.

---

## Lock

On \(v_n\), \(N=0\),
\(T_c=M\), \(R_{mn}=1\),
\(R_{ab}=1\).
Instantaneous \(MN\)
cancellation is dead.
Above/below \(\Lambda\)
is dead. Signed vertices
are not a useful \(K\).
G4 stays OPEN.
★ stays killed.
NS not solved.
