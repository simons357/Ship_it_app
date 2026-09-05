# Live feed — latest public test results

`python3 scripts/da_machine.py feed`

An ongoing scan. Re-run the command. That is the
collection. DA must stay current. A missing or
\>24h `results/da_feed.json` is **stale**. `status`
prints last-scan age. It does not fetch.

LIGO events, LHC literature, PDG, and the arXiv streams
that already touch this desk. Each item stays in its slot.
A fetch miss is **open**, not a desk fail.

---

## Sources

| Source | Slot | Can kill | Cannot |
|---|---|---|---|
| GWOSC GWTC | U | “compact binaries are not seen” | B, Q, \(F\), `nodes.json` |
| INSPIRE ATLAS / CMS / LHCb | U | a poster number the papers move | why those numbers; write \(F\) |
| arXiv hep-ex | U | a stale collider abstract | write \(F\); close \(X\) |
| arXiv gr-qc | U | a stale GW abstract | import strain into the tube |
| arXiv astro-ph.CO | U | a cosmology number outside the box | write \(F\) |
| arXiv math.AP | B | a lemma whose identity fails | close B by announcement |
| PDG landing page | U | a poster number that drifts | why those numbers |

---

## What this is not

Not leftover-close B42. Not GWTC \(\Rightarrow\) regularity.
Not LHC \(\Rightarrow F\). Not a retune of `nodes.json`.
Not a constant stream of all science.

The pipe named the streams
([`DA-PIPE.md`](DA-PIPE.md)). This command refreshes them.

---

## Scored

| Claim | Verdict |
|---|---|
| An ongoing scan belongs on the desk | **pass** |
| Each item stays in its slot | **pass** |
| DA must stay current with the latest public data | **pass** |
| A missing or \>24h feed is stale; stale DA is weaker | **pass** |
| `status` fetches the live catalogs | **fail** |
| The feed is omniscience | **fail** |
| A new LIGO event closes \(X\) | **fail** |
| A new LHC paper writes \(F\) | **fail** |
| The feed writes leftover B42 | **fail** |
| A fetch miss is a desk fail | **fail** |
| A headline retunes `nodes.json` | **fail** |

Print: `python3 scripts/da_machine.py feed`  
Age: `python3 scripts/da_machine.py status`  
Now-what: `python3 scripts/da_machine.py next`  
Council: `python3 scripts/da_machine.py nowwhat`  
Roster: [`DA-NOW.md`](DA-NOW.md)  
Pipes: [`DA-PIPE.md`](DA-PIPE.md)

Do not spawn \(n=64\). Do not write leftover B42.
