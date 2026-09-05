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

Latest public data belongs here. A stale machine is a
weaker anti-bullshit device. Up to date is a U duty.
Strain and collisions stay on U.

Track A stays the damped PDE. Theorem A does not imply B.

---

## Scored

| Claim | Verdict |
|---|---|
| Fitting roster and feed into DA makes the process stronger | **pass** |
| That shape is an agent: propose, scan, score, alert | **pass** |
| DA must be able to refresh the latest public data | **pass** |
| The agent closes \(X\) | **fail** |
| The agent writes \(F\) | **fail** |
| The agent replaces the checker | **fail** |
| Latest LIGO or LHC data writes \(X\) | **fail** |
| Cosmo Superagent sits as this agent | **fail** |
| The agent unshelves SFE or retunes `nodes.json` | **fail** |
| More sources and watch chairs may be added | **open** |

Roster: [`DA-NOW.md`](DA-NOW.md)  
Feed: [`DA-FEED.md`](DA-FEED.md)  
Machine: [`DOMAIN-ARCHITECT-MACHINE.md`](DOMAIN-ARCHITECT-MACHINE.md)
