# Lemma★ — next (Attack 6)

10 September 2026. Ideas, then a probe. **Not a proof. NS not solved.**

Locked statement: [`LEMMA-STAR.md`](LEMMA-STAR.md).
Calculator: `scripts/ns_attacks/stokes_moments.py`.
Probe: `python3 scripts/ns_attacks/attack6_scale_law.py`

---

## Ideas (honest)

1. **Do not chase a uniform pre-Young \(C\).**
   Geometry-only \(C\) in \(|T_c|\le C\|u\|_2 X\Lambda\) cannot depend
   on the highest wavenumber. The five-lane max already sat on
   a scaled triad (`sep_32`). If \(|R_{\mathrm{pre}}|\) grows with
   \(s\), that door is dead. Measure the law. Do not draw more
   random samples at \(k_{\max}=8\).

2. **The exact ★ remainder is \(\mathcal R_\star\), not \(C_*\).**
   Optimizing ★ over amplitude is the boxed ratio
   [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md). \(C_*\)
   (\(|T_c|\le C_* X^{3/2}\Lambda\)) is a different sufficient
   door for DA-NS-2. Do not treat a bounded \(C_*\) sample as
   a bound on \(\mathcal R_\star\). HH→L is still the gap.

3. **Coherent HH→L fan.**
   Many high pairs with the same sum. Product estimates lose a
   count of pairs. If they add in \(T_c\), they could kill \(C_*\).
   A fan with frozen polarization is not a test; \(T_c=0\) there
   is an accident, not a bound.

Do not revive K=0. Do not glue H1. Do not add \(K(t)\) to the PDE.
Do not cash a bounded ratio as \(C_0\).

---

## What ran

Scaled resonant triad \(k\mapsto s k\), \(s=1,2,4,8,16,32,48,64\),
best of 24 random phases plus the default, unit amplitude.
Then a coherent fan \(N=2,4,8,12,16\) with frozen seeds
(uninformative; see below).

---

## What it showed

On the scaled triad:

| \(s\) | \(\lvert R_{\mathrm{pre}}\rvert\) | \(\lvert R_{\mathrm{pre}}\rvert/s\) | \(\lvert R_{C_*}\rvert\) |
|---|---|---|---|
| 1 | 0.157 | 0.157 | 0.0401 |
| 2 | 0.314 | 0.157 | 0.0401 |
| 4 | 0.637 | 0.159 | 0.0406 |
| 8 | 1.262 | 0.158 | 0.0403 |
| 16 | 2.540 | 0.159 | 0.0405 |
| 32 | 5.093 | 0.159 | 0.0406 |
| 48 | 7.608 | 0.158 | 0.0405 |
| 64 | 10.123 | 0.158 | 0.0404 |

**Pre-Young door is dead as a uniform estimate.**
\(\lvert T_c\rvert/(\|u\|_2 X\Lambda)\simeq 0.158\,s\to\infty\) as \(s\to\infty\).
A geometry-only \(C\) independent of \(u\) does not exist for
\(|T_c|\le C\|u\|_2 X\Lambda\). The five-lane “survive” used a
crude threshold \(10^3\) on that ratio. The law already kills
uniform \(C\). It does not kill the \(C_*\) form.

**\(C_*\) survives this family.**
\(\lvert T_c\rvert/(X^{3/2}\Lambda)\simeq 0.0404\), independent of \(s\).
That is the remainder to try to prove. It is not a theorem.
One triad shape is not all divergence-free fields.

**Fan:** \(T_c=0\) at every \(N\) with those polarizations.
That is not a bound. Do not rerun it frozen. If you probe a
fan again, randomize phases.

---

## What to write next

Lemma★ **is** a uniform bound on
\[
\mathcal R_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}
{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)}.
\]
Prove it from triadic geometry or cancellation, or kill
it with a family where \(\mathcal R_\star\to\infty\).
File: [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md).

Door 1 (uniform pre-Young \(C\)) is off. K=0 stays dead.
The \(C_*\) remainder \(|T_c|\le C_* X^{3/2}\Lambda\) is a
different sufficient attack on DA-NS-2, not the boxed
form. Do not cash a bounded sample as \(C_0\).

H1 on a cylinder is a different integral. Do not merge.
