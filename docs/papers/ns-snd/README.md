# Spectral non-concentration (Paper2) — separate book

This is **not** live Domain Architect.  
This is **not** the axisymmetric swirl paper.

DA may later route to this book. It must **not** glue:

- Paper2 \(H_N\) (shell-helical GCD interaction operator) to FRA coupling \(H\)
- Paper2 \(\mu\) / simplex \(a(t)\) to swirl \(\Phi = u_\theta/r\)
- SND / GNC / “Bridge” identities to the swirl rewrite \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\)
- Route J numerics to a Clay/Millennium claim

## Faces (not a compile pair)

| Face | File | Date on the face |
|---|---|---|
| June reading PDF | [`Paper2_NS_Regularity_SND_FIXED.pdf`](Paper2_NS_Regularity_SND_FIXED.pdf) | Corrected June 2026 |
| June FIXED TeX | *not received* | Filename requested; PDF only |
| Mac “SND 2” PDF | [`Paper2_NS_Regularity_SND.pdf`](Paper2_NS_Regularity_SND.pdf) | iOS export 21 July 2026; *implies* header |
| Zenodo “implies” | [`zenodo-20272545/`](zenodo-20272545/README.md) | Public deposit; live title **claim withdrawn** |
| August TeX | [`Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`](Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex) | 1 August 2026 |
| August 1 audit | [`NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md`](NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md) | Lemma 6.1 OPEN; §7 T2 not closed |

The PDFs are **not** compiles of the TeX. Diff: [`FACES.md`](FACES.md).

**Spectral Non-Concentration** — conditional framework / criterion for 3D Navier–Stokes on \(\mathbb{T}^3\).

Author: J.R. Simons. Original draft 18 May 2026.

Object: **periodic 3D Navier–Stokes on the torus**, not axisymmetric swirl.

Paper2 also writes \(\Phi_j\) for **nonlinear shell fluxes**. That letter is not swirl \(\Phi=u_\theta/r\) and not FRA output \(\Phi\).

## What the letters mean *in this book*

| Token | Meaning here | Not this |
|---|---|---|
| **SND** | Spectral Non-Dispersal / Non-Concentration: no persistent coherent concentration of energy in a dyadic shell or helicity sector. Quantitative form: \(\|H_N[u(t)]-\widehat H_N^\mu\|_{\mathrm{op}}<\delta_0\). | Not swirl identity. Not FRA. |
| **GNC** | Goldbach Non-Concentration. The paper marks this **analytically incomplete**. A false identity \(\gcd(2k-i,2k-j)=\gcd(i,j)\) was removed. There is **no Goldbach theorem**. | Not a closed number-theory input to NS. |
| **\(H_N\)** | Finite-dimensional operator \(H_N[a]=\sum a_j B_j\) on shell-energy weights \(a\in\Delta_{N-1}\). \(B_j\) come from the normalized GCD matrix \(\widehat H_N\). | Not FRA coupling \(H\). Not Hamiltonian. |
| **Route J** | Frozen equidistributed \(\mu_j=1/N\). Numerical \(\lambda_{\min}(\widehat H_N^\mu)\) near \(-0.30\) for tested \(N\le 800\). Marked **NUMERICAL / UNDER AUDIT**, not all \(N\). | Not \(\lambda_{\min}(Q_N)>-1/2\) for all \(N\). |

Retired glue from the old dump (do not revive): `SND ≡ GNC ≡ Bridge`.

## What is proved vs open

The paper’s own chain is:

```
SND (physics)
    --OPEN-->  ||a(t) - μ||_{ℓ¹} ≤ η_N
    --table says proved-->  C_N η_N < 0.20
    --table says proved-->  spectral gap
```

**Actually proved (thin, finite-dimensional):**

- Lipschitz continuity of \(a\mapsto H_N[a]\) in \(\ell^1\) (triangle inequality)
- Weyl: *if* a frozen gap and *quantitative* operator-norm SND both hold, then evolving \(\lambda_{\min}>-1/2\)

**Internal tension (do not paper over):** the status table marks the middle arrow “proved” via the Lipschitz lemma plus numerics. The same manuscript then says the quoted \(C_N\), \(\eta_N\), and safety margin are **not used as a theorem**, and T1 still asks for an analytic bound on \(C_N\). Route J itself is **NUMERICAL / UNDER AUDIT**, not all \(N\). Treat Weyl as a conditional perturbation fact. Do not treat \(C_N\eta_N<0.20\) as an all-\(N\) theorem.

**Open / withdrawn:**

- Dynamic SND for general unaugmented Leray–Hopf solutions
- The simplex lemma \(\|a(t)-\mu\|_{\ell^1}\le\eta_N\)
- Analytic \(C_N\) (T1)
- Dynamics (T2). The previous “T2 Closed Gronwall” label is **withdrawn**
- Classical 3D Navier–Stokes regularity is **not claimed**
- GNC: false identity \(\gcd(2k-i,2k-j)=\gcd(i,j)\) removed; no Goldbach theorem

Leray energy boundedness is **not** SND smallness. That leftover has the same *shape* as swirl’s unbound \(\int\|u^r/r\|_\infty\,dt\) (energy bound does not give the needed smallness). It is **not the same estimate**. Do not identify them.

## Relation to Book B (swirl)

| | Paper2 | Swirl (22 August) |
|---|---|---|
| Domain | \(\mathbb{T}^3\), full 3D, spectral shells | Axisymmetric with swirl, cylindrical |
| Keeper | Conditional: *if* quantitative SND, then a spectral gap | Algebraic identity \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) |
| Leftover | Simplex closeness \(\|a-\mu\|_{\ell^1}\) | Strain pairing / \(\int\|u^r/r\|_\infty\,dt\) |
| Do not do | Feed GCD \(H_N\) into swirl | Feed \(\Phi=u_\theta/r\) into Paper2 \(H_N\) |

## Relation to Domain Architect

Live DA is dump-era three-verb demo. It does not implement this paper. Inverse design of “prove regularity from SND” would currently emit a vacuous PD loop (DA-VC-01 FAIL). That is a DA bug, not a theorem of this paper.

## Compile

Overleaf is a PDF printer only. Compile the August TeX as its own project if you need a new PDF. Do not merge it with the June FIXED PDF, with April Clay/SERPENT mains, or with the 22 August swirl TeX.
