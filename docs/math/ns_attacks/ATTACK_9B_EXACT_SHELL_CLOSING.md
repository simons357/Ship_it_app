# ATTACK 9B — Exact-shell coherent fan + small closing packet

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Status:** **LIVE kill attempt** (numerics). Lemma★ **OPEN**. Bound on \(C_{\mathrm{geom}}\) / \(\sup\mathcal{R}_\star\) **OPEN**. **NS not solved.** Kill lane **LIVE**.  
**Prior:** Attack 9A (AP packet) did **not** kill ★ — see [`ATTACK_9A_AP_PACKET_FAILURE.md`](./ATTACK_9A_AP_PACKET_FAILURE.md).  
**Pack locator:** [`FIVE_LANE_PACK_LOCATOR.md`](./FIVE_LANE_PACK_LOCATOR.md) — PR https://github.com/simons357/Ship_it_app/pull/48  
**Full Lemma★ SoT:** [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md)  
**Triad identities:** [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md)
**Status docs:** LIVE lock [`PROOF_LemmaStar_LIVE_LOCK.md`](./PROOF_LemmaStar_LIVE_LOCK.md); annotated proof-attempt archive [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md) (does **not** green ★; unconditional ★ **OPEN**).

**Canonical quotient:** code name `ratio_R_star_shape` \(=\mathcal{R}_\star=(T_c)_+^2/(D_s\|v\|_2^2 Y)\). Alias `ratio_R_star` → same. Legacy `ratio_star` \(=T_c/(E X\Lambda)\) is a **different** post-Young object — do **not** confuse with \(\mathcal{R}_\star\).  
(Alias: older docs write \(\mathcal{D}_s\) for the same \(D_s=Z-Y^2/X\).)

> **CRITICAL — scope of \(K_{\alpha,\beta}\):**  
> Near-shell \(K_{\alpha,\beta}\) tests **only a restricted limiting family** (exact eigen-shell \(+\,\varepsilon\) closing).  
> It is **not** the full Lemma★. The full lemma is the boxed shape inequality
> \((T_c)_+^2\le C_{\mathrm{geom}}\,D_s\|v\|_2^2 Y\) over all smooth divergence-free mean-zero fields
> (equivalently \(\sup\mathcal{R}_\star<\infty\)). See [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md).

---

## Family

Dominant exact Stokes eigen-shell plus a small closing component:
\[
v_\varepsilon=w_\alpha+\varepsilon z_\beta,\qquad
Aw_\alpha=\alpha w_\alpha,\qquad
Az_\beta=\beta z_\beta.
\]
Choose the closing direction to align with the projected self-interaction on shell \(\beta\):
\[
z_\beta\parallel\Pi_\beta B(w_\alpha,w_\alpha).
\]
The base packet \(w_\alpha\) may contain **many same-shell modes** (coherent fan). Spectral variance \(\mathcal{D}_s\) is generated **only** by the small closing component when \(\varepsilon>0\). At \(\varepsilon=0\), exact single shell \(\Rightarrow\mathcal{D}_s=0\) (and typically \(T_c=0\): vacuous, not a kill).

---

## Boxed quantity (restricted near-shell probe — NOT the full lemma)

\[
\boxed{
K_{\alpha,\beta}
=
\sup_{Aw=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
}
\]

This \(K_{\alpha,\beta}\) is a **restricted near-shell / limiting-family test**. Bounding sample \(K\) does **not** prove the full Lemma★ (\(C_{\mathrm{geom}}\) / \(\sup\mathcal{R}_\star\) remain **OPEN**); unbounded \(K\) on this family would kill ★ along that family, but finite \(K\) on this family does **not** close the full lemma.

If \(\sup_{\alpha,\beta}K_{\alpha,\beta}=\infty\), then \(\sup\mathcal{R}_\star=\infty\) along the corresponding \(\varepsilon\to0\) family → **★ dead**.  
Finite sample maxima are **not** a proof that \(K\) is bounded and are **not** a proof of ★; kill lane stays **LIVE**.

---

## CRITICAL callout — \(\beta>\alpha\) is NOT HH→L

> **Runtime max \(K\approx0.641\) at \((\alpha,\beta)=(4,8)\) is NOT HH→L.**  
> That pair has \(\beta>\alpha\) = transfer to a **higher** shell.  
> Genuine HH→L needs \(\beta<\alpha\) (output on a **lower** shell).  
> Always report \(\max K\) for \(\beta>\alpha\) and \(\beta<\alpha\) **separately**.

| Subfamily | Meaning | Sample max \(K\) (seed 1390, kmax≤10 shells) |
|-----------|---------|----------------------------------------------|
| \(\beta>\alpha\) | Higher-shell transfer — **NOT** HH→L | \(\approx 0.641\) at \((\alpha,\beta)=(4,8)\) |
| \(\beta<\alpha\) | Genuine HH→L subfamily | \(\approx 0.0123\) at \((\alpha,\beta)=(5,2)\) |

**Attack 3** is also **not** a strict HH→L map — it filters high-frequency **inputs** without restricting **output** to low frequencies; see [`ATTACK_3_BONY_HH_L.md`](./ATTACK_3_BONY_HH_L.md).

---

## \(\varepsilon\to0\) analysis (two-shell asymptotics)

Normalize \(\|w\|_2=1\), \(\|z\|_2=1\), \(z=\pm\Pi_\beta B(w,w)/\|\Pi_\beta B(w,w)\|_2\) (sign for \((T_c)_+>0\)). Energies \(e_\alpha=1\), \(e_\beta=\varepsilon^2\).

Two-shell closed form:
\[
\mathcal{D}_s
=\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}
\sim\beta(\alpha-\beta)^2\varepsilon^2.
\]
\[
Y\sim\alpha^2,\qquad \|v\|_2^2\sim1,\qquad\Lambda\to\alpha.
\]

