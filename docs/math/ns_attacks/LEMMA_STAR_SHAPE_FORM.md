# Lemma★ — canonical shape form (exact lock)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Lock:** Truth only. **NS is NOT solved.** Lemma★ is **OPEN**. Locks formulas; does **not** prove ★.

**Reframe:** ★ is a **shape** statement, not a viscosity statement. Write \(u=av\); optimize size; the worst size cancels \(\nu\); the remainder is pure geometry.

Scripts: `scripts/ns_attacks/stokes_moments.py` — aliases \(E=\|v\|_2^2\), \(T_c=\mathcal{T}_c/T_c\), \(D_s=\mathcal{D}_s\), `ratio_R_star_shape`\(=\mathcal{R}_\star\).  
Legacy **`ratio_star`** \(=T_c/(E X\Lambda)\) is a **different** post-Young object (scales as \(1/a\)) — **not** the shape quotient.

Long expansions (Fourier sums, all \(\mathcal{D}_s\) forms, ordered / \(p+q+r=0\) triad \(T_c\)): [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md).  
Filename alias for desktop `LEMMA_STAR_CANONICAL.md`: [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md) → this file.

---

## Absolute Source of Truth (lock verbatim meaning)

For a nonzero, mean-zero, divergence-free field \(v\) on the normalized torus \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\), set
\[
A=-P\Delta,\qquad B(v,v)=P[(v\cdot\nabla)v],
\]
\[
E=\|v\|_2^2,\quad
X=\|A^{1/2}v\|_2^2,\quad
Y=\|Av\|_2^2,\quad
Z=\|A^{3/2}v\|_2^2,\qquad
\Lambda=\frac{Y}{X}.
\]
Define
\[
D_s=\mathcal{D}_s=Z-\frac{Y^2}{X}=\|(A-\Lambda)A^{1/2}v\|_2^2,\qquad
T_c=\mathcal{T}_c=-\langle B(v,v),A(A-\Lambda)v\rangle.
\]
The exact shape form of Lemma★ is:
\[
\boxed{
\exists\,C_{\mathrm{geom}}<\infty\quad
\forall\,v\in C^\infty_{\mathrm{div},0}(\mathbb{T}^3)\setminus\{0\}:\quad
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,D_s(v)\,\|v\|_2^2\,Y(v).
}
\]
Here \(T_c{}_+=\max(T_c,0)\). The constant depends only on the fixed geometry and normalization—not on amplitude, Fourier support, shell count or viscosity.

Equivalently, for \(D_s>0\),
\[
\boxed{
\sup_v
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}
<\infty.
}
\]
For \(D_s=0\), the field lies on one shell and \(T_c=0\) (vacuous — not a kill).

For any fixed \(0<\theta<1\), its equivalent viscosity packaging is
\[
T_c(u)\le\theta\nu D_s(u)+C_0(\theta)\nu^{-1}\|u\|_2^2 Y(u),\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta).
\]

**This is the full lemma.** Status: **OPEN**. The near-shell quantity \(K_{\alpha,\beta}\) tests only a **restricted limiting family** — it is **not** the full lemma (see Attack 9B).

---

## Notation aliases (code / older docs)

| SoT (this lock) | Older / script form | Code (`stokes_moments.py`) |
|-----------------|---------------------|----------------------------|
| \(D_s=\mathcal{D}_s\) | \(\mathcal{D}_s\) | `Ds` |
| \(E=\|v\|_2^2\) | \(\|v\|_2^2\) | `E` |
| \(T_c=\mathcal{T}_c\) | \(\mathcal{T}_c\) | `Tc` |
| \(\mathcal{R}_\star=(T_c)_+^2/(D_s\|v\|_2^2 Y)\) | same | **`ratio_R_star_shape`** |

