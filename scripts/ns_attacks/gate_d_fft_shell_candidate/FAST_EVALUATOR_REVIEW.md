# Gate D FFT shell-subtraction candidate — 2026-10-09

This is a diagnostic prototype, NOT an approved production evaluator.

Identity: T_sc(h)=T_full(h)-T_rep(h), with T_rep=-Re sum_a <B(h_a,h_a),(A-a)h>. Physical derivatives use 2π/L, and the physical integral uses L³. Input vh must already obey the agreed Galerkin mask. High-pass K is applied only to the diagnostic.

The shell algorithm uses one nonlinear FFT convolution per occupied exact squared-radius shell; it is NOT O(M²) pair enumeration. It can be expensive when the number of occupied shells is large. No coefficient deletion threshold is used.

Run: python -m unittest -v test_fast_signed test_connected test_mask_repair
Benchmark: python benchmark_fast.py

Observed small sparse-field benchmarks: n=12 reference 0.0202 s vs FFT 0.0061 s; n=18 reference 0.0137 s vs FFT 0.0197 s; n=24 reference 0.0195 s vs FFT 0.0528 s. Single runs, not reliable production projections. Max process RSS during benchmark ~110376 KiB (includes interpreter, imports, and allocations; not evaluator-only memory).

Critical blockers: no certified accumulation-error bound, no large-N performance benchmark, no physical cutoff preregistration, no R³ domain convergence. Full production run NOT authorized.

The six-mode witness on L=2π returns 32 L³ in physical-integral normalization, corresponding to +32 on the normalized torus.
