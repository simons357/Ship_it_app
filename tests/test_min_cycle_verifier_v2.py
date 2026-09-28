"""DA independent reproduction of MIN-CYCLE verifier v2.

Inspects column-HNF, unimodular ops, both index computations,
the (2,1,1)^T regression, and malformed-input refusal.
Does not arm P2. Does not bake canonical (M, b, γ) labels.
"""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from min_cycle_verifier_v2.enumerate import (  # noqa: E402
    enumerate_basis_coeffs,
    enumerate_entry_bounded,
)
from min_cycle_verifier_v2.exceptions import MalformedInputError  # noqa: E402
from min_cycle_verifier_v2.hnf import (  # noqa: E402
    apply_ops_to_identity,
    column_hnf,
    det,
    is_column_hnf,
    matmul,
)
from min_cycle_verifier_v2.index import (  # noqa: E402
    lattice_contains,
    relative_index,
    saturation_index,
)
from min_cycle_verifier_v2.kernel import (  # noqa: E402
    in_right_kernel,
    kernel_certificate,
    left_kernel_saturated,
    right_kernel_saturated,
)
from min_cycle_verifier_v2.rational_sublattice import (  # noqa: E402
    rational_nullspace_cleared,
)
from min_cycle_verifier_v2.status import (  # noqa: E402
    ARMED,
    COEFF_MAX_CAVEAT,
    FIRST_REAL_MIN_CYCLE_RUN_PERMITTED,
    P2_ARMED,
    STATUS_FROZEN,
    status_record,
)
from min_cycle_verifier_v2.validate import require_integer_matrix  # noqa: E402

PKG = SCRIPTS / "min_cycle_verifier_v2"

# Constraint row whose saturated right kernel is the (2,1,1)^T regression.
ROW_211 = [[2, 1, 1]]
COL_211 = [[2], [1], [1]]
PRIMITIVE_CYCLE = [0, 1, -1]
BUILDER_BASIS = ([0, -1, 1], [1, -1, -1])
OLD_CLEARED = ([1, -2, 0], [1, 0, -2])  # sign-normalized form of (-1,2,0), (-1,0,2)


def _same_lattice(gens_a, gens_b) -> bool:
    return all(lattice_contains(gens_b, a)[0] for a in gens_a) and all(
        lattice_contains(gens_a, b)[0] for b in gens_b
    )


def _source_files():
    return sorted(p for p in PKG.glob("*.py") if p.name != "__pycache__")


class FrozenStatusTests(unittest.TestCase):
    def test_frozen_status_string(self):
        self.assertEqual(
            STATUS_FROZEN,
            "MIN-CYCLE v2: BUILT → SELF-TESTED → DISARMED → AWAITING DA REVIEW",
        )

    def test_not_armed(self):
        self.assertFalse(ARMED)
        self.assertFalse(P2_ARMED)
        self.assertFalse(FIRST_REAL_MIN_CYCLE_RUN_PERMITTED)

    def test_status_record_disarmed(self):
        rec = status_record()
        self.assertFalse(rec["armed"])
        self.assertFalse(rec["p2_armed"])
        self.assertFalse(rec["first_real_min_cycle_run_permitted"])
        self.assertIn("coeff_max bounds coordinates", rec["coeff_max_caveat"])

    def test_caveat_is_not_a_footnote(self):
        self.assertIn("not ||c||_∞", COEFF_MAX_CAVEAT)
        self.assertIn("entry-bounded", COEFF_MAX_CAVEAT)


