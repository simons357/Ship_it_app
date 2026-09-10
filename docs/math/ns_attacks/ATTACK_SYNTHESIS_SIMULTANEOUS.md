# ATTACK SYNTHESIS — five lanes simultaneous (Lemma★ / Route N / SND spectral drift)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Rule:** Truth only. **Navier–Stokes is NOT solved. No Millennium claim.**

## Ingest

| Source | Path | Notes |
|--------|------|-------|
| Route N extraction ledger (225 lines) | `docs/math/NS-BRUTE-FORCE-EXTRACTION-LEDGER.md` | Shellwise \(B_{M,j}\) LEAD; PDE bridge HARD |
| Fuller swirl ledger (~1032 lines) | `docs/math/NS_Brute_Force_Extraction_Ledger-SWIRL-1032.md` | Batches 017–021 signed flux / drift-corrected \(K(t)\) |
| User Downloads ledger | `/Users/jonathansimons/Downloads/NS_Brute_Force_Extraction_Ledger-2.md` | **Not mounted** in this VM |
| Centered-drift recovery | `docs/ns-recovery/CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md` | Exact Stokes-moment proof package was lost; names recovered |

Prior ATTACK_* / PROOF_LemmaStar files were **absent** from this branch at start; this pass creates them from the centered-drift notation + user paste.

## Lemma★ (packaging)

\[
\mathfrak T_c\le\theta\nu(Z-\Lambda Y)+C_0\nu^{-1}\|u\|_2^2 X\Lambda,
\]
\(C_0\) geometric only. If true with uniform \(C_0\), then \(\Lambda\) cannot blow in finite time in this Foias–Temam packaging ⇒ global regularity on \(\mathbb{T}^3\) **in this packaging**. That implication is conditional on Lemma★ — **Lemma★ is not proved**.

## Lane board (runtime filled after probes)

| Lane | Script | Expected / prior | Runtime verdict |
|------|--------|------------------|-----------------|
| 1 Covariance | `attack1_covariance.py` | \(R_\star\) falls/plateaus as \(B\uparrow\) | *pending* |
| 2 Triad / K=0 / C* | `attack2_triad_k0_cstar.py` | K=0 DEAD; \(C_*\) amp-invariant | *pending* |
| 3 Bony HH→L | `attack3_bony_hh_l.py` | HH channel bottleneck | *pending* |
| 4 Stokes | `attack4_stokes.py` | \(\mathcal D_s\ge0\); remainder needed | *pending* |
| 5 Route2 kill | `attack5_route2_kill.py` | Try to blow \(R_\star\) | *pending* |

Runtime JSON: `/opt/cursor/artifacts/ns_five_lane_2026-09-10/SYNTHESIS_RUNTIME.json`.

## Exact inequality still to attack

Close **either**:
1. \(|\mathfrak T_c|\le C\|u\|_2^2 X\Lambda\) (Lemma★ / geometric \(C\)), **or**
2. \(|\mathfrak T_c|\le C_* X^{3/2}\Lambda\) (weaker survivor; Leray-integrable if \(\int X<\infty\)),

with a proof that survives HH→L. Standard 3D product / Agmon estimates do **not** close the gap. Numerics ≠ proof.

## Route N (arithmetic) — separate book

Shellwise principal-block floor of \(\widetilde Q\) remains a **LEAD** (`route_n_shell_floor_probe.py`), not a PDE theorem. Do not weld Route N matrices to Lemma★ without a map.
