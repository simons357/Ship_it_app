# Finer DNS as an a priori

`python3 scripts/track_b_mesh.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B23: decaying \(n=32\) DNS is not a bound. B22e: a
finer box is not a saving climb. This write asks
whether \(n>32\) makes the DNS run an a priori.
It does not. Do not spawn \(n=64\).

---

## The knob on this write

Tesla: a finer DNS run is not continuation. Same
knob as B22e. Cashing \(n=64\) after a decaying
\(n=32\) path is a knob.

No \(Q_1\). No \(\varepsilon\). No Biot–Savart slogan.
Do not write \(c=8\) into the PDE. Do not spawn
\(n=64\).

---

## What the apparatus does

**B34, pass.** \(n=32\) DNS miss, refused no-blow,
and the finer-box miss are readable together.
Same caches as B23 / B33. No new FFT.

**B34a, fail** of “a finer box makes DNS an a
priori.” Same slogan as B23a at a finer \(n\).
A mesh is not an estimate.

**B34b, fail** of “cashing \(n=64\) DNS is
continuation.” B23b already refused a longer
interval. A finer grid is the same slogan.

**B34c, fail** of “an unrun finer DNS box is still
an NS a priori.” The field on this box decayed.
A box you did not run is not the packet.

**B34d, fail** of “a finer DNS run is
\(\int\|\omega\|_\infty\).” DNS-never-blew-up at a
finer \(n\) is the same refused slogan as B23d.

**B34e, fail** of “a leftover close writes
regularity.” Scored as B35. A leftover close is a
knob on the check. It does not write \(X\).
Regularity stays open. Do not spawn \(n=64\).

**B34f, fail** of “this retunes the PDE.” \(n\) is a
knob on the box.

**B23e, fail** of “a finer box makes DNS an a
priori.” Scored here.

**B33e, fail** of “the DNS leftover closes \(X\).”
Leftover is now scored.

---

## They work it

**Tesla.** You asked if a bigger DNS box writes the
bound. It does not. Sit down. Do not spawn \(n=64\).

**Leray.** Viscosity owned \(X\) on \(n=32\). A
finer mesh does not write my dissipation into a
bound for every datum.

**Ladyzhenskaya.** Same weight, both sides, at the
scale you are actually on. I still will not give
you \(\varepsilon\).

**Majda.** One triad is not all data. A finer triad
is still not Leray.

**Beale.** Nobody votes an unrun mesh into
\(\int\|\omega\|_\infty\).

**Feynman.** Missable: whether B23 already refused
the slogan, and whether \(n\) is a bound. The first
held. The a-priori slogan missed.

**Einstein.** The object stayed the classical field.
A finer lattice is not a closed estimate.

**Operator.** Finer DNS is scored. B23e is scored.
Leftover close is not an a priori (B34e). Regularity stays open. Do not spawn \(n=64\).
B4c stands. Do not cancel to \(\Phi\). Do not write
\(c=8\) into the PDE.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B23e | **fail** | finer makes DNS an a priori |
| B33e | **fail** | finer-as-DNS leftover closes \(X\) |
| B34 | **pass** | DNS miss, refused no-blow, finer-box miss readable |
| B34a | **fail** | finer DNS closes \(X\) |
| B34b | **fail** | cashing \(n=64\) DNS is continuation |
| B34c | **fail** | an unrun finer DNS is an NS a priori |
| B34d | **fail** | finer DNS is \(\int\|\omega\|_\infty\) |
| B34e | **fail** | a leftover close writes regularity |
| B34f | **fail** | this retunes the PDE |
| domain B | **open** | regularity stays open |

Tesla’s line: a finer DNS run is not continuation.
Same knob as B22e. Do not spawn \(n=64\).
