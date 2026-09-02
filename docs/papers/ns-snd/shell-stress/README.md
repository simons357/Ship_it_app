# Shell stress workbook — numerical only

[`Simons_NS_Shell_Stress_Test.xlsx`](Simons_NS_Shell_Stress_Test.xlsx)

SHA-256 `ddba329536ee…`. 287 973 bytes.

This is a **spreadsheet of pseudo-spectral runs**, not a theorem.

Workbook title: *SIMONS NS SHELL STRESS TEST*. Subtitle: reproducible numerical diagnostics for a V9/V10 spectral-transfer program.

## What it is

- Model: 3D **periodic** incompressible Navier–Stokes on a \(24^3\) grid, \(\nu=0.035\), RK4, \(dt=0.0025\), horizon \(0.25\).
- 24 runs (six dyadic-band scenarios × two intensities × two seeds). 624 sampled states.
- Sheets: README, Dashboard, Aggregates, Run Summary, Time Series, Scenario Inputs, Validation.
- Own README cell: *general 3D periodic Navier–Stokes stress test, not an axisymmetric-swirl computation and not a proof of regularity.*

\(C_+\) is positive nonlinear shell transfer over viscous enstrophy removal. \(C_+>1\) is an instantaneous ratio, not blowup. \(C_{\mathrm{net}}>1\) is instantaneous total enstrophy growth, not a continuation criterion.

## What it is not

- **Not** a theorem.
- **Not** all-\(N\) Route J (\(\lambda_{\min}(\widehat H_N^\mu)>-1/2\) for every \(N\)). Grid is \(N=24\) spatial, not the Paper2 frozen-gap \(N\le 800\) matrix audit.
- Not Clay / unconditional NS.
- **Not** the June FIXED PDF and **not** `Paper2_NS_Regularity_SND_FIXED.tex` (that TeX was not received; do not invent it).
- **Not** Book B swirl. Do not glue these shell ratios to \(\Phi=u_\theta/r\).
- **Not** live Domain Architect.

File under Paper2’s book because the object is periodic 3D dyadic shells. Keep it next to the papers, not inside `domain_architect/`.
