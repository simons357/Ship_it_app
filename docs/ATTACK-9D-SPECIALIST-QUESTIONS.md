# Specialist questions — answered in writing

13 September 2026.
Answers before anyone else reads the page.
Ordinary NS stays **open**. Soft X silent.
Word on exact-shell \(16/9\): **CLAIMED**.
Items 5–10 and 14 are also on
[`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md).

I did **not** hand-check the all-\(n\) \(T_c\)
identity. The live evaluators check
\(n=1,\dots,10\). That is not a general-\(n\)
proof.

---

## On the kill

### 1. Which identity in \(v_n\) may fail? General \(n\), not only \(n\le 8\)?

The identity that is allowed to fail is the
closed transfer

\[
N(v_n)=0,\qquad
T_c(v_n)=3n^5(3n^2+3n+1).
\]

That uses seed signs \(3/4,-1,1/4\),
vertical cancellation against \(U\) and
\(A_h U\), and the count of ordered pairs
\(\lvert a\rvert,\lvert b\rvert,\lvert a+b\rvert\le n\).
The elementary \(\mathcal R_\star\ge n/165888\)
uses this \(T_c\) as an input.

It was **not** checked by hand for general
\(n\). Evaluators reproduce it for
\(n=1,\dots,10\). Specialist review of
the all-\(n\) identity is pending.

### 2. Is \(\mathcal D_s(v_n)>0\) for every \(n\ge 1\)?

**Yes, by spectrum, not only by printed rows.**
Modes sit at
\(\lambda=n^2\lvert r\rvert^2+j^2\) with
\(\lvert r\rvert^2\in\{1,2,5\}\) and
\(\lvert j\rvert\le n\). For every
\(n\ge 1\) the values \(n^2\) and \(5n^2\)
both carry mass, so at least two
eigenvalues are occupied and
\(\mathcal D_s=Z-Y^2/X>0\).

### 3. Can normalization flip \(\mathcal R_\star\to\infty\)?

A global positive constant on the torus
measure cancels in
\(\mathcal R_\star=(T_c)_+^2/(\mathcal D_s E Y)\).
The written family already uses
\(U(nx,ny)\). Dropping that \(n\) is a
**different field**; it is not a
renormalization of \(v_n\). The lower
bound uses only positive majorants of
\(E,Y,\mathcal D_s\) and the claimed
\(T_c\ge 9n^7\). Those signs do not flip
under a positive measure factor.

### 4. If someone says \(v_n\) is “not a Navier–Stokes field”?

**Reply:** \(v_n\) is an instantaneous
admissible test field: real, mean-zero,
divergence-free, finite Fourier support,
\(\mathcal D_s>0\). It is **not** a
trajectory of the NSE. The kill is of a
boxed instantaneous estimate, not of
regularity.

---

## On exact-shell 9D

### 5. Where is the factor 3 proved?

**On this page**, in the weighted-count
section: plane–sphere incidence plus
AM-GM. It is not proved on a Ring or
Borromean page. Those counts are other
statements. Do not import them.

### 6. Hermitian estimate; which line uses conjugation?

For \(w_p\in\mathbb C^3\), \(p\cdot w_p=0\)
(\(p\) real; no conjugate in the
divergence constraint),

\[
\langle u,v\rangle=\sum_{j=1}^3\overline{u_j}v_j,
\qquad
\lvert\langle u,v\rangle\rvert^2\le\lvert u\rvert^2\lvert v\rvert^2.
\]

**Conjugation is only in \(\langle\cdot,\cdot\rangle\).**
After \(P_k\), the residual is
\(\zeta e_\perp\) with \(e_\perp\) real,
\(\lvert\zeta\rvert\le\gamma\lvert w_p\rvert\lvert w_q\rvert\).
No line sets \(\mathrm{Im}w_p=0\).

### 7. Divide by \(1-\beta/(4\alpha)\)?

**No.** Pair bounds are
\(\lvert\,\cdot\,\rvert\le\gamma\lvert w_p\rvert\lvert w_q\rvert\)
with \(\gamma=\sqrt{\beta(1-\beta/(4\alpha))}\).
\(K\) is
\(\beta\|\Pi_\beta B\|_2^2/(\alpha^2\|w\|_2^4)\).
Neither formula divides by
\(1-\beta/(4\alpha)\). The \(C=4/3\) form
divides by \(\sqrt{\beta}\), and
\(\beta>0\).

### 8. Half-symmetrization for complex coefficients?

For \(p\neq q\),
\(\sum_{p+q=k}(q\cdot w_p)w_q\) equals
half the symmetrization as an identity
of complex vectors. The involution
\((p,q)\leftrightarrow(q,p)\) does not
use conjugation. The bilinear \(q\cdot w_p\)
is \(\sum q_j(w_p)_j\) with \(q\) real.
The diagonal \(p=q\) is \(\beta=4\alpha\),
where \(\gamma=0\) and the pair bound is
already zero.

### 9. Meaning of \(\Pi_\beta\)?

**Exact lattice sphere**
\(\{\,k\in\mathbb Z^3:\lvert k\rvert^2=\beta\,\}\),
not a dyadic annulus of width 1.
The factor-3 count is a lattice count.

### 10. Both polarizations at \(p\), independent complex amplitudes?

**Yes.** \(w_p\) is already any vector in
the complex plane \(p^\perp\).
\(\lvert w_p\rvert^2\) is the sum of the
two polarization energies. The estimate
uses only \(\lvert w_p\rvert\lvert w_q\rvert\).

---

## On examples

### 11. \(K_{1,2}\) for \(w=(\sin y,\sin z,\sin x)\)

Normalized torus. Then
\(\|w\|_2^2=3/2\)
(each \(\int\sin^2=\tfrac12\)).

\[
(w\cdot\nabla)w
=
(\sin z\cos y,\;\sin x\cos z,\;\sin y\cos x).
\]

Divergence vanishes, so \(P=\mathrm{Id}\).
Each component has \(L^2\) mass \(1/4\), so
\(\|(w\cdot\nabla)w\|_2^2=3/4\).
Every frequency of the product has
\(\lvert k\rvert^2=2\)
(twelve complex modes:
\((0,\pm1,\pm1)\), \((\pm1,0,\pm1)\),
\((\pm1,\pm1,0)\)).
Thus \(\|\Pi_2 B(w,w)\|_2^2=3/4\),
\(\alpha=1\), \(\beta=2\), and

\[
K_{1,2}(w)
=
\frac{2\cdot(3/4)}{1\cdot(3/2)^2}
=
\frac{2}{3}.
\]

No script.

### 12. Any exact-shell field in the repo with \(K>1\)?

**Not in the recorded samples.**
Printed maxima are \(0.641\) and \(0.456\).
The three-shear identity is \(2/3\).
\(16/9\) is the algebraic ceiling of the
claimed majorant, not the sample max,
and not the number \(1\). Sharpness is
not claimed.

### 13. What would a counterexample look like?

One pair \((\alpha,\beta)\) with
\(\alpha>0\), \(0<\beta\le 4\alpha\),
and one finite list of
\(\widehat w(k)\in\mathbb C^3\) supported
on \(\lvert k\rvert^2=\alpha\),
\(k\cdot\widehat w(k)=0\),
\(\widehat w(-k)=\overline{\widehat w(k)}\),
\(w\neq 0\), such that
\(K_{\alpha,\beta}(w)>16/9\).

---

## On scope

### 14. One sentence a true \(4/3\) does not imply

A true \(4/3\) does not give multi-shell
control, does not repair unrestricted
\(\star\), and does not give a
continuation criterion.

### 15. Finite superposition of exact-shell fields, \(C\) depending only on the number of shells?

**No.** That would be a different
theorem. It is not claimed.

---

## On the machine

### 16. What does the named script prove, and what does it only read?

It **does not prove** \(K\le 16/9\).
As specified for this page, it checks
the growing-layer symbolic identities
against the evaluator and **reads** the
saved sweep summary. It does not run
the shell-count argument. A copy on
another branch also printed sample \(K\)
and sample counts; those prints are
not the proof.

### 17. If the script is deleted, is there a human-checkable proof?

**The claim is the written algebra**,
including §3 of the underlying proof
and the count on this page. The script
is not the proof. Deleting it does not
create a gap and does not close one.
Independent specialist review is still
pending.

---

## On replacement

### 18. First estimate \(v_n\) does not refute

\[
\|\Pi_\beta B(w,w)\|_2
\le
\frac43\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\qquad
Aw=\alpha w,\;\beta>0.
\]

\(v_n\) is multi-shell. It does not
touch this subclass bound.

### 19. Invariant along NS, or instantaneous on a subclass?

**Instantaneous, on the exact-shell
subclass.** Not an invariant of a
Navier–Stokes trajectory.

### 20. Which continuation criterion does it feed?

**None.** Not BKM, not
\(\int\lvert Au\rvert_2^2\,dt<\infty\),
not any other named continuation.
Ordinary NS stays open.
