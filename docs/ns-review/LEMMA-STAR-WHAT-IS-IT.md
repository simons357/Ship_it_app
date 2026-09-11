# What is Lemma★? — fundamental structures

**Audience:** Jonathan (smart non-specialist + researcher)  
**Purpose:** Deep basics — not the picture campaign. Five questions in order.  
**Honesty lock:** ★ **NOT** proved · NS **NOT** solved · kill lane **LIVE**.  
**Canonical math SoT:** [`LEMMA-STAR-ACTUAL-SHAPE.md`](./LEMMA-STAR-ACTUAL-SHAPE.md) · formulas: [`../math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`](../math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md) · code: `scripts/ns_attacks/ns_lemma_star_core.py`

---

## 1. What ARE these structures?

The objects are **smooth incompressible velocity fields** on the 3-torus

\[
\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3.
\]

Think: a periodic box of fluid. No walls. Velocity \(v(x)\) at each point; mass conserved locally means \(\nabla\cdot v=0\) (divergence-free). Mean flow is zero.

In Fourier space each mode has wavevector \(k\in\mathbb{Z}^3\setminus\{0\}\) and coefficient \(v_k\) with \(k\cdot v_k=0\). The Stokes operator (projected Laplacian) is

\[
A=-P\Delta,\qquad (Av)_k=|k|^2\,v_k=\lambda_k\,v_k.
\]

\(A\) measures **how fine-grained** the field is: larger eigenvalues = sharper spatial oscillation.

The nonlinear term (projected advection / cascade)

\[
B(v,v)=P[(v\cdot\nabla)v]
\]

is the geometric “fluid stretches itself” operator. Triads \(p+q=k\) in Fourier space are the transfers between scales.

From \(v\) one builds **spectral moments** (pure \(L^2\) geometry on the shape):

| Symbol | Definition | What it is |
| --- | --- | --- |
| \(E\) | \(\|v\|_2^2\) | total kinetic energy |
| \(X\) | \(\|A^{1/2}v\|_2^2=\sum\lambda_k\|v_k\|^2\) | enstrophy-like (gradient energy) |
| \(Y\) | \(\|Av\|_2^2=\sum\lambda_k^2\|v_k\|^2\) | next spectral moment |
| \(Z\) | \(\|A^{3/2}v\|_2^2=\sum\lambda_k^3\|v_k\|^2\) | next moment |
| \(\Lambda\) | \(Y/X\) | **spectral scale** — mean “how fine” the energy lives |
| \(D_s\) | \(Z-Y^2/X=\|(A-\Lambda)A^{1/2}v\|_2^2\) | **spectral spread** — variance of \(\lambda\) around \(\Lambda\) |
| \(T_c\) | \(-\langle B(v,v),A(A-\Lambda)v\rangle\) | **centered cascade / stretching** — signed transfer that tries to push \(\Lambda\) up |

So: \(E,X,Y,Z,\Lambda\) describe **where energy sits among scales**. \(D_s\) is how **spread** that distribution is (zero on a single shell). \(T_c\) is the **dangerous stretch** relative to that same centering — the part of the cascade that wants to drive the spectral scale toward blowup.

Positive part: \((T_c)_+=\max(T_c,0)\). Only upward stretch enters the danger quotient.

---

## 2. WHERE are they?

| Layer | Location |
| --- | --- |
| **Math domain** | Divergence-free, mean-zero fields on \(\mathbb{T}^3\) (Clay Statement B setting under this packaging) |
| **Geometric home** | Frequency space — shells of \(\lambda_k=|k|^2\), triad transfers \(p+q=k\) |
| **This book’s center** | Shape / \(\mathcal{R}_\star\) packaging (not a side lemma; not a swirl metaphor) |
| **Repo SoT** | `docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md` |
| **Executable formulas** | `scripts/ns_attacks/ns_lemma_star_core.py` (exact finite-support Fourier; \(D_s\) double-checked) |
| **Neighborhood probes** | Attacks 9A–9D — orbits around the center; none killed ★; none proved ★ |

Viscosity \(\nu\) and the time-dependent Navier–Stokes solution \(u(t)\) live in the **outer energy-budget wrapper**. The center claim is about **shapes** \(v\), not about a particular \(\nu\).

---

## 3. WHAT is Lemma★ / \(\mathcal{R}_\star\) packaging?

**Lemma★ is the Millennium problem in this packaging** — not a side lemma.

**Shape form (primary):** there exists a finite geometric constant \(C_{\mathrm{geom}}\) such that for every smooth nonzero divergence-free \(v\) on \(\mathbb{T}^3\),

\[
\boxed{
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
D_s(v)\,
\|v\|_2^2\,
Y(v).
}
\]

Equivalently (when \(D_s E Y>0\)):

\[
\boxed{
\sup_v\,\mathcal{R}_\star(v)<\infty,
\qquad
\mathcal{R}_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,E\,Y}.
}
\]

In words: **stretching cannot outrun spectral spread by more than one universal shape constant**, for **all** smooth shapes.

If \(D_s=0\) (pure single shell), the field cannot stretch in this centering (\(T_c=0\)); that case is vacuous, not a kill.

**Viscosity packaging (derived wrapper):** for \(0<\theta<1\),

