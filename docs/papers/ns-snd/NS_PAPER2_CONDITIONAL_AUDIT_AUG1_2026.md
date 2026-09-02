# NS Paper 2 — Conditional Status Audit

**Title:** Spectral Non-Concentration Implies Global Regularity for 3D Navier–Stokes on T^3  
**Author:** Jonathan Robert Simons, CRNA, MBS  
**Date of manuscript:** May 18, 2026  
**Audit date:** August 1, 2026  

## Verdict

This is the NS Paper 2 manuscript deposited at Zenodo version DOI 10.5281/zenodo.20272545, concept DOI 10.5281/zenodo.20272544. It is not an unconditional proof of classical 3D Navier–Stokes regularity. It is a conditional spectral reduction with a precisely stated remaining dynamical lemma.

## What the paper actually proves

1. **Theorem 4.1:** If the frozen gap condition and quantitative SND perturbation bound both hold, Weyl's inequality gives the dynamic spectral gap. This is a valid conditional operator-theoretic implication, assuming the stated operator objects and bounds.
2. **Lemma 3.1:** Finite-dimensional Lipschitz/operator-continuity estimate for H_N[a] = sum_j a_j B_j. This is elementary and valid at the stated finite-N level.
3. **Frozen gap:** The paper states a finite-N/Route-J frozen gap result. Current governance must keep the stronger analytic/all-N Route-J status as NUMERICAL / analytically incomplete unless a certified proof is separately supplied.
4. **Lemma 6.1:** The required uniform-in-time shell equidistribution/SND simplex-stability statement remains OPEN.

## Internal contradiction

Section 7 labels T2 "Closed (conditional on SND)" and claims a Gronwall closure. Section 8 then correctly lists T1 and T2 as OPEN. The Section 7 closure cannot be accepted as written because it asserts the key transfer estimate and positive damping constant without a complete derivation and uses local existence to handle the transient. Local existence only gives the trivial simplex bound ||a(t)-mu||_1 <= 2; it does not give the target 0.039 bound.

## Missing classical bridge

Even if Lemma 6.1 were proved, the paper must explicitly supply the continuation criterion from the spectral gap/non-concentration statement to global regularity of the Leray–Hopf solution. The current manuscript establishes spectral stability under SND, not by itself unconditional smoothness for every Leray–Hopf solution.

## Route J

Route J is present in the manuscript: it is named in Theorem 2.1 as the source of the frozen spectral gap. It was not missing from the submitted Paper 2. However, its status must not be upgraded merely because the manuscript calls it unconditional. The current canonical governance record classifies Route J as NUMERICAL / analytically incomplete, and separate from the Triple Lock.

## Reference/DOI problems in pasted text

The pasted references are stale or misassigned. Reference [1] lists Zenodo 10.5281/zenodo.19842060 as a GCD spectral paper, but that DOI is the published Ring Lemma version. Reference [2] lists 10.5281/zenodo.19842061, which is not the canonical NS Ring Lemma record and is unrelated in the corrected inventory. The canonical NS Paper 2 DOI is 10.5281/zenodo.20272545.

## Honest current label

**Conditional theorem / open dynamical bridge.** The paper provides a clean reduction: quantitative SND plus a frozen spectral gap implies a dynamic spectral gap. It does not prove the missing uniform SND simplex-stability lemma and does not close unconditional classical 3D Navier–Stokes regularity.

## Recommended correction

Retitle or subtitle the public manuscript to make the logical status visible, for example: "Spectral Non-Concentration and a Conditional Global-Regularity Framework for 3D Navier–Stokes on T^3." Keep the existing title only if the abstract and first page prominently say "conditional framework" and explicitly state that Lemma 6.1 is open. Remove the claim that Section 7 closes T2 unless the transfer estimate, damping estimate, and transient argument are independently proved.
