# PFPI API — v0.1 stub

**Base URL (local):** `http://127.0.0.1:8765`

Start server:

```bash
python3 -m tools.pfpi.ingest          # build index first
python3 -m tools.pfpi.serve             # or: uvicorn tools.pfpi.serve:app --port 8765
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Liveness + doc count |
| POST | `/v1/ingest?clear=true` | Rebuild SQLite index |
| GET | `/v1/search?q=` | Full-text search (BM25) |
| GET | `/v1/ledger?status=LEAD` | DA ledger filter |
| GET | `/v1/spells` | List registered spells |
| POST | `/v1/spells/run` | Run spell `{ "name": "sfe_bh_overlay", "args": {"Nmax": 200} }` |

## CLI equivalents

```bash
python3 -m tools.pfpi.search "Bridge star" --limit 5
python3 scripts/run_spell.py list
python3 scripts/run_spell.py bridge_floor_verify --Nmax 50
```

## Auth

None in v0 — add API keys in Phase 2 (`public`, `partner`, `clinical` partitions).

See `SEARCH-ENGINE-INTEGRATION-REPORT.md` for full integration playbook.
