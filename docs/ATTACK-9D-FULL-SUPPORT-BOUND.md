# Exact-shell 9D — claimed full-support bound

12 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for
\(Aw=\alpha w\);
remainder is occupancy \(s\);
the claimed bound removes that factor
on a single input shell.

**This is a different statement from unrestricted
Lemma★.** The unrestricted box is the growing-layer
family ([`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md)).
This page does not resurrect it.

If \(K\le 16/9\) holds, occupancy \(s\) is
gone on a **single input shell**. That is a
written bound on exact-shell fields, not a
sweep maximum. The three-shear field then
sits under a named ceiling, not under a
rumor.

**No as a regularity close.** A true
\(4/3\) does not kill or repair unrestricted
★. That box is already dead by the
multi-shell family \(v_n\). It does not
give a continuation criterion and it does
not restore ★ \(\Rightarrow\) global
regularity. Ordinary NS stays open.

Until a specialist signs the algebra, or a
sweep shows nothing near \(16/9\), the
word is still **CLAIMED**. Existing maxima
\(0.641\) and \(0.456\) are not near
\(16/9\approx 1.778\). That does not
unclaim the bound. Soft X silent.
NS is not solved.

Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.
Grow-\(s\) samples stay historical.
Do not cash \(0.456\) or \(0.641\) as \(C_0\).

Machine: `scripts/ns_attacks/verify_pr24_closure_review.py`.
Math pointer: [`math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md`](../math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md).
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

For \(\beta>4\alpha\) no pairs occur:
\(\lvert p+q\rvert\le 2\sqrt{\alpha}\).

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

The audit draws this count on shells
\((4,8)\), \((5,4)\), \((1,2)\) and prints
ratio \(\le 3\). That is a check, not the
lattice theorem.

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

Let \(x=\beta/\alpha\in(0,4]\). The elementary
maximum of \((3/4)x^2(1-x/4)\) is \(16/9\)
at \(x=8/3\). That is the claimed \(K\) bound.
\(C=4/3=\sqrt{16/9}\) is the constant in
\(\|\Pi_\beta B\|_2\le C\alpha\beta^{-1/2}E\).
Optimality is not claimed.

The specialist should check the kernel
calculation, the factor \(3/4\), and the
limiting-closer scope.

Random exact-shell fields on
\((4,8)\), \((5,4)\), \((9,4)\), \((16,32)\),
\((1,2)\) printed \(K\le 0.456<16/9\).
Aligned 9B \(K\approx 0.641<16/9\).
Grow-\(s\) max \(K\approx 0.456<16/9\).
Those numbers sit. They are not the proof.

---

## Status

| Item | Verdict |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Grow-\(s\) finite max as \(C_0\) | **NO.** Historical. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** \(C=4/3\). Occupancy \(s\) gone on one input shell if it holds. |
| Sweep max \(0.641\) / \(0.456\) as the ceiling | **NO.** Not the bound. |
| True \(4/3\) as a regularity close | **NO.** Does not repair ★. No continuation. |
| Unrestricted ★ | **NO.** Dead by \(v_n\). |
| Ordinary NS | **OPEN.** |
| Specialist sign of the algebra | **pending.** Soft X silent. |

NS not solved.
