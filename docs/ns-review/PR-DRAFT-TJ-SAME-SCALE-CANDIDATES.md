# Draft PR — \(T_{j\leftarrow j}\) same-scale attack candidates

**Branch:** `cursor/tj-candidates-9083`  
**Base:** `main`  
**Compare:** https://github.com/simons357/Ship_it_app/compare/main...cursor/tj-candidates-9083  
**PR create:** blocked here (`gh` integration 403; no ManagePullRequest tool in this run). Open the compare link to file the draft PR if the environment does not auto-open one.

## Title

Narrow-first \(T_{j\leftarrow j}\) / (A) attack candidates (no Clay claim)

## Body

### Summary

Jonathan’s framing lock: chat “finished” = honesty + diagnostics + conditional Gronwall; proof “finished” still needs a real handle on same-scale transfer \(T_{j\leftarrow j}\) (and a non-circular path to (A)). This PR files a **narrow-first** candidate shortlist, runs cheap analytic + light numeric probes, and records who survives.

- New: `docs/ns-review/TJ-SAME-SCALE-CANDIDATES.md`
- New: `scripts/ns_attacks/tj_same_scale_candidate_probes.py`
- Pointer: `docs/ns-review/README.md`

### Candidates (headline)

| Status | IDs |
| --- | --- |
| **DEAD** | C1 energy+visc \(R\); C2 centrifugal-only leftover; C3 circular Gronwall; C4 occupancy⇒depletion |
| **BLOCKED** | C5 pure-swirl as class bound |
| **SURVIVES (TRY)** | C6 α/Door-3; C7 HH-only budget; C8 near-shell lab; C9 triad structure; **C10 depletion⇒(A)** (principal); C11 \(T^{\mathrm{mm}}\) (axisym-conditional); C12 SND conditional-only |

### Honesty

- NS / Clay B **not** claimed
- Spectral-shift ≠ Lemma★
- No recycling \(\dot e_j / \dot Z / \Lambda'\)
- Axisymmetry labeled conditional where used
- Numerics ≠ depletion / ≠ theorem

### Probe

```bash
python3 scripts/ns_attacks/tj_same_scale_candidate_probes.py
```

Artifacts under `/opt/cursor/artifacts/tj-same-scale-candidates/`.
