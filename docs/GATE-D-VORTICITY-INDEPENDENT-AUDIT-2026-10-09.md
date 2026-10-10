# Independent vorticity audit

9 October 2026.
**Conditional pass on packaged regression and one single-pass comparison. Hardening applied. The cancellation ratio is not an error bound. The frozen \(c=200\) experiment was not launched. Gate D remains OPEN / BLOCKED.**

The named archive `GATE_D_VORTICITY_INDEPENDENT_AUDIT_2026-10-09(1).zip` was not in the uploads folder. This note records the decision text supplied with that name.

## ZIP

Uploaded evaluator `gate_d_vorticity_evaluator_2026-10-09_1abc.zip`, SHA-256 `01c5f84b775a96d21c6d2cc40f1d6f53500a071fbff658f13cf87fa90356dfe0`. Reconfirmed here. It matches the hash recorded with the filing in [`GATE-D-VORTICITY-EVALUATOR-2026-10-09.md`](GATE-D-VORTICITY-EVALUATOR-2026-10-09.md).

## Their regression

The combined regression against the ZIP’s Python files completed in 1.818 seconds. It covered the signed-transfer witness, dense-field comparisons, the FFT bridge, and mask behavior. That confirms the candidate passes its packaged regression tests in that environment. It does not establish production-scale accuracy or speed. That clock is theirs. It is not the clock below.

## Their single-pass benchmark

Four dense random divergence-free fields. Their measurement. Not rerun here.

| Grid / cutoff | Previous FFT-shell | Vorticity evaluator | Speedup |
| --- | ---: | ---: | ---: |
| \(18^3\), \(N=4\) | 0.0241 s | 0.0120 s | 2.01× |
| \(24^3\), \(N=5\) | 0.1003 s | 0.0357 s | 2.81× |
| \(30^3\), \(N=7\) | 0.4158 s | 0.1146 s | 3.63× |
| \(39^3\), \(N=12\) | 3.3633 s | 1.0609 s | 3.17× |

The two implementations agreed within approximately \(2.7\times 10^{-15}\) absolute error on these four fields. This reproduces a basic speed advantage at the tested sizes. It is not a stabilized performance study and it is not a numerical-error certificate.

## Decision

Conditional pass. Keep this faster evaluator. The audit named three remaining production issues: Hermitian symmetry and incompressibility were assumed at entry; input and memory-limit validation was incomplete; cancellation in \(T_{\mathrm{full}}-T_{\mathrm{rep}}\) has no certified numerical-error bound.

## Hardening applied after that decision

`vorticity_scalene` now checks the input before the transfer.

- \(L\) is positive and finite. \(K\) is nonnegative. If \(N\) is set, \(0\le K<N\) and \(N<n/3\).
- Coefficients are finite.
- Hermitian symmetry uses the partner index \((-\mathrm{arange}(n))\bmod n\) on the three wave axes, compared with the conjugate. A defect above \(\mathrm{tol}\cdot\max(1,\max|h|)\) raises `ValueError`. The default tolerance is \(10^{-6}\).
- The divergence check is the integer-mode contraction \(m\cdot\hat h\), at the same tolerance.
- The byte estimate is four complex vector fields plus four real vector fields. One complex field is \(3n^3\cdot 16\) bytes. The default cap is 256 MiB. An estimate above the cap raises `MemoryError`. The estimate does not cover every NumPy temporary and is not a peak-RSS certificate.

`return_parts=True` reports \(|T_{\mathrm{full}}|\), \(|T_{\mathrm{rep}}|\), \(|T_{\mathrm{sc}}|\), and

\[
\frac{|T_{\mathrm{full}}|+|T_{\mathrm{rep}}|}{\max(|T_{\mathrm{sc}}|,\mathrm{tiny})},
\]

together with the two defects, the byte estimate, the cap, and `cancellation_ratio_is_not_an_error_bound: True`. The ratio is a report. It is not a certified bound on the cancellation in \(T_{\mathrm{full}}-T_{\mathrm{rep}}\).

The transfer formula is unchanged. The locked stepper file was not edited. Its SHA-256 remains `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`.

## Checks here after hardening

`python3 -m unittest -v test_vorticity_signed` passed: 3 tests, 1.188 s. The witness check is \(32 L^3\) at \(L=2\pi\). The dense checks at \((n,N)=(18,4)\), \((24,5)\), and \((30,7)\) agree with `fast_scalene` inside the test tolerance. The new test checks the cancellation report on the packaged witness, rejects a Hermitian break, rejects a longitudinal break, and rejects `max_bytes=1`.

The locked \(G\) unit test was not rerun. No further scale-up was run. The frozen \(c=200\) experiment was not launched.

## Still open

No certified numerical-error bound. No \(N=128/160\) benchmark. No \(L\) versus \(2L\) approval. No \(\mathbb R^3\) convergence. Lemma 19 original coefficients remain uncertified. No turnover, regeneration, or cutoff-independent budget.

## STATUS

AUDIT: CONDITIONAL PASS ON PACKAGED REGRESSION AND ONE SINGLE-PASS COMPARISON.
AUDIT ZIP: NOT IN THIS UPLOADS FOLDER. DECISION TEXT IS THE SOURCE.
ZIP SHA-256: MATCHES THE RECORDED HASH.
HARDENING: ENTRY CHECKS, BYTE CAP, CANCELLATION REPORT. THE RATIO IS NOT AN ERROR BOUND.
TESTS HERE AFTER HARDENING: 3 PASSED, 1.188 s.
THEIR REGRESSION: 1.818 s. NOT THIS CLOCK.
THEIR BENCHMARK: FILED AS THEIR MEASUREMENT. NOT RERUN HERE.
LOCKED STEPPER: UNCHANGED.
FROZEN \(c=200\): NOT LAUNCHED.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
