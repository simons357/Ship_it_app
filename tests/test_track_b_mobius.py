#!/usr/bin/env python3
"""RH Track B Möbius–GCD: identities, quarantine, missing-bridge obstruction."""

from __future__ import annotations

import json
import unittest
from fractions import Fraction

from domain_architect.audit import audit_expression
from domain_architect.cli import main
from domain_architect.schema import CANONICAL_SFE_STATUS
from domain_architect.track_b_mobius import (
    LOCKED_OPERATOR,
    OUTPUT_OBSTRUCTION,
    attack,
    h_of,
    holder_always_order_n,
    looks_like_locked_operator,
    mobius_sieve,
    quarantined_operator_hit,
    spectral_snapshot,
    verify_identities,
)


class TestHValues(unittest.TestCase):
    def test_specified_local_factors(self):
        self.assertEqual(h_of(1), Fraction(1))
        self.assertEqual(h_of(2), -Fraction(3, 2))
        self.assertEqual(h_of(3), -Fraction(4, 3))
        self.assertEqual(h_of(4), Fraction(1, 2))
        self.assertEqual(h_of(8), 0)
        self.assertEqual(h_of(9), Fraction(1, 3))
        self.assertEqual(h_of(6), h_of(2) * h_of(3))
        self.assertEqual(h_of(12), h_of(4) * h_of(3))
        self.assertEqual(h_of(5), -Fraction(6, 5))


class TestExactIdentities(unittest.TestCase):
    def test_identities_on_small_n(self):
        for n in (1, 2, 6, 12, 18, 24, 36):
            check = verify_identities(n)
            self.assertTrue(check.ok, msg=check)

    def test_mertens_matches_sieve(self):
        mu = mobius_sieve(20)
        self.assertEqual(mu[1:11], [1, -1, -1, 0, -1, 1, -1, 0, 0, 1])
        check = verify_identities(10)
        self.assertEqual(check.mertens, sum(mu[1:11]))


class TestSpectrumAndHolder(unittest.TestCase):
    def test_indefinite_for_n_ge_2(self):
        for n in range(2, 21):
            snap = spectral_snapshot(n)
            self.assertTrue(snap["indefinite"], msg=n)
            self.assertGreater(snap["lambda_max"], 0)
            self.assertLess(snap["lambda_min"], 0)

    def test_holder_family_is_order_n(self):
        snap = spectral_snapshot(32)
        holder = holder_always_order_n(32, snap)
        self.assertTrue(holder["no_holder_bound_is_o_n"])
        self.assertGreater(min(holder["bounds"].values()), 0.2 * 32)
        self.assertLess(holder["|M(N)|"], holder["bounds"]["l2"] + 1e-9)


class TestAttackOutput(unittest.TestCase):
    def test_returns_obstruction_not_rh(self):
        report = attack(identity_ns=(8, 12), spectral_n=24, adversarial_n=24)
        self.assertEqual(report.output, OUTPUT_OBSTRUCTION)
        self.assertFalse(report.rh_claimed)
        self.assertEqual(report.operator, LOCKED_OPERATOR)
        self.assertTrue(all(c.ok for c in report.identities))
        blob = json.dumps(report.to_dict()) + report.narrative()
        self.assertNotIn('"status": "PROVED"', blob)
        self.assertNotIn("RH is proved", blob.lower())
        self.assertIn("not claimed", report.narrative().lower())
        statuses = {v.status for v in report.routes}
        self.assertIn(OUTPUT_OBSTRUCTION, statuses)
        why = report.conditional["why"].lower()
        self.assertIn("equivalent", why)

    def test_adversarial_random_signs_are_sqrt_n_scale(self):
        report = attack(identity_ns=(6,), spectral_n=24, adversarial_n=48)
        adv = report.adversarial
        self.assertTrue(adv["random_typical_is_sqrt_n_scale"])
        self.assertLess(adv["random_mean_abs"], 8.0 * adv["sqrt_n"])


class TestInquiryLock(unittest.TestCase):
    def test_locked_operator_is_detected(self):
        expr = "Q_N(i,j) = μ(gcd(i,j))/gcd(i,j)"
        self.assertTrue(looks_like_locked_operator(expr))
        report = audit_expression(expr)
        self.assertEqual(report.canonical_sfe_status, CANONICAL_SFE_STATUS)
        narrative = report.narrative().lower()
        self.assertIn("track b", narrative)
        self.assertIn("not rh", narrative)
        self.assertIn("missing bridge", narrative)
        self.assertNotIn("unified theory", narrative)
        self.assertEqual(report.confidence.mathematical_validation_status, "passed")

    def test_inverse_gcd_is_quarantined(self):
        hit = quarantined_operator_hit("Q_N(i,j)=1/gcd(i,j)")
        self.assertIsNotNone(hit)
        report = audit_expression("Q_N(i,j)=1/gcd(i,j)")
        self.assertTrue(any("quarantined" in w.lower() or "inverse-gcd" in w.lower() for w in report.warnings + report.notes))


class TestCli(unittest.TestCase):
    def test_track_b_flag_json(self):
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--track-b-mobius", "16", "--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["output"], OUTPUT_OBSTRUCTION)
        self.assertFalse(payload["rh_claimed"])
        self.assertTrue(all(c["decomp_matches"] for c in payload["identities"]))


if __name__ == "__main__":
    unittest.main()
