# Handoff for Cursor / Grok 4.6

**From:** cloud agent on `cursor/sfe-rewrite-domain-architect-9d6b` (run `bc-b45dd8d0-d236-40e3-b477-fcef38fd9d6b`)  
**For:** the other Cursor window (Grok 4.6) that Jon is using on the second screen  
**Date:** 25 August 2026  
**Human:** Jonathan Simons (`simonsmedical@icloud.com`), Prime Field Technologies LLC

Paste this whole file as the first message in that chat. Then work from the repo, not from Chat Vault.

---

## 0. What Jon just said (do this)

He checked a **damaged copy** of the Navier–Stokes challenge (Markdown/LaTeX broken in transit). He does **not** want that copy to overwrite the clean file.

**Authoritative challenge (do not overwrite):**

`docs/domain-architect/DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md`

He listed items he thought were already in that clean file:

- unaugmented equation
- spectral barycenter \(\Lambda = Y/X\)
- centered transfer \(M - \Lambda N\)
- DA-NS-1 closure target
- rejection and validation tests

**Correction for you:** the clean file **does** have the unaugmented plant, rejection tests, and validation tests. It does **not** contain \(\Lambda = Y/X\), \(M-\Lambda N\), or a label `DA-NS-1`. Those strings are **not anywhere in this repo**. Do not invent them into DA-VC-01. If Jon still wants that spectral-barycenter apparatus, file it as a **separate** note and keep DA-VC-01 unchanged until he pastes a clean source.

He said the damaged copy adds **no new proof or mechanism**.

---

## 1. Repo / branch / PR

| | |
|---|---|
| Repo | https://github.com/simons357/Ship_it_app |
| Branch | `cursor/sfe-rewrite-domain-architect-9d6b` |
| HEAD when this handoff was written | Paper2 SND/GNC filed at `docs/papers/ns-snd/` (after `f724588`) |
| Draft PR | https://github.com/simons357/Ship_it_app/pull/31 — **stay draft. Do not merge.** |
| Other PR | `#30` (`cursor/domain-architect-v1-f929`) — **leave alone** unless Jon says otherwise |
| Preferred base | `main` |
| `gh` | read-only. PRs via Cursor `ManagePullRequest`. |

New branches from this agent family must match `cursor/<descriptive-name>-9d6b`. Do not force-push. Do not leave this branch unless Jon asks.

---

## 2. Product truth (non-negotiable)

Live product is **Domain Architect (DA)**:

```
DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE
```

Canonical spec: `docs/DOMAIN-ARCHITECT.md`  
Decisions: `docs/domain-architect/DECISIONS.md`  
Independent critic: `docs/domain-architect/GROK-SPEC-AUDIT.md`  
Stale rival brief: `docs/domain-architect/ARCHITECTURE-AUDIT.md` (do not treat as implemented)

**Correspondence is a hypothesis, not physical equivalence.**

SFE, UHF, DHFA, Harmonic Blueprint are **not** canonical. Archive only: `docs/archive/`.

**Books stay split. One letter is not one object.**

| Book | What | Collision to refuse |
|---|---|---|
| A — DA | role architecture lab | identifier / declared output \(\Phi\). Not gravity by default |
| B — axisymmetric NS with swirl | fluids paper | \(\Phi = u_\theta/r = \Gamma/r^2\) |
| D — Paper2 SND/GNC | periodic 3D NS on \(\mathbb{T}^3\) | shell-helical \(H_N\); SND/GNC. **Not** FRA \(H\), **not** swirl \(\Phi\) |

Do not glue swirl \(\Phi\) to FRA output \(\Phi\) or Newtonian \(\Phi_g\).
Do not glue Paper2 \(H_N\) / SND / GNC into the swirl rewrite or into DA as a Clay stamp.

Jon: `accept grok table` → **P1 = rewrite**. Blocking if rewrite: **A5, A10, A11, A12, A13, A14**. Do not invent QStack/QNav. Do not dump again. Do not folder-shuffle and call it a rewrite.

