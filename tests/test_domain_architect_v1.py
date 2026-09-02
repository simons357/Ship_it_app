#!/usr/bin/env python3
"""Acceptance tests for Domain Architect v1.0."""

from __future__ import annotations

import unittest

import numpy as np

from domain_architect.compatibility import Transformation, classify_compatibility
from domain_architect.decompose import decompose
from domain_architect.dynamics import ControllerSpec, second_order_field, simulate
from domain_architect.pipeline import (
    cycle_drag_reduction,
    cycle_inverse_control,
    cycle_mechanical_electrical,
    cycle_missing_damping,
    run_benchmarks,
)
from domain_architect.residual import recover_missing_damping
from domain_architect.schema import (
    CompatibilityClass,
    CorrespondenceKind,
    FunctionalRole,
    ValidationGate,
)
from domain_architect.signature import FunctionalSignature
from domain_architect.schema import MathType
from domain_architect.synthesize import inverse_design_architecture, synthesize
from domain_architect.translate import mechanical_electrical_translation


class TestDecomposeOscillator(unittest.TestCase):
    def test_second_order_roles(self):
        dec = decompose("m*xdd + c*xd + k*x = f")
        self.assertEqual(dec.classification.pattern, "second_order_linear_ode")
        roles = {h.symbol: h.role for h in dec.hypotheses()}
        self.assertEqual(roles["x"], FunctionalRole.STATE)
        self.assertEqual(roles["m"], FunctionalRole.STATE_TRANSITION)
        self.assertEqual(roles["c"], FunctionalRole.DISSIPATION)
        self.assertEqual(roles["k"], FunctionalRole.INTERACTION)
        self.assertEqual(roles["f"], FunctionalRole.FORCING)
        levels = {n.level for n in dec.tree.walk()}
        self.assertTrue({"SYSTEM", "FUNCTIONAL_ROLE", "MECHANISM"} <= levels)
        self.assertNotIn("PARAMETER", levels)
        for hyp in dec.hypotheses():
            self.assertTrue(hyp.rationale)
            self.assertGreaterEqual(hyp.confidence, 0.0)


class TestParserDerivatives(unittest.TestCase):
    def test_newton_primes_and_letter_suffix(self):
        from domain_architect.parser import NodeKind, parse_expression

        dotted = parse_expression("x'' + x' + x = 0")
        self.assertTrue(dotted.ok)
        orders = [
            n.value
            for n in dotted.tree.walk()
            if n.kind == NodeKind.DERIVATIVE
        ]
        self.assertIn(2, orders)
        self.assertIn(1, orders)
        suffixed = parse_expression("xdd + xd + x = 0")
        self.assertTrue(suffixed.ok)
        self.assertTrue(
            any(n.kind == NodeKind.DERIVATIVE and n.value == 2 for n in suffixed.tree.walk())
        )


class TestMissingDampingRecovery(unittest.TestCase):
    def test_recovers_zeta_and_role(self):
        report = cycle_missing_damping(omega=2.0, zeta=0.15)
        self.assertEqual(report.validation_gate, ValidationGate.COMPUTATIONAL)
        self.assertIsNotNone(report.residual)
        self.assertEqual(report.residual.missing_role, FunctionalRole.DISSIPATION)
        self.assertEqual(report.residual.operator_class, "linear_damping")
        zeta_hat = report.residual.recovered_parameter["zeta"]
        self.assertAlmostEqual(zeta_hat, 0.15, delta=0.02)

    def test_missing_forcing_is_not_called_damping(self):
        # Incomplete operator R = ẍ + ω²x applied to ẍ + ω²x = A.
        t = np.linspace(0, 4, 2000)
        omega = 2.0
        a = 0.8
        x = (a / omega**2) * (1.0 - np.cos(omega * t))
        v = (a / omega) * np.sin(omega * t)
        acc = a * np.cos(omega * t)
        # Truth: ẍ + ω² x = a, so residual of the undamped homogeneous operator is a.
        residual = acc + omega**2 * x
        from domain_architect.residual import classify_missing_mechanism

        analysis = classify_missing_mechanism(residual, x=x, v=v, omega=omega)
        self.assertEqual(analysis.missing_role, FunctionalRole.FORCING)
        self.assertAlmostEqual(analysis.recovered_parameter["A"], a, delta=0.05)


