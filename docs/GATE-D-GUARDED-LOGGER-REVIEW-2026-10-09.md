# Gate D guarded-logger review

9 October 2026.
**BLOCKED. The archive was not in this environment, so its hash was not checked and its tests were not run. The frozen \(c=200\), \(s\ge 4\) experiment was not launched. Gate D remains OPEN / BLOCKED. No turnover, regeneration, shared-budget, or regularity result is claimed.**

Requested archive: `gate_d_guarded_logger_fix_2026-10-09.zip`.
Reported SHA-256: `ca01fa9ab93950174ae3ca25a932c8778910e1fc71d075deda559df914f9e020`.

## Search log

The hash was not computed, because the bytes were not here.

- Uploads directory: the newest Gate D archive present is `gate_d_vorticity_evaluator_2026-10-09_1abc.zip`. No `*guarded*` file.
- Checkout and `origin/cursor/shared-budget-32-shape-c3ed`: no `guarded_logger` path and no `sign_unverified` symbol.
- Drive search for the title, and Gmail search for the filename: no matching item.

No unit test was executed. There is no candidate test log.

The locked stepper used as the comparison baseline is still `scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py`, SHA-256 `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`. It was not edited. The locked \(G\) unit test was not rerun.

## Verdicts

| Item | Verdict | What was checked |
| --- | --- | --- |
| 0. Archive integrity | **BLOCKED** | Reported SHA was not compared with file bytes. |
| 1. Gaussian RK4 stepper unchanged | **BLOCKED** | Candidate `grid`, `project`, `nonlinear`, and `step` were not present to diff. |
| 2. Spherical Galerkin mask, separate high-pass | **BLOCKED** | No candidate mask or diagnostic to inspect. |
| 3. `sign_unverified` emits no accepted \(T_{\mathrm{sc}}\) or crossing | **BLOCKED** | The symbol is not in this checkout. |
| 4. Exploratory signed evaluator bypassed in guarded mode | **BLOCKED** | No guarded-mode call graph was available. |
| 5. Rational fallback, cancellation, memory, uncertainty in \(T_{\mathrm{sc}}\) and \(Y\) | **BLOCKED** | No candidate implementation or tests. |
| 6. Physical cutoff \(L\) versus \(2L\), frozen \(N=128,160\) labels kept | **BLOCKED** | The candidate’s convention was not present. The standing record is still unresolved. |
| 7. Remaining \(\mathbb R^3\) Gaussian comparison requirements | **BLOCKED** | The candidate does not state them here. The standing requirements are listed below and are not a completed comparison. |

A missing file is not a pass and not a fail of the unseen code.

## What the next patch has to show

One patch, after the zip is actually present and its SHA-256 matches `ca01fa9ab93950174ae3ca25a932c8778910e1fc71d075deda559df914f9e020`.

1. **Stepper.** Diff `grid`, `project`, `nonlinear`, and `step` against the locked file. Those four functions are lines 18–54 of `scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py`. A pass is an empty diff of those bodies, and the locked file’s SHA unchanged. Do not edit that file to manufacture the match.

2. **Masks.** The evolution mask and the diagnostic high-pass are different objects. The spherical Galerkin mask already used by the uncertified candidates is componentwise \(|m|<n/3\) and \(m_x^2+m_y^2+m_z^2\le N^2\), with \(N<n/3\) (`make_galerkin_mask` in `scripts/ns_attacks/gate_d_vorticity_evaluator/mask_policy.py`). The locked `grid` builds only the componentwise \(2/3\) cube (lines 24–26) and does not apply a spherical \(N\). A guarded logger may pass a spherical mask in through `ks` only if `grid`’s body is still the locked body, and the same mask is the one `step` projects with. The high-pass \(r^2>K^2\) belongs in the diagnostic. It does not belong inside `step`.

3. **`sign_unverified`.** A test must show that this flag suppresses every accepted numeric \(T_{\mathrm{sc}}\) and every crossing claim. A log line that still carries a number under that flag fails the item.

4. **Guarded bypass.** A test must show that guarded mode does not call the exploratory evaluators (`vorticity_scalene`, `fast_scalene`, `phi_scalene`, or the ordered convolution). The exploratory path can remain in the tree for separate tests.

5. **Uncertainty.** Show the exact-rational fallback, the cancellation failure path, and the memory cap firing. Report an uncertainty for \(T_{\mathrm{sc}}\) and a separate uncertainty for \(Y\). The vorticity cancellation ratio is a report on \(T_{\mathrm{full}}-T_{\mathrm{rep}}\) only. It is not this certificate, and it says nothing about \(Y\).

6. **\(L\) and \(2L\).** Do not rename the frozen labels. \(N=128\) and \(N=160\) stay integer spectral labels: \(c\le N^2\) in \(\Phi_{abc}\), with \(a=|k|^2\) for \(k\in\mathbb Z^3\). Physical wavenumber \(2\pi|k|/L\) stays beside that cut and is not substituted into \(\Phi\). On a doubled box the integer \(T_{\mathrm{sc}}\) need not move while the physical edges halve, as already measured for \((K,N)=(1,5)\) at \(L=2\pi\) and \(2L=4\pi\) in [`GATE-D-CONNECTED-DRIVER-2026-10-09.md`](GATE-D-CONNECTED-DRIVER-2026-10-09.md). DA preregisters which physical band \(N=128\) and \(N=160\) mean before any experiment approval. This review does not choose \(L\) or \(2L\).

7. **\(\mathbb R^3\) comparison.** Still required, and still not done: the periodic sample of the curl Gaussian on \([-L/2,L/2)^3\) is not the \(\mathbb R^3\) datum (`scripts/ns_attacks/gate_d_gaussian_scaffold/README.md`); a matched physical cutoff; a stated periodization error; an initial-derivative comparison; and tolerances fixed before the run. Grid size \(n\) is not the frozen cutoff \(N\).

The frozen \(c=200\), \(s\ge 4\) trajectory stays unlaunched until items 1–7 have a later verdict other than BLOCKED, and until DA has preregistered the cutoff.

## STATUS

ARCHIVE: NOT PRESENT. REPORTED SHA NOT CHECKED.
TESTS: NOT RUN.
ITEMS 1–7: BLOCKED.
LOCKED STEPPER: UNCHANGED.
\(L\) VERSUS \(2L\): UNRESOLVED. FROZEN LABELS \(N=128\) AND \(N=160\) KEPT AS INTEGER CUTOFFS.
FROZEN \(c=200\), \(s\ge 4\): NOT LAUNCHED.
NO TURNOVER, REGENERATION, SHARED BUDGET, OR REGULARITY.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
