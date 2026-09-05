# DA tick — agent-shaped, not a closer

`python3 scripts/da_machine.py agent`

The living roster and the live feed sit **inside** DA.
That makes the process stronger. The shape is an **agent**:
ordinary AI proposes, the feed scans, scripts score, alert
speaks on a watched flip. The operator still runs the
command.

It is not a closer. It is not Cosmo Superagent. It does
not replace the checker.

---

## Architecture

| Piece | Command | Slot | Does | Does not |
|---|---|---|---|---|
| Living roster | `now` | U | names who sits | a genius census; a vote |
| Live feed | `feed` | U / B | refreshes GWTC, LHC, PDG, arXiv | write \(X\) or \(F\) |
| Tick | `agent` | U | pulls both and scores the shape | autopilot a pass |
| Alert | `alert` | U | texts a watched flip | a new catalog page |
| Now-what | `next` | U / B | wall, target, words→math | write the leftover |
| Council | `nowwhat` | U / B | leftover papers + history: would try / cannot | a vote; a séance; ChatGPT freestyle |
| Hunt | `hunt` | U / B | scored edges, blocked edges, object window | write \(\mathcal{R}\); LLM fill |
| Look | `look` | B | object window anytime | a bound |
| From | `from` | U / B | your steps to the break | a fake last line |
| Proof | `proof` | B | write the NS proof chain | QED without line (6) |
| Repair | `repair` | U / A / B / Q | take A, SND, or H; name the fault and the write | export A onto B |
| Attempt | `attempt` | U / A / RH / Q | best A and RH; dream team looks; legal write | vote a missing line |

Latest public data belongs here. A stale machine is a
weaker anti-bullshit device. Up to date is a U duty.
`status` reports last-scan age. It does not fetch.
Strain and collisions stay on U.

Track A stays the damped PDE. Theorem A does not imply B.

---

## Scored

| Claim | Verdict |
|---|---|
| Fitting roster and feed into DA makes the process stronger | **pass** |
| That shape is an agent: propose, scan, score, alert | **pass** |
| DA must be able to refresh the latest public data | **pass** |
| `status` reports last-scan age without a fetch | **pass** |
| The agent closes \(X\) | **fail** |
| The agent writes \(F\) | **fail** |
| The agent replaces the checker | **fail** |
| Latest LIGO or LHC data writes \(X\) | **fail** |
| Cosmo Superagent sits as this agent | **fail** |
| The agent unshelves SFE or retunes `nodes.json` | **fail** |
| More sources and watch chairs may be added | **open** |

Roster: [`DA-NOW.md`](DA-NOW.md)  
Feed: [`DA-FEED.md`](DA-FEED.md)  
Now-what: [`DA-NEXT.md`](DA-NEXT.md)  
Council: [`DA-NOWWHAT.md`](DA-NOWWHAT.md)  
Hunt: [`DA-HUNT.md`](DA-HUNT.md)  
Repair: [`DA-REPAIR.md`](DA-REPAIR.md)  
Attempt: [`DA-ATTEMPT.md`](DA-ATTEMPT.md)  
Machine: [`DOMAIN-ARCHITECT-MACHINE.md`](DOMAIN-ARCHITECT-MACHINE.md)
