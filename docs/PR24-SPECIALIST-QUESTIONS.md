# Specialist questions on the two PR-24 writes

13 September 2026.
Answers in writing before anyone else
reads the pages. Not a sweep.
**NS not solved.** Soft X silent.

Exact-shell page:
[`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md).
Kill page:
[`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).
Questions 5–10 and 14 are also on the
exact-shell page.

---

## On the kill

**1. Which identity may fail, and was it
checked by hand for general \(n\)?**

The kill uses
\(T_c(v_n)=3n^5(3n^2+3n+1)\).
If that identity fails, the elementary
lower bound \(\mathcal R_\star\ge n/165888\)
fails. The factor \(3n^2+3n+1\) is the
number of ordered pairs
\((a,b)\in\mathbb{Z}^2\) with
\(\lvert a\rvert,\lvert b\rvert,\lvert a+b\rvert\le n\).
That count is elementary for every
\(n\ge 1\): for \(a\ge 0\), \(b\) runs
through \(2n-a+1\) values; for \(a<0\),
through \(2n+a+1\) values; the two sums
add to \(3n^2+3n+1\). The seed pairing
that supplies the remaining \(3n^5\),
and the vertical cancellation that
drops the terms paired with \(U\) and
\(A_h U\), are the identities a
specialist must still accept. Those
were matched to the live evaluators on
\(n=1,\dots,10\), not only \(n\le 8\).
They are not a hand proof for general
\(n\). Specialist reading of that
cancellation remains pending.

**2. Is \(\mathcal D_s(v_n)>0\) for every
\(n\ge 1\)?**

Yes. The support uses planar seeds
\(\lvert r\rvert^2\in\{1,2,5\}\) and
vertical frequencies \(\lvert j\rvert\le n\),
so the eigenvalues include
\(n^2\), \(2n^2\), and \(5n^2\)
(the \(j=0\) copies). Those three
numbers are distinct for every
\(n\ge 1\). At least two eigenvalues
carry mass, so
\(\mathcal D_s=X\operatorname{Var}_\mu(\lambda)>0\).
This is not only a computed-row fact.

**3. Does a change of normalization flip
\(\mathcal R_\star\to\infty\)?**

No consistent change does.
\(\mathcal R_\star(av)=\mathcal R_\star(v)\).
A global torus-measure constant that
is applied to \(E\), \(\mathcal D_s\),
\(Y\), and \(T_c\) together leaves the
ratio unchanged. Omitting the factor
\(n\) in \(U(nx,ny)\) writes a
**different field**, not a
renormalization of \(v_n\). That other
field is not this counterexample.

**4. If someone says \(v_n\) is “not a
Navier–Stokes field”?**

Reply: the boxed claim is an
**instantaneous** bound on the
admissible class
(divergence-free, real, mean-zero,
finite Fourier support,
\(\mathcal D_s>0\) on \(\mathbb{T}^3\)).
\(v_n\) sits in that class. It is not
an NSE trajectory and not a singular
solution. The family kills the
instantaneous inequality. It does not
construct a blowup.

---

## On exact-shell 9D

**5. Where is the factor \(3\) proved?**

On the exact-shell page: two-plane
incidence plus AM-GM, plus the
diagonal. Not on a Ring Lemma or
Borromean page. Those are a different
integral and are not quoted as proved.

**6. Hermitian estimate, \(w_p\in\mathbb{C}^3\),
\(w_p\perp p\), no reality assumption.
Which line uses conjugation?**

\[
k\cdot w_p
=
\sum_{j=1}^3 (k_\perp)_j\,(w_p)_j,
\qquad
\bigl\lvert k\cdot w_p\bigr\rvert
\le
\lvert k_\perp\rvert\,|w_p|.
\]

The pairing \(k\cdot w_p\) is bilinear
in the coordinates. It does not
conjugate \(w_p\). Conjugation is used
only to form
\(\lvert w_p\rvert^2=\sum_j(w_p)_j\overline{(w_p)_j}\)
and in the proof of Cauchy–Schwarz.
The same line holds if both
polarizations in \(p^\perp\) are
occupied.

**7. Does the argument divide by
\(1-\beta/(4\alpha)\)?**

No. That factor multiplies, including
inside \(K=\beta\|\Pi_\beta B\|_2^2/(\alpha^2\|w\|_2^4)\).
Nothing in the definition of \(K\)
divides by \(\lvert k_\perp\rvert\) or
by \(1-\beta/(4\alpha)\). The \(C\) form
divides by \(\sqrt{\beta}>0\).

**8. Is the ordered convolution exactly
half the symmetrization for complex
coefficients?**

Yes, because the pairing is bilinear
with real \(p,q\) and the sum runs over
all ordered pairs \(p+q=k\). Swapping
\((p,q)\) is a bijection of that set.
If the pairing were sesquilinear, the
identity would fail. The locked pairing
is \(q\cdot w_p=\sum q_j(w_p)_j\).

**9. What is \(\Pi_\beta\)?**

The spectral projection onto the exact
lattice shell
\(\{k\in\mathbb{Z}^3:\lvert k\rvert^2=\beta\}\).
It is not a dyadic annulus of width 1.
The count is a lattice count.

**10. Both polarizations at \(p\),
independent complex amplitudes?**