**Equivalence lock (do not invent a second \(D_s\)):**
\[
D_s
=\mathcal{D}_s
=Z-\frac{Y^2}{X}
=Z-\Lambda Y
=\|(A-\Lambda)A^{1/2}v\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac{1}{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2
\ge 0,
\]
since \(\Lambda=Y/X\).

**Equivalence lock for \(T_c\):** with \(N=-\langle B,Av\rangle\), \(M=-\langle AB,Av\rangle\),
\[
T_c
=\mathcal{T}_c
=-\langle B(v,v),A(A-\Lambda)v\rangle
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]
Code: `Tc = M - Lam * N` (matches the inner-product form; \(A\) self-adjoint on the divergence-free subspace).

---

## Torus / Stokes setup

\[
v(x)=\sum_{k\in\mathbb{Z}^3\setminus\{0\}} v_k e^{ik\cdot x},\quad
k\cdot v_k=0,\quad
v_{-k}=\overline{v_k}.
\]
\[
\lambda_k=|k|^2,\qquad
A=-P\Delta,\qquad
(Av)_k=\lambda_k v_k.
\]

### Linear moments as Fourier sums

\[
\begin{aligned}
E&=\|v\|_2^2=\sum_k|v_k|^2,\\
X&=\|A^{1/2}v\|_2^2=\sum_k\lambda_k|v_k|^2,\\
Y&=\|Av\|_2^2=\sum_k\lambda_k^2|v_k|^2,\\
Z&=\|A^{3/2}v\|_2^2=\sum_k\lambda_k^3|v_k|^2,\\
\Lambda&=\frac{Y}{X}.
\end{aligned}
\]

### Two-eigenvalue shells

Shells \(\alpha,\beta\) with energies \(e_\alpha,e_\beta\):
\[
\mathcal{D}_s
=\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

---

## Nonlinear transfer (signed)

\[
\widehat{B(v,v)}_k
=i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q,\quad
P_k=I-\frac{k\otimes k}{|k|^2}.
\]
\[
T_k(v)
=-\mathrm{Re}\bigl(\widehat{B}_k\cdot\overline{v_k}\bigr)
=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

**CAUTION:** keep the **signed** complex triad sum (\(\mathrm{Im}\)). Do **not** replace \(\mathrm{Im}(\cdots)\) by absolute values.

\[
N=-\langle B,Av\rangle=\sum_k\lambda_k T_k,\quad
M=-\langle AB,Av\rangle=\sum_k\lambda_k^2 T_k,
\]
\[
T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

### Ordered / \(p+q+r=0\) triad form

Ordered form (\(k=p+q\)):
\[
T_c
=\sum_{\substack{p,q\\k=p+q}}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]
Equivalently, with \(p+q+r=0\) and \(k=-r\):
\[
T_c
=\sum_{p+q+r=0}
\lambda_{-r}(\lambda_{-r}-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v}_{-r})\bigr].
\]
**Cyclic permutations of \((p,q,r)\) are OK** (same signed geometry). **Absolute values are NOT** — never replace \(\mathrm{Im}\) by \(\lvert\mathrm{Im}\rvert\) or by product moduli.

HH→L channel splits can **identify** a mechanism; only the **complete** signed \(T_c\) enters the kill criterion for ★.  
**Attack 3 caveat:** the Bony HH split filters high-frequency **inputs** and does **not** restrict **output** to low frequencies — Attack 3 is **not** a strict HH→L map ([`ATTACK_3_BONY_HH_L.md`](./ATTACK_3_BONY_HH_L.md)). Genuine HH→L as an **output** subfamily in 9B requires \(\beta<\alpha\).

### Sign check (spectral drift)

From the Galerkin identities \(X'=-2\nu Y+2N\), \(Y'=-2\nu Z+2M\):
\[
\Lambda'=\frac{2}{X}\bigl(T_c-\nu\mathcal{D}_s\bigr).
\]

---

## Complete quotient \(\mathcal{R}_\star\)

When \(D_s(v)>0\), \(\|v\|_2>0\), \(Y(v)>0\):
\[
\mathcal{R}_\star(v)
=
\frac{(T_c(v)_+)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}.
\]
Lemma★ asserts \(\sup_v\mathcal{R}_\star<\infty\), with that supremum equal to \(C_{\mathrm{geom}}\) when finite. That bound is **OPEN**.

**Alignment with prior \(T_c^2\) form:** when \(T_c\ge0\), \((T_c)_+^2=T_c^2\). Kill cares about stretching \(T_c>0\); compression \(T_c<0\) gives \(\mathcal{R}_\star=0\) under the \((T_c)_+\) form.

Homogeneity (\(a>0\)) — **exact invariance**:
\[
T_c(av)=a^3 T_c(v),\quad
D_s(av)=a^2 D_s(v),\quad
\|av\|_2^2=a^2\|v\|_2^2,\quad
Y(av)=a^2 Y(v),\quad
\Lambda(av)=\Lambda(v),\quad
\mathcal{R}_\star(av)=\mathcal{R}_\star(v).
\]
Uniform Fourier dilation \(v(n\cdot)\) likewise leaves \(\mathcal{R}_\star\) **exactly invariant**.

### Viscosity packaging (derived, not primary)

Young / AM–GM on the amplitude line recovers, for fixed \(0<\theta<1\),
\[
T_c\le\theta\nu D_s+C_0(\theta)\nu^{-1}\|v\|_2^2\,Y,
\]
with \(C_{\mathrm{geom}}=4\theta\,C_0(\theta)\) (equivalently \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\)).

---

## Near-shell \(K_{\alpha,\beta}\) — restricted family only (NOT the full lemma)

Attack 9B defines
\[
K_{\alpha,\beta}
=\sup_{Aw=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
\]
and studies
\[
\lim_{\varepsilon\to0}\mathcal{R}_\star(w_\alpha+\varepsilon z_\beta)=K_{\alpha,\beta}(w)
\]
on the **exact-shell + infinitesimal closing** family.

**CRITICAL lock:** \(K_{\alpha,\beta}\) is a **restricted near-shell / limiting-family probe**. Bounding or sampling \(K\) is **not** equivalent to proving or falsifying the full Lemma★ over all smooth divergence-free mean-zero fields. The full lemma is the boxed shape inequality / \(\sup\mathcal{R}_\star<\infty\) above. See [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md).

---

## Kill / survive table

| Outcome | Verdict |
|---------|---------|
| Some shapes make \(\mathcal{R}_\star\) arbitrarily large | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(D_s=0\) (one Fourier shell) and \(T_c>0\) | **★ dead** on that field (contradicts SoT \(T_c=0\) on one shell if it occurs) |
| Pure single shell, both sides vanish (\(T_c=0=D_s\)) | vacuous — not a kill; matches SoT |
| Live kill attempt | almost-single-shell / near two-shell / exact-shell + closing (9B \(K_{\alpha,\beta}\) **restricted family**); designed \(\Theta(m^2)\) locked-phase (9D, stub) |
| AP packet fan (9A) / fixed-gap natural ensemble (9C) | **Did not kill ★** — 9C: \(\mathcal{R}_\star\) falls \(0.11\to 0.031\), not \(m^{1/2}\) |
| Every shape has \(\mathcal{R}_\star\le K\) | that number is ★ (up to \(4\theta\)) — **not proved** |
| A list of fields with small \(\mathcal{R}_\star\) | **NOT** that number — those shapes did not kill it |
| Finite sample \(K_{\alpha,\beta}\) | **NOT** a proof of ★ — restricted family only |
| Failure to find a numerical counterexample | does **NOT** close the kill lane — falsification **LIVE**, proof **LIVE** |

**Retired false claim:** “The kill lane is closed.” — **FALSE.**

**Do not confuse** with post-Young \(R_{\mathrm{post}}=T_c/(\|v\|_2^2 Y)\) (scales as \(1/a\)) or pre-Young \(R_{\mathrm{pre}}=T_c/(\|v\|_2\,X\Lambda)\).

**Archive:** Route N / Q6 / LP-shell floors → [`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/) (**NOT Lemma★**).

## What a proof would have to be

Reason from how **signed** triads add that stretching cannot get large unless spectrum also spreads or phases cancel. That reason is **NOT written**.

**NS not solved.** Lemma★ **OPEN**. Kill lane **LIVE**. Locks formulas; does not prove ★.

## Related

- Exact formulas (long expansions): [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md)
- Canonical alias: [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md)
- Status board: [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)
- Correct record: [`ATTACK_8_CORRECT_RECORD.md`](./ATTACK_8_CORRECT_RECORD.md)
- Packet fan (9A, did not kill ★): [`ATTACK_9_PACKET_FAN.md`](./ATTACK_9_PACKET_FAN.md), [`ATTACK_9A_AP_PACKET_FAILURE.md`](./ATTACK_9A_AP_PACKET_FAILURE.md)
- Exact-shell closing (9B, **restricted \(K_{\alpha,\beta}\) probe**): [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md)
- Fixed-gap spheres (9C, **not** a kill): [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md)
- Pack locator: [`FIVE_LANE_PACK_LOCATOR.md`](./FIVE_LANE_PACK_LOCATOR.md) — https://github.com/simons357/Ship_it_app/pull/48
- Next falsifier (9D stub): [`ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](./ATTACK_9D_THETA_M2_LOCKED_PHASE.md)
- Synthesis: [`ATTACK_SYNTHESIS_SIMULTANEOUS.md`](./ATTACK_SYNTHESIS_SIMULTANEOUS.md)
- Archive (NOT ★): [`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/), [`../ARCHIVE_NOT_LEMMA_STAR.md`](../ARCHIVE_NOT_LEMMA_STAR.md)
- Probe / harness: `scripts/ns_attacks/stokes_moments.py`, `attack5_route2_kill.py`, `lemma_star_near_shell_search.py`, `attack9_packet_fan.py`, `attack9b_exact_shell_K.py`
