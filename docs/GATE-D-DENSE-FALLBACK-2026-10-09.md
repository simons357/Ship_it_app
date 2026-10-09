# Dense fallback, \(N=8\) to \(N=12\)

9 October 2026.
**Reported single runs. Not rerun here. Not a production result. Gate D remains OPEN / BLOCKED.**

Source: [`sources/DENSE_FALLBACK_N8_N12_2026-10-09.md`](sources/DENSE_FALLBACK_N8_N12_2026-10-09.md).
SHA-256: `9c0d7c325423e2bf089966f14144119dce9d78bae3c23a1badf141e2a5ad3200`.

The note reports one FFT-shell run at each of \(N=8,10,12\), on dense random fields at \(L=2\pi\):

| \(N\) | \(n\) | shells | occupied modes | seconds | max RSS KiB |
| --- | --- | --- | --- | --- | --- |
| 8 | 27 | 54 | 2108 | 0.503384 | 116456 |
| 10 | 33 | 85 | 4168 | 1.645837 | 132736 |
| 12 | 39 | 121 | 7152 | 4.395173 | 156560 |

`benchmark_dense_next.py` is not in this checkout, so these timings were not rerun. The note limits them to execution and rough scaling. It records no reference comparison at these sizes, no forward-error bound, no \(N=128/160\) claim, and no \(c=200\) trajectory. Physical cutoff matching and \(\mathbb R^3\) convergence remain unresolved. The locked stepper file was not edited. The locked \(G\) unit test was not rerun.

## STATUS

NOTE: FILED. TIMINGS NOT RERUN.
SCRIPT `benchmark_dense_next.py`: NOT IN THIS CHECKOUT.
SCOPE: EXECUTION AND ROUGH SCALING ONLY.
FROZEN \(c=200\) TRAJECTORY: NOT RUN.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
