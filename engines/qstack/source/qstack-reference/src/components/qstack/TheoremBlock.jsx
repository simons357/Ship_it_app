import React, { useState } from "react";
import { ML, MB } from "./MathBlock";

const THEOREMS = [
  {
    id: "L1",
    tag: "Lemma 1",
    title: "Universal Operator Bound",
    color: "violet",
    statement: "For arbitrary bounded projection pieces:",
    formula: "\\left\\|\\sum_{j\\in J_N}\\Delta\\gamma_j\\Pi_j\\right\\|_{\\mathrm{op}} \\le \\sum_{j\\in J_N}|\\Delta\\gamma_j|\\,\\|\\Pi_j\\|_{\\mathrm{op}}",
    consequence: "H3 follows if \\sup_{t\\ge0}\\sum_{j}|\\gamma_j[u(t)]-\\gamma_j^{\\mathrm{ref}}|\\,\\|\\Pi_j\\|_{\\mathrm{op}} < 0.20",
    note: "Crude but unconditional. Uses only triangle inequality.",
  },
  {
    id: "L2",
    tag: "Lemma 2",
    title: "Positive Projection Cage Bound",
    color: "amber",
    statement: "If each Π_j is self-adjoint positive and |Δγ_j(t)| ≤ ρ_j, then:",
    formula: "\\|R_N(t)\\|_{\\mathrm{op}} \\le \\left\\|\\sum_j \\rho_j\\Pi_j\\right\\|_{\\mathrm{op}}",
    consequence: "H3 follows if \\left\\|\\sum_j \\rho_j\\Pi_j\\right\\|_{\\mathrm{op}} < 0.20",
    note: "Right bound when coefficient signs vary but operator pieces are positive.",
  },
  {
    id: "L3",
    tag: "Lemma 3",
    title: "Orthogonal Projection Bound",
    color: "cyan",
    statement: "If the Π_j are mutually orthogonal spectral projections:",
    formula: "\\left\\|\\sum_{j\\in J_N}\\Delta\\gamma_j\\Pi_j\\right\\|_{\\mathrm{op}} = \\max_{j\\in J_N}|\\Delta\\gamma_j|",
    consequence: "H3 follows from \\sup_{t\\ge0}\\max_{j\\in J_N}|\\gamma_j[u(t)]-\\gamma_j^{\\mathrm{ref}}| < 0.20",
    note: "Best possible form. The entire H3 task becomes a uniform coefficient-envelope estimate.",
  },
  {
    id: "L4",
    tag: "Lemma 4",
    title: "Energy-Class Coefficient Cage",
    color: "emerald",
    statement: "Let u(t) be any Leray-Hopf solution. Suppose the coefficient cage:",
    formula: "\\gamma_j[u(t)]\\in I_j := [\\gamma_j^{\\mathrm{ref}}-\\rho_j,\\,\\gamma_j^{\\mathrm{ref}}+\\rho_j]",
    consequence: "\\left\\|\\sum_{j}\\rho_j\\Pi_j\\right\\|_{\\mathrm{op}}<0.20 \\implies \\sup_{t\\ge0}\\|R_N(t)\\|_{\\mathrm{op}}<0.20",
    note: "Consequently: inf_{t≥0} λ_min(H_N(t)) > −1/2.",
  },
  {
    id: "L5",
    tag: "Lemma 5",
    title: "Simplex Lipschitz Reduction",
    color: "rose",
    statement: "Assume H_N[u(t)] = H_N[a(t)]. Define the Lipschitz constant:",
    formula: "C_N := \\sup_{a\\ne b\\in\\Delta_N} \\frac{\\|H_N[a]-H_N[b]\\|_{\\mathrm{op}}}{\\|a-b\\|_{\\ell^1}}",
    consequence: "\\|H_N[a(t)]-H_N[\\mu]\\|_{\\mathrm{op}} \\le C_N\\|a(t)-\\mu\\|_{\\ell^1}",
    note: "H3 follows from: sup_{t≥0} ‖a(t)−μ‖_ℓ¹ < 0.20 / C_N",
  },
  {
    id: "T1",
    tag: "Theorem",
    title: "SND Simplex Stability",
    color: "cyan",
    statement: "Let u(t) be a Leray-Hopf solution. Let a_j(t) = ‖P_j u(t)‖²_L² / ∑_k ‖P_k u(t)‖²_L². Suppose SND_N(η_N, μ). Then:",
    formula: "\\sup_{t\\ge0}\\|a(t)-\\mu\\|_{\\ell^1} \\le \\eta_N",
    consequence: "C_N\\eta_N < 0.20 \\implies \\text{H3 holds and dynamic spectral gap persists}",
    note: "This is the exact next target. If SND is defined via physical shell flux / cascade geometry, the real task is proving the physical SND implies the ℓ¹-tube condition.",
    isTheorem: true,
  },
];

