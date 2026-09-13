# Exact-shell 9D — claimed full-support bound

12 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for
\(Aw=\alpha w\);
remainder is occupancy \(s\);
the claimed bound removes that factor
on a single input shell.

**Limitation (labeled).** This page
bounds \(K_{\alpha,\beta}(w)\) for a
single input shell \(Aw=\alpha w\).
It does not bound a general multi-shell
field. It does not bound an arbitrary
simultaneous finite-closer limit.
Unrestricted Lemma★ is a different
statement. That box is killed by \(v_n\)
([`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md)).
This page does not resurrect it.
No contradiction. Do not read past
this box.

If \(K\le 16/9\) holds, occupancy \(s\) is
gone on a **single input shell**. That is a
written bound on exact-shell fields, not a
sweep maximum. The three-shear field then
sits under a named ceiling, not under a
rumor.
write-up example \(K_{1,2}=2/3\) on
\(w=(\sin y,\sin z,\sin x)\).
Floor, not the ceiling.
Sanity: \(2/3\approx 0.667\) sits
strictly inside the claimed ceiling
\(16/9\approx 1.778\). A named floor
under a named (claimed) upper bound.
That does not prove the ceiling.
[`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md).

**No as a regularity close.** A true
\(4/3\) does not kill or repair unrestricted
★. That box is already dead by the
multi-shell family \(v_n\). It does not
give a continuation criterion and it does
not restore ★ \(\Rightarrow\) global regularity.
Ordinary NS stays open.

Until a specialist signs the algebra, or a
sweep shows nothing near \(16/9\), the
word is still **CLAIMED**. Existing maxima
\(0.641\) and \(0.456\) are not near
\(16/9\approx 1.778\). That does not
unclaim the bound.
**Independent review.** Pending. No name.
No date. Soft X silent. This page is
not a letter to Tao, Albritton, Vicol,
or Gómez-Serrano. Those names are not
the reviewer of this shell estimate.
An internal audit is not that review.
NS is not solved.

Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.
Grow-\(s\) samples stay historical.
Do not cash \(0.456\), \(0.641\), or
\(2/3\) as \(C_0\).

Machine: `scripts/ns_attacks/verify_pr24_closure_review.py`.
Math pointer: [`math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md`](math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md).
Grow-\(s\) page: [`ATTACK-9D-GROW-S.md`](ATTACK-9D-GROW-S.md).

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

**Conventions.** Normalized torus
\(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\).
Fourier \(w=\sum\widehat w_k e^{ik\cdot x}\),
Plancherel \(\|w\|_2^2=\sum\lvert\widehat w_k\rvert^2\).
Same bilinear as the locked evaluator:
\(\widehat B_k=i\,P_k\sum_{p+q=k}(q\cdot\widehat w_p)\widehat w_q\),
both orders present, no extra \(1/2\).
An ordered-convolution reading that writes
the factor \(3/4\) as \((1/2)^2\) times the
count \(3\) is a reconstruction. It does
not match this \(B\). Do not cash it as
the kernel remainder.

**Constraint set, stated with the bound.**
The inequality is for \(\alpha>0\),
\(w\neq 0\), \(Aw=\alpha w\), and \(\beta>0\).
If \(\beta>4\alpha\) no pairs occur
(\(\lvert p+q\rvert\le 2\sqrt{\alpha}\)),
so \(\Pi_\beta B=0\) and the line holds
vacuously. The cubic comparison below
uses the closed range \(0<\beta\le 4\alpha\),
i.e. \(x=\beta/\alpha\in(0,4]\). That
constraint sits here, not as a later
remark.

The limitation box above is the scope.
Do not promote this line past one
input shell.

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
Write \(k=k_\parallel+k_\perp\) with
\(k_\parallel=(\beta/(2\alpha))p\), so
\(k_\perp\cdot p=0\) and \(k_\perp\) is real.
Because \(w_p\perp p\) (complex bilinear
\(p\cdot w_p=0\)),
\(k\cdot w_p=k_\perp\cdot w_p
=\sum_j(k_\perp)_j(w_p)_j\).
The standard Hermitian product on
\(\mathbb{C}^3\) is
\(\langle u,v\rangle=\sum_j u_j\overline{v}_j\).
Then
\[
\lvert k\cdot w_p\rvert
=
\bigl\lvert\langle k_\perp,\overline{w_p}\rangle\bigr\rvert
\le
\lvert k_\perp\rvert\,\lvert w_p\rvert
=
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}\,|w_p|.
\]
Equality iff \(w_p=\lambda k_\perp\) for
some \(\lambda\in\mathbb{C}\). That choice
is a legal transverse polarization
(still \(\perp p\)). So the one-mode
bound is available for independently
complex coefficients. Modewise equality
does not make \(K=16/9\) sharp.
The claimed \(3/4\) is a later step on
the sum, not this CS.

