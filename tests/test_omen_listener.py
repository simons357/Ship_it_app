#!/usr/bin/env python3
"""Listener, offline merge, and the OMEN shelter clock."""

from __future__ import annotations

import json
import math
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from omen_listener.demo import demo_picture, demo_state
from omen_listener.detect import azimuth_from_pair, rotor_cue
from omen_listener.notes import smart_field_note
from omen_listener.geo import compass_deg, to_geo
from omen_listener.picture import SHELTER_WORDS, build_picture
from omen_listener.session import GeoPoint, ListenerSession


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = (40.0, -74.0)


def stack(sample_rate: int, count: int, freq: float, amps=(1.0, 0.55, 0.32)) -> list[float]:
    samples = []
    for i in range(count):
        samples.append(
            sum(amp * math.sin(2.0 * math.pi * (k + 1) * freq * i / sample_rate) for k, amp in enumerate(amps))
        )
    return samples


def shift(samples: list[float], delay_samples: float) -> list[float]:
    out = []
    last = len(samples) - 1
    for i in range(len(samples)):
        x = i - delay_samples
        if x <= 0.0 or x >= last:
            out.append(0.0)
            continue
        i0 = int(math.floor(x))
        frac = x - i0
        out.append(samples[i0] * (1.0 - frac) + samples[i0 + 1] * frac)
    return out


def cue(node_id: str, kind: str, east: float, north: float, t: float, threat: tuple[float, float], sigma: float) -> dict:
    lat, lon = to_geo(east, north, ORIGIN[0], ORIGIN[1])
    return {
        "node_id": node_id,
        "kind": kind,
        "t": t,
        "lat": lat,
        "lon": lon,
        "score": 0.9,
        "azimuth_deg": compass_deg(threat[0] - east, threat[1] - north),
        "azimuth_sigma_deg": sigma,
        "community_id": "c",
        "alert_id": "a",
    }


def picture_from(observations: list[dict], now: float, **extra) -> dict:
    state = {
        "community_id": "c",
        "alert_id": "a",
        "protected": {"lat": ORIGIN[0], "lon": ORIGIN[1], "label": "block"},
        "now": now,
        "listening": True,
        "observations": observations,
    }
    state.update(extra)
    return build_picture(state)


def track_pair(sigma: float = 1.0) -> list[dict]:
    west_east = ((-400.0, 0.0), (400.0, 0.0))
    observations = []
    for t, threat in ((1000.0, (0.0, 1600.0)), (1005.0, (0.0, 1500.0))):
        for index, (east, north) in enumerate(west_east):
            node_id = "west" if index == 0 else "east"
            observations.append(cue(node_id, "treetop", east, north, t, threat, sigma))
    return observations


class TestDetector(unittest.TestCase):
    def test_harmonic_stack_detected_and_lookalikes_rejected(self):
        rate, count = 16000, 2048
        clean = rotor_cue(stack(rate, count, 140.0), rate)
        weak = rotor_cue(stack(rate, count, 140.0, (1.0, 0.25, 0.12)), rate)
        tone = rotor_cue([math.sin(2.0 * math.pi * 140.0 * i / rate) for i in range(count)], rate)
        noise = rotor_cue([random.Random(1).uniform(-1.0, 1.0) for _ in range(count)], rate)
        self.assertTrue(clean.detected)
        self.assertEqual(clean.fundamental_hz, 140.0)
        self.assertGreaterEqual(clean.score, 0.45)
        self.assertTrue(weak.detected)
        self.assertFalse(tone.detected)
        self.assertFalse(noise.detected)

    def test_short_frame_rejected(self):
        cue_result = rotor_cue([0.0] * 100, 16000)
        self.assertFalse(cue_result.detected)
        self.assertEqual(cue_result.detail, "frame too short")

    def test_pair_bearing(self):
        rate = 16000
        rng = random.Random(2)
        base = [rng.uniform(-1.0, 1.0) * math.exp(-((i - 2000) / 400.0) ** 2) for i in range(4096)]
        spacing = 0.20
        for phi, heading in ((30.0, 0.0), (-20.0, 90.0)):
            delay_s = -spacing * math.sin(math.radians(phi)) / 343.0
            right = shift(base, delay_s * rate)
            azimuth = azimuth_from_pair(base, right, rate, spacing, heading)
            expected = (heading + phi) % 360.0
            self.assertIsNotNone(azimuth)
            error = (azimuth - expected + 180.0) % 360.0 - 180.0
            self.assertLess(abs(error), 3.0)


