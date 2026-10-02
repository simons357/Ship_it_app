# \(\|u\|_3\) budget — three gates

2 October 2026.
**Derivation, regularity value, novelty.
Not a new regularity mechanism.
Equation (17) remains OPEN.
NS not solved.**

Parent:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).
Code:
`scripts/ns_attacks/l3_budget_gates.py`.

Unaugmented NS on
\(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\).
Same convention as the 20 September
audit: \(A=-P\Delta\),
\(X=\lvert A^{1/2}u\rvert_2^2\),
\(Y=\lvert Au\rvert_2^2\),
\(\Lambda=Y/X\),
\(h_{K,N}=P_{\lvert k\rvert>K}u_N\).
No \(Q_1\). No \(\Phi\). No SND.
No Theorem H. Unrestricted
\(\star\) stays **KILLED**.
Lemma A and the first-variation
sign gate stay unaltered.

This page sends the
\(\lVert u\rVert_3\) form back
for the implication chain, not
as a close. Three gates, scored
separately.

---

## What is derived

For a real, mean-zero,
divergence-free field \(v\) on
the normalized torus — including
every Galerkin truncation — the
enstrophy pairing obeys

\[
\boxed{
\bigl\lvert\langle B(v,v),Av\rangle_{\mathbb R}\bigr\rvert
\le
C_S\,\lVert v\rVert_3\,Y(v).
}
\tag{L3-1}
\]

Here \(Y(v)=\lvert Av\rvert_2^2\)
and \(C_S=C_{6,2}C_{\mathrm{CZ}}\)
is the product of the Sobolev
constant \(W^{1,2}(\mathbb{T}^3)\to L^6\)
and the Calderón–Zygmund constant
\(\lVert\mathrm{Hess}\,v\rVert_2\le C_{\mathrm{CZ}}\lVert\Delta v\rVert_2\)
on divergence-free fields.
Both constants are independent of
the Galerkin cutoff.

Proof of (L3-1). Hölder with
\(\tfrac12=\tfrac13+\tfrac16\) gives

\[
\lVert(v\cdot\nabla)v\rVert_2
\le
\lVert v\rVert_3\,\lVert\nabla v\rVert_6.
\]

Sobolev on each first derivative,
then Calderón–Zygmund, gives

\[
\lVert\nabla v\rVert_6
\le
C_{6,2}\,\lVert\mathrm{Hess}\,v\rVert_2
\le
C_{6,2}C_{\mathrm{CZ}}\,\lVert\Delta v\rVert_2
=C_S\sqrt{Y(v)}.
\]

Leray is a contraction, so

\[
\bigl\lvert\langle B(v,v),Av\rangle\bigr\rvert
\le
\lVert(v\cdot\nabla)v\rVert_2\,\lVert Av\rVert_2
\le
C_S\,\lVert v\rVert_3\,Y(v).
\]

No \(Z\), no \(\lVert\nabla v\rVert_\infty\),
and no \(N\)-dependent factor enters.
The factor \(Y(v)\) is the viscous
term already present in the
enstrophy identity, not an extra
norm smuggled in after the fact.

Apply (L3-1) to \(v=h_{K,N}\).
Write \(\mathcal T(h)\) for the
full enstrophy pairing of \(h\)
and \(\mathcal T_{\mathrm{sc}}(h)\)
for the scalene part in (15) of
the audit. Monochromatic closed
triads contribute zero enstrophy
transfer. The remainder is the
seated repeated-radius term, so

\[
\mathcal T_{\mathrm{sc}}(h)
=\mathcal T(h)-\mathcal T_{\mathrm{rep}}(h),
\]

\[
\lvert\mathcal T_{\mathrm{sc}}(h)\rvert
\le
C_S\lVert h\rVert_3\,Y
+\lvert\mathcal T_{\mathrm{rep}}(h)\rvert.
\tag{L3-2}
\]

The audit already has
\(\lvert\mathcal T_{\mathrm{rep}}\rvert\le(\sqrt3/2)X\sqrt Y\).
Young with \(\varepsilon=\nu/4\) gives

\[
\frac{\sqrt3}{2}X\sqrt Y
\le
\frac{\nu}{8}Y+\frac{3}{2\nu}X^2.
\tag{L3-Y}
\]

Therefore

\[
\bigl[\mathcal T_{\mathrm{sc}}(h)-\nu Y/4\bigr]_+
\le
C_S\bigl[\lVert h\rVert_3-\tfrac{\nu}{8C_S}\bigr]_+Y
+\frac{3}{2\nu}X^2.
\]

