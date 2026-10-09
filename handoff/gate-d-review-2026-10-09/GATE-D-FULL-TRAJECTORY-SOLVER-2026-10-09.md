# Gate D — feasible full-trajectory solver

9 October 2026.
**Engineering task. Preserves signed-scalene diagnostic. Not (17).**

Parent review: [`GATE-D-REVIEW-2026-10-09.md`](GATE-D-REVIEW-2026-10-09.md).
Protocol: [`GATE-D-TURNOVER-ADVERSARIAL-TEST.md`](GATE-D-TURNOVER-ADVERSARIAL-TEST.md).

---

## Requirement

Run the six-box Signed-Gate adversary on a **full** truncated Galerkin
trajectory (all interactions among modes retained in the ball), measure

- \(D_H(0)\), \(D_H'(0)\),
- first positive episode \(I_H\),
- \(B_{I_H}=\int_{I_H}D/X\,dt\) **plus** \((b-a)d(a)\) when \(d(a)>0\),
- candidate \(\mathcal R_{I_H}\) and the ratio \(B_{I_H}/\mathcal R_{I_H}\),

without substituting a Gaussian packet and without top-\(M\) mode pruning.

Dense spherical Galerkin at cutoff \(\ge 4H\) exceeds session memory.
This note specifies a **feasible** path that keeps the diagnostic exact
on the retained Galerkin set.

---

## Design (memory-feasible, diagnostic-exact)

### Retained set

- Ball cutoff \(N = cH\) with \(c\in\{4,8\}\) (author static sweep used \(8H\);
  start evolution at \(4H\) for \(n=1\), then raise).
- State = sparse map wavevector → \(\mathbb{C}^3\) (Hermitian, divergence-free).
- **No top-\(M\) truncation** of large modes.
- Amplitude floor only for numerical zeros (e.g. \(|\hat u|^2 < 10^{-30}E\)),
  documented in the run JSON — not an energy-ranking prune.

### Nonlinear term

- Exact truncated convolution among currently active modes in the ball
  (Leray projection; same convention as `gated_initial` /
  `verify_signed_gate`).
- RHS assembled in **tiles** (hash capacity capped; flush partial
  accumulators) so peak RAM stays \(O(\#\text{active} + \text{tile})\)
  rather than \(O(m^2)\) dense tables.
- Mode birth: any convolution product landing inside the ball is admitted.

### Signed-scalene diagnostic (must match static verifier at \(t=0\))

Reuse the ordered scalene transfer \(T_{\mathrm{sc}}\) from
`verify_signed_gate` / author sweep:

- pairwise distinct squared radii, all \(>K^2\),
- imaginary-coefficient six-box packet unchanged,
- energy identity check \(X'=-2\nu Y+2T_{\mathrm{sc}}\) at \(t=0\).

### Time integrator

- Explicit RK2 or RK4 with viscous CFL from \(\nu N^2\).
- Record \(D(t)\), \(X(t)\), \(U(t)\), \(W(t)\) every step.
- Detect first downward \(D\)-crossing; quadrature for \(B_I\) includes
  \((b-a)d(a)\).

### Scoring

Report \(B_{I_H}/\mathcal R_{I_H}\) with \(\mathcal R=\int UW\) as the
prototype candidate, plus \(\int X\) (already ruled out analytically) and
\(H^{5/2}\lvert I_H\rvert\) as a **duration diagnostic only**.

---

## Implementation

| Piece | Path |
|---|---|
| Sparse tiled (hits mode budget) | [`scripts/ns_attacks/gate_d_full_trajectory.py`](../scripts/ns_attacks/gate_d_full_trajectory.py) |
| **FFT Galerkin (feasible path)** | [`scripts/ns_attacks/gate_d_full_trajectory_fft.py`](../scripts/ns_attacks/gate_d_full_trajectory_fft.py) |
| Demoted top-\(M\) runner | [`scripts/ns_attacks/gate_d_adversarial_run.py`](../scripts/ns_attacks/gate_d_adversarial_run.py) — do not use for Gate D score |
| Static reference | [`scripts/ns_attacks/gated_initial.py`](../scripts/ns_attacks/gated_initial.py) |

**Preferred engine:** FFT rfft `complex64` on \(N=512\) for cutoff \(4H\) (\(n=1\)).
Sparse \(O(m^2)\) after mode birth exceeds the session mode budget; dense
spherical arrays without rfft OOM. FFT keeps the full ball without top-\(M\).

---

## Acceptance for a Gate D numerical filing

1. `verify_signed_gate` PASS on the same packet bytes.
2. Method string does **not** contain `topM`.
3. \(t=0\) \(T_{\mathrm{sc}}\) matches verifier; energy-identity residual small.
4. \(B_{I_H}\) includes boundary term when \(d(0)>0\).
5. JSON reports `B_over_R` explicitly.
6. No theorem stamp from a single \(n\).

---

## Smoke check (9 Oct)

### Sparse tiled (`gate_d_full_trajectory.py`)

| Check | Result |
|---|---|
| \(T_{\mathrm{sc}}\) vs verifier | rel err \(0\) |
| \(D_H(0)\), \(D_H'(0)\) | match signed-packet \(t=0\) |
| top-\(M\) | **false** |
| Episode complete | **No** — `MODE_BUDGET_HIT` (~82k modes) |

### FFT Galerkin (`gate_d_full_trajectory_fft.py`) — feasible path

`python3 gate_d_full_trajectory_fft.py --smoke --n 1 --max-steps 2`

| Check | Result |
|---|---|
| FFT \(N\) | 512 at cutoff \(4H=252\) |
| \(T_{\mathrm{sc}}\) vs verifier | rel err \(\sim 2\times10^{-7}\) |
| \(D_H(0)\) | \(1.536\times10^{4}\) (match) |
| \(D_H'(0)\) | \(3.712\times10^{6}\) (match) |
| Boundary term | included in \(B_{I_H}\) |
| top-\(M\) | **false** |
| Extract growth (steps 0→2) | \(424\to 1.3\times10^{4}\to 1.8\times10^{4}\) |
| \(D\) evolution | matches sparse smoke (\(1.536\to 1.559\times10^{4}\)) |
| Episode complete | **No** — smoke window only (~2–3 min/step) |

JSON: [`scripts/ns_attacks/GATE-D-FULL-TRAJECTORY-FFT-SMOKE.json`](../scripts/ns_attacks/GATE-D-FULL-TRAJECTORY-FFT-SMOKE.json).

Full first-episode at \(dt=2\tau_{\mathrm{nl}}\) is wall-time heavy; engine is no
longer memory-blocked. Review ZIP was **not** present under
`scratch/ec43035008f2/` this session — review text filed from the handoff message.

---

## STATUS

FEASIBLE FFT SOLVER + SMOKE FILED.
FULL FIRST EPISODE: STILL UNRUN (WALL TIME).
LEMMA: NOT STAMPED.
NS NOT SOLVED.
