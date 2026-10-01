# Gate roadmap — recoverable lineage

**24 September 2026.** Audit of the fullest recoverable
Gate-1–7 record. **Does not overwrite the live board.**
This old Gate-5–7 roadmap is **superseded / obsolete** relative to
the centered route now on this book. Recovering it is lineage,
not a resurrection.

**REOPEN = recompute only.** Do not treat this page as independently
reproducible. Do not invent the missing definitions.

Internal checkpoint. **Not a closure theorem.** Ordinary NS is not
solved. Soft X silent.

Algebra lock of the recorded polynomials:
`scripts/gate5_recovered_algebra.py`,
`results/gate5_recovered_algebra.json`.
That script does **not** search chambers and does **not** define
\(u,m,d\).

Live board (unchanged):
[`CENTERED-EQUATION.md`](CENTERED-EQUATION.md),
[`CENTERED-SPECTRAL-BARYCENTER.md`](CENTERED-SPECTRAL-BARYCENTER.md),
[`CENTERED-DRIFT-K-CANDIDATES.md`](CENTERED-DRIFT-K-CANDIDATES.md),
[`CENTERED-DRIFT-INVENTORY.md`](CENTERED-DRIFT-INVENTORY.md).

The Gate polynomials were **not** present in this tree. They were
not found on the scanned NS remotes. This page is the filing of
the recovered paste.

---

## Standing rule

Do not splice later \(T_c\), \(D_s\), \(E\), \(Y\), Need★, or
\(f_\Lambda\) into these older symbols. Same letters appear later.
Identity of the two systems is **not** established.

Missing from the recovered record, and **not** filled here:

| Object | Status |
|---|---|
| Exact definitions of \(u,m,d\) | **MISSING** |
| Parameter \(c\) and the label \(P_c(z)\) | **MISSING** (recovered polynomial is \(P_0\)) |
| Sign chamber \(+++\) | **MISSING** |
| Six-permutation identity before compression into \(X,Y,Z\) | **MISSING** |
| Derivation of \(P_0\) from Gates 2–3 | **MISSING** |
| Derivation of the two \(z_{\max}\) caps | **MISSING** |
| Origin of \(\sqrt{\Delta_\triangle}/(2\sqrt{r})\) | **MISSING** |
| Exact \(L\), \(A\) in Gate 4 | **MISSING** |
| Gate-1 definitions of \(\mathcal S_\star\), \(c_\alpha\), \(e_\beta\) | **MISSING** |
| Gate-7 definitions of \(T_c\), \(D_c\), \(E\), \(Y\) | **MISSING** |
| Numerical protocol (grid, seed, sample count) | **MISSING** |

What is preserved exactly is boxed below, in the recovered notation.

---

## Gate 5 — strongest recoverable piece

Recorded polynomial

\[
P_0(z)=C_0(u,m)+C_1(u,m)\,z+C_2(u,m)\,z^2,
\qquad z=d^2.
\]

\[
\begin{aligned}
C_0(u,m)
&=
2(m+1)(u+1)\Big[
m^4+2m^3u+4m^3+m^2u^2\\
&\qquad +4m^2u+4m^2
+2mu^3+2mu^2+2u^3+2u^2
\Big],
\end{aligned}
\]

\[
C_1(u,m)
=(u+1)\Big[
-20m^3+4m^2u-32m^2
+6mu^2+24mu
+2u^2+9u+5
\Big],
\]

\[
C_2(u,m)
=
16m^2+2mu+18m-4u^2-10u-2.
\]

\[
D_+(u,m)=4C_0C_2-C_1^2.
\]

So \(D_+\) is **not** \(C_1^2-4C_0C_2\). It is the negative of that
discriminant: \(D_+=-\mathrm{disc}(P_0)\).

\[
z_*=-\frac{C_1}{2C_2},
\qquad
P_0(z_*)
=C_0-\frac{C_1^2}{4C_2}
=\frac{4C_0C_2-C_1^2}{4C_2}
=\frac{D_+}{4C_2}.
\]

