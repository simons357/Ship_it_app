# Gate D guarded-logger review

9 October 2026.
**Archive hash matches. Thirteen packaged tests passed here. Items 1, 2, and 4 pass. Items 3 and 5 fail. Items 6 and 7 stay blocked. The frozen \(c=200\), \(s\ge 4\) experiment was not launched. Gate D remains OPEN / BLOCKED. No turnover, regeneration, shared-budget, or regularity result is claimed.**

Archive: `gate_d_guarded_logger_fix_2026-10-09.zip`, filed at `scripts/ns_attacks/gate_d_guarded_logger/`.
SHA-256: `ca01fa9ab93950174ae3ca25a932c8778910e1fc71d075deda559df914f9e020`. This matches the reported hash. An earlier check in this environment found the file absent; this verdict uses the upload that arrived afterward.

## Tests rerun here

`python3 -m unittest -v test_guarded_loop test_loop_sidecar test_logger_bridge test_integrated_gate test_adaptive_certified` passed: 13 tests, 1.979 s. Log: `scripts/ns_attacks/gate_d_guarded_logger/TEST_LOG.txt`. The archive note names 10 tests in the first four modules. Those 10 passed, and the three tests in `test_adaptive_certified.py` passed as well.

The smoke inside those tests is \(n=24\), \(L=12\), \(c=200\), \(s\) to \(0.01\). It is not the frozen \(s\ge 4\) trajectory. The locked stepper file was not edited. Its SHA-256 remains `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`. The locked \(G\) unit test was not rerun.

## Verdicts

| Item | Verdict |
| --- | --- |
| 0. Archive integrity | **PASS** |
| 1. Gaussian RK4 stepper unchanged | **PASS** |
| 2. Spherical Galerkin mask, separate high-pass | **PASS** |
| 3. `sign_unverified` emits no accepted \(T_{\mathrm{sc}}\) or crossing | **FAIL** |
| 4. Exploratory signed evaluator bypassed in guarded mode | **PASS** |
| 5. Rational fallback, cancellation, memory, uncertainty in \(T_{\mathrm{sc}}\) and \(Y\) | **FAIL** |
| 6. \(L\) versus \(2L\), frozen \(N=128,160\) labels kept | **BLOCKED** |
| 7. Remaining \(\mathbb R^3\) Gaussian comparison | **BLOCKED** |

### 1. Stepper — PASS

`grid`, `project`, `nonlinear`, and `step` in both `gaussian_gate_d.py` and `gaussian_gate_d_with_sidecar.py` match the locked file, including `gaussian_curl`. `diagnostics` and `run` differ. The packaged `test_step_unchanged` compares the sidecar `step` only with the copy inside the zip. The comparison above is against `scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py`.

Zip `gaussian_gate_d.py` SHA-256 `3bc81c79b9dfb9a5f8eebc773dfc5764d84bae6352fba8581ee87156dc7cbeb9`. Sidecar SHA-256 `bb92ae5b5ac52a5ca893633b4355c01342dfecd850ed55badf01aec00b58f80e`.

### 2. Masks — PASS

With `--signed-N`, `run` replaces the \(2/3\) cube by `make_galerkin_mask` before the initial projection and before `step` (`gaussian_gate_d_with_sidecar.py`). That mask is the componentwise cube \(|m|<n/3\) intersected with \(m_x^2+m_y^2+m_z^2\le N^2\), and it rejects \(N\ge n/3\) (`mask_policy.py`). \(L\) is an unused argument. The integer ball is the Galerkin cutoff.

`check_highpass` only requires \(0\le K<N\). The evolution mask does not apply \(K\). `assess` skips modes with \(r^2\le K^2\) and rejects a nonzero coefficient outside \(N^2\) (`integrated_gate.py`). Because \(N<n/3\), that sphere sits inside the \(2/3\) cube, so the diagnostic \(N\)-cut and the evolution mask are the same integer ball.

The log sentence `periodization: sample Gaussian on periodic cube, then project and 2/3 filter` still names only the cube on a run whose `cutoff` field correctly names the spherical intersection. That sentence is a label defect. It does not change the mask passed to `step`. `high_fraction` remains a separate physical energy shell and is not the integer high-pass \(K\).

### 3. `sign_unverified` — FAIL

