"""Contracts for LISTENER. No fake animals. No fake COH. Sharing != contributing."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = (ROOT / "app/js/contracts.js").read_text()
WILD = (ROOT / "app/js/wildlife.js").read_text()
APP = (ROOT / "app/js/app.js").read_text()
HTML = (ROOT / "app/index.html").read_text()
PROTO = (ROOT / "inbox/index.html").read_text()


class CoarseLocation(unittest.TestCase):
    def test_function_exists(self):
        self.assertIn("export function coarseLocation", JS)

    def test_grid_comment_is_coarse(self):
        self.assertIn("precision: \"coarse\"", JS)
        self.assertIn("11 km", JS)


class WildlifeOnly(unittest.TestCase):
    def test_no_transcribe(self):
        self.assertIn("Never transcribe", WILD)
        self.assertIn("mustNotTranscribe", WILD)

    def test_human_exclusion_kind(self):
        self.assertIn("probable_human_excluded", JS)
        self.assertIn("excludeProbableHuman", WILD)

    def test_contribute_requires_gate(self):
        self.assertIn("humanSpeechGate", JS)
        self.assertIn("Confirm this is not human speech", JS)

    def test_app_never_claims_species(self):
        self.assertNotIn("Barred Owl", APP)
        self.assertNotIn("Frog chorus", APP)
        self.assertNotIn("rain frog", APP.lower())
        self.assertIn("No invented animals", APP)
        self.assertIn("THIS IS THE FIRST SOUND", APP)
        self.assertIn("LISTEN TO THIS RAIN", APP)
        self.assertIn("LISTEN TO THIS RAIN", HTML)
        self.assertIn("THIS IS THE FIRST SOUND", HTML)
        self.assertIn("UNKNOWN stays UNKNOWN", HTML)
        self.assertIn("rain-cta", HTML)

    def test_first_sound_is_unknown_not_contributed(self):
        self.assertIn("firstSoundDecision", WILD)
        self.assertIn("saveFirstSound", APP)
        self.assertIn("rainFirstHTML", APP)
        self.assertIn("wantDoors", APP)
        self.assertIn("humanSpeechGate = \"pending\"", APP)
        self.assertIn("THIS IS NOT HUMAN SPEECH", APP)
        self.assertIn("This phone needs the microphone", JS)


class Coherence(unittest.TestCase):
    def test_insufficient_default(self):
        self.assertIn("INSUFFICIENT FIELD DATA", JS)
        self.assertIn('display: "—"', JS)

    def test_coherence_does_not_invent(self):
        self.assertIn("return { ...COH_INSUFFICIENT }", JS)


class SessionOffline(unittest.TestCase):
    def test_session_persisted(self):
        self.assertIn("listener.v1", (ROOT / "app/js/db.js").read_text())
        self.assertIn("emptySession", JS)

    def test_failure_language(self):
        self.assertIn("Scout connection lost. Still recording", JS)
        self.assertNotIn("Peer socket", APP)
        self.assertNotIn("route negotiation", APP)


class ShareVsContribute(unittest.TestCase):
    def test_distinct(self):
        self.assertIn("canShareCard", JS)
        self.assertIn("contributesOriginal: false", JS)
        self.assertIn("SHARE A CARD ONLY", APP)
        self.assertIn("CONTRIBUTE SAFELY", APP)


class PrototypePreserved(unittest.TestCase):
    def test_visual_tokens(self):
        css = (ROOT / "app/css/app.css").read_text()
        for token in ("#020504", "#7dffa5", "#82ddff", "#ffd176", "WHAT THE WILD IS SAYING"):
            self.assertIn(token, css + HTML)
        self.assertIn("GO SCOUT", HTML)
        self.assertIn("FIELD COHERENCE", HTML)
        self.assertIn("index.html", str(ROOT / "inbox/index.html"))

    def test_prototype_file_kept(self):
        self.assertIn("GO SCOUT", PROTO)
        self.assertIn("LISTENER SIGNAL LIBRARY", PROTO)


class SwiftContracts(unittest.TestCase):
    def test_swift_models_exist(self):
        models = (ROOT / "ios/Listener/Models.swift").read_text()
        for name in ("Session", "Breadcrumb", "FieldNote", "Encounter", "SyncEvent"):
            self.assertIn(f"class {name}", models)
        self.assertIn("probableHumanExcluded", models)
        self.assertIn("INSUFFICIENT FIELD DATA", models)
        self.assertIn("sharingIsNotContributing", models)
        self.assertIn("THIS IS THE FIRST SOUND", models)
        self.assertIn("LISTEN TO THIS RAIN", models)
        self.assertIn("This phone needs the microphone", models)


class ExecutableRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(ROOT / "hub"))
        from listener_core import (  # noqa: E402
            can_contribute,
            coarse_location,
            coherence_from_field,
            first_sound_decision,
            FAILURE_MIC_DENIED,
            FAILURE_SCOUT_LOST,
            process_signal,
        )

        cls.coarse_location = staticmethod(coarse_location)
        cls.process_signal = staticmethod(process_signal)
        cls.can_contribute = staticmethod(can_contribute)
        cls.coherence_from_field = staticmethod(coherence_from_field)
        cls.first_sound_decision = staticmethod(first_sound_decision)
        cls.FAILURE_SCOUT_LOST = FAILURE_SCOUT_LOST
        cls.FAILURE_MIC_DENIED = FAILURE_MIC_DENIED

    def test_coarse_location_grid(self):
        c = self.coarse_location(32.01234, -81.09876)
        self.assertEqual(c["lat"], 32.0)
        self.assertEqual(c["lon"], -81.1)
        self.assertEqual(c["precision"], "coarse")

    def test_human_speech_excluded_from_library(self):
        d = self.process_signal(probable_human_speech=True)
        self.assertFalse(d["createEncounter"])
        self.assertFalse(d["contribute"])
        self.assertIsNone(d["transcript"])
        self.assertIsNone(d["speakerId"])
        blocked = self.can_contribute({"kind": "probable_human_excluded", "excluded": True})
        self.assertFalse(blocked["ok"])

    def test_unknown_is_first_class(self):
        d = self.process_signal(probable_human_speech=False)
        self.assertTrue(d["createEncounter"])
        self.assertEqual(d["kind"], "unknown")
        self.assertIsNone(d["candidateSpecies"])

    def test_rain_first_sound_is_unknown_not_a_species(self):
        d = self.first_sound_decision("rain")
        self.assertTrue(d["createEncounter"])
        self.assertEqual(d["kind"], "unknown")
        self.assertEqual(d["label"], "rain")
        self.assertIsNone(d["candidateSpecies"])
        self.assertIsNone(d["transcript"])
        self.assertEqual(d["contribute"], "opt-in-after-confirm")
        pending = {"kind": "unknown", "label": "rain", "humanSpeechGate": "pending"}
        self.assertFalse(self.can_contribute(pending)["ok"])
        empty = self.first_sound_decision("")
        self.assertEqual(empty["label"], "UNKNOWN")

    def test_mic_denied_copy(self):
        self.assertIn("microphone to keep the original", self.FAILURE_MIC_DENIED)
        self.assertIn("session is still here", self.FAILURE_MIC_DENIED.lower())
        self.assertNotIn("getUserMedia", self.FAILURE_MIC_DENIED)
        self.assertNotIn("NotAllowedError", self.FAILURE_MIC_DENIED)

    def test_failure_copy(self):
        self.assertIn("Scout connection lost. Still recording", self.FAILURE_SCOUT_LOST)
        self.assertNotIn("peer socket", self.FAILURE_SCOUT_LOST.lower())
        self.assertNotIn("route negotiation", self.FAILURE_SCOUT_LOST.lower())

    def test_coherence_blank_without_sync(self):
        c = self.coherence_from_field([{"nearby": True, "synchronized": True}], 100, 0.2)
        self.assertEqual(c["display"], "—")
        self.assertFalse(c["computed"])


if __name__ == "__main__":
    unittest.main()
