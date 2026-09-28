"""Malformed-input and status exceptions for the MIN-CYCLE v2 verifier."""

from __future__ import annotations


class MalformedInputError(ValueError):
    """Refused input: not a rectangular matrix of Python ``int`` entries."""


class DisarmedError(RuntimeError):
    """Raised if a live/P2 MIN-CYCLE run is requested while the verifier is disarmed."""
