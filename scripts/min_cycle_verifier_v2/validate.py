"""Refuse anything that is not a rectangular matrix of Python ints.

Bool is a subclass of int in Python; it is still malformed here.
Floats, even integral-valued, are refused. Empty and ragged
matrices are refused.
"""

from __future__ import annotations

from typing import Any, List, Sequence, Tuple

from min_cycle_verifier_v2.exceptions import MalformedInputError

Matrix = List[List[int]]


def _refuse(msg: str) -> None:
    raise MalformedInputError(msg)


def require_int(value: Any, *, where: str) -> int:
    if type(value) is not int:
        _refuse(
            f"{where}: expected a Python int, got {type(value).__name__!r}={value!r}"
        )
    return value


def require_integer_matrix(M: Any) -> Tuple[Matrix, int, int]:
    """Return a deep-copied m×n integer matrix, or refuse."""
    if M is None:
        _refuse("matrix is None")
    if isinstance(M, (str, bytes, bytearray)):
        _refuse("matrix must not be a string or bytes")
    if not isinstance(M, (list, tuple)):
        _refuse(f"matrix must be a list of rows, got {type(M).__name__}")
    if len(M) == 0:
        _refuse("empty matrix (no rows)")

    rows: Matrix = []
    n = None
    for i, row in enumerate(M):
        if isinstance(row, (str, bytes, bytearray)):
            _refuse(f"row {i} is a string or bytes, not a sequence of ints")
        if not isinstance(row, (list, tuple)):
            _refuse(f"row {i} must be a list of ints, got {type(row).__name__}")
        if n is None:
            n = len(row)
            if n == 0:
                _refuse("empty matrix (no columns)")
        elif len(row) != n:
            _refuse(f"ragged matrix: row 0 has {n} columns, row {i} has {len(row)}")
        copied = [require_int(entry, where=f"M[{i}][{j}]") for j, entry in enumerate(row)]
        rows.append(copied)

    assert n is not None
    return rows, len(rows), n


def require_integer_vector(v: Any, *, n: int | None = None, name: str = "v") -> List[int]:
    if v is None:
        _refuse(f"{name} is None")
    if isinstance(v, (str, bytes, bytearray)):
        _refuse(f"{name} must not be a string or bytes")
    if not isinstance(v, (list, tuple)):
        _refuse(f"{name} must be a list of ints, got {type(v).__name__}")
    if len(v) == 0:
        _refuse(f"{name} is empty")
    out = [require_int(entry, where=f"{name}[{j}]") for j, entry in enumerate(v)]
    if n is not None and len(out) != n:
        _refuse(f"{name} has length {len(out)}, expected {n}")
    return out


def identity(n: int) -> Matrix:
    require_int(n, where="n")
    if n < 0:
        _refuse("negative dimension")
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def zeros(m: int, n: int) -> Matrix:
    require_int(m, where="m")
    require_int(n, where="n")
    if m < 0 or n < 0:
        _refuse("negative dimension")
    return [[0] * n for _ in range(m)]


def shape(A: Sequence[Sequence[int]]) -> Tuple[int, int]:
    m = len(A)
    n = len(A[0]) if m else 0
    return m, n
