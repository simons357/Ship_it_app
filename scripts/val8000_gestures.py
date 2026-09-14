#!/usr/bin/env python3
"""VAL8000 gesture map. Gestures are not skins. Mouth timing stays put.

He types in the box. This module does not speak. No TTS.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "cosmic-graffiti" / "val8000-gestures.json"

ALIASES = {
    "line": "idle",
    "waiting": "idle",
    "answer": "normal_answer",
    "normal": "normal_answer",
    "smile": "normal_answer",
    "joke": "funny_joke",
    "funny": "funny_joke",
    "funny_joke": "funny_joke",
    "tongue": "insult",
    "tongue_out": "insult",
    "puff": "bored",
    "puff_bag": "bored",
    "puffy_bag": "bored",
    "puffy": "bored",
    "inhale": "bored",
    "header": "masthead",
}

INSULT_MARKERS = (
    "stupid",
    "idiot",
    "dumb",
    "ugly",
    "shut up",
    "you suck",
    "useless",
    "hate you",
    "loser",
    "worthless",
    "dummy",
    "insult",
)
BORED_MARKERS = ("bored", "boring", "yawn")
COMPLIMENT_MARKERS = (
    "love you",
    "handsome",
    "good job",
    "you are the best",
    "nice work",
    "compliment",
    "well done",
)
JOKE_MARKERS = ("funny", "joke", "ha ha", "haha", "lol")
SARCASM_MARKERS = ("sarcasm", "sarcastic", "yeah right", "sure you did")


@dataclass(frozen=True)
class Play:
    intent: str
    channel: str
    frames: tuple[str, ...]
    assets: tuple[str, ...]
    masthead_ok: bool
    forbidden: tuple[str, ...] = ()

    @property
    def primary(self) -> str:
        return self.frames[-1]


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def _norm_intent(intent: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", intent.strip().lower()).strip("_")
    return ALIASES.get(key, key)


def play_for(intent: str) -> Play:
    catalog = load_catalog()
    key = _norm_intent(intent)
    stills = dict(catalog.get("stills") or {})
    mouth = dict(catalog.get("mouth_stills") or {})
    for row in catalog["mappings"]:
        if row["intent"] == key:
            frames = tuple(row["frames"])
            assets = []
            for frame in frames:
                rel = stills.get(frame) or mouth.get(frame)
                if rel:
                    assets.append(rel)
            never = tuple(row.get("never") or ())
            forbidden = never
            if row.get("not"):
                forbidden = forbidden + (row["not"],)
            return Play(
                intent=key,
                channel=row["channel"],
                frames=frames,
                assets=tuple(assets),
                masthead_ok=bool(row.get("masthead_ok")),
                forbidden=forbidden,
            )
    raise KeyError(f"unknown VAL8000 intent: {intent!r}")


def classify_utterance(
    text: str,
    *,
    bored: bool = False,
    masthead: bool = False,
) -> str:
    if masthead:
        return "masthead"
    blob = " ".join(str(text or "").lower().split())
    if any(marker in blob for marker in INSULT_MARKERS):
        return "insult"
    if bored or any(marker in blob for marker in BORED_MARKERS):
        return "bored"
    if any(marker in blob for marker in COMPLIMENT_MARKERS):
        return "compliment"
    if any(marker in blob for marker in SARCASM_MARKERS):
        return "sarcasm"
    if any(marker in blob for marker in JOKE_MARKERS):
        return "funny_joke"
    if blob:
        return "normal_answer"
    return "idle"


def play_for_utterance(
    text: str,
    *,
    bored: bool = False,
    masthead: bool = False,
) -> Play:
    return play_for(classify_utterance(text, bored=bored, masthead=masthead))


def describe(play: Play) -> str:
    if len(play.frames) == 1:
        return play.frames[0]
    return " then ".join(play.frames)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    map_p = sub.add_parser("map", help="Print the play for an intent")
    map_p.add_argument("intent")
    class_p = sub.add_parser("classify", help="Classify typed text, then map")
    class_p.add_argument("text")
    class_p.add_argument("--bored", action="store_true")
    class_p.add_argument("--masthead", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "map":
        play = play_for(args.intent)
    else:
        play = play_for_utterance(
            args.text, bored=args.bored, masthead=args.masthead
        )
        print(play.intent)
    print(describe(play))
    print(play.channel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
