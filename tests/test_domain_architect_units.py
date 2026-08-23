#!/usr/bin/env python3
"""Unit tests for Domain Architect parser, checks, gravity, and protocol."""

from __future__ import annotations

import json
import unittest

import numpy as np

from domain_architect.audit import audit_expression
from domain_architect.checks import (
    GeometryRecord,
    TypeRecord,
    check_dimensions,
    check_types,
    classify_permission,
    decompose_source_state,
    expand_environment,
    warn_scale_ambiguity,
    ScaleResponseRecord,
)
from domain_architect.parser import NodeKind, parse_expression
from domain_architect.schema import (
    MathType,
    PermissionSubtype,
    SOURCE_STATE_WARNING,
    ScaleResponseSubtype,
)
from domain_architect.gravity import solve_periodic_poisson
from domain_architect.protocol import freeze_protocol, split_sets
from domain_architect.selectors import run_selector_lab


class TestParser(unittest.TestCase):
    def test_poisson_ast_shape(self):
        parsed = parse_expression("∇²Φ = 4π G ρ")
        self.assertTrue(parsed.ok)
        self.assertEqual(parsed.tree.kind, NodeKind.EQUALITY)
        pretty = parsed.tree.pretty()
        self.assertIn("Laplacian", pretty)
        self.assertIn("Multiply", pretty)
        self.assertIn("Phi", pretty)
        self.assertIn("rho", pretty)

    def test_abx_splits_into_product(self):
        parsed = parse_expression("y=abx")
        self.assertTrue(parsed.ok)
        self.assertEqual(set(parsed.tree.symbols()), {"y", "a", "b", "x"})


class TestSourceState(unittest.TestCase):
    def test_unresolved_without_rule(self):
        result = decompose_source_state(np.array([1 + 1j, 2]))
        self.assertFalse(result.resolved)
        self.assertEqual(result.warning, SOURCE_STATE_WARNING)

    def test_polar_rule(self):
        z = np.array([3 + 4j], dtype=complex)
        result = decompose_source_state(z, rule="polar")
        self.assertTrue(result.resolved)
        self.assertAlmostEqual(float(result.amplitudes[0]), 5.0)


class TestScaleAmbiguity(unittest.TestCase):
    def test_same_symbol_coordinate_and_response(self):
        warnings = warn_scale_ambiguity(
            [
                ScaleResponseRecord("lambda", ScaleResponseSubtype.WAVELENGTH),
                ScaleResponseRecord("lambda", ScaleResponseSubtype.INVERSE_EIGENVALUE),
            ]
        )
        self.assertTrue(warnings)
        self.assertIn("lambda", warnings[0])


class TestPermissionFilters(unittest.TestCase):
    def test_soft_filter(self):
        weights = np.exp(-0.3 * np.arange(8))
        check = classify_permission(weights=weights)
        self.assertEqual(check.subtype, PermissionSubtype.SOFT_FILTER)
        self.assertFalse(check.is_projector)

    def test_true_projector(self):
        p = np.array([[1.0, 0.0], [0.0, 0.0]])
        check = classify_permission(p)
        self.assertTrue(check.is_projector)
        self.assertEqual(check.subtype, PermissionSubtype.ORTHOGONAL_PROJECTOR)


class TestDimensionsAndTypes(unittest.TestCase):
    def test_poisson_dimensions(self):
        parsed = parse_expression("∇²Φ = 4π G ρ")
        result = check_dimensions(parsed.tree)
        self.assertTrue(result.consistent)

    def test_unknown_units_are_not_called_valid(self):
        parsed = parse_expression("Q = Z W")
        result = check_dimensions(parsed.tree)
        self.assertIsNone(result.consistent)
        self.assertIn("cannot yet be established", result.message.lower())

    def test_free_index_mismatch(self):
        parsed = parse_expression("G_mu_nu = T")
        records = [
            TypeRecord("G", MathType.TENSOR, indices=["mu", "nu"], rank=2),
            TypeRecord("T", MathType.SCALAR, indices=[], rank=0),
        ]
        warnings = check_types(records, parsed.tree)
        self.assertTrue(any("Free-index" in w for w in warnings))


