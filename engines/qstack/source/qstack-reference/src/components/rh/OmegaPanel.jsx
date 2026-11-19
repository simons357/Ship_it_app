import React from "react";
import { ML, MB } from "../qstack/MathBlock";

const OPERATORS = [
  {
    id: "Omega1",
    name: "Ω1",
    role: "Zero-Density Shell Projector",
    desc: "Projects onto horizontal bands Im(ρ) ∈ [T_j, T_{j+1}] in the critical strip. Analog of dyadic shell projectors P_j in QStack.",
    formula: "\\Pi_j^\\zeta f = \\int_{T_j}^{T_{j+1}} \\langle f, \\phi_t\\rangle \\phi_t\\,dt",
    color: "cyan",
    status: "DEFINED",
  },
  {
    id: "Omega3",
    name: "Ω3",
    role: "L-function Coefficient Cage",
    desc: "Certifies that Dirichlet coefficients stay within interval I_j = [α_j^ref − ρ_j, α_j^ref + ρ_j]. Non-circular: uses only Mellin-class data.",
    formula: "\\alpha_j[\\zeta] \\in I_j := [\\alpha_j^{\\mathrm{ref}}-\\rho_j,\\;\\alpha_j^{\\mathrm{ref}}+\\rho_j]",
    color: "amber",
    status: "OPEN DEBT",
  },
  {
    id: "Omega6",
    name: "Ω6",
    role: "Adaptive Zero-Repulsion Stabilizer",
    desc: "The RH analog of Q6. Selectively damps zero-density concentration off the critical line. Activation: when α_j > α_c. Enforces SZD (Spectral Zero-Dispersal).",
    formula: "\\Omega_6(\\zeta) = -\\sum_j \\lambda_j^\\zeta\\,\\Delta_j^\\zeta",
    color: "violet",
    status: "PROTOTYPE",
    isPrimary: true,
  },
  {
    id: "OmegaN",
    name: "Ω-N",
    role: "Hardy Space Gap Enforcer",
    desc: "Enforces the RH spectral gap: no eigenvalue of H_N^ζ may exceed δ₀ = 0.20 off-axis. The Hilbert–Pólya operator proxy.",
    formula: "\\inf_{t\\ge0}\\lambda_{\\min}(H_N^\\zeta(t)) > -\\tfrac{1}{2}",
    color: "emerald",
    status: "GOAL",
  },
];

const COLOR = {
  cyan:    { border: "border-cyan-700/50",    bg: "bg-cyan-950/20",    tag: "text-cyan-400",    badge: "bg-cyan-900/30 text-cyan-400 border-cyan-700" },
  amber:   { border: "border-amber-700/50",   bg: "bg-amber-950/20",   tag: "text-amber-400",   badge: "bg-amber-900/30 text-amber-400 border-amber-700" },
  violet:  { border: "border-violet-700/50",  bg: "bg-violet-950/20",  tag: "text-violet-400",  badge: "bg-violet-900/30 text-violet-400 border-violet-700" },
  emerald: { border: "border-emerald-700/50", bg: "bg-emerald-950/20", tag: "text-emerald-400", badge: "bg-emerald-900/30 text-emerald-400 border-emerald-700" },
};

export default function OmegaPanel() {
  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="mb-4">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-2 h-2 rounded-full bg-violet-400 animate-pulse" />
          <span className="text-xs text-violet-400 tracking-widest uppercase font-mono">ΩStack Language</span>
        </div>
        <h2 className="text-lg font-bold text-white">ΩStack Operator Architecture</h2>
        <p className="text-xs text-gray-400 mt-1">
          RH analog of QStack. Shift proof target: away from "find a zero off Re(s)=½" → toward certifying a persistent spectral gap via zero-density coefficient cages.
        </p>
      </div>

      {/* Strategy banner */}
      <div className="rounded-xl border border-violet-700/40 bg-violet-950/10 p-5">
        <div className="text-xs text-violet-500 uppercase tracking-widest mb-3">Core Strategy Shift</div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
          {[
            { label: "WRONG target", val: "Search for zero ρ with Re(ρ)≠½", color: "text-rose-400" },
            { label: "SHIFT to", val: "Certify: ‖R_N^ζ(t)‖_op < δ₀ = 0.20", color: "text-violet-400" },
            { label: "DATA CLASS", val: "Mellin-L² only (non-circular)", color: "text-emerald-400" },
          ].map((s) => (
            <div key={s.label} className="bg-[#12151e] border border-gray-800 rounded p-3">
              <div className="text-gray-500 mb-1">{s.label}</div>
              <div className={`${s.color} font-semibold`}>{s.val}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Operator cards */}
      <div className="grid grid-cols-1 gap-4">
        {OPERATORS.map((op) => {
          const c = COLOR[op.color];
          return (
            <div key={op.id} className={`rounded-lg border p-5 ${c.border} ${op.isPrimary ? c.bg : "bg-[#12151e]"}`}>
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className={`text-2xl font-black font-mono ${c.tag}`}>{op.name}</span>
                  <div>
                    <div className="text-sm text-gray-200 font-semibold">{op.role}</div>
                    <div className="text-xs text-gray-500 mt-0.5">{op.desc}</div>
                  </div>
                </div>
                <span className={`text-[10px] px-2 py-0.5 rounded-full border font-mono whitespace-nowrap ml-3 ${c.badge}`}>
                  {op.status}
                </span>
              </div>
              <div className="mt-3 overflow-x-auto">
                <MB>{op.formula}</MB>
              </div>
            </div>
          );
        })}
      </div>

      {/* SZD box */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">SZD — Spectral Zero-Dispersal Condition</div>
        <p className="text-xs text-gray-400 mb-4">
          The RH analog of SND (Spectral Non-Dispersal). If true, zero density stays spread along Re(s)=½ and never concentrates off-axis.
        </p>
        <MB>{"\\sup_{T\\ge0}\\,\\|\\alpha(T)-\\mu^\\zeta\\|_{\\ell^1} \\le \\eta_N^\\zeta"}</MB>
        <div className="mt-3 text-xs text-gray-600">
          Proof hierarchy: SZD → ℓ¹-tube → C_N^ζ · η_N^ζ &lt; 0.20 → RH spectral gap persists.
        </div>
      </div>

      {/* Open debts */}
      <div className="rounded-lg border border-rose-800/40 bg-rose-950/10 p-5">
        <div className="text-xs text-rose-500 uppercase tracking-widest mb-3">Open Debts (vs QStack)</div>
        <div className="space-y-2 text-xs">
          {[
            "The Hilbert–Pólya operator H^ζ is still hypothetical — must be constructed explicitly or proxied via Lax–Phillips / Connes adelic.",
            "No PDE dynamics for ζ — the 'flow' of zeros must be defined via GUE random matrix or explicit zero-counting N(T).",
            "SZD has no PDE-energy proof route — must use zero-repulsion theorems (Bohr–Landau, de la Vallée Poussin) as substitutes.",
            "Coefficient cage Ω3 must be closed from Mellin-class data only — no assuming analytic continuation beyond what's proven.",
          ].map((d, i) => (
            <div key={i} className="flex gap-3">
              <span className="text-rose-600 font-bold mt-0.5">✗</span>
              <span className="text-gray-400">{d}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}