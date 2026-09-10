# PROOF status — Lemma★ (energy remainder)

**Date:** 2026-09-10  
**Lock:** **NS is NOT solved.** Lemma★ is **OPEN**. Numerics are not a proof.  
**Kill lane:** **LIVE.** Proof lane: **LIVE.**  
**Correct record:** [`ATTACK_8_CORRECT_RECORD.md`](./ATTACK_8_CORRECT_RECORD.md)

## Retired false claims (screenshot correction)

| Claim | Verdict |
|-------|---------|
| “The kill lane is closed” | **FALSE.** Failure to find a numerical counterexample does **not** close falsification. |
| “Amplitude or frequency makes the ratio smaller” | **FALSE for \(\mathcal R_\star\).** Concerns an older non-optimized budget. Correct \(\mathcal R_\star\) is **exactly invariant** under amplitude and uniform Fourier dilation. |

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
\bigl(T_c(v)_+\bigr)^2
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
\frac{(T_c(v)_+)^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}
\quad(\mathcal{D}_s>0).
\]

**\((T_c)_+\) vs prior \(T_c^2\):** when \(T_c\ge0\), \((T_c)_+^2=T_c^2\). Kill cares about stretching \(T_c>0\).

**Numerics hygiene:** do not compare \(0.065\), \(0.073\), \(1.93\times10^{-3}\) unless each used this exact formula.

Sign check identity (code-locked):
\[
\Lambda'=\frac{2}{X}(T_c-\nu\mathcal{D}_s).
\]

Two-shell closed form (search harness + unit tests):
\[
\mathcal{D}_s=\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

If \(\sup_v\mathcal R_\star<\infty\), that supremum **is** ★ (up to \(4\theta\)). A finite list of small-\(\mathcal R_\star\) fields is **not** that number.

**Caution:** HH→L can identify a mechanism; only **complete signed** \(T_c\) (total, not favorable HH→L-only) enters the ★ kill criterion.

### Equivalent viscosity packaging (derived, not primary)

\[
T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2\,Y
=\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2 X\Lambda,
\]
with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\).

**Invariants:** \(\mathcal R_\star(av)=\mathcal R_\star(v)\); \(\mathcal R_\star(v(n\cdot))=\mathcal R_\star(v)\).

## Live kill criteria (shape)

| Criterion | Meaning |
|-----------|---------|
| \(\mathcal R_\star(v_n)\to\infty\) on some smooth family | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(\mathcal D_s=0\) and \(T_c>0\) | **★ dead** on that field |
| Pure single shell (\(T_c=0=\mathcal D_s\)) | both sides vanish — **not** a kill |
| Almost-single-shell / near two-shell / exact-shell+closing (9B) with \(\mathcal R_\star\to\infty\) or \(K_{\alpha,\beta}\to\infty\) | **LIVE kill attempt** |
| AP / coherent packet fan (Attack 9A) | **Did not kill ★** — \(\mathcal D_s\) grew faster than \(T_c\) |
| Bounded \(\mathcal R_\star\) on a sample list | those shapes did not kill it — **not a proof**; kill lane still **LIVE** |

## What is proved / killed / open

| Claim | Status | Evidence |
|-------|--------|----------|
| Lemma★ \(\Rightarrow\) no finite-time blowup of \(\Lambda\) in this packaging \(\Rightarrow\) GR on \(\mathbb{T}^3\) **in this packaging** | **Conditional implication only** | Packaging / differential inequality; **not** a Clay submission |
| K=0 form \(T_c\le\theta\nu\mathcal D_s\) | **KILLED** | Attack 2: \(\lvert T_c\rvert/\mathcal D_s\sim B\) on fixed-shape high triad |
| Young reduction of \(T_c\) toward a norm of \(B(v,v)\) | **Partial / formal** | Polarization exists; does not close 3D product gap |
| \(\lvert T_c\rvert\le C\|v\|_2 X^{3/2}\) (or equiv) by Agmon/product | **GAP — does not close** | HH→L bottleneck (Attack 3); HH is diagnostic only |
| Uniform geometric \(C_{\mathrm{geom}}\) / \(C_0\) for Lemma★ (shape form) | **OPEN — kill lane LIVE** | Sample maxes (shape★ formula only) are **not** a proof and **do not** close falsification |
| Formula lock (linear / \(\mathcal D_s\) / \(T_c\) / \(\mathcal R_\star\) / \(\Lambda'\)) | **LOCKED in docs + unit tests** | `LEMMA_STAR_SHAPE_FORM.md`; `tests/test_ns_attacks_lemma_star.py` |
| Attack 8 correct record | **CORRECT RECORD** | Kill lane LIVE; \(\mathcal R_\star\) invariants; \((T_c)_+\) |
| Attack 9A packet fan \(\gamma\) | **Did not kill ★** — \(\gamma\approx-1.39\) (decaying) | \(\mathcal D_s\|v\|_2^2 Y=O(1)\) false for AP family; see `ATTACK_9A_AP_PACKET_FAILURE.md` |
| Attack 9B exact-shell \(K_{\alpha,\beta}\) | **LIVE** | \(v_\varepsilon=w_\alpha+\varepsilon z_\beta\); \(\mathcal R_\star\to K\); kill lane still LIVE |

## What a proof would have to be

Reason from how **signed** triads add that stretching cannot get large unless spectrum also spreads or phases cancel. HH→L is the channel that could refuse that. **That reason is NOT written.** Until it is mathematics (not numerics), **do not claim global regularity.** **NS not solved.**

## Live door

1. **Prove** the boxed shape inequality (uniform \(C_{\mathrm{geom}}\) / \(\sup\mathcal R_\star<\infty\)); **or**
2. **Kill** by exhibiting a smooth shape family with \(\mathcal R_\star\to\infty\) (Attack 9B: \(K_{\alpha,\beta}\to\infty\); almost-single-shell; not another widening AP packet) using **complete** \(T_c\); **or**
3. Upgrade centering cancellation beyond \(T_c=M-\Lambda N\) to remove the dangerous HH→L piece.

## Archive (NOT Lemma★)

Route N / Q6 / LP-shell floors: [`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/), [`../ARCHIVE_NOT_LEMMA_STAR.md`](../ARCHIVE_NOT_LEMMA_STAR.md). Ledgers stay linked, labeled **NOT Lemma★**.

## Related files

- `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` — **canonical exact formulas**
- `docs/math/ns_attacks/ATTACK_8_CORRECT_RECORD.md`
- `docs/math/ns_attacks/ATTACK_9_PACKET_FAN.md`
- `docs/math/ns_attacks/ATTACK_9A_AP_PACKET_FAILURE.md`
- `docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md`
- `docs/math/ns_attacks/ATTACK_SYNTHESIS_SIMULTANEOUS.md`
- `scripts/ns_attacks/stokes_moments.py`
- `scripts/ns_attacks/attack9_packet_fan.py`
- `scripts/ns_attacks/attack9b_exact_shell_K.py`
- `tests/test_ns_attacks_lemma_star.py`
- `/opt/cursor/artifacts/attack9_packet_fan/`
- `/opt/cursor/artifacts/attack9b_exact_shell/`