Energy identity \(\sum T_k=0\) and leading \(\beta\)-shell transfer from \(B(w,w)\) give
\[
T_c(v_\varepsilon)\sim\beta(\beta-\alpha)\,\varepsilon\,\|\Pi_\beta B(w,w)\|_2
\]
(up to the alignment sign; take the stretch orientation so \(T_c>0\)).

Hence
\[
\mathcal{R}_\star(v_\varepsilon)
=\frac{(T_c)_+^2}{\mathcal{D}_s\|v\|_2^2 Y}
\;\xrightarrow{\varepsilon\to0}\;
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2}
\]
for unit \(w\). The \((\alpha-\beta)\) factors cancel between numerator and \(\mathcal{D}_s\). \(\varepsilon\) cancels in the limiting quotient.

**Relation:** for each fixed exact-shell \(w\),
\[
\lim_{\varepsilon\to0}\mathcal{R}_\star(w+\varepsilon z_\beta(w))=K_{\alpha,\beta}(w)
\le K_{\alpha,\beta}.
\]

---

## Caveat

Exact shell \(\Rightarrow\mathcal{D}_s=0\) at \(\varepsilon=0\). A merely “narrow” (finite-thickness) packet does **not** auto-keep \(\mathcal{D}_s=O(1)\):
\[
\mathcal{D}_s=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
\]
amplifies small lattice eigenvalue gaps.

---

## After 9B (SoT)

**Attack 9C** — fixed-gap spheres \(n\) and \(n+d\): \(\mathcal{D}_s\) from the **gap** (not packet width); natural closures only \(O(m)\); \(\mathcal{R}_\star\) **falls** with \(n\) (\(0.11\to 0.031\)), does **not** track \(m^{1/2}\). Natural same-shell ensemble is **NOT** a kill.  
**SoT-only until implemented** — snapshot records \(0.11\to0.031\) but **lacks** a supporting fixed-gap sweep script/data in PR #48.  
Doc: [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md).

**Next falsifier (9D):** designed \(\Theta(m^2)\)-closure subset with **locked phases** — [`ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](./ATTACK_9D_THETA_M2_LOCKED_PHASE.md).

---

## Required controls

| Control | Expectation |
|---------|-------------|
| Amplitude: \(K(aw)=K(w)\); \(\mathcal{R}_\star(av)=\mathcal{R}_\star(v)\) | Exact |
| Exact-shell \(\varepsilon=0\): \(\mathcal{D}_s\approx0\) | Pass (machine eps) |
| \(\varepsilon\to0\) probe: \(\mathcal{R}_\star(v_\varepsilon)\to K_{\alpha,\beta}(w)\) | Relative error \(\to0\) |
| Report **total** signed \(T_c\) | Not HH→L-only |
| Report \(\max K\) for \(\beta>\alpha\) and \(\beta<\alpha\) **separately** | Required |

---

## Script

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9b_exact_shell_K.py \
  --outdir /opt/cursor/artifacts/attack9b_exact_shell
```

Artifacts: `/opt/cursor/artifacts/attack9b_exact_shell/` (`attack9b.json`, `HEADLINE.md`, `NOTES_BETA_SPLIT.md`, plots).

---

## Decisive output

| Outcome | Meaning |
|---------|---------|
| Sample \(K_{\alpha,\beta}\) unbounded / growing with shell size | Counterexample route still open |
| Bounded sample max on tested pairs | Those shells did not kill ★ — **not** a proof; kill lane LIVE |
| \(\varepsilon\)-limit fails to match \(K\) | Implementation / alignment bug — fix before claiming |

---

## Runtime 2026-09-10 (seed 1390)

| Metric | Value |
|--------|-------|
| \(\max K\) all pairs | \(\approx 0.641\) at \((\alpha,\beta)=(4,8)\) — **\(\beta>\alpha\)**, NOT HH→L |
| \(\max K\) with \(\beta>\alpha\) (higher shell) | \(\approx 0.641\) at \((4,8)\) |
| \(\max K\) with \(\beta<\alpha\) (genuine HH→L) | \(\approx 0.0123\) at \((5,2)\) |
| Controls / \(\varepsilon\)-limit | **PASS** |
| Verdict | Finite sample — **not** a kill; kill lane **LIVE** |

Re-run confirmation (same `--seed 1390 --kmax 6`): same argmax pairs; \(\max_{\beta>\alpha}K\approx0.656\) at \((4,8)\), \(\max_{\beta<\alpha}K\approx0.0126\) at \((5,2)\) — optimizer scatter only; β-split unchanged. See `/opt/cursor/artifacts/attack9b_sot_rewrite/BETA_SPLIT_CONFIRM.md`.

Artifacts: `/opt/cursor/artifacts/attack9b_exact_shell/` (`attack9b.json`, `HEADLINE.md`, `NOTES_BETA_SPLIT.md`, `K_by_ab_pair.png`, `R_star_eps_limit.png`).

**NS not solved.**

---

## Next

[`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md) → [`ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](./ATTACK_9D_THETA_M2_LOCKED_PHASE.md).
