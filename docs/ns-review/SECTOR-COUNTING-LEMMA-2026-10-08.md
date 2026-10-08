# Sector-counting lemma — \(M_N \ge c\,N\log N\)

**Date:** 8 October 2026  
**Status:** **PROVED** at the stated combinatorial scope  
**Not claimed:** SND-U, criterion (17), Clay Statement B, all-shape weighted \(\rho\) sum

---

## Definition (locked)

Fix an integer \(N\ge 1\). Let
\[
\mathcal S_N \;=\; \{\,k\in\mathbb Z^3:\ |k|^2=N\,\}.
\]
A **charging shape** at shell \(N\) is an unordered pair \(\{a,b\}\) of positive integers for which there exist \(k\in\mathcal S_N\) and \(p\in\mathbb Z^3\) with
\[
1\le |p|^2\le N,
\qquad
q:=-(k+p)\ne 0,
\qquad
a=\min\bigl(|p|^2,|q|^2\bigr),\quad
b=\max\bigl(|p|^2,|q|^2\bigr),
\]
and the three legs are **non-collinear**:
\[
(x-y-z)^2\ne 4yz
\quad\text{for every permutation \((x,y,z)\) of \((a,b,N)\).}
\]
(Equivalently: the lattice triangle has positive area.)

Define
\[
M_N \;:=\; \#\{\text{charging shapes at shell \(N\)}\}.
\]

This is the same convention used by the all-shape charge-count kill probe
(`scripts/ns_attacks/all_shape_charge_count_kill.py`), which matched the
independent desk table \(266/1254/5185/58550\) at shells \(25/50/101/401\).

---

## Lemma

**Lemma (sector / shape counting).**  
There exist absolute constants \(c>0\) and \(N_0\) such that for every perfect square \(N=n^2\) with \(n\ge N_0\),
\[
\boxed{M_N \;\ge\; c\, N\log N.}
\]
(Here \(\log\) is the natural logarithm; any fixed base only rescales \(c\).)

---

## Proof

Write \(N=n^2\) with \(n\ge 3\), and set
\[
L \;:=\; \lfloor\log_2 n\rfloor,
\qquad
Y_0 \;:=\; L^2+1.
\]
Assume \(n\ge N_0\) large enough that \(Y_0\le n/4\) (so the ranges below are nonempty) and \(L\ge 1\).

### Explicit family

For integers
\[
x\in\bigl\{1,\ldots,\lfloor n/2\rfloor\bigr\},
\qquad
y\in\bigl\{Y_0,\ldots,\lfloor n/2\rfloor\bigr\},
\qquad
s\in\{1,\ldots,L\},
\]
define
\[
k=(n,0,0),\qquad
p=(-x,\,y,\,s),\qquad
q=(x-n,\,-y,\,-s).
\]
Then \(k+p+q=0\), \(|k|^2=n^2=N\), and
\[
|p|^2=x^2+y^2+s^2\le \Bigl(\frac n2\Bigr)^2+\Bigl(\frac n2\Bigr)^2+L^2
\le \frac{N}{2}+(\log_2 n)^2\le N
\]
for all \(n\ge N_0\). Likewise \(|q|^2=(n-x)^2+y^2+s^2\ge 1\). Set
\[
A:=|p|^2,\qquad B:=|q|^2,\qquad
\sigma(x,y,s):=\bigl(\min(A,B),\,\max(A,B)\bigr).
\]

### Non-collinearity

The three squared radii are \(A\), \(B\), \(N\). Collinearity would require
\((A-B-N)^2=4BN\) or a cyclic permutation. Direct expansion using
\(A-B=x^2-(n-x)^2=2nx-n^2\) and \(y\ge 1\), \(s\ge 1\) shows the
planar parallelogram spanned by \(p\) and \(q\) has nonzero area
(\(p\times q\) has a nonzero \(z\)-component proportional to \(ny\neq 0\)).
Hence every triple is non-collinear, and each \(\sigma(x,y,s)\) is a charging shape.

### Injectivity

Suppose \(\sigma(x,y,s)=\sigma(x',y',s')\). Then
\[
A-B=A'-B'
\quad\Longrightarrow\quad
2nx-n^2=2nx'-n^2
\quad\Longrightarrow\quad
x=x'.
\]
Consequently
\[
y^2+s^2=y'^2+s'^2=:T.
\]
If \(s\neq s'\), then
\[
\bigl|y^2-y'^2\bigr|=\bigl|s'^2-s^2\bigr|\le L^2.
\]
Writing \(y>y'\) without loss of generality,
\[
(y-y')(y+y')\le L^2.
\]
Since \(y-y'\ge 1\), one gets \(y+y'\le L^2\), hence \(y\le L^2\). But the
construction enforces \(y\ge Y_0=L^2+1\), a contradiction. Therefore \(s=s'\),
and then \(y=y'\).

So \(\sigma\) is injective on the index set.

### Counting

The number of admissible indices is
\[
\#I
\;=\;
L\cdot\Bigl(\lfloor n/2\rfloor-Y_0+1\Bigr)\cdot\lfloor n/2\rfloor.
\]
For \(n\ge N_0\) one has \(\lfloor n/2\rfloor-Y_0+1\ge n/4\), hence
\[
\#I \;\ge\; L\cdot\frac n4\cdot\frac n2
\;=\; \frac14\, n^2\, L
\;=\; \frac14\, N\,\lfloor\log_2 n\rfloor.
\]
Since \(\log N=2\log n\) and \(\lfloor\log_2 n\rfloor\ge (\log n)/\log 2-1\),
there is an absolute \(c>0\) with
\[
M_N \;\ge\; \#I \;\ge\; c\, N\log N.
\]
This completes the proof. \(\square\)

---

## Scope and use

| Claim | Status |
|---|---|
| \(M_N\ge c\,N\log N\) for large square shells | **PROVED** |
| Full enumeration \(M_N\sim\Theta(N^2)\) (desk \(\sim 0.4\,N^2\)) | **NUMERICAL / stronger**; not needed here |
| All-shape weighted \(\rho\) sum fails | **Expected**; needs audit per-shape \(\rho\) |
| SND-U / Clay / criterion (17) | **NOT claimed** |

**Why this matters for the shared-budget route.**  
High-pass gain on shell \(N\) is only \(N^{-1/2}\). A lower bound \(M_N\ge c\,N\log N\) already forces any all-shape rule whose average per-shape constant stays \(\gtrsim N^{-1/2-\varepsilon}\) (or even decays only like \(1/\log N\)) to blow the budget. The empirically larger \(\sim N^2\) count only strengthens the obstruction. This is a kill-test ingredient, not a regularity theorem.

**What it does not do.**  
It does not produce a summable charge rule, does not close Task 3, and does not upgrade SND-C to SND-U.

---

## Verification

Script: `scripts/ns_attacks/sector_counting_lemma_verify.py`  
JSON: `results/shared_budget/sector_counting_lemma_verify.json`

Checks: injectivity of \(\sigma\), non-collinearity spot checks, and the explicit lower bound versus \(N\log N\) for square shells.

---

*NS not solved. Criterion (17) open. Clay open. SND-U open.*
