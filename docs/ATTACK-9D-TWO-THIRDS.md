# Exact-shell 9D — three-shear floor \(K=2/3\)

13 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for \(Aw=\alpha w\);
the field below is one exact-shell example;
**this is a floor, not the ceiling.**

**One explicit value does not prove
\(\sup K\le 16/9\). It proves
\(\sup K\ge 2/3\).**
Aligned 9B \(0.641\) and grow-\(s\)
\(0.456\) sit below this.
\(2/3\approx 0.667<16/9\approx 1.778\).
Specialist review of the \(16/9\)
derivation is still pending.
Unrestricted ★ is killed by \(v_n\).
This page does not resurrect it.
NS is not solved. Soft X silent.

Bound page: [`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md).
Machine: `scripts/ns_attacks/attack9d_two_thirds.py`.
Live Stokes was not overwritten.

---

## The field (one line)

\[
w(x,y,z)=(\sin y,\sin z,\sin x).
\]

It is real, mean-zero, divergence-free.
Support is the six axis modes of
shell \(\alpha=1\):

\[
\widehat w(0,1,0)=\Bigl(-\frac{i}{2},0,0\Bigr),\quad
\widehat w(0,0,1)=\Bigl(0,-\frac{i}{2},0\Bigr),\quad
\widehat w(1,0,0)=\Bigl(0,0,-\frac{i}{2}\Bigr),
\]

and conjugates. Energy \(E=\|w\|_2^2=3/2\).

---

## Hand computation of \(K_{1,2}\)

Outputs on \(\beta=2\) are the twelve
keys with \(\lvert k\rvert^2=2\), i.e.
permutations of \((\pm 1,\pm 1,0)\).

At \(k=(1,1,0)\) the only live ordered
pair is \(p=(0,1,0)\), \(q=(1,0,0)\).
The bilinear piece is
\(i(\widehat w_p\cdot q)\widehat w_q=(0,0,-i/4)\).
Leray does not change it
(\(k\cdot B=0\)). So
\(\lvert\widehat B_k\rvert^2=1/16\).

Cyclic permutation of axes gives the
same size on every output of shell 2.
Hence

\[
\|\Pi_2 B(w,w)\|_2^2
=
12\cdot\frac{1}{16}
=
\frac{3}{4}.
\]

\[
K_{1,2}(w)
=
\frac{2\cdot(3/4)}{1^2\cdot(3/2)^2}
=
\frac{3/2}{9/4}
=
\frac{2}{3}.
\]

The live evaluator
`K_of_w` reproduces \(2/3\) to
machine precision. That is a check,
not a second claim.

---

## What this does not do

- It does not prove \(K\le 16/9\).
- It does not make \(2/3\) a universal
  constant or \(C_0\).
- It does not replace the weighted
  sphere count.
- It does not kill or repair
  unrestricted ★.
- It does not construct a singular
  NSE solution.

To move exact-shell \(16/9\) from
**CLAIMED** to supported still
requires the closed-form derivation
(specialist pending) or a sweep that
shows nothing approaches \(16/9\).
A clean floor is not that.

---

## Status

| Item | Verdict |
|---|---|
| \(K_{1,2}(w)=2/3\) on this field | **YES.** Hand + evaluator. |
| \(\sup K\ge 2/3\) | **YES.** Floor. |
| \(2/3\) as \(C_0\) or as \(16/9\) | **NO.** |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Unchanged. |
| Unrestricted ★ | **NO.** Other page. |
| Ordinary NS | **OPEN.** |
