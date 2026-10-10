# Connected signed-scalene driver

9 October 2026.
**Engineering checks passed on the packaged witness. The Lemma 19 coefficient audit is not certified. The frozen \(c=200\) experiment was not launched. Gate D remains OPEN / BLOCKED.**

Code: `scripts/ns_attacks/gate_d_connected/`.
The driver imports `step` from `scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py` and \(\Phi_{abc}\) from `scripts/ns_attacks/gate_d_phi_reference/signed_phi.py`. Neither file was edited.

| file | SHA-256 |
| --- | --- |
| `gaussian_gate_d.py` | `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56` |
| `signed_phi.py` | `3b81829ef1a0a961c747204554e6753f4d907f358151fc5357e2d1cd366e41df` |
| `driver.py` | `4c93391e2a8ce588596d53fd4e408320954d21030447bbbfa3b84c4c998d60a4` |

## Cutoff convention

\(\Phi_{abc}\) sums integer radii with \(K^2<a<b<c\le N^2\), \(a=|k|^2\), \(k\in\mathbb Z^3\). Coefficients extracted from a driver FFT are \(\hat u(k)=\widehat u(k)/n^3\).

The physical wavenumber \(2\pi|k|/L\) is stored next to that cut and is not inserted into \(\Phi_{abc}\). On the \(+32\) witness, \((K,N)=(1,5)\):

| box | physical wavenumber at \(K\) | physical wavenumber at \(N\) |
| --- | --- | --- |
| \(L=2\pi\) | \(1\) | \(5\) |
| \(2L=4\pi\) | \(1/2\) | \(5/2\) |

\(T_{\mathrm{sc}}\) is the same number on both boxes. The physical band is not. DA resolves the \(L\) versus \(2L\) comparison before approving the experiment.

\(D=T_{\mathrm{sc}}-\nu Y/4\) uses \(\nu=1/c\) and the integer-lattice moment \(Y=\sum|k|^4|\hat u|^2\). The driver’s physical \(X\), \(Y\), and \(G=T-Y/c\) are a different convention and are not added into this \(D\).

## Five checks

`python3 -m unittest -v test_connected` passed.

1. For \(m=1,2,3\) and \(A=1,2\), the connected \(T_{\mathrm{sc}}\) equals \(4m^3 A^3\).
2. The independent ordered convolution equals those same values.
3. On the \(m=2\), \(A=1\) witness, \(K=2\) gives \(0\).
4. On that witness, \(N=4\) gives \(0\).
5. On that witness, \(K=1\), \(N=5\) gives \(+32\), and the ordered convolution also gives \(+32\).

The unit test also advances the packed witness by one stepper call of size \(10^{-6}\). That call is not the frozen Gaussian experiment.

## What remains open

The original Lemma 19 coefficients are still required to reproduce \(+4m^3 A^3\) under \(T=-\operatorname{Re}\langle B,-\Delta h\rangle\). One polarization’s ordered convolution is \(-4m^3 A^3\). That negative value is not a pass. Polarization, Fourier sign, or an implementation error remains unresolved.

The locked \(G\) unit test was not rerun. No turnover, regeneration, or cutoff-independent budget is claimed.

## STATUS

FIVE ENGINEERING CHECKS: PASSED, INCLUDING \(+32\) AND THE ORDERED CONVOLUTION.
LEMMA 19 ORIGINAL COEFFICIENTS: NOT CERTIFIED. SIGN GAP UNRESOLVED.
STEPPER FILE: UNCHANGED.
\(L\) VERSUS \(2L\): DOCUMENTED, NOT RESOLVED. DA BEFORE EXPERIMENT APPROVAL.
FROZEN \(c=200\) EXPERIMENT: NOT LAUNCHED.
\(G\) UNIT TEST: NOT RERUN.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
