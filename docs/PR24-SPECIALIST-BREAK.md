# PR 24 — specialist break questions, answered

13 September 2026.
Answers written before anyone else
reads the two pages.
**This is not a close. Ordinary NS
is not solved. Soft X silent.**

Bound: [`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md).
Kill: [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).
Floor: [`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).

Questions 5–10 and 14 also sit on
the bound page. Sweeps do not replace
those lines.

---

## On the kill

**1. Which identity may fail, and
was it checked for general \(n\),
not only \(n\le 8\)?**

The identity a specialist can still
break is
\[
T_c(v_n)=3n^5(3n^2+3n+1)
\qquad(n\ge 1).
\]
The cubic factor
\(\langle D_n^3\rangle=3n^2+3n+1\)
is a three-line sum, checked by hand
for general \(n\), and by brute count
for \(n=1,\dots,20\).
The product \(3n^5\langle D_n^3\rangle\)
(seed transfer times the vertical
cubic) is the pending kernel.
Live evaluators match that product
on \(n=1,\dots,10\), not merely
\(n\le 8\). Matching ten integers is
not a proof assistant.

**2. Is \(\mathcal D_s(v_n)>0\) for
every \(n\ge 1\), or only on computed
rows?**

For every n \(\ge 1\). Modes with
\(r=(1,0)\), \(j=0\) sit on
\(\lambda=n^2\). Modes with
\(r=(1,1)\), \(j=0\) sit on
\(\lambda=2n^2\). Two eigenvalues
carry mass. Spectral variance is
positive. The computed rows are a
check, not the reason.

**3. Does a normalization change the
sign of \(\mathcal R_\star\to\infty\)?**

No. Amplitude: \(T_c\sim a^3\),
\(\mathcal D_s,E,Y\sim a^2\), so
\(\mathcal R_\star\) is invariant.
A global Plancherel constant \(c\)
scales \(T_c^2/(\mathcal D_s E Y)\)
by \(1/c\); the sequence still
diverges. The factor \(n\) in
\(U(nx,ny)\) is part of the family,
not a later normalization. Dropping
it writes a different field.

**4. If someone says \(v_n\) is
“not a Navier–Stokes field,” what
is the exact reply?**

Instantaneous admissible class, not
a trajectory. The boxed claim was an
estimate on real, mean-zero,
divergence-free fields with
\(\mathcal D_s>0\). \(v_n\) is in
that class. It is not a solution of
NSE, and it is not a blowup.

---

## On exact-shell 9D

**5. Where is the factor \(3\) proved?**

On the bound page: claimed two-plane
incidence plus AM-GM. Not Ring.
Not Borromean. Those leftovers
are REPAIR and a different count.
Do not glue.

**6. Hermitian estimate, \(w_p\in\mathbb{C}^3\),
\(w_p\perp p\), no reality.**

\[
\lvert k\cdot w_p\rvert
=
\bigl\lvert\langle k_\perp,\overline{w_p}\rangle\bigr\rvert
\le
\lvert k_\perp\rvert\,\lvert w_p\rvert.
\]
Conjugation is in
\(\langle u,v\rangle=\sum u_j\overline{v}_j\),
used once, on \(w_p\).
\(k_\perp\) is real.
Equality iff \(w_p=\lambda k_\perp\),
\(\lambda\in\mathbb{C}\).

**7. Does the argument divide by
\(1-\beta/(4\alpha)\), including in \(K\)?**

No. The one-mode bound is a product.
\(K=\beta\|\Pi_\beta B\|_2^2/(\alpha^2\|w\|_2^4)\)
has no such factor. As
\(\beta\to 4\alpha^-\) the product
vanishes. Not a singular limit.

**8. Is the ordered convolution exactly
half the symmetrization for complex
coefficients?**

No. Live \(B\) is
\(\widehat B_k=i P_k\sum_{p+q=k}(q\cdot w_p)w_q\),
both orders, no extra \(1/2\).
That is the definition for real and
for complex. Half-symmetrization is
a reconstruction. Do not cash it.

**9. What is \(\Pi_\beta\)?**

Spectral projection onto the lattice
shell \(\lvert k\rvert^2=\beta\)
exactly, \(k\in\mathbb{Z}^3\).
Not a dyadic shell of width 1.
A continuum annulus is a different
count.

**10. Both polarizations at \(p\),
independent complex amplitudes?**

The claimed bound is for that class.
Each \(w_p\) is any vector in the
complex plane \(p^\perp\).
Cauchy–Schwarz uses \(\lvert w_p\rvert\).
Occupying both transverse directions
does not weaken the one-mode line.
The later factor \(3/4\) is still
CLAIMED for that generality.

---

## On examples

**11. \(K_{1,2}\) from public modes.**

Input, shell \(\alpha=1\):

\[
\begin{aligned}
\widehat w(0,1,0)&=(-i/2,0,0),&
\widehat w(0,-1,0)&=(i/2,0,0),\\
\widehat w(0,0,1)&=(0,-i/2,0),&
\widehat w(0,0,-1)&=(0,i/2,0),\\
\widehat w(1,0,0)&=(0,0,-i/2),&
\widehat w(-1,0,0)&=(0,0,i/2).
\end{aligned}
\]

