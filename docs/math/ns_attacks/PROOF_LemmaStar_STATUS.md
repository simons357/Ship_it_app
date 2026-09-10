# PROOF status — Lemma★ (energy remainder)

**Date:** 2026-09-10  
**Lock:** **NS is NOT solved.** Lemma★ is **OPEN**. Bound on \(C_{\mathrm{geom}}\) / \(\sup\mathcal{R}_\star\) **OPEN**. Numerics are not a proof.  
**Kill lane:** **LIVE.** Proof lane: **LIVE.**  
**Correct record:** [`ATTACK_8_CORRECT_RECORD.md`](./ATTACK_8_CORRECT_RECORD.md)  
**Exact triad formulas:** [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md)

## Retired false claims (screenshot correction)

| Claim | Verdict |
|-------|---------|
| “The kill lane is closed” | **FALSE.** Failure to find a numerical counterexample does **not** close falsification. |
| “Amplitude or frequency makes the ratio smaller” | **FALSE for \(\mathcal R_\star\).** Concerns an older non-optimized budget. Correct \(\mathcal R_\star\) is **exactly invariant** under amplitude and uniform Fourier dilation. |

## Canonical form: FULL exact shape statement (absolute SoT)

**Reframe:** ★ is a **shape** statement, not a viscosity statement (\(u=av\); worst size cancels \(\nu\)). Absolute lock (2026-09-10 exact lock):
[`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md). Long expansions: [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md).

For nonzero mean-zero divergence-free \(v\) on \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\),
\[
A=-P\Delta,\quad B(v,v)=P[(v\cdot\nabla)v],
\]
\[
E=\|v\|_2^2,\quad
X=\|A^{1/2}v\|_2^2,\quad
Y=\|Av\|_2^2,\quad
Z=\|A^{3/2}v\|_2^2,\quad
\Lambda=Y/X,
\]
\[
D_s=Z-Y^2/X=\|(A-\Lambda)A^{1/2}v\|_2^2,\qquad
T_c=-\langle B(v,v),A(A-\Lambda)v\rangle.
\]
(Alias: older docs \(\mathcal{D}_s=Z-\Lambda Y\) — same as \(D_s\). Equivalent triad form \(T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k\): [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md).)

**Full Lemma★ (claim; closing bound OPEN):**
\[
\boxed{
\exists\,C_{\mathrm{geom}}<\infty\quad
\forall\,v\in C^\infty_{\mathrm{div},0}(\mathbb{T}^3)\setminus\{0\}:\quad
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,D_s(v)\,\|v\|_2^2\,Y(v).
}
\]
Equivalently (\(D_s>0\)): \(\sup_v (T_c)_+^2/(D_s\|v\|_2^2 Y)<\infty\).  
For \(D_s=0\): one shell and \(T_c=0\) — **vacuous, not a kill**.  
\(C_{\mathrm{geom}}\) depends only on fixed geometry/normalization — not amplitude, Fourier support, shell count, or viscosity. **Existence of finite \(C_{\mathrm{geom}}\) is OPEN.**

Complete quotient (**canonical** code: `ratio_R_star_shape`; alias `ratio_R_star`):
\[
\mathcal{R}_\star(v)
=
\frac{(T_c(v)_+)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}
\quad(D_s>0).
\]

**Near-shell \(K_{\alpha,\beta}\):** restricted limiting-family probe only — **not** the full lemma ([`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md)).

**Legacy `ratio_star`:** \(T_c/(E X\Lambda)\) — **different** post-Young object; do not confuse with \(\mathcal R_\star\).
**\((T_c)_+\) vs prior \(T_c^2\):** when \(T_c\ge0\), \((T_c)_+^2=T_c^2\). Kill cares about stretching \(T_c>0\).

Sign check identity (code-locked):
\[
\Lambda'=\frac{2}{X}(T_c-\nu D_s).
\]

Two-shell closed form:
\[
D_s=\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

If \(\sup_v\mathcal R_\star<\infty\), that supremum **is** ★ (up to \(4\theta\)). A finite list of small-\(\mathcal R_\star\) fields is **not** that number.

**Caution:** HH→L can identify a mechanism; only **complete signed** \(T_c\) (total, not favorable HH→L-only) enters the ★ kill criterion.

### Equivalent viscosity packaging (derived, not primary)

For fixed \(0<\theta<1\):
\[
T_c(u)\le\theta\nu D_s(u)+C_0(\theta)\nu^{-1}\|u\|_2^2 Y(u),\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta).
\]

**Invariants:** \(\mathcal R_\star(av)=\mathcal R_\star(v)\); \(\mathcal R_\star(v(n\cdot))=\mathcal R_\star(v)\).

## Live kill criteria (shape)

| Criterion | Meaning |
|-----------|---------|
| \(\mathcal R_\star(v_n)\to\infty\) on some smooth family | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(\mathcal D_s=0\) and \(T_c>0\) | **★ dead** on that field |
| Pure single shell (\(T_c=0=\mathcal D_s\)) | both sides vanish — **not** a kill |
| Almost-single-shell / near two-shell / exact-shell+closing (9B) with \(\mathcal R_\star\to\infty\) or \(K_{\alpha,\beta}\to\infty\) | **LIVE kill attempt** on that **restricted** family (sample finite); \(K_{\alpha,\beta}\) ≠ full ★ |
| AP / coherent packet fan (Attack 9A) | **Did not kill ★** — \(\mathcal D_s\) grew faster than \(T_c\) |
| Fixed-gap spheres \(n,n+d\) (Attack 9C) | **Did not kill ★** — \(\mathcal R_\star\) falls \(0.11\to 0.031\); natural same-shell **NOT** a kill |
| Designed \(\Theta(m^2)\) locked-phase closures (Attack 9D) | **LIVE falsifier** (spec; not run) |
| Bounded \(\mathcal R_\star\) on a sample list | those shapes did not kill it — **not a proof**; kill lane still **LIVE** |