Those three quantities are related. They are not the same object.

Recorded danger chamber:

\[
C_2>0,\qquad C_1<0,\qquad D_+<0,\qquad 0<z_*<z_{\max}.
\]

In that chamber the interior minimum is negative, because
\(P_0(z_*)=D_+/(4C_2)\).

Recorded range and cap (derivation of the cap **MISSING**):

\[
u>0,\qquad m>0,
\qquad
z_{\max}
=
\min\left\{
m^2,\,
\frac{(1+u)(3+4m-u)}{4}
\right\}.
\]

The original exact definitions of \(u,m,d\) are **MISSING**.
\(z=d^2\) is the only preserved relation among them.
Do not reverse-engineer \(u,m,d\) from the polynomial.

The label in the record is \(P_0\), not \(P_c\). A reliable earlier
definition of \(c\) is **MISSING**.

---

## Gate 1

Recovered target formulas:

\[
\|\Pi_\beta B(w,w)\|_2
\le
\sqrt{3\beta}\,\|w\|_2^2,
\qquad
\lvert\mathcal S_\star\rvert
\le
\sqrt{3}\,
\frac{\alpha}{\sqrt{\beta}}\,
e_\alpha\sqrt{e_\beta}.
\]

Exact earlier definitions of \(\mathcal S_\star\), \(c_\alpha\),
\(e_\beta\) are **MISSING**. Do not reconstruct them from later
shell notation and present that as the original definition.

---

## Gate 2

Recovered:

\[
f(x)=x(x-\Lambda),
\qquad
\mathcal T_{pqk}
=
\bigl[f(s)-f(t)\bigr]X
+\bigl[f(r)-f(s)\bigr]Y
+\bigl[f(t)-f(r)\bigr]Z.
\]

The full six-permutation identity before compression into
\(X,Y,Z\) is **MISSING**.

---

## Gate 3

Roadmap unambiguous: \(r,t,s\) are **lengths**, not squared lengths.

\[
r=\lvert q\rvert,\qquad t=\lvert p\rvert,\qquad s=\lvert k\rvert.
\]

\[
\Delta_\triangle
=
2(r^2t^2+t^2s^2+s^2r^2)
-(r^4+t^4+s^4).
\]

\[
\Psi_\Lambda(r,t,s)
=
\frac{\sqrt{\Delta_\triangle}}{2\sqrt{r}}
\bigl\lvert(s-t)(s+t-\Lambda)\bigr\rvert.
\]

Formula recovered. Derivation of the factor
\(\sqrt{\Delta_\triangle}/(2\sqrt{r})\) is **MISSING**.
Do not silently reinterpret the \(2\sqrt{r}\) denominator.

This is not enough to reproduce the historical Gate-2/3 → Gate-5
reduction without a new derivation. A new derivation would be a
**reopen**, not this filing.

---

## Gate 4

Recovered target and status only:

\[
L\le A,
\qquad\text{PARTIAL (not yet global)}.
\]

Precise original formulas for \(L\) and \(A\) are **MISSING**.

---

## Gate 7

Recovered target and status:

\[
(T_c)_+\lesssim\sqrt{D_s\,E\,Y},
\qquad\text{NOT YET STARTED}.
\]

The roadmap describes occupancy control / global summation.
Exact Gate-7 definitions of \(T_c\), \(D_c\), \(E\), \(Y\) are
**MISSING**. Later work uses similarly named quantities. Do not
splice those later definitions into this older Gate system.

---

## What this does not do

It does not reopen Gate 5. It does not search the danger chamber.
It does not define \(u,m,d,c,+++\).
It does not overwrite the live centered equation, barycenter,
or \(K\)-candidate sheet.
It does not stamp Need★ from the Gate-1 display.
It does not restore unrestricted \(\star\).

No new estimate is claimed. No continuation criterion.
**NS not solved.**
