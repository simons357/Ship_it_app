# Exact-shell 9D — claimed full-support bound

12 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for
\(Aw=\alpha w\);
remainder is occupancy \(s\);
the claimed bound removes that factor
on a single input shell.

**Limitation / assumption.** This page
bounds \(K_{\alpha,\beta}(w)\) only for a
single input eigen-shell \(Aw=\alpha w\).
It does not bound a general multi-shell
field. It does not bound unrestricted
\(\mathcal R_\star\). The unrestricted box
is already dead by the growing-layer
family \(v_n\)
([`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md)).
This page does not resurrect it.
**A true \(4/3\) does not repair
unrestricted ★, does not give a
continuation criterion, and does not
control a multi-shell field.**
Ordinary NS stays open.

Specialist questions:
[`PR24-SPECIALIST-QUESTIONS.md`](PR24-SPECIALIST-QUESTIONS.md).

If \(K\le 16/9\) holds, occupancy \(s\) is
gone on a **single input shell**. That is a
written bound on exact-shell fields, not a
sweep maximum. The three-shear field then
sits under a named ceiling, not under a
rumor.

**CLAIMED: written derivation available;
internal checks passed; independent
specialist review pending. Numerical
sweeps provide consistency checks only.**

Internal audit of the exact-shell argument
found no gap. The named verifier passes
its symbolic checks. That is not a
specialist sign and not a proof assistant.
Soft X silent. NS is not solved.

Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.
Grow-\(s\) samples stay historical.
Do not cash \(0.456\), \(0.641\), or the
exact three-shear \(K=2/3\) as \(C_0\).

Machine: `scripts/ns_attacks/verify_pr24_closure_review.py`.
Math pointer: [`math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md`](math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md).
Grow-\(s\) page: [`ATTACK-9D-GROW-S.md`](ATTACK-9D-GROW-S.md).

---

## Conventions

On the normalized torus
\(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\)
with measure \((2\pi)^{-3}\,dx\). Then
\[
\|w\|_2^2
=
\sum_{k\in\mathbb{Z}^3}\lvert\widehat w_k\rvert^2
=
(2\pi)^{-3}\int_{\mathbb{T}^3}\lvert w\rvert^2\,dx.
\]
The same \(E,A,B,P\) as
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
\(K_{\alpha,\beta}(w)\) is defined only for
\(\alpha>0\) and \(w\neq 0\).
\(\Pi_\beta\) is the spectral projection
onto the exact lattice shell
\(\{k\in\mathbb{Z}^3:\lvert k\rvert^2=\beta\}\).
It is not a dyadic annulus of width 1.
The count below is a lattice count.

---

## Admissible \((\alpha,\beta)\)

The output shell is \(\beta>0\).
A pair \(p+q=k\) with
\(\lvert p\rvert^2=\lvert q\rvert^2=\alpha\)
and \(\lvert k\rvert^2=\beta\) exists only if
\[
0<\beta\le 4\alpha,
\]
because \(\lvert p+q\rvert\le\lvert p\rvert+\lvert q\rvert=2\sqrt{\alpha}\).
For \(\beta>4\alpha\), \(\Pi_\beta B=0\) and \(K=0\).
The nontrivial constraint set sitting next
to the bound is therefore
\[
\alpha>0,\qquad w\neq 0,\qquad 0<\beta\le 4\alpha.
\]
Equivalently \(x=\beta/\alpha\in(0,4]\).
The \(16/9\) line is the maximum of a
one-variable function on that interval,
not a maximum over an unstated range.

---

## Claimed bound

For \(Aw=\alpha w\), the same Leray-projected
\(B(w,w)=P[(w\cdot\nabla)w]\) satisfies

\[
\|\Pi_\beta B(w,w)\|_2
\le
\frac{4}{3}\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\qquad
\beta>0.
\]

Equivalently \(K_{\alpha,\beta}(w)\le 16/9\).
Both supports may grow. Each transverse
polarization may have independent complex
coefficients. Optimality of the constant is
not claimed.

For \(\beta>4\alpha\) the bound is vacuous:
\(\Pi_\beta B=0\).

See the limitation box above. No contradiction
with the multi-shell kill of unrestricted ★.

---

## Geometry on one input shell

Fix \(p+q=k\), \(\lvert p\rvert^2=\lvert q\rvert^2=\alpha\),
\(\lvert k\rvert^2=\beta\). Then
\(k\cdot p=k\cdot q=\beta/2\) and
\[
\lvert k_\perp\rvert^2
=
\beta-\frac{\beta^2}{4\alpha}
=
\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr).
\]
Because \(w_p\perp p\),
\[
\lvert k\cdot w_p\rvert
\le
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}\,|w_p|.
\]
The Fourier bilinear on the locked evaluator is
\[
\widehat B_k
=
i\,P_k\sum_{p+q=k}(q\cdot w_p)w_q
=
i\,P_k\sum_{p+q=k}(k\cdot w_p)w_q.
\]
A crude pair bound with \(\lvert P_k w_q\rvert\le|w_q|\)
returns occupancy. The \(3/4\) form below
uses the symmetrized estimate on top of
the weighted count. That coefficient comes
from algebra and geometry, not from search
results.

---

## Symmetrized interaction estimate

This is the step the bound needs.
For \(p+q=k\) on the specified shells,

\[
\bigl\lvert
P_k\bigl[(q\cdot w_p)w_q+(p\cdot w_q)w_p\bigr]
\bigr\rvert
\le
\sqrt{\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)}
\,|w_p|\,|w_q|.
\]

Because \(k\) is real and \(p\cdot w_p=0\),
\[
k\cdot w_p
=
k_\perp\cdot w_p
=
\sum_{j=1}^3 (k_\perp)_j\,(w_p)_j.
\]
Cauchy–Schwarz on \(\mathbb{C}^3\) is then
the explicit line
\[
\bigl\lvert k\cdot w_p\bigr\rvert
=
\Bigl\lvert\sum_{j=1}^3 (k_\perp)_j\,(w_p)_j\Bigr\rvert
\le
\lvert k_\perp\rvert\,|w_p|,
\]
and likewise for \(w_q\). The pairing \(k\cdot w_p\) is bilinear
in the coordinates. It does not
conjugate \(w_p\). Conjugation is used
only to form
\(\lvert w_p\rvert^2=\sum_j(w_p)_j\overline{(w_p)_j}\)
and in the proof of Cauchy–Schwarz.
This uses only \(p\cdot w_p=0\) and
\(k_\perp\in\mathbb{R}^3\). Both
transverse polarizations at \(p\) may
be occupied, with independent complex
amplitudes; \(w_p\) is an arbitrary
vector in \(p^\perp\subset\mathbb{C}^3\).
After the in-plane cancellation in §3,
the projected symmetrized term is
bounded by this factor times
\(|w_q|\), not twice that.
Saturation is not claimed.

The ordered convolution equals half its
symmetrization for complex coefficients
as well, because the pairing is bilinear
and the sum runs over all ordered pairs
\(p+q=k\). A sesquilinear pairing would
break the identity. The locked pairing
is \(q\cdot w_p=\sum q_j(w_p)_j\).
\[
\sum_{p+q=k}(q\cdot w_p)w_q
=
\frac12
\sum_{p+q=k}
\bigl[(q\cdot w_p)w_q+(p\cdot w_q)w_p\bigr].
\]

---

## Weighted count

Let \(S\subset\{p:\lvert p\rvert^2=\alpha\}\),
\(a_p\ge 0\), and
\(c_k=\sum_{p+q=k}a_p a_q\).
The claimed lattice inequality is

\[
\sum_{\lvert k\rvert^2=\beta}c_k^2
\le
3\Bigl(\sum_{p\in S}a_p^2\Bigr)^2.
\]

Write \(M=\sum_{p\in S}a_p^2\) and expand
\[
\sum_k c_k^2
=
\sum_{p,r\in S}
a_p a_r
\sum_{k\in K(p,r)}
a_{k-p}a_{k-r},
\]
where \(K(p,r)\) is the set of \(k\) with
\(\lvert k\rvert^2=\beta\) and
\(k\cdot p=k\cdot r=\beta/2\)
(so that \(k-p\) and \(k-r\) lie on the
input shell).

- If \(p\) and \(r\) are linearly independent,
  the two affine planes meet the sphere
  \(\lvert k\rvert^2=\beta\) in at most two
  points, so \(\lvert K(p,r)\rvert\le 2\).
- If \(r=\lambda p\) and
  \(\lvert p\rvert^2=\lvert r\rvert^2=\alpha\),
  then \(\lambda=\pm 1\). The case \(r=p\) is
  the diagonal. The case \(r=-p\) forces
  \(\beta=0\), which is excluded.

Off-diagonal terms therefore meet at most
two outputs. Weighted AM-GM
\(2a_pa_ra_{k-p}a_{k-r}\le a_p^2 a_{k-p}^2+a_r^2 a_{k-r}^2\)
bounds that contribution by \(2M^2\).
The diagonal \(p=r\) contributes at most
\(M^2\). Adding those pieces gives the
factor \(3\). This count is proved
**on this page**, from the two-plane
incidence and that AM-GM. It is not
proved on a Ring Lemma or Borromean
page. Those are a different integral.
It is not a finite-shell experiment.

This is not the Ring Lemma and not a
Borromean triad. Those are a different
integral, and the Ring Lemma is not
quoted as proved
([`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md),
[`H1-SOT.md`](H1-SOT.md)).

