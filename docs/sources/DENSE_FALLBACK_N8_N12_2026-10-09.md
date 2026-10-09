# Gate D adaptive dense fallback benchmark — 9 October 2026

Executed `OPENBLAS_NUM_THREADS=1 python benchmark_dense_next.py N` in the supplied adaptive evaluator tree. New dense random Hermitian-symmetrized, Leray-projected Fourier fields with spherical cutoff N; fixed L=2π. Unnormalized FFT coefficient amplitudes scaled by n^-3. Measurements are single runs, not stabilized repetitions.

| N | n | shells | occupied modes | method | runtime seconds | max RSS KiB |
|---:|---:|---:|---:|---|---:|---:|
| 8 | 27 | 54 | 2108 | fft_shell | 0.503384 | 116456 |
| 10 | 33 | 85 | 4168 | fft_shell | 1.645837 | 132736 |
| 12 | 39 | 121 | 7152 | fft_shell | 4.395173 | 156560 |

These runs establish execution and rough scaling only. No independent reference comparisons were made at N=8–12, no forward floating-point error bound, no hard peak-memory cap, no N=128/160 performance claim. The very small transfer values in these test fields are not representative of the coherent Gaussian packet. The current fallback loops over all occupied squared-radius shells and is unlikely to be practical at large N without algorithmic redesign. No production c=200 trajectory was launched. Physical cutoff matching and R3 domain convergence remain unresolved. Gate D OPEN / BLOCKED.
