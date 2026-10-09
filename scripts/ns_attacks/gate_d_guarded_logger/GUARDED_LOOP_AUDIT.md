# Gate D guarded logger fix — 2026-10-09

Inspected the connected Gaussian driver and found a fail-closed bypass: `diagnostics(...)` ran the expensive exploratory signed evaluator **before** the safe sidecar nulled its output. This could consume substantial time and memory, even when the accepted result was `sign_unverified`.

Repair: with `--safe-sidecar`, skip the exploratory signed computation entirely; call the exact-sparse fail-closed sidecar directly, and log `diagnostic_status`, `T_sc`, `D`, `d_over_X`. Unverified fields remain null. The original RK4 `step()` source is unchanged.

Tests: `python -m unittest -q test_guarded_loop test_loop_sidecar test_logger_bridge test_integrated_gate`: 10 PASS. A mocking test asserts the exploratory signed evaluator is NEVER called in safe-sidecar mode. Small n=24, N=6, K=1, L=12, c=200, s_end=.01 smoke returns `sign_unverified`, no crossing.

Limitations: No rigorous numerical-error certificate, large-N scalability, approved L/2L physical cutoff, or R³ domain convergence. Exact sparse sidecar remains a diagnostic prototype; no frozen s>=4 run. Gate D OPEN/BLOCKED.
