# Gate D — adversarial turnover test (protocol)

8 October 2026.
**Next calculation under the obstruction protocol. Not (17).**

Parent: [`GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md`](GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md).

---

## Question

\[
\boxed{\textbf{Does nonlinear turnover supply exactly the missing half derivative?}}
\]

Use the coherent packet that realizes the sharp static \(H^{1/2}\)
obstruction (Gate C), not an arbitrary field.

---

## Pipeline

\[
\text{coherent Gate-C packet}
\longrightarrow
\text{exact }D(0),\,D'(0)
\longrightarrow
\text{turnover-scale episode law}
\longrightarrow
\text{measure }H^{5/2}\lvert I_H\rvert
\]

### Scales ( \(E=1\) normalization )

| Quantity | Scaling |
|---|---|
| \(X\) | \(H^2\) |
| \(Y\) | \(H^4\) |
| \(\mathcal T_{\mathrm{sc}}\) | \(H^{9/2}\) |
| Normalized height \(\mathcal T_{\mathrm{sc}}/X\) | \(H^{5/2}\) |
| Viscous time \(\tau_\nu\) | \(H^{-2}\) → product \(H^{1/2}\) (not enough) |
| Target window / \(\tau_{\mathrm{nl}}\) | \(H^{-5/2}\) |

### Pass / fail

| Measured \(H^{5/2}\lvert I_H\rvert\) | Reading |
|---|---|
| \(O(1)\) (window \(\sim H^{-5/2}\)) | Turnover matches the missing half — promote Turnover Lemma |
| \(\gg 1\) (window \(\gtrsim H^{-2}\) at full height) | Gate D in serious trouble |

---

## Deliverables

1. Exact \(D(0)\), \(D'(0)\) for the coherent packet.
2. Episode interval \(I_H\) (or proxy) and \(H^{5/2}\lvert I_H\rvert\).
3. Comparison to \(\sum B_I\) / \(\mathcal S_{K,N}\) integrands using the
   archive episode identity when available.

---

## STATUS

PROTOCOL READY — EXECUTION PENDING.
NS NOT SOLVED.
