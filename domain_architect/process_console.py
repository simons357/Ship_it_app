"""Process Console — engineering lane, schema v5.

The console represents process state. It does not wait on, and does
not change its verdict because of, a run's scientific outcome. Q4-1
v1 displaying INCONCLUSIVE is an acceptance test, not a fallback.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .atlas import ScientificMap, default_atlas
from .errata import (
    LIVE_TAYLOR_GREEN,
    WITHDRAWN_TAYLOR_GREEN,
    live_values_block,
    sweep_repository,
)
from .process_schema import (
    ProcessRun,
    PromotionDecision,
    SchemaError,
    compute_process_status,
    promotion_decision,
)
from .q4_runs import default_runs, write_run_fixtures
from .schema import PROCESS_RULES, SCHEMA_VERSION, ProcessStatus, StampKind
from .stamps import FX2_ID, FX2_TITLE, fx2_complete

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PACKAGE_ROOT / "data" / "process_console"


@dataclass
class RunView:
    run: ProcessRun
    process_status: ProcessStatus
    promotion: PromotionDecision
    promotion_reason: str
    failed_checks: list[dict[str, Any]]
    stamps: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        payload = self.run.to_dict()
        payload["console"] = {
            "process_status": self.process_status.value,
            "process_status_display": self.process_status.value.upper(),
            "promotion": self.promotion.value,
            "promotion_reason": self.promotion_reason,
            "failed_consistency_checks": self.failed_checks,
            "scientific_outcome_ignored_for_verdict": True,
            "schema_version": SCHEMA_VERSION,
        }
        return payload


@dataclass
class ConsoleSnapshot:
    schema_version: str = SCHEMA_VERSION
    fx2: dict[str, Any] = field(default_factory=dict)
    rules: tuple[str, ...] = PROCESS_RULES
    runs: list[RunView] = field(default_factory=list)
    atlas: ScientificMap = field(default_factory=default_atlas)
    live_taylor_green: dict[str, Any] = field(
        default_factory=lambda: dict(LIVE_TAYLOR_GREEN)
    )
    withdrawn_taylor_green: dict[str, Any] = field(
        default_factory=lambda: dict(WITHDRAWN_TAYLOR_GREEN)
    )
    stamp_kinds: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "fx2": self.fx2,
            "rules": list(self.rules),
            "runs": [v.to_dict() for v in self.runs],
            "atlas": self.atlas.to_dict(),
            "live_taylor_green": self.live_taylor_green,
            "withdrawn_taylor_green": self.withdrawn_taylor_green,
            "stamp_kinds": self.stamp_kinds,
            "ns_solved": False,
        }

    def view_for(self, run_id: str) -> RunView:
        for view in self.runs:
            if view.run.run_id == run_id:
                return view
        raise KeyError(run_id)


class ProcessConsole:
    """Load, judge, and render process runs against schema v5."""

    def __init__(self, runs: list[ProcessRun] | None = None) -> None:
        self.runs = list(runs) if runs is not None else default_runs()
        if not fx2_complete(s for run in self.runs for s in run.stamps):
            raise SchemaError("F-X2 incomplete: a stamp is not a typed v5 kind")

    @classmethod
    def load_data_dir(cls, data_dir: Path | None = None) -> "ProcessConsole":
        root = data_dir or DATA_DIR
        run_dir = root / "runs"
        if not run_dir.is_dir():
            return cls()
        runs: list[ProcessRun] = []
        for path in sorted(run_dir.glob("*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            runs.append(ProcessRun.from_dict(payload))
        return cls(runs)

    def render_run(self, run: ProcessRun) -> RunView:
        status = compute_process_status(run)
        decision, reason = promotion_decision(run)
        return RunView(
            run=run,
            process_status=status,
            promotion=decision,
            promotion_reason=reason,
            failed_checks=[c.to_dict() for c in run.failed_consistency_checks],
            stamps=[s.to_dict() for s in run.stamps],
        )

    def snapshot(self) -> ConsoleSnapshot:
        return ConsoleSnapshot(
            fx2={"id": FX2_ID, "title": FX2_TITLE, "complete": True},
            runs=[self.render_run(run) for run in self.runs],
            stamp_kinds=[
                {"kind": k.value, "label": k.label} for k in StampKind
            ],
        )

    def promote(self, run_id: str) -> dict[str, Any]:
        view = self.snapshot().view_for(run_id)
        return {
            "run_id": run_id,
            "allowed": view.promotion is PromotionDecision.ALLOWED,
            "decision": view.promotion.value,
            "reason": view.promotion_reason,
            "process_status": view.process_status.value,
        }

    def render_html(self) -> str:
        from .console_html import render_console_html

        return render_console_html(self.snapshot())

    def write_static(self, dest_dir: Path | None = None) -> dict[str, Path]:
        dest = dest_dir or (DATA_DIR / "site")
        dest.mkdir(parents=True, exist_ok=True)
        snap = self.snapshot()
        html_path = dest / "index.html"
        json_path = dest / "ledger.json"
        html_path.write_text(self.render_html(), encoding="utf-8")
        json_path.write_text(json.dumps(snap.to_dict(), indent=2) + "\n", encoding="utf-8")
        write_run_fixtures(DATA_DIR / "runs")
        (DATA_DIR / "atlas").mkdir(parents=True, exist_ok=True)
        (DATA_DIR / "atlas" / "scientific_map.json").write_text(
            json.dumps(snap.atlas.to_dict(), indent=2) + "\n", encoding="utf-8"
        )
        (DATA_DIR / "errata").mkdir(parents=True, exist_ok=True)
        (DATA_DIR / "errata" / "taylor_green.json").write_text(
            json.dumps(
                {
                    "live": snap.live_taylor_green,
                    "withdrawn": snap.withdrawn_taylor_green,
                    "block": live_values_block(),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        sweep = sweep_repository(PACKAGE_ROOT)
        (DATA_DIR / "errata" / "sweep.json").write_text(
            json.dumps(sweep.to_dict(), indent=2) + "\n", encoding="utf-8"
        )
        return {"html": html_path, "ledger": json_path}