Yes. \(w_p\) is an arbitrary vector in
the complex plane \(p^\perp\subset\mathbb{C}^3\),
with \(w_{-p}=\overline{w_p}\) for a real
field. The displayed line uses only
\(p\cdot w_p=0\).

---

## On examples

**11. Public \(K_{1,2}\) for
\(w=(\sin y,\sin z,\sin x)\).**

Six input modes, each of mass \(1/4\):

| \(k\) | \(\widehat w_k\) |
|---|---|
| \((0,1,0)\) | \((-i/2,0,0)\) |
| \((0,-1,0)\) | \((i/2,0,0)\) |
| \((0,0,1)\) | \((0,-i/2,0)\) |
| \((0,0,-1)\) | \((0,i/2,0)\) |
| \((1,0,0)\) | \((0,0,-i/2)\) |
| \((-1,0,0)\) | \((0,0,i/2)\) |

\(\|w\|_2^2=6\cdot(1/4)=3/2\).
Already divergence-free bilinear
\(B=(\sin z\cos y,\sin x\cos z,\sin y\cos x)\).
Twelve output modes on \(\lvert k\rvert^2=2\),
each of mass \(1/16\):

\[
\begin{aligned}
\widehat B_{(0,1,1)}&=(-i/4,0,0),&
\widehat B_{(0,-1,-1)}&=(i/4,0,0),\\
\widehat B_{(0,-1,1)}&=(-i/4,0,0),&
\widehat B_{(0,1,-1)}&=(i/4,0,0),\\
\widehat B_{(1,0,1)}&=(0,-i/4,0),&
\widehat B_{(-1,0,-1)}&=(0,i/4,0),\\
\widehat B_{(1,0,-1)}&=(0,-i/4,0),&
\widehat B_{(-1,0,1)}&=(0,i/4,0),\\
\widehat B_{(1,1,0)}&=(0,0,-i/4),&
\widehat B_{(-1,-1,0)}&=(0,0,i/4),\\
\widehat B_{(-1,1,0)}&=(0,0,-i/4),&
\widehat B_{(1,-1,0)}&=(0,0,i/4).
\end{aligned}
\]

\(\|\Pi_2 B\|_2^2=12\cdot(1/16)=3/4\).
Then
\(K_{1,2}=2\cdot(3/4)/(3/2)^2=2/3\).
Physical check:
\((2\pi)^{-3}\int(\sin^2 y+\sin^2 z+\sin^2 x)=3/2\)
and
\((2\pi)^{-3}\int(\sin^2 z\cos^2 y+\sin^2 x\cos^2 z+\sin^2 y\cos^2 x)=3/4\).

**12. Any exact-shell field in the repo
with \(K>1\)?**

No. Printed maxima are
\(2/3\), \(\approx 0.641\), \(\approx 0.456\).
The ceiling is \(16/9\) because that is
\(\sup g\) on \((0,4]\), not because a
field attained it. Optimality is not
claimed. Absence of \(K>1\) is not a
reason to replace \(16/9\) by \(1\).

**13. What would a counterexample look
like?**

One pair \((\alpha,\beta)\) with
\(\alpha>0\) and \(0<\beta\le 4\alpha\),
and one conjugate-closed divergence-free
list \(\{\widehat w_k\}\) supported on
\(\lvert k\rvert^2=\alpha\), such that
\(K_{\alpha,\beta}(w)>16/9\).

---

## On scope

**14. One sentence a true \(4/3\) does
not imply.**

A true \(4/3\) does not repair
unrestricted ★, does not give a
continuation criterion, and does not
control a multi-shell field.

**15. Finite superposition and a \(C\)
that depends only on the number of
shells?**

No. That would be a different theorem.
This page does not claim it. The family
\(v_n\) is multi-shell; a bound
\(C=C(N_{\mathrm{shells}})\) is not
written here.

---

## On the machine

**16. What the script proves, and what
it only reads.**

It proves nothing. It is not a proof
assistant. It **checks** the planar seed
transfers \(3/4,-1,1/4\), the cubic
count \(3n^2+3n+1\) by enumeration on
small \(n\), and the growing-layer
moments against
`stokes_moments.py` and
`ns_lemma_star_core.py` on
\(n=1,2,3,4,5,6,8,10\). It **computes**
the three-shear \(K=2/3\) and the
identity \(g(8/3)=16/9\). It **reads**
`results/attack9b_grow_s/grow_s.json`.
It does not run the shell-count
experiments.

**17. If the script is deleted?**

The claims still have human-checkable
writes on the two pages. The script is
a consistency check. Deleting it does
not unclaim \(16/9\) and does not
unkill unrestricted ★.

---

## On replacement

**18. First written estimate that
\(v_n\) does not refute.**

\[
\|\Pi_\beta B(w,w)\|_2
\le
\frac43\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\qquad
Aw=\alpha w.
\]

A replacement energy-budget closure on
the full class is **OPEN** and is not
written. Need★ is MISSING.

**19. Invariant along NS, or only
instantaneous on a subclass?**

Only an instantaneous bound on the
subclass \(Aw=\alpha w\). An NSE
solution leaves one shell immediately.
Not invariant along the flow.

**20. Which continuation criterion
does it feed?**

None. Not BKM, not
\(\int\|Au\|_2^2\,dt<\infty\),
not any other continuation criterion.
A true \(4/3\) is **NO** as a regularity
close.

---

Ordinary NS stays open. Soft X silent.
