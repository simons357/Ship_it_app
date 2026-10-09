# Program gates A–D — narrowed order

8 October 2026; notation fixed 9 October 2026 from the sharp-band source.
**Sharp signed band \(H^{1/2}\) → resource-weighted turnover.
Not (17). Gate A is not closed by that source.**

Desk: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).
Kill A: [`GATE-A-KILL-CERTIFICATE.md`](GATE-A-KILL-CERTIFICATE.md).
Deficit C: [`GATE-C-HALF-DERIVATIVE.md`](GATE-C-HALF-DERIVATIVE.md).
Attack D: [`GATE-D-HALF-DERIVATIVE-ATTACK.md`](GATE-D-HALF-DERIVATIVE-ATTACK.md).
Review D: [`GATE-D-REVIEW-2026-10-09.md`](GATE-D-REVIEW-2026-10-09.md).

---

## Ruling

**Do not add a 52nd, 70th, or 100th finite family.**

[`sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt`](sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt)
defines \(H\) as wavenumber through \(H\le|k|\le 4H\). Its signed ratio
\(R(H)\) has matching power bounds of exponent \(1/2\). Gate C is closed for that audited assembly: the deficit is a
half derivative, with \(\Lambda\sim H\) denoting frequency, so
\(\Lambda^{1/2}\sim H^{1/2}\). If squared frequency is \(L=H^2\), the same
factor is \(L^{1/4}\). The same source leaves Gate A diagnostic and unresolved.
Do not carry “Gate A killed.” The separate \(L_{z_n}\) note is not that
closure and is not a premise of Gate C. This does not prove (17).
Gate D **target** (not stamped lemma):
\[
\boxed{\textbf{Resource-Weighted Turnover Lemma}}
\]
\[
B_I=\int_I d(t)\,dt\le C\mathcal R_I,
\qquad
\sum_I\mathcal R_I\le C_{\mathrm{data},\nu,T},
\]
constants uniform in the Galerkin cutoff. Critical turnover \(H^{-5/2}\)
is a duration scale. Fast turnover does not settle recurrence: the
resource must pay for repeated episodes without reusing the same budget.
Duration ≢ resource. Score \(B_I/\mathcal R_I\).
Prototype: small-\(\ell^1\) \(R_4\) with \(\int UW\) — large-packet
repetition resource still open.

---

## Gate order

\[
\boxed{
\text{static deficit}
\to H^{1/2}
\to
\text{critical turnover }H^{-5/2}
\to
\text{resource for recurrence}
}
\]

| Gate | Mission | Status |
|---|---|---|
| **A** | As named by the sharp-band source | **Diagnostic and unresolved** |
| **B** | Shared-energy accounting | Not the band exponent |
| **C** | Sharp instantaneous signed band | **CLOSED — deficit \(H^{1/2}\)** (wavenumber; \(L^{1/4}\) if \(L=H^2\)) |
| **D** | Turnover and recurrence | **OPEN — not stamped; evidence pending** |

---

## Parked

- No 51→70→100 family extensions
- No shell-count / Young / generic instantaneous phase as main line
- No random-phase fishing; Ring without bridge; swirl-as-substitute; B41→NSE
- No Gaussian substitute for the six-box Signed-Gate adversary

---

## Immediate work (Gate D)

1. Feasible full-trajectory six-box solver preserving signed-scalene
   diagnostic — [`GATE-D-FULL-TRAJECTORY-SOLVER.md`](GATE-D-FULL-TRAJECTORY-SOLVER.md).
2. Score \(B_{I_H}/\mathcal R_{I_H}\) with \(B_I=\int d\,dt\) only
   (boundary term is reconstruction, not additive).
3. Demote prior top-\(M\) “complete episode” rows
   ([`GATE-D-ADVERSARIAL-RUN-RESULTS.md`](GATE-D-ADVERSARIAL-RUN-RESULTS.md)).
4. Next test: a completed, corrected episode followed through
   regeneration, measuring both \(B_I/\mathcal R_I\) and cumulative
   resource use. A successful finite run would support the target, not
   prove the uniform bound. Lemma remains a target, not a stamp.

---

## STATUS

GATE A: DIAGNOSTIC AND UNRESOLVED IN THE SHARP-BAND SOURCE.
GATE C: CLOSED FOR THE AUDITED ASSEMBLY — \(\Lambda^{1/2}\sim H^{1/2}\) (\(\Lambda\sim H\) = FREQUENCY).
GATE D: OPEN — BOTH OBLIGATIONS REQUIRED, UNIFORM IN CUTOFF (NOT STAMPED).
IMPLEMENTATION CORRECTED; DYNAMICAL EVIDENCE PENDING.
FULL CORRECTED EPISODE THROUGH REGENERATION: UNRUN.
NS NOT SOLVED.