class TestGeometryExpansion(unittest.TestCase):
    def test_e_expands(self):
        geo = GeometryRecord(geometry="S^1", topology="periodic", gauge="zero_mean")
        env = expand_environment(geo)
        self.assertEqual(env["topology"], "periodic")
        self.assertIn("gauge", env)


class TestGravitySubtract(unittest.TestCase):
    def test_mean_subtraction_documented(self):
        rho = np.ones(32)
        result = solve_periodic_poisson(rho, mean_policy="subtract")
        self.assertTrue(result.compatibility.compatible)
        self.assertTrue(result.compatibility.mean_subtraction_performed)
        self.assertTrue(np.allclose(result.potential, 0.0))


class TestSelectorBudget(unittest.TestCase):
    def test_equal_budget(self):
        rng = np.random.default_rng(0)
        field = rng.normal(size=40)
        lab = run_selector_lab(field, budget=5, random_seeds=(1, 2), include_optimized=True)
        self.assertTrue(all(r.retained_count == 5 for r in lab.results))
        self.assertEqual(len(lab.protocol_hash), 64)


class TestProtocolSplit(unittest.TestCase):
    def test_hash_changes_when_config_changes(self):
        a = freeze_protocol({"budget": 4, "seeds": [1, 2]})
        b = freeze_protocol({"budget": 5, "seeds": [1, 2]})
        self.assertNotEqual(a.protocol_hash, b.protocol_hash)
        split = split_sets(["a", "b", "c", "d", "e"], fractions=(0.4, 0.2, 0.4), seed=0)
        self.assertEqual(len(split.development) + len(split.validation) + len(split.test), 5)
        self.assertTrue(set(split.development).isdisjoint(split.test))


class TestEinsteinHandling(unittest.TestCase):
    def test_gr_not_forced_to_five_roles(self):
        report = audit_expression(
            "G_mu_nu + Lambda g_mu_nu = 8 pi G / c^4 T_mu_nu"
        )
        extra = " ".join(report.extra_structures).lower()
        self.assertIn("metric", extra)
        self.assertIn("stress-energy", extra)
        self.assertIn("gauge", extra)
        self.assertIn("not reduced to a five-component mapping", " ".join(report.warnings).lower())


class TestDerivativeTokensDoNotBreakPoisson(unittest.TestCase):
    def test_poisson_still_parses(self):
        report = audit_expression("∇²Φ = 4π G ρ")
        self.assertTrue(any(a["candidate_role"] == "state" for a in report.role_assignments))
        self.assertTrue(any(a["candidate_role"] == "forcing" for a in report.role_assignments))


class TestRegistryImmutability(unittest.TestCase):
    def test_cannot_overwrite_original_expression(self):
        from domain_architect.registry import EquationRecord, EquationRegistry

        reg = EquationRegistry()
        reg.add_equation(
            EquationRecord(
                equation_id="SFE-H999",
                family="SFE",
                original_expression="A=B",
            )
        )
        with self.assertRaises(ValueError):
            reg.add_equation(
                EquationRecord(
                    equation_id="SFE-H999",
                    family="SFE",
                    original_expression="A=C",
                )
            )


class TestShippedRegistry(unittest.TestCase):
    def test_json_loads(self):
        from pathlib import Path

        root = Path(__file__).resolve().parents[1] / "data" / "domain_architect"
        eqs = json.loads((root / "historical_equations.json").read_text())
        cfs = json.loads((root / "conflicts.json").read_text())
        self.assertGreaterEqual(len(eqs), 16)
        self.assertTrue(any(e["equation_id"] == "SFE-H001" for e in eqs))
        self.assertTrue(any(c["relation"] == "INCOMPATIBLE" for c in cfs))
        retired = [e for e in eqs if e["audit_disposition"] == "RETIRE"]
        self.assertTrue(retired)
        self.assertTrue(all(e.get("original_expression") is not None for e in retired))


if __name__ == "__main__":
    unittest.main()
