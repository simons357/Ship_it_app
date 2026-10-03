# Ring Lemma reconciliation — three Oct 2 uploads vs July ledger / Oct locks

**Date:** 2026-10-03  
**Branch:** `cursor/ring-lemma-reconcile-0cc5`  
**Sources ingested:** [`ring-lemma/`](./ring-lemma/) (from Jonathan’s Oct 2 uploads)  
**Governing locks:** [`CLAIM-LEDGER-AUDIT-2026-10.md`](./CLAIM-LEDGER-AUDIT-2026-10.md) · [`SCIENTIFIC-REPORT.md`](./SCIENTIFIC-REPORT.md) · [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md) · [`TJ-SAME-SCALE-CANDIDATES.md`](./TJ-SAME-SCALE-CANDIDATES.md)

**Rules:** No Clay. SND = texture. NS-10 OPEN. NS-11 not claimed. NS-6 Ring needs scoped relabel. Numerics ≠ proof.

---

## 0. Plain English (for Jonathan)

**What the Ring Lemma is now.** A **spatial** bound on how fast the vorticity direction \(\xi=\omega/|\omega|\) can vary, for **band-limited** (single-shell / frequency-cutoff) fields on \(\mathbb{T}^3\). The Oct 2 corrected note proves: on the \(L^2\)-threshold set \(E_c=\{|\omega|\ge c\|\omega\|_2\}\), \(\|\nabla\xi\|_{L^\infty(E_c)}\lesssim L^{5/2}/c\), and that power is sharp. Under an extra amplitude hypothesis (\(|\omega|\) comparable to \(\|\omega\|_\infty\), or \(\|\omega\|_\infty\lesssim A\|\omega\|_2\)), the bound drops to order \(L\). That is geometry. It is **not** a Navier–Stokes theorem.

**What still needs proving.**

| Gap | Status |
| --- | --- |
| Classical dynamical SND (legacy NS-10) | **OPEN** — hypothesis / C12 texture only |
| Same-scale shell transfer \(T_{j\leftarrow j}\) | **OPEN** (unaugmented face) |
| PRODUCT-BLOCK / \(\sup\mathcal{R}_\star<\infty\) | **OPEN** (Lemma★ hinge) |
| Absolute \(\alpha_+\) / stretch control | **OPEN** / not seated |
| Classical 3D NS regularity (NS-11) | **NOT CLAIMED** |

**June 19 TeX vs Oct 2 corrected note.** The June 19 manuscript’s Ring Lemma geometry (**linear** \(2^{j^*}\) on \(E_c\) from Bernstein mishandling) is **superseded / withdrawn as geometry** by the Oct 2 note. Keep June 19 as **archive of the augmented-program narrative and overclaims**, not as geometric SoT. The Oct 2 note **does not** salvage June’s dashboard “Main Theorem / CF closes / SND for classical is the only gap” packaging.

**No Clay claim.** Ring geometry alone never implies Clay Statement B.

---

## 1. What each uploaded file claims

### 1.1 Ledger reconciliation text (`RingLemma_Ledger_Reconciliation_2026-10-02`)

**Role:** Proposed correction record against July ledger rows NS-1…NS-11, using an April Ring source (`492e0654f_RingLemma_Final.tex`) plus the Oct 2 geometric correction.

| Status class | Rows / findings |
| --- | --- |
| **PROVED (new geometry IDs)** | **RL-G1** \(L^2\)-threshold \(\|\nabla\xi\|_\infty(E_c)\le C L^{5/2}/c\) — in corrected note. **RL-G2** sharpness family order \(L^{5/2}\) on \(E_{1/2}\) (and fixed \(c<1\)). **RL-G3** peak-relative / amplitude-conditioned linear-in-\(L\) bounds. |
| **OPEN** | **RL-G4** dynamical amplitude control + PDE regularity consequence. |
| **NOT established by cited April source** | NS-1 (operator mismatch / dissipation sign), NS-2 (Φ-renorm absent), NS-3 (dissipation-rate absent), NS-4 (SND equivalence), NS-5 (three-way regime as theorem), **NS-6 three-shell \(H_N\)** (distinct claim; proof not in vorticity manuscript), NS-7 (finite dangerous duration), NS-8 (Gronwall needs valid \(H^1\) budget; uses augmentation), NS-9 (augmented global regularity via this proof), NS-11. |
| **OPEN + repair needed** | **NS-10** — even classical SND would not auto-remove augmentation; de-augmentation obstruction remains. |

**Primary finding (keep):** July NS-6 as recorded (three-shell static operator inequality with \(H_N\), spectral projections) is **not** the April/June vorticity-direction Ring Lemma. Do **not** swap IDs. Do **not** mark the three-shell inequality “disproved” because the vorticity lemma failed. Obtain a real \(H_N\) source or leave NS-6 three-shell as **SOURCE MISSING / OPEN**.

**Repo note:** This agent run still does **not** have in-repo bytes for `CURRENT_CLAIM_LEDGER_JULY23_FULL.md` (see claim-ledger audit). The reconciliation text’s SHA for that file is external evidence Jonathan supplied; treat row-by-row conclusions as applying to the pasted/audited July face + the attached Ring sources.

