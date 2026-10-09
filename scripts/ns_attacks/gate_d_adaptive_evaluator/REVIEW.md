# Gate D shell-batched evaluator — experimental candidate, 2026-10-09

Implements full-minus-repeated signed transfer using vectorized batches of occupied squared-radius shells. Preserves original fast_signed.py reference and existing driver; **does not modify the Navier–Stokes stepper**. No coefficient deletion.

Tests: `python -m unittest -v test_batched` (3/3 PASS); additional existing regression tests remain available. Witness +32 at L=2π corresponds to +32 L³ for the physical integral.

Single-run indicative timings (seconds), reference / batched:
- n=18 N=4 S=14: 0.0314 / 0.0547 (0.57×)
- n=24 N=5 S=22: 0.1555 / 0.1380 (1.13×)
- n=30 N=7 S=42: 0.4913 / 0.6348 (0.77×)

These are not stable performance estimates; batching is NOT a demonstrated general speedup. The estimated memory cap is conservative and does not bound all NumPy FFT temporaries or peak RSS. No N=128/160 test.

Error monitoring recommendation: log |T_full|, |T_rep|, |T_sc|, cancellation ratio (|T_full|+|T_rep|)/max(|T_sc|,tiny), float64/longdouble or independent method comparisons, and compensated summation. **No rigorous forward error bound is established**. In particular, small differences on small tests are not a numerical certificate.

Physical cutoff matching, R³-to-periodic convergence, DA preregistration, and full c=200 trajectory remain BLOCKED.
