# Gate D adaptive signed-transfer evaluator — October 9, 2026

A hybrid diagnostic candidate was added without changing the Gaussian Navier–Stokes stepper. `hybrid_signed.py` selects direct *ordered* Fourier convolution for genuinely sparse coefficient support and falls back to the existing FFT-shell evaluator when the number of occupied modes squared exceeds `max_pairs`. There is no coefficient-magnitude threshold. The existing spherical cutoff and high-pass conventions are retained.

Command: `python -m unittest -q test_batched test_fast_signed test_connected test_mask_repair test_hybrid`
Result: 14 tests PASS (2.561 s). This includes the +32 six-mode witness, FFT-shell agreement on a projected random field, and earlier mask/reference tests.

Sparse witness indicative single-run times, seconds, for n=18,24,30: FFT-shell 0.03876,0.20828,0.40000; sparse-ordered 0.00037,0.00039,0.00053. This is a deliberately sparse field and is **not** a dense-shell benchmark or evidence of performance at N=128/160. The adaptive branch has no demonstrated dense speedup over the prior FFT-shell code.

Limitations: no rigorous floating-point forward-error bound, no enforced wall-clock or RSS limit, no high-cutoff benchmark, no L-versus-2L physical cutoff approval, no R3-versus-periodic convergence. `max_pairs` is a complexity switch, not a memory certificate. The FFT-shell fallback may still be expensive. The fixed c=200 trajectory has not run. Gate D OPEN / BLOCKED.
