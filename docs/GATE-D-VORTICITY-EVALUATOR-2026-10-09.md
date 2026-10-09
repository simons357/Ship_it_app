# Vorticity-form signed evaluator

9 October 2026.
**Candidate. Not production certified. The frozen Gaussian trajectory was not run. Gate D remains OPEN / BLOCKED.**

Archive SHA-256: `01c5f84b775a96d21c6d2cc40f1d6f53500a071fbff658f13cf87fa90356dfe0`.
Files: `scripts/ns_attacks/gate_d_vorticity_evaluator/`.

`vorticity_scalene` evaluates \(T_{\mathrm{sc}}=T_{\mathrm{full}}-T_{\mathrm{rep}}\) from \((u\cdot\nabla)u=\nabla(|u|^2/2)-u\times\operatorname{curl}u\), using divergence-free receivers. Each occupied squared-radius shell takes inverse FFTs of velocity and vorticity. There is no coefficient-magnitude cutoff. `grid`, `project`, `nonlinear`, and `step` match the locked stepper. The locked file was not edited. Its SHA-256 remains `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`. The shared files match the adaptive-evaluator copy byte for byte.

## Checks rerun here

`python3 -m unittest -v test_vorticity_signed` passed: 2 tests, 1.162 s. The witness check is \(32 L^3\) at \(L=2\pi\). The dense checks at \((n,N)=(18,4)\), \((24,5)\), and \((30,7)\) agree with `fast_scalene` inside the test tolerance.

The archive’s one-off timing table was not rerun. No vorticity benchmark script is in the zip. That table is not a certified speedup.

## Still blocked

No \(N=128/160\) benchmark, no hard memory cap, no forward-error bound, no \(\mathbb R^3\) convergence, and no \(L\) versus \(2L\) approval. Measured agreement is not a cancellation certificate for \(T_{\mathrm{full}}-T_{\mathrm{rep}}\). The original Lemma 19 coefficients remain uncertified. The locked \(G\) unit test was not rerun. No turnover, regeneration, or cutoff-independent budget is claimed.

## STATUS

CANDIDATE: FILED. NOT PRODUCTION CERTIFIED.
TWO TESTS: PASSED HERE.
ARCHIVE TIMING TABLE: NOT RERUN.
LOCKED STEPPER: UNCHANGED.
FROZEN TRAJECTORY: NOT RUN.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
