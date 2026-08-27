# Overnight demo — copy-paste for Jonathan

Wake-up sheet for the Domain Architect loop on branch
`cursor/ns-b-five-finger-router-0cc5` (PR #28).

**What this is:** a structural translator (auto map → reconstruct → compare →
tuning handoff → incompleteness → drill-down → dual-SFE).  
**What this is not:** ToE, Clay/Millennium proof, hybrid SFE, prime-`P`, or
`λ_min` bake-in. Canonical SFE status stays **unresolved**.

Artifacts from the overnight run live under `/opt/cursor/artifacts/`.

---

## 0. One-shot full loop (start here)

```bash
cd /workspace
python3 scripts/overnight_honest_loop_demo.py
```

Then wire tuning JSON into the old bridge-style dial story (no optimizer):

```bash
python3 -m domain_architect --tuning-json \
  "partial_t omega = (omega * nabla) u + nu Delta omega" \
  > /tmp/ns_tuning.json

python3 -m domain_architect --tuning-json \
  "nabla^2 Phi = 4 pi G rho" \
  > /tmp/grav_tuning.json

python3 scripts/bridge_tuning_handoff_demo.py /tmp/ns_tuning.json
python3 scripts/bridge_tuning_handoff_demo.py /tmp/grav_tuning.json
```

---

## 1. Gravity (Poisson book)

```bash
python3 -m domain_architect "nabla^2 Phi = 4 pi G rho"
python3 -m domain_architect --tuning-json "nabla^2 Phi = 4 pi G rho"
```

---

## 2. Partial / thin NS (incompleteness)

```bash
python3 -m domain_architect --incompleteness-json \
  "partial_t omega = nu Delta omega"
```

Expect `is_complete=false` and book-template candidates for missing
advection / incompressibility — not new physics.

---

## 3. Full classical NS-B

```bash
python3 -m domain_architect \
  "partial_t omega = (omega * nabla) u + nu Delta omega"
```

---

## 4. NS vs gravity compare (unlike books)

```bash
python3 -m domain_architect --compare \
  "partial_t omega = (omega * nabla) u + nu Delta omega" \
  "nabla^2 Phi = 4 pi G rho"
```

---

## 5. Drill-down / recompose (`--decompose-json`)

```bash
python3 -m domain_architect --decompose-json \
  "partial_t omega = (omega * nabla) u + nu Delta omega" \
  > /tmp/ns_decompose.json
```

Mermaid sketch of the module tree (optional):

```bash
python3 - <<'PY'
import json
from pathlib import Path
d = json.loads(Path("/tmp/ns_decompose.json").read_text())
print("```mermaid")
print("flowchart TD")

def walk(node, parent=None):
    mid = node["module_id"].replace("-", "_")
    label = node.get("label", mid).replace('"', "'")
    print(f'  {mid}["{mid}: {label}"]')
    if parent:
        print(f"  {parent} --> {mid}")
    for ch in node.get("children") or []:
        walk(ch, mid)

walk(d["root"])
print("```")
PY
```

---

## 6. Put SFE in twice (`--sfe-compare`)

```bash
python3 -m domain_architect --list-sfe

# Same candidate twice → IDENTICAL; still not canonical
python3 -m domain_architect --sfe-compare SFE-H001 SFE-H001

# Distinct historical candidates → INCOMPATIBLE; no hybrid
python3 -m domain_architect --sfe-compare SFE-H001 SFE-H002
```

---

## 7. Roles → sketch + tests

```bash
python3 -m domain_architect --roles-sketch \
  "admissibility,interaction,state,scale_response,realized_output"

python3 -m unittest discover -s tests -p 'test_*.py'
```

---

## Artifact index (overnight)

| File | Contents |
|------|----------|
| `overnight_demo_suite.log` | Concatenated full suite run |
| `overnight_honest_loop_demo.txt` | One-shot demo stdout |
| `overnight_honest_loop_summary.json` | Machine summary |
| `ns_tuning_export.json` / `grav_tuning_export.json` | Bridge dials |
| `ns_decompose.json` / `ns_decompose_tree.mmd` | Drill-down + mermaid |
| `ns_incompleteness.json` | Thin-NS gap report |
| `ns_vs_gravity_compare.log` | Unlike-book compare |
| `sfe_put_in_twice_*.log` | Dual-SFE demos |
| `bridge_tuning_handoff_*.txt` | How old UIs would wire dials |
| `unit_test_results.txt` | Full unittest output |

Longer narrative: [`06-OVERNIGHT-HONEST-LOOP.md`](06-OVERNIGHT-HONEST-LOOP.md).
