# Gate D — adversarial turnover test (protocol)

8 October 2026.
**Obstruction protocol — resource-weighted. Not (17).**

Parent: [`GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md`](GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md).

---

## Question

\[
\boxed{\textbf{Does nonlinear turnover supply exactly the missing half derivative?}}
\]

Use the coherent packet that realizes the sharp static \(H^{1/2}\)
obstruction (Gate C), not an arbitrary field.

Do **not** stop at \(\lvert I_H\rvert\stackrel{?}{\lesssim}H^{-5/2}\).
Measure \(B_{I_H}\) against the candidate resource consumed on \(I_H\).

---

## Pipeline

\[
\text{coherent Gate-C packet}
\longrightarrow
\text{exact }D(0),\,D'(0)
\longrightarrow
\text{episode }I_H,\; B_{I_H}
\longrightarrow
\frac{B_{I_H}}{\text{resource on }I_H}
\text{ as }H\to\infty
\]

### Scales (\(E=1\))

| Quantity | Scaling |
|---|---|
| \(X\) | \(H^2\) |
| \(Y\) | \(H^4\) |
| \(\mathcal T_{\mathrm{sc}}\) | \(H^{9/2}\) |
| Normalized height \(\mathcal T_{\mathrm{sc}}/X\) | \(H^{5/2}\) |
| Viscous time \(\tau_\nu\) | \(H^{-2}\) → product \(H^{1/2}\) (not enough) |
| Target / \(\tau_{\mathrm{nl}}\) | \(H^{-5/2}\) |

### Pass / fail (resource-weighted)

| \(B_{I_H}\) | Resource on \(I_H\) | Reading |
|---|---|---|
| \(\to 0\) | any | Extra gain — excellent |
| \(O(1)\) | \(O(1)\) of globally finite \(\sum\mathcal R\) | OK — recurrence paid by resource |
| \(O(1)\) | \(o(1)\) | **Gate D trouble** |
| Window \(\sim H^{-5/2}\) at full height | — | Critical turnover match (still need resource for repetition) |
| Window \(\gtrsim H^{-2}\) at full height | — | Viscous scale only — static half survives |

Prototype resource (small Fourier-\(\ell^1\)): \(\mathcal R\sim\int UW\,dt\)
controlling \(\lvert R_4\rvert\lesssim UWX\).

---

## Deliverables

1. Exact \(D(0)\), \(D'(0)\) for the coherent packet.
2. Episode \(I_H\), value \(B_{I_H}\), and \(H^{5/2}\lvert I_H\rvert\).
3. Candidate resource increment on \(I_H\) and the ratio
   \(B_{I_H}/\Delta\mathcal R_{I_H}\).
4. Comparison to the archive episode identity when available.

---

## STATUS

PROTOCOL READY — RESOURCE-WEIGHTED.
Executable brief: [`GATE-D-ADVERSARIAL-RUN-BRIEF.md`](GATE-D-ADVERSARIAL-RUN-BRIEF.md).
Orbit-R4 + episode-balance excerpts: filed under `docs/sources/`.
EXECUTION: **BLOCKED** on six-box Signed-Gate packet bytes — see
[`GATE-D-EXECUTION-BLOCKER.md`](GATE-D-EXECUTION-BLOCKER.md).
NS NOT SOLVED.
