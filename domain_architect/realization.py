"""Realization: architecture → predicted outcome y.

This is the ordinary name for the one SFE *function* worth keeping —
an outcome model. It is not a field equation and it is not called SFE.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

from .dynamics import ControllerSpec, free_oscillator_trajectory, second_order_field, simulate


@dataclass
class Realization:
    """y = realization(architecture)."""

    name: str
    y: np.ndarray
    t: np.ndarray
    method: str
    assumptions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "method": self.method,
            "n_samples": int(self.y.size),
            "y_final": float(self.y[-1]) if self.y.size else None,
            "assumptions": list(self.assumptions),
        }


def realize_second_order(
    *,
    omega: float,
    zeta: float,
    x0: tuple[float, float] = (1.0, 0.0),
    t_final: float = 6.0,
    dt: float = 0.005,
    controller: ControllerSpec | None = None,
) -> Realization:
    """Predict the state trajectory of a second-order linear plant."""
    if controller is None:
        traj = free_oscillator_trajectory(
            omega=omega,
            zeta=zeta,
            x0=x0[0],
            v0=x0[1],
            t_final=t_final,
            dt=dt,
        )
        method = "RK4 free response — standard IVP, not Domain Architect itself"
    else:
        sim = simulate(
            second_order_field(omega, zeta),
            x0=np.array(x0, dtype=float),
            t_final=t_final,
            dt=dt,
            controller=controller,
        )
        traj = sim.trajectory
        method = "RK4 + saturated PD — standard control, not Domain Architect itself"
    return Realization(
        name="second_order_linear",
        y=traj.x.copy(),
        t=traj.t.copy(),
        method=method,
        assumptions=[
            "lumped second-order linear plant",
            "constant coefficients",
            "state is the first component of x",
        ],
    )


def realize(
    architecture: str,
    predictor: Callable[[], Realization] | None = None,
) -> Realization:
    if predictor is not None:
        return predictor()
    raise ValueError(
        f"no realization is registered for {architecture!r}; "
        "supply an explicit predictor"
    )
