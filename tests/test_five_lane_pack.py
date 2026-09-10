"""Recovered ffe858c five-lane pack sits. Live stokes_moments not overwritten."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "jonathan-handoff/GROK-HEAVY/01-swirl-publishing/five-lane-pack"
SCRIPTS = PACK / "scripts" / "ns_attacks"
NINEB = ROOT / "results/ns_five_lane_2026-09-10/attack9b_exact_shell"
LIVE = ROOT / "scripts" / "ns_attacks" / "stokes_moments.py"
PHONE = ROOT / "docs" / "FIVE-LANE-PACK.md"

REQUIRED = (
    "__init__.py",
    "stokes_moments.py",
    "run_all_five.py",
    "attack1_covariance.py",
    "attack2_triad_k0_cstar.py",
    "attack3_bony_hh_l.py",
    "attack4_stokes.py",
    "attack5_route2_kill.py",
    "attack9_packet_fan.py",
    "attack9b_exact_shell_K.py",
    "lemma_star_near_shell_search.py",
)


class FiveLanePackTests(unittest.TestCase):
    def test_full_folder_and_phone(self):
        self.assertTrue(PACK.is_dir())
        self.assertTrue((PACK / "README.md").is_file())
        self.assertTrue((PACK / "THIS-BRANCH.md").is_file())
        self.assertTrue((PACK / "tests/test_ns_attacks_lemma_star.py").is_file())
        self.assertTrue(PHONE.is_file())
        self.assertIn("ffe858c", PHONE.read_text())
        self.assertIn("not overwritten", PHONE.read_text())
        missing = [n for n in REQUIRED if not (SCRIPTS / n).is_file()]
        self.assertEqual(missing, [])
        py = sorted(p.name for p in SCRIPTS.glob("*.py"))
        self.assertEqual(len(py), 11)

    def test_live_stokes_moments_not_replaced(self):
        text = LIVE.read_text()
        self.assertIn("def hh_l_sphere_pairs", text)
        pack_sm = (SCRIPTS / "stokes_moments.py").read_text()
        self.assertNotIn("def hh_l_sphere_pairs", pack_sm)

    def test_pack_formula_tests_pass(self):
        import os
        import subprocess

        env = os.environ.copy()
        env["PYTHONPATH"] = str(PACK / "scripts")
        code = (
            "import importlib.util, sys\n"
            f"sys.path.insert(0, {str(PACK / 'scripts')!r})\n"
            "import ns_attacks.stokes_moments as sm\n"
            "assert 'five-lane-pack' in sm.__file__, sm.__file__\n"
            f"p = {str(PACK / 'tests/test_ns_attacks_lemma_star.py')!r}\n"
            "spec = importlib.util.spec_from_file_location('pack_t', p)\n"
            "mod = importlib.util.module_from_spec(spec)\n"
            "spec.loader.exec_module(mod)\n"
            "ns = [n for n in dir(mod) if n.startswith('test_')]\n"
            "assert len(ns) >= 10, ns\n"
            "for n in ns:\n"
            "    getattr(mod, n)()\n"
            "print('pack_tests', len(ns))\n"
        )
        proc = subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("pack_tests", proc.stdout)

    def test_attack9b_json_and_plots(self):
        data = json.loads((NINEB / "attack9b.json").read_text())
        self.assertEqual(data["attack"], "9B")
        self.assertIs(data["ns_solved"], False)
        self.assertAlmostEqual(data["max_K"]["K"], 0.6410131735094131, places=10)
        self.assertEqual(data["max_K"]["alpha"], 4)
        self.assertEqual(data["max_K"]["beta"], 8)
        self.assertTrue((NINEB / "K_by_ab_pair.png").is_file())
        self.assertTrue((NINEB / "R_star_eps_limit.png").is_file())
        self.assertTrue((NINEB / "BETA_SPLIT_CONFIRM.md").is_file())


if __name__ == "__main__":
    unittest.main()
