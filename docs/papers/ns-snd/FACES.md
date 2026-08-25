# Paper2 has two faces. They are not a compile pair.

Do **not** treat the June PDF as a compile of the August TeX, or the reverse.

| | June reading PDF | August repaired TeX |
|---|---|---|
| File | [`Paper2_NS_Regularity_SND_FIXED.pdf`](Paper2_NS_Regularity_SND_FIXED.pdf) | [`Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`](Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex) |
| Title | *Spectral Non-Concentration as a Conditional Regularity Criterion* | *Spectral Non-Concentration and a Conditional Global-Regularity Framework* |
| Date on the face | Corrected June 2026 (original draft 18 May) | 1 August 2026 (header still 18 May) |
| Length | 7 pages | 572 lines of TeX |
| GNC / false gcd | **Absent** | Present: GNC analytically incomplete; \(\gcd(2k-i,2k-j)=\gcd(i,j)\) removed |
| Frozen gap | Hypothesis 2.1, cited from Paper 1. Numerics \(N\le 800\) mentioned only as what the *original* draft mixed with an asymptotic | Route J **NUMERICAL / UNDER AUDIT**, \(N\le 800\), no all-\(N\) theorem |
| Product \(C_N\eta_N<\delta_0\) | Status table: **Numerical/conditional.** Sample \(C_N\eta_N\approx 0.067<0.20\) | Status table: middle arrow **proved** (lemma + numerics), then a remark that those numbers are **not a theorem** |
| T2 / Gronwall | §7 is a **proof plan**: target \(d'\le -\kappa d+\varepsilon_N\). Explicitly not a completed proof | Previous “T2 Closed Gronwall” **withdrawn**. Lists five missing requirements. No Gronwall closure claimed |
| Simplex lemma | Lemma 6.1 **open** | SND Simplex Stability **open** |
| Classical 3D NS | **Not claimed** | **Not claimed** |
| Paper 1 citation | Zenodo `10.5281/zenodo.19842060` | Preprint, “historical reference only” |

## What they agree on

Conditional Weyl: *if* frozen gap and quantitative operator-norm closeness, then \(\lambda_{\min}>-1/2\). Lipschitz of \(H_N[a]\) is triangle inequality. Leray boundedness is not simplex smallness. The leftover is \(\|a(t)-\mu\|_{\ell^1}\). That leftover is **not** swirl’s \(\int\|u^r/r\|_\infty\,dt\).

## Which face to use

- **Later caution on Route J and GNC:** August TeX.
- **Cleaner honesty on the product \(C_N\eta_N\):** June PDF (numerical/conditional, not “proved”).
- **Do not merge them into one claim.** If a single source is required, say which face you are compiling. Do not cite the PDF as “the August paper” or the TeX as “the June FIXED PDF.”

Neither face is Domain Architect. Neither face is the 22 August swirl paper. Neither face is Clay.
