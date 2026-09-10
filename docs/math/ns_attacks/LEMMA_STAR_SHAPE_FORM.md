# Lemma★ — canonical shape form (exact lock)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Lock:** Truth only. **NS is NOT solved.** Lemma★ is **OPEN**. This note locks formulas; it does not prove ★.

## Reframe (lock)

**Lemma★ is no longer a viscosity statement. It is a shape statement.**

Change only the size of a fixed shape \(v\) via \(u=av\). Optimize over size. Worst size cancels \(\nu\). What remains is pure geometry on the shape.

Scripts: `scripts/ns_attacks/stokes_moments.py`

| Code name | Object |
|-----------|--------|
| **`ratio_R_star_shape`** | **Canonical** \(\mathcal R_\star=(T_c)_+^2/(\mathcal D_s\|v\|_2^2 Y)\) |
| `ratio_R_star` | Alias property → same as `ratio_R_star_shape` |
| **`ratio_star`** (legacy) | **Different** post-Young \(T_c/(E X\Lambda)\) — scales as \(1/a\); **not** \(\mathcal R_\star\) |

Do **not** confuse legacy `ratio_star` with the canonical shape quotient.

---

## Torus / Stokes setup

\[
\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3
\]
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

---

## Linear moments

\[
\|v\|_2^2=\sum|v_k|^2,\quad
X=\|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2,\quad
Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2,\quad
Z=\|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2,
\]
\[
\Lambda=Y/X.
\]

(Code alias: \(E=\|v\|_2^2\).)

---

## Centered spectral dissipation \(\mathcal D_s\) (3 equivalent forms)

