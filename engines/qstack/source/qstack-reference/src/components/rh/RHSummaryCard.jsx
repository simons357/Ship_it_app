import React, { useState } from "react";
import { ML, MB } from "../qstack/MathBlock";

const DEBTS = [
  { id: "D1", label: "H_N^ζ Construction", desc: "Berry–Keating / Connes / Lax–Phillips", value: 0.0, color: "rose", open: true },
  { id: "D2", label: "SZD Proof", desc: "‖α(T)−μ^ζ‖_ℓ¹ ≤ η_N^ζ via repulsion", value: 0.0, color: "amber", open: true },
  { id: "D3", label: "C_N^ζ Computation", desc: "Lipschitz constant of H_N^ζ on Δ_N", value: 0.0, color: "amber", open: true },
  { id: "D4", label: "Zero-Free Region", desc: "de la Vallée Poussin (known, partial)", value: 0.72, color: "cyan", open: false },
  { id: "D5", label: "GUE Numerics", desc: "10²² zeros verified on critical line", value: 0.91, color: "emerald", open: false },
];

const QS_RH = [
  { qs: "Leray-Hopf u(t) ∈ L²∩L²Ḣ¹", rh: "Mellin-L² class ζ(s), s ∈ strip" },
  { qs: "Dyadic shell P_j", rh: "Horizontal band Π_j^ζ, Im∈[T_j,T_{j+1}]" },
  { qs: "Shell amplitude a_j[u]", rh: "Zero density α_j(T)" },
  { qs: "Probability simplex Δ_N", rh: "Zero-density simplex Δ_N^ζ" },
  { qs: "SND condition", rh: "SZD condition" },
  { qs: "Q6 adaptive damping", rh: "Ω6 zero repulsion" },
  { qs: "Coefficient cage ρ_j", rh: "Zero-density cage ρ_j^ζ" },
  { qs: "‖R_N(t)‖_op < 0.20", rh: "‖R_N^ζ(T)‖_op < 0.20" },
  { qs: "H3 goal", rh: "Riemann Hypothesis" },
];

const STATUS_COLOR = {
  rose:    { bar: "bg-rose-600",    text: "text-rose-400",    border: "border-rose-700/40",    bg: "bg-rose-950/10" },
  amber:   { bar: "bg-amber-500",   text: "text-amber-400",   border: "border-amber-700/40",   bg: "bg-amber-950/10" },
  cyan:    { bar: "bg-cyan-500",    text: "text-cyan-400",    border: "border-cyan-700/40",    bg: "bg-cyan-950/10" },
  emerald: { bar: "bg-emerald-500", text: "text-emerald-400", border: "border-emerald-700/40", bg: "bg-emerald-950/10" },
};

