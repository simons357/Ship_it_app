"""Q4-1 historical fixture (v1) and preregistered successor (v2).

v1 is a deliberately defective historical run. Process Console must
render it INCONCLUSIVE, expose the failed consistency check, and
refuse promotion — even if someone later writes a glowing scientific
outcome on the record.

v2 is a new preregistered run: direct D_s, scale-aware residual,
locked hashes, the same decision window unless DA changes it first.
It does not inherit the 3,915/663 diagnostic imbalance as evidence.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .errata import (
    LIVE_R_SQUARED,
    LIVE_TC_OVER_NU_DS,
    WITHDRAWN_DIAGNOSTIC_IMBALANCE,
    WITHDRAWN_TAYLOR_GREEN,
)
from .process_schema import (
    Q4_DECISION_WINDOW,
    ConsistencyCheck,
    ProcessRun,
    StampRecord,
)
from .protocol import freeze_protocol
from .schema import ProcessStatus, StampKind

DIRECT_DS_FORM = "D_s = Z - ΛY = ‖A^{1/2}(A-Λ)u‖² ≥ 0"
SCALE_AWARE_RESIDUAL = "R_κ = (T_c - ν D_s) / (ν D_s)  (scale-aware; not a count ratio)"
CLOSED_SHORTCUT = (
    "Broad spectral state ⇏ pointwise viscous payment of the dangerous term"
)

Q4_1_V1_ID = "Q4-1-v1"
Q4_1_V2_ID = "Q4-1-v2"

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "process_console"


def _hash_payload(payload: dict[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()


def q4_1_v1_historical() -> ProcessRun:
    """Defective historical run: proxy counts instead of direct D_s."""
    failed = ConsistencyCheck(
        check_id="Q4-1-v1-CC-direct-Ds",
        stipulated_formula=DIRECT_DS_FORM,
        implementation=(
            "count ratio 3915/663 (broad-spectral hits / pointwise viscous hits)"
        ),
        passed=False,
        detail=(
            "Implementation used the withdrawn 3,915/663 diagnostic imbalance "
            "as a proxy for T_c/(ν D_s). That is not the stipulated direct "
            "D_s form and is not a scale-aware residual."
        ),
    )
    return ProcessRun(
        run_id=Q4_1_V1_ID,
        title="Q4-1 v1 — historical Taylor–Green diagnostic (defective)",
        version="v1",
        lane="historical",
        process_status=ProcessStatus.INCONCLUSIVE,
        scientific_outcome=(
            "Do not read. Any apparent positive reading is void: the "
            "consistency check failed."
        ),
        executed=True,
        preregistered=False,
        decision_window=Q4_DECISION_WINDOW,
        consistency_checks=[failed],
        stamps=[
            StampRecord(
                kind=StampKind.CONSISTENCY_CHECK,
                statement=DIRECT_DS_FORM,
                status="failed",
                notes=failed.detail,
            )
        ],
        protocol_hash="",
        code_hashes={},
        diagnostics={
            "withdrawn_fraction": dict(WITHDRAWN_TAYLOR_GREEN),
            "withdrawn_imbalance": dict(WITHDRAWN_DIAGNOSTIC_IMBALANCE),
            "used_direct_Ds": False,
            "used_scale_aware_residual": False,
        },
        inherited_evidence_ids=[],
        notes=[
            "Deliberately retained as a defective historical run.",
            "Process Console acceptance test: display INCONCLUSIVE.",
            "Do not promote to evidence.",
            CLOSED_SHORTCUT,
        ],
        historical=True,
        defective=True,
    )


def q4_1_v2_preregistration() -> ProcessRun:
    """Genuinely new preregistered run. Not evidence yet."""
    protocol = freeze_protocol(
        {
            "run_id": Q4_1_V2_ID,
            "D_s_form": DIRECT_DS_FORM,
            "residual": SCALE_AWARE_RESIDUAL,
            "decision_window": Q4_DECISION_WINDOW.to_dict(),
            "live_taylor_green": {
                "r_squared": LIVE_R_SQUARED,
                "T_c_over_nu_D_s": LIVE_TC_OVER_NU_DS,
            },
            "inherit_q4_1_v1_imbalance": False,
            "inherit_withdrawn_fraction": False,
        }
    )
    locked_code = {
        "domain_architect/q4_runs.py": _hash_payload({"module": "q4_runs", "v": "v2"}),
        "domain_architect/process_schema.py": _hash_payload({"module": "process_schema"}),
        "direct_Ds": _hash_payload({"formula": DIRECT_DS_FORM}),
        "scale_aware_residual": _hash_payload({"formula": SCALE_AWARE_RESIDUAL}),
    }
    check = ConsistencyCheck(
        check_id="Q4-1-v2-CC-direct-Ds-prereg",
        stipulated_formula=DIRECT_DS_FORM,
        implementation="locked; not executed. Direct D_s form is the only admitted diagnostic.",
        passed=True,
        detail=(
            "Preregistration locks the formula. No numerical result is "
            "claimed. 3915/663 is not an input."
        ),
    )
    return ProcessRun(
        run_id=Q4_1_V2_ID,
        title="Q4-1 v2 — preregistered direct-D_s / scale-aware residual",
        version="v2",
        lane="research",
        process_status=ProcessStatus.PREREGISTERED,
        scientific_outcome="not_run",
        executed=False,
        preregistered=True,
        decision_window=Q4_DECISION_WINDOW,
        consistency_checks=[check],
        stamps=[
            StampRecord(
                kind=StampKind.CONSISTENCY_CHECK,
                statement="Preregistration locks direct D_s and the scale-aware residual.",
                status="locked_not_executed",
                notes="Not a proof. Not a reproduction. Not evidence.",
            )
        ],
        protocol_hash=protocol.protocol_hash,
        code_hashes=locked_code,
        diagnostics={
            "D_s_form": DIRECT_DS_FORM,
            "residual": SCALE_AWARE_RESIDUAL,
            "live_taylor_green": {
                "r_squared": LIVE_R_SQUARED,
                "T_c_over_nu_D_s": LIVE_TC_OVER_NU_DS,
            },
            "inherits_3915_663": False,
        },
        inherited_evidence_ids=[],
        notes=[
            "Genuinely new preregistered run. Not a continuation of v1 evidence.",
            "Same decision window as v1 unless DA changes it beforehand.",
            "Locked hashes must match before the window is opened.",
        ],
        historical=False,
        defective=False,
    )


def default_runs() -> list[ProcessRun]:
    return [q4_1_v1_historical(), q4_1_v2_preregistration()]


def write_run_fixtures(dest_dir: Path | None = None) -> list[Path]:
    dest = dest_dir or (_DATA_DIR / "runs")
    dest.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for run in default_runs():
        path = dest / f"{run.run_id}.json"
        path.write_text(json.dumps(run.to_dict(), indent=2) + "\n", encoding="utf-8")
        written.append(path)
    return written
