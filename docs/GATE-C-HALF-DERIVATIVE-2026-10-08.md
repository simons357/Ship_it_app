# Gate C — exact missing exponent

8 October 2026. Wording tightened 9 October 2026.
**CLOSED for the audited assembly. Not (17). Not a claim about every estimate.**

Parents:
[`GATE-A-KILL-CERTIFICATE-2026-10-07.md`](GATE-A-KILL-CERTIFICATE-2026-10-07.md),
[`GATE-B-SHARED-ENERGY-2026-10-07.md`](GATE-B-SHARED-ENERGY-2026-10-07.md).

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

---

## Frequency convention

\(H\) is frequency. In the schematic below, \(\Lambda\) means that same frequency,
\[
\Lambda\sim H,
\]
not squared frequency. Squared frequency is \(H^2\) (as in \(X\sim H^2\)).

Under that reading
\[
\Lambda^{1/2}\sim H^{1/2}
\]
is one half derivative.

If instead \(\Lambda=H^2\) were squared frequency, a half derivative would be
\(\Lambda^{1/4}=H^{1/2}\), and the written factor \(\Lambda^{1/2}\) would be
a full derivative. That reading is not used. Calling \(\Lambda^{1/2}\) a half
derivative requires \(\Lambda\) to mean frequency.

---

## RESULT

After Gate A (positive all-shape assembly killed) and the shared-energy
correction of Gate B — low modes forced to share
\(\sum_k\lvert u_k\rvert^2=E\) instead of each borrowing a full
\(\sqrt{E_0}\) — the residual aggregate of **this assembly** has schematic form
\[
\mathcal T_{\mathrm{bad}}
\lesssim
\nu Y\times\Lambda^{1/2}.
\]

The exact missing exponent of this assembly is therefore
\[
\boxed{\tfrac12},
\]
meaning \(\Lambda^{1/2}\) with \(\Lambda\) the frequency, equivalently \(H^{1/2}\).

Plain statement:

\[
\boxed{\text{We need a dynamical mechanism worth one half derivative.}}
\]

The enemy of this calculation is named. The sentence does not say that every
estimate loses the same power.

---

## Scope of CLOSED

CLOSED identifies the deficit of the audited assembly: the Gate A positive
all-shape load after the Gate B shared-energy redo. That closes that
calculation. It does not establish that every possible estimate must lose
the same exponent.

---

## What this is / is not

| Claim | Status |
|---|---|
| Deficit of the audited assembly | \(\Lambda^{1/2}\sim H^{1/2}\) (half derivative; \(\Lambda\) = frequency) |
| Every estimate loses \(\tfrac12\) | **Not claimed** |
| Proof of (17) | **Not claimed** |
| That signed / phase / B41 / C10 already supplies the half | **Open** — Gate D only |
| Further finite-family extensions | **Parked** |

---

## Gate D contract

Two obligations. Constants uniform in the Galerkin cutoff:
\[
B_I=\int_I d(t)\,dt\le C\mathcal R_I,
\qquad
\sum_I\mathcal R_I\le C_{\mathrm{data},\nu,T}.
\]

Critical turnover \(H^{-5/2}\) is a duration scale. Fast turnover alone does
not settle recurrence. The resource must pay for repeated episodes without
reusing the same budget.

Next decisive test: a completed, corrected episode followed through
regeneration.

Bridge: onset \(O(\rho^{-2})\) (amplitude) ↔ \(H^{1/2}\) (frequency).

Out of scope as substitutes: shell-count; Young; generic instantaneous
phase; Ring without bridge; swirl-as-substitute; B41→NSE; random-phase.

Setup corrections on the solver (episode cost, dealias, fixed \(K\)) do not
validate this contract. Status of that work: implementation corrected;
dynamical evidence pending.

---

## STATUS

GATE C: CLOSED FOR THE AUDITED ASSEMBLY — DEFICIT = HALF DERIVATIVE
(\(\Lambda\sim H\), so \(\Lambda^{1/2}\sim H^{1/2}\)).
NOT A UNIVERSAL EXPONENT FOR EVERY ESTIMATE.
GATE B: SHARED-ENERGY CORRECTION ACCEPTED AS THE SETUP FOR THIS EXPONENT.
GATE D: ACTIVE — TWO OBLIGATIONS ABOVE; DYNAMICAL EVIDENCE PENDING.
(17) NOT CLAIMED.
NS NOT SOLVED.
