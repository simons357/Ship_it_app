# Independent audit — Simons Φ-renorm swirl paper (22 Aug 2026)

**Authority:** user-pasted independent audit of `Simons_PhiRenorm_Swirl_2026-06-30` (treat as definitive).  
**Do not:** close the strain bound, soften the open problem, claim NS / Clay solved, or scrape personal commentary beyond this audit text.

**Sources in this repo**

| File | Role |
| --- | --- |
| [`docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-06-30.tex`](../papers/swirl/Simons_PhiRenorm_Swirl_2026-06-30.tex) | June 30 SoT TeX (relabeled) |
| [`docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-06-30.pdf`](../papers/swirl/Simons_PhiRenorm_Swirl_2026-06-30.pdf) | Recompiled face with \(\dot H^{1.3}\) (upload pack for Zenodo `21071991`; live Zenodo PDF may still be pre-relabel until token apply) |
| [`docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-08-22.tex`](../papers/swirl/Simons_PhiRenorm_Swirl_2026-08-22.tex) | Companion Part D note with \(\dot H^{1.3}\) and \(r^3\) energy already in place |
| [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md) | KEEP / PARK honesty card (separate from Lemma★) |

---

## KEEP findings (unchanged math)

1. **Phi equation CORRECT** — `lem:Phieq` is the classical equation for \(\Phi=u^\theta/r\). No spurious \(-\Phi/r^2\) term. Left as written.
2. **Lions bookkeeping CORRECT** — \(\beta=0.6\) gives dissipation order \((\beta+2)/2=1.3>5/4\). Left as written.
3. **Barrier UNCHANGED** — uniform-in-\(\eps\) control of \(\|u^r/r\|_{L^\infty}\) remains open and is equivalent in difficulty to axisymmetric-with-swirl global regularity. `op:gronwall` left as stated. This paper is a **conditional** reduction — **not** a global regularity proof, **not** Clay closed.

---

## REAL ERROR (relabel, not repair)

**Mistake.** Energy / dual norms were labeled \(\dot H^{2.6}\). Testing \(\eps(-\Delta)^{1.3}u\) against \(u\) produces \(\eps\|u\|_{\dot H^{1.3}}^2\). The number \(2.6\) is the operator composition order, not the energy norm.

**Sites (June 30 TeX line numbers):** 408, 415, 426, 522, 561, 675, 768, 820–823, 907.

**Change applied:** every \(\dot H^{2.6}\) → \(\dot H^{1.3}\) (including \(\dot H^{2.6}_r\)).

**Duality (lines 768, 820–823):** now
\[
\bigl|\langle\eps(-\Delta)^{1.3}u,\varphi\rangle\bigr|
\le\eps\|u\|_{\dot H^{1.3}}\|\varphi\|_{\dot H^{1.3}},
\]
which matches \(\langle(-\Delta)^{1.3}u,\varphi\rangle=\langle(-\Delta)^{0.65}u,(-\Delta)^{0.65}\varphi\rangle\). Compactness still closes; the test function needs less regularity than the old (incorrect) pairing suggested.

---

## OPTIONAL (\(r^3\) measure)

Audit item 4: rewrite the \(\Phi\) energy in \(r^3\,\mathrm{d}r\,\mathrm{d}z\) (self-adjoint \(\mathcal{L}_4\), no axis boundary term).

**Disposition in this PR**

- June 30 TeX: **not** rewritten (audit says optional; mandatory work is the \(\dot H\) relabel). Section structure stays the \(r\,\mathrm{d}r\,\mathrm{d}z\) face with the explicit axis boundary term.
- August 22 companion TeX: already carries the clean \(r^3\) identity \((*)\) and leaves the strain barrier open under `eq:B1` / `lem:gronwall`. Use that file for the \(r^3\) packaging; do not conflate it with Lemma★ PRODUCT-BLOCK.

---

## What changed in this branch

| Item | Status |
| --- | --- |
| Deposit June 30 TeX + PDF | Done |
| \(\dot H^{2.6}\to\dot H^{1.3}\) at all listed sites | Done |
| Dual pairing at 768 / 820–823 | Done (\(\dot H^{1.3}\)) |
| `lem:Phieq` | Untouched (KEEP correct) |
| Lions \(\beta=0.6\) | Untouched (KEEP correct) |
| `op:gronwall` / \(\|u^r/r\|_\infty\) barrier | Untouched (still OPEN) |
| Optional \(r^3\) rewrite of June 30 §Phi-energy | Deferred to Aug 22 companion |
| Clay / unconditional NS claim | **Not** claimed |

---

## DA routing (do not conflate)

| Object | Label |
| --- | --- |
| Φ-renorm swirl algebra / conditional reduction | **KEEP** (this book) |
| Open condition | \(\sup_\eps\int_0^T\|u^r_\eps/r\|_{L^\infty}\,\mathrm{d}t<\infty\) |
| Clay Statement B / Millennium | **NOT** closed by this paper |
| Lemma★ / \(\mathcal{R}_\star\) PRODUCT-BLOCK | Separate packaging — related program, different object |

See DA inventory **NS-Φ** and conflict **C-GLUE-4**: keep the identity; do not feed it to SFE / Theorem H / Clay glue.