class MalformedInputTests(unittest.TestCase):
    def test_refuse_none(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix(None)

    def test_refuse_empty_rows(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix([])

    def test_refuse_empty_columns(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix([[]])

    def test_refuse_ragged(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix([[1, 2], [3]])

    def test_refuse_float(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix([[1.0, 0]])

    def test_refuse_integral_float(self):
        with self.assertRaises(MalformedInputError):
            right_kernel_saturated([[2.0, 1.0, 1.0]])

    def test_refuse_bool(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix([[True, False]])

    def test_refuse_str_matrix(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix("[[1,0]]")

    def test_refuse_str_entry(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix([["1", 0]])

    def test_refuse_none_entry(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix([[1, None]])

    def test_refuse_bytes(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix(b"10")

    def test_refuse_dict(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix({0: [1, 0]})

    def test_refuse_complex(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix([[1 + 0j]])

    def test_refuse_row_string(self):
        with self.assertRaises(MalformedInputError):
            require_integer_matrix(["10"])

    def test_kernel_refuses_malformed(self):
        with self.assertRaises(MalformedInputError):
            right_kernel_saturated([[1, 2, 3.5]])

    def test_hnf_refuses_malformed(self):
        with self.assertRaises(MalformedInputError):
            column_hnf([[1], [2, 3]])


class UnimodularHNFTests(unittest.TestCase):
    def _check(self, M):
        rec = column_hnf(M)
        m, n = len(M), len(M[0])
        self.assertTrue(rec.every_op_unimodular())
        self.assertTrue(all(op.det_sign in (-1, 1) for op in rec.ops))
        self.assertEqual(matmul(M, rec.U), rec.H)
        self.assertTrue(is_column_hnf(rec.H, rec.pivot_rows))
        self.assertEqual(apply_ops_to_identity(n, rec.ops), rec.U)
        if n <= 6:
            self.assertEqual(det(rec.U), rec.det_sign)
            self.assertEqual(abs(det(rec.U)), 1)
        return rec

    def test_identity(self):
        rec = self._check([[1, 0], [0, 1]])
        self.assertEqual(rec.rank, 2)
        self.assertEqual(rec.H, [[1, 0], [0, 1]])

    def test_row_211(self):
        rec = self._check(ROW_211)
        self.assertEqual(rec.rank, 1)
        self.assertEqual(rec.H[0][0], 1)
        self.assertEqual(rec.H[0][1], 0)
        self.assertEqual(rec.H[0][2], 0)

    def test_tall_211_column(self):
        rec = self._check(COL_211)
        self.assertEqual(rec.rank, 1)
        self.assertEqual(len(rec.U), 1)
        self.assertEqual(abs(det(rec.U)), 1)

    def test_negative_pivot_is_flipped(self):
        rec = self._check([[-2, -4]])
        self.assertGreater(rec.H[0][0], 0)

    def test_zero_row_skipped(self):
        rec = self._check([[0, 0, 0], [2, 1, 1]])
        self.assertEqual(rec.rank, 1)
        self.assertEqual(rec.pivot_rows, [1])

    def test_two_dependent_rows(self):
        rec = self._check([[1, 2, 3], [2, 4, 6]])
        self.assertEqual(rec.rank, 1)

    def test_full_rank_rectangular(self):
        rec = self._check([[1, 0, 5], [0, 1, 7]])
        self.assertEqual(rec.rank, 2)
        self.assertEqual(rec.H[0][2], 0)
        self.assertEqual(rec.H[1][2], 0)

    def test_swap_is_unimodular(self):
        rec = column_hnf([[0, 1]])
        kinds = {op.kind for op in rec.ops}
        self.assertTrue(rec.every_op_unimodular())
        self.assertTrue(kinds <= {"swap_cols", "neg_col", "add_col"})

    def test_add_multiple_is_unimodular(self):
        rec = column_hnf([[2, 1]])
        self.assertTrue(any(op.kind == "add_col" for op in rec.ops))
        self.assertTrue(rec.every_op_unimodular())

    def test_ops_replay_matches_U(self):
        rec = column_hnf([[3, 5, 7], [1, 0, 2]])
        self.assertEqual(apply_ops_to_identity(3, rec.ops), rec.U)

    def test_no_unknown_op_kinds(self):
        rec = column_hnf([[4, 6, 8, 10], [0, 1, 1, 1]])
        for op in rec.ops:
            self.assertIn(op.kind, ("swap_cols", "neg_col", "add_col"))


class SaturatedKernelTests(unittest.TestCase):
    def test_identity_has_trivial_kernel(self):
        self.assertEqual(right_kernel_saturated([[1, 0], [0, 1]]), [])

    def test_kernel_vectors_are_integer_null(self):
        M = [[2, 1, 1, 0], [0, 2, 0, 2]]
        for v in right_kernel_saturated(M):
            self.assertTrue(in_right_kernel(M, v))
            self.assertTrue(any(v))

    def test_saturation_index_one(self):
        M = [[2, 1, 1]]
        basis = right_kernel_saturated(M)
        self.assertEqual(saturation_index(basis), 1)

    def test_left_kernel_of_column_211(self):
        basis = left_kernel_saturated(COL_211)
        self.assertEqual(len(basis), 2)
        self.assertEqual(saturation_index(basis), 1)

    def test_certificate_h_equals_mu(self):
        cert = kernel_certificate([[5, 3, 1], [0, 2, 4]])
        self.assertTrue(cert["H_equals_MU"])
        self.assertTrue(cert["every_op_unimodular"])
        self.assertTrue(cert["not_a_rational_nullspace"])
        self.assertEqual(cert["search_space"], "saturated integer kernel ker_Z(M)")

    def test_zero_matrix_kernel_is_standard_basis(self):
        basis = right_kernel_saturated([[0, 0], [0, 0]])
        self.assertEqual(len(basis), 2)
        self.assertTrue(_same_lattice(basis, ([1, 0], [0, 1])))

    def test_content_row_still_saturated(self):
        basis = right_kernel_saturated([[2, 4, 6]])
        self.assertEqual(saturation_index(basis), 1)
        self.assertTrue(in_right_kernel([[2, 4, 6]], [1, -2, 1]))
        self.assertTrue(in_right_kernel([[2, 4, 6]], [-2, 1, 0]))


class Regression211Tests(unittest.TestCase):
    """Independent reproduction of the required (2,1,1)^T regression."""

    def test_saturated_basis_matches_builder_lattice(self):
        basis = right_kernel_saturated(ROW_211)
        self.assertTrue(_same_lattice(basis, BUILDER_BASIS))

    def test_contains_missing_primitive_cycle(self):
        basis = right_kernel_saturated(ROW_211)
        ok, coeffs = lattice_contains(basis, PRIMITIVE_CYCLE)
        self.assertTrue(ok)
        self.assertIsNotNone(coeffs)
        self.assertTrue(in_right_kernel(ROW_211, PRIMITIVE_CYCLE))

    def test_builder_reported_basis_is_saturated(self):
        self.assertEqual(saturation_index(BUILDER_BASIS), 1)
        self.assertTrue(in_right_kernel(ROW_211, BUILDER_BASIS[0]))
        self.assertTrue(in_right_kernel(ROW_211, BUILDER_BASIS[1]))

    def test_old_q_lattice_has_index_two(self):
        old = rational_nullspace_cleared(ROW_211)
        self.assertTrue(_same_lattice(old, OLD_CLEARED) or _same_lattice(old, ([1, -2, 0], [1, 0, -2])))
        self.assertEqual(saturation_index(old), 2)

    def test_old_lattice_misses_primitive_cycle(self):
        old = rational_nullspace_cleared(ROW_211)
        ok, _ = lattice_contains(old, PRIMITIVE_CYCLE)
        self.assertFalse(ok)

    def test_relative_index_old_in_saturated_is_two(self):
        sat = right_kernel_saturated(ROW_211)
        old = rational_nullspace_cleared(ROW_211)
        self.assertEqual(relative_index(old, sat), 2)

    def test_independent_index_one_via_minors(self):
        sat = right_kernel_saturated(ROW_211)
        # Second, independent computation: gcd of 2×2 minors.
        self.assertEqual(saturation_index(sat), 1)

    def test_column_orientation_of_211(self):
        # (2,1,1)^T as a column: left kernel is the same 2-dimensional lattice.
        left = left_kernel_saturated(COL_211)
        right = right_kernel_saturated(ROW_211)
        self.assertTrue(_same_lattice(left, right))
        self.assertTrue(lattice_contains(left, PRIMITIVE_CYCLE)[0])

    def test_old_generators_are_even_in_last_two_coords(self):
        old = rational_nullspace_cleared(ROW_211)
        for v in old:
            # Up to units, cleared Q-basis of [2,1,1] has even y,z.
            self.assertEqual(v[1] % 2, 0)
            self.assertEqual(v[2] % 2, 0)

    def test_primitive_cycle_has_odd_yz(self):
        self.assertEqual(PRIMITIVE_CYCLE[1] % 2, 1)
        self.assertEqual(PRIMITIVE_CYCLE[2] % 2, 1)


class IndexComputationTests(unittest.TestCase):
    def test_standard_basis_index_one(self):
        self.assertEqual(saturation_index([[1, 0, 0], [0, 1, 0]]), 1)

    def test_even_sublattice_index_four(self):
        self.assertEqual(saturation_index([[2, 0], [0, 2]]), 4)

    def test_index_two_plane_in_z3(self):
        self.assertEqual(saturation_index([[-1, 2, 0], [-1, 0, 2]]), 2)

    def test_relative_index_requires_containment(self):
        with self.assertRaises(MalformedInputError):
            relative_index([[1, 0, 0]], [[0, 1, 0], [0, 0, 1]])

    def test_lattice_contains_zero(self):
        ok, coeffs = lattice_contains([[1, 0], [0, 1]], [0, 0])
        self.assertTrue(ok)
        self.assertEqual(coeffs, [0, 0])

    def test_lattice_rejects_half(self):
        ok, _ = lattice_contains([[2, 0], [0, 2]], [1, 0])
        self.assertFalse(ok)


class CoeffMaxCaveatTests(unittest.TestCase):
    def test_every_enumeration_carries_the_caveat(self):
        rec = enumerate_basis_coeffs(ROW_211, 1)
        self.assertEqual(rec["coeff_max_caveat"], COEFF_MAX_CAVEAT)
        self.assertFalse(rec["is_global_inf_norm_minimum"])
        self.assertTrue(rec["disarmed"])
        self.assertFalse(rec["p2_data_used"])
        self.assertFalse(rec["canonical_labels_used"])

    def test_basis_coeff_bound_can_miss_short_cycle(self):
        # Same lattice as ker[1,1,1], skewed generators.
        b1 = [1, -1, 0]
        b2 = [5, -4, -1]  # (0,1,-1) = b2 - 5 b1
        short = [0, 1, -1]
        ok, coeffs = lattice_contains([b1, b2], short)
        self.assertTrue(ok)
        self.assertGreaterEqual(max(abs(c) for c in coeffs), 5)
        self.assertEqual(max(abs(x) for x in short), 1)

    def test_entry_bounded_finds_the_short_cycle(self):
        rec = enumerate_entry_bounded([[1, 1, 1]], 1)
        cycles = [tuple(c["c"]) for c in rec["cycles"]]
        self.assertIn((0, 1, -1), cycles)
        self.assertIn((0, -1, 1), cycles)
        self.assertTrue(rec["is_global_inf_norm_minimum"])

    def test_basis_enumeration_on_211_with_coeff_one_contains_primitive(self):
        rec = enumerate_basis_coeffs(ROW_211, 1)
        cycles = [tuple(c["c"]) for c in rec["cycles"]]
        self.assertIn((0, 1, -1), cycles)
        self.assertIn((0, -1, 1), cycles)

    def test_enumeration_status_is_frozen_disarmed(self):
        rec = enumerate_basis_coeffs([[1, 0, 0]], 1)
        self.assertEqual(rec["status"]["status_frozen"], STATUS_FROZEN)


class FirewallTests(unittest.TestCase):
    """No canonical M, b, γ-labels and no P2 data in the computational core."""

    FORBIDDEN = (
        "CANONICAL_TREE",
        "PARALLELOGRAM",
        "parallelogram",
        "gamma-label",
        "γ-label",
        "γ_label",
        "canonical M",
        "NAVIER",
        "Navier",
    )

    CORE = (
        "hnf.py",
        "kernel.py",
        "index.py",
        "validate.py",
        "rational_sublattice.py",
        "exceptions.py",
    )

    def test_core_has_no_canonical_labels(self):
        for name in self.CORE:
            text = (PKG / name).read_text(encoding="utf-8")
            for tok in self.FORBIDDEN:
                self.assertNotIn(tok, text, msg=f"{name} contains {tok}")

    def test_core_has_no_p2_matrices(self):
        for name in self.CORE:
            text = (PKG / name).read_text(encoding="utf-8")
            self.assertNotIn("PARALLELOGRAM_M", text)
            self.assertNotIn("TREE_TO_LOOP", text)

    def test_package_does_not_import_p2_stack(self):
        for path in _source_files():
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("ns_attacks", text)
            self.assertNotIn("torus_p2", text)
            self.assertNotIn("one_cycle_loss", text)

    def test_hashes_are_stable_sha256(self):
        digest = hashlib.sha256()
        for path in _source_files():
            digest.update(path.read_bytes())
        hexd = digest.hexdigest()
        self.assertEqual(len(hexd), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in hexd))


class ExtraKernelTests(unittest.TestCase):
    def test_single_zero_column(self):
        basis = right_kernel_saturated([[1, 0, 2], [0, 0, 3]])
        # x1 free? Row1: x0 + 2 x2 = 0; row2: 3 x2 = 0 => x2=0, x0=0, x1 free.
        self.assertEqual(len(basis), 1)
        self.assertTrue(_same_lattice(basis, ([0, 1, 0],)))

    def test_3x3_rank_2(self):
        M = [[1, 0, 1], [0, 1, 1], [1, 1, 2]]
        basis = right_kernel_saturated(M)
        self.assertEqual(len(basis), 1)
        self.assertTrue(in_right_kernel(M, basis[0]))
        self.assertEqual(saturation_index(basis), 1)

    def test_random_small_matrices_are_saturated(self):
        # Deterministic, not a live search.
        mats = [
            [[7, 3, 5, 1]],
            [[1, 2], [3, 6], [4, 8]],
            [[2, 0, 0], [0, 3, 0]],
            [[1, 1, 1, 1], [1, -1, 1, -1]],
        ]
        for M in mats:
            basis = right_kernel_saturated(M)
            if basis:
                self.assertEqual(saturation_index(basis), 1)
            for v in basis:
                self.assertTrue(in_right_kernel(M, v))


if __name__ == "__main__":
    unittest.main()
