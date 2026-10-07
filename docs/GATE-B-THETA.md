# Gate B — Dish #3: global energy sharing and \(\theta\)

7 October 2026.
**Gate B active. Gate A UNRESOLVED / DIAGNOSTIC ONLY.
Not OPEN, not FAILED, not DEAD. Not (17).
NS not solved.**

Helm: do not chase larger \(c\), and do not
manufacture an infinite-sequence note to
finish Gate A. Frozen multiplicity-5 /
smallest-leg convention stands. The
\(\rho\)-floor sequence stays diagnostic.
17 / 32 / 51 results stay valid at their
stated finite scopes.

Parents:
[`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md),
[`SHARED-BUDGET-32-SHAPE-EXTENSION.md`](SHARED-BUDGET-32-SHAPE-EXTENSION.md).
Filed geometry (Library, not invented here):
September 20 scalene note (\(\Delta\),
\(\mathcal T_{abc}\), \(C_{abc}\) majorant);
October 7 51-shape and rebalancing notes.
Code: `scripts/ns_attacks/gate_b_theta.py`.
Packet: [`../packets/GATE-B-THETA-2026-10-07.md`](../packets/GATE-B-THETA-2026-10-07.md).

---

## Status correction

| Object | Language |
|---|---|
| Gate A | **UNRESOLVED / DIAGNOSTIC ONLY** |
| \(L_{z_n}\) growth on the \(z_n=2n^2\) subnet | Diagnostic \(\ell^1\) load. Not a kill. |
| 17 / 32 / 51 finite scopes | Valid as stated |
| General-\(c\) allocation, including \(1/(2c)\), under frozen smallest-leg | **Not a source-of-truth lemma.** Algebra suggests the same face; do not promote. |
| Coercive reason that \(C_{abc}\) is a cost the positive allocation must pay | **Missing.** Equation (16) of the September 20 note is an upper bound. |
| Infinite lattice sequence with proved divergent *allocation cost* | **Missing.** Do not file one just to close Gate A. |

The previous “Outcome B / kill certificate” wording is
withdrawn as a program status. The finite computations
remain on the board as diagnostics.

---

## Dish #3

The Gate A defect both sides keep hitting is

\[
f_x\le\sqrt{E}
\]

spent independently on many interactions. Retain the
low-shell amplitudes and use the actual energy identity

\[
\boxed{\sum_x f_x^2=E.}
\]

Write the all-shape positive majorant schematically

\[
\mathcal T_{\mathrm{sc}}^{+}
\lesssim
\sum_x f_x\,Q_x(f),
\qquad
Q_x
=\sum_{(x,y,z)\ \mathrm{triad}}
C_{xyz}\,f_y f_z.
\]

One Cauchy–Schwarz:

\[
\boxed{
\sum_x f_x Q_x
\le
\sqrt{E}\,
\Bigl(\sum_x Q_x^2\Bigr)^{1/2}.
}
\tag{B-1}
\]

That replaces an \(\ell^1\)-style family cost by an
\(\ell^2\) assembly. The square root can be large.
The target is one number, not regularity:

\[
\boxed{\theta=\text{frequency loss remaining after global energy sharing}.}
\]

---

## From \(Q\) to \(\rho\), diagnostically

The September 20 majorant is

\[
\lvert\mathcal T_{abc}\rvert
\le
C_{abc}\sqrt{E_a E_b E_c},
\qquad
C_{abc}
=\sqrt{3\Delta}
\Bigl(
\frac{\lvert c-b\rvert}{\sqrt a}
+\frac{\lvert c-a\rvert}{\sqrt b}
+\frac{\lvert b-a\rvert}{\sqrt c}
\Bigr).
\]

This is an **upper** bound. It does not by itself
force the positive transfer to pay \(C_{abc}\).

On a \(Y\)-charged middle/high pair,
\(b^2 f_b^2\le Y\) and \(c^2 f_c^2\le Y\), so
\(f_b\le\sqrt Y/b\), \(f_c\le\sqrt Y/c\). Then

\[
Q_x
\le
\frac Yc\Bigl(\sum_b\frac{C_{xbc}^2}{b^2}\Bigr)^{1/2}.
\]

The 51-shape note defines, at the filed low anchor
and \(c=25\),

\[
\rho_a
=\frac1{50}
\sqrt{\sum_{b\in B_a}\frac{C_{a,b}^2}{b^2}}
=\frac1{2c}
\sqrt{\sum_b\frac{C_{a,b}^2}{b^2}}.
\]

The same algebraic face with variable \(c\) is
**diagnostic only** (not a promoted lemma). Under
that face, \(Q_a\le 2\rho_a Y\), and (B-1) becomes

\[
\boxed{
\mathcal T_{\mathrm{sc}}^{+}
\le
2S\,\sqrt{E}\,Y,
\qquad
S=\lVert\rho\rVert_{\ell^2},
\quad
L=\lVert\rho\rVert_{\ell^1}.
}
\tag{B-2}
\]

Gate A spent \(L\sqrt{E}\,Y\). Gate B spends
\(S\sqrt{E}\,Y\). Always

\[
S\le L\le\sqrt{M}\,S.
\]

If many comparable anchors share energy, \(L\) can
grow while \(S\) does not.

Operational definition, on a family with high
shell \(c\sim\Lambda\):

\[
S\sim c^{\theta}
\qquad\bigl(\text{i.e. }\Lambda^{\theta}\bigr).
\]

| \(\theta\) | Meaning |
|---|---|
| \(0\) | No remaining frequency loss after sharing. \(T^{+}\lesssim\sqrt{E}\,Y\). Major investigation — still an upper bound, still not (17). |
| \(\tfrac12\) | Half a derivative left for the structural machinery. |
| substantially \(>0\) | Exact shortfall of Gate B. |

Negative diagnostic \(\hat\theta\) is a gain on that
sample, not a theorem.

---

## Diagnostic numbers (rerun here)

Fixed \(c=25\) anchors \(5,9,13\) (51-shape \(\rho\),
reproduced):

| | \(\rho_5\) | \(\rho_9\) | \(\rho_{13}\) | \(L\) | \(S\) |
|---|---:|---:|---:|---:|---:|
| value | \(0.631855\) | \(0.825307\) | \(1.083316\) | \(2.540\) | \(1.501\) |

Diagnostic subnet \(z_n=2n^2\) (same rectangle as
the old load probe; **not** a kill):

| \(n\) | \(c\) | \(M\) | \(L=\lVert\rho\rVert_1\) | \(S=\lVert\rho\rVert_2\) | \(\hat\theta\) vs previous |
|---:|---:|---:|---:|---:|---:|
| 20 | 800 | 68 | 2.436 | 0.306 | — |
| 40 | 3200 | 227 | 4.213 | 0.289 | \(-0.041\) |
| 80 | 12800 | 794 | 7.622 | 0.281 | \(-0.021\) |
| 160 | 51200 | 2892 | 14.277 | 0.276 | \(-0.011\) |

\(L\) grows like \(n\). \(S\) stays \(O(1)\) and
slightly decreases. Mean \(\hat\theta\approx-0.024\),
consistent with \(\theta=0\) on this sample.

That is the bookkeeping correction: the \(\ell^1\)
load can look dangerous while the one global
Cauchy–Schwarz remainder does not carry a
positive power of \(\Lambda\).

It does **not** prove \(\theta=0\) for the
all-shape sum. It does **not** make the
\(C\)-majorant coercive. It does **not** prove
(17).

---

## What Gate B does not do

- Does not close Gate A.
- Does not supply the missing general-\(c\)
  allocation lemma.
- Does not turn an upper bound into a cost.
- Does not produce an infinite divergent
  allocation-cost sequence.
- Does not recover a half derivative by
  declaration if a later all-shape estimate
  of \(\lVert Q\rVert_2\) reintroduces
  \(\Lambda^{1/2}\).
- Does not assume Serrin / ESS.

If a later estimate of \(\lVert Q\rVert_2\)
without passing through \(\rho\) and the
\(Y\)-charge bounds yields a different
\(\theta\), that number wins. The present
\(\theta=0\) reading is conditional on (B-2).

---

## Lock

Gate A: **UNRESOLVED / DIAGNOSTIC ONLY.**
Gate B: **ACTIVE.** Dish #3 is (B-1)–(B-2).
On the filed diagnostic subnet, \(S=O(1)\)
while \(L\) grows; \(\hat\theta\approx 0\).
\(\theta=0\) is not a theorem for all shapes.
\(C_{abc}\) remains an upper bound.
(17) OPEN as a regularity criterion; not
this page’s claim.
No larger \(c\). No manufactured infinite
kill. NS not solved.
