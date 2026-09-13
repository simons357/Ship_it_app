# Exact-shell 9D — full-support bound

12 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for \(Aw=\alpha w\);
remainder is occupancy \(s\);
this write removes that factor on one input shell.

**Different statement from unrestricted Lemma★.**
That box is killed by \(v_n\).
This page does not resurrect it.
Specialist review of the weighted count and
the polarization factor is pending.
NS is not solved.

Phone lock: [`../../ATTACK-9D-FULL-SUPPORT-BOUND.md`](../../ATTACK-9D-FULL-SUPPORT-BOUND.md).
Grow-\(s\) record: [`../../ATTACK-9D-GROW-S.md`](../../ATTACK-9D-GROW-S.md).
Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.

---

## Bound

For \(Aw=\alpha w\), the same Leray-projected
\(B(w,w)=P[(w\cdot\nabla)w]\) satisfies

\[
\|\Pi_\beta B(w,w)\|_2
\le
\frac{4}{3}\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\qquad
\beta>0.
\]

Equivalently \(K_{\alpha,\beta}(w)\le 16/9\), where

\[
K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
\]

Both supports may grow. Each transverse
polarization may have independent complex
coefficients. Optimality of \(4/3\) is not claimed.
For \(\beta>4\alpha\) no pairs occur.

This does not control an arbitrary simultaneous
finite-closer limit. It does not control a
general multi-shell field. The growing-layer
family is multi-shell. No contradiction.

---

## Weighted count

Let \(S\subset\{p:\lvert p\rvert^2=\alpha\}\),
\(a_p\ge 0\), and
\(c_k=\sum_{p+q=k}a_p a_q\). Then

\[
\sum_{\lvert k\rvert^2=\beta}c_k^2
\le
3\Bigl(\sum_{p\in S}a_p^2\Bigr)^2.
\]

Expand the square. A fixed distinct pair
\((p,r)\) can meet at most two outputs:
each output must obey \(\lvert k\rvert^2=\beta\)
and \(k\cdot p=k\cdot r=\beta/2\).
Two independent affine planes meet a sphere
in at most two points. The dependent distinct
case is \(r=-p\), impossible for \(\beta>0\).
Weighted AM-GM bounds the off-diagonal by
twice the squared mass. The diagonal is at
most once the squared mass.

The audit draws this count on
\((4,8)\), \((5,4)\), \((1,2)\) and prints
ratio \(\le 3\). That is a check, not the
lattice theorem.

---

## Polarization and \(K\)

The count plus the exact complex
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

The factor \(3/4\) is the claimed
polarization remainder. The specialist
must check the kernel calculation, that
factor, and the limiting-closer scope.
DA has not replaced that reading by a
proof assistant.

The three-shear field
\(w=(\sin y,\sin z,\sin x)\)
gives \(K_{1,2}=2/3\) by hand.
That raises the floor of \(\sup K\)
above aligned 9B \(0.641\).
Grow-\(s\) max \(K\approx 0.456\).
A sample is not the bound.
Do not cash \(2/3\) as \(C_0\) or as \(16/9\).
Phone: [`../../ATTACK-9D-TWO-THIRDS.md`](../../ATTACK-9D-TWO-THIRDS.md).

---

## Status

| Item | Verdict |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Grow-\(s\) finite max as \(C_0\) | **NO.** Historical. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Specialist pending. |
| Unrestricted ★ | **NO.** Other page. |
| Ordinary NS | **OPEN.** |
