# Unaugmented 3-D NS — proof-chain honesty card

**Face:** unaugmented classical 3-D Navier–Stokes (no \(Q\)-stack, no added field).  
**Chain:** [`UNAUG-GENERIC-3D-PROOF-CHAIN.md`](./UNAUG-GENERIC-3D-PROOF-CHAIN.md) (11 September 2026).  
**Clay Statement B / NS closed:** **NOT claimed.**

These five paragraphs are binding for this face.

---

## Honesty card (locked)

**Terminology.** This chain’s **Lemma Star** is the \(\omega_\ast\) centering identity. Because \(\sum J_k=0\), the unknown barycenter \(\Lambda\) can be shifted off the right-hand side of \(T_c\). That identity is **finished**. It is bookkeeping. It is distinct from the later **ratio bound** \(\sup\mathcal{R}_\star<\infty\). Establishing the identity does not establish that bound or control nonlinear transfer.

**Dissipation threshold.** Because \(\rho_j\) is normalized by palinstrophy \(P_j\), the comparison \(\rho_j<\nu\) belongs to the enstrophy–palinstrophy estimate in (A). It is not an absorption criterion for the displayed shell-energy budget, whose viscous term is \(\nu Z_j\).

**Cross-scale terms.** This program proposes to handle cross-scale interactions using standard estimates. Their precise bounds and summability remain to be supplied within this chain; they are not established by this note. They are not the named obstruction. The named remainder is \(T_{j\leftarrow j}\).

**Remaining closure.** Conditions (A)–(C) describe candidate routes for completing this particular proof chain. The principal unresolved term is the same-scale transfer \(T_{j\leftarrow j}\). Step 6 describes a proposed closure mechanism: it requires (A), or a depletion estimate implying (A), without using \(\dot e_j\), \(\dot Z\) or \(\Lambda'\) to reintroduce the quantity being bounded. Lemma Star is used before (A), not instead of (A).

**Scope of computations.** The reported measurements concern small exact disks and the stated restricted classes. They establish no uniform conclusion as \(K_{\max}\to\infty\) or for generic data. Observed occupancy 1 alongside alignment approximately \(1/2\) does not establish the depletion required for closure.

---

## Reading rules (do not green)

| Claim | Status on this face |
| --- | --- |
| Lemma Star (\(\omega_\ast\) shift; \(\Lambda'=2(T_c-\nu D_s)/X\)) | Finished bookkeeping. Not a bound. |
| Identity \(\Rightarrow\) ratio bound / uniform \(\mathcal{R}_\star\) | **False** — refuse |
| Identity \(\Rightarrow\) regularity / Clay B | **False** — refuse |
| \(\rho_j<\nu\) as shell-energy absorption into \(\nu Z_j\) | **False** — that comparison lives in (A), not the shell-energy viscous term |
| \(\rho_j<\nu\) proved for generic data | **False** — refuse |
| Cross-scale bounds + summability | **Not supplied** in this chain |
| \(T_{j\leftarrow j}\) controlled | **OPEN** (principal remainder) |
| Numerics (occupancy \(\approx 1\), alignment \(\approx 1/2\)) \(\Rightarrow\) depletion / closure | **False** — refuse |
| Swirl axial reduction as Step 7 of generic 3-D | **False** — subclass only |

Do not bound \(T_{j\leftarrow j}\) by \(\dot e_j\), \(\dot Z\), or \(\Lambda'\). Do not treat restricted-disk samples as a uniform theorem.

---

## One-line status

**Lemma Star finished as bookkeeping. Remainder \(T_{j\leftarrow j}\). \(\rho_j<\nu\) is (A), not \(\nu Z_j\). Generic unaugmented 3-D regularity not claimed.**
