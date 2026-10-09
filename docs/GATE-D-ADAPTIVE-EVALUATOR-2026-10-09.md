# Adaptive signed-transfer evaluator

9 October 2026.
**Experimental candidate. Not a production evaluator. The frozen \(c=200\) trajectory was not run. Gate D remains OPEN / BLOCKED.**

Archive SHA-256: `df4b29dde808ae181d3a1ab8bf5e1533eb6429e77bc4c3021de2e70e1481696c`.
Files: `scripts/ns_attacks/gate_d_adaptive_evaluator/`.

`batched_signed.py` evaluates the full-minus-repeated transfer in batches of occupied squared-radius shells. `hybrid_signed.py` uses direct ordered convolution when the number of occupied modes squared is at most `max_pairs`, and otherwise calls the FFT-shell evaluator. There is no coefficient-magnitude cutoff. `grid`, `project`, `nonlinear`, and `step` match the locked stepper. The locked file was not edited. Its SHA-256 remains `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`. The shared shell-candidate files in this archive match `scripts/ns_attacks/gate_d_fft_shell_candidate/` byte for byte.

## Checks rerun here

`python3 -m unittest -v test_batched test_fast_signed test_connected test_mask_repair test_hybrid` passed: 14 tests, 2.676 s. The archive note’s 2.561 s was not the clock on this run.

The witness assertions use \(32(2\pi)^3\) at \(L=2\pi\). On that box, \(L^3=(2\pi)^3\), so the value is \(32 L^3\). The archive’s single-run batch timings were not rerun here. The archive itself says those timings are not a demonstrated general speedup.

## Still blocked

No forward-error bound, no \(N=128/160\) test, no \(L\) versus \(2L\) approval, and no \(\mathbb R^3\) convergence. `max_pairs` is a complexity switch. The original Lemma 19 coefficients remain uncertified. The locked \(G\) unit test was not rerun. No turnover, regeneration, or cutoff-independent budget is claimed.

## STATUS

CANDIDATE: FILED. NOT APPROVED FOR PRODUCTION.
FOURTEEN TESTS: PASSED HERE IN 2.676 s.
STEPPER BODY: UNCHANGED. LOCKED FILE UNCHANGED.
ARCHIVE BATCH TIMINGS: NOT RERUN HERE.
FROZEN \(c=200\) TRAJECTORY: NOT RUN.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