As \(\beta\to 4\alpha^-\),
\(\lvert k_\perp\rvert\to 0\). The estimate
is a product. Nothing in the argument
divides by \(\lvert k_\perp\rvert\) or by
\(1-\beta/(4\alpha)\). The claimed
envelope \(f(x)\) vanishes at \(x=4\).
The \(C\) form has \(\alpha/\sqrt{\beta}\);
here \(\beta\to 4\alpha>0\), so
\(\sqrt{\beta}\) stays bounded away from
zero. At \(\beta=4\alpha\) the pairs are
collinear, \(k_\perp=0\), \(k\cdot w_p=0\),
and those contributions vanish. Not a
singular limit.
The Fourier bilinear on the locked evaluator is
\[
\widehat B_k
=
i\,P_k\sum_{p+q=k}(q\cdot w_p)w_q
=
i\,P_k\sum_{p+q=k}(k\cdot w_p)w_q.
\]
A crude pair bound with \(\lvert P_k w_q\rvert\le|w_q|\)
returns occupancy. The claimed \(3/4\) form
uses the exact complex polarization
cancellation on top of the weighted count
below. Specialist review should check that
kernel step. DA has not replaced it by a
proof assistant.

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

The factor \(3\) is derived on this page
from the two-plane proposition below
plus AM-GM. It is not imported from
the Ring Lemma (REPAIR) or from a
Borromean triad count. Those are a
different leftover. Do not glue them
here.

Expand the square:
\[
\sum_{\lvert k\rvert^2=\beta}c_k^2
=
\sum_{p,r\in S}a_p a_r
\sum_{k\in\mathcal K(p,r)}a_{k-p}a_{k-r},
\]
where
\(\mathcal K(p,r)
=\{k:\lvert k\rvert^2=\beta,\,
k\cdot p=k\cdot r=\beta/2,\,
k-p,k-r\in S\}\).

**Claimed proposition — two-plane incidence.**
A fixed pair \((p,r)\) can meet only those
outputs. Isolated on this page.