The guarded sidecar path itself does what this item asks of that path. `assess` returns `T_sc: None`, `D_sign: 'unknown'`, and `sign_certified_for_stored_coefficients: False` when the mode budget is exceeded (`integrated_gate.py`). `diagnostic_record` sets `crossing_certified: False` on every record (`logger_bridge.py`). The \(n=24\) smoke rows have `diagnostic_status=sign_unverified`, `T_sc` null, `D` null, and `crossing_certified` false.

Two holes remain in the same archive.

- `adaptive_certified.evaluate` still returns `fast_value` equal to the vorticity transfer on a record whose status is `sign_unverified`. On `make_pair(52)` with `max_exact_modes=2`, that value was about \(5.594\times 10^{-12}\) while `T_sc` was null.
- The safe-sidecar log header sets `T_sc_implemented` and `D_implemented` true whenever `--signed-K` is present, including the smoke whose data rows are unverified (`gaussian_gate_d_with_sidecar.py`).

A `sign_unverified` record in this package can still carry a numeric signed transfer, and the header can still say the signed diagnostic is implemented.

### 4. Guarded bypass — PASS

With `--safe-sidecar`, `run` calls `diagnostics` with both signed cutoffs forced to `None`, then calls `diagnostic_record`. `diagnostics` calls `signed_diagnostics` only when the signed cutoff is set. `assess` does not call `vorticity_scalene` or `evaluate_checked`. `test_no_exploratory_signed_call` patches `signed_diagnostics` to raise, and that test passed. The stepper’s `nonlinear` still runs, because the row still stores production and \(G\). That is the RK4 nonlinearity, not the exploratory signed evaluator.

`adaptive_certified.evaluate` is not on this path. It still calls `vorticity_scalene` before deciding the status. Item 4 is the guarded mode only.

### 5. Exact fallback, cancellation, memory, uncertainty — FAIL

On the packaged witness \(m=2\), \(A=1\), \(K=1\), \(N=6\), `phi_scalene`, `ordered_transfer`, and `transfer_exact` each returned \(+32\). That is the packaged-witness agreement. It is not a Lemma 19 certification. The original-coefficient sign gap stays unresolved.

`assess` builds the viscosity by `Fraction(float(nu))` with default `nu=1/200` (`integrated_gate.py`). In Python that float is `0.005`, and

\[
\mathrm{Fraction}(0.005)=\frac{5764607523034235}{1152921504606846976}\ne\frac{1}{200}.
\]

The absolute gap is \(3/28823037615171174400\), about \(1.04\times 10^{-19}\). On `make_pair(54)`, \(T=0\) and \(Y=6720\), so the viscosity \(1/200\) gives \(D=-42/5\). The reported `D_normalized_exact` is \(-605283789918594675/72057594037927936\). Those fractions differ by about \(1.75\times 10^{-16}\). Both signs are negative, and the \(j=52\) signs also agreed. The stored \(D\) is still not the rational value for viscosity \(1/200\), and `sign_certified_for_stored_coefficients` is true on that record.

`logger_bridge` stores \(T_{\mathrm{sc}}\) as the binary64 value of \((2\pi)^3\) times the normalized rational. It does not store \(Y\). `certified_float_enclosure` in `exact_discrete_y.py` is not called by `assess` or the logger. The same log row still carries the stepper’s physical float \(Y\), which is a different convention and has no enclosure. There is no uncertainty on the logged \(T_{\mathrm{sc}}\) and no uncertainty on the logged \(Y\).

`cancellation_report` labels itself a heuristic and sets `rigorous_error_bound` false (`fail_closed.py`). Equal inputs return `fail_cancellation`. The guarded path does not call it. A passing heuristic is not a bound on \(T_{\mathrm{full}}-T_{\mathrm{rep}}\) and says nothing about \(Y\).

Memory enforcement does fire. `preflight(200, 10)` raises `MemoryError` because the estimate \(576 n^3\) exceeds the default 2 GiB ceiling. A cap of 1 byte also raises. The estimate is not a peak-RSS certificate. The \(N=128\) grid needs \(n>384\), and this default ceiling rejects that grid before any transfer. That is a safeguard, not a scale-up.

### 6. \(L\) and \(2L\) — BLOCKED

