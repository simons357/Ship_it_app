# Honest OPEN board

**Status:** a Domain Architect lab protocol, September 2026  
**Not a Navier–Stokes proof.** Clay is **NOT CLAIMED**. DA-VC-01 stays **FAIL**.  
**Shell-estimate filter:** [`AXISYMMETRIC-SHELL-AUDIT.md`](AXISYMMETRIC-SHELL-AUDIT.md).

The OPEN chorus was mixing four different kinds of unfinished work:

| Bucket | Meaning | How DA closes it |
|---|---|---|
| **WITHDRAWN** | The claim is finished as a claim | Stop saying OPEN |
| **REJECTED** | Dump / glue / not live DA | Take it off the board |
| **MISSING** | No bytes here | Hunt files; do not invent theorems |
| **CONDITIONAL** | Energy does not give smallness | Leftover-split: keep the coercive part; \(\sigma\) is a named hypothesis |
| **DA engineering** | Software gates | A13 fail-closed inverse design; A5 declared \(T\) still owed |
| **STILL OPEN** | Genuine remaining math | Short list only |

Canonical spec: [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md).  
Siblings: [`LEFTOVER-REPAIR.md`](LEFTOVER-REPAIR.md), [`LOCALIZED-REPAIR.md`](LOCALIZED-REPAIR.md).  
Challenge: [`DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md`](DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md).  
Shell estimate (this remainder is \(T_{j\leftarrow j}\), not Clay): [`docs/papers/swirl/AXISYMMETRIC-SHELL-ESTIMATE.md`](../papers/swirl/AXISYMMETRIC-SHELL-ESTIMATE.md).

## What actually remains open (math)

1. **GAP1 Step F / Fujii remainder** — one calculation, not a slogan. Operators A and B are already **not identical**. \(\lambda_{\min}/\log N\to-1/(2\pi)\) is **not a theorem**.
2. **Route J all-\(N\)** — \(N\le 800\) numerical. Not a regularity proof. Stays separate from SND / GNC / Bridge Triple Lock.
3. **NS-open / Clay Statement B** — not a DA validation gate. Stamping it from DA fails DA-VC-01. Not a close of the axisymmetric shell estimate.
4. **Axisymmetric-with-swirl shell remainder \(T_{j\leftarrow j}\)** — Class: unaugmented axisymmetric NS with swirl. Quantity: labeled \(Z_j\) (energy \(\neq\) enstrophy). Remainder: \(T_{j\leftarrow j}\). Assumed: [no DNS; no closed stepper]. Spectral-shift identity is bookkeeping, not Lemma★. \(\rho_j<\nu\) is enstrophy–palinstrophy (A), not energy-budget absorption. Occupancy 1 with \(\alpha\approx 1/2\) is not depletion. (A)–(C) and Step 6 are candidate routes. Leftover still **OPEN**. Clay **NOT CLAIMED**. DA-VC-01 stays **FAIL**.

The three NS leftovers (swirl strain, unconditional Ring SND, Paper2 simplex 7–8) are **conditional closes**: if \(\sigma\) then the rest of that book runs. \(\sigma\) is not proved. That is the only honest theorem-shaped close DA can give them. Do **not** set \(\sigma_{\mathrm{strain}}=T_{j\leftarrow j}\).

## What DA just closed in software (A13)

Synthesize of unaugmented NS / Clay slogans / `maximize profit` is
`inverse_design[refused]`. No PD loop. Recognized setpoints (`x=1`,
`x → 1.0`) still get a controller.

This does **not** make DA-VC-01 a pass. T1 still needs a declared
\(T\colon\Gamma\mapsto r^2\Phi\) (A5). D1/D2 stay unclassified.

## Run it

```
python -m domain_architect cycle open-board
python -m domain_architect cycle axisymmetric-shell
python -m domain_architect synthesize --target "global smoothness of unaugmented axisymmetric Navier-Stokes with swirl" --constraint "classical NS"
python -m domain_architect cycle leftover-repair
python -m domain_architect cycle localized-repair
```

Desktop Cycle tab: **Honest OPEN board** and **Axisymmetric shell (T_{j←j} OPEN)**.

## What this does not do

- It does not prove classical unaugmented Navier–Stokes.
- It does not prove RH or Goldbach.
- It does not invent the GAP1 10–20 line closure.
- It does not import E8 / Chat Vault / 2.2 Hz paint / QStack into live DA.
- It does not award `TRANSFORMABLE` without a real \(T\).
