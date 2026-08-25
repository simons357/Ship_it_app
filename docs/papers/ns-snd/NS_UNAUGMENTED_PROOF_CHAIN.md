# Classical (unaugmented) NS — proof chain

Mac source was not readable on this VM:
`/Users/jonathansimons/Desktop/RH_Proof_Chain_Synthesis/00_status/NS_UNAUGMENTED_PROOF_CHAIN.md`
(47 lines). Filed from the chat paste. Operator-norm bars (`\|…\|`) that chat
dropped are restored in the steps; the words are his.

Archon QStack axis-drain Steps 1–6 are regularized (ε>0), not this chain.

This page is only the Statement-B / classical Leray–Hopf program (no Q1, no Φ-renorm, no ε-absorbing ball).

Governing equations (Clay Statement B, torus form):

\[
\partial_t u + (u\cdot\nabla)u = -\nabla p + \nu\Delta u,\qquad \nabla\cdot u=0
\quad\text{on }\mathbb{T}^3,\quad u_0\in H^1.
\]

Objects: Leray–Hopf weak solution \(u(t)\); dyadic shells \(E_j\); normalized simplex \(a(t)\in\Delta_{N-1}\); shell operator \(H_N[a]=\sum_j a_j B_j\); frozen reference \(\widehat H_N^\mu=H_N[\mu]\), \(\mu_j=1/N\).

| # | Step | Status |
|---|---|---|
| 1 | Leray–Hopf energy inequality: \(a(t)\) exists on the simplex (boundedness, not smallness) | STANDARD / INHERITED |
| 2 | Ring Lemma (NS-6): static three-shell lower bound for \(Q_N\) / \(H_N\) geometry | PROVED (standalone; not Clay alone) |
| 3 | Finite-\(N\) operator continuity: \(\|H_N[a]-H_N[b]\|_{\mathrm{op}}\le C_N\|a-b\|_{\ell^1}\) | PROVED |
| 4 | Frozen gap (Route J): \(\lambda_{\min}(\widehat H_N^\mu)>-1/2+\delta_0\) for tested \(N\le 800\) | NUMERICAL / UNDER AUDIT (no analytic all-\(N\) claim) |
| 5 | Weyl master implication (Paper2 Thm): quantitative SND + frozen gap \(\Rightarrow\) dynamic spectral gap \(\inf_t\lambda_{\min}(H_N[u(t)])>-1/2\) | PROVED (conditional on SND + FG) |
| 6 | Global summation / conditional \(H^1\) bound (NS-7, NS-8): if [SND] holds for all \(t\), then dangerous-regime time is finite and global \(H^1\) follows | PROVED (conditional on [SND]) |
| 7 | SND simplex stability: \(\|a(t)-\mu\|_{\ell^1}\le\eta_N\) uniform in \(t\) for classical Leray–Hopf (Left arrow / Lem.~6.1) | OPEN |
| 8 | Dynamic [SND] preservation (NS-10): unaugmented classical flow keeps \(\|H_N[u(t)]-\widehat H_N^\mu\|_{\mathrm{op}}<\delta_0\) for all \(t\ge0\) | OPEN |
| 9 | Continuation: spectral gap / non-concentration \(\Rightarrow\) smooth Leray–Hopf continuation (must be supplied explicitly) | OPEN / INCOMPLETE in repaired Paper2 |

Gap — Dynamic SND / uniform simplex stability for classical (no Q1) Leray–Hopf; \(\varepsilon\to0\) does not close this | OPEN

Gap — Analytic all-\(N\) frozen gap (Route J beyond finite numerics) | OPEN / UNDER AUDIT

Conclusion — classical global regularity (NS-11 / Clay Statement B) | **NOT CLAIMED**

Hard rules: classical Clay NOT CLAIMED. Dynamic SND OPEN. Leray boundedness ≠ SND smallness. Augmented / ε-regularized proofs do not transfer.

Controlling face (Desktop pack name): `06_navier_stokes_shelf/03_conditional_unaugmented_SND/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`

Status cross-check: July 23 ledger NS-6…NS-11; `NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md`; `CLOSURE_DRIFT_LEDGER.md` (**still missing** on this VM; Drive `TRIPLE_LOCK_VERIFIED_DETAILS_2026-08-02.md` is same ledger family, **different document** — partial only). Frankie `ns_routej_bridge_recovery/CURRENT_CLAIM_LEDGER.md` is the file for Route J (“does it have J?”) and is **still missing**; Drive `74ecca4e5` millennium progress report **cannot answer Route J**. Packet: [`docs/packets/MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md`](../../packets/MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md).

## Domain Architect note

- **Controlling face:** August repaired TeX [`Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`](Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex). Same file he named under `06_navier_stokes_shelf/03_conditional_unaugmented_SND/`.
- **Cross-check:** the August 1 audit is already in this repo: [`NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md`](NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md).
- This chain is **not** the June FIXED PDF compile.
- Step 2 Ring Lemma (NS-6) is **not** Ring-book fluids \(\inf J/X \ge c_*\) unless the source says so; do not identify them.
- Letters: Paper2 \(H_N[a]\) is not Q6 \(H_N\).
- Localized reparation default cut is leftover **7–8**, not step 2. Step 2 is already PROVED. NS-11 / Clay Statement B is not claimed.
