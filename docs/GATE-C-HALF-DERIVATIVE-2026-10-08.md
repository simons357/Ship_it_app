# Gate C — exact missing exponent

8 October 2026. Notation fixed 9 October 2026 from the sharp-band source.
**CLOSED for the audited assembly’s \(\tfrac12\)-derivative deficit. Not (17).**

\(\Lambda\sim H\) explicitly denotes frequency. In the sharp-band source, that
frequency is wavenumber: fields supported in \(H\le|k|\le 4H\). The deficit
is \(\Lambda^{1/2}\sim H^{1/2}\). If squared frequency is \(L=H^2\), the same
factor is \(L^{1/4}\).

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
Write \(\Lambda\) for this same frequency, so \(\Lambda\sim H\) and the deficit
is \(\Lambda^{1/2}\sim H^{1/2}\): one half derivative. If squared frequency
is denoted by \(L=H^2\), the same factor is \(L^{1/4}\).

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

CLOSED applies to this audited assembly: the sharp instantaneous signed
band estimate. It does not prove (17). Gate D’s episode bound and summable
recurrence resource both remain required, uniformly in the cutoff.

---

## What this is / is not

| Claim | Status |
|---|---|
| Audited assembly (sharp signed band) | **CLOSED** — deficit \(\Lambda^{1/2}\sim H^{1/2}\) (\(\Lambda\sim H\) = frequency) |
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

Next test: a completed, corrected episode followed through regeneration,
measuring both \(B_I/\mathcal R_I\) and cumulative resource use. A
successful finite run would support the target, not prove the uniform bound.

Out of scope as substitutes: shell-count; Young; generic instantaneous
phase; Ring without bridge; swirl-as-substitute; B41→NSE; random-phase.

Setup corrections on the solver do not validate this contract.
Status: implementation corrected; dynamical evidence pending.

---

## STATUS

GATE C: CLOSED FOR THE AUDITED ASSEMBLY — DEFICIT \(\Lambda^{1/2}\sim H^{1/2}\)
(\(\Lambda\sim H\) = FREQUENCY / WAVENUMBER).
IF \(L=H^2\), THE SAME FACTOR IS \(L^{1/4}\).
GATE A: NOT CLOSED BY THIS SOURCE.
GATE D: OPEN — EPISODE BOUND AND SUMMABLE RESOURCE BOTH REQUIRED,
UNIFORM IN CUTOFF. A FINITE RUN DOES NOT PROVE THAT BOUND.
(17) NOT CLAIMED.
NS NOT SOLVED.
