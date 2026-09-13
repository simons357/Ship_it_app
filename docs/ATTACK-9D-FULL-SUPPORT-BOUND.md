# Exact-shell 9D — claimed full-support bound

12 September 2026; internal-audit line 13 September 2026.
Unaugmented NS on \(\mathbb{T}^3\);
quantity is \(K_{\alpha,\beta}(w)\) for
\(Aw=\alpha w\);
remainder is occupancy \(s\);
the claimed bound removes that factor
on a single input shell.

**CLAIMED:** written derivation available;
internal checks passed; independent
specialist review pending. Numerical
sweeps provide consistency checks only.

No reviewer is named on this page.
No date is booked. A list of possible
later readers is not an assignment.
Soft X silent.

### Limitation (read this first)

| This page claims | This page does not claim |
|---|---|
| A bound for \(Aw=\alpha w\) on **one input shell** | A bound for a general multi-shell field |
| Occupancy \(s\) gone **if** \(K\le 16/9\) holds | A continuation criterion |
| Written algebra/geometry for that shell | Unrestricted \(\star\), or a repair of \(\star\) |
| Internal audit + symbolic checks | Independent specialist sign |

Unrestricted \(\star\) is a different statement.
Its counterexample is the growing-layer
family \(v_n\)
([`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md)).
This page does not resurrect that box.
A true \(4/3\) does not kill or repair it.

If \(K\le 16/9\) holds, occupancy \(s\) is
gone on a **single input shell**. That is a
written bound on exact-shell fields, not a
sweep maximum. The three-shear field then
sits under a named ceiling, not under a
rumor. The coefficient comes from algebra
and geometry, not from search results.

**No as a regularity close.** A true
\(4/3\) does not kill or repair unrestricted
★. That box is already dead by the
multi-shell family \(v_n\). It does not
give a continuation criterion and it does
not restore ★ \(\Rightarrow\) global
regularity. Ordinary NS stays open.

An internal audit of the exact-shell
argument found no gap. The named verifier
also passes its symbolic checks. That is
an internal audit. Independent specialist
review remains pending. Soft X silent.
NS is not solved.

Designed \(\Theta(m^2)\) 9D stays **NO**.
`attack9d_theta_m2_locked_phase.py` was not written.
Grow-\(s\) samples stay historical.
Do not cash \(0.456\) or \(0.641\) as \(C_0\).

Machine: `scripts/ns_attacks/verify_pr24_closure_review.py`.
That script checks the symbolic identity
and compares growing-layer calculations
with the evaluator. It reads the saved
sweep summary. It does **not** perform the
shell-count experiments on this page.
Math pointer: [`docs/math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md`](math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md).
Grow-\(s\) page: [`ATTACK-9D-GROW-S.md`](ATTACK-9D-GROW-S.md).

The next review is concrete: verify the
weighted incidence argument (factor \(3\),
derived below on this page) and the
Hermitian residual estimate. Do not
import the Ring Lemma or Borromean triad
count. Those are other statements.

---

## Conventions

Normalized torus measure on \(\mathbb{T}^3\).
Fourier coefficients are \(\mathbb C^3\)-valued.
The inner product used on polarizations is
Hermitian: \(\lvert\langle u,v\rangle\rvert\le\lvert u\rvert\,\lvert v\rvert\)
for \(u,v\in\mathbb C^3\). That is the
Cauchy–Schwarz that is claimed to survive
independently complex polarizations. It is
not a real-alignment hypothesis.

The ratio \(K_{\alpha,\beta}(w)\) is defined
only for \(\alpha>0\) and \(w\ne 0\):

\[
K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\,\|w\|_2^4},
\qquad
Aw=\alpha w.
\]

\(P\) and \(P_k\) on this page are the
Leray projector. \(B(w,w)=P[(w\cdot\nabla)w]\).

Admissible \((\alpha,\beta)\) for a
nonvacuous pair on one input shell:

\[
\alpha>0,\qquad 0<\beta\le 4\alpha.
\]

The geometric constraint is
\(\lvert p+q\rvert\le 2\sqrt{\alpha}\), so
\(\beta>4\alpha\) admits no pairs and
\(\Pi_\beta B(w,w)=0\). The \(C=4/3\) form
uses \(\beta>0\). At the endpoints of
\(x=\beta/\alpha\in(0,4]\), the elementary
majorant below is \(0\).

**Boundary \(\beta\to 4\alpha\).** Write
\(\gamma=\sqrt{\beta(1-\beta/(4\alpha))}\).
Then \(\gamma\to 0\). Every pair estimate
on this page is of the form
\(\lvert\,\cdot\,\rvert\le\gamma\,\lvert w_p\rvert\,\lvert w_q\rvert\).
Nothing divides by \(\gamma\) or by
\(1-\beta/(4\alpha)\). The \(C=4/3\) form
divides by \(\sqrt{\beta}\), and
\(\beta\to 4\alpha>0\), so that factor
stays bounded. The case \(\beta=0\) is
already excluded from \(K\) and from the
pair geometry.

---

## Claimed bound

For \(Aw=\alpha w\),

\[
\|\Pi_\beta B(w,w)\|_2
\le
\frac{4}{3}\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\qquad
\beta>0.
\]

Equivalently \(K_{\alpha,\beta}(w)\le 16/9\).
Both supports may grow. Each transverse
polarization may have independent complex
coefficients. Optimality of the constant is
not claimed.

For \(\beta>4\alpha\) no pairs occur:
\(\lvert p+q\rvert\le 2\sqrt{\alpha}\).

This does not control an arbitrary simultaneous
finite-closer limit, and it does not control
a general multi-shell field. The growing-layer
family is multi-shell. No contradiction.

---

## Geometry on one input shell

Fix \(p+q=k\), \(\lvert p\rvert^2=\lvert q\rvert^2=\alpha\),
\(\lvert k\rvert^2=\beta\). Then
\(k\cdot p=k\cdot q=\beta/2\) and
\[
\lvert k_\perp\rvert^2
=
\beta-\frac{\beta^2}{4\alpha}
=
\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr).
\]
Because \(w_p\perp p\),
\[
\lvert k\cdot w_p\rvert
\le
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}\,|w_p|.
\]
The Fourier bilinear on the locked evaluator is
\[
\widehat B_k
=
i\,P_k\sum_{p+q=k}(q\cdot w_p)w_q
=
i\,P_k\sum_{p+q=k}(k\cdot w_p)w_q.
\]
A crude pair bound with \(\lvert P_k w_q\rvert\le|w_q|\)
returns occupancy.

---

## Symmetrized interaction

The step that removes occupancy is the
symmetrized interaction. For \(p+q=k\)
on the specified shells,

\[
\left|P_k\!\left[(q\cdot w_p)w_q+(p\cdot w_q)w_p\right]\right|
\le
\sqrt{\beta\left(1-\frac{\beta}{4\alpha}\right)}
\,|w_p|\,|w_q|.
\]

The inner product on polarizations is
Hermitian,
\(\langle u,v\rangle=\sum_{j=1}^3 \overline{u_j}v_j\).
For every \(u,v\in\mathbb C^3\),
\(\lvert\langle u,v\rangle\rvert^2\le\lvert u\rvert^2\lvert v\rvert^2\).
No reality or alignment is used.

After \(P_k\), the in-plane parts cancel
by the real geometry of \(k,p,q\). The
residual is a single complex multiple of
a real unit vector \(e_\perp\perp k\):
\(\zeta e_\perp\) with \(\zeta\in\mathbb C\).
Then
\(\lvert P_k[(q\cdot w_p)w_q+(p\cdot w_q)w_p]\rvert=\lvert\zeta\rvert\),
and Hermitian Cauchy–Schwarz on the
remaining coefficients gives
\(\lvert\zeta\rvert\le\gamma\lvert w_p\rvert\lvert w_q\rvert\).
Saturation is not claimed. Independently
complex transverse coefficients stay
inside this inequality because it never
used \(\mathrm{Im}=0\).

The complete kernel cancellation is in
§3 of the underlying proof. This page
does not replace that calculation.

The ordered convolution equals half its
symmetrization. Squaring contributes
\(1/4\); the weighted count contributes
\(3\). Together,

\[
\|\Pi_\beta B(w,w)\|_2^2
\le
\frac34\beta\left(1-\frac{\beta}{4\alpha}\right)\|w\|_2^4.
\]

---

## One-variable maximum (redo by hand)

Assume the displayed \(L^2\) majorant and
the constraint \(x=\beta/\alpha\in(0,4]\).
Then

\[
K_{\alpha,\beta}(w)
\le
f(x)
:=
\frac34 x^2\Bigl(1-\frac x4\Bigr)
=
\frac34\Bigl(x^2-\frac{x^3}4\Bigr).
\]

Differentiate:

\[
f'(x)=\frac34 x\Bigl(2-\frac{3x}4\Bigr).
\]

Critical points in \((0,4]\): \(x=8/3\).
Endpoints: \(f(x)\to 0\) as \(x\to 0^+\),
and \(f(4)=0\). The interior value is

\[
f\Bigl(\frac83\Bigr)
=
\frac34\cdot\frac{64}9\cdot\Bigl(1-\frac23\Bigr)
=
\frac{16}9.
\]

So, **given** the claimed pointwise
majorant and \(\beta\le 4\alpha\),

\[
K_{\alpha,\beta}(w)\le\frac{16}9.
\]

The ratio \(x=8/3\) lies strictly inside
the geometric interval. It is not a
missing-boundary accident of dropping
\(\beta\le 4\alpha\).

The equivalent form
\(\|\Pi_\beta B\|_2\le\frac43\alpha\beta^{-1/2}\|w\|_2^2\)
is \(\sqrt{16/9}=4/3\) for \(\beta>0\).
Optimality of the constant is not claimed.

This paragraph checks only the
optimization step. It does not certify
§3. Independent specialist review should
redo the kernel identity, the Hermitian
step, the factor \(3/4\), the weighted
incidence argument, this derivative,
and the limiting-closer scope. DA has
not replaced that by a proof assistant.

---

## Weighted count (factor \(3\), on this page)

Let \(S\subset\{p:\lvert p\rvert^2=\alpha\}\),
\(a_p\ge 0\), \(M=\sum_{p\in S}a_p^2\), and
\(c_k=\sum_{p+q=k}a_p a_q\).
The lattice inequality used above is

\[
\sum_{\lvert k\rvert^2=\beta}c_k^2
\le
3M^2.
\]

This count is derived here. It is **not**
the Ring Lemma and **not** a Borromean
triad count. Do not import those.

Expand the square. A pair \((p,r)\)
contributes only at outputs \(k\) with
\(\lvert k\rvert^2=\beta\) and
\(k\cdot p=k\cdot r=\beta/2\).
Write \(K(p,r)\) for that set of \(k\).

- If \(p\) and \(r\) are linearly independent,
  two affine planes meet the sphere
  \(\lvert k\rvert^2=\beta\) in at most two
  points: \(\lvert K(p,r)\rvert\le 2\).
- If \(r=\lambda p\) and
  \(\lvert p\rvert^2=\lvert r\rvert^2=\alpha\),
  then \(\lambda=\pm 1\). The case \(r=p\)
  is the diagonal: \(\lvert K(p,p)\rvert\le 1\).
  The case \(r=-p\) forces \(\beta=0\),
  which is excluded: \(K(p,-p)=\emptyset\).

So a fixed distinct pair meets at most
two outputs. Weighted AM-GM on each
surviving summand bounds the
off-diagonal contribution by \(2M^2\).
The diagonal is at most \(M^2\).
Total factor \(3\).

**Reviewer flag.** Redo the AM-GM sum
and the plane-sphere incidence. A
printed ratio \(\le 3\) on a sample
shell is a consistency check, not this
argument.

---

## Exact three-shear example and historical numbers

The exact three-shear field attains

\[
K=\frac23
\]

by direct evaluation on that field.
This is an identity, not a search result.

**Sanity, not sharpness.**
\(\frac23\approx 0.667 < 16/9\approx 1.778\).
The exact example sits **strictly inside**
the claimed upper bound. It is a lower
example. It does not prove the upper
bound and it does not claim that
\(16/9\) is sharp.

Historical numerical consistencies
(not the bound, not \(C_0\)):

- random exact-shell fields on
  \((4,8)\), \((5,4)\), \((9,4)\), \((16,32)\),
  \((1,2)\): \(K\le 0.456<16/9\);
- aligned 9B: \(K\approx 0.641<16/9\);
- grow-\(s\) max: \(K\approx 0.456<16/9\).

Those numbers sit. They are not the proof.
They are not near \(16/9\approx 1.778\).
That does not unclaim the bound.

---

## Status

| Item | Verdict |
|---|---|
| Designed \(\Theta(m^2)\) 9D | **NO.** Dead. |
| Grow-\(s\) finite max as \(C_0\) | **NO.** Historical. |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Written derivation available; internal checks passed; independent specialist review pending. Occupancy \(s\) gone on one input shell if it holds. |
| Admissible \((\alpha,\beta)\) | \(\alpha>0\), \(0<\beta\le 4\alpha\) for a nonvacuous pair. \(\beta>4\alpha\) is empty. |
| One-variable max of \(f(x)=\frac34 x^2(1-x/4)\) on \((0,4]\) | Elementary: \(16/9\) at \(x=8/3\). Redo by hand. Does not certify §3. |
| Numerical sweeps | Consistency checks only. Not an alternative path to the word. |
| Sweep max \(0.641\) / \(0.456\) as the ceiling | **NO.** Not the bound. |
| Exact three-shear \(K=2/3\) | Identity on that field. Sits under \(16/9\). Not the ceiling. |
| True \(4/3\) as a regularity close | **NO.** Does not repair ★. No continuation. |
| Unrestricted ★ | **NO.** Dead by \(v_n\). |
| Ordinary NS | **OPEN.** |
| \(2/3\) vs \(16/9\) | Lower example strictly inside claimed upper bound. Not sharpness. Not a proof of \(16/9\). |
| \(\beta\to 4\alpha\) | \(\gamma\to 0\). No division by \(\gamma\). \(\sqrt{\beta}\) stays positive. |
| Factor \(3\) | Derived on this page from incidence + AM-GM. Not Ring / Borromean. |
| Independent specialist sign | **pending.** No name. No date. Soft X silent. |
| Named verifier | Symbolic identity and growing-layer vs evaluator. Reads the saved sweep summary. Does not run the shell-count experiments on this page. |

NS not solved.
