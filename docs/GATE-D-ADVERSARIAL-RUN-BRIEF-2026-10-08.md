# Gate D — executable adversarial run brief

8 October 2026.
**Operational brief. Lemma recorded, not stamped. Not (17).**

Parents:
[`GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md`](GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md),
[`GATE-D-EXECUTION-BLOCKER-2026-10-08.md`](GATE-D-EXECUTION-BLOCKER-2026-10-08.md).

Sources:
- [`sources/NS_ORBIT_R4_SMALL_DATA_2026-09-20.md`](sources/NS_ORBIT_R4_SMALL_DATA_2026-09-20.md)
- [`sources/NS_EPISODE_BALANCE_NOTE_2026-09-20.md`](sources/NS_EPISODE_BALANCE_NOTE_2026-09-20.md)
- [`sources/Signed-Gate-B-Sharp-Band-Exponent-POINTER-2026-10-07.md`](sources/Signed-Gate-B-Sharp-Band-Exponent-POINTER-2026-10-07.md)

---

## Target (unchanged)

\[
\boxed{\textbf{Resource-Weighted Turnover Lemma}}
\]
\[
B_I\le C\,\mathcal R_I,
\qquad
\sum_I\mathcal R_I
\le C(u_0,\nu,K,T).
\]

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
> \(E=1\), evolve the full Galerkin system, and compute \(D_H(0)\),
> \(D_H'(0)\), the first positive episode \(I_H\), its cost
> \[
> B_{I_H}=\int_{I_H}\frac{D_H}{X_H}\,dt,
> \]
> and candidate resource spends. Test increasing \(H=63n\).
> **Do not substitute the Gaussian packet.**

---

## Score outcomes

| Outcome | Reading |
|---|---|
| \(B_H\to 0\) | Extra dynamical gain — excellent |
| \(B_H=O(1)\) with \(O(1)\) spend of a globally finite resource | OK — recurrence paid |
| \(B_H=O(1)\) while resource spend is \(o(1)\) | **Dangerous — damages Gate D** (recurrence too cheap) |

Also record \(H^{5/2}\lvert I_H\rvert\) as a diagnostic against critical
turnover scaling.

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

---

## Episode identity (measurement)

\[
B_I=\int_I\frac{D}{X}\,dt
=
\int_a^b(b-s)
\left[
\frac{Q_\Sigma}{X}+\frac{V}{X}+\frac{M}{X}-\frac{DX'}{X^2}
\right]ds.
\]

---

## Unlock checklist

| Item | Status in this vault |
|---|---|
| Orbit R4 prototype identities | **Filed** (author paste excerpt) |
| Episode balance identity | **Filed** (author paste excerpt) |
| Adversary named (six-box Signed-Gate) | **Named** |
| `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt` bytes | **Pending drop** |
| `verify_signed_gate.py` / `Signed-Gate-Checks.json` | **Pending drop** |
| Galerkin evolution + \(B_{I_H}\)/resource score | **Blocked on packet bytes** |

Conceptual blocker: **cleared**.
Operational blocker: **packet binary ingest** for the evolution run.

---

## STATUS

GATE D: OPERATIONAL BRIEF READY.
LEMMA: RECORDED, NOT STAMPED.
NEXT JOB: GET SIX-BOX GATE-C PACKET THROUGH EPISODE/RESOURCE MEASUREMENT.
(17) NOT CLAIMED.
NS NOT SOLVED.
