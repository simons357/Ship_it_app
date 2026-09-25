"""Taylor–Green erratum and live-value sweep.

Live scientific values (schema v5):

    r^2 = 2.2291
    T_c / (ν D_s) = 1.2259

The withdrawn Taylor–Green fraction 3915/663 is provenance only
and must be marked WITHDRAWN wherever it is retained.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .schema import SCHEMA_VERSION

LIVE_R_SQUARED = 2.2291
LIVE_TC_OVER_NU_DS = 1.2259

WITHDRAWN_TG_NUMERATOR = 3915
WITHDRAWN_TG_DENOMINATOR = 663
WITHDRAWN_TG_FRACTION = WITHDRAWN_TG_NUMERATOR / WITHDRAWN_TG_DENOMINATOR

LIVE_TAYLOR_GREEN = {
    "r_squared": LIVE_R_SQUARED,
    "T_c_over_nu_D_s": LIVE_TC_OVER_NU_DS,
    "latex": r"r^2=2.2291,\qquad \frac{T_c}{\nu D_s}=1.2259",
    "status": "live",
    "role": "scientific_value",
}

WITHDRAWN_TAYLOR_GREEN = {
    "numerator": WITHDRAWN_TG_NUMERATOR,
    "denominator": WITHDRAWN_TG_DENOMINATOR,
    "display": "3915/663 WITHDRAWN",
    "approx": WITHDRAWN_TG_FRACTION,
    "status": "WITHDRAWN",
    "role": "historical_provenance_only",
    "do_not_cite_as_evidence": True,
    "replaced_by": LIVE_TAYLOR_GREEN,
}

# Count-imbalance form of the same withdrawn diagnostic.
WITHDRAWN_DIAGNOSTIC_IMBALANCE = {
    "broad_spectral_counts": WITHDRAWN_TG_NUMERATOR,
    "pointwise_viscous_counts": WITHDRAWN_TG_DENOMINATOR,
    "status": "WITHDRAWN",
    "role": "historical_provenance_only",
    "do_not_cite_as_evidence": True,
    "note": (
        "Q4-1 v1 treated 3,915 broad-spectral hits versus 663 "
        "pointwise viscous hits as if that ratio paid the dangerous "
        "term. That imbalance is not evidence and is not inherited "
        "by Q4-1 v2."
    ),
}

_FRACTION_PATTERNS = (
    re.compile(r"\b3[, ]?915\s*/\s*663\b"),
    re.compile(r"\b3915\s*/\s*663\b"),
    re.compile(r"\b3[, ]?915\b"),
)

_SKIP_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
    "artifacts",
}

_TEXT_SUFFIXES = {
    ".md",
    ".tex",
    ".json",
    ".py",
    ".txt",
    ".html",
    ".rst",
    ".csv",
}


@dataclass
class SweepHit:
    path: str
    line: int
    text: str
    classification: str


@dataclass
class SweepReport:
    schema_version: str = SCHEMA_VERSION
    live_values: dict[str, Any] = field(default_factory=lambda: dict(LIVE_TAYLOR_GREEN))
    withdrawn: dict[str, Any] = field(default_factory=lambda: dict(WITHDRAWN_TAYLOR_GREEN))
    hits: list[SweepHit] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "live_values": self.live_values,
            "withdrawn": self.withdrawn,
            "hits": [h.__dict__ for h in self.hits],
            "live_artifact_violations": [
                h.__dict__
                for h in self.hits
                if h.classification == "live_unmarked_withdrawn"
            ],
        }


_PROVENANCE_MARKERS = (
    "WITHDRAWN",
    "HISTORICAL PROVENANCE",
    "HISTORICAL_PROVENANCE",
    "DO_NOT_CITE_AS_EVIDENCE",
    "DEFECTIVE HISTORICAL",
    "Q4-1-V1",
    "Q4-1 V1",
)


def classify_hit(text: str, *, context: str = "") -> str:
    blob = f"{text}\n{context}".upper()
    if any(marker in blob for marker in _PROVENANCE_MARKERS):
        return "historical_withdrawn"
    if "2.2291" in text or "1.2259" in text:
        return "live_replacement_context"
    return "live_unmarked_withdrawn"


def sweep_paths(paths: Iterable[Path], *, root: Path | None = None) -> SweepReport:
    report = SweepReport()
    root = root or Path(".")
    for path in paths:
        if not path.is_file() or path.suffix.lower() not in _TEXT_SUFFIXES:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        try:
            rel = str(path.relative_to(root))
        except ValueError:
            rel = str(path)
        file_blob = "\n".join(lines)
        for i, line in enumerate(lines, start=1):
            if not any(p.search(line) for p in _FRACTION_PATTERNS):
                continue
            lo = max(0, i - 6)
            hi = min(len(lines), i + 5)
            context = "\n".join(lines[lo:hi]) + "\n" + file_blob[:4000]
            report.hits.append(
                SweepHit(
                    path=rel,
                    line=i,
                    text=line.strip(),
                    classification=classify_hit(line, context=context),
                )
            )
    return report


def iter_repo_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in root.rglob("*"):
        if any(part in _SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.is_file() and path.name != "sweep.json":
            out.append(path)
    return out


def sweep_repository(root: Path) -> SweepReport:
    return sweep_paths(iter_repo_files(root), root=root)


def live_values_block() -> str:
    return (
        "Live Taylor–Green scientific values (schema v5):\n\n"
        f"    r^2 = {LIVE_R_SQUARED}\n"
        f"    T_c / (ν D_s) = {LIVE_TC_OVER_NU_DS}\n\n"
        "Withdrawn fraction 3915/663 is historical provenance only."
    )


def write_sweep_report(report: SweepReport, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