## What is proved / killed / open

| Claim | Status | Evidence |
|-------|--------|----------|
| Lemma★ \(\Rightarrow\) no finite-time blowup of \(\Lambda\) in this packaging \(\Rightarrow\) GR on \(\mathbb{T}^3\) **in this packaging** | **Conditional implication only** | Packaging / differential inequality; **not** a Clay submission |
| K=0 form \(T_c\le\theta\nu\mathcal D_s\) | **KILLED** | Attack 2: \(\lvert T_c\rvert/\mathcal D_s\sim B\) on fixed-shape high triad |
| Young reduction of \(T_c\) toward a norm of \(B(v,v)\) | **Partial / formal** | Polarization exists; does not close 3D product gap |
| \(\lvert T_c\rvert\le C\|v\|_2 X^{3/2}\) (or equiv) by Agmon/product | **GAP — does not close** | Attack 3 HH **input** bottleneck (not strict HH→L — no low-output restriction) |
| Uniform geometric \(C_{\mathrm{geom}}\) / \(C_0\) / \(\sup\mathcal{R}_\star<\infty\) for Lemma★ (shape form) | **OPEN — kill lane LIVE** | Definitions + claim locked; closing estimate **not proved**; sample maxes ≠ proof |
| Formula lock (linear / \(D_s\) / \(T_c\) / \(\mathcal R_\star\) / \(\Lambda'\); full shape ★) | **LOCKED in docs + unit tests** | `LEMMA_STAR_SHAPE_FORM.md`, `LEMMA_STAR_EXACT_FORMULAS.md`; `tests/test_ns_attacks_lemma_star.py` |
| Attack 8 correct record | **CORRECT RECORD** | Kill lane LIVE; \(\mathcal R_\star\) invariants; \((T_c)_+\) |
| Attack 9A packet fan \(\gamma\) | **Did not kill ★** — \(\gamma\approx-1.39\) (decaying) | \(\mathcal D_s\|v\|_2^2 Y=O(1)\) false for AP family; see `ATTACK_9A_AP_PACKET_FAILURE.md` |
| Attack 9B exact-shell \(K_{\alpha,\beta}\) | **LIVE** — \(\max_{\beta>\alpha}K\approx0.641\) at \((4,8)\); \(\max_{\beta<\alpha}K\approx0.0123\) at \((5,2)\) | **Restricted near-shell probe, not full ★**; SoT: `ATTACK_9B_EXACT_SHELL_CLOSING.md`; \((4,8)\) is **not** HH→L; controls PASS; not a kill |
| Attack 9C fixed-gap spheres | **Did not kill ★** — \(\mathcal R_\star\) \(0.11\to 0.031\) | **SoT-only** — no sweep script/data in PR #48; natural same-shell **NOT** a kill |
| Attack 9D \(\Theta(m^2)\) locked phase | **LIVE falsifier** (stub) | Designed \(\Theta(m^2)\)-closure subset with locked phases |

## What a proof would have to be

Reason from how **signed** triads add that stretching cannot get large unless spectrum also spreads or phases cancel. HH→L is the channel that could refuse that. **That reason is NOT written.** Until it is mathematics (not numerics), **do not claim global regularity.** **NS not solved.**

## Live door

1. **Prove** the boxed shape inequality (uniform \(C_{\mathrm{geom}}\) / \(\sup\mathcal R_\star<\infty\)); **or**
2. **Kill** by exhibiting a smooth shape family with \(\mathcal R_\star\to\infty\) (Attack 9D: designed \(\Theta(m^2)\) locked-phase closures; 9B: \(K_{\alpha,\beta}\to\infty\) on its **restricted** family; almost-single-shell; **not** natural fixed-gap same-shell, **not** another widening AP packet) using **complete** \(T_c\); **or**
3. Upgrade centering cancellation beyond \(T_c=-\langle B,A(A-\Lambda)v\rangle\) to remove the dangerous HH→L piece.

## Archive (NOT Lemma★)

Route N / Q6 / LP-shell floors: [`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/), [`../ARCHIVE_NOT_LEMMA_STAR.md`](../ARCHIVE_NOT_LEMMA_STAR.md). Ledgers stay linked, labeled **NOT Lemma★**.

## Related files

- `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` — **canonical full claim (absolute SoT)**
- `docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md` — triad / spectral identities
- `docs/math/ns_attacks/ATTACK_8_CORRECT_RECORD.md`
- `docs/math/ns_attacks/ATTACK_9_PACKET_FAN.md`
- `docs/math/ns_attacks/ATTACK_9A_AP_PACKET_FAILURE.md`
- `docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md`
- `docs/math/ns_attacks/ATTACK_9C_FIXED_GAP_SPHERES.md`
- `docs/math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md`
- `docs/math/ns_attacks/ATTACK_SYNTHESIS_SIMULTANEOUS.md`
- `scripts/ns_attacks/stokes_moments.py`
- `scripts/ns_attacks/attack9_packet_fan.py`
- `scripts/ns_attacks/attack9b_exact_shell_K.py`
- `tests/test_ns_attacks_lemma_star.py`
- `/opt/cursor/artifacts/attack9_packet_fan/`
- `/opt/cursor/artifacts/attack9b_exact_shell/`
