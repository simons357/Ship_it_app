# Original five lanes (PR 48)

**Source:** https://github.com/simons357/Ship_it_app/pull/48  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**NS not solved. ★ not proved.** Screenshots are not the pack.

Phone: [`../../FIVE-LANE-DISCUSSION.md`](../../FIVE-LANE-DISCUSSION.md).  
Math: [`../math/ns_attacks/LEMMA_STAR_CANONICAL.md`](../math/ns_attacks/LEMMA_STAR_CANONICAL.md), [`../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).  
JSON: [`COMPUTE.md`](COMPUTE.md).

---

## Recovered discussion (screenshots)

The screenshot records:

- “Finished Five-lane NS drill”
- “Five-lane drill done; K=0 dead; Lemma★ survives numeric kill only (not proved); HH→L still the gap.”

A later Grok screenshot identifies **“Lane two”** as the analytic attempt to prove an \(X^{3/2}\)-type bound.

Those excerpts **do not** name all five lanes. The assignments below are recovered from the PR 48 pack (`run_all_five.py`, `attack1`–`attack5`, `results/ns_five_lane_2026-09-10/`), not from the screenshots.

**Later attacks 9A–9D are not the five lanes.** Do not substitute them. Packet attacks 9–12 on this branch are a different campaign.

---

## The original five (locked)

From `scripts/ns_attacks/run_all_five.py`:

| Lane | Name | Script | Original target | 10 Sep verdict |
|---|---|---|---|---|
| **1** | Covariance | `attack1_covariance.py` | Amplitude / phase survival of the dimensionless ratios at fixed shape | `SURVIVE_numeric_NOT_proof` |
| **2** | Triad / K=0 / \(C_*\) | `attack2_triad_k0_cstar.py` | Kill \(T_c\le\theta\nu\mathcal D_s\); test the remainder \(\lvert T_c\rvert\le C_* X^{3/2}\Lambda\) | `K0_DEAD_Cstar_SURVIVES_numeric` |
| **3** | Bony HH→L | `attack3_bony_hh_l.py` | Split \(T_c\) into HH / HL / LL parent channels | `HH_CHANNEL_LIVE_BOTTLENECK_no_closure` |
| **4** | Stokes | `attack4_stokes.py` | Moment identities, \(\mathcal D_s\ge 0\), viscous absorption is not enough | `STOKES_IDENTITIES_OK_absorption_needs_remainder` |
| **5** | Route 2 | `attack5_route2_kill.py` | Numeric kill/bound of \(\mathcal R_\star\) on a search list | `SURVIVE_numeric_gap_remains` |

Headline of that run: `kill_lane: LIVE`. `lemma_star: OPEN`. `LemmaStar_C0_killed: false`.

Notes for lane 1–5 docs: [`../math/ns_attacks/ATTACK_1_COVARIANCE.md`](../math/ns_attacks/ATTACK_1_COVARIANCE.md), [`ATTACK_2_TRIAD_K0_CSTAR.md`](../math/ns_attacks/ATTACK_2_TRIAD_K0_CSTAR.md), [`ATTACK_3_BONY_HH_L.md`](../math/ns_attacks/ATTACK_3_BONY_HH_L.md), [`ATTACK_4_STOKES.md`](../math/ns_attacks/ATTACK_4_STOKES.md), [`ATTACK_5_ROUTE2.md`](../math/ns_attacks/ATTACK_5_ROUTE2.md).

---

## Lane two and the two \(X^{3/2}\) objects

Do not merge these.

**Original lane 2** (the pack): the remainder
\[
\lvert T_c\rvert\le C_* X^{3/2}\Lambda.
\]
Under \(u=av\) both sides scale as \(a^3\). Amplitude-invariant. K=0 died on the same lane. Numeric \(C_*\approx 0.004058\) on that triad is **not** \(C_{\star}=\sqrt{\sup\mathcal R_\star}\). Not a theorem.

**The other \(X^{3/2}\) line** (older “missing inequality,” sometimes hung on lane 3 / PRODUCT-BLOCK):
\[
\lvert T_c\rvert\le C\|u\|_2 X^{3/2}.
\]
Under \(u=av\): left \(a^3\), right \(a^4\). **DEAD BY SCALING.** Not an open gap toward ★. Not original lane 2.

The Grok screenshot’s “Lane two = analytic \(X^{3/2}\) bound” names the **type** of remainder on lane 2. It does not prove that remainder, and it does not revive the \(a^4\) bound.

---

## Not the five lanes

| Later | What it is |
|---|---|
| Attack 6 | Uniform pre-Young \(C\) in \(\lvert T_c\rvert\le C\|u\|_2 X\Lambda\) — **dead** (\(\sim s\)) |
| Attack 8 (this branch) | Three-key probe. Five-lane `ATTACK_8_CORRECT_RECORD.md` is a different file on PR 48 (name collision; not copied) |
| **9A** | AP packet. \(\mathcal D_s\) wins. Not a kill |
| **9B** | Exact-shell \(K_{\alpha,\beta}\). Finite max. Not a kill |
| **9C** | Fixed-gap spheres = Attack 11 here. Not a kill |
| **9D** | Designed \(\Theta(m^2)\) = Freiman-AP, already dead. Screenshot fixed-output \(\Theta(m^2)\) is a counting error |
| Attack 12 | Lattice HH→L **fan**. Not five-lane Attack 3 |

HH→L in the screenshot (“still the gap”) is original **lane 3** (Bony channel diagnostic). After the \(a^4\) death, that lane does not supply a live product target. The lattice fan is a later packet. Do not merge them.

---

## Canonical mathematics (agrees)

Smooth, nonzero, mean-zero, divergence-free \(v\) on \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\). The identities keep \(E=\|v\|_2^2\). Setting \(E=1\) is optional: \(\mathcal R_\star\) is unchanged under \(v\mapsto av\).

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
\[
T_c=M-\Lambda N=-\langle B(v,v),A(A-\Lambda)v\rangle.
\]
\[
\mathcal D_s=Z-\Lambda Y=Z-Y^2/X=\|(A-\Lambda)A^{1/2}v\|_2^2\ge 0.
\]

For a smooth unforced Navier–Stokes solution:
\[
\Lambda'=\frac{2}{X}(T_c-\nu\mathcal D_s).
\]

Original ★ (viscosity packaging), \(0<\theta<1\), \(C_0\) independent of the field:
\[
T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}EY.
\]

Equivalent shape target:
\[
(T_{c+})^2\le C_{\mathrm{geom}}\,\mathcal D_s\,E\,Y,
\qquad
T_{c+}=\max(T_c,0),\qquad
C_{\mathrm{geom}}=4\theta C_0.
\]
\[
\mathcal R_\star(v)=\frac{(T_{c+})^2}{\mathcal D_s\,E\,Y}\qquad(\mathcal D_s>0).
\]
The target is \(\sup_v\mathcal R_\star(v)<\infty\).

Amplitude \(v\mapsto av\), \(a>0\): \(T_c\to a^3 T_c\), \(\mathcal D_s\to a^2\mathcal D_s\), \(E\to a^2 E\), \(Y\to a^2 Y\). Therefore \(\mathcal R_\star\) is unchanged.

Fourier (\(\lambda_k=|k|^2\); signed \(\mathrm{Im}\), no abs):
\[
T_k=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr],
\qquad
T_c=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]
\[
\mathcal D_s
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac{1}{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2.
\]

Four corrections remain in force: the \(a^4\) missing inequality is dead; ★ \(\Rightarrow\) GR in this packaging, not equivalent; test both signs of \(T_c\); Section 4 is not proved. Near-shell limit equals \(K_{\alpha,\beta}\) only for aligned, sign-selected \(z_\beta\).

Remaining job: uniform \(\mathcal R_\star\), or a family that diverges. One large finite value is not a kill.

**NS not solved.**
