# Swirl WITH vs WITHOUT Φ-cancel

**Book:** axisymmetric Navier–Stokes with swirl  
**Engine:** Domain Architect inquiry (FRA classifier, not a proof engine)  
**ChatVault:** **no.** Inquiry refuses drain.  
**Clay NS / RH:** **not claimed.** Unconditional NS smoothness is still a hypothesized realization, not a theorem.

Two faces sit on the DA desktop so both inquiry paths can run side by side.

## WITH cancel (live Phi)

**PDF:** `domain_architect/static/faces/01_phi_renormalization.pdf`  
**DOI:** [10.5281/zenodo.22050974](https://doi.org/10.5281/zenodo.22050974) (sibling [22050975](https://doi.org/10.5281/zenodo.22050975))  
**SHA256 (live file, do not regenerate):** `735ab6586a1edb0fee29e6c797a0a12c82a0d2a4e24e667b8d65c6899a2e3c55`  
**Operator:** \(r^{-4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\), \(\Phi=\Gamma/r^2=u_\theta/r\).

Q1-augmented / Φ-system. The identity is algebra. Classical regularity without augmentation remains **Open** on that paper’s own dashboard. **Q1 ≠ classical.**

June conditional Phi [10.5281/zenodo.21071991](https://doi.org/10.5281/zenodo.21071991) is archive (`/faces/superseded/june_phi_conditional.pdf`).

## WITHOUT cancel

**PDF:** `domain_architect/static/faces/swirl_without_cancel.pdf` (DA face; no matching pre-cancel Zenodo PDF)  
**Operator:** \(D_t\Omega=(1/r^4)\partial_z(\Gamma^2)+\nu L_{\mathrm{cyl}}\Omega\), \(\Gamma=r u_\theta\).

The \(1/r^4\) centrifugal axis term is still in the equations. Point at the WITH-cancel PDF as later work. This face does not apply \(\Phi=\Gamma/r^2\).

## Named citations (from live 22050974 §1.2 / Thm 3.2)

Wired as **citations, not proof stamps**. None of these close unaugmented 3D NS.

| Person | Live ref | What it is | What it is not |
|---|---|---|---|
| **R. Danchin (2007)** | §1.2 [6] | Names the \(1/r^4\) term as the obstruction to direct energy methods on the WITHOUT operator | Not Φ-cancel. Does not remove the prefactor. Does not prove swirl regularity |
| Ladyzhenskaya; Ukhovskii–Yudovich (1968) | §1.2 [1][2] | Without swirl (\(u_\theta\equiv 0\)), regularity is classical | Does not apply to with-swirl large data |
| Chae–Lee (2002) | §1.2 [3] | Small-swirl regularity | Not large swirl |
| Chen–Fang–Zhang (2017) | §1.2 [4] | Regularity *if* swirl stays in \(L^\infty_t L^3_x\) | A criterion, not a bound on the WITHOUT operator |
| Hou–Li (2008) | §1.2 [5] | Dynamic stability / blow-up with boundary | Not large-data global regularity |
| Ladyzhenskaya–Prodi–Serrin via Bahouri–Chemin–Danchin (2011) | Thm 3.2 [9] | Bootstraps the **Q1-augmented** system to \(C^\infty\) | Not unaugmented classical NS |
| Constantin–Fefferman (1993) | Def 4.1 [8] | Vorticity-direction criterion in the stability energy | A criterion, not a Clay stamp |

Tao is not named on 22050974. Do not steal credit. Do not pretend any of these close unaugmented 3D NS.

## Gaps (will not fill)

### GAP-SWIRL-AXIS — WITHOUT ↛ WITH

WITHOUT still has \(D_t\Omega=(1/r^4)\partial_z(\Gamma^2)+\nu L_{\mathrm{cyl}}\Omega\). WITH applies \(\Phi=\Gamma/r^2=u_\theta/r\) so \(r^{-4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\). **Danchin names the hole; he does not cancel it.**

**Next-attempt lemma (not RH/Goldbach):** Chen–Fang–Zhang \(L^\infty_t L^3_x\) swirl criterion (live [4]). Still open because the bound is not in hand on the WITHOUT operator.

### GAP-Q1-CLASSICAL — Φ-cancel ↛ unaugmented NS

Even when the Φ identity holds, live 22050974 is Q1-augmented. LPS bootstrap is for that PDE. **Q1 ≠ classical.** Constantin–Fefferman is a criterion, not Clay.

**Next-attempt lemma (not RH/Goldbach):** ε-independence of \(C(\varepsilon)=2\sup_t\|u^r_\varepsilon/r\|_\infty\) (June 21071991 OP2 / Serrin-type). That is the remaining axis advection obstruction after \(1/r^4\) is relocated into Φ.

## Run both paths

```bash
python3 -m domain_architect --swirl-with-cancel
python3 -m domain_architect --swirl-without-cancel
python3 -m domain_architect --swirl-compare
python3 -m domain_architect --site
# Inquiry → Inquire WITH / WITHOUT / Compare
```

WITH does not solve WITHOUT. Neither face is unconditional classical 3D NS. Domain Architect does not stamp either gap filled.