class TestWindow(unittest.TestCase):
    def test_track_opens_conservative_clock(self):
        pic = picture_from(track_pair(), 1005.0)
        omen = pic["omen"]
        self.assertTrue(omen["open"])
        self.assertEqual(omen["urgency"], "move")
        self.assertAlmostEqual(omen["heading_deg"], 180.0, delta=2.0)
        self.assertAlmostEqual(omen["speed_m_s"], 20.0, delta=1.0)
        self.assertAlmostEqual(omen["threat"]["north_m"], 1500.0, delta=30.0)
        self.assertIn("1.5 km", omen["where"])
        self.assertIn("north", omen["where"])
        self.assertIn("Move inside", omen["guidance"])
        conservative = omen["time_to_closest_s"] - omen["time_uncertainty_s"]
        self.assertEqual(omen["decision_seconds"], math.floor(conservative - omen["lead_s"]))
        self.assertGreater(omen["decision_seconds"], 20)
        self.assertEqual(pic["comms"], "local")
        self.assertFalse(pic["stale"])
        self.assertTrue(any(layer["type"] == "decision" for layer in pic["layers"]))

    def test_hover_is_visible_and_window_stays_closed(self):
        observations = []
        for t in (1000.0, 1006.0):
            observations.extend(
                [
                    cue("west", "treetop", -300.0, 0.0, t, (0.0, 500.0), 1.0),
                    cue("east", "treetop", 300.0, 0.0, t, (0.0, 500.0), 1.0),
                ]
            )
        pic = picture_from(observations, 1006.0)
        self.assertFalse(pic["omen"]["open"])
        self.assertEqual(pic["omen"]["reason"], "no_trajectory")
        self.assertTrue(pic["contact"]["visible"])
        self.assertTrue(pic["contact"]["placed"])
        self.assertIsNone(pic["omen"]["decision_seconds"])

    def test_receding_and_wide_miss_stay_closed(self):
        receding = []
        for t, threat in ((1000.0, (0.0, 700.0)), (1005.0, (0.0, 900.0))):
            receding.append(cue("west", "treetop", -300.0, 0.0, t, threat, 1.0))
            receding.append(cue("east", "treetop", 300.0, 0.0, t, threat, 1.0))
        pic = picture_from(receding, 1005.0)
        self.assertFalse(pic["omen"]["open"])
        self.assertEqual(pic["omen"]["reason"], "receding")
        self.assertTrue(pic["contact"]["visible"])

        wide = []
        for t, threat in ((1000.0, (-150.0, 2200.0)), (1005.0, (0.0, 2200.0))):
            wide.append(cue("west", "treetop", -300.0, 0.0, t, threat, 1.0))
            wide.append(cue("east", "treetop", 300.0, 0.0, t, threat, 1.0))
        pic = picture_from(wide, 1005.0)
        self.assertEqual(pic["omen"]["reason"], "wide_miss")
        self.assertFalse(pic["omen"]["open"])
        self.assertTrue(pic["contact"]["placed"])

    def test_parallel_bearings_and_single_ray(self):
        parallel = [
            cue("west", "phone", -200.0, 0.0, 1000.0, (0.0, 400.0), 1.0),
            cue("east", "phone", 200.0, 0.0, 1000.0, (0.0, 400.0), 1.0),
        ]
        parallel[0]["azimuth_deg"] = 0.0
        parallel[1]["azimuth_deg"] = 0.0
        pic = picture_from(parallel, 1000.0)
        self.assertEqual(pic["omen"]["reason"], "weak_geometry")
        self.assertFalse(pic["omen"]["open"])
        self.assertTrue(any(layer["type"] == "bearing" for layer in pic["layers"]))

        one = [cue("only", "treetop", 0.0, 0.0, 1000.0, (0.0, 800.0), 1.0)]
        pic = picture_from(one, 1000.0)
        self.assertEqual(pic["omen"]["reason"], "no_trajectory")
        self.assertFalse(pic["contact"]["placed"])
        self.assertEqual(pic["contact"]["where"], "heard, not placed yet")

        heard = [dict(one[0])]
        heard[0]["azimuth_deg"] = None
        pic = picture_from(heard, 1000.0)
        self.assertEqual(pic["omen"]["reason"], "no_bearing")
        self.assertIn("which listener", pic["omen"]["guidance"])

    def test_large_circle_does_not_invent_a_clock(self):
        pic = picture_from(track_pair(sigma=25.0), 1005.0)
        self.assertFalse(pic["omen"]["open"])
        self.assertEqual(pic["omen"]["reason"], "weak_geometry")
        self.assertTrue(pic["contact"]["placed"])
        self.assertIn("too large", pic["omen"]["guidance"])

    def test_comms_down_projects_then_caps(self):
        fresh = picture_from(track_pair(), 1005.0)
        later = picture_from(track_pair(), 1020.0)
        capped = picture_from(track_pair(), 1085.0)
        self.assertEqual(later["comms"], "down")
        self.assertTrue(later["stale"])
        self.assertTrue(later["omen"]["clock_estimated"])
        self.assertLess(later["omen"]["decision_seconds"], fresh["omen"]["decision_seconds"])
        self.assertAlmostEqual(later["omen"]["threat"]["north_m"], 1200.0, delta=40.0)
        self.assertEqual(capped["omen"]["extrapolated_s"], 45.0)
        self.assertAlmostEqual(capped["omen"]["threat"]["north_m"], 600.0, delta=40.0)
        self.assertEqual(capped["omen"]["urgency"], "shelter_now")
        self.assertEqual(capped["omen"]["decision_seconds"], 0)
        again = picture_from(track_pair(), 1100.0)
        self.assertEqual(again["omen"]["extrapolated_s"], 45.0)
        self.assertAlmostEqual(again["omen"]["threat"]["north_m"], capped["omen"]["threat"]["north_m"], delta=1.0)

    def test_guidance_stays_on_shelter(self):
        pictures = [
            picture_from(track_pair(), 1005.0),
            picture_from([], 1005.0),
            picture_from([], 1005.0, listening=False),
            demo_picture(1005.0),
            demo_picture(1020.0),
        ]
        for pic in pictures:
            text = pic["omen"]["guidance"].lower()
            for banned in SHELTER_WORDS:
                self.assertNotIn(banned, text)


