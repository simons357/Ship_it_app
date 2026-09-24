# B★ — centered pairing vs \(\sqrt{\mathcal D_s}\)

16 September 2026.
**Does not sit as a universal \(C\).
Not a closed-form kill.
Not a useful \(K\).
Unrestricted ★ stays killed by \(v_n\).
NS not solved.**

Operator inequality, unforced
smooth mean-zero divergence-free
fields on \(\mathbb{T}^3\):

\[
[T_c]_+
\le
C\,X\,\Lambda^{1/2}\,\mathcal D_s^{1/2}.
\tag{B★}
\]

\(T_c=M-\Lambda N\),
\(\Lambda=Y/X\),
\(\mathcal D_s=Z-Y^2/X\),
\(X=\|A^{1/2}u\|_2^2\),
\(Y=\|Au\|_2^2\),
\(Z=\|A^{3/2}u\|_2^2\),
\(N=-\langle B(u,u),Au\rangle\),
\(M=-\langle AB(u,u),Au\rangle\).

Equivalent (sign flip \(u\mapsto -u\),
\(T_c\) odd):

\[
\lvert T_c\rvert^2
\le
C^2\,X\,Y\,\mathcal D_s.
\]

Ratio
\(R_B=\lvert T_c\rvert/(X\Lambda^{1/2}\mathcal D_s^{1/2})\).
A universal \(C\) is
\(\sup R_B<\infty\).

Identity and second pass:
[`BSTAR-PROOF.md`](BSTAR-PROOF.md).
Machine:
`python3 scripts/bstar_attack.py`
and
`python3 scripts/bstar_symmetrize.py`.
Do not overwrite
`stokes_moments.py`.

Path: [`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md).
Centered drift:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
Killed ★:
[`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).

Triangle geometry:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).
First lift:
[`TRIANGLE-LIFT.md`](TRIANGLE-LIFT.md).
Energy-class ladder:
[`ENERGY-K.md`](ENERGY-K.md).
Pairing CS doors:
[`L-DOOR.md`](L-DOOR.md).
Instantaneous \(MN\):
[`MN-CANCEL.md`](MN-CANCEL.md).
First jet:
[`PATHWISE.md`](PATHWISE.md).
Short interval:
[`INTERVAL.md`](INTERVAL.md).
Incoming ledger:
[`CENTERED-LEDGER.md`](CENTERED-LEDGER.md).
Chart reset:
[`RESET.md`](RESET.md).
Relative width:
[`WIDTH.md`](WIDTH.md).
SBP / \(\Phi_e\):
[`SBP.md`](SBP.md).
Do not start leftover 1.
Do not weld \(\star\).
Do not cash B★ as G5.

---

## Verdict

**No universal \(C\) sits on the
evidence of this desk.**

First-pass families (triads,
amplitude, separation, \(v_n\),
shears, HH→L, random) did **not**
send \(R_B\to\infty\). That pass
survived.

Second pass kept \(T_c\) as one
pairing and hit the imag
\(|k|^{-2}\) cutoff family

\[
\widehat u(k)=i\,|k|^{-2}\,e_\perp(k),
\qquad 0<|k|\le K.
\]

On the live FFT evaluator,
\(K=3,4,6,8,10,12,16\):

| \(K\) | \(\Lambda\) | \(R_B\) | \(R_B/\Lambda^{1/4}\) | \(R_L\) |
|---|---|---|---|---|
| 3 | 7.59 | 0.0635 | 0.0382 | 0.498 |
| 4 | 12.1 | 0.0841 | 0.0451 | 0.569 |
| 6 | 24.1 | 0.112 | 0.0507 | 0.718 |
| 8 | 40.4 | 0.135 | 0.0537 | 0.835 |
| 10 | 60.8 | 0.153 | 0.0550 | 0.939 |
| 12 | 85.4 | 0.169 | 0.0555 | 1.036 |
| 16 | 147 | 0.195 | 0.0561 | 1.205 |

\(R_B\) rises with \(K\).
\(R_B/\Lambda^{1/4}\) is saturating
near \(0.056\). \(\Lambda(K)\to\infty\).
That is the death shape for a
uniform \(C\), the same *shape* as
\(v_n\) for ★. A closed-form \(T_c\)
is **not** written. Finite \(0.195\)
is not \(C\). Do not seat B★.

Helical polarization of the same
spectrum has \(T_c\approx 0\)
(Beltrami-like cancel). Imag does
not cancel. Polarization is the
content.

---

## First pass (still true)

| Family | \(R_B\) | Verdict |
|---|---|---|
| Growing-layer \(v_n\) | \(0.0178\to 0.0061\) for \(n=1..8\). \(R_\star\) *grows*. | **Does not kill B★.** Kills ★, not this. \(R_B\sim R_\star^{1/2}\sqrt{E/X}\) and \(E/X\sim n^{-2}\). |
| Amplitude \(u=Au\) | Invariant. Pairing \(\sim A^3\), RHS \(\sim A^3\). | Pass. |
| Shear \((u\cdot\nabla)u=0\) | \(T_c=0\). | \(0\le 0\). Not a test. |
| One shell / ABC | \(\mathcal D_s=0\), \(T_c=0\). | Vacuous. |
| Exact triad, separation | Max \(\approx 0.095\) at \(m=1\); shrinks as \(m\) grows. | Separation *shrinks* \(R_B\). |
| Ascent on four modes | \(0.449\). | Finite local max. Not \(C\). Not the cutoff family. |

---

## If it had sat, it was still not a close

AM-GM on B★:

\[
\lvert T_c\rvert
\le
\theta\nu\mathcal D_s
+\frac{C^2}{4\theta\nu}\,XY.
\]

The remainder coefficient is
\(K\sim Y/\nu\).
Not energy-class.
Not a useful \(K\) for Route B.
Not G5.

The imag cutoff family removes
the hypothesis. Do not AM-GM a
false bound.

---

## Lock

B★ does not sit as a universal
\(C\). Imag \(|k|^{-2}\) cutoff
grows \(R_B\) like \(\Lambda^{1/4}\).
Helix cancels; imag does not.
Identity of the pairing sits
([`BSTAR-PROOF.md`](BSTAR-PROOF.md)).
Even a true B★ would not be a
useful \(K\).
★ stays killed by \(v_n\).
Catalog B open stays 1.
NS not solved.
