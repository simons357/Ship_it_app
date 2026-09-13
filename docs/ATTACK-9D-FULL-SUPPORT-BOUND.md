# Exact-shell 9D — claimed full-support bound

12 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for
\(Aw=\alpha w\);
remainder is occupancy \(s\);
the claimed bound removes that factor
on a single input shell.

**This is a different statement from unrestricted
Lemma★. That box is killed by the growing-layer
family. This page does not resurrect it.**

Specialist review of the weighted sphere count
and the polarization identity is pending.
Computational samples sit under \(16/9\).
A sample is not the bound. Soft X silent.
NS is not solved.

Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.
Grow-\(s\) samples stay historical.
Do not cash \(0.456\), \(0.641\), or
\(2/3\) as \(C_0\).
The write-up example is the
three-shear field
\(w=(\sin y,\sin z,\sin x)\):
one line, \(K_{1,2}=2/3\) by hand.
That is a floor of \(\sup K\).
It is not \(16/9\). A random-search
table is not the example.
[`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md).

Derivation: [`math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md`](math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md).
Machine: `scripts/ns_attacks/verify_pr24_closure_review.py`.
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

For \(\beta>4\alpha\) no pairs occur.

This does not control an arbitrary simultaneous
finite-closer limit, and it does not control
a general multi-shell field. The growing-layer
family is multi-shell. No contradiction.

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

After expanding the square, a fixed distinct
pair \((p,r)\) can meet at most two outputs:
each output must obey
\(\lvert k\rvert^2=\beta\) and
\(k\cdot p=k\cdot r=\beta/2\).
Two independent affine planes meet a sphere
in at most two points. The dependent distinct
case is \(r=-p\), impossible for \(\beta>0\).
Weighted AM-GM bounds the off-diagonal by
twice the squared mass. The diagonal is at
most once the squared mass.

The audit draws this count on shells
\((4,8)\), \((5,4)\), \((1,2)\) and prints
ratio \(\le 3\). That is a check, not the
lattice theorem.

---

## Polarization and the \(K\) form

The review combines the count with the exact
complex polarization cancellation to get

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

The specialist should check the kernel
calculation, the factor \(3/4\), and the
limiting-closer scope. DA has not replaced
that reading by a proof assistant.

The write-up example is the
three-shear field: one line,
\(K_{1,2}=2/3\) by hand and on the
live evaluator. That clears
aligned 9B \(0.641\) and grow-\(s\)
\(0.456\). It sits well under
\(16/9\). Random exact-shell
samples on \((4,8)\), \((5,4)\),
\((9,4)\), \((16,32)\), \((1,2)\)
printed \(K\le 0.456\). Those are
sweep maxima. The hand field is
the example. None of them is the
\(16/9\) proof. To move \(16/9\)
from CLAIMED to supported still
needs the closed-form derivation
or a sweep that shows nothing
gets near \(16/9\).

---

## Status

| Item | Verdict |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Grow-\(s\) finite max as \(C_0\) | **NO.** Historical. |
| Three-shear \(K=2/3\) as \(C_0\) | **NO.** Write-up example. Floor only. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Specialist pending. |
| Unrestricted ★ | **NO.** Other page. |
| Ordinary NS | **OPEN.** |
