"""Vorticity-form signed transfer.

T_sc = T_full - T_rep, using (u·grad)u = grad(|u|^2/2) - u×curl(u)
and divergence-free receivers. No coefficient deletion and no production
error certificate. The cancellation ratio is a report, not a bound.
The byte estimate does not cover every NumPy temporary.
"""
import numpy as np


def _estimate_bytes(n):
    """One complex vector field is 3*n^3*16 bytes; one real field is half that."""
    complex_field = 3 * n**3 * 16
    real_field = 3 * n**3 * 8
    # h, curl(h), one inverse-FFT buffer, one shell, plus u, Ah, v_shell, w_shell.
    return 4 * complex_field + 4 * real_field


def _validate(h, L, K, N, tol):
    if not np.isfinite(L) or L <= 0:
        raise ValueError('L must be a positive finite length')
    if K < 0:
        raise ValueError('K must be nonnegative')
    if N is not None and not (0 <= K < N):
        raise ValueError('Require 0 <= K < N')
    if not np.isfinite(h).all():
        raise ValueError('Fourier coefficients must be finite')
    n = h.shape[1]
    index = (-np.arange(n)) % n
    partner = np.conjugate(h[:, index][:, :, index][:, :, :, index])
    scale = max(1.0, float(np.max(np.abs(h))))
    hermitian_defect = float(np.max(np.abs(h - partner)))
    if hermitian_defect > tol * scale:
        raise ValueError(f'input is not Hermitian at the working tolerance; defect {hermitian_defect}')
    modes = np.rint(np.fft.fftfreq(n) * n).astype(int)
    mx, my, mz = np.meshgrid(modes, modes, modes, indexing='ij')
    divergence = mx * h[0] + my * h[1] + mz * h[2]
    divergence_defect = float(np.max(np.abs(divergence)))
    if divergence_defect > tol * scale:
        raise ValueError(f'input is not divergence-free at the working tolerance; defect {divergence_defect}')
    return hermitian_defect, divergence_defect


def vorticity_scalene(vh, L, K=0, N=None, *, return_parts=False, tol=1e-6, max_bytes=256 * 1024**2):
    a = np.asarray(vh)
    if a.ndim != 4 or a.shape[0] != 3 or len(set(a.shape[1:])) != 1:
        raise ValueError('expected (3,n,n,n)')
    n = a.shape[1]
    if N is not None and N >= n / 3:
        raise ValueError('N must be < n/3')
    if max_bytes <= 0:
        raise ValueError('max_bytes must be positive')
    estimated = _estimate_bytes(n)
    if estimated > max_bytes:
        raise MemoryError(f'estimated {estimated} bytes exceeds cap {max_bytes}')
    hermitian_defect, divergence_defect = _validate(a, L, K, N, tol)
    modes = np.rint(np.fft.fftfreq(n) * n).astype(int)
    mx, my, mz = np.meshgrid(modes, modes, modes, indexing='ij')
    r2 = mx * mx + my * my + mz * mz
    keep = r2 > K * K
    if N is not None:
        keep &= r2 <= N * N
    h = np.where(keep[None, ...], a, 0)
    alpha = 2 * np.pi / L
    kx, ky, kz = (alpha * mx, alpha * my, alpha * mz)

    def curl_hat(v):
        return np.stack((1j * (ky * v[2] - kz * v[1]), 1j * (kz * v[0] - kx * v[2]), 1j * (kx * v[1] - ky * v[0])))

    def physical(v):
        return np.fft.ifftn(v, axes=(-3, -2, -1)).real

    u = physical(h)
    ah = physical((alpha**2 * r2)[None, ...] * h)

    def cross_integral(v, omega, receiver):
        return float(L**3 * np.mean(np.sum(np.cross(v, omega, axisa=0, axisb=0, axisc=0) * receiver, axis=0)))

    full = cross_integral(u, physical(curl_hat(h)), ah)
    repeated = 0.0
    shells = np.unique(r2[keep])
    for shell in shells:
        hs = np.where((r2 == shell)[None, ...], h, 0)
        vs = physical(hs)
        ws = physical(curl_hat(hs))
        repeated += cross_integral(vs, ws, ah - alpha**2 * shell * u)
    out = float(full - repeated)
    if not return_parts:
        return out
    tiny = np.finfo(float).tiny
    ratio = (abs(full) + abs(repeated)) / max(abs(out), tiny)
    return out, {
        'full': float(full),
        'repeated': float(repeated),
        'shell_count': int(len(shells)),
        'abs_full': abs(float(full)),
        'abs_repeated': abs(float(repeated)),
        'abs_T_sc': abs(out),
        'cancellation_ratio': float(ratio),
        'hermitian_defect': hermitian_defect,
        'divergence_defect': divergence_defect,
        'estimated_bytes': int(estimated),
        'memory_cap': int(max_bytes),
        'cancellation_ratio_is_not_an_error_bound': True,
    }