---

## Coefficient algebra

Squaring the half-symmetrization contributes
\(1/4\). The weighted count contributes \(3\).
Together,

\[
\|\Pi_\beta B(w,w)\|_2^2
\le
\frac34\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)
\|w\|_2^4.
\]

Then
\[
K_{\alpha,\beta}(w)
=
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
\le
\frac34\Bigl(\frac{\beta}{\alpha}\Bigr)^2
\Bigl(1-\frac{\beta}{4\alpha}\Bigr)
\le
\frac{16}{9}
\qquad
(0<\beta\le 4\alpha).
\]

Let \(x=\beta/\alpha\in(0,4]\) and
\[
g(x)
=
\frac34 x^2\Bigl(1-\frac x4\Bigr)
=
\frac34\Bigl(x^2-\frac{x^3}4\Bigr).
\]
Then
\[
g'(x)
=
\frac34\Bigl(2x-\frac{3x^2}4\Bigr)
=
\frac34 x\Bigl(2-\frac{3x}4\Bigr).
\]
The only critical point in \((0,4]\) is
\(x=8/3\). The endpoints give
\(g(x)\to 0\) as \(x\to 0^+\) and \(g(4)=0\).
At the critical point
\[
g\Bigl(\frac83\Bigr)
=
\frac34\cdot\frac{64}9\cdot\Bigl(1-\frac23\Bigr)
=
\frac34\cdot\frac{64}9\cdot\frac13
=
\frac{16}9.
\]
So \(\sup_{x\in(0,4]}g(x)=16/9\).
That is the claimed \(K\) bound.
\(C=4/3=\sqrt{16/9}\) is the constant in
\(\|\Pi_\beta B\|_2\le C\alpha\beta^{-1/2}E\).

