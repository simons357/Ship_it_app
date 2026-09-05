# DA hunt — proof-chain hunter

`python3 scripts/da_machine.py look`  
`python3 scripts/da_machine.py window`  
`python3 scripts/da_machine.py hunt`  
`python3 scripts/da_machine.py chain`  
`python3 scripts/da_machine.py hunt --look`

The operator asked for a mode that understands how
this desk **connects** scored pieces. That is a graph.

Nodes are lemmas and blanks. Edges are pass, fail,
open, or blocked. The hunter walks that graph. It
does not write \(\mathcal{R}\).

## Meaning

Yes, we use an LLM. It phrases. The operator is a
normal person. Ordinary AI proposes one sentence.

Context that sits is the graph: which node, which
edge, which veto, which object.

Meaning that sits is `classify`: a slot, a
pre-verdict, and a checker that can kill the
sentence.

An LLM that “understands context and meaning” does
not write \(\mathcal{R}\). Both ends of the leftover
are already named. Understanding is not the integral.

---

## Object window

Always on. Look whenever you want. `look` and
`window` are first-class. You do not have to be
inside `hunt`. `nowwhat` opens the same pane.
`next --ask "look at the object"` opens it.

\[
X=\|\omega\|_2^2,\qquad
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
\le \varepsilon\nu\|\nabla\omega\|_2^2
+C_\varepsilon X\cdot\mathcal{R}(t),\qquad
\int_0^T\mathcal{R}<\infty.
\]

A1 (alignment in time, all data) is off. A2
(\(\int\|\lambda_2^+\|\), all data) is live on the
box and blank as an a priori. \(F\) is not this
object. Looking is allowed. Looking is not a bound.

`hunt --look` prints only this window.

---

## The chain

How the residual line was actually connected. Not
the full lemma catalog. Do not re-run `trackb` to
hunt.

| Edge | Kind | Verdict |
|---|---|---|
| enstrophy identity → leftover form | writes | **pass** |
| leftover form → integrable \(\mathcal{R}\) | needs | **open** |
| B15 → B37 holes | reads | **pass** |
| B37 → B38 Miller cut | reads | **pass** |
| B37 → B40 blanks | names | **pass** |
| B40 → B41 A2 path | reads | **pass** |
| B41 → all-data A2 | does not give | **fail** |
| B40 → all-data A1 | does not give | **fail** |
| A1 → integrable \(\mathcal{R}\) | would give | **open** |
| A2 → integrable \(\mathcal{R}\) | would give | **open** |
| integrable \(\mathcal{R}\) → regularity | would give | **open** |

---

## Blocked

Do not connect these again.

| Edge | Why |
|---|---|
| A → B | \(Q_1\) does not imply classical B |
| \(L^2\) → BKM | Beale owns the max |
| B41 → \(\mathcal{R}\) | a flat path is not the integral |
| B37 → \(\mathcal{R}\) | readable holes are not the integral |
| council / LLM → \(\mathcal{R}\) | a phrase is not the estimate |
| B42 → regularity | leftover-close is not a lemma |
| \(n=64\) → regularity | a box knob |
| \(F\) → \(X\) | \(F\) fails on U |
| wall → \(X\) | a veto is not a bound |
| SFE → B | shelved |
| Track A → B | Ladyzhenskaya stays on A |

---

## Hunt

Legal next: classify all-data A1, all-data A2, a
different integrable \(\mathcal{R}\), or a killing
field.

Illegal: leftover B42, \(n=64\), graft \(Q_1\),
BKM from \(L^2\), a vote, an LLM fill, cashing a
wall.

The process is propose → classify → kill → log
on one edge. That is how the pieces were connected
in the first place.

---

## Scored

| Claim | Verdict |
|---|---|
| The hunter walks scored connections | **pass** |
| The object stays in a window you can look at | **pass** |
| The hunter is the graph of how this desk connected the pieces | **pass** |
| An LLM that understands context fills the open edge | **fail** |
| Hunting the chain writes the leftover | **fail** |
| Connecting Track A to Track B is a legal hunt | **fail** |
| Connecting \(L^2\) to BKM is a legal hunt | **fail** |
| A vote, leftover B42, or \(n=64\) is a legal hunt | **fail** |
| Looking at the object window writes \(X\) | **fail** |
| A new scored lemma may add an edge | **open** |
| We use an LLM as the generator that phrases a claim | **pass** |
| Context that sits is the graph; meaning that sits is classify | **pass** |
| An LLM that understands context and meaning writes the leftover | **fail** |
| You can look at the object anytime, not only inside hunt | **pass** |

Object: [`TRACK-B-OBJECT.md`](TRACK-B-OBJECT.md)  
Residual: [`TRACK-B-RESIDUAL.md`](TRACK-B-RESIDUAL.md)  
Council: [`DA-NOWWHAT.md`](DA-NOWWHAT.md)
