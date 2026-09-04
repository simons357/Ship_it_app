# Finer box as an a priori

`python3 scripts/track_b_finer.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B22: longer \(n=32\) past room time did not produce
\(c=8\). High shells stayed empty. This write asks
whether \(n>32\) closes \(X\). It does not.
Do not spawn \(n=64\).

---

## The knob on this write

Tesla: a bigger FFT is not continuation. \(n\) is a
knob on the box. Cashing \(n=64\) after a decaying
\(n=32\) path is a knob.

No \(Q_1\). No \(\varepsilon\). No Biot–Savart slogan.
Do not write \(c=8\) into the PDE. Do not spawn
\(n=64\).

---

## What the apparatus does

**B33, pass.** Longer \(n=32\) miss, empty high
shells, and the short window are readable together.
Same caches as B22 / B32. No new FFT.

**B33a, fail** of “a finer box closes \(X\).”
A mesh is not an estimate. The working box already
cannot host the cascade the slogan wants.

**B33b, fail** of “cashing \(n=64\) is continuation.”
Continuation is an estimate, not a finer mesh. Past
the sitting of \(c=8\) the path still decayed.

**B33c, fail** of “an unrun \(n=64\) box is still an
NS a priori.” The field on this box went down. A
box you did not run is not the packet.

**B33d, fail** of “a finer box is
\(\int\|\omega\|_\infty\).” A mesh is not the max
criterion.

**B33e, open.** DNS leftover is B23e. Finer-as-DNS
is the same knob, a later close. Do not spawn
\(n=64\).

**B33f, fail** of “this retunes the PDE.” \(n\) is a
knob on the box.

**B22e, fail** of “a finer box produces a saving
climb.” Scored here.

**B32e, fail** of “a finer box closes \(X\).”
Leftover is now scored.

---

## They work it

**Tesla.** You asked for a bigger box. That is a
knob on the check. The field on this box went down.
Do not buy \(n=64\) to hide that.

**Leray.** Viscosity owned \(X\) on \(n=32\). A
finer mesh does not write my dissipation into a
bound.

**Ladyzhenskaya.** Same weight, both sides, at the
scale you are actually on. \(n=32\) dealias cannot
host a fat \(j=4\). I still will not give you
\(\varepsilon\).

**Majda.** Still CONC at \(T=0.384\). Occupation of
CONC is not a cascade you buy with points.

**Beale.** Nobody votes an unrun mesh into
\(\int\|\omega\|_\infty\).

**Feynman.** Missable: \(T\) versus \(0.375\),
empty high shells, and whether \(n\) is a bound.
The first two held. The a-priori slogan missed.

**Einstein.** The object stayed the classical field.
A finer lattice is not a finer estimate.

**Operator.** The finer box is scored. B22e is
scored. Next: DNS leftover (B23e). Do not spawn
\(n=64\). B4c stands. Do not cancel to \(\Phi\).
Do not write \(c=8\) into the PDE.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B22e | **fail** | finer (\(n>32\)) produces a saving climb |
| B32e | **fail** | a finer box closes \(X\) |
| B33 | **pass** | longer miss, empty high shells, short window readable |
| B33a | **fail** | a finer box closes \(X\) |
| B33b | **fail** | cashing \(n=64\) is continuation |
| B33c | **fail** | an unrun \(n=64\) is an NS a priori |
| B33d | **fail** | a finer box is \(\int\|\omega\|_\infty\) |
| B33e | **open** | finer makes DNS an a priori |
| B33f | **fail** | this retunes the PDE |
| domain B | **open** | DNS leftover is B23e |

Tesla’s line: a bigger FFT is not continuation.
\(n\) is a knob on the box. Do not spawn \(n=64\).
