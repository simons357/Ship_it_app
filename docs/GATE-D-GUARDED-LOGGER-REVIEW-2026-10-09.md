# Gate D guarded-logger review

9 October 2026.
**Local review, not DA sign-off. Items 1–4 pass. Items 5–7 stay blocked. The frozen \(c=200\), \(s\ge 4\) experiment was not launched. Gate D remains OPEN / BLOCKED. No turnover, regeneration, shared-budget, or regularity result is claimed.**

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
| 3. `sign_unverified` cannot establish a crossing | **PASS** |
| 4. Exploratory signed evaluator bypassed in guarded mode | **PASS** |
| 5. Rational fallback, cancellation, memory, and numerical uncertainty | **BLOCKED** |
| 6. Fixed-physical-cutoff convention for \(L\) and \(2L\) | **BLOCKED** |
| 7. Comparison with the original \(\mathbb R^3\) Gaussian | **BLOCKED** |

### 1. Stepper — PASS

`grid`, `project`, `nonlinear`, and `step` in both `gaussian_gate_d.py` and `gaussian_gate_d_with_sidecar.py` match the locked file, including `gaussian_curl`. `diagnostics` and `run` differ. The packaged `test_step_unchanged` compares the sidecar `step` only with the copy inside the zip. The comparison above is against `scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py`.

Zip `gaussian_gate_d.py` SHA-256 `3bc81c79b9dfb9a5f8eebc773dfc5764d84bae6352fba8581ee87156dc7cbeb9`. Sidecar SHA-256 `bb92ae5b5ac52a5ca893633b4355c01342dfecd850ed55badf01aec00b58f80e`.

### 2. Masks — PASS

With `--signed-N`, `run` replaces the \(2/3\) cube by `make_galerkin_mask` before the initial projection and before `step` (`gaussian_gate_d_with_sidecar.py`). That mask is the componentwise cube \(|m|<n/3\) intersected with \(m_x^2+m_y^2+m_z^2\le N^2\), and it rejects \(N\ge n/3\) (`mask_policy.py`). \(L\) is an unused argument. The integer ball is the Galerkin cutoff.

`check_highpass` only requires \(0\le K<N\). The evolution mask does not apply \(K\). `assess` skips modes with \(r^2\le K^2\) and rejects a nonzero coefficient outside \(N^2\) (`integrated_gate.py`). Because \(N<n/3\), that sphere sits inside the \(2/3\) cube, so the diagnostic \(N\)-cut and the evolution mask are the same integer ball.

The log sentence `periodization: sample Gaussian on periodic cube, then project and 2/3 filter` still names only the cube on a run whose `cutoff` field correctly names the spherical intersection. That sentence is a label defect. It does not change the mask passed to `step`. `high_fraction` remains a separate physical energy shell and is not the integer high-pass \(K\).

### 3. `sign_unverified` — PASS

The guarded sidecar path itself does what this item asks of that path. `assess` returns `T_sc: None`, `D_sign: 'unknown'`, and `sign_certified_for_stored_coefficients: False` when the mode budget is exceeded (`integrated_gate.py`). `diagnostic_record` sets `crossing_certified: False` on every record (`logger_bridge.py`). The \(n=24\) smoke rows have `diagnostic_status=sign_unverified`, `T_sc` null, `D` null, and `crossing_certified` false.

Two holes remain in the same archive.

- `adaptive_certified.evaluate` still returns `fast_value` equal to the vorticity transfer on a record whose status is `sign_unverified`. On `make_pair(52)` with `max_exact_modes=2`, that value was about \(5.594\times 10^{-12}\) while `T_sc` was null. The metadata repair does not change this file.
- The original header set `T_sc_implemented` and `D_implemented` true. The metadata repair replaces those with `T_sc_code_available` and `D_code_available`, and it sets `accepted_T_sc_verified`, `accepted_D_verified`, and `crossing_certified` false. That header hole is closed. The `fast_value` hole is not.

Under this requirement, `sign_unverified` does not establish a crossing. `fast_value` can still sit on that record. It is not an accepted crossing.

### 4. Guarded bypass — PASS

With `--safe-sidecar`, `run` calls `diagnostics` with both signed cutoffs forced to `None`, then calls `diagnostic_record`. `diagnostics` calls `signed_diagnostics` only when the signed cutoff is set. `assess` does not call `vorticity_scalene` or `evaluate_checked`. `test_no_exploratory_signed_call` patches `signed_diagnostics` to raise, and that test passed. The stepper’s `nonlinear` still runs, because the row still stores production and \(G\). That is the RK4 nonlinearity, not the exploratory signed evaluator.

`adaptive_certified.evaluate` is not on this path. It still calls `vorticity_scalene` before deciding the status. Item 4 is the guarded mode only.

### 5. Exact fallback, cancellation, memory, uncertainty — BLOCKED

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

