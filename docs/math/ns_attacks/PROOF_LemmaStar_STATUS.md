# PROOF status — Lemma★ (energy remainder)

**Date:** 2026-09-10  
**Lock:** **NS is NOT solved.** Lemma★ is **OPEN**. Numerics are not a proof.

## Canonical form: shape statement (exact lock)

**Lemma★ is no longer a viscosity statement. It is a shape statement.**

Exact torus / linear / \(\mathcal D_s\) / nonlinear / \(T_c\) / \(\mathcal R_\star\) formulas:
[`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md).

On divergence-free fields on \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\), with \(\lambda_k=|k|^2\), \(A=-P\Delta\),
\[
\|v\|_2^2=\sum|v_k|^2,\quad
X=\sum\lambda_k|v_k|^2,\quad
Y=\sum\lambda_k^2|v_k|^2,\quad
Z=\sum\lambda_k^3|v_k|^2,\quad
\Lambda=Y/X,
\]
\[
\mathcal{D}_s=Z-\Lambda Y=Z-Y^2/X=\sum\lambda_k(\lambda_k-\Lambda)^2|v_k|^2\ge0,
\]
\[
T_k=-\mathrm{Re}(\widehat B_k\cdot\overline{v_k})
=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr]
\quad\text{(signed; no abs)},
\]
\[
N=\sum\lambda_k T_k,\quad
M=\sum\lambda_k^2 T_k,\quad
T_c=M-\Lambda N=\sum\lambda_k(\lambda_k-\Lambda)T_k,
\]
the **canonical ★** asserts one geometric constant \(C_{\mathrm{geom}}\) such that
\[
\bigl(T_c(v)\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal{D}_s(v)\,
\|v\|_2^2\,
Y(v).
\]

Complete quotient (scripts: `ratio_R_star` / `ratio_R_star_shape`):
\[
\mathcal{R}_\star(v)
=
\frac{(T_c(v))^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}
\quad(\mathcal{D}_s>0).
\]

Sign check identity (code-locked):
\[
\Lambda'=\frac{2}{X}(T_c-\nu\mathcal{D}_s).
\]

Two-shell closed form (search harness + unit tests):
\[
\mathcal{D}_s=\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

If \(\sup_v\mathcal R_\star<\infty\), that supremum **is** ★ (up to \(4\theta\)). A finite list of small-\(\mathcal R_\star\) fields is **not** that number.

**Caution:** HH→L can identify a mechanism; only **complete signed** \(T_c\) enters the ★ kill criterion.

### Equivalent viscosity packaging (derived, not primary)

\[
T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2\,Y
=\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2 X\Lambda,
\]
with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\).

**\(u=av\):** worst size cancels \(\nu\); \(\mathcal R_\star(av)=\mathcal R_\star(v)\). If the shape line holds for every \(v\) with one \(C_{\mathrm{geom}}\), original ★ holds for every amplitude and every \(\nu\). If it fails for even one shape, ★ is false.

## Live kill criteria (shape)

| Criterion | Meaning |
|-----------|---------|
| \(\mathcal R_\star(v_n)\to\infty\) on some smooth family | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(\mathcal D_s=0\) and \(T_c\neq 0\) | **★ dead** on that field |
| Pure single shell (\(T_c=0=\mathcal D_s\)) | both sides vanish — **not** a kill |
| Almost-single-shell / near two-shell with \(\mathcal D_s\to0^+\) but \(\mathcal R_\star\to\infty\) (complete \(T_c\)) | **live kill attempt** |
| Bounded \(\mathcal R_\star\) on a sample list | those shapes did not kill it — **not a proof** of a uniform \(C_{\mathrm{geom}}\) |

## What is proved / killed / open

| Claim | Status | Evidence |
|-------|--------|----------|
| Lemma★ \(\Rightarrow\) no finite-time blowup of \(\Lambda\) in this packaging \(\Rightarrow\) GR on \(\mathbb{T}^3\) **in this packaging** | **Conditional implication only** | Packaging / differential inequality; **not** a Clay submission |
| K=0 form \(T_c\le\theta\nu\mathcal D_s\) | **KILLED** | Attack 2: \(\lvert T_c\rvert/\mathcal D_s\sim B\) on fixed-shape high triad |
| Young reduction of \(T_c\) toward a norm of \(B(v,v)\) | **Partial / formal** | Polarization exists; does not close 3D product gap |
| \(\lvert T_c\rvert\le C\|v\|_2 X^{3/2}\) (or equiv) by Agmon/product | **GAP — does not close** | HH→L bottleneck (Attack 3); HH is diagnostic only |
| Uniform geometric \(C_{\mathrm{geom}}\) / \(C_0\) for Lemma★ (shape form) | **OPEN — survives numeric kill drill** | Attack 5 + near-shell/HH→L harness with **complete signed \(T_c\)** and two-shell \(\mathcal D_s\); finite \(\max\mathcal R_\star\) on samples is **not** a proof |
| Formula lock (linear / \(\mathcal D_s\) / \(T_c\) / \(\mathcal R_\star\) / \(\Lambda'\)) | **LOCKED in docs + unit tests** | `LEMMA_STAR_SHAPE_FORM.md`; `tests/test_ns_attacks_lemma_star.py` |
| Amplitude-invariant \(C_*\) for \(X^{3/2}\Lambda\) remainder | **OPEN (numeric support)** | Attack 2 / Attack 5 survivors |

## What a proof would have to be

Reason from how **signed** triads add that stretching cannot get large unless spectrum also spreads or phases cancel. HH→L is the channel that could refuse that. **That reason is NOT written.** Until it is mathematics (not numerics), **do not claim global regularity.** **NS not solved.**

## Live door (unchanged in substance)

1. **Prove** the boxed shape inequality (uniform \(C_{\mathrm{geom}}\) / \(\sup\mathcal R_\star<\infty\)), or the weaker \(C_* X^{3/2}\Lambda\) bound; **or**
2. **Kill** by exhibiting a smooth shape family with \(\mathcal R_\star\to\infty\) (esp. almost-single-shell / near two-shell) using **complete** \(T_c\); **or**
3. Upgrade centering cancellation beyond \(T_c=M-\Lambda N\) to remove the dangerous HH→L piece.

## Related files

- `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` — **canonical exact formulas**
- `docs/math/ns_attacks/ATTACK_SYNTHESIS_SIMULTANEOUS.md`
- `docs/math/ns_attacks/DA-SHAPE-TEXTURE-LINK.md`
- `scripts/ns_attacks/stokes_moments.py` — Galerkin moments / \(T_c\) / \(\mathcal R_\star\)
- `scripts/ns_attacks/lemma_star_near_shell_search.py` — near-shell + HH→L harness
- `scripts/ns_attacks/attack5_route2_kill.py`
- `tests/test_ns_attacks_lemma_star.py`
- `/opt/cursor/artifacts/ns_five_lane_2026-09-10/`
- `/opt/cursor/artifacts/lemma_star_formula_lock/` — formula-lock walkthrough
