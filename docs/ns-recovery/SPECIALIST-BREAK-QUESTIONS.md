# Specialist break questions — answered before review

**Date:** 13 September 2026  
**This book.** Answers a specialist can use to try to break the pages.  
**NS is not solved.** Soft X silent.

9D items 5–10 and 14 are also on
[`ATTACK-9D-FULL-SUPPORT-SCORE.md`](ATTACK-9D-FULL-SUPPORT-SCORE.md).

---

## On the kill

### 1. Which identity may fail, and is it by hand for all \(n\)?

The identity a specialist can break is the all-\(n\) transfer formula

\[
T_c(v_n)=3n^5(3n^2+3n+1),
\]

from the planar seed transfers \(3/4,-1,1/4\) at eigenvalues \(1,2,5\),
the vanishing of \(N\), and the vertical cubic count \(3n^2+3n+1\).

This book checked that formula **on the evaluator** for \(n=1,\ldots,8\)
(PR #24’s script also lists \(n=10\)). It was **not** checked by hand
for general \(n\) on this book. The elementary comparison
\(T_c\ge 9n^7\Rightarrow\mathcal R_\star\ge n/165888\) **uses that
formula**. Evaluator growth through \(n=8\) does not need the formula.
Divergence as \(n\to\infty\) does, unless another all-\(n\) lower bound
is written.

### 2. Is \(D_s(v_n)>0\) for every \(n\ge 1\)?

**Yes, for every \(n\ge 1\), by hand, not only on computed rows.**

At \(j=0\) the planar seed occupies three eigenvalues
\(\lambda=n^2,2n^2,5n^2\), each with positive mass
(\(|r|^2\in\{1,2,5\}\)). Distinct eigenvalues with positive mass
force \(D_s>0\). Vacuous single-shell is excluded for every \(n\ge 1\).

### 3. Does a change of normalization stop \(\mathcal R_\star\to\infty\)?

**No**, for the two changes that get named.

- An overall factor of \(n\) on \(U(nx,ny)\) is amplitude. \(\mathcal R_\star(av)=\mathcal R_\star(v)\).
- A global torus-measure factor \(\mu\) (Plancherel \(E=\mu\sum|v_k|^2\) vs \(E=\sum|v_k|^2\)) multiplies \(E,D_s,Y\) by \(\mu\) and \(T_c\) by \(\mu\), so \(\mathcal R_\star\) by \(1/\mu\). That constant is independent of \(n\). It cannot bound the sequence or flip the sign of \((T_c_+)^2\).

A *shape* change (extra \(n\) on some components only) would be a
different family. The locked Fourier law is
\(\widehat v_n(nr_1,nr_2,j)=\frac i2(-r_2,r_1,0)\), no extra \(n\).

### 4. “\(v_n\) is not a Navier–Stokes field.”

**Reply:** This is a counterexample to the proposed **instantaneous**
estimate on the admissible class (mean-zero, divergence-free, finite
Fourier support on \(\mathbb T^3\)). It is **not** a trajectory of
the Navier–Stokes equation and it does **not** construct a singular
solution.

---

## On exact-shell 9D

### 5. Where is the factor \(3\) proved?

**On the PR #24 exact-shell page**, as the weighted count
\(\sum_{|k|^2=\beta}c_k^2\le 3(\sum a_p^2)^2\): two affine planes
meet a sphere in at most two points; \(r=-p\) forces \(\beta=0\);
weighted AM-GM gives off-diagonal \(\le 2\) and diagonal \(\le 1\).

That argument is **not** the Ring Lemma and **not** a Borromean /
band-limited direction bound. Those live in a different book
(\(J/X\), Littlewood–Paley). They prove a different count. Do not
import them.

The factor \(3\) is still **CLAIMED**. Finite audit draws are not
the lattice theorem.

### 6. Hermitian estimate, \(w_p\in\mathbb C^3\), \(w_p\perp p\), no reality

See the 9D score page. Conjugation is used only in the Hermitian
modulus and Cauchy–Schwarz. Reindexing \(p\leftrightarrow q\) does
not use conjugation.

### 7. Division by \(1-\beta/(4\alpha)\)?

**No.** The factor multiplies, in
\(\lvert k_\perp\rvert^2=\beta(1-\beta/(4\alpha))\) and in
\(K\le\frac34(\beta/\alpha)^2(1-\beta/(4\alpha))\).
At \(\beta=4\alpha\) the factor is zero and the bound is \(K=0\).
\(K\) itself is \(\beta\|\Pi_\beta B\|_2^2/(\alpha^2\|w\|_2^4)\).
No hidden division.

### 8. Ordered convolution vs symmetrization, complex coefficients

**Exactly half, for any coefficients.** If
\(S=\sum_{p+q=k}(q\cdot w_p)w_q\), the swap \(p\leftrightarrow q\)
gives \(S=\sum(p\cdot w_q)w_p\), hence
\(S=\frac12\sum\bigl[(q\cdot w_p)w_q+(p\cdot w_q)w_p\bigr]\).
Algebraic. No reality assumption.

### 9. What is \(\Pi_\beta\)?

**Spectral projection onto the exact lattice shell** \(\{|k|^2=\beta\}\),
\(k\in\mathbb Z^3\setminus\{0\}\). Not a dyadic annulus of width 1.
The incidence count is a lattice count.

### 10. Both polarizations at \(p\), independent complex amplitudes?

**Claimed yes.** \(w_p\in\mathbb C^3\) already holds both transverse
components. The estimate is in terms of the Hermitian \(|w_p|\).
That is part of what a specialist must sign. It is not a second
theorem.

---

## On examples

### 11. Public \(K_{1,2}\) for \(w=(\sin y,\sin z,\sin x)\)

Normalized torus, \(\|e^{ik\cdot x}\|_2^2=1\).

\[
\begin{align*}
\widehat w(0,1,0)&=(-\tfrac i2,0,0),&
\widehat w(0,-1,0)&=(\tfrac i2,0,0),\\
\widehat w(0,0,1)&=(0,-\tfrac i2,0),&
\widehat w(0,0,-1)&=(0,\tfrac i2,0),\\
\widehat w(1,0,0)&=(0,0,-\tfrac i2),&
\widehat w(-1,0,0)&=(0,0,\tfrac i2).
\end{align*}
\]

Six modes, each \(|\widehat w|^2=1/4\), so \(E=3/2\). Shell \(\alpha=1\).

At \(k=(1,1,0)\): only \(p=(0,1,0)\), \(q=(1,0,0)\) is live.
\(q\cdot\widehat w_p=-i/2\),
\((q\cdot\widehat w_p)\widehat w_q=(0,0,-1/4)\).
The swapped ordered pair vanishes.
\(\widehat B_k=i(0,0,-1/4)=(0,0,-i/4)\).
Leray is idle (\(k\cdot\widehat B_k=0\)).
\(|\widehat B_k|^2=1/16\).

Twelve lattice points with \(|k|^2=2\) (permutations of \((\pm1,\pm1,0)\)).
Cyclic axes give the same size. So
\(\|\Pi_2 B\|_2^2=12/16=3/4\) and

\[
K_{1,2}(w)=\frac{2\cdot(3/4)}{(3/2)^2}=\frac23.
\]

No script required.

### 12. Any exact-shell field in this repo with \(K>1\)?

**No.** Three-shear is \(2/3\). Aligned 9B max is \(0.641\).
Grow-\(s\) max is \(0.456\). Natural 9D max is \(0.469\).

\(16/9\) is the elementary maximum of the claimed majorant
\(\frac34 x^2(1-x/4)\) at \(x=\beta/\alpha=8/3\), not a fitted
constant and not \(1\). At the three-shear ratio \(x=2\) the
majorant is \(3/2>2/3\). Absence of a sample with \(K>1\) does
not prove \(K\le 1\).

### 13. What a counterexample looks like

One pair \((\alpha,\beta)\) with \(\alpha>0\), \(0<\beta\le 4\alpha\),
and one finite list \(\{(k,w_k):|k|^2=\alpha\}\) with
\(k\cdot w_k=0\), \(w\neq 0\), such that \(K_{\alpha,\beta}(w)>16/9\).
If the field is required real, also \(w_{-k}=\overline{w_k}\).

---

## On scope

### 14. One sentence a true \(4/3\) does not imply

A true \(4/3\) does not repair unrestricted ★, does not give a
continuation criterion, and does not control multi-shell fields.

### 15. Finite superposition, \(C\) depending only on shell count?

**No** such theorem sits here. A bound whose constant depends only
on the number of shells is a **different** statement. It has not
been written. \(v_n\) occupies \(\Theta(n)\) shells and would be
the first test of any such \(C\).

---

## On the machine

### 16. What `verify_pr24_closure_review.py` actually does

It **proves no identity**. Its own docstring says it is not a
proof assistant.

It **computes:** growing-layer \(N\), \(T_c\), \(\mathcal R_\star\)
on `stokes_moments` and `ns_lemma_star_core` for listed \(n\);
match to \(T_c=3n^5(3n^2+3n+1)\); three finite weighted-count
draws (\((4,8),(5,4),(1,2)\), ratio \(\le 3\)); five random
exact-shell \(K\) samples under \(16/9\).

It **reads:** `results/attack9b_grow_s/grow_s.json` and hashes
listed docs and scripts.

Finite checks. The all-\(n\) \(T_c\) identity and the lattice
count remain pending.

### 17. If the script is deleted?

**Yes, the claim still has a human-checkable written argument**
(weighted count + symmetrized kernel + elementary max). The
script is not the proof. Deleting it removes checks, not the
page.

---

## On replacement

### 18. First estimate \(v_n\) does not refute

\(v_n\) is not exact-shell, so it does not refute

\[
\|\Pi_\beta B(w,w)\|_2
\le
\frac43\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2
\qquad(Aw=\alpha w,\;\alpha>0,\;w\neq 0).
\]

That inequality is still **CLAIMED**, not a replacement for ★.

### 19. Invariant along NS?

**No.** Instantaneous bound on the exact-shell subclass.
Not a conserved or monotone quantity along a Navier–Stokes
trajectory.

### 20. Which continuation criterion does it feed?

**None.** Not BKM, not \(\int|Au|_2^2\,dt<\infty\), not
★ \(\Rightarrow\) GR. A true \(4/3\) gives no continuation
criterion.

---

**NS not solved.** Soft X silent.
