# Exact-shell 9D — claimed full-support bound

12 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for \(Aw=\alpha w\);
remainder is occupancy \(s\);
the claimed bound removes that factor
on a single input shell.

**This is a different statement from unrestricted
Lemma★.** The unrestricted box is killed by the
growing-layer family. This page does not
resurrect it. Specialist review of the
weighted count, the kernel step, and the
polarization factor is pending.
NS is not solved.

Phone lock: [`../../ATTACK-9D-FULL-SUPPORT-BOUND.md`](../../ATTACK-9D-FULL-SUPPORT-BOUND.md).
Grow-\(s\) record: [`../../ATTACK-9D-GROW-S.md`](../../ATTACK-9D-GROW-S.md).
Write-up example: [`../../ATTACK-9D-TWO-THIRDS.md`](../../ATTACK-9D-TWO-THIRDS.md).
Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.

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

Equivalently \(K_{\alpha,\beta}(w)\le 16/9\), where

\[
K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
\]

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

This does not control an arbitrary simultaneous
finite-closer limit, and it does not control
a general multi-shell field. The growing-layer
family is multi-shell. No contradiction.

If \(K\le 16/9\) holds, occupancy \(s\)
is gone on a single input shell.
That is a written bound on exact-shell
fields, not a sweep maximum.
The three-shear field then sits under
a named ceiling, not under a rumor.
No as a regularity close. A true
\(4/3\) does not restore
★ \(\Rightarrow\) global regularity.
Until a specialist signs, or a sweep
shows nothing near \(16/9\), the word
is still CLAIMED.

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
Because \(w_p\perp p\) (complex bilinear
\(p\cdot w_p=0\)) and \(k_\perp\) is real,
\[
\lvert k\cdot w_p\rvert
\le
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}\,|w_p|.
\]
This is Cauchy–Schwarz on \(\mathbb{C}^3\)
for the standard Hermitian inner product.
It saturates when \(w_p\) is complex-parallel
to \(k_\perp\). Independent complex
polarizations do not weaken this one-mode
bound. The claimed \(3/4\) is a later
step on the sum, not this CS.
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

### Claimed proposition — two-plane incidence

The two bullets above. Isolated so a
specialist can accept or break them by
naming one pair that meets three outputs
on a shell \(\beta>0\). Isolating is not
certification.

**Status: CLAIMED.** Isolated so a
specialist can accept it or break it
by naming one pair \((p,r)\) that meets
three outputs on a shell \(\beta>0\).
Isolating the proposition is not a
proof assistant.

The audit draws this count on
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

The write-up example is the
three-shear field
\(w=(\sin y,\sin z,\sin x)\):
one line, \(K_{1,2}=2/3\) by hand.
That raises the floor of \(\sup K\)
above aligned 9B \(0.641\).
Random exact-shell fields on
\((4,8)\), \((5,4)\), \((9,4)\), \((16,32)\),
\((1,2)\) printed \(K\le 0.456<16/9\).
Grow-\(s\) max \(K\approx 0.456<16/9\).
Those numbers sit. They are not the proof.
Do not cash \(2/3\) as \(C_0\) or as \(16/9\).
To move \(16/9\) from CLAIMED to
supported still needs the closed-form
or a near-ceiling sweep. Neither sits.

---

## Status

| Item | Verdict |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Grow-\(s\) finite max as \(C_0\) | **NO.** Historical. |
| Three-shear \(K=2/3\) as \(C_0\) | **NO.** write-up example. Floor only. |
| Two-plane incidence as a theorem | **NO.** Isolated. Still CLAIMED. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** \(C=4/3\). Occupancy \(s\) gone on one input shell if it holds. |
| Cubic max of the claimed envelope | **YES** as calculus at \(x=8/3\). **NO** as a proof of the envelope. |
| Live audit as \(16/9\) | **NO.** Internal check. Not independent review. |
| Reconstructed \(3/4=(1/2)^2\cdot 3\) | **NO.** Live \(B\) has no extra \(1/2\). |
| Sweep max \(0.641\) / \(0.456\) as the ceiling | **NO.** Not the bound. |
| True \(4/3\) as a regularity close | **NO.** Does not repair ★. No continuation. |
| Unrestricted ★ | **NO.** Dead by \(v_n\). |
| Ordinary NS | **OPEN.** |
| Specialist sign of the algebra | **pending.** Soft X silent. |

NS not solved.
