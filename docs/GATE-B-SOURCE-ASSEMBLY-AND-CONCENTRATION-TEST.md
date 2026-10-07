# Gate B — source assembly and concentration test

7 October 2026.
**First assembly test. Nonnegative \(Q_x\). \(\theta\ge\tfrac12\).
Exact optimal \(\theta\) OPEN. Not (17). NS not solved.**

This is the repo seating of
`Gate-B-Source-Assembly-and-Concentration-Test-2026-10-07.txt`.
Checker: `scripts/ns_attacks/nonnegative_qx_assembly.py`.

Parents: Dish #3 on `cursor/gate-b-theta-62ec` (PR #172). The
\(\rho\)-face reading \(\hat\theta\approx 0\) used \(Y\)-charges
and an inner Cauchy–Schwarz. This page does **not** pass
through \(\rho\).

---

## Object

Low vertex \(x\), nonnegative amplitudes \(f\ge 0\),
September 20 majorant \(C_{abc}\ge 0\):

\[
Q_x(f)
=
\sum_{\substack{(x,y,z)\\x<y<z}}
C_{xyz}\,f_y f_z,
\qquad
C_{abc}
=
\sqrt{3\Delta}
\Bigl(
\frac{\lvert c-b\rvert}{\sqrt a}
+\frac{\lvert c-a\rvert}{\sqrt b}
+\frac{\lvert b-a\rvert}{\sqrt c}
\Bigr).
\]

Energy and enstrophy (\(x=\lvert k\rvert^2\)):

\[
E=\sum_x f_x^2,
\qquad
\Omega=\sum_x x\,f_x^2,
\qquad
\Lambda=\max\{x:f_x>0\}.
\]

Dish #3 pays the low index once:

\[
\mathcal T_{\mathrm{sc}}^{+}
\le
\sqrt{E}\,\lVert Q(f)\rVert_2.
\]

A **uniform power bound** on this explicit \(Q\) is a constant
\(K\), independent of scale, such that for every \(f\ge 0\)

\[
\lVert Q(f)\rVert_2
\le
K\,\Lambda^{\theta}\,\Omega(f).
\]

---

## Lemma (similar triad)

Take one fixed positive lattice triad and dilate lengths by
\(t\) (so radii \(a,b,c\) scale as \(t^2\)). Equal-energy split
\(f_a=f_b=f_c=1/\sqrt3\). Homogeneity of \(C_{abc}\) is degree
three in \(t\):

\[
C(t^2 a,t^2 b,t^2 c)=t^3 C(a,b,c),
\qquad
\Omega\mapsto t^2\Omega.
\]

Hence

\[
\frac{\lVert Q\rVert_2}{\Omega}
\quad\text{scales as}\quad
t=\Lambda^{1/2}.
\]

Checker lock: \(n=4\to 8\to 16\to 32\), mean \(\hat\theta=1/2\)
to machine precision on this family.

**Therefore every uniform power bound on this nonnegative
\(Q_x\) requires \(\theta\ge\tfrac12\).**

The exact optimal value remains **OPEN**. The similar-triad
family saturates \(1/2\); it does not prove that \(1/2\) is
also a uniform upper bound on every overlapping assembly.

---

## What this rules out

The \(\rho\)-face of Dish #3 converted \(\ell^1\) load \(L\)
into \(\ell^2\) assembly \(S\) *after* \(Y\)-charging the high
legs and an inner Cauchy–Schwarz on partners. That can read
\(\hat\theta\approx 0\) on a diagnostic subnet.

It is **not** a gain extracted from the explicit nonnegative
\(Q_x\). Regrouping this majorant cannot cancel the half
derivative forced by concentration on a similar high-frequency
triad.

The \(C_{abc}\) formula remains an **upper** bound on
\(\lvert\mathcal T_{abc}\rvert\). This page does not make it
coercive.

---

## Next test

Keep the signs. Do not replace \(\sum T\) by \(\sum\lvert T\rvert\)
before grouping. See
[`GATE-B-SIGNED-CANCELLATION-TEST.md`](GATE-B-SIGNED-CANCELLATION-TEST.md).

---

## Lock

Nonnegative \(Q_x\): \(\theta\ge\tfrac12\) for any uniform
power bound. Optimal \(\theta\) OPEN.
Cannot obtain the desired gain by regrouping this majorant.
Gate A UNRESOLVED / DIAGNOSTIC ONLY. Gate B active.
(17) OPEN. NS not solved.
