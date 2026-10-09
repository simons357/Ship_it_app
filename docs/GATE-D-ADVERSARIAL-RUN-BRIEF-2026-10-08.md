# Gate D — executable adversarial run brief

8 October 2026 (corrections from 9 Oct review).
**Operational brief. Target recorded, not stamped. Not (17).**

Parents:
[`GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md`](GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md),
[`GATE-D-EXECUTION-BLOCKER-2026-10-08.md`](GATE-D-EXECUTION-BLOCKER-2026-10-08.md),
[`GATE-D-REVIEW-2026-10-09.md`](GATE-D-REVIEW-2026-10-09.md).

Sources:
- [`sources/NS_ORBIT_R4_SMALL_DATA_2026-09-20.md`](sources/NS_ORBIT_R4_SMALL_DATA_2026-09-20.md)
- [`sources/NS_EPISODE_BALANCE_NOTE_2026-09-20.md`](sources/NS_EPISODE_BALANCE_NOTE_2026-09-20.md)
- [`sources/Signed-Gate-B-Sharp-Band-Exponent-POINTER-2026-10-07.md`](sources/Signed-Gate-B-Sharp-Band-Exponent-POINTER-2026-10-07.md)

---

## Target (unchanged as program goal; not proved)

\[
\boxed{\textbf{Resource-Weighted Turnover Lemma}}
\]
\[
B_I=\int_I d(t)\,dt\le C\mathcal R_I,
\qquad
\sum_I\mathcal R_I\le C_{\mathrm{data},\nu,T},
\]
constants uniform in the Galerkin cutoff. Fast turnover does not replace
the second obligation.

Stack:
\[
\text{static deficit}
\to H^{1/2}
\to
\text{critical turnover }H^{-5/2}
\to
\textbf{find the resource that pays for recurrence}.
\]

---

## Brief to the NS agent

> **Gate D adversarial run:** use the six-box Gate-C packet
> (`Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt` +
> `verify_signed_gate.py` / `Signed-Gate-Checks.json`), normalize to
> \(E=1\), evolve the **full** Galerkin trajectory (no top-\(M\)
> substitute; no Gaussian substitute), and compute \(D_H(0)\),
> \(D_H'(0)\), the first positive episode \(I_H\), its cost
> \[
> B_{I_H}=\int_{I_H}\frac{D_H}{X_H}\,dt
> \]
> **plus** \((b-a)d(a)\) when the episode starts with \(d(a)>0\),
> and the ratio \(B_{I_H}/\mathcal R_{I_H}\). Test increasing \(H=63n\).

---

## Score outcomes

Score the measured ratio \(B_{I_H}/\mathcal R_{I_H}\) and global
summability of \(\mathcal R\). Do not rely on coarse \(O(1)/o(1)\) alone.

| Outcome | Reading |
|---|---|
| \(B_H\to 0\) | Extra dynamical gain — excellent |
| \(B_H/\mathcal R_H\) bounded with \(\sum\mathcal R<\infty\) | OK — recurrence paid |
| \(B_H\) order-one while resource spend collapses too fast for a global sum | **Dangerous — damages Gate D** |

Also record \(H^{5/2}\lvert I_H\rvert\) as a **duration diagnostic only**
(duration ≢ resource).

---

## Already ruled out as recurrence resource

**Plain energy dissipation is not enough** at critical turnover scaling.
If \(X\sim H^2\) and \(\lvert I_H\rvert\sim H^{-5/2}\), then
\[
\int_{I_H}X\,dt\sim H^{-1/2},
\]
while \(B_H\) could remain \(O(1)\). The resource must carry **stronger
information** than ordinary energy loss.

Prototype that *does* work on a restricted class (Orbit R4 small-data):
\[
\mathcal R\sim\int UW\,dt,
\qquad
\int_0^T UW\,dt
\le
\frac{U_0^2}{2(\nu-U_0)}.
\]
Large-packet repetition resource: **open mathematical gap**.

---

## Episode identity (measurement)

\[
B_I=\int_I\frac{D}{X}\,dt.
\]
First-moment form (when \(D(a)=0\)):
\[
B_I
=
\int_a^b(b-s)
\left[
\frac{Q_\Sigma}{X}+\frac{V}{X}+\frac{M}{X}-\frac{DX'}{X^2}
\right]ds.
\]
**If \(d(a)>0\) at initial time, add \((b-a)d(a)\).**

---

## Unlock checklist

| Item | Status in this vault |
|---|---|
| Orbit R4 prototype identities | **Filed** |
| Episode balance identity | **Filed** (boundary term restored in protocol) |
| Adversary (six-box Signed-Gate) | **Ingested** |
| `verify_signed_gate.py` / `Signed-Gate-Checks.json` | **PASS** |
| Static author sweep | **Filed** (not episode cost) |
| Prior top-\(M\) evolution | **Demoted** — not full-trajectory |
| Full-trajectory \(B_{I_H}/\mathcal R_{I_H}\) | **Unrun** — next solver task |

---

## STATUS

GATE D: VALID TARGET; LEMMA NOT STAMPED.
SOURCE BLOCKER: CLOSED.
FULL-TRAJECTORY TEST: UNRUN.
NEXT: FEASIBLE SOLVER PRESERVING SIGNED-SCALENE DIAGNOSTIC.
(17) NOT CLAIMED.
NS NOT SOLVED.
