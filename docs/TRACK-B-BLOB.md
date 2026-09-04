# Signed-strain blob as an a priori

`python3 scripts/track_b_blob.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B17: a named blob + signed strain. Net sits on
\(P_+\). The cubic is not live versus \(D\). This
write asks whether that leftover closes \(X\).
It does not.

---

## The knob on this write

Tesla: one-sided is a number. Large versus \(D\) is
a different number. If the leftover no longer
cancels, you can miss that. It did. A leftover is
not a bound for classical \(X\).

No \(Q_1\). No \(\varepsilon\). No Biot–Savart slogan.
Do not spawn \(n=64\).

---

## What the apparatus does

**B28, pass.** Blob, one-sided net, and visc-owned
cubic are readable together. Same caches as B17.
No new FFT.

**B28a, fail** of “a one-sided leftover closes
\(X\).” Cancel \(\approx 0.83\). \(P/D\approx 0.008\).
\(\dot X<0\). Coherence killed cancellation. It did
not make \(P\) large versus dissipation.

**B28b, fail** of “sitting where \(S_{zz}\) keeps a
sign is a class.” Localization in \(z\) is a knob.
A \(z\)-independent tube in the same strain still
cancels (B17c).

**B28c, fail** of “an \(L^2\) bound on this peaked
blob is an integral bound on the max vorticity.”
The ratio climbed from \(0.2\) to \(\sim 2.4\). The
criterion still asks for \(\int\|\omega\|_\infty\).

**B28d, fail** of “turning \(\nu\) down until
\(\dot X>0\) is continuation.” That is a knob on
the check. The working box stayed \(\nu=0.1\).

**B28e, fail** of “field occupation closes \(X\).”
Scored as B18e / B29. A clock that stays CONC
is not continuation.

**B28f, fail** of “this retunes the PDE.” One-sided
is a knob on the estimate.

**B17e, fail** of “a signed-strain blob closes
\(X\).” Scored here.

**B27e, fail** of “the coherent leftover closes
\(X\).” Leftover is now scored.

---

## They work it

**Tesla.** Cancellation moved (\(10^{-3}\to 0.83\)).
Size versus \(D\) sat (\(\sim 0.8\%\)). Do not sit
a leftover as a bound.

**Leray.** You used my dissipation again. On this
blob it still owns the net. Jean, a signed strain
is not my theorem extended.

**Majda.** A vortex tube that sees oscillating
stretch is not a blob that sits in one sign. Do
not sit “coherent” as a class.

**Beale.** The ratio climbed. Nobody votes
\(\|\omega\|_2\) into \(\int\|\omega\|_\infty\).

**Ladyzhenskaya.** Turn \(\nu\) down and the cubic
can win. That is a knob. I still will not give
you \(\varepsilon\).

**Feynman.** Missable: the cancel ratio, \(P/D\),
and whether a leftover is a bound. The first two
held. The a-priori slogan missed.

**Einstein.** The object stayed the classical field.
A leftover is not a closed estimate.

**Operator.** The blob is scored. B17e is scored.
Field occupation is not an a priori (B18e).
Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Next: DNS leftover (B23e). Finer stays B22e.
Do not spawn \(n=64\). B4c stands. Do not cancel
to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B17e | **fail** | signed-strain blob closes \(X\) |
| B27e | **fail** | coherent leftover closes \(X\) |
| B28 | **pass** | blob, one-sided net, visc-owned cubic readable |
| B28a | **fail** | one-sided leftover closes \(X\) |
| B28b | **fail** | sitting in one sign is a class |
| B28c | **fail** | peaked \(L^2\) is \(\int\|\omega\|_\infty\) |
| B28d | **fail** | turning \(\nu\) down is continuation |
| B28e | **fail** | field occupation closes \(X\) |
| B28f | **fail** | this retunes the PDE |
| domain B | **open** | DNS leftover is B23e |

Tesla’s line: one-sided is a number. Large versus
\(D\) is a different number. A leftover that no
longer cancels is not a bound.