Divide by \(X\) and integrate.
The quadratic remainder is
controlled by \(E'+2\nu X=0\):

\[
\int_0^T\frac{X_N}{\nu}\,dt
\le
\frac{E_0}{2\nu^2}.
\]

The leftover is the high-mode
\(L^3\) budget

\[
\boxed{
\mathcal S^{(3)}_{K,N}(T)
=\int_0^T
\bigl[\lVert h_{K,N}\rVert_3-c\nu\bigr]_+
\Lambda_N\,dt,
\qquad
c=\frac{1}{8C_S}.
}
\tag{L3-3}
\]

\[
\mathcal S_{K,N}(T)
\le
C_S\,\mathcal S^{(3)}_{K,N}(T)
+C(\nu,E_0).
\tag{L3-4}
\]

So (17) follows from

\[
\boxed{
\forall u_0\in C^\infty_{\mathrm{div}},\
\forall\nu>0,\quad
\exists K=K(u_0,\nu)<\infty:\quad
\forall T<\infty,\quad
\sup_N\mathcal S^{(3)}_{K,N}(T)<\infty.
}
\tag{L3-5}
\]

(L3-5) has **not** been proved.
It is the \(\lVert u\rVert_3\)
form of (17), not a replacement
for the geometry.

---

## Gate 1 — derivation

| Claim | Score |
|---|---|
| (L3-1) | **PASS.** Cutoff-uniform. Constant \(C_S=C_{6,2}C_{\mathrm{CZ}}\) named. No hidden \(Z\) or \(\lVert\nabla u\rVert_\infty\). |
| (L3-2)–(L3-4) | **PASS** as algebra on top of the seated \(\mathcal T_{\mathrm{rep}}\) bound and Young. |
| (L3-5) as an a priori NSE bound | **FAIL.** The integrand still carries \(\Lambda=Y/X\). That is a higher spectral moment. Removing it requires \(\lVert h\rVert_3\le c\nu\) uniformly, which is a smallness statement, not an energy-class bound. |

Bernstein on the high-pass field,

\[
\lVert h_K\rVert_3
\le
C\lVert h_K\rVert_{\dot H^{1/2}}
\le
C K^{-1/2}\sqrt{X},
\]

is true and cutoff-uniform. Using
it to force \(\lVert h_K\rVert_3\le c\nu\)
assumes a bound on \(X\). That is
the conclusion of (16). Circular.
Do not write it as a derivation of
(L3-5).

Gagliardo–Nirenberg

\[
\lVert u\rVert_3^4\le C\,EX
\]

is interpolation on \(\dot H^{1/2}\).
Substituting it into (L3-1) returns
an energy-class enstrophy estimate
of Foias–Temam type, \(X'\lesssim X^3/\nu^5\),
which does not close. It is not a
new \(L^3\) mechanism.

---

## Gate 2 — regularity value

Prodi–Serrin: \(u\in L^p_t L^q_x\) with
\(\frac2p+\frac3q\le 1\) and \(q>3\).
The endpoint \(q=3\) forces \(p=\infty\),
which is Escauriaza–Seregin–Šverák:
\(u\in L^\infty_t L^3_x\) implies
regularity.

| Resulting condition | Versus LPS / ESS | Mechanism? |
|---|---|---|
| \(\lVert u\rVert_3\le\nu/C_S\) uniformly | Small-data subset of ESS | No. Already classical. |
| \(u\in L^\infty_t L^3_x\) | Exactly ESS | No. ESS is the theorem. |
| \(u\in L^p_t L^3_x\) for finite \(p\) | Subcritical in time; does **not** close (L3-1) | No. Scaling forbids it. |
| (L3-5): \(\int[\lVert h_K\rVert_3-c\nu]_+\Lambda\,dt<\infty\) | Not an LPS class. Weighted by \(\Lambda\). Implied by ESS (because ESS \(\Rightarrow\) regularity \(\Rightarrow\) \(\Lambda\) bounded). The converse is (17) in other units. | **Reformulation, not a new mechanism.** |

A frequency-localized LPS criterion
already exists in the literature
(Cheskidov–Dai and related Besov
window statements). Those results
still *assume* a Serrin- or
Besov-class integral on a frequency
window. They do not produce a
cutoff-uniform NSE budget that
forces the high-mode \(L^3\) excess
to stay integrable without that
assumption.

The microscope asked for — a
budget that controls only the
growth-capable part of the \(L^3\)
behaviour without first assuming
an ESS-class quantity is finite —
is exactly (L3-5). It is not
proved. Bernstein does not prove
it. The Fourier-triangle geometry
does not prove it. It is (17)
after (L3-1).

---

## Gate 3 — novelty

(L3-1) is the standard Hölder plus
Sobolev estimate used in the
Ladyzhenskaya–Prodi–Serrin proofs
at the \(L^3\) endpoint. Equivalent
writings:

\[
\lvert b(v,v,Av)\rvert
\le
C\lVert v\rVert_3\,\lVert\nabla v\rVert_6\,\lVert\Delta v\rVert_2,
\]

\[
\lVert\nabla v\rVert_6\le C\lVert\Delta v\rVert_2.
\]

Textbook sources: Ladyzhenskaya;
Prodi (1959); Serrin (1962);
Constantin–Foias; Temam. The
endpoint regularity theorem is
Escauriaza–Seregin–Šverák (2003).
A \(\Lambda\)-weighted or
\(\dot H^{1/2}\) rewriting is
algebraically the same embedding,
not a different inequality.

(L3-5) is not in those papers as a
claimed a priori bound. It is also
not a new estimate: it is (17)
composed with (L3-1). No novelty
is asserted.

---

## Implication chain to attack

```
(L3-1)  classical, cutoff-uniform      PASS
        |
        v
(L3-2)  T_sc(h) ≤ C_S ||h||_3 Y + |T_rep|
        |
        v
(L3-4)  S ≤ C_S S^{(3)} + controlled
        |
        v
(L3-5)  sup_N S^{(3)}_{K,N}(T) < ∞     OPEN
        |
        |  equivalent, not weaker
        v
 (17)   sup_N S_{K,N}(T) < ∞           OPEN
        |
        v
 (16)   uniform X_N                    conditional
        |
        v
      continuation / Galerkin limit    standard
```

Attack (L3-5), not the algebra of
(L3-1). A proof of (L3-5) that
assumes \(\lVert u\rVert_3\in L^\infty_t\)
or a bound on \(X\) is ESS or
circular. A proof that only uses
\(E\), \(\nu\), and the seated
geometry would be the interesting
outcome. It is not written here.

---

## Lock

(L3-1) PASS, classical, no hidden
higher norm.
(L3-5) OPEN, equivalent to (17),
not an LPS class.
ESS already handles
\(L^\infty_t L^3_x\).
Bernstein plus (L3-1) does not
remove the need for (17).
No novelty. No close.
Lemma A unaltered.
Sign gate unaltered.
NS not solved.
