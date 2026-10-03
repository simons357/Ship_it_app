# L3-5 exact shear obstruction

3 October 2026.
**Exact counterfamily to an energy-only
bound for (L3-5). Does not refute the
fixed-datum statement. (L3-5) remains
OPEN. Prefer the signed scalene budget.
NS not solved.**

Parent:
[`L3-BUDGET-GATES.md`](L3-BUDGET-GATES.md)
(PR #153).
Packet:
[`packets/L3-5-Exact-Shear-Obstruction-2026-10-03.md`](../packets/L3-5-Exact-Shear-Obstruction-2026-10-03.md).

Unaugmented NS on
\(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\).
Same convention as the L3 budget
gates and the 20 September audit:
\(A=-P\Delta\),
\(X=\lvert A^{1/2}u\rvert_2^2\),
\(Y=\lvert Au\rvert_2^2\),
\(\Lambda=Y/X\),
\(h_{K,N}=P_{\lvert k\rvert>K}u_N\),
and the high-mode \(L^3\) budget
\(\mathcal S^{(3)}_{K,N}(T)\) of (L3-3).
No \(Q_1\). No \(\Phi\). No SND.
No Theorem H. No RH.
Unrestricted \(\star\) stays **KILLED**.
Lemma A and the first-variation
sign gate stay unaltered.

This page files an exact shear
counterfamily. It obstructs a reverse
comparison of \(\mathcal S^{(3)}\)
against an energy-only remainder.
It does **not** kill the fixed-datum
statement (L3-5).

---

## Status

| Claim | Score |
|---|---|
| Exact shear family: \((u\cdot\nabla)u=0\), viscous decay only | **PROVED** (construction) |
| \(\mathcal S^{(3)}_{K,N}(T)\) can diverge at fixed \(E\), \(\nu\), \(K\), \(T\) as the datum varies | **PROVED** (this family) |
| Reverse energy-only comparison for \(\mathcal S^{(3)}\) | **IMPOSSIBLE** |
| One-way estimate (L3-4) | **VALID** (unchanged) |
| Fixed-datum (L3-5): \(K=K(u_0,\nu)\) for one smooth datum | **OPEN** — **not refuted** |
| Clay / NS regularity | **NOT CLAIMED** |

---

## Family

Using the conventions of PR #153,
define

\[
g(y,t)
=
\frac{a}{\sqrt{L}}
\sum_{r=m}^{m+L-1}
e^{-\nu r^{2} t}\,e^{i r y},
\qquad
u=(\operatorname{Re} g,\,0,\,\operatorname{Im} g),
\qquad
1\le L\le m.
\]

These fields satisfy exactly

\[
(u\cdot\nabla)u=0,
\qquad
E(0)=a^{2},
\qquad
\int_0^T X\,dt\le\frac{a^{2}}{2\nu},
\qquad
\Lambda\ge m^{2}.
\]

They evolve solely by viscosity, so
they solve the full equations and
every Galerkin truncation containing
their support.

---

## Lower bound

For \(m>K\), throughout
\(0\le t\le(16\nu m^{2})^{-1}\),

\[
\lVert h_{K,N}(t)\rVert_3
\ge
d\,a\,L^{1/6},
\qquad
d=\frac{e^{-1/4}}{2(2\pi)^{1/3}}.
\]

Consequently, for any fixed \(T>0\)
and sufficiently large \(m\),

\[
\boxed{
\mathcal S^{(3)}_{K,N}(T)
\ge
\frac{\bigl[d\,a\,L^{1/6}-c\nu\bigr]_+}{16\nu}.
}
\]

Taking \(L=m\to\infty\) makes this
diverge at fixed energy, viscosity,
\(K\), and time horizon.

---

## Stress tests

| Test | Exact outcome |
|---|---|
| Growing layer, \(L=m\) | Budget diverges |
| Relative near-shell, \(m=j^{2}\), \(L=j\) | Budget diverges while relative shell width \(\to 0\) |
| Single shell, \(L=1\) | Integrated budget stays bounded independently of frequency |
| Nonlinear transfer | Every interaction vanishes; original signed scalene budget is exactly zero |

---

## What this kills, and what it does not

**Killed.** An energy-only reverse
bound that would control
\(\mathcal S^{(3)}_{K,N}(T)\) from
\(E\), \(\nu\), \(K\), and \(T\) alone,
uniformly in the initial datum.
The \(L^3\) replacement can assign
arbitrarily large cost to flows that
produce no nonlinear growth.

**Not killed.** The one-way estimate
(L3-4),
\(\mathcal S\le C_S\,\mathcal S^{(3)}+C(\nu,E_0)\),
remains valid. A reverse comparison
with an energy-only remainder is
impossible; the forward comparison is
not touched.

**Not killed.** The fixed-datum
statement (L3-5):

\[
\forall u_0\in C^\infty_{\mathrm{div}},\
\forall\nu>0,\quad
\exists K=K(u_0,\nu)<\infty:\quad
\forall T<\infty,\quad
\sup_N\mathcal S^{(3)}_{K,N}(T)<\infty.
\]

This family varies the initial datum.
(L3-5) permits \(K\) and its bound to
depend on one fixed smooth datum; that
statement remains **OPEN**. Bounds that
use detailed initial spectral
information are not excluded.

---

## Priority consequence

Concrete reason to prioritize the
original signed scalene budget: it
retains the cancellation that the
\(L^3\) replacement discards. On this
family the signed scalene budget is
exactly zero, while
\(\mathcal S^{(3)}\) can be driven
arbitrarily large.

Attack (L3-5) at fixed datum, or
return to the signed geometry. Do not
treat an energy-only reverse bound on
\(\mathcal S^{(3)}\) as available.

---

## Lock

Exact shear obstruction to an
energy-only reverse bound for
\(\mathcal S^{(3)}\): **PROVED**.
Fixed-datum (L3-5): **OPEN**,
**not refuted**.
(L3-4) one-way: **VALID**.
Energy-only reverse comparison:
**IMPOSSIBLE**.
Prefer signed scalene budget.
No novelty claim beyond the
construction.
No close.
Lemma A unaltered.
Sign gate unaltered.
NS not solved.