---

### 1.2 Corrected geometric note (Oct 2, 2026) — **current geometric SoT**

File: [`ring-lemma/RingLemma_Corrected_Geometric_Note_2026-10-02.tex`](./ring-lemma/RingLemma_Corrected_Geometric_Note_2026-10-02.tex)

| Claim | Status in the note |
| --- | --- |
| Band-limited \(\|\nabla\xi\|_{L^\infty(E_c)}\le (C/c)\,L^{5/2}\) | **PROVED** (Prop. 1) |
| Explicit DF family: lower bound \(\ge a L^{5/2}\) on \(E_{1/2}\); uniform \(CL\) on original \(E_c\) **false** | **PROVED** (Prop. 2) |
| Peak set \(F_a=\{|\omega|\ge a\|\omega\|_\infty\}\): \(\|\nabla\xi\|\le (C/a)L\); or under \(\|\omega\|_\infty\le A\|\omega\|_2\), order \(CAL/c\) on \(E_c\) | **PROVED** (Prop. 3) — spatial / conditional on amplitude |
| Dynamical preservation under NS; regularity theorem | **Explicitly not asserted** |
| Novelty / publication readiness | **Not audited** |

**Scope sentence (from the note’s Remark):** frequency localization alone gives only \(A\lesssim L^{3/2}\); single-shell support is not generally invariant under nonlinear convolution; no PDE conclusion without matching a geometric regularity criterion’s exact hypotheses.

---

### 1.3 June 19 Ring / SND manuscript — **superseded for geometry; archive for narrative**

File: [`ring-lemma/RingLemma_Simons_June19_2026.tex`](./ring-lemma/RingLemma_Simons_June19_2026.tex)

Dashboard claims (augmented unless marked):

| Dashboard row | June label | Honest status after Oct 2 + locks |
| --- | --- | --- |
| Augmented \(Q\)-operators defined | Done | **Definitions exist**; identities/signs need separate audit (recon text flags Q1/Q3 dissipation issues in April face) |
| Ring Lemma \(\|\nabla\xi\|\le C\cdot 2^{j^*}\) on \(E_c\) | **Proved** | **WITHDRAWN as stated** — Bernstein gap; correct power is \(5/2\) without amplitude control; sharpness kills uniform \(CL\) on fixed-\(c\) \(E_c\) |
| CF Question 2.2 answered (band-limited) | Yes | **OVERCLAIM** — wrong geometric bound; even corrected bound is not automatic CF close without criterion hypotheses + dynamics |
| Shell-Spread Poincaré + finite spread time | Proved | **NOT established** as classical/unaugmented theorem (recon: shell-spread proof sketch gaps; finite duration ≠ growth control) |
| Global Summation Lemma | Proved | **Conditional / incomplete** for classical; uses \(Q_3\) coercivity; de-augmentation obstruction admitted in-text |
| Conditional \(H^1\) under [SND] | Proved | **Conditional packaging only** if a valid budget exists; **not** from SND alone in these manuscripts |
| Main Theorem: global \(C^\infty\) augmented | Proved | **CONFLICT** with Oct locks — at best narrow fixed-\(\varepsilon\) Lions-augmented (NS-9 relabel); this manuscript’s two-regime proof leans on bad geometry + unproved pieces |
| Dynamical [SND] for classical NS | Open | **KEEP OPEN** (NS-10) |
| Unconditional classical regularity | Not claimed | **KEEP** (NS-11) |

**Zeta-clock / prime spacetime sections (§ temporal):** structural storytelling tying \(Q_6\) to \(\zeta\) zeros and RH. Treat as **not proved PDE**; do not import into NS claim ledger as proved. Conditional-on-RH remarks cut both ways and must not green classical NS.

---

## 2. Consistency with July NS-6 / NS-7 / NS-8 / NS-10 and Oct audit

| July ID | July label (outreach face) | Oct claim-ledger audit | Ring uploads reconcile | Recommended now |
| --- | --- | --- | --- | --- |
| **NS-6** | Ring PROVED standalone | **RELABEL** — scoped PROVED or OPEN/REVIEW; texture; not Clay | Vorticity Ring ≠ three-shell \(H_N\); June linear bound **false**; Oct note proves **RL-G1…G3** only | Split: **NS-6a** = RL-G1…G3 **PROVED (spatial, scoped)**; **NS-6b** three-shell \(H_N\) = **SOURCE MISSING / OPEN**; never “Ring ⇒ regularity” |
| **NS-7** | Finite dangerous-regime duration PROVED | (not KEEP as classical close) | Not established by April/June sources as stated | **OPEN / RELABEL** — do not equate with Global Summation or shell-spread by name |
| **NS-8** | Conditional \(H^1\) / Gronwall under SND | Conditional only if budget holds | Gronwall step OK **if** integrable coefficient supplied; manuscripts do not supply classical budget from SND alone | **CONDITIONAL** at best; not classical close |
| **NS-10** | Dynamic SND classical OPEN | **KEEP** + map to \(T_{j\leftarrow j}\) / PRODUCT-BLOCK / \(\alpha_+\) | Confirmed OPEN; de-augmentation still blocks “SND ⇒ classical” shortcut in these papers | **KEEP OPEN**; map as in claim-ledger audit §1 |
| **NS-11** | Classical regularity NOT CLAIMED | **KEEP** | Confirmed | **KEEP** |