\[
\mathcal{D}_s
=Z-\Lambda Y
=Z-Y^2/X
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac1{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2.
\]

In particular \(\mathcal D_s\ge 0\).

### Two-eigenvalue shells

Shells \(\alpha,\beta\) with energies \(e_\alpha,e_\beta\) (here \(e_\alpha=\sum_{\lambda_k=\alpha}|v_k|^2\)):

\[
\mathcal{D}_s
=\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

---

## Nonlinear transfer

\[
B(v,v)=P[(v\cdot\nabla)v],\quad
\widehat{B(v,v)}_k
=i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q,\quad
P_k=I-\frac{k\otimes k}{|k|^2}.
\]
\[
T_k(v)
=-\mathrm{Re}\bigl(\widehat{B}_k\cdot\overline{v_k}\bigr)
=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

**Caution:** keep the **signed** complex triad sum. Do **not** replace \(\mathrm{Im}(\cdots)\) by absolute values.

\[
N=-\langle B,Av\rangle=\sum\lambda_k T_k,\quad
M=-\langle AB,Av\rangle=\sum\lambda_k^2 T_k,
\]
\[
T_c
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k
=\sum_{p+q=k}\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

### Ordered triad / \(p+q+r=0\) form

With \(k=p+q=-r\) (so \(p+q+r=0\)):

\[
T_c
=\sum_{p+q+r=0}
\lambda_{-r}(\lambda_{-r}-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_{-r}})\bigr].
\]

(Equivalent cyclic writings that keep the same signed \(\mathrm{Im}\) are allowed; absolute-value rearrangements are not.)

HH→L channel splits can **identify** a mechanism; only the **complete** signed \(T_c\) enters the kill criterion for ★.  
**Attack 3 caveat:** the Bony HH split filters high-frequency **inputs** and does **not** restrict **output** to low frequencies — Attack 3 is **not** a strict HH→L map ([`ATTACK_3_BONY_HH_L.md`](./ATTACK_3_BONY_HH_L.md)). Genuine HH→L as an **output** subfamily in 9B requires \(\beta<\alpha\).

---

## Sign check (spectral drift)

From the Galerkin identities \(X'=-2\nu Y+2N\), \(Y'=-2\nu Z+2M\):

\[
\Lambda'=\frac{2}{X}\bigl(T_c-\nu\mathcal{D}_s\bigr).
\]

---

## Complete quotient / canonical shape★

When \(\mathcal D_s(v)>0\), \(\|v\|_2>0\), \(Y(v)>0\), with positive part \((T_c)_+=\max(T_c,0)\):

\[
\mathcal{R}_\star(v)
=
\frac{(T_c(v)_+)^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}.
\]

Expanded (same when \(T_c\ge0\)):
\[
\mathcal{R}_\star(v)
=
\frac{
\Bigl(
\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl((q\cdot v_p)(v_q\cdot\overline{v_k})\bigr)
\Bigr)_+^{\!2}
}{
\bigl[\sum\lambda_k(\lambda_k-\Lambda)^2|v_k|^2\bigr]
\bigl[\sum|v_k|^2\bigr]
\bigl[\sum\lambda_k^2|v_k|^2\bigr]
}.
\]

**Alignment with prior \(T_c^2\) form:** older Galerkin probes used \(T_c^2\) in the numerator. When \(T_c\ge0\), \((T_c)_+^2=T_c^2\). For kill we care about stretching \(T_c>0\); compression \(T_c<0\) gives \(\mathcal R_\star=0\) under the \((T_c)_+\) form and is not a stretching counterexample.

**Numerics hygiene:** do **not** compare legacy reported values \(0.065\), \(0.073\), \(1.93\times10^{-3}\) unless each used exactly this \(\mathcal R_\star\) formula.

**Boxed shape inequality (canonical ★):** there exists one geometric constant \(C_{\mathrm{geom}}\) (independent of amplitude and of \(\nu\)) such that for every divergence-free \(v\) on \(\mathbb{T}^3\),
\[
\boxed{
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal{D}_s(v)\,
\|v\|_2^2\,
Y(v)
}
\]
i.e. \(\sup_v\mathcal R_\star<\infty\) with that supremum equal to \(C_{\mathrm{geom}}\) (when the sup is finite).

Homogeneity (\(a>0\)) — **exact invariance** (not “ratio gets smaller”):
\[
T_c(av)=a^3 T_c(v),\quad
\mathcal D_s(av)=a^2\mathcal D_s(v),\quad
\|av\|_2^2=a^2\|v\|_2^2,\quad
Y(av)=a^2 Y(v),\quad
\Lambda(av)=\Lambda(v),\quad
\mathcal R_\star(av)=\mathcal R_\star(v).
\]

Uniform Fourier dilation \(v(n\cdot)\) (mode \(k\mapsto nk\)) likewise leaves \(\mathcal R_\star\) **exactly invariant**. Claims that amplitude or frequency makes the ratio smaller concern an **older non-optimized budget**, not \(\mathcal R_\star\).

### Viscosity packaging (derived, not primary)

Young / AM–GM on the amplitude line recovers
\[
T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2\,Y
=\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2\,X\Lambda,
\]
with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\).

---

## Kill / survive table

| Outcome | Verdict |
|---------|---------|
| Some shapes make \(\mathcal R_\star\) arbitrarily large | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(\mathcal D_s=0\) (one Fourier shell) and \(T_c>0\) | **★ dead** on that field |
| Pure single shell, both sides vanish (\(T_c=0=\mathcal D_s\)) | vacuous — not a kill |
| Live kill attempt | almost-single-shell / near two-shell / exact-shell + closing (9B \(K_{\alpha,\beta}\)); designed \(\Theta(m^2)\) locked-phase (9D, stub) |
| AP packet fan (9A) / fixed-gap natural ensemble (9C) | **Did not kill ★** — 9C: \(\mathcal R_\star\) falls \(0.11\to 0.031\), not \(m^{1/2}\) |
| Every shape has \(\mathcal R_\star\le K\) | that number is ★ (up to \(4\theta\)) |
| A list of fields with small \(\mathcal R_\star\) | **NOT** that number — those shapes did not kill it |
| Failure to find a numerical counterexample | does **NOT** close the kill lane — falsification **LIVE**, proof **LIVE** |

**Retired false claim:** “The kill lane is closed.” — **FALSE.**

**Do not confuse** with post-Young \(R_{\mathrm{post}}=T_c/(\|v\|_2^2 Y)\) (scales as \(1/a\)) or pre-Young \(R_{\mathrm{pre}}=T_c/(\|v\|_2\,X\Lambda)\). Those older budgets are where “amplitude makes the ratio smaller” can appear; they are **not** \(\mathcal R_\star\).

**Archive:** Route N / Q6 / LP-shell floors → [`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/) (**NOT Lemma★**).

## What a proof would have to be

Reason from how **signed** triads add that stretching cannot get large unless spectrum also spreads or phases cancel. HH→L is the channel that could refuse that. That reason is **NOT written**.

**NS not solved.**

## Related

- Status board: [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)
- Correct record: [`ATTACK_8_CORRECT_RECORD.md`](./ATTACK_8_CORRECT_RECORD.md)
- Packet fan (9A, did not kill ★): [`ATTACK_9_PACKET_FAN.md`](./ATTACK_9_PACKET_FAN.md), [`ATTACK_9A_AP_PACKET_FAILURE.md`](./ATTACK_9A_AP_PACKET_FAILURE.md)
- Exact-shell closing (9B): [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md)
  \[
  K_{\alpha,\beta}=\sup_{Aw=\alpha w}\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4},\quad
  \lim_{\varepsilon\to0}\mathcal R_\star(w_\alpha+\varepsilon z_\beta)=K_{\alpha,\beta}(w).
  \]
  **CRITICAL:** sample \(\max K\approx0.641\) at \((4,8)\) has \(\beta>\alpha\) (higher shell, **not** HH→L). Genuine HH→L subfamily \(\beta<\alpha\): sample max \(\approx0.0123\) at \((5,2)\).
- Fixed-gap spheres (9C, **not** a kill): [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md) — \(\mathcal R_\star\) \(0.11\to 0.031\); **SoT-only** until probe (no sweep script/data in PR #48)
- Pack locator: [`FIVE_LANE_PACK_LOCATOR.md`](./FIVE_LANE_PACK_LOCATOR.md) — https://github.com/simons357/Ship_it_app/pull/48
- Next falsifier (9D stub): [`ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](./ATTACK_9D_THETA_M2_LOCKED_PHASE.md) — designed \(\Theta(m^2)\) locked-phase closures
- Synthesis: [`ATTACK_SYNTHESIS_SIMULTANEOUS.md`](./ATTACK_SYNTHESIS_SIMULTANEOUS.md)
- Archive (NOT ★): [`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/), [`../ARCHIVE_NOT_LEMMA_STAR.md`](../ARCHIVE_NOT_LEMMA_STAR.md)
- Probe / harness: `scripts/ns_attacks/stokes_moments.py`, `attack5_route2_kill.py`, `lemma_star_near_shell_search.py`, `attack9_packet_fan.py`, `attack9b_exact_shell_K.py` (9C/9D scripts not yet present)
