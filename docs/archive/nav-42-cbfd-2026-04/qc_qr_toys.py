"""Archive-only Track C toys (25 August 2026 queued pastes).

Not live Domain Architect. Do not import into domain_architect/.
Not A_3 / Track A. Not Paper2 SND. Not Ring J/X. Clay is NOT CLAIMED.

qc_coherence is a normalized-vector overlap (fidelity-like), not vorticity
alignment with e_max. qr_resonance is a Welch peak-power fraction, not
enstrophy production. Forbidden in live domain_architect/*.py.

Paste 2 (25 Aug 2026) is the same two functions plus unused imports
`scipy.stats.entropy` and `scipy.signal.correlate` (never called) and a
`__main__` demo on `[0.8, 0.1, 0.05, 0.05]`. Those unused imports are
**not** copied here. Paste 3 (this message) is the same as paste 1; not re-filed.
"""

from __future__ import annotations

import numpy as np

try:
    from scipy.signal import welch
except ImportError:  # this VM has numpy; scipy is optional
    welch = None


def qc_coherence(state, reference=None):
    """Q_c toy: alignment-as-fidelity. Archive only."""
    state = np.asarray(state, dtype=float)
    state = state / (np.linalg.norm(state) + 1e-10)
    if reference is None:
        # Paste default: L1-uniform, not L2-normalized (unlike `state`).
        reference = np.ones_like(state) / len(state)
    else:
        reference = np.asarray(reference, dtype=float)
        reference /= np.linalg.norm(reference) + 1e-10
    fidelity = np.abs(np.dot(state, reference)) ** 2
    return float(fidelity)


def qr_resonance(timeseries, fs=1.0):
    """Q_r toy: dominant Welch-mode fraction. Archive only."""
    if welch is None:
        raise RuntimeError("scipy is not installed; qr_resonance skipped")
    ts = np.asarray(timeseries, dtype=float)
    _freqs, psd = welch(ts, fs=fs, nperseg=min(256, len(ts)))
    if len(psd) == 0:
        return 0.0
    total_power = np.sum(psd)
    peak_power = np.max(psd)
    return float(peak_power / (total_power + 1e-10))


if __name__ == "__main__":
    state = np.array([0.8, 0.1, 0.05, 0.05])
    print("Q_c (coherence):", qc_coherence(state))
    if welch is None:
        print("Q_r (resonance): skipped (scipy not installed)")
    else:
        t = np.linspace(0, 10, 1000)
        signal = np.sin(2 * np.pi * 5 * t)
        print("Q_r (resonance):", qr_resonance(signal))
