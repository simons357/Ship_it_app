#!/usr/bin/env python3
"""Tests for AI Surgeon phone stills: identify, study, lab, trauma 07, twist."""

from __future__ import annotations

import unittest
from pathlib import Path

from ai_surgeon import screens_engine as eng

ROOT = Path(__file__).resolve().parents[1]
SURGEON = ROOT / "ai_surgeon"


class TestIdentifyBeforeCut(unittest.TestCase):
    def test_appendix_is_a_hit(self):
        result = eng.identify_touch(0.64, 0.74)
        self.assertEqual(result["state"], "HIT")
        self.assertEqual(result["grabbed"], "appendix")
        self.assertEqual(result["points"], 15)
        self.assertIn("SCALPEL", result["unlocks"])
        self.assertTrue(result["advance"])

    def test_cecum_is_a_named_miss(self):
        result = eng.identify_touch(0.50, 0.36)
        self.assertEqual(result["state"], "MISS")
        self.assertEqual(result["grabbed"], "cecum")
        self.assertEqual(result["points"], -5)
        self.assertIn("cecum", result["footer"].lower())
        self.assertFalse(result["advance"])
        self.assertEqual(result["unlocks"], ())

    def test_case_does_not_advance_on_field_miss(self):
        result = eng.identify_touch(0.02, 0.02)
        self.assertEqual(result["state"], "MISS")
        self.assertEqual(result["grabbed"], "field")
        self.assertFalse(result["advance"])


class TestStudySeeDo(unittest.TestCase):
    def test_venous_congestion_comes_first(self):
        hit = eng.grade_study_card(3, "B")
        self.assertTrue(hit["correct"])
        self.assertEqual(hit["points"], 10)
        miss = eng.grade_study_card(3, "A")
        self.assertFalse(miss["correct"])
        self.assertEqual(miss["points"], 0)

    def test_scrub_locked_until_four_cards(self):
        self.assertFalse(eng.study_gate(3)["scrub_unlocked"])
        self.assertTrue(eng.study_gate(4)["scrub_unlocked"])

    def test_name_before_divide(self):
        hit = eng.name_before_divide("mesoappendix")
        self.assertTrue(hit["correct"])
        self.assertTrue(hit["unlock_gesture"])
        self.assertEqual(hit["points"], 25)
        wrong = eng.name_before_divide("ileocolic")
        self.assertTrue(wrong["wrong_structure"])
        self.assertEqual(wrong["points"], -25)

    def test_gesture_locked_until_named(self):
        locked = eng.apply_gesture(False, "hold")
        self.assertFalse(locked["ok"])
        wrong = eng.apply_gesture(True, "swipe")
        self.assertFalse(wrong["ok"])
        ok = eng.apply_gesture(True, "hold")
        self.assertTrue(ok["ok"])
        self.assertEqual(ok["points"], 25)

    def test_hemostat_for_peritoneum(self):
        hit = eng.call_for_instrument("open_peritoneum", "hemostat")
        self.assertTrue(hit["correct"])
        miss = eng.call_for_instrument("open_peritoneum", "bovie")
        self.assertFalse(miss["correct"])
        self.assertEqual(miss["points"], -10)


class TestLabAndTwist(unittest.TestCase):
    def test_field_add_subtract_presets(self):
        self.assertEqual(eng.classify_lab(eng.lab_preset("FIELD")), "FIELD")
        self.assertEqual(eng.classify_lab(eng.lab_preset("ADD")), "ADD")
        self.assertEqual(eng.classify_lab(eng.lab_preset("SUBTRACT")), "SUBTRACT")
        self.assertIn("arteries", eng.lab_preset("ADD"))
        self.assertNotIn("peritoneum", eng.lab_preset("SUBTRACT"))

    def test_toggle_layer(self):
        on = eng.toggle_layer(eng.FIELD_LAYERS, "arteries")
        self.assertEqual(eng.classify_lab(on), "ADD")
        off = eng.toggle_layer(on, "arteries")
        self.assertEqual(eng.classify_lab(off), "FIELD")

    def test_twist_wraps_and_touch_commits(self):
        self.assertEqual(eng.twist_index(4, 1, 5), 0)
        self.assertEqual(eng.touch_commit(eng.NIB_TRAY, 2), "CLAMP")
        self.assertEqual(eng.airway_select(2), "ETT")
        self.assertEqual(eng.airway_select(3), "MASK")

    def test_legal_tray_hides_illegal_tools(self):
        legal = eng.legal_tray("ligate_the_base")
        self.assertIn("CLAMP", legal)
        self.assertNotIn("SPONGE", legal)
        self.assertEqual(eng.legal_tray("identify"), ())

    def test_propofol_too_fast(self):
        slow = eng.propofol_rate(0)
        self.assertFalse(slow["too_fast"])
        self.assertIn("2.0", slow["dose"])
        fast = eng.propofol_rate(1.4)
        self.assertTrue(fast["too_fast"])

    def test_verse_asymmetric(self):
        surg = eng.verse_view("surgeon")
        gas = eng.verse_view("anaesthesia")
        scrub = eng.verse_view("scrub")
        self.assertTrue(surg["sees_field"])
        self.assertFalse(surg["sees_numbers"])
        self.assertTrue(gas["sees_numbers"])
        self.assertFalse(gas["sees_field"])
        self.assertTrue(scrub["sees_both"])
        self.assertEqual(eng.verse_spin(0), "Lap chole")


