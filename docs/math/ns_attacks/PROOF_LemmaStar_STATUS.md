# PROOF status — Lemma★ (energy remainder)

**Date:** 2026-09-10  
**Lock:** **NS is NOT solved.** Lemma★ is **OPEN**. Numerics are not a proof.

## Canonical form: shape statement

**Lemma★ is no longer a viscosity statement. It is a shape statement.**

Full derivation, boxed inequality, and \(\mathcal R_\star\) definition:
[`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md).

On divergence-free fields on \(\mathbb{T}^3\), with Stokes operator \(A\) and
\[
E=\|u\|_2^2,\quad
X=\|A^{1/2}u\|_2^2,\quad Y=\|Au\|_2^2,\quad Z=\|A^{3/2}u\|_2^2,\quad\Lambda=\frac{Y}{X},
\]
\[
\mathcal N=-\langle B(u,u),Au\rangle,\quad
\mathcal M=-\langle B(u,u),A^2u\rangle,\quad
\mathfrak T_c=\mathcal M-\Lambda\mathcal N,\quad
\mathcal D_s=Z-\Lambda Y\ge0,
\]
the **canonical ★** asserts there is one geometric constant \(C_{\mathrm{geom}}\) such that for every divergence-free shape \(v\),
\[
\bigl(\mathfrak T_c(v)\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal D_s(v)\,
E(v)\,
Y(v).
\]

Shape ratio (amp- and \(\nu\)-invariant; scripts: `ratio_R_star_shape`):
\[
\mathcal R_\star(v)
=
\frac{\bigl(\mathfrak T_c(v)\bigr)^2}{\mathcal D_s(v)\,E(v)\,Y(v)}
\quad(\mathcal D_s>0).
\]

If \(\sup_v\mathcal R_\star<\infty\), that supremum **is** ★ (up to \(4\theta\)). A finite list of small-\(\mathcal R_\star\) fields is **not** that number.

### Equivalent viscosity packaging (derived, not primary)

\[
\mathfrak T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1} E\,Y
=\theta\nu\mathcal D_s+C_0\nu^{-1}\|u\|_2^2 X\Lambda,
\]
with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\). Pre-Young / amplitude form: \(|\mathfrak T_c|\le C\|u\|_2 X\Lambda\), then Young in \(\nu\).

**\(u=av\):** worst size cancels \(\nu\); what remains is the boxed shape line. If the shape line holds for every \(v\) with one \(C_0(\theta)\), original ★ holds for every amplitude and every \(\nu\). If it fails for even one shape, ★ is false.

## Live kill criteria (shape)

| Criterion | Meaning |
|-----------|---------|
| \(\mathcal R_\star(v_n)\to\infty\) on some smooth family | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(\mathcal D_s=0\) and \(\mathfrak T_c>0\) | **★ dead** on that field |
| Pure single shell (\(\mathfrak T_c=0=\mathcal D_s\)) | both sides vanish — **not** a kill |
| Almost-single-shell with \(\mathcal D_s\to0^+\) but \(\mathcal R_\star\to\infty\) | **live kill attempt** |
| Bounded \(\mathcal R_\star\) on a sample list | those shapes did not kill it — **not a proof** of a uniform \(C_{\mathrm{geom}}\) |

## What is proved / killed / open

| Claim | Status | Evidence |
|-------|--------|----------|
| Lemma★ \(\Rightarrow\) no finite-time blowup of \(\Lambda\) in this packaging \(\Rightarrow\) GR on \(\mathbb{T}^3\) **in this packaging** | **Conditional implication only** | Packaging / differential inequality; **not** a Clay submission |
| K=0 form \(\mathfrak T_c\le\theta\nu\mathcal D_s\) | **KILLED** | Attack 2: \(\lvert T_c\rvert/\mathcal D_s\sim B\) on fixed-shape high triad (\(0.0035\to349\)) |
| Young reduction of \(\mathfrak T_c\) toward a norm of \(B(u,u)\) | **Partial / formal** | Polarization exists; does not close 3D product gap |
| \(|\mathfrak T_c|\le C\|u\|_2 X^{3/2}\) (or equiv) by Agmon/product | **GAP — does not close** | HH→L bottleneck (Attack 3) |
| Uniform geometric \(C_{\mathrm{geom}}\) / \(C_0\) for Lemma★ (shape form) | **OPEN — survives numeric kill drill** | Attack 1+5: max \(\lvert R_{\mathrm{pre}}\rvert\approx5.09\) on 978 samples; almost-shell \(\mathcal R_\star\) probe — see Attack 5; **not** \(\to\infty\); **still not a proof** |
| Amplitude-invariant \(C_*\) for \(X^{3/2}\Lambda\) remainder | **OPEN (numeric support)** | Attack 2: \(C_*\approx0.004058\) fixed triad; Attack 5 max \(\approx0.0406\) |

## What a proof would have to be

Reason from how triads add that stretching cannot get large unless spectrum also spreads or phases cancel. HH→L is the channel that could refuse that. **That reason is NOT written.** Until it is mathematics (not numerics), **do not claim global regularity.** **NS not solved.**

## Live door (unchanged in substance)

1. **Prove** the boxed shape inequality (uniform \(C_{\mathrm{geom}}\) / \(\sup\mathcal R_\star<\infty\)), or the weaker \(C_* X^{3/2}\Lambda\) bound; **or**
2. **Kill** by exhibiting a smooth shape family with \(\mathcal R_\star\to\infty\) (esp. almost-single-shell); **or**
3. Upgrade centering cancellation beyond \(\mathfrak T_c=\mathcal M-\Lambda\mathcal N\) to remove the dangerous HH→L piece.

## Related files

- `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` — **canonical** boxed ★ + \(\mathcal R_\star\)
- `docs/math/ns_attacks/ATTACK_SYNTHESIS_SIMULTANEOUS.md`
- `docs/math/ns_attacks/DA-SHAPE-TEXTURE-LINK.md` — DA SHAPE ↔ \(v\); texture/ratio ↔ \(\mathcal R_\star\)
- `docs/ns-recovery/CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md`
- `scripts/ns_attacks/`
- `/opt/cursor/artifacts/ns_five_lane_2026-09-10/`
- `/opt/cursor/artifacts/da-shape-texture/` — DA shape/texture demo (splicer branch), not a proof
