"""State evolution and a constrained state controller.

    ẋ = F(x, u, t)
    e = x★ − x
    u = clip(K(x, e, C), u_min, u_max)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np


VectorField = Callable[[np.ndarray, float, float], np.ndarray]


def rk4_step(f: VectorField, state: np.ndarray, action: float, t: float, dt: float) -> np.ndarray:
    k1 = f(state, action, t)
    k2 = f(state + 0.5 * dt * k1, action, t + 0.5 * dt)
    k3 = f(state + 0.5 * dt * k2, action, t + 0.5 * dt)
    k4 = f(state + dt * k3, action, t + dt)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def second_order_field(omega: float, zeta: float) -> VectorField:
    """ẋ = F(x, u, t) for ẍ + 2ζω ẋ + ω² x = u."""

    def f(state: np.ndarray, action: float, t: float) -> np.ndarray:
        _ = t
        x, v = float(state[0]), float(state[1])
        acc = action - 2.0 * zeta * omega * v - (omega**2) * x
        return np.array([v, acc], dtype=float)

    return f


def produced_intensity_field(omega: float, zeta: float, x_eq: float) -> VectorField:
    """Lumped intensity analog: ẍ + 2ζω ẋ + ω² x = ω² x_eq + u.

    Uncontrolled (u=0) equilibrium is the baseline intensity x_eq.
    This is not a k-equation and not 3D Navier–Stokes.
    """

    def f(state: np.ndarray, action: float, t: float) -> np.ndarray:
        _ = t
        x, v = float(state[0]), float(state[1])
        acc = (omega**2) * x_eq + action - 2.0 * zeta * omega * v - (omega**2) * x
        return np.array([v, acc], dtype=float)

    return f


def pd_control(
    state: np.ndarray,
    target: float,
    *,
    kp: float,
    kd: float,
    u_min: float,
    u_max: float,
    feedforward: float = 0.0,
) -> tuple[float, float]:
    error = target - float(state[0])
    raw = feedforward + kp * error - kd * float(state[1])
    action = float(np.clip(raw, u_min, u_max))
    return action, error


@dataclass
class Trajectory:
    t: np.ndarray
    x: np.ndarray
    v: np.ndarray
    u: np.ndarray
    e: np.ndarray
    saturated: np.ndarray

    def terminal_error(self) -> float:
        return float(abs(self.e[-1]))

    def max_control(self) -> float:
        return float(np.max(np.abs(self.u)))


@dataclass
class ControllerSpec:
    target: float
    kp: float = 4.0
    kd: float = 2.0
    u_min: float = -10.0
    u_max: float = 10.0
    feedforward: float = 0.0


@dataclass
class SimulationReport:
    trajectory: Trajectory
    settled: bool
    constraint_violations: int
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, float | int | bool | list[str]]:
        return {
            "settled": self.settled,
            "terminal_error": self.trajectory.terminal_error(),
            "max_control": self.trajectory.max_control(),
            "constraint_violations": self.constraint_violations,
            "notes": list(self.notes),
        }


def simulate(
    field: VectorField,
    *,
    x0: np.ndarray,
    controller: ControllerSpec,
    t_final: float = 8.0,
    dt: float = 0.01,
    settle_tol: float = 0.05,
) -> SimulationReport:
    n = int(round(t_final / dt)) + 1
    t = np.linspace(0.0, t_final, n)
    x = np.zeros(n)
    v = np.zeros(n)
    u = np.zeros(n)
    e = np.zeros(n)
    sat = np.zeros(n, dtype=int)
    state = np.asarray(x0, dtype=float).reshape(2)
    violations = 0
    for i in range(n):
        action, error = pd_control(
            state,
            controller.target,
            kp=controller.kp,
            kd=controller.kd,
            u_min=controller.u_min,
            u_max=controller.u_max,
            feedforward=controller.feedforward,
        )
        raw = (
            controller.feedforward
            + controller.kp * error
            - controller.kd * float(state[1])
        )
        if raw < controller.u_min - 1e-12 or raw > controller.u_max + 1e-12:
            violations += 1
            sat[i] = 1
        x[i], v[i], u[i], e[i] = float(state[0]), float(state[1]), action, error
        if i + 1 < n:
            state = rk4_step(field, state, action, t[i], dt)
    traj = Trajectory(t=t, x=x, v=v, u=u, e=e, saturated=sat)
    settled = bool(np.all(np.abs(e[-int(0.5 / dt) :]) < settle_tol))
    notes = [
        "Controller is saturated PD plus the feedforward needed to balance "
        "known restoring at x★. It is a synthesized feedback mechanism, "
        "not a claim of optimality.",
    ]
    if settled:
        notes.append(f"State entered |e| < {settle_tol} over the last 0.5 time units.")
    else:
        notes.append("Target was not reached under the stated gains and constraints.")
    return SimulationReport(
        trajectory=traj,
        settled=settled,
        constraint_violations=violations,
        notes=notes,
    )


def free_oscillator_trajectory(
    *,
    omega: float,
    zeta: float,
    x0: float = 1.0,
    v0: float = 0.0,
    t_final: float = 8.0,
    dt: float = 0.01,
) -> Trajectory:
    """Integrate ẍ + 2ζω ẋ + ω² x = 0."""
    field = second_order_field(omega, zeta)
    n = int(round(t_final / dt)) + 1
    t = np.linspace(0.0, t_final, n)
    x = np.zeros(n)
    v = np.zeros(n)
    state = np.array([x0, v0], dtype=float)
    for i in range(n):
        x[i], v[i] = float(state[0]), float(state[1])
        if i + 1 < n:
            state = rk4_step(field, state, 0.0, t[i], dt)
    zeros = np.zeros(n)
    return Trajectory(t=t, x=x, v=v, u=zeros, e=zeros, saturated=zeros.astype(int))
