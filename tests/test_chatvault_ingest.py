#!/usr/bin/env python3
"""Any-source ChatVault ingest into the repo inbox — not browser localStorage."""

from __future__ import annotations

import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from domain_architect import site_server
from domain_architect.chatvault_ingest import (
    COPY_CAP_BYTES,
    classify_filename,
    ingest_file,
    ingest_path,
    looks_like_chatgpt_export,
    write_inbox_payload,
)
from domain_architect.cli import main
from domain_architect.site_server import MAX_INBOX_POST_BYTES, SiteHandler


class TestClassifyAndOrigin(unittest.TestCase):
    def test_wav_is_audio_not_chatgpt(self) -> None:
        self.assertEqual(classify_filename("voice.wav", "audio/wav"), "audio")
        self.assertEqual(classify_filename("clip.MP4"), "movie")
        self.assertEqual(classify_filename("scan.PDF"), "pdf")
        self.assertFalse(looks_like_chatgpt_export(b"RIFF"))
        self.assertFalse(looks_like_chatgpt_export({"mapping": "not-an-object"}))


class TestIngestPath(unittest.TestCase):
    def test_wav_writes_json_and_copies_tiny_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = Path(tmp) / "inbox"
            src = Path(tmp) / "voice.wav"
            src.write_bytes(b"RIFF\x24\x00\x00\x00WAVEfmt ")
            result = ingest_path(src, inbox)
            self.assertEqual(result.count, 1)
            entry = result.entries[0]
            self.assertEqual(entry["origin_class"], "human_record")
            self.assertEqual(entry["source_type"], "audio")
            self.assertEqual(entry["source_ai"], "human")
            self.assertIn("inbox", entry["search_tags"])
            self.assertTrue(entry["media_path"].endswith("voice.wav") or "voice" in entry["media_path"])
            payload = json.loads(result.written[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["format"], "chatvault-export")
            self.assertEqual(payload["entries"][0]["origin_class"], "human_record")
            copied = inbox / "media" / "voice.wav"
            self.assertTrue(copied.is_file())
            self.assertEqual(copied.read_bytes()[:4], b"RIFF")
            self.assertNotIn("USER:", entry["raw_content"])
            index = json.loads((inbox / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(index["count"], 1)

    def test_text_letter_is_human_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = Path(tmp) / "inbox"
            src = Path(tmp) / "letter.txt"
            src.write_text("Dear colleague, the wav is on the bench.\n", encoding="utf-8")
            result = ingest_path(src, inbox)
            entry = result.entries[0]
            self.assertEqual(entry["origin_class"], "human_record")
            self.assertEqual(entry["source_type"], "letter")
            self.assertIn("wav is on the bench", entry["raw_content"])
            self.assertFalse((inbox / "media" / "letter.txt").exists())

    def test_copy_cap_writes_json_without_copying(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = Path(tmp) / "inbox"
            inbox.mkdir()
            src = Path(tmp) / "huge.wav"
            src.write_bytes(b"RIFF" + b"\x00" * 40)
            entries = ingest_file(src, inbox, copy_cap=8)
            self.assertEqual(entries[0]["origin_class"], "human_record")
            self.assertEqual(entries[0]["source_type"], "audio")
            self.assertEqual(entries[0]["media_path"], "")
            self.assertIn("copy_cap=", entries[0]["raw_content"])
            self.assertFalse(any((inbox / "media").glob("*.wav")))

    def test_directory_skips_node_modules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "drop"
            (root / "node_modules").mkdir(parents=True)
            (root / "node_modules" / "ignore.txt").write_text("secret", encoding="utf-8")
            (root / "keep.txt").write_text("Keep this letter.", encoding="utf-8")
            inbox = Path(tmp) / "inbox"
            result = ingest_path(root, inbox)
            titles = [entry["title"] for entry in result.entries]
            self.assertIn("keep.txt", titles)
            self.assertNotIn("ignore.txt", titles)

    def test_cli_ingest_chatvault(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = Path(tmp) / "inbox"
            src = Path(tmp) / "note.txt"
            src.write_text("A paper margin note.\n", encoding="utf-8")
            rc = main(["--ingest-chatvault", str(src), "--inbox", str(inbox)])
            self.assertEqual(rc, 0)
            sidecars = list(inbox.glob("*.json"))
            sidecars = [path for path in sidecars if path.name != "index.json"]
            self.assertEqual(len(sidecars), 1)
            payload = json.loads(sidecars[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["format"], "chatvault-export")
            self.assertEqual(payload["entries"][0]["origin_class"], "human_record")


class TestInboxHttp(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "inbox").mkdir()
        self._orig = site_server.CHATVAULT
        site_server.CHATVAULT = self.root
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), SiteHandler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.origin = f"http://127.0.0.1:{self.port}"

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        site_server.CHATVAULT = self._orig
        self.tmp.cleanup()

    def test_post_json_sidecar_and_list(self) -> None:
        entry = {
            "format": "chatvault-export",
            "schema_version": "chatvault-engine-0.3.0",
            "entries": [
                {
                    "id": "ent_inboxprobe",
                    "title": "voice.wav",
                    "source_type": "audio",
                    "source_ai": "human",
                    "origin_class": "human_record",
                    "raw_content": "REAL AUDIO STUB voice.wav\nmime=audio/wav\nsize=16\n",
                    "summary": "stub",
                    "search_tags": ["inbox", "audio"],
                }
            ],
        }
        req = urllib.request.Request(
            f"{self.origin}/api/inbox",
            data=json.dumps(entry).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as res:
            self.assertEqual(res.status, 200)
            posted = json.loads(res.read().decode("utf-8"))
        self.assertTrue(posted["ok"])
        self.assertEqual(posted["count"], 1)
        with urllib.request.urlopen(f"{self.origin}/api/inbox") as res:
            listing = json.loads(res.read().decode("utf-8"))
        self.assertEqual(listing["count"], 1)
        name = listing["files"][0]["name"]
        with urllib.request.urlopen(f"{self.origin}/chatvault/inbox/{name}") as res:
            sidecar = json.loads(res.read().decode("utf-8"))
        self.assertEqual(sidecar["format"], "chatvault-export")
        self.assertEqual(sidecar["entries"][0]["origin_class"], "human_record")
        self.assertEqual(sidecar["entries"][0]["source_type"], "audio")

    def test_post_rejects_non_export(self) -> None:
        req = urllib.request.Request(
            f"{self.origin}/api/inbox",
            data=b'{"hello":"nope"}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)

    def test_copy_cap_constant_is_documented(self) -> None:
        self.assertEqual(COPY_CAP_BYTES, 100 * 1024 * 1024)
        self.assertLessEqual(MAX_INBOX_POST_BYTES, 5 * 1024 * 1024)
        self.assertGreaterEqual(MAX_INBOX_POST_BYTES, 64 * 1024)


class TestWriteInboxPayload(unittest.TestCase):
    def test_single_entry_wraps_as_export(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            inbox = Path(tmp)
            written = write_inbox_payload(
                {
                    "id": "ent_wrap",
                    "title": "clip.mp4",
                    "source_type": "movie",
                    "origin_class": "human_record",
                    "raw_content": "REAL MOVIE STUB clip.mp4\n",
                },
                inbox,
            )
            self.assertEqual(len(written), 1)
            payload = json.loads(written[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["format"], "chatvault-export")
            self.assertEqual(payload["entries"][0]["source_type"], "movie")


if __name__ == "__main__":
    unittest.main()
