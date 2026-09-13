"""Unified spell runner — execute registered pattern-hunter scripts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from packages.shared_core.config import load_spell_registry

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARTIFACT_DIR = Path("/opt/cursor/artifacts")


def list_spells(registry_path: Path | None = None) -> dict[str, Any]:
    reg = load_spell_registry(registry_path)
    return reg.get("spells", {})


def _args_to_argv(spell_id: str, entry: dict[str, Any], args: dict[str, Any]) -> list[str]:
    """Map spell args dict to CLI positional arguments."""
    schema = entry.get("args_schema") or {}

    if spell_id == "sfe_bh_overlay":
        if "Nmax" in args:
            return [str(int(args["Nmax"]))]
        if "sizes" in args:
            return [str(int(x)) for x in args["sizes"]]
        return []

    if spell_id == "hb_ringdown":
        argv: list[str] = []
        if "split" in args:
            argv.extend(["--split", str(args["split"])])
        if "mc" in args:
            argv.extend(["--mc", str(int(args["mc"]))])
        return argv

    if spell_id == "bridge_floor_verify":
        if "Nmax" in args:
            return [str(int(args["Nmax"]))]
        return []

    # Default: pass numeric args in schema order, then any extra values
    argv = []
    for key in schema:
        if key in args:
            argv.append(str(args[key]))
    for key, val in args.items():
        if key not in schema:
            argv.append(str(val))
    return argv


def run_spell(
    spell_id: str,
    args: dict[str, Any] | None = None,
    *,
    registry_path: Path | None = None,
    repo_root: Path = REPO_ROOT,
    timeout: int = 300,
) -> dict[str, Any]:
    """Run a registered spell and return structured result."""
    reg = load_spell_registry(registry_path)
    spells = reg.get("spells", {})
    if spell_id not in spells:
        raise KeyError(f"Unknown spell: {spell_id}")

    entry = spells[spell_id]
    script_rel = entry["script"]
    script_path = repo_root / script_rel
    if not script_path.exists():
        raise FileNotFoundError(f"Spell script not found: {script_path}")

    argv = [sys.executable, str(script_path)]
    argv.extend(_args_to_argv(spell_id, entry, args or {}))

    proc = subprocess.run(
        argv,
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    meta = reg.get("meta", {})
    artifact_dir = Path(meta.get("artifact_dir", DEFAULT_ARTIFACT_DIR))
    output_name = entry.get("output")
    artifact_path: Path | None = None
    artifact_url: str | None = None

    if output_name:
        candidate = artifact_dir / output_name if "/" not in output_name else repo_root / output_name
        if candidate.exists() and candidate.is_file():
            artifact_path = candidate
            artifact_url = str(artifact_path)

    return {
        "spell": spell_id,
        "name": entry.get("name"),
        "command": argv,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "artifact_path": str(artifact_path) if artifact_path else None,
        "artifact_url": artifact_url,
        "tags": entry.get("tags", []),
    }


def run_spell_json(spell_id: str, args: dict[str, Any] | None = None, **kwargs: Any) -> str:
    return json.dumps(run_spell(spell_id, args, **kwargs), indent=2)
