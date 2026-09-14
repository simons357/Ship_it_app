#!/usr/bin/env python3
"""VAL8000 humor + ElevenLabs mouth + Cosmic Graffiti desks, not a swarm."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CG = ROOT / "docs" / "cosmic-graffiti"
DOC = CG / "val8000.md"
NEWSROOM = CG / "NEWSROOM.md"
DESKS = CG / "desks.json"
SPEAK = ROOT / "scripts" / "val8000_speak.py"
NEWSROOM_PY = ROOT / "scripts" / "cg_newsroom.py"


class TestVal8000HumorAndMouth(unittest.TestCase):
    def test_terminator_and_skynet_are_jokes_not_a_ban(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Terminator", text)
        self.assertIn("Skynet", text)
        self.assertIn("I'll be back — after the footnote.", text)
        self.assertIn("He is **not** Skynet", text)
        self.assertIn("Idle mouth: a straight line.", text)
        self.assertIn("After he answers, he usually smiles.", text)
        self.assertIn("Metal teeth are rare.", text)
        self.assertNotIn("Smile when the joke earns it.", text)
        self.assertNotIn("not a terminator, not a skull", text.lower())

    def test_elevenlabs_never_falls_back_to_stock_tts(self) -> None:
        src = SPEAK.read_text(encoding="utf-8")
        self.assertNotIn("subprocess", src)
        self.assertNotIn("espeak", src)
        self.assertNotIn("pyttsx", src)
        self.assertIn("premade", src)
        env = os.environ.copy()
        env.pop("ELEVENLABS_API_KEY", None)
        env.pop("VAL8000_VOICE_ID", None)
        proc = subprocess.run(
            ["python3", str(SPEAK), "diagnose"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("ELEVENLABS_API_KEY", proc.stdout)
        self.assertIn("never spoke", proc.stdout.lower())


class TestNewsroomIsNotSkynet(unittest.TestCase):
    def test_roster_names_desks_and_refuses_the_swarm(self) -> None:
        roster = json.loads(DESKS.read_text(encoding="utf-8"))
        ids = {d["id"] for d in roster["desks"]}
        self.assertEqual(ids, {"frequency", "val8000", "ask", "cosmo", "humor"})
        self.assertTrue(roster["not_skynet"])
        self.assertTrue(roster["not_ten_thousand_agents"])
        self.assertIn("Saturday Night Live", roster["analogy"])
        self.assertEqual(roster["showrunner"], "Jonathan Simons")
        roles = {d["id"]: d["snl_role"] for d in roster["desks"]}
        self.assertEqual(roles["frequency"], "Weekend Update news")
        self.assertEqual(roles["val8000"], "Weekend Update jokes")
        news = NEWSROOM.read_text(encoding="utf-8").lower()
        self.assertIn("why", news)
        self.assertIn("parallel git branches", news)
        self.assertIn("ten thousand agents", news)

    def test_newsroom_cli_explains_the_failure(self) -> None:
        why = subprocess.run(
            ["python3", str(NEWSROOM_PY), "why"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Skynet stays a punchline", why.stdout)
        status = subprocess.run(
            ["python3", str(NEWSROOM_PY), "status"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertIn("VAL8000", status.stdout)
        self.assertIn("not Skynet", status.stdout)
        self.assertIn("val8000.md", status.stdout)
        self.assertIn("present", status.stdout)


class TestWritersRoomIsSNLNotSwarm(unittest.TestCase):
    def test_table_prints_weekend_update(self) -> None:
        proc = subprocess.run(
            ["python3", str(NEWSROOM_PY), "table"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Weekend Update jokes", proc.stdout)
        self.assertIn("private magazines", proc.stdout)
        self.assertIn("RUNDOWN.md", proc.stdout)

    def test_packet_is_jokes_after_news_not_closes(self) -> None:
        update = (CG / "writers-room" / "weekend-update.md").read_text(
            encoding="utf-8"
        )
        cold = (CG / "writers-room" / "cold-open.md").read_text(encoding="utf-8")
        room = (CG / "WRITERS-ROOM.md").read_text(encoding="utf-8")
        blob = "\n".join([update, cold]).lower()
        self.assertIn("weekend update", room.lower())
        self.assertIn("one rundown", room.lower())
        self.assertIn("coffee did not explode", update.lower())
        self.assertIn("nobody in those papers claimed 2", update.lower())
        self.assertIn("da-vc-01", update.lower())
        self.assertIn("fail", update.lower())
        self.assertNotIn("ns solved", blob)
        self.assertNotIn("rh is proved", blob)
        self.assertNotIn("riemann hypothesis is proved", blob)
        self.assertIn("be back", cold.lower())


if __name__ == "__main__":
    unittest.main()
