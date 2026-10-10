# Gate D review — 9 October 2026

**Review complete. Gate D remains a valid target — not a proved lemma.
Not (17).**

Author source pack (expected; **not on disk this session**):
`scratch/ec43035008f2/Gate-D-Review-and-Separate-Gaussian-Extension-2026-10-09.zip`.

Vault pack filed from this handoff message:
[`handoff/gate-d-review-2026-10-09/`](../handoff/gate-d-review-2026-10-09/)
and `handoff/Gate-D-Review-and-Separate-Gaussian-Extension-2026-10-09.VAULT.zip`.
Merge author ZIP extras when that archive lands.

Parents:
[`GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md`](GATE-D-HALF-DERIVATIVE-ATTACK-2026-10-08.md),
[`GATE-D-TURNOVER-ADVERSARIAL-TEST-2026-10-08.md`](GATE-D-TURNOVER-ADVERSARIAL-TEST-2026-10-08.md),
[`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

---

## Verdict

| Item | Status |
|---|---|
| Gate D as program target | **Valid** |
| Resource-Weighted Turnover Lemma | **Not proved / not stamped** |
| Old source blocker (Orbit R4, episode balance, Signed-Gate bytes) | **Closed — sources recovered** |
| Large-packet resource paying for repeated episodes | **Open mathematical gap** |
| Six-box full-trajectory \(B_{I_H}/\mathcal R_{I_H}\) test | **Unrun** (execution gap) |

---

## Corrections (binding)

1. **Restore the initial boundary term.**
   If an episode starts at initial time with \(d(a)>0\), the episode cost includes
   \((b-a)\,d(a)\) in addition to the first-time-moment integral. Do not omit it.

2. **Remove claimed equivalence between duration and resource bounds.**
   A window estimate \(\lvert I\rvert\lesssim H^{-5/2}\) is **not** interchangeable
   with \(B_I\le C\mathcal R_I\) and \(\sum\mathcal R_I\) controlled. Duration match
   alone does not close recurrence.

3. **Test the ratio \(B_I/\mathcal R_I\), not merely “\(O(1)\) versus \(o(1)\).”**
   Score the family by the measured ratio and whether \(\sum\mathcal R_I\) stays
   globally finite. Coarse \(O(1)/o(1)\) slogans are insufficient.

---

## Mathematical gap

No large-packet (Gate-C / six-box scale) resource has yet been shown to pay for
**repeated** episodes. The small-\(\ell^1\) Orbit-R4 prototype
\(\int UW\,dt\le U_0^2/(2(\nu-U_0))\) remains restricted-class only.

---

## Execution gap

The six-box **full-trajectory** test remains unrun. A straightforward dense
Galerkin implementation exceeds this session’s memory.

Prior static sweep / truncated-mode experiments are **not** substitutes for that
full-trajectory signed-scalene diagnostic.

**Next Gate D task:** a feasible full-trajectory solver that preserves the exact
signed-scalene diagnostic (six-box adversary, no Gaussian substitute) —
[`GATE-D-FULL-TRAJECTORY-SOLVER-2026-10-09.md`](GATE-D-FULL-TRAJECTORY-SOLVER-2026-10-09.md),
[`scripts/ns_attacks/gate_d_full_trajectory.py`](../scripts/ns_attacks/gate_d_full_trajectory.py).

---

## Separate Gaussian experiment (through \(s=4\))

Filed separately: [`GATE-D-GAUSSIAN-EXTENSION-2026-10-09.md`](GATE-D-GAUSSIAN-EXTENSION-2026-10-09.md).

Neither resolution met the second-handoff test. Fine-scale activity grew, but
mixed interactions dominated. Outcome: **unresolved at the declared horizon** —
not evidence that regeneration is impossible.

---

## STATUS

GATE D: VALID TARGET; LEMMA NOT STAMPED.
SOURCE BLOCKER: CLOSED.
MATH GAP: LARGE-PACKET RECURRENCE RESOURCE.
EXECUTION GAP: FULL-TRAJECTORY SIX-BOX SOLVER.
(17) NOT CLAIMED.
NS NOT SOLVED.
