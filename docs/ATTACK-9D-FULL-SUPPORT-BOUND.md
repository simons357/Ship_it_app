# Exact-shell 9D — claimed full-support bound

13 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for
\(Aw=\alpha w\);
remainder is occupancy \(s\);
the claimed bound removes that factor
on a single input shell.

**This is a different statement from unrestricted
Lemma★.** The unrestricted box is killed by the
growing-layer family
([`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md)).
This page does not resurrect it.

**CLAIMED:** written derivation available;
internal checks passed; independent
specialist review pending. Numerical
sweeps provide consistency checks only.

An internal audit of the underlying
proof found no gap in the exact-shell
argument. The named verifier also
passes its symbolic checks. That is
an internal audit. It is not an
outside specialist sign.

**No as a regularity close.** A true
\(4/3\) does not kill or repair unrestricted
★. That box is already dead by the
multi-shell family \(v_n\). It does not
give a continuation criterion and it does
not restore ★ \(\Rightarrow\) global regularity.
Ordinary NS stays open. Soft X silent.

Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.
Do not cash \(0.456\), \(0.641\), or
\(2/3\) as \(C_0\).

Write-up example: \(K_{1,2}=2/3\) on
\(w=(\sin y,\sin z,\sin x)\).
This is the write-up example.
If \(K\le 16/9\) holds, occupancy \(s\)
is gone: a written bound on exact-shell
fields, not a sweep maximum.
Floor, not the ceiling.
[`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md).

Underlying proof: [`math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md`](math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md)
(the symmetrized estimate is §3).
Machine: `scripts/ns_attacks/verify_pr24_closure_review.py`.
Grow-\(s\) record (historical): [`ATTACK-9D-GROW-S.md`](ATTACK-9D-GROW-S.md).

The verifier checks the symbolic
identity and compares growing-layer
calculations with the evaluator. It
reads the saved sweep summary. It
does **not** perform the 9B / grow-\(s\)
shell-count experiments recorded on
those pages.

---

## Conventions

Normalized torus
\(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\)
with the locked Plancherel measure of
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
\(K_{\alpha,\beta}\) is defined only for
\(\alpha>0\) and \(w\neq 0\).

**Admissible \((\alpha,\beta)\).** Input
shell \(\alpha>0\). Output shell
\(\beta>0\). Lattice pairs require
\(\lvert p+q\rvert\le 2\sqrt{\alpha}\), so
\(\beta\le 4\alpha\). If \(\beta>4\alpha\)
the sum is empty and the bound is
vacuous. The closed constraint set used
for the \(16/9\) maximum is therefore
\[
\alpha>0,\qquad
0<\beta\le 4\alpha,
\qquad\text{equivalently}\qquad
x=\beta/\alpha\in(0,4].
\]

Pairing on polarizations: \(k\in\mathbb{Z}^3\)
is real, so \(k\cdot w=\sum k_i w_i\)
coincides with the Hermitian inner
product \(\langle k,w\rangle\) on
\(\mathbb{C}^3\). Cauchy–Schwarz is
\(\lvert\langle u,v\rangle\rvert\le\|u\|_2\|v\|_2\)
for that Hermitian product. It does
not require real or aligned
polarizations.

\[
K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
\]

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

The coefficient comes from algebra and
geometry, not from search results.

This does not control an arbitrary simultaneous
finite-closer limit, and it does not control
a general multi-shell field. The growing-layer
family is multi-shell. No contradiction.

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
returns occupancy.

---

## Crucial step — symmetrized interaction

For \(p+q=k\) on the specified shells,

\[
\bigl\lvert
P_k\!\bigl[(q\cdot w_p)w_q+(p\cdot w_q)w_p\bigr]
\bigr\rvert
\le
\sqrt{\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)}
\,|w_p|\,|w_q|.
\]

The in-plane components cancel after
projection. The remaining component
is estimated by Hermitian
Cauchy–Schwarz on \(\mathbb{C}^3\).
Independent complex polarizations are
allowed because the inner product is
\(\langle u,v\rangle=\sum_i \overline{u_i}v_i\);
the inequality does not use a real
alignment. The complete calculation is
§3 of the underlying proof.

The ordered convolution equals half
its symmetrization. Squaring contributes
\(1/4\); the weighted count contributes
\(3\). Together,

\[
\|\Pi_\beta B(w,w)\|_2^2
\le
\frac34\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)\|w\|_2^4.
\]

---

## One-variable maximum (redo by hand)

From the last display and the definition
of \(K\), on the admissible set
\(x=\beta/\alpha\in(0,4]\),

\[
K_{\alpha,\beta}(w)
\le
\frac34 x^2\Bigl(1-\frac{x}{4}\Bigr)
=:f(x).
\]

