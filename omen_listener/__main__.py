"""JSON in, decision-window JSON out. No network."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from omen_listener.demo import demo_close_picture, demo_close_state, demo_picture, demo_state
from omen_listener.picture import build_picture


def _print(payload: dict) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="omen_listener")
    sub = parser.add_subparsers(dest="cmd", required=True)

    picture = sub.add_parser("picture", help="build a decision window from a state file")
    picture.add_argument("--state", required=True, type=Path)
    picture.add_argument("--now", type=float, default=None)

    demo = sub.add_parser("demo", help="write the tree-line sample the overlay reads")
    demo.add_argument("--out", required=True, type=Path)

    args = parser.parse_args(argv)
    if args.cmd == "picture":
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if args.now is not None:
            state["now"] = args.now
        _print(build_picture(state))
        return 0
    if args.cmd == "demo":
        out = args.out
        out.mkdir(parents=True, exist_ok=True)
        fresh_state = demo_state(1005.0)
        later_state = demo_state(1020.0)
        (out / "state.json").write_text(json.dumps(fresh_state, indent=2) + "\n", encoding="utf-8")
        (out / "state_later.json").write_text(json.dumps(later_state, indent=2) + "\n", encoding="utf-8")
        (out / "picture.json").write_text(json.dumps(demo_picture(1005.0), indent=2) + "\n", encoding="utf-8")
        (out / "picture_later.json").write_text(json.dumps(demo_picture(1020.0), indent=2) + "\n", encoding="utf-8")
        (out / "state_close.json").write_text(json.dumps(demo_close_state(), indent=2) + "\n", encoding="utf-8")
        (out / "picture_close.json").write_text(json.dumps(demo_close_picture(), indent=2) + "\n", encoding="utf-8")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
