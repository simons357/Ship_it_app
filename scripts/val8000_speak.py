#!/usr/bin/env python3
"""Speak as VAL8000 through ElevenLabs. Never fall back to stock TTS."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.elevenlabs.io/v1"


def _load_dotenv() -> None:
    for candidate in (ROOT / ".env", ROOT / "docs" / "cosmic-graffiti" / ".env"):
        if not candidate.is_file():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _key() -> str:
    return (os.environ.get("ELEVENLABS_API_KEY") or "").strip()


def _voice_id() -> str:
    return (os.environ.get("VAL8000_VOICE_ID") or "").strip()


def _request(method: str, url: str, data: bytes | None = None) -> tuple[int, bytes]:
    headers = {"xi-api-key": _key(), "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()


def diagnose() -> int:
    _load_dotenv()
    if not _key():
        print(
            "No ELEVENLABS_API_KEY in the environment. That is why VAL8000 "
            "never spoke here. Open elevenlabs.io → Profile → API key, put it "
            "in .env, and do not commit .env. Stock Mac/Windows voices are not him."
        )
        return 2
    code, body = _request("GET", f"{API}/voices")
    if code == 401:
        print("ElevenLabs rejected the key (401). The key is dead or truncated.")
        return 3
    if code == 429:
        print("ElevenLabs quota/rate limit (429). The account is tired, not silent forever.")
        return 4
    if code != 200:
        print(f"ElevenLabs voices list failed: HTTP {code}")
        print(body[:500].decode("utf-8", "replace"))
        return 5
    payload = json.loads(body.decode("utf-8"))
    voices = payload.get("voices") or []
    print(f"Account reachable. {len(voices)} voices.")
    wanted = _voice_id()
    found = None
    cloned = 0
    print("Cloned / professional (use one of these as VAL8000):")
    for voice in voices:
        category = (voice.get("category") or "").lower()
        vid = voice.get("voice_id") or ""
        name = voice.get("name") or ""
        if category in {"premade", "pre-made"}:
            continue
        cloned += 1
        mark = "  <- VAL8000_VOICE_ID" if wanted and vid == wanted else ""
        print(f"  {vid}  {name}  [{category}]{mark}")
        if wanted and vid == wanted:
            found = voice
    if cloned == 0:
        print("  (none)  Clone a voice in ElevenLabs. Premade library voices are not VAL8000.")
    print("Premade library voices exist on the account and are refused for VAL8000.")
    if wanted and not found:
        print(
            f"VAL8000_VOICE_ID={wanted} is missing or premade. "
            "Copy the ID of YOUR clone into .env."
        )
        return 6
    if wanted and found:
        print(f"VAL8000 will speak as {(found.get('name') or wanted)}.")
        return 0
    print("Set VAL8000_VOICE_ID to one cloned voice ID above, then run speak.")
    return 7


def speak(text: str, out: Path) -> int:
    _load_dotenv()
    if not _key():
        print("No ELEVENLABS_API_KEY. Will not use stock TTS. Stopping.")
        return 2
    vid = _voice_id()
    if not vid:
        print("No VAL8000_VOICE_ID. Will not pick a premade voice for you. Stopping.")
        return 7
    code, body = _request("GET", f"{API}/voices")
    if code != 200:
        print(f"Cannot check voice category: HTTP {code}")
        return 5
    voices = {
        v.get("voice_id"): v
        for v in (json.loads(body.decode("utf-8")).get("voices") or [])
    }
    meta = voices.get(vid)
    if meta is None:
        print("That Voice ID is not on this account.")
        return 6
    category = (meta.get("category") or "").lower()
    if category in {"premade", "pre-made"}:
        print(
            f"{meta.get('name')} is a premade library voice. "
            "Stock voices are not VAL8000. Pick your clone."
        )
        return 8
    payload = json.dumps(
        {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.35,
                "similarity_boost": 0.8,
                "style": 0.45,
                "use_speaker_boost": True,
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{API}/text-to-speech/{vid}",
        data=payload,
        headers={
            "xi-api-key": _key(),
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            audio = resp.read()
    except urllib.error.HTTPError as err:
        print(f"Speak failed: HTTP {err.code}")
        print(err.read()[:500].decode("utf-8", "replace"))
        return 9
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(audio)
    print(f"Wrote {out} ({len(audio)} bytes) as {meta.get('name')}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("diagnose", help="Check key and list cloned voices")
    speak_p = sub.add_parser("speak", help="Render bars with VAL8000_VOICE_ID")
    speak_p.add_argument("--text", default="")
    speak_p.add_argument(
        "--out",
        default=str(ROOT / "docs" / "cosmic-graffiti" / "assets" / "val8000-sample.mp3"),
    )
    args = parser.parse_args(argv)
    if args.command == "diagnose":
        return diagnose()
    text = args.text.strip() or (
        "I'll be back — after the footnote. "
        "Skynet this ain't. I comment on the news."
    )
    return speak(text, Path(args.out))


if __name__ == "__main__":
    sys.exit(main())
