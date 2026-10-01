# Five-lane Navier–Stokes — recovered discussion and math

**Source:** [PR #48](https://github.com/simons357/Ship_it_app/pull/48) · branch `cursor/ns-five-lane-lemma-star-1390`  
**Working math:** [`docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md`](./docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md), [`docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](./docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md)  
**Harness:** `scripts/ns_attacks/run_all_five.py`  
**Status:** discussion and identity lock. **NS is not solved. Lemma★ is OPEN.**

Attacks **9A–9D are later.** They are **not** the five lanes.

---

## Recovered discussion (screenshots)

The finish screenshot records:

> Finished Five-lane NS drill  
> Five-lane drill done; K=0 dead; Lemma★ survives numeric kill only (not proved); HH→L still the gap.

That line matches the 10 September 2026 simultaneous run headline in `results/ns_five_lane_2026-09-10/SYNTHESIS_RUNTIME.json`:

```json
{
  "attack1": "SURVIVE_numeric_NOT_proof",
  "attack2": "K0_DEAD_Cstar_SURVIVES_numeric",
  "attack3": "HH_CHANNEL_LIVE_BOTTLENECK_no_closure",
  "attack4": "STOKES_IDENTITIES_OK_absorption_needs_remainder",
  "attack5": "SURVIVE_numeric_gap_remains",
  "LemmaStar_C0_killed": false
}
```

A later Grok screenshot identifies **“Lane two”** as the analytic attempt to prove an \(X^{3/2}\)-type bound.

**What the excerpts do not contain:** the complete names and assignments of the original five lanes. Those names are recovered from PR #48 files (`run_all_five.py`, Attack 1–5 notes), not from the screenshots.

---

## The original five lanes (PR #48)

`run_all_five.py` launches **exactly these five scripts**. That is the drill.

| Lane | Name in the pack | Script | What it did | Runtime (10 Sep 2026) |
|---|---|---|---|---|
| 1 | Covariance | `attack1_covariance.py` | Amplitude / phase / Galerkin ratio hygiene | SURVIVE numeric, **not** a proof |
| 2 | Triad / K=0 / \(C_*\) | `attack2_triad_k0_cstar.py` | Kill viscosity-only absorption; measure \(C_*=T_c/(X^{3/2}\Lambda)\) | **K=0 DEAD**; \(C_*\) finite on that triad only |
| 3 | Bony HH→L | `attack3_bony_hh_l.py` | Split complete signed \(T_c\) by parent-wavevector channel | HH live bottleneck; **no closure** |
| 4 | Stokes | `attack4_stokes.py` | Moment identities \(E,X,Y,Z,\Lambda,D_s\) | Identities OK; remainder still needed |
| 5 | Route-2 kill | `attack5_route2_kill.py` | Adversarial search for large \(\mathcal R_\star\) | SURVIVE numeric; sample list ≠ constant |

**Not lanes 1–5:** Attack 8 (status record), Attacks 9A–9D (later packet / shell probes). Do not relabel 9A–9D as the five-lane drill.

### “Lane two” vs \(X^{3/2}\)

Three different objects. Do not collapse them.

| Object | Scaling under \(u=av\) | Status |
|---|---|---|
| Screenshot “Lane two”: an analytic \(X^{3/2}\)-type bound | depends which form | name is **not** in the finish screenshot |
| PR #48 Lane 2, \(C_*\) form \(\lvert T_c\rvert\le C_* X^{3/2}\Lambda\) | both sides \(a^3\) | **unproved**; Attack 2 measured a sample \(C_*\), did not prove a uniform one |
| \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\) | left \(a^3\), right \(a^4\) | **false** as a universal estimate; discard by algebra |

Attack 2 in the files is the triad / K=0 / \(C_*\) **numeric** lane. It is not a written proof of any \(X^{3/2}\) bound. The discarded \(\|u\|_2 X^{3/2}\) product also appears as a prior analytic claim in the Attack 3 notes; that is the HH→L lane, not a license to treat the false product as Lane 2.

---

## Canonical mathematics

Setting: smooth, nonzero, mean-zero, divergence-free \(v\) on
\[
\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3.
\]
The torus is \(2\pi\)-normalized. Some notes take \(\|v\|_2=1\); that is optional, because \(\mathcal R_\star(av)=\mathcal R_\star(v)\).

\[
A=-P\Delta,\qquad B(v,v)=P[(v\cdot\nabla)v].
\]
\[
E=\|v\|_2^2,\quad
X=\|A^{1/2}v\|_2^2,\quad
Y=\|Av\|_2^2,\quad
Z=\|A^{3/2}v\|_2^2,\quad
\Lambda=Y/X.
\]
\[
N=-\langle B(v,v),Av\rangle,\qquad
M=-\langle AB(v,v),Av\rangle.
\]

### Centered nonlinear drift

\[
T_c=M-\Lambda N=-\bigl\langle B(v,v),\,A(A-\Lambda)v\bigr\rangle.
\]

### Centered spectral dissipation

\[
D_s=Z-\Lambda Y=Z-\frac{Y^2}{X}=\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2^2\ge 0.
\]

### Evolution identity

For a smooth unforced Navier–Stokes solution:
\[
\Lambda'=\frac{2}{X}(T_c-\nu D_s).
\]

### Original Lemma★ target

\[
T_c\le\theta\nu D_s+C_0\nu^{-1} E Y,
\]
with \(0<\theta<1\) and \(C_0\) independent of the field. **OPEN.**

### Equivalent shape target

\[
\bigl(T_c_+\bigr)^2\le C_{\mathrm{geom}}\,D_s\,E\,Y,
\qquad
T_c_+=\max(T_c,0),
\qquad
C_{\mathrm{geom}}=4\theta C_0.
\]
For \(D_s>0\),
\[
\mathcal R_\star(v)=\frac{(T_c_+)^2}{D_s\,E\,Y},
\qquad
\text{target: }\sup_v\mathcal R_\star(v)<\infty.
\]

If \(D_s=0\): one shell and \(T_c=0\). Not a kill.

### Amplitude scaling \(v\mapsto av\), \(a>0\)

\[
T_c\mapsto a^3 T_c,\quad
D_s\mapsto a^2 D_s,\quad
E\mapsto a^2 E,\quad
Y\mapsto a^2 Y.
\]
Therefore \(\mathcal R_\star\) is unchanged.

### Fourier form

\[
\lambda_k=|k|^2.
\]
\[
T_k=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr]
\quad\text{(signed; never abs-value the triad sum).}
\]
\[
T_c=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]
\[
D_s
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac1{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2.
\]
Two-shell:
\[
D_s=\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

Also \(N=\sum\lambda_k T_k\), \(M=\sum\lambda_k^2 T_k\), and \(T_c(-v)=-T_c(v)\) while \(D_s,E,Y\) are even.

---

## What the drill established (and did not)

| Claim | Status |
|---|---|
| K=0 form \(T_c\le\theta\nu D_s\) | **DEAD** (Lane 2: \(\lvert T_c\rvert/D_s\) grows with amplitude) |
| Lemma★ / \(\sup\mathcal R_\star<\infty\) | **OPEN** — survived this numeric kill only |
| HH→L closes a product bound | **No.** Still the analytic gap (Lane 3) |
| Uniform \(C_*\) or pre-Young \(C\) | **Not proved** |
| Five-lane numeric samples | **Not** a proof; one large finite \(\mathcal R_\star\) only raises \(C_{\mathrm{geom}}\) |

**Remaining target (unchanged):** prove \(\sup\mathcal R_\star<\infty\), or construct a family on which it diverges. Complete signed \(T_c\) only. Check \(-v\).

**NS not solved.**
