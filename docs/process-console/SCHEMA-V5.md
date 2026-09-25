# Schema v5

Process objects are versioned independently of the FRA evidence ladder
(levels 0–6). Console code refuses any other `schema_version`.

## StampKind

Stored as an enum, not a sentence.

- `proved`
- `reproduced`
- `consistency_check`

Rejected tokens: `DA-STAMPED`, `DA_STAMPED`, `STAMPED`, `DA-STAMP`.

F-X2 (`domain_architect/stamps.py`) is the relabel gate. Console
startup requires every stamp on every loaded run to be a typed kind.

## ProcessStatus

`preregistered` · `executed` · `inconclusive` · `withdrawn` ·
`closed_negative`

`compute_process_status` does not read `scientific_outcome`.

## Promotion

Default is **prohibited**. INCONCLUSIVE, WITHDRAWN, PREREGISTERED,
failed consistency checks, and closed negatives cannot be promoted.
The HTTP desk returns HTTP 409 on `POST /api/promote` for those runs.
