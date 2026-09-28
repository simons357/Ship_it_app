#!/usr/bin/env python3
"""DA self-test + hashes for MIN-CYCLE verifier v2.

Independent reproduction of the (2,1,1)^T regression, index-1
check, unimodular HNF log, and one malformed-input refusal.
Does not arm P2. Does not load canonical (M, b, γ) labels.
"""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(ROOT))

from min_cycle_verifier_v2.hnf import column_hnf, det, matmul  # noqa: E402
from min_cycle_verifier_v2.index import (  # noqa: E402
    lattice_contains,
    relative_index,
    saturation_index,
)
from min_cycle_verifier_v2.kernel import right_kernel_saturated  # noqa: E402
from min_cycle_verifier_v2.rational_sublattice import (  # noqa: E402
    rational_nullspace_cleared,
)
from min_cycle_verifier_v2.status import (  # noqa: E402
    COEFF_MAX_CAVEAT,
    DA_CONCLUSION,
    RESEARCH_CHAIN,
    STATUS_FROZEN,
    status_record,
)
from min_cycle_verifier_v2.validate import require_integer_matrix  # noqa: E402
from min_cycle_verifier_v2.exceptions import MalformedInputError  # noqa: E402

PKG = SCRIPTS / "min_cycle_verifier_v2"
RESULTS = ROOT / "results"


def sha256_files(paths: list[Path]) -> dict:
    files = {}
    h_all = hashlib.sha256()
    for path in sorted(paths):
        data = path.read_bytes()
        files[str(path.relative_to(ROOT))] = hashlib.sha256(data).hexdigest()
        h_all.update(path.name.encode())
        h_all.update(b"\0")
        h_all.update(data)
        h_all.update(b"\0")
    return {"files": files, "bundle": h_all.hexdigest()}


def reproduce_211() -> dict:
    M = [[2, 1, 1]]
    rec = column_hnf(M)
    sat = right_kernel_saturated(M)
    old = rational_nullspace_cleared(M)
    primitive = [0, 1, -1]
    builder = ([0, -1, 1], [1, -1, -1])
    in_sat, coeffs_sat = lattice_contains(sat, primitive)
    in_old, _ = lattice_contains(old, primitive)
    in_builder, _ = lattice_contains(builder, primitive)
    return {
        "M": M,
        "constraint_column_211T": True,
        "H": rec.H,
        "U": rec.U,
        "H_equals_MU": matmul(M, rec.U) == rec.H,
        "det_U": det(rec.U),
        "running_det_sign": rec.det_sign,
        "every_op_unimodular": rec.every_op_unimodular(),
        "n_ops": len(rec.ops),
        "ops": [op.describe() for op in rec.ops],
        "saturated_basis": sat,
        "builder_reported_basis": [list(v) for v in builder],
        "same_lattice_as_builder": all(
            lattice_contains(sat, v)[0] for v in builder
        )
        and all(lattice_contains(builder, v)[0] for v in sat),
        "old_q_cleared_basis": old,
        "index_saturated_gcd_minors": saturation_index(sat),
        "index_old_gcd_minors": saturation_index(old),
        "relative_index_old_in_saturated": relative_index(old, sat),
        "primitive_cycle": primitive,
        "primitive_in_saturated": in_sat,
        "primitive_saturated_coeffs": coeffs_sat,
        "primitive_in_old_lattice": in_old,
        "primitive_in_builder_basis": in_builder,
        "repair": (
            "search is over a saturated integer kernel, not a "
            "finite-index lattice from a rational nullspace"
        ),
    }


def reproduce_malformed_refusal() -> dict:
    sample = [[2, 1, 1.0]]
    try:
        require_integer_matrix(sample)
        refused = False
        message = ""
    except MalformedInputError as exc:
        refused = True
        message = str(exc)
    return {
        "sample": "[[2, 1, 1.0]]",
        "refused": refused,
        "exception": "MalformedInputError",
        "message": message,
    }


def run_unittests() -> dict:
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"), pattern="test_min_cycle_verifier_v2.py")
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
    return {
        "testsRun": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "passed": result.wasSuccessful(),
    }


def main() -> int:
    py_files = sorted(PKG.glob("*.py"))
    hashes = sha256_files(py_files)
    regression = reproduce_211()
    refusal = reproduce_malformed_refusal()
    tests = run_unittests()
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status_frozen": STATUS_FROZEN,
        "da_conclusion": DA_CONCLUSION,
        "research_chain": RESEARCH_CHAIN,
        "coeff_max_caveat": COEFF_MAX_CAVEAT,
        "status": status_record(),
        "hashes_sha256": hashes,
        "independent_211_regression": regression,
        "independent_malformed_refusal": refusal,
        "unittest": tests,
        "p2_data_used": False,
        "canonical_Mb_gamma_labels_used": False,
        "armed": False,
        "builder_binary_stamped": False,
        "builder_artifacts_in_this_repo": False,
        "note": (
            "This is DA's independent reproduction of the v2 repair. "
            "SPEC-MIN-CYCLE-VERIFIER-V2-2026-09-28.txt was cited but is "
            "not present in this repository; the builder's code and hashes "
            "were not deposited here. DA does not stamp an unseen binary. "
            "P2 remains disarmed."
        ),
    }
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / "min_cycle_v2_da_audit.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("\n=== DA AUDIT SUMMARY ===")
    print("status:", STATUS_FROZEN)
    print("conclusion:", DA_CONCLUSION)
    print("tests:", tests)
    print("211 primitive in saturated:", regression["primitive_in_saturated"])
    print("211 primitive in old lattice:", regression["primitive_in_old_lattice"])
    print("index sat / old / relative:",
          regression["index_saturated_gcd_minors"],
          regression["index_old_gcd_minors"],
          regression["relative_index_old_in_saturated"])
    print("malformed refused:", refusal["refused"])
    print("bundle sha256:", hashes["bundle"])
    print("wrote", out)
    return 0 if tests["passed"] and regression["primitive_in_saturated"] and not regression["primitive_in_old_lattice"] and refusal["refused"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
