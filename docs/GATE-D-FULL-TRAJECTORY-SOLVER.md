# Gate D — feasible full-trajectory solver

Dated: [`GATE-D-FULL-TRAJECTORY-SOLVER-2026-10-09.md`](GATE-D-FULL-TRAJECTORY-SOLVER-2026-10-09.md).

Six-box full trajectory still unrun. Measurement module is the tested
reference (initials, generated modes, initial boundary term, 80-mode check):
[`GATE-D-SIGNED-MEASUREMENT-MODULE.md`](GATE-D-SIGNED-MEASUREMENT-MODULE.md).

First-step cutoff comparison only: \(8H\) and \(12H\) differ by about
\(1.27\times 10^{-9}\) in \(L^2\) at energy 1. That does not establish
later-trajectory convergence. Continuation still running with the same
field, viscosity, cutoff, and time step. Next derivative is about \(8.1\)
billion ordered mode pairs. No further accepted state
([`GATE-D-CUTOFF-CHECK.md`](GATE-D-CUTOFF-CHECK.md)).
