# Lemma★ — 9B counting lock

10 September 2026. Analytic exclusion, then a
target. **Not a proof of ★. NS not solved.**

Phone: stay in this chat.

---

## What the screenshot got wrong

It put \(\Theta(m^2)\) pairs on **one** output
mode, or on a **fixed** number of outputs.
That cannot happen.

Fix \(k\). Then \(p+q=k\) forces \(q=k-p\).
Each input \(p\) has one partner. If the
input support has \(m\) keys, the number of
ordered pairs landing on that \(k\) is at
most \(m\). Not \(\Theta(m^2)\).

Total pairs across **all** outputs can still
be as large as \(m^2\). Squared amplitudes
on many outputs add in \(\|\Pi_\beta B\|_2\).
Growing the number of output modes is a
real test. Coherence there is not fake.
Parking \(\Theta(m^2)\) onto a fixed output
set is the error.

That fixed-output version of 9D cannot
unbound \(K_{\alpha,\beta}\). See below.
Do not rebuild Freiman-AP (already dead).
Do not rebuild the screenshot.

---

## A bound that does not care about phases

Incompressibility: \(p\cdot w_p=0\), so
\(q\cdot w_p=(k-p)\cdot w_p=k\cdot w_p\).
The bilinear piece at \(k\) obeys
\[
\bigl|\widehat{B(w,w)}_k\bigr|
\le
|k|\sum_p|w_p|\,|w_{k-p}|
\le
|k|\,\|w\|_2^2.
\]
Leray does not enlarge the vector.

If the projected interaction occupies \(s\)
keys on shell \(\beta\),
\[
\|\Pi_\beta B(w,w)\|_2^2
\le
s\,\beta\,\|w\|_2^4.
\]
The 9B quotient is
\[
K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
\le
s\frac{\beta^2}{\alpha^2}.
\]
Two inputs on shell \(\alpha\) satisfy
\(\sqrt{\beta}=|p+q|\le 2\sqrt{\alpha}\), so
\(\beta\le 4\alpha\), hence
\[
K_{\alpha,\beta}(w)\le 16s.
\]
Independent of phases and polarizations.

**Fixed \(s\)** (one output, or a bounded
number): \(K\) is uniformly bounded. That
kill shape is closed. Analytic, not numeric.

**Growing \(s\)**: this estimate does **not**
give a uniform \(C_0\). That remains live
for the 9B family.

---

## Correct uniform target (full 9B family)

★ on this family is equivalent to
\[
\|\Pi_\beta B(w,w)\|_2
\le
C\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2
\]
for some \(C\) independent of \(w,\alpha,\beta\).
That bound holds if and only if
\(\sup K_{\alpha,\beta}<\infty\).
It is the \(\varepsilon\to 0\) form of ★
on exact shells, not a new leftover.

A bound \(\|\Pi_\beta B\|_2\le C\alpha\|w\|_2^2\)
is the wrong packaging: it leaves a factor
\(\sqrt{\beta}\) (so \(K\lesssim\beta\)) and
does not control the 9B quotient.

Keep the frequency factors. Dropping \(|k|\)
is not this target.

---

## What remains

Full complex polarizations, growing input
**and** output support, frequency factors
kept. Probe:
`python3 scripts/ns_attacks/attack9b_output_counting.py`

Scores: [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).
9B JSON: [`five-lane-export/ATTACK_9B.md`](five-lane-export/ATTACK_9B.md).

Do not cash a finite \(\sqrt{K}\) as \(C_0\).
Do not glue this to H1.
NS not solved. ★ open.