DA approval is pending. The recommended interpretation is filed in [`GATE-D-CUTOFF-CONVENTION-2026-10-09.md`](GATE-D-CUTOFF-CONVENTION-2026-10-09.md): \((L,N=128)\) matches \((2L,N=256)\), and \((L,N=160)\) matches \((2L,N=320)\). The original labels stay the reference-box cutoffs. The doubled-box runs are extra matched-resolution comparisons, and they are resource-blocked. The logger header that keeps the same integer \(N\) on a doubled box is the other reading. It is not this recommendation.

`assess` certifies a \(D\) sign only when \(L\) is exactly \(2\pi\). At \(L=4\pi\), `make_pair(52)` returns `physical_box_sign_unverified`, with no \(T_{\mathrm{sc}}\), `D_sign` unknown, and `crossing_certified` false. A sign of \(D\) on a frozen coefficient array does not certify the trajectory that produced the array.

### 7. \(\mathbb R^3\) comparison — BLOCKED

Blocked as an audit of a completed comparison. The requirements are already fixed. The periodic sample on a box is not the \(\mathbb R^3\) packet until periodization, box size, and domain convergence are shown (`scripts/ns_attacks/gate_d_gaussian_scaffold/README.md`).

## Metadata repair

`gate_d_metadata_repair_candidate_2026-10-09.zip`, SHA-256 `8d07445a462f880bf96126010231c559ef27e968de5c2a13f52c9140c76db8d6`, is filed at `scripts/ns_attacks/gate_d_metadata_repair/`. The guarded-logger zip in the same review folder is the archive already tested: SHA-256 `ca01fa9ab93950174ae3ca25a932c8778910e1fc71d075deda559df914f9e020`.

Every shared file matches that logger except `gaussian_gate_d_with_sidecar.py`. The header no longer has `T_sc_implemented` or `D_implemented`. It sets `T_sc_code_available` and `D_code_available` from the signed cutoffs, and it sets `accepted_T_sc_verified`, `accepted_D_verified`, and `crossing_certified` false. `grid`, `project`, `nonlinear`, and `step` still match the locked stepper.

Fourteen tests passed here in 1.985 s, including `test_metadata_is_not_certificate`. The smoke is \(s=0.01\). The periodization sentence still says “project and 2/3 filter” on a run whose cutoff is the spherical intersection. `adaptive_certified.py` and `integrated_gate.py` are unchanged, so `fast_value` is still returned on `sign_unverified`, and the viscosity is still `Fraction(float(1/200))`.

## Next required patch

The logger patch is separate from items 6 and 7. The four RK4 bodies stay matched to the locked file.

- On every `sign_unverified` record, including `adaptive_certified.evaluate`, omit `fast_value` and every other numeric transfer. Make the periodization sentence name the spherical mask that `step` actually receives.
- Build the viscosity as `Fraction(1, c)` from the integer \(c\). Certify a \(D\) sign only from that rational. Put the normalized exact \(Y\), and a float enclosure of both \(T_{\mathrm{sc}}\) and \(Y\), on the log record. Keep `rigorous_error_bound` false until a bound exists. That sign still does not certify the trajectory.

The frozen \(c=200\), \(s\ge 4\) trajectory stays unlaunched.

## STATUS

ARCHIVE SHA-256: MATCHES.
TESTS HERE: 13 PASSED, 1.979 s. SMOKE \(s=0.01\) ONLY.
ITEM 1 STEPPER BODIES: PASS. LOCKED FILE UNCHANGED.
ITEM 2 MASKS: PASS.
ITEM 3 `sign_unverified`: PASS. IT DOES NOT ESTABLISH A CROSSING. `fast_value` IS STILL RETURNED AND IS NOT A CROSSING.
ITEM 4 GUARDED BYPASS: PASS.
ITEM 5 LARGE-FIELD CERTIFICATION: BLOCKED. VISCOSITY RATIONAL IS NOT \(1/200\). LOGGED \(Y\) HAS NO ENCLOSURE. NOT A PRODUCTION CERTIFICATE.
ITEM 6 FIXED PHYSICAL CUTOFF: BLOCKED. RECOMMENDED \((L,128)\leftrightarrow(2L,256)\) AND \((L,160)\leftrightarrow(2L,320)\). DA APPROVAL PENDING. MATCHED RUNS RESOURCE-BLOCKED.
ITEM 7 \(\mathbb R^3\): BLOCKED. DOMAIN CONVERGENCE NOT SHOWN.
METADATA REPAIR: SHA `8d07445a462f880bf96126010231c559ef27e968de5c2a13f52c9140c76db8d6`. HEADER NO LONGER CLAIMS ACCEPTED \(T_{\mathrm{sc}}\). 14 TESTS PASSED IN 1.985 s. `fast_value` AND THE VISCOSITY RATIONAL UNCHANGED.
A SIGN OF \(D\) ON A FROZEN COEFFICIENT ARRAY DOES NOT CERTIFY THE TRAJECTORY.
LEMMA 19: NOT CERTIFIED. PACKAGED WITNESS AGREEMENT \(+32\) ONLY.
FROZEN \(c=200\), \(s\ge 4\): NOT LAUNCHED.
NO TURNOVER, REGENERATION, SHARED BUDGET, OR REGULARITY.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
