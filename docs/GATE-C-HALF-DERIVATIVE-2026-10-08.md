# Gate C — exact missing exponent

8 October 2026. Notation fixed 9 October 2026 from the sharp-band source.
**CLOSED for the sharp instantaneous signed band estimate. Optimal wavenumber exponent \(1/2\). Gate A is not a premise. (17) is not established.**

The sharp-band source is the reference. \(H\) is the wavenumber, on the band
\(H\le|k|\le 4H\). The optimal exponent is \(H^{1/2}\). Where \(\Lambda\)
appears, it is defined there by \(\Lambda\sim H\), so \(\Lambda^{1/2}\) is
the same factor. If squared frequency is \(L=H^2\), the factor is \(L^{1/4}\).

Source:
[`sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt`](sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt).

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

Gate A remains unresolved and is not a premise.

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
The deficit is \(H^{1/2}\): one half derivative in wavenumber. Where
\(\Lambda\) is written, \(\Lambda\sim H\), so \(\Lambda^{1/2}=H^{1/2}\). If
squared frequency is \(L=H^2\), the same factor is \(L^{1/4}\).

---

## RESULT

\[
\boxed{H^{1/2}}
\]

\[
\boxed{\text{We need a dynamical mechanism worth one half derivative.}}
\]

The normalization is the key. \(1/2\) is the sharp uniform exponent for
this signed static ratio. It does not settle the unsigned \(Q_x\) exponent
(\(\tfrac12\le\theta_Q\le 2\) in the source) or a time budget along one
fixed solution. The uploaded nonnegative assembly defines a separate
quotient \(R_H=\lVert Q\rVert_2/Y\) with the same unresolved interval, and
must be compared with that definition before its verdict is imported.

---

## Scope of CLOSED

The signed static test is complete. Dynamical control is open.

CLOSED applies to the sharp instantaneous signed band estimate, whose
optimal wavenumber exponent is \(1/2\). Gate A remains unresolved and is
not a premise. (17) is not established.

The remaining dynamical target, with \(h_{K,N}=P_{>K}u_N\), is
\[
\mathcal S_{K,N}(T)
=
\int_0^T
\frac{\bigl(\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr)_+}{X_N}\,dt.
\]
The denominator is \(X_N\). There is no extra \(Y_N\) factor. \(Y_N\) appears
only inside the positive-part threshold.

The six-box test must measure how long the positive episode lasts and what
resource pays for its accumulated budget. Completing one episode would
provide evidence. Cutoff-uniform control and summable recurrence would
still require proof.

---

## What this is / is not

| Claim | Status |
|---|---|
| Signed static ratio \(R(H)\) | **Complete** — sharp uniform exponent \(1/2\) |
| Nonnegative \(Q\) quotient \(R_H=\lVert Q\rVert_2/Y\) | **Not this test** — \(1/2\le\theta\le 2\), optimum unresolved ([`sources/GATE-B-UPLOADED-SOURCES-2026-10-09.md`](sources/GATE-B-UPLOADED-SOURCES-2026-10-09.md)) |
| Unsigned \(Q_x\) exponent, or a time budget on one solution | **Not settled** |
| Same factor if \(L=H^2\) | \(L^{1/4}\) (and \(\Lambda^{1/2}\) only where \(\Lambda\sim H\)) |
| Gate A | **Unresolved** — not a premise |
| (17) | **Not established** |
| Dynamical control of \(\mathcal S_{K,N}\) | **Open** — denominator \(X_N\), no extra \(Y_N\) |
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
completed finite episode can support Gate D, but cannot establish
cutoff-uniform control or summable recurrence.

Out of scope as substitutes: shell-count; Young; generic instantaneous
phase; Ring without bridge; swirl-as-substitute; B41→NSE; random-phase.

Setup corrections on the solver do not validate this contract.
Status: implementation corrected; dynamical evidence pending.

---

## STATUS

SIGNED STATIC TEST: COMPLETE. DYNAMICAL CONTROL: OPEN.
GATE C: CLOSED FOR THE SHARP INSTANTANEOUS SIGNED BAND ESTIMATE.
OPTIMAL WAVENUMBER EXPONENT \(H^{1/2}\). WHERE \(\Lambda\) APPEARS, \(\Lambda\sim H\).
IF \(L=H^2\), THE SAME FACTOR IS \(L^{1/4}\).
GATE A: UNRESOLVED — NOT A PREMISE.
GATE D: OPEN ON EPISODE CONTROL AND RECURRENCE FUNDING.
A FINITE EPISODE CAN SUPPORT GATE D AND CANNOT ESTABLISH CUTOFF-UNIFORM
CONTROL OR SUMMABLE RECURRENCE.
(17) NOT ESTABLISHED.
NS NOT SOLVED.
