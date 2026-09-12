# Swirl wall correction

12 September 2026.
**Not a close. NS not solved.
Occupation decay from the detector is
withdrawn.**

Axisymmetric-with-swirl Navier–Stokes,
unaugmented, on \(\mathbb{R}^3\);
quantities \(F=u^\theta/r\) and
\(G=\omega^\theta/r\); the wall is a
time-window *if*; remainder of the
shell estimate is still
\(T_{j\leftarrow j}\); [no extra field];
the detector does not give occupation
decay.

Operator source
`Swirl_Wall_Correction_2026-09-12.md`
is not on this branch. This page seats
that correction. Filter:
[`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).
Shell estimate:
[`AXISYM-SHELL.md`](AXISYM-SHELL.md).
Probe: `python3 scripts/swirl_wall_correction.py`

Do not start H1. Do not weld ★.
Do not use this wall to close
\(T_{j\leftarrow j}\).

---

## What was wrong in the detector

Three concrete errors.

1. **Variables swapped.** The live
   dictionary is
   \[
   F=\frac{u^\theta}{r},\qquad
   G=\frac{\omega^\theta}{r},\qquad
   \Gamma=ru^\theta=r^2F,\qquad
   U=\frac{u^r}{r}.
   \]
   Swapping \(F\) with \(G\) makes every
   later energy the wrong equation.

2. **Integrating factor.** Wrong sign,
   and \(p\) missing. The exponent that
   belongs with the \(F^p\) compression
   term is
   \[
   \mu(t)=p(1-d)\int^t\overline U_{d,p}(s)\,ds.
   \]
   Here \(\alpha=p(d+1)+1\) and
   \(\overline U_{d,p}\) is the
   \(|F|^p\)-weighted mean of \(U\) on
   \(d\mu_\alpha\). From the identity
   below, \(\dot Z_{\alpha,p}\) carries
   \(p(d-1)\) times that moment, which
   is \(-p(1-d)\) times it. The factor
   \(e^\mu\) cancels that term. A sign
   error reverses amplification and
   damping. Dropping \(p\) is the wrong
   power.

3. **Wall miscopied.** A time integral
   was written as a spatial integral,
   and the threshold lost its square
   root. The source wall is
   \[
   \int_{\sigma-h}^{\sigma}
   \bigl\|(u^r)_-(t)\bigr\|_\infty\,dt
   \le
   2\sqrt{\nu h\log\log(e^e h_0/h)}.
   \]
   It is a conditional criterion over
   time windows. It does not establish
   a five-dimensional spatial
   occupation bound.

Shahmurov, *Hardy Criticality in
Axisymmetric Swirl*,
[arXiv:2605.01875](https://arxiv.org/abs/2605.01875),
§1–2, uses the same \(F,G,U\) and the
five-dimensional Bessel operator
\(\Delta_5\). That paper’s §5 is the
circulation identity at
\(\alpha=2p+1\). It is not occupation
decay. The five-dimensional weight
\(\alpha=3\) is a measure for an
energy, not occupation of a set in
five dimensions.

---

## What is kept

Unaugmented. No extra field.

**Identity (power-weight \(F^p\)).**
For \(p>1\), \(\alpha>1\),
\(Z_{\alpha,p}=\int|F|^p\,d\mu_\alpha\),
\(d\mu_\alpha=r^\alpha\,dr\,dz\),
\(H=|F|^{p/2}\),
\[
\begin{aligned}
\frac1p\dot Z_{\alpha,p}
&+\nu\frac{4(p-1)}{p^2}\int|\nabla H|^2\,d\mu_\alpha
+\nu\frac{(3-\alpha)(\alpha-1)}{p}\int H^2 r^{\alpha-2}\,dr\,dz\\
&=\frac{\alpha-(2p+1)}{p}\int U|F|^p\,d\mu_\alpha.
\end{aligned}
\]
At \(\alpha=p(d+1)+1\) the compression
coefficient is \(d-1\). That is the
identity behind the integrating factor
above. Conditional energy estimate:
after \(e^\mu\), the remaining job is
still the viscous form and whatever
is not absorbed. That is an *if* on
\(\overline U_{d,p}\), not a close.

**Circulation endpoint.** At
\(\alpha=2p+1\) the same identity is
the classical \(L^p\) energy of
\(\Gamma\). No new a priori.

**The wall, as a window.** If the
time-window bound holds on
\([\sigma-h,\sigma]\), that is a
named hypothesis. It is not a spatial
occupation theorem.

**Good-set estimate.** The supplied
good-set estimate remains fixed in
this audit. It is not rewritten here.

---

## What is dropped

If a paragraph needs one of these to
move, the paragraph is out.

- The detector establishes occupation
  decay.
- The wall is a five-dimensional
  spatial occupation bound.
- \(F=\omega^\theta/r\) or
  \(G=u^\theta/r\).
- An integrating factor with the
  opposite sign, or without \(p\).
- A spatial rewrite of the wall, or
  the same threshold without the
  square root.
- A close of \(T_{j\leftarrow j}\),
  of unrestricted regularity, or of
  Lemma★, by this detector.

Visibility of a 5-D Bessel operator
is not uniform smallness of a
remainder.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| SWC_F_G | **pass** | \(F=u^\theta/r\), \(G=\omega^\theta/r\) |
| SWC_IF | **pass** | exponent \(p(1-d)\int\overline U_{d,p}\) |
| SWC_identity | **pass** | power-weight \(F^p\) identity, unaugmented |
| SWC_wall_time | **pass** | wall is a time-window *if* |
| SWC_good_set | **pass** | supplied good-set left fixed |
| SWC_occ_from_detector | **fail** | occupation decay withdrawn |
| SWC_five_d_occupation | **fail** | \(\Delta_5\) is not a 5-D occupation bound |
| SWC_remainder | **fail** | \(T_{j\leftarrow j}\) still open |
| SWC_ns_solved | **fail** | class and the wall *if* stay in the sentence |

NS not solved.