class TestSessionAndMesh(unittest.TestCase):
    def _session(self, token: str | None = None) -> ListenerSession:
        return ListenerSession(
            "north-oak",
            GeoPoint(40.0, -74.0),
            community_token=token,
            label="north oak",
        )

    def test_wearable_wake_gates_the_microphone(self):
        session = self._session()
        node = {"node_id": "phone-1", "kind": "phone", "lat": 40.0, "lon": -74.0}
        samples = stack(16000, 2048, 140.0)
        self.assertIsNone(session.ingest_pcm(node, samples, 16000, 950.0, azimuth_deg=10.0))
        self.assertFalse(
            session.apply_wake(
                {"community_id": "other", "alert_id": "x", "command": "listen", "issued_at": 900.0},
                950.0,
            )
        )
        self.assertTrue(
            session.apply_wake(
                {
                    "community_id": "north-oak",
                    "alert_id": "alert-1",
                    "command": "listen",
                    "issued_at": 900.0,
                    "ttl_s": 100.0,
                    "source": "wearable",
                },
                950.0,
            )
        )
        heard = session.ingest_pcm(node, samples, 16000, 950.0, azimuth_deg=12.0)
        self.assertIsNotNone(heard)
        self.assertAlmostEqual(heard["fundamental_hz"], 140.0, delta=5.0)
        self.assertIsNone(session.ingest_pcm(node, [random.Random(3).uniform(-1, 1) for _ in range(2048)], 16000, 951.0))
        self.assertFalse(session.listening(1100.0))
        self.assertIsNone(session.ingest_pcm(node, samples, 16000, 1100.0, azimuth_deg=12.0))
        session.apply_wake(
            {"community_id": "north-oak", "alert_id": "alert-1", "command": "listen", "issued_at": 1100.0, "ttl_s": 50},
            1110.0,
        )
        self.assertTrue(session.listening(1110.0))
        self.assertFalse(
            session.apply_wake(
                {"community_id": "north-oak", "alert_id": "alert-1", "command": "stop", "issued_at": 1110.0},
                1110.0,
            )
        )

    def test_bundles_merge_offline_and_ignore_other_groups(self):
        session = self._session(token="oak")

        def local(obs: dict) -> dict:
            stamped = dict(obs)
            stamped["community_id"] = "north-oak"
            stamped["alert_id"] = "alert-1"
            return stamped

        first = {
            "type": "omen.bundle",
            "community_id": "north-oak",
            "alert_id": "alert-1",
            "community_token": "oak",
            "observations": [local(cue("west", "treetop", -100.0, 0.0, 1000.0, (0.0, 400.0), 3.0))],
        }
        self.assertEqual(session.ingest_bundle(first), 1)
        self.assertEqual(session.ingest_bundle(first), 0)
        other = dict(first)
        other["community_id"] = "south-oak"
        self.assertEqual(session.ingest_bundle(other), 0)
        wrong = dict(first)
        wrong["community_token"] = "nope"
        wrong["observations"] = [local(cue("east", "treetop", 100.0, 0.0, 1000.0, (0.0, 400.0), 3.0))]
        self.assertEqual(session.ingest_bundle(wrong), 0)
        second = dict(first)
        second["observations"] = [local(cue("east", "treetop", 100.0, 0.0, 1000.0, (0.0, 400.0), 3.0))]
        self.assertEqual(session.ingest_bundle(second), 1)
        exported = session.export_bundle("phone-1", 1001.0)
        self.assertEqual(exported["type"], "omen.bundle")
        self.assertEqual(len(exported["observations"]), 2)
        self.assertNotIn("socket", json.dumps(exported))

    def test_tree_line_uses_several_systems(self):
        fresh = demo_picture(1005.0)
        later = demo_picture(1020.0)
        self.assertEqual(fresh["systems"], ["phone", "treetop", "wearable"])
        self.assertEqual(fresh["opened_by"], "wearable")
        self.assertTrue(fresh["omen"]["open"])
        self.assertEqual(fresh["comms"], "local")
        self.assertIn("north", fresh["omen"]["where"])
        self.assertEqual(later["comms"], "down")
        self.assertLess(later["omen"]["decision_seconds"], fresh["omen"]["decision_seconds"])
        self.assertTrue(any(item["kind"] == "treetop" and item.get("alt_m") == 14.0 for item in fresh["listeners"]))

    def test_cli_reads_state_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            state = {
                "community_id": "c",
                "alert_id": "a",
                "protected": {"lat": 40.0, "lon": -74.0},
                "now": 1005.0,
                "listening": True,
                "observations": track_pair(),
            }
            path.write_text(json.dumps(state), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "omen_listener", "picture", "--state", str(path), "--now", "1020"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
        pic = json.loads(proc.stdout)
        self.assertEqual(pic["comms"], "down")
        self.assertTrue(pic["omen"]["open"])

    def test_committed_overlay_matches_builder(self):
        disk = json.loads((ROOT / "omen_listener" / "overlay" / "picture.json").read_text(encoding="utf-8"))
        live = demo_picture(1005.0)
        self.assertEqual(disk["omen"]["decision_seconds"], live["omen"]["decision_seconds"])
        self.assertEqual(disk["omen"]["guidance"], live["omen"]["guidance"])
        later = json.loads((ROOT / "omen_listener" / "overlay" / "picture_later.json").read_text(encoding="utf-8"))
        self.assertEqual(later["comms"], "down")
        self.assertEqual(later["omen"]["decision_seconds"], demo_picture(1020.0)["omen"]["decision_seconds"])


class TestCoherenceAndNotes(unittest.TestCase):
    def test_tree_line_locks_the_field(self):
        pic = demo_picture(1005.0)
        self.assertEqual(pic["coherence"]["state"], "locked")
        self.assertEqual(pic["coherence"]["label"], "Field locked")
        self.assertEqual(pic["coherence"]["lit"], [item["node_id"] for item in pic["listeners"]])
        self.assertTrue(all(item["coherent"] for item in pic["listeners"]))
        self.assertEqual(pic["coherence"]["value"], 1.0)

    def test_quiet_field_stays_dark(self):
        pic = picture_from([], 1005.0)
        self.assertEqual(pic["coherence"]["state"], "quiet")
        self.assertEqual(pic["coherence"]["lit"], [])
        self.assertEqual(pic["coherence"]["value"], 0.0)

    def test_one_listener_is_partial(self):
        heard = [cue("only", "phone", 0.0, 0.0, 1000.0, (0.0, 400.0), 8.0)]
        pic = picture_from(heard, 1000.0)
        self.assertEqual(pic["coherence"]["state"], "partial")
        self.assertEqual(pic["coherence"]["lit"], ["only"])
        self.assertTrue(pic["listeners"][0]["coherent"])

    def test_stale_listener_is_not_lit(self):
        late = cue("late", "phone", 0.0, -100.0, 980.0, (0.0, 200.0), 8.0)
        late["azimuth_deg"] = None
        pic = picture_from(track_pair() + [late], 1005.0)
        self.assertEqual(pic["coherence"]["state"], "locked")
        self.assertIn("west", pic["coherence"]["lit"])
        self.assertNotIn("late", pic["coherence"]["lit"])
        stale = next(item for item in pic["listeners"] if item["node_id"] == "late")
        self.assertFalse(stale["coherent"])

    def test_smart_note_sends_in_one_line_and_clicks_off(self):
        session = ListenerSession("north-oak", GeoPoint(40.0, -74.0), community_token="oak")
        picture = demo_picture(1005.0)
        expected = smart_field_note(picture, node_id="phone-maple", t=1005.0)
        self.assertEqual(
            expected["text"],
            f"{picture['omen']['decision_seconds']}s · {picture['omen']['where']} · field locked",
        )
        self.assertNotIn("\n", expected["text"])
        note = session.send_smart("phone-maple", 1005.0)
        self.assertEqual(note["status"], "sent")
        self.assertEqual(note["text"], "field quiet")
        preset = session.send_preset("inside", "phone-maple", 1004.0)
        self.assertEqual(preset["text"], "Inside")
        exported = session.export_bundle("phone-maple", 1005.0)
        self.assertEqual(len(exported["field_notes"]), 2)
        other = ListenerSession("north-oak", GeoPoint(40.0, -74.0), community_token="oak")
        other.ingest_bundle(exported)
        self.assertEqual([item["text"] for item in other.field_notes()], ["Inside", note["text"]])
        self.assertTrue(all(item["status"] == "received" for item in other.field_notes()))
        other.click_off(note["id"])
        other.ingest_bundle(exported)
        self.assertEqual([item["text"] for item in other.field_notes()], ["Inside"])
        session.click_off(note["id"])
        session.click_off(preset["id"])
        self.assertEqual(session.field_notes(), [])
        self.assertEqual(session.export_bundle("phone-maple", 1005.0)["field_notes"], [])


class TestJavaScriptPort(unittest.TestCase):
    def test_node_port_matches_python(self):
        fresh = demo_picture(1005.0)
        later = demo_picture(1020.0)
        samples = stack(16000, 2048, 140.0)
        payload = {
            "picture": demo_state(1005.0),
            "later": demo_state(1020.0),
            "samples": samples,
            "sampleRate": 16000,
            "bundles": [
                {
                    "type": "omen.bundle",
                    "community_id": "north-oak",
                    "alert_id": "alert-1",
                    "community_token": "oak",
                    "observations": [cue("west", "treetop", -10.0, 0.0, 1000.0, (0.0, 100.0), 3.0)],
                },
                {
                    "type": "omen.bundle",
                    "community_id": "north-oak",
                    "alert_id": "alert-1",
                    "community_token": "oak",
                    "observations": [cue("west", "treetop", -10.0, 0.0, 1000.0, (0.0, 100.0), 3.0)],
                },
                {
                    "type": "omen.bundle",
                    "community_id": "other",
                    "alert_id": "alert-1",
                    "community_token": "oak",
                    "observations": [cue("east", "treetop", 10.0, 0.0, 1000.0, (0.0, 100.0), 3.0)],
                },
            ],
        }
        # The cue helper stamps community "c". The duplicate west observation
        # still merges to one because the bundle community check happens first
        # and the observation community is then rejected... stamp it.
        for bundle in payload["bundles"]:
            if bundle["community_id"] != "north-oak":
                continue
            for obs in bundle["observations"]:
                obs["community_id"] = "north-oak"
                obs["alert_id"] = "alert-1"
        proc = subprocess.run(
            ["node", str(ROOT / "tests" / "js_parity.js")],
            input=json.dumps(payload),
            check=True,
            capture_output=True,
            text=True,
        )
        out = json.loads(proc.stdout)
        self.assertEqual(out["picture"]["omen"]["decision_seconds"], fresh["omen"]["decision_seconds"])
        self.assertEqual(out["picture"]["omen"]["urgency"], fresh["omen"]["urgency"])
        self.assertEqual(out["picture"]["omen"]["where"], fresh["omen"]["where"])
        self.assertEqual(out["picture"]["omen"]["guidance"], fresh["omen"]["guidance"])
        self.assertEqual(out["picture"]["comms"], fresh["comms"])
        self.assertEqual(out["picture"]["systems"], fresh["systems"])
        self.assertAlmostEqual(out["picture"]["omen"]["threat"]["north_m"], fresh["omen"]["threat"]["north_m"], delta=1e-6)
        self.assertEqual(out["later"]["omen"]["decision_seconds"], later["omen"]["decision_seconds"])
        self.assertEqual(out["later"]["comms"], "down")
        self.assertEqual(out["later"]["omen"]["where"], later["omen"]["where"])
        self.assertTrue(out["cue"]["detected"])
        self.assertEqual(out["cue"]["fundamentalHz"], 140.0)
        self.assertEqual(out["merged"], 1)
        self.assertEqual(out["picture"]["coherence"]["state"], fresh["coherence"]["state"])
        self.assertEqual(out["picture"]["coherence"]["lit"], fresh["coherence"]["lit"])
        self.assertEqual(out["note"]["text"], smart_field_note(fresh, node_id="phone-maple", t=1005.0)["text"])


if __name__ == "__main__":
    unittest.main()
