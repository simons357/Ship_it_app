# Packet: canonical helical channel γ=(Δ,σ)

28 September 2026.
Sprint 01 source of truth filed. Coefficient identities
certified on k+p+q=0. v2 not run. NS not solved.
DA-NS-2 remains open.

Working page: [`docs/CANONICAL-CHANNEL-GAMMA.md`](../docs/CANONICAL-CHANNEL-GAMMA.md)

Sprint 01: [`docs/DA-NS-SPRINT-01-PHASE-LOCK-AND-FULL-HELICAL-FLOW-2026-09-07.md`](../docs/DA-NS-SPRINT-01-PHASE-LOCK-AND-FULL-HELICAL-FLOW-2026-09-07.md)

## Frozen rule

\[
\gamma=(\Delta,\sigma),\qquad
k+p+q=0,\qquad
\sigma=(s_k,s_p,s_q)\text{ heterochiral}.
\]

Six signed channels per geometric triangle. Not three
cyclic output rewrites. One coefficient per signed channel.

\[
\Theta_{\Delta,\sigma}
=
\operatorname{Re}\bigl(g_{\Delta,\sigma}\,
\overline{a_k^{s_k}a_p^{s_p}a_q^{s_q}}\bigr).
\]

Conjugation is essential.

## Coefficient map

On consistent frames \(h_s(-k)=\overline{h_s(k)}\):

\[
G_0=(h_p^{s_p}\times h_q^{s_q})\cdot h_k^{s_k},
\qquad
g_{\mathrm{ordered}}=-i s_p\lvert\mu\rvert G_0.
\]

\(|g_{\mathrm{energy}}|=|G_0|\). The unimodular ratio
\(U=g_{\mathrm{energy}}/G_0\) is a frame/triangle
convention, not identically \(+1\):

| Δ | \(U\) on default axis |
|---|---|
| T1 | \(+1\) |
| T2 | \(-1\) |
| T3 | \(\pm i\) |
| T4, seed | \(\arg\in\{\pm\pi/6,\pm 5\pi/6\}\) |

Do not treat \(U=1\) as universal. \(b_\gamma\) must use
the energy-fit \(g\) or apply \(U\) to \(G_0\).

\(g_W=\tfrac12(s_p\lvert p\rvert-s_q\lvert q\rvert)G_{\mathrm{cross}}\)
is the k-leg fold and vanishes on live odd-\(k\) isosceles
channels.

## Charge identities (heterochiral)

\[
Q_{\mathrm{abs}}=\sum_{m\in\Delta,\,\pm}\lvert m\rvert\,\tau_m
=2Q_3,\qquad
Q_3=2o\,\tau_o,
\qquad
\mathfrak T_c^{\mathrm{het}}=R_\Lambda Q_{\mathrm{abs}}.
\]

\(Q_3\) is the three-mode reduction. Do not rename it \(Q_{\mathrm{abs}}\).

## Payload

`results/canonical_24_channel_payload.json`
— parallelogram rewritten as \(k+p+q=0\),
\(4\,\Delta\times 6\,\sigma=24\) channels, generated
from scratch. Old \(24\times 12\) numerics not reused.

`results/full_flow_identity.json`
— seed plus parallelogram, 30 heterochiral certifications.

## Not done

v2. Primitive test. DA-NS-2. Any regularity claim.