The ratio \(x=8/3\) occurs on the lattice:
\(p=(1,1,1)\), \(q=(1,1,-1)\) give
\(\alpha=3\), \(\beta=8\). The maximizer of
the bound function is not excluded by
shell geometry. That does not say \(K\)
attains \(16/9\). Optimality of the
constant is not claimed.
The coefficient is algebra and geometry,
not a search result. A reviewer should
still redo this derivative by hand.
Independent review of the §3 kernel
step remains pending.

---

## Boundary \(\beta\to 4\alpha\)

At \(\beta=4\alpha\), \(\lvert k_\perp\rvert=0\)
and \(g(4)=0\). The interaction estimate
uses \(\lvert k_\perp\rvert\) as a
**multiplier**, never as a denominator.
Nothing in the argument divides by
\(\lvert k_\perp\rvert\) or requires it
bounded away from zero. At the endpoint
the symmetrized bound is \(0\), so those
pairs do not contribute. The equivalent
form \(\|\Pi_\beta B\|_2\le(4/3)\alpha\beta^{-1/2}E\)
divides by \(\sqrt{\beta}=2\sqrt{\alpha}>0\),
not by \(\lvert k_\perp\rvert\). The
quotient \(K\) has \(\beta\) in the
numerator. Nothing divides by
\(1-\beta/(4\alpha)\), including in the
definition of \(K\). The endpoint is
regular.

---

## Three-shear example and historical numbers

The three-shear field
\[
w(x,y,z)=(\sin y,\ \sin z,\ \sin x)
\]
is exact-shell with \(\alpha=1\). Its bilinear
lives on \(\beta=2\), is already divergence-free,
and gives
\(\|w\|_2^2=3/2\),
\(\|\Pi_2 B(w,w)\|_2^2=3/4\),
hence **\(K=2/3\) exactly**.
The locked evaluator reproduces that value.
This sits **strictly inside** the claimed
ceiling: \(2/3=6/9<16/9\). It is an exact
lower example, not a matching lower bound,
and it does not make \(16/9\) sharp.

