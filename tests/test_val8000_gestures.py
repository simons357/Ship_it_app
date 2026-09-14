#!/usr/bin/env python3
"""VAL8000 gestures: insult is tongue, bored is inhale then puff-bag."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import val8000_gestures as gestures  # noqa: E402

CG = ROOT / "docs" / "cosmic-graffiti"
ASSETS = CG / "assets"
SPEC = CG / "val8000-gestures.md"
CATALOG = CG / "val8000-gestures.json"
GUIDE = CG / "val8000.md"
SKINS_JSON = ASSETS / "skins" / "skins.json"
LIVE_PY = ROOT / "domain_architect"

INHALE = ASSETS / "val8000-gesture-inhale.png"
PUFF = ASSETS / "val8000-gesture-puff-bag.png"
TONGUE = ASSETS / "val8000-gesture-tongue-out.png"
LINE = ASSETS / "val8000-mouth-line.png"
SMILE = ASSETS / "val8000-mouth-smile.png"
TEETH = ASSETS / "val8000-mouth-teeth.png"


class TestGestureStills(unittest.TestCase):
    def test_three_original_stills_exist(self) -> None:
        for path in (INHALE, PUFF, TONGUE):
            self.assertTrue(path.is_file(), path.name)
            self.assertGreater(path.stat().st_size, 20_000, path.name)

    def test_stills_are_not_the_mouth_pack(self) -> None:
        mouths = {LINE.read_bytes(), SMILE.read_bytes(), TEETH.read_bytes()}
        self.assertNotEqual(INHALE.read_bytes(), PUFF.read_bytes())
        self.assertNotEqual(PUFF.read_bytes(), TONGUE.read_bytes())
        self.assertNotEqual(INHALE.read_bytes(), TONGUE.read_bytes())
        for path in (INHALE, PUFF, TONGUE):
            self.assertNotIn(path.read_bytes(), mouths, path.name)


class TestGestureSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = SPEC.read_text(encoding="utf-8")
        cls.guide = GUIDE.read_text(encoding="utf-8")

    def test_lock_sentences(self) -> None:
        spec = self.spec
        self.assertIn("Gestures are not skins.", spec)
        self.assertIn("Insult is the tongue, not teeth.", spec)
        self.assertIn("Bored is inhale then puff-bag, not idle rest.", spec)
        self.assertIn("Masthead is the un-puffed idle line.", spec)
        self.assertIn("Masthead never uses the tongue.", spec)
        self.assertIn("Masthead never uses the puff-bag.", spec)
        self.assertIn("He types in the box. No TTS.", spec)
        self.assertIn("Idle is a straight line.", spec)
        self.assertIn("Normal answer is a smile.", spec)
        self.assertIn("Teeth are compliment, funny joke, or sarcasm.", spec)

    def test_jon_bits_and_stills(self) -> None:
        spec = self.spec
        self.assertIn("takes a deep breath in", spec)
        self.assertIn("puffs up like a big puffy bag", spec)
        self.assertIn("sticks his tongue out", spec)
        self.assertIn("val8000-gesture-inhale.png", spec)
        self.assertIn("val8000-gesture-puff-bag.png", spec)
        self.assertIn("val8000-gesture-tongue-out.png", spec)
        self.assertIn("Do not write these plays into `assets/skins/skins.json`.", spec)

    def test_no_product_name_no_tts_no_clay(self) -> None:
        blob = self.spec + "\n" + CATALOG.read_text(encoding="utf-8")
        self.assertNotIn("HAL 9000", blob)
        self.assertNotIn("HAL9000", blob)
        self.assertNotIn("I'm sorry Dave", blob)
        self.assertNotIn("Clay", blob)
        src = (ROOT / "scripts" / "val8000_gestures.py").read_text(encoding="utf-8")
        for banned in (
            "speechSynthesis",
            "elevenlabs",
            "espeak",
            "pyttsx",
            "subprocess",
            "new Audio",
        ):
            self.assertNotIn(banned, src)

    def test_pointer_does_not_clobber_mouth_timing(self) -> None:
        guide = self.guide
        self.assertIn("val8000-gestures.md", guide)
        self.assertIn("Teeth when someone compliments him.", guide)
        self.assertIn("Teeth when he tells a funny joke.", guide)
        self.assertIn("Teeth when he uses sarcasm.", guide)
        self.assertIn("Idle mouth: a straight line.", guide)
        self.assertIn("After he answers, he usually smiles.", guide)


class TestGestureMappings(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_catalog_is_not_skins(self) -> None:
        cat = self.catalog
        self.assertTrue(cat["not_skins"])
        self.assertTrue(cat["types_in_the_box"])
        self.assertTrue(cat["no_tts"])
        self.assertEqual(cat["mouth_timing_file"], "val8000.md")
        self.assertIn("assets/skins/skins.json", cat["do_not_overwrite"])
        if SKINS_JSON.is_file():
            skins = json.loads(SKINS_JSON.read_text(encoding="utf-8"))
            ids = {row["id"] for row in skins.get("skins", [])}
            for gesture in ("inhale", "puff-bag", "tongue-out", "bored", "insult"):
                self.assertNotIn(gesture, ids)
            self.assertNotIn("gesture", json.dumps(skins).lower())

    def test_intent_table(self) -> None:
        expected = {
            "idle": ("mouth", ("line",), True),
            "normal_answer": ("mouth", ("smile",), False),
            "compliment": ("mouth", ("teeth",), False),
            "funny_joke": ("mouth", ("teeth",), False),
            "sarcasm": ("mouth", ("teeth",), False),
            "insult": ("gesture", ("tongue-out",), False),
            "bored": ("gesture", ("inhale", "puff-bag"), False),
            "masthead": ("mouth", ("line",), True),
        }
        for intent, (channel, frames, masthead_ok) in expected.items():
            play = gestures.play_for(intent)
            self.assertEqual(play.channel, channel, intent)
            self.assertEqual(play.frames, frames, intent)
            self.assertEqual(play.masthead_ok, masthead_ok, intent)

    def test_insult_is_tongue_not_teeth(self) -> None:
        play = gestures.play_for("insult")
        self.assertEqual(play.frames, ("tongue-out",))
        self.assertEqual(play.channel, "gesture")
        self.assertNotIn("teeth", play.frames)
        self.assertIn("teeth", play.forbidden)
        self.assertTrue(play.assets[0].endswith("val8000-gesture-tongue-out.png"))

    def test_bored_is_inhale_then_puff_not_idle(self) -> None:
        play = gestures.play_for("bored")
        self.assertEqual(play.frames, ("inhale", "puff-bag"))
        self.assertEqual(gestures.describe(play), "inhale then puff-bag")
        self.assertNotIn("line", play.frames)
        self.assertNotIn("idle", play.frames)
        self.assertIn("idle", play.forbidden)
        self.assertFalse(play.masthead_ok)

    def test_masthead_never_tongue_or_bag(self) -> None:
        play = gestures.play_for("masthead")
        self.assertEqual(play.frames, ("line",))
        self.assertTrue(play.masthead_ok)
        for banned in ("tongue-out", "puff-bag", "inhale"):
            self.assertNotIn(banned, play.frames)
            self.assertIn(banned, play.forbidden)

    def test_teeth_triggers_stay_on_the_mouth_channel(self) -> None:
        for intent in ("compliment", "funny_joke", "sarcasm", "joke"):
            play = gestures.play_for(intent)
            self.assertEqual(play.frames, ("teeth",), intent)
            self.assertEqual(play.channel, "mouth", intent)

    def test_classify_typed_lines(self) -> None:
        self.assertEqual(gestures.classify_utterance("you are an idiot"), "insult")
        self.assertEqual(gestures.classify_utterance("shut up VAL"), "insult")
        self.assertEqual(gestures.classify_utterance("this is boring"), "bored")
        self.assertEqual(gestures.classify_utterance("", bored=True), "bored")
        self.assertEqual(gestures.classify_utterance("nice work"), "compliment")
        self.assertEqual(gestures.classify_utterance("tell a funny joke"), "funny_joke")
        self.assertEqual(gestures.classify_utterance("yeah right"), "sarcasm")
        self.assertEqual(gestures.classify_utterance("what is Q1"), "normal_answer")
        self.assertEqual(gestures.classify_utterance(""), "idle")
        self.assertEqual(
            gestures.classify_utterance("you are an idiot", masthead=True),
            "masthead",
        )

    def test_insult_beats_bored_and_masthead_beats_insult(self) -> None:
        self.assertEqual(
            gestures.classify_utterance("you stupid boring lamp"),
            "insult",
        )
        play = gestures.play_for_utterance("you suck", masthead=True)
        self.assertEqual(play.intent, "masthead")
        self.assertEqual(play.frames, ("line",))

    def test_cli_map(self) -> None:
        insult = subprocess.run(
            ["python3", str(ROOT / "scripts" / "val8000_gestures.py"), "map", "insult"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("tongue-out", insult.stdout)
        bored = subprocess.run(
            ["python3", str(ROOT / "scripts" / "val8000_gestures.py"), "map", "bored"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("inhale then puff-bag", bored.stdout)

    def test_live_da_python_still_does_not_import_val8000(self) -> None:
        for path in LIVE_PY.rglob("*.py"):
            blob = path.read_text(encoding="utf-8")
            self.assertNotIn("val8000", blob)
            self.assertNotIn("VAL8000", blob)


if __name__ == "__main__":
    unittest.main()
