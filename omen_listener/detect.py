"""Rotor-cue detector for a civil warning listener.

A cue is a harmonic stack — a fundamental plus two overtones — inside the
band small rotors usually occupy. Fans, mowers, and helicopters can make
the same shape. This module raises a warning. It does not name an airframe
and it does not produce an engagement solution.

Thresholds are duplicated in ``portable/omen_listener.js``. Keep them together.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Contract values. Same numbers live in portable/omen_listener.js.
F_MIN_HZ = 80.0
F_MAX_HZ = 250.0
F_STEP_HZ = 5.0
P1_OVER_NOISE = 8.0
P2_OVER_NOISE = 5.0
P3_OVER_NOISE = 4.0
MIN_SCORE = 0.45
SPEED_OF_SOUND_M_S = 343.0


@dataclass(frozen=True)
class RotorCue:
    detected: bool
    score: float
    fundamental_hz: float | None
    detail: str


def _hann(samples: list[float]) -> list[float]:
    n = len(samples)
    if n <= 1:
        return list(samples)
    scale = 2.0 * math.pi / (n - 1)
    return [samples[i] * (0.5 - 0.5 * math.cos(scale * i)) for i in range(n)]


def goertzel_power(samples: list[float], sample_rate: float, freq: float) -> float:
    """Normalized power at an exact frequency. ``samples`` should be windowed.

    The tone is not snapped to a DFT bin. A short phone frame is only a few
    hertz wide, and rotor fundamentals rarely land on a bin center.
    """
    n = len(samples)
    if n == 0 or freq <= 0.0 or freq >= sample_rate / 2.0:
        return 0.0
    omega = 2.0 * math.pi * freq / sample_rate
    coeff = 2.0 * math.cos(omega)
    s1 = 0.0
    s2 = 0.0
    for x in samples:
        s0 = x + coeff * s1 - s2
        s2 = s1
        s1 = s0
    power = s1 * s1 + s2 * s2 - coeff * s1 * s2
    if power < 0.0:
        power = 0.0
    return power / (n * n)


def rotor_cue(samples: list[float], sample_rate: float) -> RotorCue:
    """Score one microphone frame.

    Needs at least 1024 samples and an 8 kHz rate so the third harmonic
    of the search band still fits under Nyquist.
    """
    if sample_rate < 8000 or len(samples) < 1024:
        return RotorCue(False, 0.0, None, "frame too short")
    windowed = _hann([float(s) for s in samples])
    best_score = 0.0
    best_f: float | None = None
    f = F_MIN_HZ
    while f <= F_MAX_HZ + 1e-9:
        if 3.0 * f >= sample_rate * 0.45:
            break
        p1 = goertzel_power(windowed, sample_rate, f)
        p2 = goertzel_power(windowed, sample_rate, 2.0 * f)
        p3 = goertzel_power(windowed, sample_rate, 3.0 * f)
        noise_bins: list[float] = []
        # Sit between harmonics. A probe a few hertz off the fundamental
        # is still inside the window's main lobe and would fake a noise floor.
        for frac in (0.55, 0.72, 1.35, 1.62, 2.28, 2.55):
            nf = f * frac
            if nf < 40.0 or nf >= sample_rate * 0.45:
                continue
            if min(abs(nf - f), abs(nf - 2.0 * f), abs(nf - 3.0 * f)) < 12.0:
                continue
            noise_bins.append(goertzel_power(windowed, sample_rate, nf))
        if len(noise_bins) < 3:
            f += F_STEP_HZ
            continue
        noise_bins.sort()
        noise = max(noise_bins[len(noise_bins) // 2], 1e-18)
        ratio2 = p2 / p1 if p1 > 0.0 else 0.0
        ratio3 = p3 / p1 if p1 > 0.0 else 0.0
        stack = (
            p1 > P1_OVER_NOISE * noise
            and p2 > P2_OVER_NOISE * noise
            and p3 > P3_OVER_NOISE * noise
            and 0.04 <= ratio2 <= 2.5
            and 0.01 <= ratio3 <= 2.5
        )
        if stack:
            weakest = min(p1 / P1_OVER_NOISE, p2 / P2_OVER_NOISE, p3 / P3_OVER_NOISE)
            score = weakest / noise / 4.0
            if score > 1.0:
                score = 1.0
            if score > best_score:
                best_score = score
                best_f = f
        f += F_STEP_HZ
    if best_f is None or best_score < MIN_SCORE:
        return RotorCue(False, best_score, best_f, "no harmonic stack")
    return RotorCue(True, best_score, best_f, "harmonic stack")


def _correlation(left: list[float], right: list[float], lag: int) -> float:
    n = min(len(left), len(right))
    acc = 0.0
    count = 0
    for i in range(n):
        j = i - lag
        if 0 <= j < n:
            acc += left[i] * right[j]
            count += 1
    if count == 0:
        return 0.0
    return acc / count


def delay_right_minus_left(
    left: list[float],
    right: list[float],
    sample_rate: float,
    max_delay_s: float,
) -> float | None:
    """Estimate ``t_right - t_left`` in seconds.

    Positive means the right microphone heard the frame later.
    """
    n = min(len(left), len(right))
    if n < 256 or sample_rate <= 0.0 or max_delay_s <= 0.0:
        return None
    max_lag = max(1, int(math.ceil(max_delay_s * sample_rate)))
    best_lag = 0
    best = _correlation(left, right, 0)
    for lag in range(-max_lag, max_lag + 1):
        if lag == 0:
            continue
        value = _correlation(left, right, lag)
        if value > best:
            best = value
            best_lag = lag
    # Empirical sign: the lag that lines the channels up is the opposite of
    # (t_right - t_left). Negate so callers can treat a positive result as
    # "right microphone is later".
    if best_lag <= -max_lag or best_lag >= max_lag:
        return -best_lag / sample_rate
    left_c = _correlation(left, right, best_lag - 1)
    mid_c = best
    right_c = _correlation(left, right, best_lag + 1)
    denom = left_c - 2.0 * mid_c + right_c
    delta = 0.0
    if denom != 0.0:
        delta = 0.5 * (left_c - right_c) / denom
        if delta > 1.0:
            delta = 1.0
        elif delta < -1.0:
            delta = -1.0
    return -(best_lag + delta) / sample_rate


def azimuth_from_delay(
    delay_s: float,
    spacing_m: float,
    array_heading_deg: float,
    speed_of_sound: float = SPEED_OF_SOUND_M_S,
) -> float | None:
    """Compass azimuth from a left/right pair.

    ``array_heading_deg`` is the direction the pair faces (broadside),
    degrees clockwise from north. The right microphone is on the right
    when looking that way. A source to the right arrives at the right
    microphone first, so ``delay_s`` (right minus left) is negative.
    """
    if spacing_m <= 0.0 or speed_of_sound <= 0.0:
        return None
    arg = (-speed_of_sound * delay_s) / spacing_m
    if arg > 1.0:
        arg = 1.0
    elif arg < -1.0:
        arg = -1.0
    phi_deg = math.degrees(math.asin(arg))
    return (array_heading_deg + phi_deg) % 360.0


def azimuth_from_pair(
    left: list[float],
    right: list[float],
    sample_rate: float,
    spacing_m: float,
    array_heading_deg: float,
) -> float | None:
    """Bearing from two microphones on one node. Returns degrees, or None."""
    if spacing_m <= 0.0:
        return None
    max_delay_s = spacing_m / SPEED_OF_SOUND_M_S
    delay = delay_right_minus_left(left, right, sample_rate, max_delay_s)
    if delay is None:
        return None
    return azimuth_from_delay(delay, spacing_m, array_heading_deg)