**SND lock:** remains **conditional shell texture** (C12). Exact Augmented ↔ SND equivalence (**NS-4**) stays **WITHDRAWN**. Unconditional Statement B from SND/Ring stays **PARK** ([`SCIENTIFIC-REPORT.md`](./SCIENTIFIC-REPORT.md) §5).

**Unaugmented lock:** OPEN at \(T_{j\leftarrow j}\) and PRODUCT-BLOCK — Ring uploads do **not** touch those objects.

---

## 3. Overclaim flags (blunt)

1. **Ring ⇒ Clay / classical regularity** — refuse. Oct note refuses PDE consequence; June CF corollary overclaims even before the Bernstein fix.
2. **SND proved for classical Leray–Hopf** — refuse. June correctly marks Open; do not green via \(Q_6\) damping stories or numerics.
3. **June Ring Lemma “Proved” at order \(2^{j^*}\) on \(E_c\)** — **false**. Missing \(2^{3j/2}\) in \(L^2\to L^\infty\); sharpness family kills fixed-\(c\) linear bound.
4. **“Only gap is dynamical SND; then Main Theorem extends to classical”** — **false / dangerous**. De-augmentation obstruction is in June itself; Oct recon + NS-9 barrier (\(\|u^r/r\|_\infty\)) + PRODUCT-BLOCK / \(T_{j\leftarrow j}\) remain. SND is not the sole remaining door.
5. **NS-6 July three-shell \(H_N\) proved by Ring TeX** — **false**. Different claim; different ID.
6. **Q1/Q3 dissipation identities** as written in April/June faces — recon flags sign/growth issues; do not cite those identities as proved dissipation without a repaired PDE analysis.
7. **Zeta-clock ⇒ fluid regularity / RH bridge as NS proof** — refuse for the claim ledger.
8. **HH / \(N=32\) / IPR screenshots ⇒ SND theorem** — already refused in [`HH-SPECTRAL-CONCENTRATION-AUDIT.md`](./HH-SPECTRAL-CONCENTRATION-AUDIT.md); corrected note now on disk does not change that.

---

## 4. Proposed claim IDs (geometry only — do not replace NS-6 three-shell)

| ID | Statement | Status |
| --- | --- | --- |
| **RL-G1** | \(\|\nabla\xi\|_{L^\infty(E_c)}\le (C/c)L^{5/2}\) for band-limited \(\omega\not\equiv0\) | **PROVED** (Oct 2 note) |
| **RL-G2** | Sharpness: order \(L^{5/2}\) attained on \(E_{1/2}\) (fixed \(c<1\)) | **PROVED** |
| **RL-G3** | Linear-in-\(L\) on peak set \(F_a\), or on \(E_c\) under amplitude ratio \(A\) | **PROVED** (spatial; \(A\) not dynamical) |
| **RL-G4** | Dynamical amplitude control + PDE regularity consequence | **OPEN** |

These are vorticity-geometry IDs. They sit under the SND/Ring **texture** shelf. They do **not** close PRODUCT-BLOCK, \(T_{j\leftarrow j}\), or Clay.

---

## 5. Scoreboard

| Object | Verdict |
| --- | --- |
| Oct 2 corrected geometric note | **KEEP** as Ring **geometry** SoT (RL-G1…G3) |
| June 19 Ring Lemma geometry | **SUPERSEDED / WITHDRAWN** |
| June 19 augmented Main Theorem packaging | **DO NOT SHIP** as proved classical or Clay; conflict with NS-9 scoped relabel |
| July NS-6 standalone PROVED | **RELABEL** per §2 |
| July NS-10 / NS-11 | **KEEP** OPEN / NOT CLAIMED |
| SND classical | **OPEN** (texture only) |
| Clay Statement B | **NOT CLAIMED** |

---

## 6. One-line verdict

**Ring Lemma (honest): band-limited vorticity-direction gradient bounds of order \(L^{5/2}\) (sharp), or order \(L\) under amplitude control — spatial only. June 19 linear Ring + “SND is the last door to classical” are dead as outreach. Classical SND, \(T_{j\leftarrow j}\), and PRODUCT-BLOCK remain open; no Clay.**

---

## 7. Companions

- Source tree: [`ring-lemma/README.md`](./ring-lemma/README.md)  
- Claim ledger audit: [`CLAIM-LEDGER-AUDIT-2026-10.md`](./CLAIM-LEDGER-AUDIT-2026-10.md)  
- PR paste: [`PR-DRAFT-RING-LEMMA-RECONCILIATION.md`](./PR-DRAFT-RING-LEMMA-RECONCILIATION.md)