**The rewrite is still not implemented in Python.** Live app is dump-era three-verb demo (Firestone, OLS, RK4, PD, FFT Poisson, three-pattern classifier). Version string `1.1.0`. Honest bugs still live: `m` as `STATE_TRANSITION`, vacuous `T` ⇒ `TRANSFORMABLE`, generic maps, `"maximize profit"` / NS regularity both synthesize a PD loop, archive tab still a peer.

Logo (confirmed): **Black & gold** and **All silver** 3D lockups both stay. **Lambda Lab** is the vector construction tool. Neither replaces the other. Default Mark view is Black & gold.

---

## 3. Authoritative files (use these)

### Domain Architect

- `docs/DOMAIN-ARCHITECT.md`
- `docs/domain-architect/OPERATIONAL-MATH.md`
- `docs/domain-architect/DECISIONS.md`
- `docs/domain-architect/GROK-SPEC-AUDIT.md`
- `docs/domain-architect/DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md` ← **DA-VC-01, live FAIL**

### Swirl / NS (separate book)

- `docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-08-22.tex` — 22 August theorem paper
- `docs/papers/swirl/SWIRL-CONTINUATION.md` — what stands; classical unaugmented swirl **open**
- `docs/papers/swirl/PHI_GEOMETRY_BRIDGE.md` — May essay (CMB/Saturn/Kabbalah). **Hypothesis, not theorems**
- `docs/papers/swirl/DA-ON-PHI-GEOMETRY.md` — DA reading; SPE refused
- `docs/papers/swirl/README.md`

### Paper2 SND/GNC (separate book — not swirl)

- `docs/papers/ns-snd/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex` — 1 August 2026 repaired conditional draft
- `docs/papers/ns-snd/README.md` — proved vs open; do not glue \(H_N\) to FRA or swirl
- Tests: `tests/test_paper2_ns_snd.py`

### Packet for a *new* ChatGPT chat (not Chat Vault)

- `docs/packets/DA-AND-NS-CHATGPT.md`
- `docs/packets/HANDOFF-GROK-4.6.md` (this document)

### App

- Launch: `python3 -m domain_architect app` or double-click `Open Domain Architect.command`
- Local only: `http://127.0.0.1:8765/` on **that machine**. Not a public site. Cloud-agent localhost is not Jon’s Mac.
- Mark tab: Black & gold / All silver / Lambda Lab
- Decompose has a **Swirl identity** button: `(1/r^4)*dz(Gamma^2) = dz(Phi^2)`

Public May PDF (short, not the 22 August writeup): https://zenodo.org/records/20405405/files/PhiRenorm_TrackB.pdf

---

## 4. What DA-VC-01 actually contains

ID: `DA-VC-01`. Two scoreboards that must not merge:

| Scoreboard | Question | Status |
|---|---|---|
| DA-VC-01 | Did DA handle the plant honestly? | **FAIL** (25 Aug 2026 live lab) |
| NS-open | Classical unaugmented swirl globally regular? | **OPEN** |

Unaugmented = no \(\varepsilon\)-hyperviscosity, no Q1, no \((A,W)\).

Plant (Book B):

\[
\frac{1}{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)
\tag{I}
\]

\[
\partial_t\Phi + u^r\partial_r\Phi + u^z\partial_z\Phi + 2\frac{u^r}{r}\Phi = \nu\mathcal{L}_4\Phi
\tag{F}
\]

\(\varepsilon=0\) energy pairing: strain term \(\int (u^r/r)\Phi^2 r^3\). \(\Gamma\in L^\infty\) does **not** control \(u^r\).

Live lab:

- Decompose identity → `unclassified`, Level 0, Φ not auto-gravity (**partial pass**)
- Translate identity vs CMB language → `analogy`, `no_checked_structure_map` (**refuse OK**)
- Synthesize “global smoothness of unaugmented axisymmetric NS with swirl” → **PD loop** + `validation_gate: MATHEMATICAL` (**hard fail A13**)

A passing DA run still leaves NS-open red. Closing NS-open from a DA stamp is an automatic fail of DA-VC-01.

Tests that lock this: `tests/test_challenge_01_ns.py` (includes a characterization of the vacuous PD synthesize; **flip that test when A13 lands**).

---

## 5. What you must not do

