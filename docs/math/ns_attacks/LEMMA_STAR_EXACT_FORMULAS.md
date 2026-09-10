# Lemma★ — exact formulas (shape form)

**Status:** definitions / identities only. Bound on \(C_{\mathrm{geom}}\) / \(\sup\mathcal{R}_\star\) **OPEN**. **NS not solved.** Kill lane **LIVE**.

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390` / PR #48  
**Lock:** Truth only. Locks formulas; does **not** prove ★.

| Role | File |
|------|------|
| **Canonical boxed claim** (+ viscosity packaging + kill table) | [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md) → [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md) |
| **Exact formulas** (this file) | linear moments, all \(\mathcal{D}_s\) forms, two-shell, \(B/T_k/N/M/T_c\), ordered / \(p+q+r=0\) triad, boxed \(\mathcal{R}_\star\), \(\Lambda'\) |
| Code | `scripts/ns_attacks/stokes_moments.py` (`Tc = M - Lam * N`, **`ratio_R_star_shape`**) |

Desktop paths (`/Users/jonathansimons/Desktop/Harmonic Universe Book/LEMMA_STAR_EXACT_FORMULAS.md`, `LEMMA_STAR_CANONICAL.md`) were **not mounted** here; LaTeX norms restored as \(\|\cdot\|_2\), missing equals restored from the on-branch SoT lock. Do **not** invent a second claim box here.

---

## 1. Torus setup, Fourier, Stokes operator

On \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\), nonzero mean-zero divergence-free \(v\):
\[
v(x)=\sum_{k\in\mathbb{Z}^3\setminus\{0\}} v_k e^{ik\cdot x},\qquad
k\cdot v_k=0,\qquad
v_{-k}=\overline{v_k}.
\]
\[
\lambda_k=|k|^2,\qquad
A=-P\Delta,\qquad
(Av)_k=\lambda_k v_k,\qquad
B(v,v)=P[(v\cdot\nabla)v].
\]

---

## 2. Linear moments \(E,X,Y,Z,\Lambda\)

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

## 3. All equivalent forms of \(\mathcal{D}_s\) (alias \(D_s\))

**Do not invent a second \(D_s\).** All of the following are the **same** nonnegative object:
\[
\begin{aligned}
\mathcal{D}_s
&=D_s
=Z-\Lambda Y
=Z-\frac{Y^2}{X}
=\|(A-\Lambda)A^{1/2}v\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac{1}{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2
\ge 0.
\end{aligned}
\]
Code: `Ds` via `moments()`; cross-checks `Ds_variance_sum`, `Ds_double_sum`.

### Two-shell closed form

On exactly two eigenvalue shells \(\alpha,\beta\) with energies \(e_\alpha,e_\beta\):
\[
\mathcal{D}_s
=\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]
Code: `Ds_two_shell`.

**Vacuous case:** \(\mathcal{D}_s=0\) \(\Leftrightarrow\) support on a single Fourier shell \(\Rightarrow\) \(T_c=0\) (not a kill).

---

## 4. Nonlinear \(B\), signed \(T_k\) — CAUTION

\[
\widehat{B(v,v)}_k
=i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q,\qquad
P_k=I-\frac{k\otimes k}{|k|^2}.
\]
\[
T_k(v)
=-\mathrm{Re}\bigl(\widehat{B}_k\cdot\overline{v_k}\bigr)
=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

**CAUTION:** keep the **signed** \(\mathrm{Im}\). **No absolute values.** Never replace \(\mathrm{Im}(\cdots)\) by \(\lvert\mathrm{Im}\rvert\) or by product moduli.

Energy conservation of the bilinear form on mean-zero fields:
\[
\sum_k T_k=0.
\]

---

## 5. \(N\), \(M\), and \(T_c\)

\[
N=-\langle B,Av\rangle=\sum_k\lambda_k T_k,\qquad
M=-\langle AB,Av\rangle=\sum_k\lambda_k^2 T_k.
\]
\[
\begin{aligned}
T_c
=\mathcal{T}_c
&=-\langle B(v,v),A(A-\Lambda)v\rangle
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k
=\sum_{p+q=k}\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\end{aligned}
\]
Code: `Tc = M - Lam * N`; also `Tc_from_triads`, `Tc_from_B_field`.

---

## 6. Ordered triad / \(p+q+r=0\) form

**Ordered** Fourier triples with \(k=p+q\):
\[
T_c
=\sum_{\substack{p,q\\k=p+q}}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

**\(p+q+r=0\) form** (set \(k=-r\)):
\[
T_c
=\sum_{p+q+r=0}
\lambda_{-r}(\lambda_{-r}-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v}_{-r})\bigr].
\]

| Allowed | Forbidden |
|---------|-----------|
| Cyclic permutations of \((p,q,r)\) (same signed geometry) | Replacing \(\mathrm{Im}\) by \(\lvert\mathrm{Im}\rvert\) |
| Complete signed sum over all triads | Favorable HH→L-only truncation as a kill criterion |
| Ordered \((p,q,k)\) with \(k=p+q\) | Absolute values on triad products |

**HH→L:** channel splits (Attack 3 / 9B \(\beta<\alpha\)) may **identify** a mechanism; only the **complete signed** \(T_c\) enters the ★ kill criterion. Attack 3 is **not** a strict HH→L output map ([`ATTACK_3_BONY_HH_L.md`](./ATTACK_3_BONY_HH_L.md)).

---

## 7. Boxed shape quotient \(\mathcal{R}_\star\)

When \(D_s(v)>0\), \(\|v\|_2>0\), \(Y(v)>0\):
\[
\boxed{
\mathcal{R}_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}
}
\]
with \(T_c{}_+=\max(T_c,0)\). Canonical code: **`ratio_R_star_shape`**. Alias `ratio_R_star` → same. Legacy `ratio_star` \(=T_c/(E X\Lambda)\) is a **different** post-Young object.

### Compression \(\Rightarrow\) zero quotient

\[
T_c\le 0\quad\Rightarrow\quad (T_c)_+=0\quad\Rightarrow\quad\mathcal{R}_\star=0.
\]
Kill cares about stretching \(T_c>0\). When \(T_c\ge 0\), \((T_c)_+^2=T_c^2\).

### Exact invariances

For \(a>0\): \(\mathcal{R}_\star(av)=\mathcal{R}_\star(v)\).  
Uniform Fourier dilation: \(\mathcal{R}_\star(v(n\cdot))=\mathcal{R}_\star(v)\).

**Retired false claim:** “Amplitude or frequency makes the ratio smaller” — **FALSE for \(\mathcal{R}_\star\)**.

---

## 8. Sign check \(\Lambda'\)

From
\[
X'=-2\nu Y+2N,\qquad Y'=-2\nu Z+2M,
\]
\[
\Lambda'=\frac{2}{X}\bigl(T_c-\nu\mathcal{D}_s\bigr).
\]
Code: `Lambda_prime_rhs` / `Lambda_prime_from_XY` — identity check, **not** a proof of ★.

---

## 9. Pointer: full claim + viscosity packaging (canonical)

Full boxed Lemma★ (\(\sup\mathcal{R}_\star<\infty\) / geometric \(C_{\mathrm{geom}}\)), viscosity packaging
\[
T_c(u)\le\theta\nu D_s(u)+C_0(\theta)\nu^{-1}\|u\|_2^2 Y(u),\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta),
\]
and kill/survive table:

→ [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md)  
→ [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md)

That bound remains **OPEN**. This formulas note supplies identities only.

---

## 10. Near-shell \(K_{\alpha,\beta}\) — restricted family only

\[
K_{\alpha,\beta}
=\sup_{Aw=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4},\qquad
\lim_{\varepsilon\to0}\mathcal{R}_\star(w_\alpha+\varepsilon z_\beta)=K_{\alpha,\beta}(w)
\]
on the exact-shell + infinitesimal closing family only.

**CRITICAL:** \(K_{\alpha,\beta}\) is a **restricted** near-shell / limiting-family probe — **not** the full Lemma★. See [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md).

---

## Related

- Canonical claim alias: [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md)
- Primary claim SoT: [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md)
- Status: [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)
- Locator: [`FIVE_LANE_PACK_LOCATOR.md`](./FIVE_LANE_PACK_LOCATOR.md) — https://github.com/simons357/Ship_it_app/pull/48
- Code / tests: `scripts/ns_attacks/stokes_moments.py`, `tests/test_ns_attacks_lemma_star.py`

**NS not solved.** \(\sup\mathcal{R}_\star\) **OPEN**. No invented proof.
