"""Living dream team: papers talk; a conversation cannot close X."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_living import CLAIMS, KINGDOMS, SPEAKERS, TURNS, run  # noqa: E402


class DaLivingTests(unittest.TestCase):
    def test_living_is_process_not_a_close(self):
        tmp = Path(tempfile.mkdtemp()) / "da_living_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["L1"]["verdict"], "pass")
        self.assertEqual(by["L2"]["verdict"], "pass")
        self.assertEqual(by["L3"]["verdict"], "pass")
        self.assertEqual(by["L4"]["verdict"], "fail")
        self.assertEqual(by["L5"]["verdict"], "fail")
        self.assertEqual(by["L6"]["verdict"], "fail")
        self.assertEqual(by["L7"]["verdict"], "fail")
        self.assertEqual(by["L8"]["verdict"], "fail")
        self.assertEqual(by["L9"]["verdict"], "fail")
        self.assertEqual(by["L10"]["verdict"], "fail")
        self.assertEqual(by["L11"]["verdict"], "fail")
        self.assertEqual(by["L12"]["verdict"], "fail")
        self.assertEqual(by["L13"]["verdict"], "open")
        self.assertEqual(by["L14"]["verdict"], "fail")
        self.assertEqual(by["L15"]["verdict"], "pass")
        self.assertEqual(by["L16"]["verdict"], "fail")
        self.assertEqual(by["L17"]["verdict"], "pass")
        self.assertEqual(by["L18"]["verdict"], "fail")
        self.assertEqual(by["L19"]["verdict"], "fail")
        self.assertEqual(by["L20"]["verdict"], "fail")
        self.assertEqual(by["L21"]["verdict"], "fail")
        self.assertEqual(by["L22"]["verdict"], "fail")
        self.assertEqual(by["L23"]["verdict"], "fail")
        self.assertEqual(by["L24"]["verdict"], "fail")
        self.assertEqual(by["L25"]["verdict"], "fail")
        self.assertEqual(by["L26"]["verdict"], "fail")
        self.assertEqual(by["L27"]["verdict"], "fail")
        self.assertEqual(by["L28"]["verdict"], "fail")
        self.assertEqual(by["L29"]["verdict"], "fail")
        self.assertEqual(by["L30"]["verdict"], "fail")
        self.assertEqual(by["L31"]["verdict"], "fail")
        self.assertEqual(by["L32"]["verdict"], "fail")
        self.assertEqual(by["L33"]["verdict"], "fail")
        self.assertEqual(by["L34"]["verdict"], "fail")
        self.assertEqual(by["L35"]["verdict"], "fail")
        self.assertEqual(by["L36"]["verdict"], "fail")
        self.assertEqual(by["L37"]["verdict"], "fail")
        self.assertEqual(by["L38"]["verdict"], "fail")
        self.assertEqual(by["L39"]["verdict"], "fail")
        self.assertEqual(by["L40"]["verdict"], "fail")
        self.assertEqual(by["L41"]["verdict"], "fail")
        self.assertEqual(by["L42"]["verdict"], "fail")
        self.assertEqual(by["L43"]["verdict"], "fail")
        self.assertEqual(by["L44"]["verdict"], "fail")
        self.assertEqual(by["L45"]["verdict"], "fail")
        self.assertEqual(by["L46"]["verdict"], "fail")
        self.assertEqual(by["L47"]["verdict"], "fail")
        self.assertEqual(by["L48"]["verdict"], "fail")
        self.assertEqual(by["L49"]["verdict"], "fail")
        self.assertEqual(by["L50"]["verdict"], "fail")
        self.assertEqual(by["L51"]["verdict"], "fail")
        self.assertEqual(by["L52"]["verdict"], "fail")
        self.assertEqual(by["L53"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["regularity_after"], "open")
        self.assertEqual(payload["meta"]["possible_to_close_X"], "open")
        self.assertTrue(payload["meta"]["not_a_vote"])
        self.assertTrue(payload["meta"]["not_a_close"])
        self.assertTrue(payload["meta"]["not_channeling"])
        self.assertTrue(payload["meta"]["papers_not_persons"])
        self.assertIn("residual", payload["meta"]["next_write"])
        self.assertTrue((ROOT / "docs" / "DA-LIVING.md").is_file())
        who = {k["who"] for k in KINGDOMS}
        self.assertTrue(any("Tao" in w for w in who))
        self.assertTrue(any("Sverak" in w for w in who))
        self.assertGreaterEqual(len(KINGDOMS), 8)

    def test_they_talk_to_each_other(self):
        names = set(SPEAKERS)
        for must in (
            "Tao",
            "Sverak",
            "Seregin",
            "Escauriaza",
            "Nadirashvili",
            "Caffarelli",
            "Fefferman",
            "Constantin",
            "Beale",
            "Koch",
            "Chemin-Gallagher",
            "Cannone-Planchon",
            "Tataru",
            "Grujic",
            "Vicol",
            "Buckmaster",
            "Elgindi",
            "Hou",
            "Miller",
            "Albritton",
            "Beirao-Berselli",
            "Chae",
            "Giga-Miura",
            "Jia",
            "Guillod",
            "Hou-Wang-Yang",
            "Lei-Ren-Tian",
            "CSTY",
            "Kozono-Taniuchi",
            "Neustupa-Penel",
            "Lin",
            "Vasseur",
            "Farwig",
            "Cheskidov",
            "Masmoudi",
            "Wolf",
            "Galdi",
            "Temam",
            "Isett",
            "Tsai",
            "Lemarie-Rieusset",
            "Danchin",
            "Kukavica",
            "Barker",
            "Robinson",
            "Operator",
        ):
            self.assertIn(must, names)
        self.assertNotIn("Ladyzhenskaya", names)
        self.assertNotIn("Leray", names)
        self.assertGreaterEqual(len(TURNS), 16)
        addressed = [t for t in TURNS if t["to"]]
        self.assertEqual(len(addressed), len(TURNS))
        living = {
            "Tao",
            "Sverak",
            "Seregin",
            "Escauriaza",
            "Nadirashvili",
            "Caffarelli",
            "Kohn",
            "Constantin",
            "Fefferman",
            "Beale",
            "Koch",
            "Chemin-Gallagher",
            "Cannone-Planchon",
            "Tataru",
            "Grujic",
            "Vicol",
            "Buckmaster",
            "Elgindi",
            "Hou",
            "Miller",
            "Albritton",
            "Beirao-Berselli",
            "Chae",
            "Giga-Miura",
            "Jia",
            "Guillod",
            "Hou-Wang-Yang",
            "Lei-Ren-Tian",
            "CSTY",
            "Kozono-Taniuchi",
            "Neustupa-Penel",
            "Lin",
            "Vasseur",
            "Farwig",
            "Cheskidov",
            "Masmoudi",
            "Wolf",
            "Galdi",
            "Temam",
            "Isett",
            "Tsai",
            "Lemarie-Rieusset",
            "Danchin",
            "Kukavica",
            "Barker",
            "Robinson",
        }
        cross = [
            t
            for t in TURNS
            if t["speaker"] in living and living.intersection(t["to"])
        ]
        self.assertGreaterEqual(len(cross), 8)
        tao = next(t for t in TURNS if t["speaker"] == "Tao")
        self.assertEqual(tao["slot"], "B")
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertEqual(payload_open_count(), 1)

    def test_no_dead_fluids_in_living_room(self):
        dead = {"Leray", "Kato", "Majda", "Ladyzhenskaya", "Nirenberg", "Scheffer", "Sohr", "Foias", "Heywood"}
        self.assertTrue(dead.isdisjoint(set(SPEAKERS)))


def payload_open_count() -> int:
    return sum(1 for c in CLAIMS if c["verdict"] == "open")


if __name__ == "__main__":
    unittest.main()
