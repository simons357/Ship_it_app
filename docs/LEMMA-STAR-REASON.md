# The ★ reason — map, not a theorem

12 September 2026.
Unaugmented Navier–Stokes on \(\mathbb{T}^3\);
quantity is
\(\mathcal R_\star=(T_c)_+^2/(\mathcal D_s E Y)\);
remainder is signed stretching \((T_c)_+\)
versus spectral spread \(\mathcal D_s\);
no extra field. Unrestricted
\(\sup\mathcal R_\star<\infty\) is **NO**.

**This page is a map of cheap CS.
It is not a proof. It is not the kill.
The kill is the growing-layer family.
NS is not solved.**

The named kill arrived. Unrestricted
\(\sup\mathcal R_\star<\infty\) is **NO**.
Family: [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).
That page now lists every kill-relevant
side-condition written here, and checks
\(v_n\) against each. This page stays a
map of why cheap CS hides occupancy.
It is not the kill.
Need★ cannot repair the dead box.

Do not turn Attack 12’s table into
this sentence. Do not merge \(0.71\)
with \(\sqrt{K}\approx 0.711\).
Do not start H1 from ABC_λ.
Do not glue this integral to
\(A_{\mathrm{bad}}\).

Statement: [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md).
Identities: [`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Grow \(s\): [`ATTACK-9D-GROW-S.md`](ATTACK-9D-GROW-S.md).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).

---

## The sentence (map)

Signed stretching is
\[
T_c
=
\sum_k\lambda_k(\lambda_k-\Lambda)T_k
=
\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]
Keep \(\mathrm{Im}\). Do not replace it
by an absolute value. Only the complete
signed sum enters \(\mathcal R_\star\).

Spectral spread is
\[
\mathcal D_s
=
\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=
\frac{1}{2X}
\sum_{k,\ell}
\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2
|v_k|^2|v_\ell|^2.
\]
One shell \(\Rightarrow\mathcal D_s=0
\Rightarrow T_c=0\). Vacuous. Not a kill.

HH→L is the dangerous channel: two
high inputs, a lower output. The weight
\(\lambda_k(\lambda_k-\Lambda)\) is then
order \(\beta\cdot\alpha\) when \(\Lambda\)
sits near the high shell. The vertex
in Attack 12 carries \(\sqrt{\beta}\),
not \(\sqrt{\alpha}\). That is why the
channel looks able to stretch.

On every scored family that occupies
that channel, \(\mathcal D_s\) (or the
9B denominator \(\alpha^2/\beta\)) grew
at least as fast as \((T_c)_+\).
AP: \(\mathcal D_s\) wins. Adjacent
spheres: landings \(O(m)\),
\(\mathcal R_\star\) falls. HH→L fan:
\(\mathcal R_\star\sim\beta/\alpha\),
falls as the high shell climbs.
N-shell: saturates. 9B aligned closer:
finite \(K\) on samples. Grow \(s\)
(random pol, \(k_{\max}=8\)): max
\(K\approx 0.456\), max \(s=192\);
larger \(s\) did not raise \(K\).
ABC_λ: finite gate, not a kill.

That is the map. It is not the reason
as a theorem. The reason would force
the same comparison for every field,
or fail on a family with
\(\mathcal R_\star\to\infty\).

---

## Why a cheap CS is not the reason

The modal bound
\(\lvert\widehat B_k\rvert\le\lvert k\rvert\|v\|_2^2\)
gives
\(\lvert T_k\rvert\le\sqrt{\lambda_k}\,E\,\lvert v_k\rvert\).
Cauchy–Schwarz through the weights
\(\lambda_k(\lambda_k-\Lambda)\) then
returns an occupancy factor: a number
of active keys, not a uniform
\(C_{\mathrm{geom}}\). That is the same
hole as \(K\le 16s\). Fixed occupancy
is dead as a kill. Growing occupancy
is live write 1.

So “signed stretching cannot outrun
spread because of CS” is either false
or it hides \(s\). Hiding \(s\) is
how the screenshot 9D died.

---

## What leftover 4 is now

The named kill arrived:
\(\mathcal R_\star(v_n)\to\infty\).
Family: [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).
Unrestricted \(\sup\mathcal R_\star<\infty\)
is **NO**. Grow \(s\) on the 9B family
is historical. It did not kill ★.

Leftover 4 is a replacement
energy-budget estimate that \(v_n\)
does not kill. Need★ cannot repair
the dead box unless its hypotheses
or conclusion change.
[`NEED-STAR-HH-L-DUAL.md`](NEED-STAR-HH-L-DUAL.md).

A larger finite \(K\) only raises a
sample. It is not this kill.

Do not redo: five lanes 1–5, 9A,
natural 9C, finite 9B
(\(K\approx 0.641\)), small-lattice
truncated ABC, SuperGrok falsifier
stamp, Dream Team vote.

Out of this book: Q-stack, SND,
Theorem H, Cosmo five fingers,
augmented NSE. B-hand map:
[`DA-NS-FIVE-FINGER.md`](DA-NS-FIVE-FINGER.md).
MAP, not a close.

NS not solved. Unrestricted ★ killed.
Replacement closure OPEN.