\[
T_c(u)\le\theta\nu D_s(u)+C_0(\theta)\nu^{-1}\|u\|_2^2 Y(u),
\qquad C_{\mathrm{geom}}=4\theta C_0(\theta).
\]

Young in \(\nu\) recovers the energy-budget form from the shape form. Viscosity is outer bookkeeping; the hard claim is the uniform bound on \(\mathcal{R}_\star\).

**Why this packages Clay B:** if ★ holds, the dangerous spectral scale \(\Lambda\) cannot blow up in finite time → enstrophy stays controlled → global regularity on \(\mathbb{T}^3\). Packaging right ≠ prize won. ★ is **open**.

**Not the full lemma:** the near-shell family \(K_{\alpha,\beta}\) is a **restricted limiting probe**, not full ★. Bounded \(K\) on that family does not prove \(\sup\mathcal{R}_\star<\infty\).

---

## 4. HOW does it work?

**Mechanism in one chain:**

1. Read the fluid as a **shape in frequency space** (moments \(E,X,Y,Z\) → scale \(\Lambda\) and spread \(D_s\)).
2. Measure **centered stretching** \(T_c\) — the cascade’s attempt to drive \(\Lambda\) up.
3. Form the dimensionless danger score \(\mathcal{R}_\star=(T_c)_+^2/(D_s E Y)\).
4. Lemma★ asserts that score is **uniformly bounded** over all smooth shapes.
5. Boundedness ⇒ finite \(C_{\mathrm{geom}}\) ⇒ (via the \(\nu\)-wrapper) spectral scale controlled in the NSE energy budget ⇒ no finite-time blowup **in this packaging**.

**What cancels under amplitude \(u=av\):** replace \(v\) by \(av\). Then

\[
E\sim a^2,\quad X,Y,Z,D_s\sim a^2,\quad T_c\sim a^3
\]

(triad is quadratic in velocity, then one more factor from the weights). Numerator \((T_c)_+^2\sim a^6\); denominator \(D_s E Y\sim a^6\). Ratio \(\mathcal{R}_\star\) is **amplitude-invariant**. Size is not the problem; shape is.

**What the outer \(\nu\) wrapper does:** after amplitude optimization, Young’s inequality absorbs viscosity into \(\theta\nu D_s + C\nu^{-1}(\cdots)\). The shape inequality is what remains. That is why ★ is called a **shape statement**.

**How the campaign used this:** Attacks 9A–9D probed neighborhoods (AP packets, near-shell \(K_{\alpha,\beta}\), fixed-gap spheres, locked-phase stubs). Language: those probes **did not kill ★**. They also did **not** prove ★. Finite small samples ≠ supremum. Kill lane remains **LIVE** (need either a true blowing family for \(\mathcal{R}_\star\), or a triadic proof of the uniform bound — HH→L / PRODUCT-BLOCK still open).

---

## 5. Is it scale invariant?

Short answer: **\(\mathcal{R}_\star\) is amplitude-invariant and uniform-dilation-invariant. Viscosity cancels in the shape form. Full spacetime NSE is not “scale-free” in the naive PDE sense — the claim that matters here is about shape.**

| Transformation | What happens | \(\mathcal{R}_\star\) |
| --- | --- | --- |
| **Amplitude** \(v\mapsto a v\) | Size up/down; moments and \(T_c\) scale as above | **Invariant** |
| **Uniform Fourier dilation** (rescale all wavevectors by the same factor, normalize) | Moves the whole spectrum to finer/coarser shells together | **Invariant** |
| **Viscosity** \(\nu\) | Appears in the energy-budget wrapper; cancelled under \(u=av\) size optimization | **Not in the shape quotient** |
| **Non-uniform reshaping** (change relative shell weights, phases, triad geometry) | Changes spread vs stretch | **Not invariant** — this is the actual content of ★ |
| **Near-shell restriction** \(K_{\alpha,\beta}\) | Only a slice of shape space | **Not** a substitute for full \(\sup\mathcal{R}_\star\) |

So: “scale invariant” in the precise sense used here means **the danger score does not care about overall loudness or overall uniform zoom of the Fourier support**. It cares about **relative geometry** — how stretch sits against spectral spread. That is why viscosity is an outer wrapper and why greening a few numeric fields cannot close ★.

---

## Status (one card)

| Claim | Truth |
| --- | --- |
| What is ★? | Uniform bound on \(\mathcal{R}_\star\) (shape form) ≡ Millennium packaging of Clay B here |
| Proved? | **No** |
| NS solved? | **No** |
| Kill lane? | **LIVE** |
| \(K_{\alpha,\beta}\)? | Restricted near-shell family only ≠ full ★ |
| Attacks 9A–9D? | Neighborhood probes; **did not kill ★**; did not prove ★ |

**Center = shape / \(\mathcal{R}_\star\) packaging. Door still locked.**

---

## Related (other branches / PRs)

Picture campaign and English barycenter live on the campaign / English branches (not required to read this card). Energy-budget + PRODUCT-BLOCK: `LEMMA-STAR-DA-NS-1.md` on the DA-NS-1 packaging branch. Exact Fourier lock-in: `LEMMA-STAR-EXACT-FORMULAS.md` / `domain_architect/rstar_quantities.py` on the R★ formulas branch.
