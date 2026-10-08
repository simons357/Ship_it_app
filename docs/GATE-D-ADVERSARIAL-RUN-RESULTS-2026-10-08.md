# Gate D — adversarial run results (numerical evidence)

8 October 2026.
**Numerical evidence only. No theorem stamp. Not (17).**

Adversary: six-box `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07`
(`verify_signed_gate.py` PASS; `Signed-Gate-Checks.json`).
**Gaussian not substituted.**

Runner: [`scripts/ns_attacks/gate_d_adversarial_run.py`](../scripts/ns_attacks/gate_d_adversarial_run.py)
JSON: [`scripts/ns_attacks/GATE-D-ADVERSARIAL-RUN.json`](../scripts/ns_attacks/GATE-D-ADVERSARIAL-RUN.json)

---

## Method (stated limitations)

- Sparse Galerkin on ball \(|k|\le 4H\); full truncated convolution among retained modes.
- Euler steps; after each step keep top \(M\) modes by \(|\hat u|^2\) (\(M=2500\) for \(n=1\), \(4000\) for \(n=2\)).
- \(\nu = \tfrac14\cdot 4\,T/(\sqrt{E}Y)=T/Y\) at \(E=1\) so \(D(0)=T-\nu Y/4>0\).
- At \(t=0\): \(T_{\mathrm{sc}}\) matches verifier to machine precision; energy identity
  \(X'=-2\nu Y+2T_{\mathrm{sc}}\) residual \(<10^{-10}\).

This is evidence under the stated truncation, not a certified continuum limit.

---

## Measured table

| \(n\) | \(H\) | \(D_H(0)\) | \(D_H'(0)\) | \(\lvert I_H\rvert\) | \(H^{5/2}\lvert I_H\rvert\) | \(B_{I_H}\) | \(\int_{I_H}UW\,dt\) | \(\int_{I_H}X\,dt\) (ruled out) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 63 | \(1.536\times10^{4}\) | \(3.711\times10^{6}\) | \(5.685\times10^{-2}\) | \(1.791\times10^{3}\) | \(0.0550\) | \(2.604\times10^{6}\) | \(2.366\times10^{3}\) |
| 2 | 126 | \(1.959\times10^{5}\) | \(2.286\times10^{8}\) | \(1.403\times10^{-2}\) | \(2.501\times10^{3}\) | \(0.0581\) | \(7.100\times10^{6}\) | \(2.372\times10^{3}\) |

Episode status: **COMPLETE_FIRST_EPISODE** at both \(n\) (downward \(D\) crossing found).

---

## Score against the three-way rubric

| Outcome | These two points |
|---|---|
| \(B_H\to 0\) | **Not seen** — \(B\approx 0.055\)–\(0.058\) |
| \(B_H=O(1)\) with \(O(1)\) globally finite resource | UW spend is **huge** (\(10^6\)–\(10^7\)), not a tight \(O(1)\) paydown on \(I_H\) alone |
| \(B_H=O(1)\) with \(o(1)\) resource | **Not observed** — \(B/\int UW \sim 10^{-8}\) |

Additional diagnostics:

- \(H^{5/2}\lvert I_H\rvert\sim 1800\)–\(2500\gg 1\): first episode lasts far longer than critical turnover \(H^{-5/2}\).
- \(\int_{I_H}X\,dt\sim 2.4\times10^{3}\) while \(B\sim 0.06\): plain energy integral is not the paying resource (already ruled out analytically at critical scaling; here the episode is longer, so \(\int X\) is even larger).
- \(U_0\not\le\nu/4\): small-\(\ell^1\) prototype ceiling does not apply to this adversary.

**Preliminary family reading (two points only):** not the dangerous cheap-recurrence case; not yet \(B\to0\). Need more \(H=63n\) before a family score. **No lemma stamp.**

---

## STATUS

PACKET INGESTED. VERIFY PASS.
GATE D ADVERSARIAL RUN: NUMERICAL EVIDENCE FILED FOR \(n=1,2\).
THEOREM STAMP: FALSE.
(17) NOT CLAIMED.
NS NOT SOLVED.