const COLOR_MAP = {
  violet: { border: "border-violet-700/60", tag: "text-violet-400", bg: "bg-violet-950/10" },
  amber: { border: "border-amber-700/60", tag: "text-amber-400", bg: "bg-amber-950/10" },
  cyan: { border: "border-cyan-700/60", tag: "text-cyan-400", bg: "bg-cyan-950/10" },
  emerald: { border: "border-emerald-700/60", tag: "text-emerald-400", bg: "bg-emerald-950/10" },
  rose: { border: "border-rose-700/60", tag: "text-rose-400", bg: "bg-rose-950/10" },
};

export default function TheoremBlock() {
  const [expanded, setExpanded] = useState("T1");

  return (
    <div className="space-y-4 max-w-3xl mx-auto">
      <div className="mb-6">
        <h2 className="text-lg font-bold text-white">Lemmas & Theorems</h2>
        <p className="text-xs text-gray-400 mt-1">
          Click any item to expand the full statement and consequence.
        </p>
      </div>

      {THEOREMS.map((thm) => {
        const c = COLOR_MAP[thm.color];
        const open = expanded === thm.id;
        return (
          <div
            key={thm.id}
            className={`rounded-lg border transition-all ${c.border} ${open ? c.bg : "bg-[#12151e]"}`}
          >
            <button
              className="w-full px-5 py-4 flex items-center justify-between text-left"
              onClick={() => setExpanded(open ? null : thm.id)}
            >
              <div className="flex items-center gap-3">
                <span className={`text-xs font-bold uppercase tracking-widest ${c.tag}`}>
                  {thm.tag}
                </span>
                <span className="text-sm text-gray-200">{thm.title}</span>
                {thm.isTheorem && (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-900/40 text-cyan-400 border border-cyan-800 tracking-widest uppercase">
                    Open Target
                  </span>
                )}
              </div>
              <span className="text-gray-600 text-xs">{open ? "▲" : "▼"}</span>
            </button>

            {open && (
              <div className="px-5 pb-5 space-y-3">
                <div className="text-xs text-gray-400">{thm.statement}</div>
                <MB>{thm.formula}</MB>
                {thm.consequence && (
                  <>
                    <div className="text-xs text-gray-500 uppercase tracking-widest">Consequence</div>
                    <MB>{thm.consequence}</MB>
                  </>
                )}
                {thm.note && (
                  <div className={`text-xs rounded border p-3 ${c.border} ${c.bg} ${c.tag}`}>
                    {thm.note}
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}

      {/* Work plan */}
      <div className="mt-8 rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">Immediate Work Plan</div>
        <div className="space-y-3">
          {[
            { n: "1", title: "Classify the projections", desc: "Determine if Π_j are mutually orthogonal, commuting, or general bounded operators. Decides whether threshold is max, ℓ², or ℓ¹ norm." },
            { n: "2", title: "Write the exact coefficient formula", desc: "For each γ_j[u]: is it an amplitude, normalized ratio, shell flux, helical imbalance, angle, or time-averaged observable?" },
            { n: "3", title: "Derive coefficient intervals", desc: "For every j ≤ N, prove γ_j[u] ∈ I_j using only energy-class quantities or finite-shell identities." },
            { n: "4", title: "Certify the polytope radius", desc: "Compute or prove sup_{γ∈∏I_j} ‖∑(γ_j − γ_j^ref)Π_j‖_op < 0.20." },
          ].map((s) => (
            <div key={s.n} className="flex gap-4 text-xs">
              <div className="w-6 h-6 rounded-full border border-gray-600 flex items-center justify-center text-gray-500 flex-shrink-0 mt-0.5">
                {s.n}
              </div>
              <div>
                <div className="text-gray-200 font-semibold mb-1">{s.title}</div>
                <div className="text-gray-500">{s.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}