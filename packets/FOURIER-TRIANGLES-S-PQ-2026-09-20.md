# Fourier triangles — pair vector \(S_{pq}\) (equation (1))

**20 September 2026 formula; seated 24 September 2026 on this book.**
Source note: `origin/cursor/fourier-triangles-audit-f37a:packets/FOURIER-TRIANGLES-AUDIT-2026-09-20.md`.
Machine: `scripts/fourier_triangle_s_pq.py`.

The 24 Sep Grok Heavily audit failed **G1.(1)** closed because this
formula / script was not on that disk. The formula was already
written in the 20 Sep note. This filing seats it. It does **not**
invent the missing \(\alpha=98\) / 432-realization stamp, a
BOTH-SIGNS family, or Schulze–Pillot citations.

**Not a closure theorem.** Ordinary NS is not solved. Soft X silent.
Does not alter the SBP / \(\phi/d\) / low-tail / sign-realizability
gates.

---

## Frame

For one interaction \(p+q=k\),

\[
a=|p|^2,\quad b=|q|^2,\quad c=|k|^2,\quad
s=p\cdot q=\frac{c-a-b}{2},\quad
\Delta=ab-s^2=|p\times q|^2.
\]

Noncollinear frame: \(e_0=k/\sqrt c\), \(e_1\) in the triangle plane
perpendicular to \(k\), \(e_2\) normal to that plane.

\[
p=x e_0+h e_1,\qquad q=y e_0-h e_1,
\]
\[
x=\frac{c+a-b}{2\sqrt c},\quad
y=\frac{c+b-a}{2\sqrt c},\quad
h=\sqrt{\Delta/c}.
\]

\[
u_p=A_1\frac{h e_0-x e_1}{\sqrt a}+A_2 e_2,
\qquad
u_q=B_1\frac{h e_0+y e_1}{\sqrt b}+B_2 e_2.
\]

Then \(q\cdot u_p=k\cdot u_p\) and \(p\cdot u_q=k\cdot u_q\).

---

## Boxed identities — EXACT

\[
S_{pq}=P_k[(q\cdot u_p)u_q+(p\cdot u_q)u_p].
\]

\[
\boxed{
S_{pq}
=
\frac{h(b-a)}{\sqrt{ab}}A_1B_1\,e_1
+
\sqrt c\,h
\left(
\frac{A_1B_2}{\sqrt a}+\frac{A_2B_1}{\sqrt b}
\right)e_2.
}
\tag{1}
\]

\[
\widehat B(u,u)(k)
=
iP_k\sum_{p+q=k}(q\cdot u_p)u_q
=
\frac i2\sum_{p+q=k}S_{pq}.
\tag{2}
\]

The factor \(1/2\) belongs to the ordered symmetrized sum.

If \(a=b=\alpha\) and \(c=\beta\),

\[
\boxed{
S_{pq}
=
\sqrt{\beta\left(1-\frac{\beta}{4\alpha}\right)}
(A_1B_2+A_2B_1)\,e_2.
}
\tag{3}
\]

The in-plane transverse component cancels. The normal component
generally remains.

\[
\boxed{
(P_kp)\cdot S_{pq}
=
\frac{b-a}{c}(k\cdot u_p)(k\cdot u_q).
}
\tag{4}
\]

Rechecked here in numpy (no sympy on this environment). The source
note’s sympy residual is **REPORTED**, not rebuilt.

---

## What this does not do

It does not obtain DA-NS-2 or theorem (17).
It does not stamp \(\alpha=98\), \(P=(3,5,-8)\), \(Q=(-8,3,5)\),
\(K=(-5,8,-3)\), or 432 ordered realizations.
It does not invent `hilbert_gram.relevant_primes`.
It does not seat a BOTH-SIGNS family.

**NS not solved.**
