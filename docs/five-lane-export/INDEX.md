# Five-lane Lemma★ — search hits

Dated 10 September 2026. Recovery, not a proof.
**NS not solved. ★ not proved.**

This is what sat on disk / GitHub. Not LAST-KEY.
Not Hyp-Lat. Not an Origin `codebase/.../pull/48` URL.

---

## Highest-priority hits (found)

| What | Where |
|---|---|
| PR **#48** | https://github.com/simons357/Ship_it_app/pull/48 |
| Branch | `cursor/ns-five-lane-lemma-star-1390` |
| Title | Five-lane Lemma★ drill: K=0 dead, ★ survives numeric |
| Agent (PR footer) | https://cursor.com/agents/bc-01a00412-6516-7002-95f2-051faf8ba0eb |
| Sync PR **#50** | https://github.com/simons357/Ship_it_app/pull/50 |
| Packaging PR **#49** | https://github.com/simons357/Ship_it_app/pull/49 |
| Shape PRs **#51, #52** | R★ shape / exact Fourier formulas |

**Origin URL `https://cursor.com/codebase/.../pull/48`:**
**not found** on this machine, in git, or in PR
bodies. GitHub PR 48 is the pack.

---

## Not found

- `LAST-KEY-LEMMA-STAR`
- `Hyp-Lat` / `Lat-Emb` as files
  (Hyp-ST★ is this branch:
  [`../LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md`](../LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md);
  Hyp-Lat★ is **not written**)
- Downloads copies
- `cursor.com/codebase/` links

---

## 1. Absolute defs (five-lane pack)

Canonical lock, copied here:
[`LEMMA_STAR_SHAPE_FORM.md`](LEMMA_STAR_SHAPE_FORM.md).

On \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\),
\(A=-P\Delta\), \(\lambda_k=|k|^2\), \(k\cdot v_k=0\):

\[
\begin{aligned}
\|v\|_2^2 &= \sum|v_k|^2,\\
X &= \|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2,\\
Y &= \|Av\|_2^2=\sum\lambda_k^2|v_k|^2,\\
Z &= \|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2,\\
\Lambda &= Y/X,\\
\nu &= \text{viscosity (PDE; cancels in }\mathcal R_\star\text{)},\\
\theta &\in(0,1)\text{ Young slice}.
\end{aligned}
\]

Code alias \(E=\|v\|_2^2\).

\[
\mathcal D_s=Z-\Lambda Y=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2\ge 0.
\]

\[
T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k,
\]
\[
T_k=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr]
\quad\text{(signed; no abs)}.
\]

**Lemma★ (viscosity packaging):**
\[
T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2\,X\Lambda,
\]
\(C_0\) geometry-only. Equivalent shape form:
\[
(T_c)_+^2\le C_{\mathrm{geom}}\,\mathcal D_s\,\|v\|_2^2\,Y,
\qquad
\mathcal R_\star=\frac{(T_c)_+^2}{\mathcal D_s\|v\|_2^2 Y},
\quad C_0=C_{\mathrm{geom}}/(4\theta).
\]

**Not ★:** Attack-2 remainder
\(|T_c|\le C_* X^{3/2}\Lambda\). K=0
(\(T_c\le\theta\nu\mathcal D_s\)) is **dead**.

Same defs live on this branch:
`scripts/ns_attacks/stokes_moments.py`,
[`../LEMMA-STAR.md`](../LEMMA-STAR.md),
[`../LEMMA-STAR-R.md`](../LEMMA-STAR-R.md).

---

## 2. Exact HH→L map (two writings)

**A. Bony channel (five-lane Attack 3).**
Parents \(p,q\) of a triad \(p+q=k\). Cut \(k_{\mathrm{cut}}\):

- HH: \(|p|\ge k_{\mathrm{cut}}\) and \(|q|\ge k_{\mathrm{cut}}\)
- HL: exactly one of \(|p|,|q|\) high
- LL: both low

\(T_c\) recomputed with \(B\) restricted to each
channel. Target bound that HH→L blocks:
\[
|T_c|\le C\|u\|_2 X^{3/2}.
\]
Diagnostic only. No closure.
[`ATTACK_3_BONY_HH_L.md`](ATTACK_3_BONY_HH_L.md),
`attack3_bony_hh_l.py`.

**B. Lattice fan (this branch, Attack 12).**
Low key \(k\) on shell \(\beta=|k|^2\). High partners
\(p,q\) on sphere \(\alpha\) with \(p+q=k\).
Incompressibility:
\[
k\cdot p=\beta/2\qquad\Rightarrow\qquad |q|^2=\alpha.
\]
Pair counts 2–12, not \(\Theta(m^2)\).
\(\mathcal R_\star\sim\beta/\alpha\). No blow.
`scripts/ns_attacks/attack12_hh_l_fan.py`,
`hh_l_sphere_pairs` / `hh_l_one_key_field` /
`hh_l_whole_shell_field` in
`scripts/ns_attacks/stokes_moments.py`.
Score: [`../LEMMA-STAR-PACKET.md`](../LEMMA-STAR-PACKET.md).

Do not merge A and B as one theorem. A is a
product-estimate gap. B is a lattice packet.

---

## 3. Whole PR #48

GitHub: https://github.com/simons357/Ship_it_app/pull/48

This export is the Lemma★ slice only. PR 48
also dumped SND / Q6 / SFE papers. **Do not
merge that pile onto this branch.** Archive
on that PR: `docs/math/ARCHIVE_NOT_LEMMA_STAR.md`.

Copied here: shape form, Attack 3, headline,
shape-star summary, proof-status board,
attack3 script.

**Original computation (the JSON, not a re-proof):**
[`COMPUTE.md`](COMPUTE.md).
`results/ns_five_lane_2026-09-10/`,
`results/ns_five_lane_shape_star/`.
Scripts: `scripts/ns_attacks/run_all_five.py`,
`attack1`–`attack5`.

---

## Five-lane headline (already scored here)

K=0 dead. Uniform pre-Young \(C\) dead.
★ survives numeric kill only (not a proof).
HH→L analytic bound still missing.
Lattice fan: no kill. Enumerator still live.
H1 is a different integral.