\(E=6\cdot(1/4)=3/2\).
Outputs on \(\beta=2\): the twelve
keys that are permutations of
\((\pm 1,\pm 1,0)\).
At \(k=(1,1,0)\) the only live
ordered pair is \(p=(0,1,0)\),
\(q=(1,0,0)\):
\(i(\widehat w_p\cdot q)\widehat w_q=(0,0,-i/4)\).
Leray is idle. \(\lvert\widehat B_k\rvert^2=1/16\).
Cyclic axes give the same size on
every output of shell 2. Hence
\(\|\Pi_2 B\|_2^2=12/16=3/4\) and
\[
K_{1,2}
=
\frac{2\cdot(3/4)}{1\cdot(3/2)^2}
=
\frac{2}{3}.
\]
No script required.

**12. Any exact-shell field in the
repo with \(K>1\)?**

No. Seated values:
three-shear \(2/3\approx 0.667\),
aligned 9B \(\approx 0.641\),
grow-\(s\) \(\approx 0.456\).
All sit under \(1\) and under
\(16/9\approx 1.778\).
The ceiling is \(16/9\) because that
is the max of the claimed envelope
\((3/4)x^2(1-x/4)\) at \(x=8/3\),
not because a sample approached it.
Do not replace \(16/9\) by \(1\).
A finite max is not the bound.

**13. What does a counterexample
look like?**

One pair \((\alpha,\beta)\) with
\(0<\beta\le 4\alpha\) and one finite
conjugate-closed, divergence-free
list \(\{w_p:\lvert p\rvert^2=\alpha\}\)
such that \(K_{\alpha,\beta}(w)>16/9\).
That kills the constant.
A sequence with \(K\to\infty\) kills
\(\sup K<\infty\). Those are different
statements. If \(16/9\) is false, the
\(v_n\) kill of unrestricted ★ still
stands.

---

## On scope

**14. One sentence a true \(4/3\)
does not imply.**

A true \(4/3\) does not repair
unrestricted ★, does not give a
continuation criterion, and does
not control a multi-shell field.

**15. Finite superposition of
exact-shell fields, \(C\) depending
only on the number of shells?**

No. That is a different theorem.
This page does not claim it.
\(v_n\) is already a growing
multi-shell field on which
\(\mathcal R_\star\) is unbounded.

---

## On the machine

**16. What does
`verify_pr24_closure_review.py`
actually check, and what does it
only read?**

Checks live: growing-layer moments
against the closed-form \(T_c\) and
against a saved \(n=1..4\) table;
\(N=0\); \(\mathcal D_s>0\);
\(\mathcal R_\star\) increasing on
the listed \(n\); match to the
standalone core; random exact-shell
\(K\) on five pairs; random
weighted-count ratios on three
pairs.
Reads only: grow-\(s\) JSON and
source hashes.
It does not prove \(T_c\) for all
\(n\). It does not prove two-plane
incidence. It does not prove
\(16/9\).

**17. If the script is deleted, does
the claim still have a
human-checkable proof?**

The kill has a human-checkable
elementary lower bound
\(\mathcal R_\star\ge n/165888\)
once \(T_c=3n^5(3n^2+3n+1)\) is
granted, and \(\langle D_n^3\rangle\)
is a three-line sum.
The exact-shell \(16/9\) is a
human-checkable **claim**, not a
certified proof.
The floor \(K_{1,2}=2/3\) is
human-checkable by hand (Q11).
Deleting the script deletes the
internal check, not those writes.

---

## On replacement

**18. First estimate \(v_n\) does
not refute, as a displayed
inequality?**

None sits. Leftover 4 is named
(replacement energy-budget closure)
and is **OPEN**. DA has not written
the inequality. Need★ is MISSING
and cannot repair the dead box.
The first displayed **claim** that
\(v_n\) does not touch is the
exact-shell line
\(\|\Pi_\beta B\|_2\le(4/3)\alpha\beta^{-1/2}\|w\|_2^2\),
because \(v_n\) is multi-shell.
That line is still CLAIMED. It is
not leftover 4.

**19. Invariant along NS, or only
instantaneous on a subclass?**

The missing replacement is not
written, so it is neither.
The exact-shell claim, if true, is
an instantaneous bound on exact
eigenfields of \(A\). It is not an
NS invariant.

**20. Which continuation criterion
does it feed — BKM,
\(\int\|Au\|_2^2\,dt<\infty\), or
something else?**

None. Not BKM. Does not feed
\(\int\|Au\|_2^2\,dt<\infty\), and
does not restore
★ \(\Rightarrow\) global regularity.
Ordinary NS stays open.

---

## Status

| Item | Verdict |
|---|---|
| \(v_n\) kills unrestricted ★ | **YES.** Instantaneous class. |
| \(T_c\) identity for all \(n\) | **CLAIMED.** Hand cubic. Live \(n\le 10\). |
| Exact-shell \(16/9\) | **CLAIMED.** |
| Factor \(3\) from Ring / Borromean | **NO.** |
| \(K>1\) in the repo | **NO.** |
| Replacement inequality displayed | **NO.** OPEN. |
| Continuation from \(4/3\) | **NO.** |
| Ordinary NS | **OPEN.** |

NS not solved. Soft X silent.
