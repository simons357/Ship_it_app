# Gate D — adversarial turnover test (protocol)

8 October 2026 (corrections from 9 Oct review).
**Obstruction protocol — resource-weighted. Not (17).**

Parent: [`GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md`](GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md).
Review: [`GATE-D-REVIEW-2026-10-09.md`](GATE-D-REVIEW-2026-10-09.md).

---

## Question

\[
\boxed{\textbf{Does nonlinear turnover supply exactly the missing half derivative?}}
\]

Use the coherent packet that realizes the sharp static \(H^{1/2}\)
obstruction (Gate C), not an arbitrary field. **No Gaussian substitute.**

Do **not** stop at \(\lvert I_H\rvert\stackrel{?}{\lesssim}H^{-5/2}\).
Score
\[
\frac{B_{I_H}}{\mathcal R_{I_H}}
\]
as \(H\to\infty\), and whether \(\sum\mathcal R_I\) remains globally finite.

---

## Pipeline

\[
\text{coherent Gate-C packet}
\longrightarrow
\text{exact }D(0),\,D'(0)
\longrightarrow
\text{episode }I_H,\; B_{I_H}\text{ (include }(b-a)d(a)\text{ if }d(a)>0)
\longrightarrow
\frac{B_{I_H}}{\mathcal R_{I_H}}
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
| Target / \(\tau_{\mathrm{nl}}\) | \(H^{-5/2}\) (duration diagnostic only) |

### Pass / fail (resource-weighted)

Score by the **measured ratio** \(B_{I_H}/\mathcal R_{I_H}\) and global
summability of \(\mathcal R\). Coarse \(O(1)/o(1)\) slogans alone are
insufficient (9 Oct).

| Reading | Meaning |
|---|---|
| \(B_{I_H}\to 0\) | Extra gain — excellent |
| \(B_{I_H}/\mathcal R_{I_H}\) bounded and \(\sum\mathcal R<\infty\) | Recurrence paid by resource |
| \(B_{I_H}\) stays order-one while \(\mathcal R_{I_H}\) shrinks too fast for a global sum | **Gate D trouble** |
| \(H^{5/2}\lvert I_H\rvert\sim O(1)\) | Critical **duration** match only — still need resource for repetition |
| \(H^{5/2}\lvert I_H\rvert\gg 1\) at full height | Duration longer than critical — separate from resource score |

**Duration ≢ resource.** A window estimate
\(\lvert I\rvert\lesssim H^{-5/2}\) must not be treated as equivalent to
\(B_I\le C\mathcal R_I\).

Prototype resource (small Fourier-\(\ell^1\) only): \(\mathcal R\sim\int UW\,dt\)
controlling \(\lvert R_4\rvert\lesssim UWX\). Large-packet recurrence
resource remains an open mathematical gap.

---

## Episode cost (boundary term)

\[
B_I=\int_I\frac{D}{X}\,dt.
\]
If the episode starts at initial time with \(d(a)>0\), the first-moment
identity includes \((b-a)\,d(a)\) (episode-balance source). Restore it.

---

## Deliverables

1. Exact \(D(0)\), \(D'(0)\) for the coherent packet.
2. Episode \(I_H\), value \(B_{I_H}\) **with boundary term**, and
   \(H^{5/2}\lvert I_H\rvert\) as a duration diagnostic.
3. Candidate resource increment on \(I_H\) and the ratio
   \(B_{I_H}/\mathcal R_{I_H}\).
4. **Full-trajectory** evolution among retained modes — no top-\(M\)
   substitute. See [`GATE-D-FULL-TRAJECTORY-SOLVER.md`](GATE-D-FULL-TRAJECTORY-SOLVER.md).

---

## STATUS

PROTOCOL READY — RESOURCE-WEIGHTED; SCORE \(B_I/\mathcal R_I\).
DURATION ≢ RESOURCE; BOUNDARY TERM RESTORED.
FULL-TRAJECTORY SIX-BOX TEST: UNRUN.
NS NOT SOLVED.
