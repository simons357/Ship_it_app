"""Archive-only Track C toys (25 August 2026 queued pastes).

Not live Domain Architect. Do not import into domain_architect/.
Not A_3 / Track A. Not Paper2 SND. Not Ring J/X. Clay is NOT CLAIMED.

qc_coherence is a normalized-vector overlap (fidelity-like), not vorticity
alignment with e_max. qr_resonance is a Welch peak-power fraction, not
enstrophy production. Forbidden in live domain_architect/*.py.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import welch


def qc_coherence(state, reference=None):
    """Q_c toy: alignment-as-fidelity. Archive only."""
    state = np.asarray(state, dtype=float)
    state = state / (np.linalg.norm(state) + 1e-10)
    if reference is None:
        reference = np.ones_like(state) / len(state)
    else:
        reference = np.asarray(reference, dtype=float)
        reference /= np.linalg.norm(reference) + 1e-10
    fidelity = np.abs(np.dot(state, reference)) ** 2
    return float(fidelity)


def qr_resonance(timeseries, fs=1.0):
    """Q_r toy: dominant Welch-mode fraction. Archive only."""
    ts = np.asarray(timeseries, dtype=float)
    _freqs, psd = welch(ts, fs=fs, nperseg=min(256, len(ts)))
    if len(psd) == 0:
        return 0.0
    total_power = np.sum(psd)
    peak_power = np.max(psd)
    return float(peak_power / (total_power + 1e-10))
