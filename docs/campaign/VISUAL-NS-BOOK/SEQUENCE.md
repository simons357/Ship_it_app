# Lesson sequence — Visual NS Book

Each lesson: **hero image** → **one short plain-language explanation** → optional **what the equation means** → **honesty line**.

Image paths are relative to the repo root. Prefer the listed file; aliases are in [`IMAGE-INVENTORY.md`](./IMAGE-INVENTORY.md).

---

## 01 — What is Navier–Stokes?

| | |
| --- | --- |
| **Hero** | `docs/ns-review/assets/lemma-campaign/t3_torus_shape_render.png` |
| **Plain** | Imagine arrows filling a wrap-around box: at every point, “which way is the fluid going?” Navier–Stokes is the standard continuum model for a sticky, incompressible fluid — Newton’s laws written as PDEs. Our math question lives on that ideal model (here a 3-torus), not on a photograph of water. |
| **Equation box (optional)** | \(\partial_t u + \mathbb{P}((u\cdot\nabla)u)=\nu\Delta u\), \(\nabla\cdot u=0\). Left: velocity changes because flow pushes flow. Right: viscosity smooths. Pressure (inside \(\mathbb{P}\)) keeps the fluid from compressing. |
| **Honesty** | This book is a map of a question, not a claim that the question is answered. |

Full card: [`chapters/01-what-is-navier-stokes.md`](./chapters/01-what-is-navier-stokes.md)

---

## 02 — Why it matters

| | |
| --- | --- |
| **Hero** | `docs/ns-review/visual-journey/figures/proof-chain.png` |
| **Plain** | Engineers use Navier–Stokes every day (weather, pipes, aircraft, blood flow). The Clay Millennium question asks something sharper: can the *ideal* smooth equations develop an infinite spike of spin in finite time? Mapping that question carefully is useful even before anyone closes it — a clean floor plan helps the next person who walks in. |
| **Equation box (optional)** | Skip formulas on Skool. On Substack: “regularity” means the solution stays smooth for all positive times; “blowup” means some size (usually gradients / spin) goes to infinity in finite time so the smooth solution cannot continue. |
| **Honesty** | Caring about the map ≠ claiming the prize. We do not stamp “solved.” |

Full card: [`chapters/02-why-it-matters.md`](./chapters/02-why-it-matters.md)

---

## 03 — The floor plan (where the study stands)

| | |
| --- | --- |
| **Hero** | `docs/ns-review/visual-journey/figures/proof-chain.png` |
| **Plain** | Think of Navier–Stokes as a house. This picture is the floor plan of **what our study has mapped so far**: definitions, identities, packaging, and one last open door drawn as dashed math. Solid rooms = named objects. Dashed warm nodes = estimates still needed. |
| **Equation box (optional)** | Trunk sketch: NSE on \(\mathbb{T}^3\) → moments \(E,X,Y,Z\) and scale \(\Lambda=Y/X\) → spread \(D_s\) and centered stretch \(T_c\) → Lemma★ packaging → product / shape bound (open) → continuation (conditional). |
| **Honesty** | Dashed doors are open. The map is not upstairs finished. |

Full card: [`chapters/03-floor-plan.md`](./chapters/03-floor-plan.md)

---

## 04 — This room: the barycenter

| | |
| --- | --- |
| **Hero** | `docs/ns-review/assets/lemma-campaign/lemma-star-barycenter.png` |
| **Plain** | In frequency space, spin lives across big swirls and tiny swirls. The **barycenter** \(\Lambda\) is the center of mass of that spin. We are standing in that room: stretch vs spread is measured *around that center*, not around zero. That is “where we are” relative to the map. |
| **Equation box (optional)** | \(\Lambda=Y/X\) — enstrophy-weighted mean eigenvalue. Spread \(D_s=Z-\Lambda Y\ge 0\). Centered stretch \(T_c=-\langle B(v,v),A(A-\Lambda)v\rangle\). |
| **Honesty** | Being in the room means the bookkeeping is correctly centered. It does **not** mean the last door is open. |

Full card: [`chapters/04-barycenter.md`](./chapters/04-barycenter.md)

---

## 05 — Tug-of-war: stretch vs spread

| | |
| --- | --- |
| **Hero** | `docs/ns-review/assets/lemma-campaign/03-tug-of-war-stretch-vs-spread.png` |
| **Plain** | Two forces compete at the barycenter. **Stretch** (\(T_c\)) tries to pump energy toward finer scales. **Spread** (\(D_s\)) measures how smeared the spin is away from the center. If stretch permanently wins, the center can race away — that is the danger this packaging watches. |
| **Equation box (optional)** | Shape score \(\mathcal{R}_\star=(T_c)_+^2/(D_s\, E\, Y)\). Lemma★ says this dimensionless score stays geometrically controlled for every smooth shape — **as a hypothesis**, not a theorem. |
| **Honesty** | Uniform control of \(\mathcal{R}_\star\) is still **OPEN** (PRODUCT-BLOCK). Pictures of tug-of-war are intuition, not closure. |

