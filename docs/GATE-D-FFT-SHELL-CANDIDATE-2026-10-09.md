# FFT shell-subtraction candidate

9 October 2026.
**Diagnostic prototype. Not an approved production evaluator. The frozen \(c=200\) experiment was not launched. Gate D remains OPEN / BLOCKED.**

Archive SHA-256: `555cc89b7bc48425be8942c9071b755ab5d376a7b6283be3c1ec24f9459d65ce`.
Files: `scripts/ns_attacks/gate_d_fft_shell_candidate/`.

The candidate sets \(T_{\mathrm{sc}}(h)=T_{\mathrm{full}}(h)-T_{\mathrm{rep}}(h)\), with one FFT convolution per occupied squared-radius shell. Physical derivatives use \(2\pi/L\), and the integral uses \(L^3\). `signed_phi.py` in the archive matches the filed September reference byte for byte. The locked stepper file was not edited. Its SHA-256 remains `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`. In this copy, `step` has the same body; `diagnostics` and `run` accept an optional integer high-pass, and `run` can replace the evolution mask when `--signed-N` is set.

## Checks rerun here

`python3 -m unittest -v test_fast_signed test_connected test_mask_repair` passed: 9 tests.

On the packaged \(m=2\), \(A=1\) witness with \(K=1\), \(N=6\):

| box | `fast_scalene` | bridge | \(32 L^3\) |
| --- | --- | --- | --- |
| \(L=2\pi\) | \((2\pi)^3\cdot 32\) | \((2\pi)^3\cdot 32\) | \((2\pi)^3\cdot 32\) |
| \(L=4\pi\) | \((2\pi)^3\cdot 32\) | \((2\pi)^3\cdot 32\) | \(8\cdot(2\pi)^3\cdot 32\) |

At \(L=2\pi\), \(32 L^3\) equals the torus value \(+32\) times \((2\pi)^3\). At \(L=4\pi\) the two evaluators stay on \((2\pi)^3\cdot 32\) and do not follow \(32 L^3\). The \(L\) versus \(2L\) comparison is still unresolved.

One benchmark rerun, \(N=3\), agreed with the pair reference to about \(10^{-16}\). The timings were speedups \(1.21\), \(0.25\), and \(0.17\) at \(n=12,18,24\). They do not reproduce the archive note’s \(3.3\times\), \(0.70\times\), and \(0.37\times\). One run is not a production projection. Process RSS on this rerun was \(51212\) KiB.

## Still blocked

No certified accumulation-error bound, no large-\(N\) benchmark, no physical-cutoff preregistration, and no \(\mathbb R^3\) domain convergence. The original Lemma 19 coefficients remain uncertified. The locked \(G\) unit test was not rerun. No turnover, regeneration, or cutoff-independent budget is claimed.

## STATUS

CANDIDATE: FILED. NOT APPROVED FOR PRODUCTION.
NINE PACKAGED TESTS: PASSED HERE.
\(L=2\pi\) WITNESS: \(32 L^3=(2\pi)^3\cdot 32\).
\(L=4\pi\): SAME VALUE, NOT \(32 L^3\).
LOCKED STEPPER FILE: UNCHANGED.
BENCHMARK SPEEDUPS IN THE ARCHIVE NOTE: NOT REPRODUCED ON THIS RERUN.
FROZEN \(c=200\) EXPERIMENT: NOT LAUNCHED.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