- If \(p\) and \(r\) are linearly independent,
  two affine planes meet the sphere
  \(\lvert k\rvert^2=\beta\) in at most two points.
  So \(\#\mathcal K(p,r)\le 2\).
- If \(r=\lambda p\) and \(\lvert p\rvert^2=\lvert r\rvert^2=\alpha\),
  then \(\lambda=\pm 1\). The case \(r=p\) is
  the diagonal. The case \(r=-p\) forces
  \(\beta=0\), which is excluded.

Split. Diagonal \(p=r\):
\(\#\mathcal K(p,p)\le 1\), hence
\[
\sum_p a_p^2\sum_{k\in\mathcal K(p,p)}a_{k-p}^2
\le
\Bigl(\sum_{p\in S}a_p^2\Bigr)^2.
\]
Off-diagonal \(p\neq r\):
\(\#\mathcal K(p,r)\le 2\) and AM-GM
\(a_p a_r a_{k-p}a_{k-r}
\le\tfrac12(a_p^2 a_{k-p}^2+a_r^2 a_{k-r}^2)\)
bounds that contribution by twice the
squared mass. Total factor \(3\).

A specialist can break the two-plane
step by naming one pair that meets
three outputs on a shell \(\beta>0\).
Isolating is not certification.
The derivation of \(3\) from that
proposition plus AM-GM sits here.
There is no other pointer.

The audit draws this count on shells
\((4,8)\), \((5,4)\), \((1,2)\) and prints
ratio \(\le 3\). That is a check, not the
lattice theorem.

**What the machine actually ran.**
`verify_pr24_closure_review.py` is an
internal check. It is not independent
review. It does four things:

1. Live growing-layer moments against
   the closed-form \(T_c\) and against
   a saved \(n=1..4\) table.
2. Live random exact-shell \(K\) on five
   pairs. Those \(K\) sit under \(16/9\).
   That is a sample, not the bound.
3. Live random weighted-count ratios on
   three pairs. Ratio \(\le 3\) there.
   That is not the lattice theorem.
4. Reads the grow-\(s\) maximum from a
   saved sweep JSON. It does not rerun
   that sweep.

It does not run a near-ceiling search.
It does not certify \(16/9\). A reviewer
who treats those printed ratios as the
count experiment will trust the number
for the wrong reason.

---

## Polarization and the \(K\) form

Combining the count with the claimed
polarization cancellation gives

\[
K_{\alpha,\beta}(w)
\le
\frac{3}{4}\Bigl(\frac{\beta}{\alpha}\Bigr)^2
\Bigl(1-\frac{\beta}{4\alpha}\Bigr)
\le
\frac{16}{9}
\qquad
(0<\beta\le 4\alpha).
\]

Let \(x=\beta/\alpha\in(0,4]\) — the
constraint set above, not an unspoken
range. Write
\[
f(x)
=
\frac{3}{4}x^2\Bigl(1-\frac{x}{4}\Bigr)
=
\frac{3}{4}\Bigl(x^2-\frac{x^3}{4}\Bigr).
\]
Then
\[
f'(x)
=
\frac{3}{4}\Bigl(2x-\frac{3x^2}{4}\Bigr)
=
\frac{3}{4}\,x\Bigl(2-\frac{3x}{4}\Bigr).
\]
Critical points \(x=0\) (excluded) and
\(x=8/3\in(0,4]\). Endpoints:
\(f(x)\to 0\) as \(x\to 0^+\),
\(f(4)=0\). The interior value is
\[
f\Bigl(\frac{8}{3}\Bigr)
=
\frac{3}{4}\cdot\frac{64}{9}\cdot\Bigl(1-\frac{2}{3}\Bigr)
=
\frac{3}{4}\cdot\frac{64}{9}\cdot\frac{1}{3}
=
\frac{16}{9}.
\]
That is the maximum of the **claimed
envelope**. It does not prove the
envelope. \(C=4/3=\sqrt{16/9}\) is the
constant in
\(\|\Pi_\beta B\|_2\le C\alpha\beta^{-1/2}E\).
Optimality of \(4/3\) is not claimed.

Internal check: this one-variable
calculus sits. Independent review
still has to sign the kernel, the
factor \(3/4\), the two-plane count,
and the limiting-closer scope.
Those are different jobs.

Random exact-shell fields on
\((4,8)\), \((5,4)\), \((9,4)\), \((16,32)\),
\((1,2)\) printed \(K\le 0.456<16/9\).
Aligned 9B \(K\approx 0.641<16/9\).
Grow-\(s\) max \(K\approx 0.456<16/9\).
Those numbers sit. They are not the proof.

---

## Specialist break lines

Full answers:
[`PR24-SPECIALIST-BREAK.md`](PR24-SPECIALIST-BREAK.md).
These six plus 14 sit here so a
reviewer does not hunt.

**5.** Factor \(3\) is derived on this
page (two-plane + AM-GM). Not Ring.
Not Borromean.

**6.** For \(w_p\in\mathbb{C}^3\),
\(w_p\perp p\), no reality:
\(\lvert k\cdot w_p\rvert
=\lvert\langle k_\perp,\overline{w_p}\rangle\rvert
\le\lvert k_\perp\rvert\,\lvert w_p\rvert\).
Conjugation is in
\(\langle u,v\rangle=\sum u_j\overline{v}_j\),
used once, on \(w_p\).

**7.** Nothing divides by
\(1-\beta/(4\alpha)\). The boxed
\(K=\beta\|\Pi_\beta B\|_2^2/(\alpha^2\|w\|_2^4)\)
has no such factor.

**8.** Ordered convolution is not
half the symmetrization, for real
or for complex. Live \(B\) keeps
both orders and no extra \(1/2\).

**9.** \(\Pi_\beta\) is the spectral
projection onto the lattice shell
\(\lvert k\rvert^2=\beta\) exactly.
Not a dyadic shell of width 1.

**10.** Yes. Both transverse
polarizations at \(p\), independent
complex amplitudes. The one-mode
line uses \(\lvert w_p\rvert\).
The factor \(3/4\) is still CLAIMED
for that class.

**11.** Public modes of
\(w=(\sin y,\sin z,\sin x)\):
\(\widehat w(0,\pm 1,0)=(\mp i/2,0,0)\),
\(\widehat w(0,0,\pm 1)=(0,\mp i/2,0)\),
\(\widehat w(\pm 1,0,0)=(0,0,\mp i/2)\).
Twelve outputs on \(\beta=2\), each
\(\lvert\widehat B_k\rvert^2=1/16\),
so \(K_{1,2}=2/3\). Hand arithmetic
on [`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md).

**12.** No exact-shell field in this
repo has \(K>1\). The seated max is
\(2/3\). The ceiling is \(16/9\)
because that is the envelope max,
not because a sample approached it.

**13.** A counterexample is one pair
\((\alpha,\beta)\) and one
conjugate-closed divergence-free
list on \(\lvert p\rvert^2=\alpha\)
with \(K_{\alpha,\beta}(w)>16/9\).

**14.** A true \(4/3\) does not repair
unrestricted ★, does not give a
continuation criterion, and does
not control a multi-shell field.

**15.** No. A constant that depends
only on the number of shells is a
different theorem.

---

## Status

| Item | Verdict |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Grow-\(s\) finite max as \(C_0\) | **NO.** Historical. |
| Three-shear \(K=2/3\) as \(C_0\) | **NO.** write-up example. Floor only. |
| \(2/3<16/9\) as a sanity check | **YES.** Floor strictly inside claimed ceiling. Not a proof of \(16/9\). |
| Factor \(3\) as a theorem | **NO.** On-page from claimed two-plane + AM-GM. |
| Ring Lemma / Borromean as this count | **NO.** Different leftover. REPAIR. |
| Two-plane incidence as a theorem | **NO.** Isolated. Still CLAIMED. |
| Named independent reviewer / date | **NO.** Pending. Soft X silent. Not a letter. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** \(C=4/3\). Occupancy \(s\) gone on one input shell if it holds. |
| Cubic max of the claimed envelope | **YES** as calculus at \(x=8/3\). **NO** as a proof of the envelope. |
| Live audit as \(16/9\) | **NO.** Internal check. Not independent review. |
| Reconstructed \(3/4=(1/2)^2\cdot 3\) | **NO.** Live \(B\) has no extra \(1/2\). |
| Sweep max \(0.641\) / \(0.456\) as the ceiling | **NO.** Not the bound. |
| True \(4/3\) as a regularity close | **NO.** Does not repair ★. No continuation. |
| Unrestricted ★ | **NO.** Dead by \(v_n\). |
| Ordinary NS | **OPEN.** |
| Specialist sign of the algebra | **pending.** Soft X silent. |
| Factor \(3\) from Ring / Borromean | **NO.** On this page. |
| \(K>1\) in the repo | **NO.** Seated max \(2/3\). |
| Multi-shell \(C\) from shell count | **NO.** Different theorem. |

NS not solved.
