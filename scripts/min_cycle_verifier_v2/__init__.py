"""MIN-CYCLE v2 verifier — DA independent reproduction.

Search space: saturated integer kernel via column HNF.
Not a rational nullspace with denominators cleared.
Not armed. No canonical (M, b, γ) labels. No P2 data.
"""

from min_cycle_verifier_v2.enumerate import (
    enumerate_basis_coeffs,
    enumerate_entry_bounded,
)
from min_cycle_verifier_v2.exceptions import DisarmedError, MalformedInputError
from min_cycle_verifier_v2.hnf import column_hnf, det, is_column_hnf, matmul
from min_cycle_verifier_v2.index import (
    lattice_contains,
    relative_index,
    saturation_index,
)
from min_cycle_verifier_v2.kernel import (
    in_right_kernel,
    kernel_certificate,
    left_kernel_saturated,
    right_kernel_saturated,
)
from min_cycle_verifier_v2.rational_sublattice import rational_nullspace_cleared
from min_cycle_verifier_v2.status import (
    COEFF_MAX_CAVEAT,
    DA_CONCLUSION,
    RESEARCH_CHAIN,
    STATUS_FROZEN,
    status_record,
)
from min_cycle_verifier_v2.validate import require_integer_matrix

__all__ = [
    "COEFF_MAX_CAVEAT",
    "DA_CONCLUSION",
    "DisarmedError",
    "MalformedInputError",
    "RESEARCH_CHAIN",
    "STATUS_FROZEN",
    "column_hnf",
    "det",
    "enumerate_basis_coeffs",
    "enumerate_entry_bounded",
    "in_right_kernel",
    "is_column_hnf",
    "kernel_certificate",
    "lattice_contains",
    "left_kernel_saturated",
    "matmul",
    "rational_nullspace_cleared",
    "relative_index",
    "require_integer_matrix",
    "right_kernel_saturated",
    "saturation_index",
    "status_record",
]
