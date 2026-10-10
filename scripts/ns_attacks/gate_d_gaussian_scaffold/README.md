# Gate D Gaussian packet — replacement scaffold (2026-10-09)

**Not the recovered historical driver. Not DA-preregistered. Not a Gate D episode test.**

This runnable scaffold implements the specified analytic curl initial datum on a sampled periodic cube and evolves nondimensional classical unforced 3D NSE with viscosity 1/c using a 2/3-dealiased pseudospectral integrating-factor RK4 stepper. It records energy, X, Y, full enstrophy production, high-shell energy, and Fourier divergence. It does **not** implement the project's signed scalene triad transfer T_sc, its threshold D, or the project's precise G diagnostic; these fields are `null` deliberately. No downward crossing can be assessed with this code.

The R^3 Gaussian is sampled on [-L/2,L/2)^3, Fourier-projected, and dealiased; this is **not** the same initial datum as the R^3 field. L and 2L convergence and a matched physical spectral cutoff require preregistration. `n` here is grid points per axis, **not** automatically the Gate D cutoff N=128/160. The meaning of the frozen N must be resolved before production.

Run smoke: `python gaussian_gate_d.py --n 12 --L 12 --c 200 --s-end 0.02 --ds 0.01 --output smoke.jsonl`

Pending: obtain exact T_sc and G definitions, audit Gaussian curl and initial derivatives, choose physical box L and cutoff geometry, specify tolerances/checkpoint protocol, compare against existing PR #175 solver, get DA approval. The full frozen experiment has NOT run.
