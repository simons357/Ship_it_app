# Gate D — cutoff check at the first step

9 October 2026.
**Early-step comparison only. Continuation has not accepted another state. Not a turnover.**

The solver and the initial field were left unchanged. The larger cutoff was a separate comparison run.

With initial energy normalized to 1, the first-step velocity fields at \(8H\) and \(12H\) differ by about \(1.27\times 10^{-9}\) in \(L^2\). That comparison supports only the first step. It does not establish convergence of the later trajectory.

The continuation is still running with the same field, viscosity, cutoff, and time step. No additional state has been accepted yet. The calculation is not being tuned to force a turnover. Elapsed computation time tells us nothing further about the fluid.

At the last accepted state, the signed excess had risen from about \(16405\) to \(16602\). That step showed growth, not turnover.

The practical bottleneck is the next derivative: this sparse solver evaluates roughly \(8.1\) billion ordered mode pairs. The first-step cutoff comparison is complete. Continuing the trajectory is much more expensive.

One completed six-box episode would be evidence. Cutoff-uniform control and summable recurrence remain unproved. The signed static test stays complete. Dynamical control stays open.

---

## STATUS

FIRST-STEP \(8H\) VS \(12H\): \(L^2\) DIFFERENCE ABOUT \(1.27\times 10^{-9}\) AT ENERGY 1.
SCOPE: FIRST STEP ONLY. NOT LATER-TRAJECTORY CONVERGENCE.
NEXT DERIVATIVE: ABOUT \(8.1\) BILLION ORDERED MODE PAIRS.
SOLVER, FIELD, VISCOSITY, CUTOFF, TIME STEP: UNCHANGED.
CONTINUATION: STILL RUNNING. NO FURTHER ACCEPTED STATE. NOT TUNED.
ELAPSED COMPUTE TIME: NOT A FLUID OBSERVATION.
LAST ACCEPTED STEP: SIGNED EXCESS ABOUT \(16405\to 16602\). GROWTH, NOT TURNOVER.
NS NOT SOLVED.
