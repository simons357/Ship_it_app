# Unaugmented 3D NS — proof-chain honesty card

**Face:** unaugmented classical 3D Navier–Stokes (no \(Q\)-stack, no added field).  
**Status:** **OPEN** at same-scale transfer \(T_{j\leftarrow j}\); Lemma★ packaging still **OPEN** at PRODUCT-BLOCK (\(\sup\mathcal{R}_\star\)).  
**Clay Statement B / NS closed:** **NOT claimed.**  
**Authoritative lock (Jonathan R. Simons):** the five paragraphs below are binding for this face.  
**Companions:** [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md) · [`SCIENTIFIC-REPORT.md`](./SCIENTIFIC-REPORT.md) · [`CREDIT-BODY-OF-WORK.md`](./CREDIT-BODY-OF-WORK.md)

Mac source `UNAUG_3D_NS_PROOF_CHAIN.md` was not mirrored in this environment; terminology and honesty below are taken from the locked paste.

---

## Honesty card (locked)

**Terminology.** We call the exact bookkeeping relation the **spectral-shift identity**. It is distinct from the **Lemma★ ratio bound** discussed in earlier attack notes. Establishing the identity does not establish that bound or control nonlinear transfer.

**Dissipation threshold.** Because \(\rho_j\) is normalized by palinstrophy \(P_j\), the comparison \(\rho_j<\nu\) belongs to the enstrophy–palinstrophy estimate in (A). It is not an absorption criterion for the displayed shell-energy budget, whose viscous term is \(\nu Z_j\).

**Cross-scale terms.** This program proposes to handle cross-scale interactions using standard estimates. Their precise bounds and summability remain to be supplied within this chain; they are not established by this note.

**Remaining closure.** Conditions (A)–(C) describe candidate routes for completing this particular proof chain. The principal unresolved term is the same-scale transfer \(T_{j\leftarrow j}\). Step 6 describes a proposed closure mechanism: it requires (A), or a depletion estimate implying (A), without using \(\dot e_j\), \(\dot Z\) or \(\Lambda'\) to reintroduce the quantity being bounded.

**Scope of computations.** The reported measurements concern small exact disks and the stated restricted classes. They establish no uniform conclusion as \(K_{\max}\to\infty\) or for generic data. Observed occupancy 1 alongside alignment approximately \(1/2\) does not establish the depletion required for closure.

---

## Reading rules (do not green)

| Claim | Status on this face |
| --- | --- |
| Spectral-shift identity (\(\Lambda'=2(T_c-\nu D_s)/X\) bookkeeping, or the shell Door-1 partition) | Algebra / bookkeeping only |
| Identity \(\Rightarrow\) Lemma★ ratio bound / uniform \(\mathcal{R}_\star\) | **False** — refuse |
| Identity \(\Rightarrow\) regularity / Clay B | **False** — refuse |
| \(\rho_j<\nu\) as shell-energy absorption into \(\nu Z_j\) | **False** — that comparison lives in (A), not the shell-energy viscous term |
| Cross-scale bounds + summability | **Not supplied** in this chain |
| \(T_{j\leftarrow j}\) controlled | **OPEN** (principal remainder) |
| Numerics (occupancy \(\approx 1\), alignment \(\approx 1/2\)) \(\Rightarrow\) depletion / closure | **False** — refuse |
| PRODUCT-BLOCK \(\sup_v\mathcal{R}_\star(v)<\infty\) | **OPEN** (Lemma★ hinge; separate packaging) |

Do not bound \(T_{j\leftarrow j}\) by \(\dot e_j\), \(\dot Z\), or \(\Lambda'\). Do not treat restricted-disk samples as a uniform theorem.

---

## One-line status

**Unaugmented 3D face: OPEN at \(T_{j\leftarrow j}\). Lemma★ packaging: OPEN at PRODUCT-BLOCK. Spectral-shift identity ≠ Lemma★ bound. Numerics ≠ depletion. NS / Clay B not claimed.**