Public coefficients, so a reviewer can
reproduce \(2/3\) without the script.
Six input modes, each of mass \(1/4\):
\(\widehat w_{(0,1,0)}=(-i/2,0,0)\) and
conjugate; \(\widehat w_{(0,0,1)}=(0,-i/2,0)\)
and conjugate;
\(\widehat w_{(1,0,0)}=(0,0,-i/2)\) and
conjugate. Then \(\|w\|_2^2=3/2\).
Twelve output modes on \(\lvert k\rvert^2=2\),
each of mass \(1/16\):
\(\widehat B_{(0,\pm 1,\pm 1)}\) along \(e_1\),
\(\widehat B_{(\pm 1,0,\pm 1)}\) along \(e_2\),
\(\widehat B_{(\pm 1,\pm 1,0)}\) along \(e_3\),
with amplitudes \(\pm i/4\) as in
[`PR24-SPECIALIST-QUESTIONS.md`](PR24-SPECIALIST-QUESTIONS.md)
(question 11). Then
\(\|\Pi_2 B\|_2^2=12/16=3/4\) and
\(K_{1,2}=2\cdot(3/4)/(3/2)^2=2/3\).

No exact-shell field in this repo has
\(K>1\). The ceiling is \(16/9\) because
that is \(\sup g\), not because a field
attained it. A counterexample would be
one pair \((\alpha,\beta)\) and one
conjugate-closed list on
\(\lvert k\rvert^2=\alpha\) with
\(K_{\alpha,\beta}>16/9\).

A finite superposition of exact-shell
fields does **not** inherit a \(C\) that
depends only on the number of shells.
That would be a different theorem.
This page does not claim it.

Historical numerical maxima sit beside it.
They are consistency checks, not the bound.

| Source | \(K\) | Role |
|---|---|---|
| Three-shear \(w=(\sin y,\sin z,\sin x)\) | \(2/3\) exactly | Named example |
| Aligned 9B at \((4,8)\) | \(\approx 0.641\) | Historical sample |
| Grow-\(s\) max at \((16,32)\) | \(\approx 0.456\) | Historical sample |
| Claimed ceiling | \(16/9\approx 1.778\) | Written bound |

Do not merge \(2/3\), \(0.641\), and \(0.456\).
None of them is \(C_0\).

---

## Verifier

`scripts/ns_attacks/verify_pr24_closure_review.py`
proves nothing. It checks the planar
seed transfers, the small-\(n\) cubic
count, and growing-layer moments
against the two evaluators. It computes
the three-shear \(K=2/3\) and
\(g(8/3)=16/9\). It reads the saved
sweep summary. It does not perform the
shell-count experiments described here.
If the script is deleted, the writes
on this page and on the kill page
remain human-checkable.

The first written estimate that \(v_n\)
does not refute is the displayed
exact-shell bound above. It is
instantaneous on \(Aw=\alpha w\), not
invariant along NS, and it feeds no
continuation criterion (not BKM, not
\(\int\|Au\|_2^2\,dt<\infty\)).
A replacement energy-budget closure
on the full class is **OPEN** and is
not written.

---

## Independent review

No named reviewer. No date.
Independent specialist review is
**pending**. This page is not assigned
to Tao, Vicol, Gómez-Serrano, or any
other named reader of the broader NS
program. Those names are a different
list. They have not been asked to sign
this estimate. This is not a Dream Team
vote. Soft X silent.

---

## What the next review checks

Redo the one-variable maximum of
\(g(x)=(3/4)x^2(1-x/4)\) on \((0,4]\).
The written calculus sits above.
Then verify the weighted incidence
argument (two-plane plus AM-GM) that
produces the factor \(3\), and the
complex-polarization identity: the
Hermitian line
\(\lvert k\cdot w_p\rvert\le\lvert k_\perp\rvert\,|w_p|\)
together with the §3 in-plane cancellation.
The limitation box is the scope.

---

## Status

| Item | Verdict |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Grow-\(s\) finite max as \(C_0\) | **NO.** Historical. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Written derivation available; internal checks passed; independent specialist review pending. Numerical sweeps provide consistency checks only. |
| Three-shear \(K=2/3\) as the ceiling | **NO.** Exact example under the claimed bound. |
| Sweep max \(0.641\) / \(0.456\) as the ceiling | **NO.** Not the bound. |
| True \(4/3\) as a regularity close | **NO.** Does not repair ★. No continuation. |
| Unrestricted ★ | **NO.** Dead by \(v_n\). |
| Ordinary NS | **OPEN.** |
| Specialist sign of the algebra | **pending.** Soft X silent. |

NS not solved.
