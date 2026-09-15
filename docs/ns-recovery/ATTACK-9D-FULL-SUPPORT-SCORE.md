# Exact-shell 9D — claimed full-support bound (this book’s score)

**Date:** 13 September 2026  
**Other book:** [`docs/ATTACK-9D-FULL-SUPPORT-BOUND.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaugmented-r4-vorticity-f80e/docs/ATTACK-9D-FULL-SUPPORT-BOUND.md) on [PR #24](https://github.com/simons357/Ship_it_app/pull/24).

**CLAIMED:** written derivation available; internal checks passed;
independent specialist review pending. Numerical sweeps provide
consistency checks only.

An internal audit of the exact-shell argument reported no gap, and
the named verifier passed its symbolic checks. That is an internal
audit. This book does **not** stamp the algebra. Independent
specialist review remains pending.

**This is a different statement from unrestricted Lemma★.**
The unrestricted box is dead on the growing-layer family \(v_n\).
This page does not resurrect it.

If \(K\le 16/9\) holds, occupancy \(s\) is gone on a **single input
shell**. That is a written bound on exact-shell fields, not a sweep
maximum. The three-shear field then sits under a named ceiling, not
under a rumor.

**No as a regularity close.** A true \(4/3\) does not kill or repair
unrestricted ★. That box is already dead by the multi-shell family
\(v_n\). It does not give a continuation criterion and it does not
restore ★ \(\Rightarrow\) global regularity. Ordinary NS stays open.
Soft X silent. NS is not solved.

Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.
Do not cash \(0.456\), \(0.641\), or \(2/3\) as \(C_0\).

The meaningful next review is concrete: the weighted incidence
argument and the complex-polarization identity. Exact-shell scope
stays separated from unrestricted ★.

Specialist break answers: [`SPECIALIST-BREAK-QUESTIONS.md`](SPECIALIST-BREAK-QUESTIONS.md).
Items 5–10 and 14 are repeated below so the defense sits on this page.

Setup: [`docs/math/ns_attacks/ATTACK_9D_SETUP.md`](../math/ns_attacks/ATTACK_9D_SETUP.md).  
Floor: [`NINE-D-TWO-THIRDS.md`](NINE-D-TWO-THIRDS.md).  
Kill of ★: [`GROWING-LAYER-SCORE.md`](GROWING-LAYER-SCORE.md).

---

## Conventions

Normalized torus \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\) with
the locked \(L^2\) measure of this book
(\(\|e^{ik\cdot x}\|_2^2=1\)). \(K_{\alpha,\beta}(w)\) is defined
for \(\alpha>0\) and \(w\neq 0\) with \(Aw=\alpha w\). For
\(\beta>4\alpha\) no pairs occur.

---

## Claimed bound

For \(Aw=\alpha w\), the same Leray-projected \(B(w,w)=P[(w\cdot\nabla)w]\)
is claimed to satisfy

\[
\|\Pi_\beta B(w,w)\|_2
\le
\frac{4}{3}\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\qquad
\beta>0.
\]

Equivalently \(K_{\alpha,\beta}(w)\le 16/9\).
Both supports may grow. Each transverse polarization may have
independent complex coefficients. Optimality of the constant is
not claimed. The coefficient is claimed from algebra and geometry,
not from search results.

This does not control an arbitrary simultaneous finite-closer limit,
and it does not control a general multi-shell field. The growing-layer
family is multi-shell. No contradiction.

---

## Symmetrized interaction (the step this summary was missing)

For \(p+q=k\) on the specified shells, the claimed kernel estimate is

\[
\bigl|P_k\bigl[(q\cdot w_p)w_q+(p\cdot w_q)w_p\bigr]\bigr|
\le
\sqrt{\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)}\,|w_p|\,|w_q|.
\]

The in-plane components cancel after projection. The remaining
component is claimed to satisfy Cauchy–Schwarz even with independently
complex polarizations. Complete calculation: §3 of the PR #24 proof.

The ordered convolution equals half its symmetrization. Squaring
contributes \(1/4\); the weighted count contributes \(3\). Together

\[
\|\Pi_\beta B(w,w)\|_2^2
\le
\frac34\,\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)\|w\|_2^4.
\]

Hence \(K_{\alpha,\beta}(w)\le\frac34(\beta/\alpha)^2(1-\beta/(4\alpha))\le 16/9\)
for \(0<\beta\le 4\alpha\). The elementary max of
\((3/4)x^2(1-x/4)\) on \(x\in(0,4]\) is \(16/9\) at \(x=8/3\).
That calculus step is elementary. The incidence factor \(3\) and
the polarization identity are what a specialist must sign.

---

## Specialist questions 5–10 and 14

**5. Factor \(3\).** Written on the PR #24 exact-shell page as the
weighted lattice count. It is **not** the Ring Lemma and **not** a
Borromean / LP direction bound. Those prove a different count.
The factor \(3\) is still CLAIMED.

**6. Hermitian form, no reality.** For \(w_p\in\mathbb C^3\),
\(p\cdot w_p=0\) (complex bilinear, \(p\) real),

\[
k=\frac{\beta}{2\alpha}\,p+k_\perp,
\qquad
k\cdot w_p=k_\perp\cdot w_p,
\qquad
\lvert k\cdot w_p\rvert
\le
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}\,|w_p|.
\]

The last line is Hermitian Cauchy–Schwarz on \(\mathbb C^3\).
That is the line that uses conjugation (the modulus
\(|w_p|^2=w_p\cdot\overline{w_p}\)). The projector identity
\(\lvert P_k v\rvert^2=\lvert v\rvert^2-\lvert k\cdot v\rvert^2/\beta\)
is the same Hermitian modulus. Reindexing \(p\leftrightarrow q\)
uses no conjugation.

**7. Division by \(1-\beta/(4\alpha)\).** Nowhere. The factor
multiplies. At \(\beta=4\alpha\) it is zero and \(K=0\). \(K\) is
\(\beta\|\Pi_\beta B\|_2^2/(\alpha^2\|w\|_2^4)\). No hidden
normalization divides by that term.

**8. Half-symmetrization.** Exact for complex coefficients.
\(S=\sum_{p+q=k}(q\cdot w_p)w_q\) equals half the symmetrized
sum by \(p\leftrightarrow q\). Algebra, not reality.

**9. \(\Pi_\beta\).** Spectral projection onto the exact lattice
shell \(\{|k|^2=\beta\}\), \(k\in\mathbb Z^3\setminus\{0\}\).
Not a dyadic annulus. The count is lattice.

**10. Both polarizations, independent complex amplitudes.**
Claimed: \(w_p\in\mathbb C^3\) already holds both transverse
directions; the estimate uses \(|w_p|\). Specialist must sign
that. Not a second theorem.

**14. A true \(4/3\) does not imply** a repair of unrestricted ★,
a continuation criterion, or multi-shell control.

---

## Verifier (what the named script actually does)

PR #24 machine: `scripts/ns_attacks/verify_pr24_closure_review.py`.

It checks the symbolic identity and compares growing-layer
calculations with the evaluator. It reads the saved sweep summary.
It does **not** perform the shell-count experiments described on
the writeup.

This book’s independent checks: three-shear \(K_{1,2}=2/3\) on
[`scripts/ns_lemma_star_core.py`](../../scripts/ns_lemma_star_core.py);
growing-layer \(v_n\) on the same core. Those do not certify the
lattice count.

---

## Floor and historical numbers (consistency only)

| Object | \(K\) | Role |
|---|---|---|
| Three-shear \(w=(\sin y,\sin z,\sin x)\), \(\alpha=1\), \(\beta=2\) | **\(2/3\)** exact, public twelve-mode arithmetic | Write-up example. Floor \(\sup K\ge 2/3\). See break Q11. |
| Aligned 9B max | \(0.641\) at \((4,8)\) | Historical sweep. Consistency check only. |
| Grow-\(s\) max | \(0.456\) at \((16,32)\) | Historical sweep. Consistency check only. |
| Natural 9D growing I/O max | \(0.469\) at \((1,2)\) | Historical sweep. Consistency check only. |

Sweeps sit under \(16/9\approx 1.778\). That is consistency, not
an alternative path to support. Do not write “or a sweep shows
nothing near \(16/9\)” as a way to unclaim the bound.

---

## Status

| Item | This book |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Sweep max as \(C_0\) or as the ceiling | **NO.** Consistency only. |
| Three-shear \(K_{1,2}=2/3\) | Floor. Not the ceiling. Not \(C_0\). |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Written derivation available; internal checks passed; independent specialist review pending. |
| True \(4/3\) as a regularity close | **NO.** Does not repair ★. No continuation. |
| Unrestricted ★ | **NO.** Dead by \(v_n\). |
| Ordinary NS | **OPEN.** |
| Next review | Weighted incidence and the complex-polarization identity. |

**NS not solved.**