class TestMechanicalElectricalTranslation(unittest.TestCase):
    def test_transformable_not_direct(self):
        record = mechanical_electrical_translation()
        self.assertEqual(record.kind, CorrespondenceKind.MATHEMATICAL_CORRESPONDENCE)
        self.assertIn("m", record.mapping)
        self.assertTrue(record.compatibility)
        verdicts = {c.verdict for c in record.compatibility}
        self.assertIn(CompatibilityClass.TRANSFORMABLE, verdicts)
        self.assertNotIn(CompatibilityClass.INCOMPATIBLE, verdicts)
        self.assertTrue(any(c.transformation is not None for c in record.compatibility))
        self.assertIn("si_dimensions", record.broken)

    def test_analogy_without_T_is_incompatible(self):
        left = FunctionalSignature(
            FunctionalRole.DISSIPATION,
            MathType.SCALAR,
            units=(1, 0, -1, 0, 0, 0, 0),
        )
        right = FunctionalSignature(
            FunctionalRole.DISSIPATION,
            MathType.SCALAR,
            units=(1, 2, -3, -2, 0, 0, 0),
        )
        report = classify_compatibility("c", left, "R", right)
        self.assertEqual(report.verdict, CompatibilityClass.INCOMPATIBLE)
        self.assertIn("no explicit executable transformation", " ".join(report.reasons).lower())


class TestSynthesisRefusesIllegal(unittest.TestCase):
    def test_incompatible_replacement_raises(self):
        from domain_architect.compatibility import CompatibilityReport

        dec = decompose("m*xdd + c*xd + k*x = f")
        bad = CompatibilityReport(
            left="c",
            right="nonsense",
            verdict=CompatibilityClass.INCOMPATIBLE,
            kind=CorrespondenceKind.ANALOGY,
            interface_match=False,
            dimension_match=False,
        )
        with self.assertRaises(ValueError):
            synthesize(dec, replacements={"c": "nonsense"}, compatibility=[bad])

    def test_inverse_design_lists_feedback(self):
        cand = inverse_design_architecture("x=1", ["|u|<=1"])
        joined = " ".join(cand.components).lower()
        self.assertIn("measure", joined)
        self.assertIn("control", joined)
        self.assertIn("constraint", joined)


class TestControllerSettles(unittest.TestCase):
    def test_pd_reaches_target_under_constraint(self):
        report, sim = cycle_inverse_control(target=1.0, u_max=8.0)
        self.assertTrue(sim.settled)
        self.assertLess(sim.trajectory.max_control(), 8.0 + 1e-9)
        self.assertEqual(report.validation_gate, ValidationGate.COMPUTATIONAL)

    def test_rk4_free_oscillator_energy_decays(self):
        from domain_architect.dynamics import free_oscillator_trajectory

        traj = free_oscillator_trajectory(omega=2.0, zeta=0.2, t_final=6.0)
        e0 = traj.x[0] ** 2 + (traj.v[0] / 2.0) ** 2
        e1 = traj.x[-1] ** 2 + (traj.v[-1] / 2.0) ** 2
        self.assertLess(e1, 0.25 * e0)


class TestDragWorkflow(unittest.TestCase):
    def test_surrogate_respects_mass_constraint(self):
        report = cycle_drag_reduction()
        pred = report.prediction
        self.assertIsNotNone(pred)
        self.assertLessEqual(pred["mass"], 1.1 + 1e-12)
        self.assertGreater(pred["D_R"], 0.0)
        self.assertIn("Navier", " ".join(report.notes))


class TestBenchmarks(unittest.TestCase):
    def test_suite(self):
        payload = run_benchmarks()
        self.assertTrue(payload["missing_damping"]["passed"])
        self.assertEqual(payload["missing_damping"]["missing_role"], "dissipation")
        self.assertTrue(payload["inverse_control"]["passed"])
        self.assertIn("TRANSFORMABLE", payload["mechanical_electrical"]["verdicts"])


if __name__ == "__main__":
    unittest.main()