Full card: [`chapters/05-tug-of-war.md`](./chapters/05-tug-of-war.md)

---

## 06 — Shape is not size

| | |
| --- | --- |
| **Hero** | `docs/ns-review/assets/lemma-campaign/02-shape-ne-size.png` |
| **Plain** | Crank the amplitude of the whole field: the shape score is built so overall loudness cancels. What’s left is geometry among shells — relative arrangement of swirls, not how hard you turn the volume knob. Same idea for uniform Fourier dilation. |
| **Equation box (optional)** | Under \(v\mapsto a v\), numerator and denominator of \(\mathcal{R}_\star\) scale the same way. Uniform dilation likewise leaves the quotient unchanged. That is why we talk about **shape**, not raw size. |
| **Honesty** | Scale invariance of the score does not prove the score is bounded. Boundedness is the open door. |

Full card: [`chapters/06-shape-not-size.md`](./chapters/06-shape-not-size.md)

---

## 07 — The last door on this floor

| | |
| --- | --- |
| **Hero** | `docs/ns-review/visual-journey/figures/chain-status-card.png` |
| **Plain** | The last door = prove the shape score stays finite for every smooth field (\(\sup_v\mathcal{R}_\star<\infty\)), or an equivalent product-scale bound on centered stretch. Energy-only 3D products do not finish it; high×high triads are the live stress. We describe the door. We do not announce we walked through. |
| **Equation box (optional)** | Target: \(\sup_v\mathcal{R}_\star(v)<\infty\). Live routes include HH-channel control, HL/LL dilation-invariant estimates, structure on \(T_c\), and a live kill search for families with \(\mathcal{R}_\star\to\infty\). |
| **Honesty** | PRODUCT-BLOCK is **OPEN**. Clay Statement B is **not solved**. A Monday sprint will not close Clay. |

Full card: [`chapters/07-last-door.md`](./chapters/07-last-door.md)

---

## 08 — What “blowup” means (and does not)

| | |
| --- | --- |
| **Hero** | `docs/ns-review/assets/lemma-campaign/03-tug-of-war-stretch-vs-spread.png` |
| **Plain** | Blowup ≠ explosion ≠ Big Bang. In PDEs it means some size (usually spin / gradients) goes to infinity in **finite time**, so the smooth mathematical solution cannot continue. Theoretical singularity of the equations — not a claim about the universe ending. |
| **Equation box (optional)** | Along strong solutions the spectral-shift identity \(\Lambda'=2(T_c-\nu D_s)/X\) tracks how the barycenter moves. That identity is bookkeeping. It is **not** the Lemma★ bound and does not by itself imply regularity. |
| **Honesty** | Explaining blowup carefully is education. It is not evidence that blowup happens — or that it doesn’t. |

Full card: [`chapters/08-blowup.md`](./chapters/08-blowup.md)

---

## 09 — Viscosity as wrapper (optional depth)

| | |
| --- | --- |
| **Hero** | `docs/ns-review/assets/lemma-campaign/06-viscosity-melts-wrapper.png` |
| **Plain** | Viscosity is the sticky part that melts sharp features. In the energy-budget packaging it sits in an outer wrapper: part of stretch is absorbed by spread scaled by \(\nu\), and a remainder pays a geometric cost. After optimizing that trade, the hard content is still the shape bound. |
| **Equation box (optional)** | \(T_c\le\theta\nu D_s+C_0(\theta)\nu^{-1} E Y\). Finite geometric \(C_0\) is equivalent (up to constants) to uniform \(\mathcal{R}_\star\) — and is still hypothesized. |
| **Honesty** | Pure “viscosity eats everything” without a geometric remainder is **dead**. The wrapper form is bookkeeping around an open constant. |

Full card: [`chapters/09-viscosity-wrapper.md`](./chapters/09-viscosity-wrapper.md)

---

## 10 — Recap: map, not proof

| | |
| --- | --- |
| **Hero** | `docs/ns-review/assets/lemma-campaign/lemma-star-barycenter.png` |
| **Plain** | Week / series in one breath: fluid model → house floor plan → barycenter room → tug-of-war → shape ≠ size → last door still open. Math is awesome when you can say what the symbols *mean*. You’re invited to walk the map. You’re not being sold a trophy. |
| **Equation box (optional)** | Point curious readers to `docs/ns-review/SCIENTIFIC-REPORT.md` (scientific face) and `docs/ns-review/PROOF-CHAIN-CLEAN.md` (definitions). |
| **Honesty** | Visual book = education / map. **Not a proof.** NS not solved. |

Full card: [`chapters/10-recap-map-not-proof.md`](./chapters/10-recap-map-not-proof.md)
