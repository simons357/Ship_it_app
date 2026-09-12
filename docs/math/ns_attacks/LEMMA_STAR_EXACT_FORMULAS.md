# Lemma★ — exact formulas (shape form)

**Status:** definitions / identities only. Unrestricted \(\sup\mathcal{R}_\star<\infty\) **KILLED** by \(v_n\). Replacement closure **OPEN**. **NS not solved.**

**Date:** 2026-09-10  
**Branch:** `cursor/unaugmented-r4-vorticity-f80e` (identities from PR #48 / five-lane lock)  
**Desktop source:** `/Users/jonathansimons/Desktop/Harmonic Universe Book/LEMMA_STAR_EXACT_FORMULAS.md` was **not mounted** in this environment; formulas reconstructed from the on-branch SoT lock + companion outline (LaTeX norms restored as \(\|\cdot\|_2\), missing equals restored).

**This note does not prove ★.** It locks the exact identities used by numerics and by the claim docs.

| Role | File |
|------|------|
| **Canonical boxed claim** (+ four corrections + viscosity packaging) | [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md) |
| **Exact formulas** (this file) | definitions, \(D_s\) forms, triad / \(T_c\), \(\mathcal{R}_\star\), \(\Lambda'\), aligned near-shell limit |
| Historical formula lock | [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md) — not a second claim |
| Older attempt (archive) | [`LEMMA_STAR_OLDER_ATTEMPT_ARCHIVE.md`](./LEMMA_STAR_OLDER_ATTEMPT_ARCHIVE.md) |
| Code lock | `scripts/ns_attacks/stokes_moments.py` (`Tc = M - Lam * N`, **`ratio_R_star_shape`**) |
| Independent core (does **not** replace the live Stokes file) | `scripts/ns_attacks/ns_lemma_star_core.py` — direct triad sum, two \(D_s\) formulas raise on mismatch |

---

## 1. Setup and linear moments

On the normalized torus \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\), take a nonzero mean-zero divergence-free field
\[
v(x)=\sum_{k\in\mathbb{Z}^3\setminus\{0\}} v_k e^{ik\cdot x},\qquad
k\cdot v_k=0,\qquad
v_{-k}=\overline{v_k}.
\]
Stokes operator and bilinear term:
\[
A=-P\Delta,\qquad
(Av)_k=\lambda_k v_k,\qquad
\lambda_k=|k|^2,\qquad
B(v,v)=P[(v\cdot\nabla)v].
\]

Linear moments (SoT / code):
\[
\begin{aligned}
E&=\|v\|_2^2=\sum_k|v_k|^2,\\
X&=\|A^{1/2}v\|_2^2=\sum_k\lambda_k|v_k|^2,\\
Y&=\|Av\|_2^2=\sum_k\lambda_k^2|v_k|^2,\\
Z&=\|A^{3/2}v\|_2^2=\sum_k\lambda_k^3|v_k|^2,\\
\Lambda&=\frac{Y}{X}.
\end{aligned}
\]

---

## 2. All equivalent forms of \(D_s\) (alias \(\mathcal{D}_s\))

**Do not invent a second \(D_s\).** Older docs writing \(\mathcal{D}_s=Z-\Lambda Y\) mean the **same** object:
\[
\begin{aligned}
D_s
&=\mathcal{D}_s
=Z-\frac{Y^2}{X}
=Z-\Lambda Y
=\|(A-\Lambda)A^{1/2}v\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac{1}{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2
\ge 0.
\end{aligned}
\]
Code: `Ds`.

### Two-shell closed form

On exactly two eigenvalue shells \(\alpha,\beta\) with shell energies \(e_\alpha,e_\beta\):
\[
D_s
=\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

**Vacuous case:** \(D_s=0\) \(\Leftrightarrow\) support on a single Fourier shell \(\Rightarrow\) \(T_c=0\) (not a kill).

---

## 3. Nonlinear \(B\), signed \(T_k\), moments \(N,M\), and \(T_c\)

Fourier bilinear form:
\[
\widehat{B(v,v)}_k
=i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q,\qquad
P_k=I-\frac{k\otimes k}{|k|^2}.
\]

Signed modal transfer (**keep \(\mathrm{Im}\)**; never replace by absolute values):
\[
T_k(v)
=-\mathrm{Re}\bigl(\widehat{B}_k\cdot\overline{v_k}\bigr)
=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Energy conservation of the bilinear form on mean-zero fields:
\[
\sum_k T_k=0.
\]

Centered moment transfers:
\[
N=-\langle B,Av\rangle=\sum_k\lambda_k T_k,\qquad
M=-\langle AB,Av\rangle=\sum_k\lambda_k^2 T_k.
\]

Inner-product / spectral form of the centered drift (because \(A\) is self-adjoint on the divergence-free subspace):
\[
\begin{aligned}
T_c
&=-\langle B(v,v),A(A-\Lambda)v\rangle
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\end{aligned}
\]
Code: `Tc = M - Lam * N`.

---

## 4. Ordered triad expansion of \(T_c\)

Write the sum over **ordered** Fourier triples \((p,q,k)\) with \(p+q=k\) (each ordered pair \((p,q)\) counted once; \(k\) determined):
\[
T_c
=\sum_{\substack{p,q\\k=p+q}}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]
Equivalently (same signed sum):
\[
T_c
=\sum_{p+q=k}\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

**Caution (signed triads):** HH→L channel splits may **identify** a mechanism; only the **complete** signed \(T_c\) enters the kill criterion for ★. Do **not** replace \(\mathrm{Im}(\cdots)\) by \(\lvert\cdot\rvert\). Attack 3’s Bony HH split filters high-frequency **inputs** and does **not** restrict **output** to low frequencies ([`ATTACK_3_BONY_HH_L.md`](./ATTACK_3_BONY_HH_L.md)).

---

## 5. Boxed shape quotient \(\mathcal{R}_\star\)

When \(D_s(v)>0\), \(\|v\|_2>0\), \(Y(v)>0\):
\[
\boxed{
\mathcal{R}_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}
}
\]
with \(T_c{}_+=\max(T_c,0)\). Canonical code name: **`ratio_R_star_shape`**. Alias `ratio_R_star` → same. Legacy `ratio_star` \(=T_c/(E X\Lambda)\) is a **different** post-Young object (scales as \(1/a\)) — **not** \(\mathcal{R}_\star\).

### Oddness: \((T_c)_+^2\) vs \(T_c^2\) when testing all fields

\[
T_c(-v)=-T_c(v),
\qquad
D_s(-v)=D_s(v),\qquad
E(-v)=E(v),\qquad
Y(-v)=Y(v).
\]
A coded probe with \((T_c)_+\) reports \(\mathcal{R}_\star=0\) when \(T_c<0\). That is the viscous remainder (only stretching is fought). It is **not** a reason to discard the shape. Reverse the field and the same geometry stretches. A universal bound on \((T_c)_+^2\) over all fields is equivalent to a universal bound on \(T_c^2\). When \(T_c\ge 0\), \((T_c)_+^2=T_c^2\).

### Exact invariances (homogeneity)

For \(a>0\):
\[
\begin{aligned}
T_c(av)&=a^3 T_c(v),&
D_s(av)&=a^2 D_s(v),&
\|av\|_2^2&=a^2\|v\|_2^2,\\
Y(av)&=a^2 Y(v),&
\Lambda(av)&=\Lambda(v),&
\mathcal{R}_\star(av)&=\mathcal{R}_\star(v).
\end{aligned}
\]
Uniform Fourier dilation \(v(n\cdot)\) likewise leaves \(\mathcal{R}_\star\) **exactly invariant**.

**Retired false claim:** “Amplitude or frequency makes the ratio smaller” — **FALSE for \(\mathcal{R}_\star\)** (older non-optimized budget).

---

## 6. Sign check \(\Lambda'\)

From the Galerkin moment ODEs
\[
X'=-2\nu Y+2N,\qquad Y'=-2\nu Z+2M,
\]
the spectral-scale identity is
\[
\Lambda'=\frac{2}{X}\bigl(T_c-\nu D_s\bigr).
\]
This is a **definition / identity check** in code — not a proof of ★.

---

## 7. Pointer: full claim + viscosity packaging (canonical)

The **full Lemma★ claim** (boxed geometric inequality / \(\sup\mathcal{R}_\star<\infty\)), four corrections, equivalent viscosity packaging
\[
T_c(u)\le\theta\nu D_s(u)+C_0(\theta)\nu^{-1}\|u\|_2^2 Y(u),\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta),
\]
and remaining target live in the canonical claim doc — **not** duplicated here:

→ [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md)

That bound remains **OPEN**. This formulas note supplies identities only.

---

## 8. Near-shell \(K_{\alpha,\beta}\) — restricted family only

Attack 9B defines
\[
K_{\alpha,\beta}
=\sup_{Aw=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
\]
The displayed limit
\[
\lim_{\varepsilon\to0}\mathcal{R}_\star(w_\alpha+\varepsilon z_\beta)=K_{\alpha,\beta}(w)
\]
holds **only** for an aligned, sign-selected closer
\[
z_\beta=\pm\Pi_\beta B(w,w)/\|\Pi_\beta B(w,w)\|_2
\]
(sign so \((T_c)_+>0\)). For arbitrary \(z_\beta\) on shell \(\beta\), the limit is the squared projection
\[
\lim_{\varepsilon\to0}\mathcal{R}_\star(w+\varepsilon z_\beta)
=
\frac{\beta\,\bigl|\langle\Pi_\beta B(w,w),z_\beta\rangle\bigr|^2}{\alpha^2\|w\|_2^4\|z_\beta\|_2^2}.
\]

**CRITICAL:** \(K_{\alpha,\beta}\) is a **restricted** near-shell / limiting-family probe. Bounding or sampling \(K\) is **not** the full Lemma★. See [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md).

---

## Related

- Canonical claim: [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md)
- Phone corrections: [`../../LEMMA-STAR-CORRECTIONS.md`](../../LEMMA-STAR-CORRECTIONS.md)
- Archive: [`LEMMA_STAR_OLDER_ATTEMPT_ARCHIVE.md`](./LEMMA_STAR_OLDER_ATTEMPT_ARCHIVE.md)
- Historical formulas: [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md)
- Status: [`../../five-lane-export/PROOF_LemmaStar_STATUS.md`](../../five-lane-export/PROOF_LemmaStar_STATUS.md)
- Attack 9B: [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md)
- Drill: https://github.com/simons357/Ship_it_app/pull/48
- Code: `scripts/ns_attacks/stokes_moments.py`, `scripts/ns_attacks/ns_lemma_star_core.py`, `tests/test_lemma_star_corrections.py`, `tests/test_ns_lemma_star_core.py`

**NS not solved.** \(\sup\mathcal{R}_\star\) **OPEN**. No invented proof.
