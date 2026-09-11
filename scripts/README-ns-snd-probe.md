# NS / SND honest probe

Script: `scripts/ns_snd_honest_probe.py`

## What it does

Synthetic Fourier / band-limited checks that support the *toolkit* side of the
program without overclaiming:

- shell energy ratios \(\rho = J/X\) on random modes
- a toy Ring-Lemma-style inequality on random Lipschitz direction fields
- arithmetic identity \(c_* = 6/\pi^2 = \zeta(2)^{-1}\) documented as **analogy only**

## What it does **not** do

- prove Theorem H
- prove SND-U
- resolve Clay Statement (B)

See `docs/ns-review/THEOREM-H-ATTACK-PLAN.md` and the adversarial verdict.
