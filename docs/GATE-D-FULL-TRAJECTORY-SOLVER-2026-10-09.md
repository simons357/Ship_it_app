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
- \(B_{I_H}=\int_{I_H}d\,dt\) only (\(d=D/X\); do **not** add \((b-a)d(a)\)),
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
- Detect first downward \(d\)-crossing; quadrature \(B_I=\int d\,dt\) only
  (boundary term is reconstruction, not additive).

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

**Preferred engine:** FFT rfft `complex64` with **Orszag dealias**
\(N\ge 3k_{\max}\) (⇒ \(N=768\) at cutoff \(4H=252\)), fixed \(K\), full
\(X,Y\), and \(B_I=\int d\,dt\) only. See
[`GATE-D-FFT-CORRECTIONS-2026-10-09.md`](GATE-D-FFT-CORRECTIONS-2026-10-09.md).

Prior \(N=512\) / double-counted / \(X_H,Y_H\) runs are **not** Gate D evidence.

---

## Acceptance for a Gate D numerical filing

1. `verify_signed_gate` PASS on the same packet bytes.
2. Method string does **not** contain `topM`.
3. \(t=0\) \(T_{\mathrm{sc}}\) matches verifier; energy-identity residual small.
4. \(B_{I_H}=\int d\,dt\) only; boundary field is documentation-only.
5. JSON reports `B_over_R` for fixed \(K\), full \(X,Y\); `dealiased: true`.
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

### FFT Galerkin — corrections pending re-smoke

See [`GATE-D-FFT-CORRECTIONS-2026-10-09.md`](GATE-D-FFT-CORRECTIONS-2026-10-09.md).

| Issue in `18a267f3` | Fix |
|---|---|
| \(B_I\) double-counted \((b-a)d(a)\) | \(B_I=\int d\,dt\) only |
| \(N=512\) aliases at \(k_{\max}=252\) | \(N=768\) Orszag |
| \(H\)-filter \(X_H,Y_H\) | fixed \(K\), full \(X,Y\) |

Prior FFT smoke / “\(D\) rising” partial: **PROVISIONAL_INVALID**.

---

## STATUS

CORRECTIONS FILED; PRIOR FFT EVIDENCE DEMOTED.
FULL FIRST EPISODE: UNRUN.
LEMMA: NOT STAMPED.
NS NOT SOLVED.
