"""Poisson gravity laboratory with explicit zero-mode handling.

The laboratory represents the established Newtonian Poisson problem by
functional roles. It does not derive gravity.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .schema import (
    EvidenceLevel,
    RecoveryKind,
    REPRESENTATION_NOT_DERIVATION,
    ScaleResponseSubtype,
)


@dataclass
class PoissonCompatibility:
    source_mean: float
    zero_mode_removed: bool
    mean_subtraction_performed: bool
    potential_gauge: str
    compatible: bool
    message: str


@dataclass
class GravitySolveResult:
    potential: np.ndarray | None
    wavenumbers: np.ndarray
    modal_potential: np.ndarray | None
    compatibility: PoissonCompatibility
    recovery_kind: RecoveryKind
    evidence_level: EvidenceLevel
    statement: str
    scale_coordinate: str
    scale_response: str
    role_map: str
    divided_by_k_squared: bool


def spectral_response(kappa: np.ndarray) -> np.ndarray:
    """R_g(κ) = 1/κ² for κ ≠ 0. The zero mode is never inverted."""
    kappa = np.asarray(kappa, dtype=float)
    response = np.full_like(kappa, np.nan, dtype=float)
    nonzero = np.abs(kappa) > 0
    response[nonzero] = 1.0 / np.square(kappa[nonzero])
    return response


def solve_periodic_poisson(
    rho: np.ndarray,
    *,
    G: float = 1.0,
    length: float = 2.0 * np.pi,
    mean_policy: str = "reject",
    potential_gauge: str = "zero_mean",
) -> GravitySolveResult:
    """Solve ∇²Φ = 4πGρ on a 1-D periodic interval.

    ``mean_policy`` is ``reject`` or ``subtract``. The k=0 mode is never
    evaluated through 1/k².
    """
    rho = np.asarray(rho, dtype=float)
    n = rho.size
    dx = length / n
    source_mean = float(np.sum(rho) * dx / length)
    rho_work = rho.copy()
    mean_subtracted = False
    compatible = abs(source_mean) <= 1e-12
    message = "source mean is consistent with periodic solvability"
    if not compatible:
        if mean_policy == "subtract":
            rho_work = rho - source_mean
            mean_subtracted = True
            compatible = True
            message = (
                "nonzero source mean detected; mean subtracted before the "
                "inverse Laplacian was applied"
            )
        else:
            return GravitySolveResult(
                potential=None,
                wavenumbers=_wavenumbers(n, length),
                modal_potential=None,
                compatibility=PoissonCompatibility(
                    source_mean=source_mean,
                    zero_mode_removed=True,
                    mean_subtraction_performed=False,
                    potential_gauge=potential_gauge,
                    compatible=False,
                    message=(
                        "periodic Poisson problem is incompatible: source mean "
                        f"= {source_mean:.6g} ≠ 0. Inverse-Laplacian 1/k² was "
                        "not evaluated."
                    ),
                ),
                recovery_kind=RecoveryKind.REPRESENTATION_RECOVERY,
                evidence_level=EvidenceLevel.MATHEMATICAL_COMPATIBILITY,
                statement=REPRESENTATION_NOT_DERIVATION,
                scale_coordinate="kappa_n = k_n",
                scale_response="R_g(kappa_n) = 1/kappa_n^2",
                role_map="Phi = inverse_Laplacian(4 π G ρ) on the orthogonal complement of constants",
                divided_by_k_squared=False,
            )

    k = _wavenumbers(n, length)
    rho_hat = np.fft.fft(rho_work)
    phi_hat = np.zeros_like(rho_hat, dtype=complex)
    response = spectral_response(k)
    # ∇²Φ = 4πGρ  ⇒  -k² Φ_k = 4πG ρ_k  ⇒  Φ_k = -4πG ρ_k / k²
    nonzero = np.abs(k) > 0
    phi_hat[nonzero] = -4.0 * np.pi * G * rho_hat[nonzero] * response[nonzero]
    if potential_gauge == "zero_mean":
        phi_hat[0] = 0.0
        gauge_note = "additive constant fixed by zero spatial mean"
    else:
        gauge_note = f"additive constant left arbitrary ({potential_gauge})"
    potential = np.real(np.fft.ifft(phi_hat))
    return GravitySolveResult(
        potential=potential,
        wavenumbers=k,
        modal_potential=phi_hat,
        compatibility=PoissonCompatibility(
            source_mean=source_mean,
            zero_mode_removed=True,
            mean_subtraction_performed=mean_subtracted,
            potential_gauge=gauge_note,
            compatible=True,
            message=message,
        ),
        recovery_kind=RecoveryKind.REPRESENTATION_RECOVERY,
        evidence_level=EvidenceLevel.MATHEMATICAL_COMPATIBILITY,
        statement=REPRESENTATION_NOT_DERIVATION,
        scale_coordinate="kappa_n = k_n",
        scale_response="R_g(kappa_n) = 1/kappa_n^2",
        role_map="Phi = inverse_Laplacian(4 π G ρ) on the orthogonal complement of constants",
        divided_by_k_squared=True,
    )


def _wavenumbers(n: int, length: float) -> np.ndarray:
    return 2.0 * np.pi * np.fft.fftfreq(n, d=length / n)


def newtonian_role_map() -> dict[str, str]:
    return {
        "recovery_kind": RecoveryKind.REPRESENTATION_RECOVERY.value,
        "label": "Functional-role representation of established Newtonian Poisson gravity.",
        "statement": REPRESENTATION_NOT_DERIVATION,
        "scale_coordinate_subtype": ScaleResponseSubtype.SPECTRAL_COORDINATE.value,
        "scale_response_subtype": ScaleResponseSubtype.TRANSFER_FUNCTION.value,
        "evidence_level": str(int(EvidenceLevel.MATHEMATICAL_COMPATIBILITY)),
    }


def newtonian_fra_map() -> dict[str, str]:
    """Historical alias. Prefer newtonian_role_map."""
    return newtonian_role_map()
