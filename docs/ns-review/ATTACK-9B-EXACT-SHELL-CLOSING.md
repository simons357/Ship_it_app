# Attack 9B — Exact-shell coherent fan + small closing packet

**Date:** 2026-09-10  
**Name (locked):** **Attack 9B — Exact-shell + closing packet**  
**Branch lineage:** DA (`cursor/da-attack9b-sot-0cc5`) ↔ five-lane (`cursor/ns-five-lane-lemma-star-1390`)  
**Prior:** Attack 9A (AP packet) = **negative for kill** — [`ATTACK-9-COHERENT-PACKET-FAN.md`](./ATTACK-9-COHERENT-PACKET-FAN.md)  
**Also prior / next SoT:** Attack **9C** fixed-gap spheres = **not a kill** — [`ATTACK-9C-FIXED-GAP-SPHERES.md`](./ATTACK-9C-FIXED-GAP-SPHERES.md)  
**Depends on:** exact \(\mathcal R_\star\) ([`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md))  
**Status:** **LIVE kill attempt** (numerics). Finite sample **NOT** a kill. Lemma★ **OPEN**. **NS NOT SOLVED.** No SFE. Kill lane **LIVE**.  
**Canonical five-lane twin:** [`../math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md`](../math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md)

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

## Boxed quantity \(K_{\alpha,\beta}\)

\[
\boxed{
K_{\alpha,\beta}
=
\sup_{A w=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
}
\]

If \(\sup_{\alpha,\beta}K_{\alpha,\beta}=\infty\), then \(\sup\mathcal{R}_\star=\infty\) along the corresponding \(\varepsilon\to0\) family → **★ dead**.  
Finite sample maxima are **not** a proof that \(K\) is bounded; kill lane stays **LIVE**.

Code: `domain_architect/kab_quantity.py`; probe: `scripts/ns_attacks/attack9b_exact_shell_K.py`.

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

## After 9B (SoT naming)

| Attack | Role | Status |
|--------|------|--------|
| **9A** AP packet | Widening coherent fan | **Did not kill** |
| **9B** Exact-shell + closing (this doc) | \(K_{\alpha,\beta}\) | **LIVE**; finite sample \(\max K\approx0.641\) **not** a kill |
| **9C** Fixed-gap spheres | Natural same-shell; \(D_s\) from gap; closures \(O(m)\) | **Did not kill** (\(0.11\to0.031\)) — [`ATTACK-9C-FIXED-GAP-SPHERES.md`](./ATTACK-9C-FIXED-GAP-SPHERES.md) |
| **9D** \(\Theta(m^2)\) locked phases | Remaining packet falsifier | **LIVE** (spec) — [`ATTACK-9D-THETA-M2-LOCKED-PHASE.md`](./ATTACK-9D-THETA-M2-LOCKED-PHASE.md) |

**Rename note:** Earlier DA docs called \(\Theta(m^2)\) “9C” — **renamed to 9D** to match user SoT.

---

## Required controls

| Control | Expectation |
|---------|-------------|
| Amplitude: \(K(aw)=K(w)\); \(\mathcal{R}_\star(av)=\mathcal{R}_\star(v)\) | Exact |
| Exact-shell \(\varepsilon=0\): \(\mathcal{D}_s\approx0\) | Pass (machine eps) |
| \(\varepsilon\to0\) probe: \(\mathcal{R}_\star(v_\varepsilon)\to K_{\alpha,\beta}(w)\) | Relative error \(\to0\) |
| Report **total** signed \(T_c\) | Not HH→L-only |

---

## Script

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9b_exact_shell_K.py \
  --outdir /opt/cursor/artifacts/attack9b_exact_shell
```

Artifacts target: `/opt/cursor/artifacts/attack9b_exact_shell/` (`attack9b.json`, `HEADLINE.md`, plots).  
**This environment:** `/opt/cursor/artifacts/attack9b_exact_shell/` was **missing** at encode time; HEADLINE locked under `results/ns_five_lane_2026-09-10/attack9b_exact_shell/HEADLINE.md`.

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
| \(\max K\) seen | \(\approx 0.641\) at \((\alpha,\beta)=(4,8)\) |
| Controls / \(\varepsilon\)-limit | **PASS** |
| Verdict | Finite sample — **not** a kill; kill lane **LIVE** |

Copied HEADLINE excerpt: max K = `0.6410131735094131` at `(4, 8)`; `controls_all_pass=True`; `eps_limit_all_pass=True`.

**Refuse:** “9B killed ★.” Finite \(K\) sample ≠ kill. **NS not solved.**

---

## Hard refusals

- Refuse “AP packet closed kill lane.”
- Refuse “9B killed ★” / “exact-shell sample closed kill lane.”
- Refuse “same-shell ensemble kills ★.”
- Refuse “kill lane closed” from 9A, 9B, 9C, or 9D.
- Refuse greening ★ / “almost proved” / “numerics prove ★.”
- Refuse treating “narrow packet” as automatic \(D_s=O(1)\).
- Refuse another widening AP packet as the next clean test.

---

## Jonathan action

**None.**

**NS NOT SOLVED.**