export default function RHSummaryCard() {
  const [debts, setDebts] = useState(DEBTS);

  const closedDebts = debts.filter((d) => !d.open).length;
  const totalDebts = debts.length;
  const readiness = Math.round((closedDebts / totalDebts) * 100);

  const rhCertified = debts.every((d) => !d.open);

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="mb-4">
        <div className="flex items-center gap-3 mb-2">
          <div className={`w-2 h-2 rounded-full ${rhCertified ? "bg-violet-400 animate-pulse" : "bg-gray-600"}`} />
          <span className={`text-xs tracking-widest uppercase font-mono ${rhCertified ? "text-violet-400" : "text-gray-500"}`}>
            {rhCertified ? "RH — CERTIFIED" : "RH — IN PROGRESS"}
          </span>
        </div>
        <h2 className="text-lg font-bold text-white">ΩStack RH Summary Card</h2>
        <p className="text-xs text-gray-400 mt-1">Live proof readiness tracker. Closes when all open debts are resolved.</p>
      </div>

      {/* Master status */}
      <div className={`rounded-xl border p-5 ${rhCertified ? "border-violet-700/60 bg-violet-950/20" : "border-gray-700 bg-[#12151e]"}`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className={`text-2xl font-bold font-mono ${rhCertified ? "text-violet-300" : "text-gray-400"}`}>
              {rhCertified ? "Re(ρ) = ½ · · · CERTIFIED ✓" : "Re(ρ) = ½ · · · NOT YET CERTIFIED"}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              Proof readiness: <span className={readiness > 60 ? "text-emerald-400" : "text-amber-400"}>{readiness}%</span>
              &nbsp;·&nbsp; {closedDebts}/{totalDebts} debts closed
            </div>
          </div>
          <div className="text-right">
            <MB>{"C_N^\\zeta\\eta_N^\\zeta < 0.20"}</MB>
          </div>
        </div>
        {/* Readiness bar */}
        <div className="mt-4 h-2 bg-gray-800 rounded-full">
          <div
            className="h-full rounded-full bg-violet-500 transition-all duration-700"
            style={{ width: `${readiness}%` }}
          />
        </div>
      </div>

      {/* Open debts */}
      <div className="space-y-3">
        <div className="text-xs text-gray-500 uppercase tracking-widest">Proof Debts</div>
        {debts.map((d) => {
          const c = STATUS_COLOR[d.color];
          const pct = Math.round(d.value * 100);
          return (
            <div key={d.id} className={`rounded-lg border p-4 ${c.border} ${d.open ? "" : c.bg}`}>
              <div className="flex items-center justify-between mb-2">
                <div>
                  <span className={`text-xs font-bold font-mono ${c.text}`}>{d.id}</span>
                  <span className="text-sm text-gray-200 ml-3">{d.label}</span>
                </div>
                <span className={`text-[10px] px-2 py-0.5 rounded-full border font-mono ${d.open ? "bg-rose-900/30 text-rose-400 border-rose-700" : "bg-emerald-900/30 text-emerald-400 border-emerald-700"}`}>
                  {d.open ? "OPEN" : "✓ DONE"}
                </span>
              </div>
              <div className="text-xs text-gray-500 mb-2">{d.desc}</div>
              <div className="h-1.5 bg-gray-800 rounded-full">
                <div className={`h-full rounded-full ${c.bar} transition-all duration-500`} style={{ width: `${pct}%` }} />
              </div>
              <div className="flex justify-between text-[10px] text-gray-600 mt-1 font-mono">
                <span>0%</span>
                <span className={c.text}>{pct}%</span>
                <span>100%</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* QStack ↔ ΩStack analogy table */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] overflow-hidden">
        <div className="text-xs text-gray-500 uppercase tracking-widest p-4 border-b border-gray-800">QStack ↔ ΩStack Analogy</div>
        <div className="divide-y divide-gray-800/60">
          {QS_RH.map((row, i) => (
            <div key={i} className="grid grid-cols-2 text-xs">
              <div className="px-4 py-2.5 text-cyan-400/80 font-mono border-r border-gray-800">{row.qs}</div>
              <div className="px-4 py-2.5 text-violet-400/80 font-mono">{row.rh}</div>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-2 text-[10px] font-bold uppercase tracking-widest border-t border-gray-700">
          <div className="px-4 py-2 text-cyan-600 border-r border-gray-700">QStack (NS)</div>
          <div className="px-4 py-2 text-violet-600">ΩStack (RH)</div>
        </div>
      </div>

      {/* Proof hierarchy */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Full Proof Chain</div>
        <MB>{"\\mathrm{SZD} \\Rightarrow \\|\\alpha-\\mu^\\zeta\\|_{\\ell^1}\\le\\eta_N^\\zeta \\Rightarrow C_N^\\zeta\\eta_N^\\zeta < 0.20 \\Rightarrow \\lambda_{\\min}(H_N^\\zeta)>-\\tfrac12 \\Rightarrow \\mathrm{RH}"}</MB>
      </div>
    </div>
  );
}