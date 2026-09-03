# Game theory on the 16 (does it narrow?)

`python3 scripts/da_machine.py game`

Short answer: **it re-ranks the score. It does not write \(F\).**
Two games, two answers. Do not glue them.

## Game R (the score)

Players: the knobs except \(R\).  
Value of a coalition \(S\):

\[
v(S)=\mathrm{lock}\,R(S)-\mathrm{baseline}.
\]

Shapley value is the average marginal when a knob is added
to a random coalition. That is the axiomatic version of
“who is pivotal,” the same question permutation importance
and the Hilbert flush already asked.

Monte Carlo Shapley (\(240\) permutations) recovers the
**same four**: vacuum, Planck, \(S_c\), \(\delta\). So Game R
does **not** narrow past the flush. It agrees with it.

## Game U (the unifier claim)

\[
u(S)=1\text{ if every must-hit is in }S,\text{ else }0.
\]

Must-hits: the four couplings, QCD scale, Planck, vacuum.
Shapley is \(1/7\) on each of those and \(0\) on everyone
else. That ranking is **by definition**, not by data. It
protects nature leftovers. It does not discover them.

This is why game theory feels like it “narrows” toward
gravity and the couplings: you already put them in the
winning coalition of Game U. The score game (R) still
says the couplings are not pivotal for \(R\).

## What it cannot do

- Write \(F\).
- Collapse the waveform.
- Decide whether vacuum is topological.
- Replace the missing Cosmo names.
- Turn a cheap signal (“the app said possible”) into a costly one.

Cheap talk stays cheap. Nature is not a player who pays
when the app is wrong.

Keep Game R and Game U separate. Agreement on the four
score-pivots is a robustness check, not emergence.
