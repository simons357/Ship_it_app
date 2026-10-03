# L3 shear obstruction — ingest (3 Oct 2026)

**Source:** Jonathan upload `L3-5-Exact-Shear-Obstruction-2026-10-03.txt`  
**Archive:** [`archives/l3-shear/L3-5-Exact-Shear-Obstruction-2026-10-03.txt`](./archives/l3-shear/L3-5-Exact-Shear-Obstruction-2026-10-03.txt)  
**Cited upstream:** [PR #153](https://github.com/simons357/Ship_it_app/pull/153) head `ce8b1ee585aa89be77fa41f7a69748cb2a82da5a` (`docs/L3-BUDGET-GATES.md`, `docs/FOURIER-TRIANGLE.md`)  
**Honesty locks (sibling ns-review cards when present):** unaugmented face / \(T_{j\leftarrow j}\) OPEN · TJ candidates C6–C12 · PRODUCT-BLOCK OPEN · no Clay.

**Claim line:** No Clay. Absolute (A) not seated and not killed. Energy-only L3-budget strengthening **DEAD**. Datum-sensitive L3-5 **OPEN**. Signed scalene route (17) **not refuted**.

---

## 0. Verdict in one line

Exact parallel-shear trajectories kill any **universal** \(F(E_0,\nu,K,T)\) bound on the \(\Lambda\)-weighted high-frequency \(L^3\) budget \(S3\), including \(K=K(E_0,\nu)\). They do **not** kill L3-5 as quantified (datum-dependent \(K\) / budget). Transfer is identically zero, so this is a wrong-proxy rejection test, not a regularity counterexample.

---

## 1. What the note proves / kills / leaves open

### Proved (analytic; elementary trajectories)

- Family \(u_{m,L}\) of smooth, unforced, mean-zero, divergence-free 3D periodic NSE solutions with \((u\cdot\nabla)u\equiv 0\), heat evolution only, exact full Galerkin solutions when \(N\) contains the support.
- Fixed initial energy \(E(0)=a^2\) and viscosity \(\nu\); total dissipation budget \(\int_0^T X\le a^2/(2\nu)\) independent of \(m,L\).
- Analytic lower bound \(\|u(t)\|_3\ge d\,a\,L^{1/6}\) on a viscous window \(\tau_m=1/(16\nu m^2)\).
- Integrated excess: for \(m>K\) and \(T\ge\tau_m\),
  \[
  S3_{K,N}(T)\ge\frac1{16\nu}\bigl[d\,a\,L^{1/6}-c\nu\bigr]_+
  \]
  which \(\to\infty\) as \(m\to\infty\) with \(L=m\) (and still diverges on a relative near-shell subfamily \(m=j^2\), \(L=j\)).
- On the same trajectories: \(T_{\mathrm{sc}}=T_{\mathrm{rep}}=T(u)=0\) and signed budget \(S_{K,N}(T)=0\).
- Hence no uniform reverse comparison \(S3\le C\,S+F(E_0,\nu,K,T)\).

### Killed

| Claim | Status |
| --- | --- |
| Universal \(S3\le F(E_0,\nu,K,T)\) for all smooth data of energy \(E_0\), all \(N\) | **DEAD** |
| Same with \(K\) chosen from \(E_0,\nu\) (or \(E_0,\nu,T\)) only | **DEAD** |
| Energy-only strengthening of L3-5 | **DEAD** |
| Two-way algebraic interchangeability of \(S3\) and signed \(S\) via L3-4 | **DEAD** (L3-4 remains one-way) |

### Not killed / still open

| Claim | Status |
| --- | --- |
| L3-5 as written: for each fixed smooth \(u_0,\nu\), some \(K(u_0,\nu)\) with \(\sup_N S3_{K,N}(T)<\infty\) | **OPEN** (datum-sensitive) |
| Repeated-radius estimate; original signed scalene budget / criterion (17) | **not refuted** (holds trivially \(0=0\) here) |
| Global regularity / Clay | **untouched** |
| Absolute (A) / depletion \(\Rightarrow\) (A) | **untouched** |
| Fixed absolute squared-radius strip estimates | **not refuted** (near-shell width grows) |
| Absolute radial variance \(D_s\) bounds | **not claimed** |
| Single smooth datum with diverging Galerkin budgets | **not constructed** |
| Uniform initial-\(H^1\) counterfamily | **not constructed** |

Note’s own status line (kept): energy-only L3 strengthening falsified; L3-5 as in PR #153 remains open; signed scalene route (17) not refuted.

---

## 2. Map to candidate map / live doors

| Seat | Relation to this note | Status after ingest |
| --- | --- | --- |
| **C6** (\(\alpha_+\) hinge) | Shears have zero nonlinearity ⇒ stretch / production zero, while \(S3\) can still diverge. Shows \(L^3\) high-tail cost is **not** a proxy for \(\alpha_+\) production. Does **not** control \(\alpha_+\) and does **not** kill the C6 TRY seat. | **TRY unchanged** |
| **C7** (HH / near-shell) | Relative near-shell shear with growing occupancy drives \(S3\to\infty\) at zero transfer. Reinforces: energy-only / occupancy \(L^3\) mass ≠ HH product bound. Consistent with naive energy-only HH already **DEAD**. Geometric HH product still missing. | **TRY unchanged** (energy-only HH still dead) |
| **C10** (depletion \(\Rightarrow\) (A), principal) | Untouched. Note redirects priority to signed production (17), not to a non-circular depletion theorem. | **TRY / empty** |
| **C11** (\(T^{\mathrm{mm}}\), axisym) | Parallel shears are not the mixed swirl+meridional axisym class. Orthogonal. | **TRY unchanged** (axisym-conditional) |
| **\(T_{j\leftarrow j}\)** | All ordered interactions vanish (collinear shear supports). Subclass zero — same honesty as pure-swirl checks: not a class bound. | **OPEN** |
| **PRODUCT-BLOCK** / \(\sup\mathcal{R}_\star\) | Different face (Lemma★ trunk). Not addressed. | **OPEN** |
| **Ring / SND** (C12) | Not addressed. | **conditional-only** |
| **Absolute (A)** | Not seated; not falsified. Zero-transfer shears do not probe \(\rho_j<\nu\) under active same-scale flux. | **OPEN / not claimed** |

**Priority implication (from the note, accepted):** stop selling energy-only \(S3\) as a regularity gate; keep signed scalene / actual nonlinear production as the budget that vanishes on these examples. Any continued L3-5 proof must name the datum-sensitive high-frequency input and control nonlinear regeneration without presupposing uniform \(H^1\) / ESS.

---

## 3. Honesty check (overclaim refuse)

| Tempting package | Verdict |
| --- | --- |
| “L3-5 is dead” | **OVERCLAIM** — only the **energy-only strengthening** is dead; PR #153 quantifiers remain open |
| “Kills the L3 route / all energy-geometry arguments” | **OVERCLAIM** — note explicitly refuses this |
| “Refutes (17) / repeated-radius / global regularity” | **FALSE** — note says the opposite |
| “Clay progress / Clay obstruction” | **REFUSE** — no Clay claim; family is globally smooth |
| “Kills absolute (A)” or “proves (A)” | **REFUSE** — (A) not in scope; \(T\equiv 0\) |
| “Closes \(T_{j\leftarrow j}\) / PRODUCT-BLOCK” | **REFUSE** — transfer vanishes by geometry of the subclass |
| “Single-datum Galerkin blowup of \(S3\)” | **not constructed** |
| Note’s own claim boundary (§7–§10) | **KEEP** — careful; independent review still appropriate |

Computational checks in the note are implementation probes only (divergence-free / vanishing ordered dots / moments). The obstruction itself is analytic.

---

## 4. Files

- Source archive: `docs/ns-review/archives/l3-shear/L3-5-Exact-Shear-Obstruction-2026-10-03.txt`
- This summary: `docs/ns-review/L3-SHEAR-OBSTRUCTION-2026-10.md`
- Index: `docs/ns-review/README.md`
- PR paste card: `docs/ns-review/PR-DRAFT-L3-SHEAR-OBSTRUCTION.md`