class TestTraumaCase07(unittest.TestCase):
    def test_coherence_runs_the_clock(self):
        slow = eng.TraumaCase07(coherence=0)
        fast = eng.TraumaCase07(coherence=100)
        self.assertAlmostEqual(slow.arrest_deadline(), 78.0)
        self.assertAlmostEqual(fast.arrest_deadline(), 56.0)
        self.assertLess(fast.arrest_deadline(), slow.arrest_deadline())

    def test_needle_buys_time_tube_is_definitive_fluid_is_wrong(self):
        case = eng.TraumaCase07(coherence=44, elapsed=0)
        base = case.remaining()
        needled = case.act("needle")
        self.assertGreater(needled.remaining(), base)
        self.assertFalse(needled.tube)
        tubed = needled.act("tube")
        self.assertTrue(tubed.tube)
        self.assertFalse(tubed.dead)
        fluid = eng.TraumaCase07(coherence=44).act("fluid")
        self.assertLess(fluid.points, 590)
        self.assertIn("obstructive", fluid.notes[-1].lower())

    def test_death_voids_score(self):
        case = eng.TraumaCase07(coherence=100, elapsed=0)
        dead = case.step(case.arrest_deadline() + 1)
        self.assertTrue(dead.dead)
        self.assertEqual(dead.points, 0)

    def test_errors_first_time_breaks_ties(self):
        self.assertEqual(eng.errors_first(1, 9 * 60 + 12, 4, 8 * 60 + 4), "a")
        self.assertEqual(eng.errors_first(1, 100, 1, 90), "b")
        self.assertEqual(eng.errors_first(2, 10, 2, 10), "tie")


class TestHubAndArtifacts(unittest.TestCase):
    def test_sixteen_stills_present(self):
        stills = SURGEON / "stills"
        names = [
            "01-anesthesia-pen.png",
            "02-art-fidelity.png",
            "03-hardware-ladder.png",
            "04-identify-before-you-cut.png",
            "05-cecum-appendix-a.png",
            "06-cecum-appendix-b.png",
            "07-surgery-verse.png",
            "08-tablet-pencil-mat.png",
            "09-the-lab.png",
            "10-twist-stylus.png",
            "11-the-nib.png",
            "12-study-one.png",
            "13-see-one.png",
            "14-do-one.png",
            "15-call-for-instrument.png",
            "16-trauma-pneumo.png",
        ]
        for name in names:
            path = stills / name
            self.assertTrue(path.is_file(), name)
            self.assertGreater(path.stat().st_size, 8_000, name)

    def test_mockups_and_brochure_generated(self):
        gen = SURGEON / "generators"
        for name in [
            "screen-01-study-one.png",
            "screen-02-see-one.png",
            "screen-03-do-one-decision.png",
            "screen-04-scrub-tech.png",
            "screen-05-trauma-vitals.png",
            "screen-06-teach-one.png",
            "AI-Surgeon-Brochure.pdf",
            "brochure.py",
            "mockups.py",
        ]:
            self.assertTrue((gen / name).is_file(), name)
        pdf = (gen / "AI-Surgeon-Brochure.pdf").read_bytes()
        self.assertTrue(pdf.startswith(b"%PDF"))

    def test_hub_links_screens_not_replacing_trauma(self):
        hub = (SURGEON / "index.html").read_text(encoding="utf-8")
        screens = (SURGEON / "screens.html").read_text(encoding="utf-8")
        self.assertIn("screens.html", hub)
        self.assertIn("ai-surgeon-module02-trauma.html", hub)
        self.assertIn("ai-surgeon-prototype.html", hub)
        self.assertIn("#identify", hub)
        self.assertIn("#lab", hub)
        self.assertIn("#verse", hub)
        self.assertIn("#anesthesia", hub)
        self.assertIn("pen.html", hub)
        self.assertIn("Not a medical device", hub)
        self.assertIn("phone.js", screens)

    def test_playable_routes_in_phone_js(self):
        js = (SURGEON / "phone.js").read_text(encoding="utf-8")
        for route in (
            "identify", "lab", "study", "see", "do", "call",
            "anesthesia", "nib", "verse", "trauma", "anatomy", "pen",
        ):
            self.assertIn(route, js)

    def test_serve_still_binds_loopback(self):
        from ai_surgeon.serve import public_path, PREFIX
        self.assertEqual(public_path("/"), "index.html")
        self.assertEqual(public_path(PREFIX + "/screens.html"), "screens.html")
        self.assertEqual(public_path("/stills/06-cecum-appendix-b.png"), "stills/06-cecum-appendix-b.png")


if __name__ == "__main__":
    unittest.main()
