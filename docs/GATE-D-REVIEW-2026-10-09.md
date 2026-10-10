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

The six-box **full-trajectory** episode remains unrun.

Reported measurement module
([`GATE-D-SIGNED-MEASUREMENT-MODULE-2026-10-09.md`](GATE-D-SIGNED-MEASUREMENT-MODULE-2026-10-09.md)):
reproduces the six-box initial calculations, retains generated-mode
contributions and the initial boundary term, and passes a separate 80-mode
trajectory check. That is a tested reference for the large solver. It is
not the episode. The named zip is not on this mount.

Prior static sweep / truncated-mode experiments are **not** substitutes for that
full-trajectory signed-scalene diagnostic.

**Next Gate D task:** a feasible full-trajectory solver that preserves the exact
signed-scalene diagnostic (six-box adversary, no Gaussian substitute) —
[`GATE-D-FULL-TRAJECTORY-SOLVER-2026-10-09.md`](GATE-D-FULL-TRAJECTORY-SOLVER-2026-10-09.md),
[`GATE-D-FFT-CORRECTIONS-2026-10-09.md`](GATE-D-FFT-CORRECTIONS-2026-10-09.md).

FFT path must: (i) score \(B_I=\int d\,dt\) without double-counting
\((b-a)d(a)\); (ii) Orszag-dealias (\(N\ge 3k_{\max}\), ⇒ 768 at \(4H\));
(iii) use fixed \(K\) and full \(X,Y\). Prior \(N=512\) partials are not evidence.

Those three corrections fix the stated setup errors. They do not validate
Gate D. Partial runs stay provisional.

**Next test:** a completed, corrected episode followed through
regeneration, measuring both \(B_I/\mathcal R_I\) and cumulative resource
use. Fast turnover alone cannot settle recurrence. The resource must pay
for repeated episodes without reusing the same budget. A completed finite
episode can support Gate D, but cannot establish cutoff-uniform control
or summable recurrence.
FFT setup is corrected as reported; partial runs remain provisional.

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
MATH GAP: LARGE-PACKET RECURRENCE RESOURCE (NO BUDGET REUSE).
SETUP: IMPLEMENTATION CORRECTED; DYNAMICAL EVIDENCE PENDING.
MEASUREMENT MODULE: TESTED REFERENCE (SIX-BOX INITIALS, GENERATED MODES,
INITIAL BOUNDARY TERM, 80-MODE CHECK). FULL SIX-BOX EPISODE: UNRUN.
THIRD-TRANSFER PACKET: BEGINNING ONLY (CONSISTENCY REVIEW, NOT A RERUN).
NEXT TEST: SIX-BOX SIGNED-SCALENE EPISODE — TURNOVER AND RESOURCE.
(17) NOT CLAIMED.
NS NOT SOLVED.
