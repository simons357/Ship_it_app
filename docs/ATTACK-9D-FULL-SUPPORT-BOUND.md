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
Vacuous if \(\beta>4\alpha\) (no pairs).

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
satisfies Cauchy–Schwarz even with
independently complex polarizations.
The complete calculation is §3 of the
underlying proof.

The ordered convolution equals half
its symmetrization. Squaring contributes
\(1/4\); the weighted count contributes
\(3\). Together,

\[
\|\Pi_\beta B(w,w)\|_2^2
\le
\frac34\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)\|w\|_2^4.
\]

That gives the stated \(K\le 16/9\).
Let \(x=\beta/\alpha\in(0,4]\). The
elementary maximum of
\((3/4)x^2(1-x/4)\) is \(16/9\) at
\(x=8/3\). Then
\(C=4/3=\sqrt{16/9}\) in
\(\|\Pi_\beta B\|_2\le C\alpha\beta^{-1/2}E\).

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
and the complex-polarization identity.
The exact-shell scope is correctly
separated from unrestricted ★.

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
| Complex-polarization identity | **CLAIMED.** Next review. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Written derivation available; internal checks passed; independent specialist review pending. |
| Sweep as a path to “supported” | **NO.** Consistency checks only. |
| True \(4/3\) as a regularity close | **NO.** Does not repair ★. No continuation. |
| Unrestricted ★ | **NO.** Dead by \(v_n\). |
| Ordinary NS | **OPEN.** |

NS not solved.