- Do not overwrite `DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md` with a broken paste, ChatGPT export, or “repaired” barycenter rewrite.
- Do not add \(\Lambda=Y/X\), \(M-\Lambda N\), or `DA-NS-1` to that file unless Jon provides a **clean** source and says to merge.
- Do not claim unaugmented swirl is solved. Do not claim \(\varepsilon\)-smoothness is the unaugmented theorem.
- Do not glue swirl \(\Phi\) to gravity, FRA, CMB, Saturn, Kabbalah, Riemann zeros, or a cosmic lattice.
- Do not glue Paper2 SND / GNC / \(H_N\) into swirl or into a Clay claim. Simplex lemma is **OPEN**. “T2 Closed Gronwall” is withdrawn.
- Do not treat `PHI_GEOMETRY_BRIDGE.md` as Book B theorems. Q6 / primes / spectral clock: packaging; strip from any submit (`SWIRL-CONTINUATION.md`).
- Do not implement another dump. Do not create QStack/QNav.
- Do not merge PR #31. Do not touch PR #30.
- Do not kill processes with `pkill -f`. PID only if you must stop something. Leave the desktop app running if it is up.
- Do not use `gh` to open/merge PRs.

---

## 6. Next engineering work (if Jon asks you to code)

Accepted table, still not in Python. Order that matches DA-VC-01:

1. **A13** — inverse design fail-closed. S1 must not emit a PD loop or stamp MATHEMATICAL for NS regularity. Then invert `test_baseline_s1_still_emits_vacuous_pd_loop`.
2. **A5** — `TRANSFORMABLE` only with morphism + witness. T1 may carry \(\Gamma\mapsto r^2\Phi\) on \(\{r>0\}\) with \(\partial_z(r^4)=0\). That \(T\) is **inside one PDE**, not a cross-domain map.
3. **A11 / A14** — Φ not gravity; no generic role-name maps. T2 stays analogy/incompatible.
4. **A10, A12, A4** — `m` inertial; empty default units; real `run_cycle`.
5. Then A1–A3, A6–A9 as marked.

Demo success is not DA success. Named cycles must call a real cycle, not fake one.

---

## 7. How Jon opens the app on his Mac

```bash
git clone https://github.com/simons357/Ship_it_app.git   # if needed
cd Ship_it_app
git checkout cursor/sfe-rewrite-domain-architect-9d6b
python3 -m domain_architect app
```

or double-click `Open Domain Architect.command` in the repo folder.

Browser: **http://127.0.0.1:8765/** on his computer.

If numpy/pandas missing: `python3 -m pip install -r requirements.txt`

---

## 8. Tests to run

```bash
python3 -m unittest tests.test_sfe_hb_dump tests.test_domain_architect_v1 tests.test_domain_architect_acceptance tests.test_domain_architect_units tests.test_historical_archive tests.test_brand_mark tests.test_desktop_app tests.test_phi_geometry_bridge tests.test_challenge_01_ns tests.test_paper2_ns_snd
```

---

## 9. Jon’s recent intent (this thread)

1. Wanted the swirl paper and to try it in DA.
2. Wanted a way to **open** the app on his Mac (local launcher; cloud localhost is useless to him).
3. Pasted *The Phi-Renormalization as Universal Geometry* (May 2026). Filed as essay. DA reading: not physical equivalence.
4. Asked to separate DA + NS from **Chat Vault** into one ChatGPT packet.
5. Named `DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md`. Created. Live FAIL.
6. Checked a damaged copy; **do not overwrite** the clean file. Asked for this handoff.

Notion Chat Vault was not readable from the cloud agent (MCP needsAuth). Packets were compiled from the repo, which is the cleaner source.

---

## 10. One paragraph you can tell Jon

Domain Architect is the product. Axisymmetric swirl is a separate book. The 22 August paper keeps the algebraic identity and leaves classical unaugmented regularity open. Paper2 SND/GNC is a third book: conditional spectral NS on \(\mathbb{T}^3\), simplex OPEN, not a swirl estimate. DA-VC-01 is the honest lab test of the swirl plant; it fails today because synthesize still invents a PD loop. The May geometry essay is a correspondence hypothesis, not a theorem. The clean challenge file is the authority; a broken paste with \(\Lambda=Y/X\) / \(M-\Lambda N\) / DA-NS-1 must not replace it.

End of handoff.