The integer labels stay integer labels. \(N=128\) and \(N=160\) are not renamed. \(\Phi_{abc}\) still cuts on \(a=|k|^2\) for \(k\in\mathbb Z^3\). Physical wavenumber \(2\pi|k|/L\) is written beside that cut. The smoke header records both `physical_kmax` \(=2\pi N/L\) and `physical_kmax_doubled_box_same_N` \(=\pi N/L\). For the smoke, \(N=6\), \(L=12\), those values are \(\pi\) and \(\pi/2\).

`assess` certifies a \(D\) sign only when \(L\) is exactly \(2\pi\). At \(L=4\pi\), `make_pair(52)` returns `physical_box_sign_unverified`, `T_sc` absent, `D_sign` unknown, and `crossing_certified` false. The smoke uses \(L=12\), so its rows stay unverified. This refusal is not a choice of the frozen experiment’s box. DA still has to preregister which physical band the integer labels \(N=128\) and \(N=160\) mean. This review does not choose \(L\) or \(2L\).

### 7. \(\mathbb R^3\) comparison — BLOCKED

The archive does not contain that comparison. These requirements have to be fixed before one is attempted.

- The periodic sample of the curl Gaussian on \([-L/2,L/2)^3\), then projected, is not the \(\mathbb R^3\) datum (`scripts/ns_attacks/gate_d_gaussian_scaffold/README.md`).
- Name the physical box and the physical spectral cutoff. Keep \(N=128\) and \(N=160\) as integer labels. Grid size \(n\) must satisfy \(N<n/3\), and \(n\) is not that frozen cutoff.
- State a periodization error between the \(\mathbb R^3\) field and the periodic sample, in a named norm, as the box grows.
- Compare the \(\mathbb R^3\) initial derivative with the periodic Galerkin derivative at the initial time. Fix the tolerance before the run.
- State which \(Y\) enters \(D\): the integer-lattice moment, or the stepper’s physical moment. They differ by the factor \((2\pi)^4/L\) on the bridge convention already recorded for \(L\) and \(2L\).
- Fix tolerances for energy, divergence, and the signed diagnostic before the run.

## Next required patch

One patch, with the four RK4 bodies still matching the locked file.

- On every `sign_unverified` record, including `adaptive_certified.evaluate`, omit `fast_value` and every other numeric transfer. In safe-sidecar mode set `T_sc_implemented` and `D_implemented` false, and make the periodization sentence name the spherical mask that `step` actually receives.
- Build the viscosity as `Fraction(1, c)` from the integer \(c\). Certify a \(D\) sign only from that rational. Put the normalized exact \(Y\), and a float enclosure of both \(T_{\mathrm{sc}}\) and \(Y\), on the log record. Keep `rigorous_error_bound` false until a bound exists.
- Leave \(L\) versus \(2L\) unchosen. Leave \(N=128\) and \(N=160\) as integer labels.

The frozen \(c=200\), \(s\ge 4\) trajectory stays unlaunched.

## STATUS

ARCHIVE SHA-256: MATCHES.
TESTS HERE: 13 PASSED, 1.979 s. SMOKE \(s=0.01\) ONLY.
ITEM 1 STEPPER BODIES: PASS. LOCKED FILE UNCHANGED.
ITEM 2 MASKS: PASS.
ITEM 3 `sign_unverified`: FAIL. NUMERIC `fast_value` STILL RETURNED. HEADER STILL CLAIMS \(T_{\mathrm{sc}}\) IMPLEMENTED.
ITEM 4 GUARDED BYPASS: PASS.
ITEM 5 EXACT \(D\) AND UNCERTAINTY: FAIL. VISCOSITY RATIONAL IS NOT \(1/200\). LOGGED \(Y\) HAS NO ENCLOSURE.
ITEM 6 \(L\) VERSUS \(2L\): BLOCKED. LABELS \(N=128\) AND \(N=160\) KEPT.
ITEM 7 \(\mathbb R^3\): BLOCKED. REQUIREMENTS LISTED. COMPARISON NOT RUN.
LEMMA 19: NOT CERTIFIED. PACKAGED WITNESS AGREEMENT \(+32\) ONLY.
FROZEN \(c=200\), \(s\ge 4\): NOT LAUNCHED.
NO TURNOVER, REGENERATION, SHARED BUDGET, OR REGULARITY.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
