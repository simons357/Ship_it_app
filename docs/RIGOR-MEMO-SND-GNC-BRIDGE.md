# Rigor memo — SND ≡ GNC ≡ Bridge (June 5, 2026)

**Source read:** full PDF body of `SND_GNC_BRIDGE_UNIFIED.pdf`  
**Zenodo:** living DOI [10.5281/zenodo.20552399](https://doi.org/10.5281/zenodo.20552399) · version [10.5281/zenodo.20552400](https://doi.org/10.5281/zenodo.20552400)  
**Creator on Zenodo:** Simons, **Jonathan Robert** (not “Jonathan R.” — May batch uses the abbreviation; June Bridge records hide under the full middle name)  
**Companion:** T2 / Gronwall — [10.5281/zenodo.20552080](https://doi.org/10.5281/zenodo.20552080)  
**Author:** Jonathan Robert Simons · Prime Field Technologies  
**Memo purpose:** freeze proved vs open vs label drift so Route J / C / NS / RH stop getting mixed.

---

## Status lock (from the paper’s own labels)

| Claim | Status |
| --- | --- |
| **SND ⇔ GNC ⇔ Bridge** (same condition on Q_N) | **[Proved]** |
| **T2 Gronwall ⇔ SND** | **[Proved]** |
| κ\* = 6/π² = ζ(2)⁻¹ as shared threshold (asymptotic / structural) | **[Proved]** (asymptotic) |
| SND ⇒ NS global H¹ regularity on T³ | **[Proved, conditional on SND]** |
| Bridge ⇒ Strong Goldbach for n ≥ n₀(κ\*) | **[Proved, conditional]** |
| Bridge ⇒ RH | **[Proved, conditional]** — paper names this **Route C** (2 analytic gaps) |
| Unconditional λ_min(Q_N) > −1/2 for all N | **[Open]** — paper’s single open item |

**Submission framing that matches the PDF:** publish the **equivalence** as the result. Do not claim unconditional Millennium closure until the floor is proved.

---

## Route-name lock (fix the mish-mash)

| Label | Meaning | Domain |
| --- | --- | --- |
| **SND** | Spectral Non-Dispersal — max shell fraction ≤ ρ₀ | **NS** |
| **GNC** | Goldbach Non-Concentration — no dark state / Rayleigh ≥ κ\* | **Goldbach** |
| **Bridge** | λ_min(Q_N) > −1/2 for all N | Shared spectral floor |
| **Route C** (RH corollary) | Bridge ⇒ RH (conditional; 2 gaps) | **RH** |
| **Route J** | Squarefree / non-squarefree mixing **norm bound** (*Quantum Lens*) | Arithmetic hub — **not** the NS theorem, **not** a synonym for Bridge |
| **T2** | Inter-shell flux / Gronwall form of SND | **NS** |

**Stop saying “Route J closed” when you mean the June 5 equivalence.**  
What closed June 5: **SND ≡ GNC ≡ Bridge**.  
What did **not** close: unconditional Bridge floor.

**Internal collision inside the same PDF:** §6 also lists “Route C” as a *candidate strategy* (Tracy–Widom / GUE left-tail) for proving the open floor. That overloads the RH-corollary name. Prefer:

- **Route C (RH)** = Bridge ⇒ RH (summary table / Corollary 1)  
- **Floor strategy TW** = Tracy–Widom candidate in §6 (rename in next draft; don’t call it Route C)

May 19 Drive packet listing Bridge Q4 as **Open** is consistent: that was before the equivalence paper, and the **unconditional floor** is still open after June 5.

---

## Equivalence proof — line-by-line read (§4)

Operator: Q_N(i,j) = 1/gcd(i,j); H_N via Möbius decomposition (§2.1).

1. **Bridge ⇒ GNC**  
   λ_min > −1/2 ⇒ no unit vector sits at or below the dark / sub-κ\* regime; apply to v_k; GNC with κ\* = 6/π².  
   *Referee note:* short; load-bearing if λ_min and the GNC threshold are identified carefully with the same normalization of H_N vs Q_N.

2. **GNC ⇒ Bridge**  
   Contrapositive: if λ_min ≤ −1/2, some unit w has Rayleigh ≤ −1/2; paper argues this forces a prime-pair coupling failure below κ\*, violating GNC.  
   *Referee note:* this is the thinnest arrow. Needs the precise map from an arbitrary near-minimizer w to a Goldbach difference vector (or a density argument). Grab any later version that makes that map explicit.

3. **Bridge ⇔ SND**  
   Shell fractions a_j as a probability vector; GCD-weighted dispersion d_gcd(a, μ) as Rayleigh of H_N at v_j = √a_j; SND (ρ ≤ ρ₀ < κ\*) bound ↔ λ_min > −1/2 on that vector.  
   *Referee note:* clean structural idea; check that the shell-index GCD model is the intended physical/arithmetic identification (not only formal).

Paper’s own remark: equivalences are **structural** and do **not** require the unconditional floor. Correct as a claim type: *if any one holds, all three hold*.

---

## The floor gap (only equation that still seals Millennium-style claims)

| Bound | Value | Role |
| --- | --- | --- |
| Bridge need | λ_min(Q_N) **> −1/2** | Open for all N |
| Older analytic floor (GCD / edge constant C = π/2 − log 2) | ≈ **−0.877** | Too weak (below −1/2) |
| Capstone §2.2 | Asymptotic → 6/π² − 1/2 ≈ **+0.108**; numeric λ_min > −1/2 for N ≤ 5000 | Evidence, not uniform proof |

**Hunt in other versions:** one uniform proof that λ_min(Q_N) > −1/2 for all N ≥ 1.  
If found → Triple Lock becomes unconditional and Corollary 1 fires.  
If not → keep framing as **structural equivalence + conditional corollaries**.

---

## What is genuinely strong

The equivalence theorem is a real, publishable structural result: NS, Goldbach, and RH share **one finite-N spectral condition**. That is a better journal story than three separate near-misses. Ring Lemma / T2 / Möbius decomposition remain the supporting toolkit; they do not replace the open floor.

---

## Checklist when opening another `.tex` / PDF

- [ ] Does it prove λ_min(Q_N) > −1/2 **for all N**, or only asymptotics / numerics / rough inputs?  
- [ ] Does “Route J closed” mean mixing-norm (Quantum Lens) or did someone mislabel Bridge / Route C?  
- [ ] Is H_N vs Q_N normalization consistent with κ\* and −1/2?  
- [ ] Is GNC ⇒ Bridge arrow expanded beyond contrappositive sketch?  
- [ ] Author string: search **Jonathan Robert** for June Bridge records.

---

## One-line lock

**Equivalence closed. Floor open. NS = SND. RH = Route C (via Bridge). Route J ≠ Bridge.**
