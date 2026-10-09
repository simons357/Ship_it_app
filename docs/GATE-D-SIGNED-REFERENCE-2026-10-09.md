# Gate D signed-scalene reference

9 October 2026.
**Small-field reference for the 7 October ordered-convolution cut. Not the 20 September original. Not wired into the stepper. Gate D remains open and blocked.**

Files: `scripts/ns_attacks/gate_d_signed_diagnostic/`.
Archive SHA-256: `e0fca0efb942a5be1cdc60159faae4fdfb456754896aca5705369cbe46a81ba9`.
The packaged checksums of `signed_scalene.py` and `gaussian_gate_d.py` match.

`signed_scalene.py` evaluates \(-\operatorname{Re}\langle P(v\cdot\nabla v),-\Delta v\rangle\) and drops any interaction whose three squared Fourier radii are not distinct. An optional cutoff can require all three legs to satisfy \(|k|>\mathrm{cutoff}\). It uses physical wavenumbers \(2\pi k/L\) and the physical volume \(L^3\). The 7 October note uses the normalized torus. Those two normalizations agree in the test, where \(L=2\pi\). They are not the same convention in general. The 20 September cutoff and normalization are still unchecked.

The evaluator is not called by the time stepper. The included driver still leaves \(T_{\mathrm{sc}}\) and \(D\) null. It does set the production probe \(G=T-Y/c\). The locked \(G\) unit test was not rerun.

The new checks were rerun here and passed:

- a one-shell field gives signed-scalene transfer \(0\);
- one exact three-radius triad, on which every interaction is scalene, matches the pseudospectral full production to 8 places.

That second check does not test a field that also contains repeated-radius interactions. It does not verify arbitrary scalene filtering, continuum \(\mathbb R^3\) convergence, or the six-box packet. No turnover, regeneration, or cutoff-independent budget is claimed. The frozen experiment has not been launched.

`signed_scalene.py` remains this 7 October reference. It is not a certified substitute for the 20 September \(\Phi_{abc}\). The Gaussian stepper stays disconnected until that formula is ported, the six-mode identity \(T_{\mathrm{sc}}=4m^3 A^3\) is tested, and an independent ordered convolution agrees ([`GATE-D-SIGNED-DIAGNOSTIC-2026-10-09.md`](GATE-D-SIGNED-DIAGNOSTIC-2026-10-09.md)).

## STATUS

REFERENCE EVALUATOR: 7 OCTOBER CUT, SMALL FIELD. NOT THE 20 SEPTEMBER ORIGINAL.
PHYSICAL \(2\pi/L\) NORMALIZATION: NOT RECONCILED WITH THE NORMALIZED TORUS EXCEPT AT \(L=2\pi\).
NOT WIRED INTO THE STEPPER. \(T_{\mathrm{sc}}\) AND \(D\) IN THE DRIVER: NULL.
ONE-SHELL AND ALL-SCALENE TRIAD CHECKS: PASSED HERE.
\(G\) UNIT TEST: NOT RERUN.
GATE D: OPEN AND BLOCKED.
NS NOT SOLVED.