Endpoints: \(f(x)\to 0\) as \(x\to 0^+\),
and \(f(4)=0\). Interior critical points:

\[
f'(x)=\frac34 x\Bigl(2-\frac{3x}{4}\Bigr)=0
\quad\Rightarrow\quad
x=\frac83
\]

(\(x=0\) is not interior). The point
\(x=8/3\) lies in \((0,4]\). Then

\[
f\Bigl(\frac83\Bigr)
=
\frac34\cdot\frac{64}{9}\cdot\Bigl(1-\frac{2}{3}\Bigr)
=
\frac34\cdot\frac{64}{9}\cdot\frac13
=
\frac{16}{9}.
\]

So \(\sup f=16/9\) on the closed
constraint set above. Then
\(C=4/3=\sqrt{16/9}\) in
\(\|\Pi_\beta B\|_2\le C\alpha\beta^{-1/2}E\).
This is the step an independent
reviewer should redo by hand. It is
not a search result. The claimed bound
is this elementary maximum, not a
statement that \(x=8/3\) is attained
on the integer lattice.

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

Expand the square. A fixed pair \((p,r)\)
contributes only at outputs \(k\) that satisfy
\(\lvert k\rvert^2=\beta\) and
\(k\cdot p=k\cdot r=\beta/2\).

- If \(p\) and \(r\) are linearly independent,
  two affine planes meet the sphere
  \(\lvert k\rvert^2=\beta\) in at most two points.
- If \(r=\lambda p\) and \(\lvert p\rvert^2=\lvert r\rvert^2=\alpha\),
  then \(\lambda=\pm 1\). The case \(r=p\) is
  the diagonal. The case \(r=-p\) forces
  \(\beta=0\), which is excluded.

So a fixed distinct pair meets at most two
outputs. Weighted AM-GM bounds the
off-diagonal contribution by twice the
squared mass. The diagonal is at most once
the squared mass. Total factor \(3\).

**Claimed proposition — two-plane incidence.**
The two bullets above. Isolated so a
specialist can accept or break them by
naming one pair that meets three outputs
on a shell \(\beta>0\). Isolating is not
certification. Internal audit found no
gap. Independent specialist review of
this incidence argument, and of the
complex-polarization identity, is the
meaningful next check.

---

## Write-up example and historical numbers

The named example is the three-shear field
\(w=(\sin y,\sin z,\sin x)\):
exact-shell \(\alpha=1\), output \(\beta=2\),
twelve outputs each of size \(1/16\),
so \(K_{1,2}=2/3\) by hand.
That proves \(\sup K\ge 2/3\). It does
not prove the ceiling.
[`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md).

Historical consistency checks (not the bound):

| Source | Number | Role |
|---|---|---|
| Three-shear write-up | \(K_{1,2}=2/3\approx 0.667\) | Floor. Pointable interaction. |
| Aligned 9B search | \(\approx 0.641\) at \((4,8)\) | Search max. |
| Grow-\(s\) (seed 1390) | \(\approx 0.456\) at \((16,32)\) | Search max. |

\(2/3\) clears both search maxima and
sits well under \(16/9\approx 1.778\).
Those numbers sit. They are not the proof.

---

## Next review

Verify the weighted incidence argument
and the complex-polarization identity
(Hermitian CS after the in-plane cancel).
Redo the one-variable maximum of
\(f(x)=(3/4)x^2(1-x/4)\) on \((0,4]\)
by hand. The exact-shell scope is
correctly separated from unrestricted ★.

---

## Status

| Item | Verdict |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Grow-\(s\) / aligned 9B finite max as \(C_0\) | **NO.** Historical consistency. |
| Three-shear \(K=2/3\) as \(C_0\) | **NO.** Write-up example. Floor only. |
| Internal audit of the exact-shell argument | **Passed.** No gap found. Not an outside sign. |
| Named verifier symbolic checks | **Passed.** Not a proof assistant. |
| Two-plane incidence as a theorem | **CLAIMED.** Isolated. Next review. |
| Complex-polarization identity | **CLAIMED.** Hermitian CS after in-plane cancel. Next review. |
| Admissible \((\alpha,\beta)\) / \(x\in(0,4]\) | **Stated.** \(\beta\le 4\alpha\) from \(\lvert p+q\rvert\le 2\sqrt{\alpha}\). |
| One-variable max \(f(8/3)=16/9\) | **Written.** Redo by hand. Not a lattice attainment. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Written derivation available; internal checks passed; independent specialist review pending. |
| Sweep as a path to “supported” | **NO.** Consistency checks only. |
| True \(4/3\) as a regularity close | **NO.** Does not repair ★. No continuation. |
| Unrestricted ★ | **NO.** Dead by \(v_n\). |
| Ordinary NS | **OPEN.** |

NS not solved.
