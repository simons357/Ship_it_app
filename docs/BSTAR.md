# B★ — centered pairing vs \(\sqrt{\mathcal D_s}\)

16 September 2026.
**Attacked. Not seated. Not a close.
Unrestricted ★ stays killed.
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

Machine:
`python3 scripts/bstar_attack.py`.
Do not overwrite
`stokes_moments.py`.

Path: [`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md).
Centered drift:
[`CENTERED-DRIFT.md`](CENTERED-DRIFT.md).
Killed ★:
[`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).

Do not start leftover 1.
Do not weld \(\star\).

---

## First: try to kill it

Families already on the desk,
plus the requested ones.
Keep \(T_c\) as one pairing.
Do not split \(M\) and \(\Lambda N\)
as the first move.

| Family | \(R_B\) | Verdict |
|---|---|---|
| Growing-layer \(v_n\) | \(0.0178\to 0.0061\) for \(n=1..8\). \(R_\star\) *grows*. | **Does not kill B★.** Kills ★, not this. \(R_B\sim R_\star^{1/2}\sqrt{E/X}\) and \(E/X\sim n^{-2}\). |
| Amplitude \(u=Au\) | Invariant. Pairing \(\sim A^3\), RHS \(\sim A^3\). | Pass. |
| Shear \((u\cdot\nabla)u=0\) | \(T_c=0\). | \(0\le 0\). Not a test. |
| One shell / ABC | \(\mathcal D_s=0\), \(T_c=0\). | Vacuous. |
| Exact triad \((1,0,0),(0,m,0),(1,m,0)\) | Max \(R_B\approx 0.095\) at \(m=1\). At \(m=16\): \(R_B\approx 6\cdot 10^{-4}\). | Separation *shrinks* \(R_B\). |
| Two keys, no closer | \(T_c=0\). | No triad. |
| Dilated high triad | Falls with scale. | Pass. |
| HH→L one-key (aligned) | \(T_c=0\) (gap-cancel). | Not a test. |
| HH→L fan / energy split | \(R_B\le 0.004\). | Finite. |
| Random many-mode, \(k_{\max}\le 5\) | \(R_B\le 0.012\). | Finite. |

Largest printed \(R_B\) on this
hunt: \(\approx 0.095\), local
three-wave, not a high-frequency
monster. Finite is not \(C\).
Finite is not a kill.

Cauchy–Schwarz door
\(\lvert T_c\rvert\le\|A^{1/2}B\|_2\,\mathcal D_s^{1/2}\)
stayed
\(\|A^{1/2}B\|_2/\sqrt{XY}\le 0.86\)
on the same list. That is a
sufficient majorant, not a proof
of a uniform \(C\).

---

## Why \(v_n\) cannot kill this

On the unit torus, mean-zero,
\(X\ge E\), so
\(R_B=\sqrt{R_\star}\,\sqrt{E/X}\le\sqrt{R_\star}\).
\(v_n\) makes \(R_\star\sim n\) and
\(E/X\sim n^{-2}\), hence
\(R_B\to 0\).
B★ is a *different box* from
unrestricted ★. Do not restore
\(\sup R_\star<\infty\).

---

## If it sits, it is still not a close

AM-GM on B★:

\[
\lvert T_c\rvert
\le
\theta\nu\mathcal D_s
+\frac{C^2}{4\theta\nu}\,X^2\Lambda
=
\theta\nu\mathcal D_s
+\frac{C^2}{4\theta\nu}\,XY.
\]

The remainder coefficient is
\(K\sim Y/\nu\), or
\(K_Y\sim X/\nu\).
Neither is energy-class.
This is **not** a useful \(K\)
for Route B continuation.
Gronwall still wants an
\(H^1\) or \(H^2\) ceiling.

B★, if true, is a geometric
bound with a \(\sqrt{\mathcal D_s}\)
factor. It is not leftover 1.
It does not seat G5.

---

## Proof status

**OPEN.** Survived the named
families. Not proved.

Crude Sobolev / Kato–Ponce does
**not** seat it:
\(\|u\cdot\nabla u\|_{H^1}\) wants
\(\|\nabla u\|_\infty\), and
\(H^2(\mathbb{T}^3)\not\subset W^{1,\infty}\).
That stall is not a kill.

A proof has to keep the centered
multiplier \(A-\Lambda I\), use
full triad symmetrization and
incompressibility, and not
estimate \(M\) and \(\Lambda N\)
separately unless forced.
That page is not written.

Death if a later admissible
field has \(R_B\to\infty\).
Record the field and stop
patching.

---

## Lock

B★ attacked. Not seated.
\(v_n\) does not kill it.
Amplitude matches.
Separation shrinks \(R_B\).
Even a true B★ is not a
useful \(K\).
★ stays killed.
Catalog B open stays 1.
NS not solved.
