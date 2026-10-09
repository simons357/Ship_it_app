# Gate C — exact missing exponent

8 October 2026. Notation fixed 9 October 2026 from the sharp-band source.
**CLOSED for the sharp instantaneous signed band estimate. Not (17).**

Source:
[`sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt`](sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt).

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

The same source leaves Gate A diagnostic and unresolved. This note does
not use “Gate A killed” as a premise.

---

## Frequency convention

\(H\) denotes wavenumber. The fields in the source are supported in the band
\[
H\le |k|\le 4H.
\]
The signed ratio is
\[
R(H)
=
\sup_{h\neq 0}
\frac{\lvert\mathcal T_{\mathrm{sc}}(h)\rvert}{\sqrt{E}\,Y},
\]
with
\(E=\sum_k\lvert\hat h(k)\rvert^2\) and
\(Y=\sum_k\lvert k\rvert^4\lvert\hat h(k)\rvert^2\).

Matching power bounds in that note give the exponent \(1/2\):
\[
R(H)\le 1728\sqrt{H},
\qquad
R(63n)\ge c_*\sqrt{63n}.
\]
The deficit is therefore \(H^{1/2}\): one half derivative in wavenumber.

If squared frequency is denoted by \(L=H^2\), the same factor is \(L^{1/4}\).

---

## RESULT

\[
\boxed{H^{1/2}}
\]

\[
\boxed{\text{We need a dynamical mechanism worth one half derivative.}}
\]

This is the exponent of this explicitly defined signed ratio. It is not a
determination of the earlier unsigned \(Q_x\) operator norm.

---

## Scope of CLOSED

CLOSED applies to the sharp instantaneous signed band estimate above.
It does not prove (17). Gate D’s turnover and recurrence bounds remain open.

---

## What this is / is not

| Claim | Status |
|---|---|
| Sharp instantaneous signed band | **CLOSED** — deficit \(H^{1/2}\) (wavenumber) |
| Same factor in squared frequency \(L=H^2\) | \(L^{1/4}\) |
| Gate A killed by this source | **No** — source leaves Gate A diagnostic and unresolved |
| Proof of (17) | **Not claimed** |
| Gate D turnover and recurrence | **Open** |
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

Out of scope as substitutes: shell-count; Young; generic instantaneous
phase; Ring without bridge; swirl-as-substitute; B41→NSE; random-phase.

Setup corrections on the solver do not validate this contract.
Status: implementation corrected; dynamical evidence pending.

---

## STATUS

GATE C: CLOSED FOR THE SHARP INSTANTANEOUS SIGNED BAND ESTIMATE.
DEFICIT \(H^{1/2}\) (WAVENUMBER): ONE HALF DERIVATIVE.
IF \(L=H^2\), THE SAME FACTOR IS \(L^{1/4}\).
GATE A: NOT CLOSED BY THIS SOURCE.
GATE D: TURNOVER AND RECURRENCE OPEN.
(17) NOT CLAIMED.
NS NOT SOLVED.
