# DA next — now-what spoke

`python3 scripts/da_machine.py next`  
`python3 scripts/da_machine.py next --ask "what do we do from here"`  
`python3 scripts/da_machine.py nowwhat`

DA sits in the middle. The rim is the support system:
live feed (LIGO, LHC, PDG, arXiv), past papers, living
papers, the residual catalog. The hard sentence is
**we are up to this part — now what.** This command
names the wall in English, names the target in math,
and turns an operator question into a slot plus a
sentence the checker can kill.

It does not write the leftover. It does not vote.

---

## Target

On Track B the target is

\[
X=\|\omega\|_2^2,\qquad
\int_0^T\mathcal{R}(t)\,dt<\infty.
\]

That is **not** \(F\). \(F\) is the producing-map on
the Standard Model poster (slot U). Realization is not
the NS leftover. LIGO is not \(1/r^4\).

---

## The wall

Scored through B41 on the \(n=32\) box. A1 is off. A2
is live and did not blow on the B15 path. Neither
integral is known for all data. Around the wall means
write one of those integrals, a different integrable
\(\mathcal{R}\), or a killing field. Not leftover-close
B42. Not \(n=64\).

Dream-team pointers: Tao (residual), Fefferman (A1 if),
Miller (A2 cut). Those are claims to classify, not a
committee fill. A lost operator who says **now what**
gets the leftover council (`nowwhat`): twenty-two
papers, each with a next try and a veto. Not ChatGPT
freestyle. Not a vote.

---

## Spokes

| Spoke | Command | Does | Does not |
|---|---|---|---|
| Feed | `feed` | refresh GWTC, LHC, PDG, arXiv | write \(X\) or \(F\) |
| Living / watch | `now` | who sits | a genius census |
| Past bench | `team` | papers + experiment | a vote |
| Residual | `trackb` | lemma catalog | leftover B42 |
| Translate | `next --ask` | words → slot + math | invent \(\mathcal{R}\) |
| Council | `nowwhat` | leftover papers: would try / cannot | a vote or a close |
| Checker | `check --domain B` | run the leftover tests | a close |

Re-run `feed` so the rim is not stale. `status` reports
age. A missing or \>24h scan is weaker.

---

## Scored

| Claim | Verdict |
|---|---|
| DA sits in the middle; feed, dream team, and residual are spokes | **pass** |
| `next` can translate “what now” into a math sentence | **pass** |
| On Track B the target is \(X\) / integrable \(\mathcal{R}\), not \(F\) | **pass** |
| A stale feed makes `next` weaker | **pass** |
| The next spoke writes the leftover | **fail** |
| Latest LIGO or arXiv announcement closes \(X\) | **fail** |
| The dream team votes the middle into existence | **fail** |
| The realization variable on B is \(F\) | **fail** |
| `next` is leftover-close B42 or \(n=64\) | **fail** |
| More spokes may be added | **open** |

Print: `python3 scripts/da_machine.py next`  
Lost: `python3 scripts/da_machine.py nowwhat`  
Council: [`DA-NOWWHAT.md`](DA-NOWWHAT.md)  
Feed: [`DA-FEED.md`](DA-FEED.md)  
Agent: [`DA-AGENT.md`](DA-AGENT.md)  
Residual: [`TRACK-B-RESIDUAL.md`](TRACK-B-RESIDUAL.md)
