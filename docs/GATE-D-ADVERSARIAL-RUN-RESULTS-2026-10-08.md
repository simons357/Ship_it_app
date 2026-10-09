# Gate D — adversarial run results (demoted — not full-trajectory)

8 October 2026; **demoted by 9 Oct review**.
**Not full-trajectory evidence. No theorem stamp. Not (17).**

Adversary: six-box `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07`
(`verify_signed_gate.py` PASS; `Signed-Gate-Checks.json`).
**Gaussian not substituted.**

Runner: [`scripts/ns_attacks/gate_d_adversarial_run.py`](../scripts/ns_attacks/gate_d_adversarial_run.py)
JSON: [`scripts/ns_attacks/GATE-D-ADVERSARIAL-RUN.json`](../scripts/ns_attacks/GATE-D-ADVERSARIAL-RUN.json)

Review: [`GATE-D-REVIEW-2026-10-09.md`](GATE-D-REVIEW-2026-10-09.md).

---

## Why this is demoted

Method used **top-\(M\) Euler** after each step (keep largest \(M\) modes by
\(|\hat u|^2\)). That is **not** the six-box full-trajectory test required
by Gate D. A straightforward dense Galerkin path OOMs; the execution gap
remains open.

Do **not** cite these rows as complete-episode evidence for the
Resource-Weighted Turnover Lemma.

---

## Method (stated limitations — historical)

- Sparse Galerkin on ball \(|k|\le 4H\); truncated convolution among retained modes.
- Euler steps; after each step keep top \(M\) modes by \(|\hat u|^2\) (\(M=2500\) for \(n=1\), \(4000\) for \(n=2\)).
- \(\nu = \tfrac14\cdot 4\,T/(\sqrt{E}Y)=T/Y\) at \(E=1\) so \(D(0)=T-\nu Y/4>0\).
- At \(t=0\): \(T_{\mathrm{sc}}\) matches verifier to machine precision; energy identity
  \(X'=-2\nu Y+2T_{\mathrm{sc}}\) residual \(<10^{-10}\).
- **Missing (9 Oct):** initial boundary term \((b-a)d(a)\) was not scored;
  pass/fail used coarse \(O(1)/o(1)\) language rather than \(B_I/\mathcal R_I\).

---

## Measured table (historical / truncated-mode only)

| \(n\) | \(H\) | \(D_H(0)\) | \(D_H'(0)\) | \(\lvert I_H\rvert\) | \(H^{5/2}\lvert I_H\rvert\) | \(B_{I_H}\) (no boundary term) | \(\int_{I_H}UW\,dt\) | \(\int_{I_H}X\,dt\) (ruled out) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 63 | \(1.536\times10^{4}\) | \(3.711\times10^{6}\) | \(5.685\times10^{-2}\) | \(1.791\times10^{3}\) | \(0.0550\) | \(2.604\times10^{6}\) | \(2.366\times10^{3}\) |
| 2 | 126 | \(1.959\times10^{5}\) | \(2.286\times10^{8}\) | \(1.403\times10^{-2}\) | \(2.501\times10^{3}\) | \(0.0581\) | \(7.100\times10^{6}\) | \(2.372\times10^{3}\) |

Episode status in the runner JSON said `COMPLETE_FIRST_EPISODE` — **retract
as Gate D evidence**. Truncated-mode downward \(D\) crossing ≠ certified
full-trajectory episode.

---

## What remains usable

- Packet ingest + `verify_signed_gate` PASS.
- Static \(t=0\) moments and energy-identity check on the signed packet.
- Author static sweep exponents (separate): \(X\sim H^{2.00}\), \(D\sim H^{3.77}\),
  \(D/X\sim H^{1.77}\), \(\tau_{\mathrm{local}}\sim H^{-2.31}\) at cutoff \(8H\).

---

## STATUS

PRIOR TOP-\(M\) EPISODE CLAIMS: DEMOTED.
FULL-TRAJECTORY SIX-BOX \(B_I/\mathcal R_I\): UNRUN.
THEOREM STAMP: FALSE.
(17) NOT CLAIMED.
NS NOT SOLVED.
