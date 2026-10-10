#!/usr/bin/env python3
"""Connect the September 20 signed-scalene evaluator to the Gaussian driver.

The Navier–Stokes stepper is imported and not modified. This module does not
launch the frozen c=200 production experiment.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

NS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(NS / 'gate_d_signed_diagnostic'))
sys.path.insert(0, str(NS / 'gate_d_phi_reference'))

import gaussian_gate_d as gauss  # noqa: E402
from signed_phi import ordered_transfer, phi_scalene, witness  # noqa: E402

STEPPER_PATH = NS / 'gate_d_signed_diagnostic' / 'gaussian_gate_d.py'
PHI_PATH = NS / 'gate_d_phi_reference' / 'signed_phi.py'

# Integer-radius cut used by the +32 witness check. Not a physical wavenumber.
WITNESS_K = 1
WITNESS_N = 5
WITNESS_M = 2
WITNESS_A = 1
WITNESS_VALUE = 32


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_hashes():
    return {
        'stepper_sha256': sha256(STEPPER_PATH),
        'phi_sha256': sha256(PHI_PATH),
        'driver_sha256': sha256(Path(__file__)),
    }


def coeff_to_fft(coeff, n):
    """Pack normalized torus coefficients into an unnormalized NumPy FFT."""
    vh = np.zeros((3, n, n, n), dtype=complex)
    for key, val in coeff.items():
        idx = tuple(int(x) % n for x in key)
        vh[(slice(None),) + idx] = np.asarray(val, dtype=complex) * n**3
    return vh


def fft_to_coeff(vh, tol=1e-12):
    """Invert coeff_to_fft. Integer mode index, coefficient vh/n**3."""
    n = vh.shape[1]
    bins = np.rint(np.fft.fftfreq(n) * n).astype(int)
    mag = np.max(np.abs(vh), axis=0)
    coeff = {}
    for ix, iy, iz in np.argwhere(mag > tol * n**3):
        key = (int(bins[ix]), int(bins[iy]), int(bins[iz]))
        coeff[key] = vh[:, ix, iy, iz] / n**3
    return coeff


def torus_moments(coeff):
    """X and Y on the integer lattice: sum |k|^{2} |û|^{2} and sum |k|^{4} |û|^{2}."""
    energy_x = 0.0
    energy_y = 0.0
    for key, value in coeff.items():
        radius = sum(int(t) * int(t) for t in key)
        mass = float(np.vdot(value, value).real)
        energy_x += radius * mass
        energy_y += radius * radius * mass
    return energy_x, energy_y


def physical_edges(K, N, L):
    """Physical wavenumbers of the integer cutoffs. Not used inside Phi_abc."""
    factor = 2 * np.pi / L
    return {
        'L': L,
        'K_integer': K,
        'N_integer': N,
        'k_phys_at_K': factor * K,
        'k_phys_at_N': factor * N,
    }


def diagnose(vh, L, c, K, N):
    """Signed diagnostic on a driver FFT state. Does not call the stepper."""
    coeff = fft_to_coeff(vh)
    t_sc = phi_scalene(coeff, K=K, N=N)
    t_ordered = ordered_transfer(coeff, K=K, N=N, scalene=True)
    x_torus, y_torus = torus_moments(coeff)
    nu = 1.0 / c
    d_value = t_sc - nu * y_torus / 4
    rate = d_value / x_torus if x_torus != 0 else None
    return {
        'T_sc': t_sc,
        'T_ordered': t_ordered,
        'X_torus': x_torus,
        'Y_torus': y_torus,
        'nu': nu,
        'D': d_value,
        'd': rate,
        'cutoff': physical_edges(K, N, L),
        'convention': (
            'Phi_abc uses integer radii |k|^2 with K^2 < a < b < c <= N^2. '
            'Physical wavenumber 2*pi*|k|/L is recorded and is not substituted '
            'into Phi_abc. L versus 2L is unresolved.'
        ),
    }


def five_checks(n=16, L=2 * np.pi, c=200):
    """The five engineering checks. Not a Lemma 19 certification."""
    family = []
    for m in (1, 2, 3):
        for amp in (1, 2):
            packed = coeff_to_fft(witness(m, amp), n)
            row = diagnose(packed, L, c, K=0, N=float('inf'))
            expected = 4 * m**3 * amp**3
            family.append({
                'm': m,
                'A': amp,
                'expected': expected,
                'T_sc': row['T_sc'],
                'T_ordered': row['T_ordered'],
            })
    base = coeff_to_fft(witness(WITNESS_M, WITNESS_A), n)
    low = diagnose(base, L, c, K=2, N=float('inf'))
    high = diagnose(base, L, c, K=0, N=4)
    plus = diagnose(base, L, c, K=WITNESS_K, N=WITNESS_N)
    return {
        'family': family,
        'K2_is_zero': low['T_sc'],
        'N4_is_zero': high['T_sc'],
        'plus_32': plus,
    }


def report():
    checks = five_checks()
    payload = {
        'hashes': source_hashes(),
        'stepper_unchanged_symbol': gauss.step.__module__ + '.step',
        'production_experiment': 'not launched',
        'checks': {
            'family_match': all(
                abs(row['T_sc'] - row['expected']) < 1e-9
                and abs(row['T_ordered'] - row['expected']) < 1e-9
                for row in checks['family']
            ),
            'K2': checks['K2_is_zero'],
            'N4': checks['N4_is_zero'],
            'plus_32_T_sc': checks['plus_32']['T_sc'],
            'plus_32_T_ordered': checks['plus_32']['T_ordered'],
            'edges_L': checks['plus_32']['cutoff'],
            'edges_2L': physical_edges(WITNESS_K, WITNESS_N, 4 * np.pi),
        },
    }
    return payload


if __name__ == '__main__':
    print(json.dumps(report(), indent=2, default=str))
