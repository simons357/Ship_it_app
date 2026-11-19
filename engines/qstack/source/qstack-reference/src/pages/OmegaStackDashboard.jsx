import React, { useState } from "react";
import { Link } from "react-router-dom";
import OmegaPanel from "../components/rh/OmegaPanel";
import ZeroShellViz from "../components/rh/ZeroShellViz";
import RHRouteMap from "../components/rh/RHRouteMap";
import RHTheoremBlock from "../components/rh/RHTheoremBlock";
import RHSummaryCard from "../components/rh/RHSummaryCard";
import ShellTopologyMap from "../components/shared/ShellTopologyMap";
import H3ZeroCorrelation from "../components/shared/H3ZeroCorrelation";
import FormulaReference from "../components/shared/FormulaReference";
import SpectralShellHierarchy from "../components/rh/SpectralShellHierarchy";

const TABS = [
  { id: "operators",  label: "Ω Operators" },
  { id: "zeros",      label: "Zero Shells" },
  { id: "hierarchy",  label: "Shell Hierarchy" },
  { id: "route",      label: "RH Route" },
  { id: "theorems",   label: "Ω Theorems" },
  { id: "summary",    label: "RH Card" },
  { id: "shells",     label: "Shell Map" },
  { id: "h3rh",      label: "H3↔RH" },
];

export default function OmegaStackDashboard() {
  const [activeTab, setActiveTab] = useState("operators");

  return (
    <div className="min-h-screen bg-[#0d0f14] text-gray-100 font-mono">
      <FormulaReference />
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#10131a] px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-violet-400 animate-pulse" />
              <span className="text-xs text-violet-400 tracking-widest uppercase">ΩStack Language</span>
            </div>
            <h1 className="text-xl font-bold text-white mt-1">
              Adaptive Zero-Repulsion Stabilizer — <span className="text-violet-400">Ω6</span>
            </h1>
          </div>
          <Link to="/" className="text-xs px-3 py-1.5 rounded border border-cyan-700 text-cyan-400 hover:bg-cyan-900/20 transition-colors tracking-wider uppercase font-mono hidden md:block">
            ← QStack
          </Link>
          <div className="text-right hidden md:block">
            <div className="text-xs text-gray-500">RH Spectral Route</div>
            <div className="text-xs text-gray-600 mt-1">δ₀ = 0.20 · ‖R_N^ζ(T)‖_op target</div>
          </div>
        </div>
      </header>

      {/* Proof chain bar */}
      <div className="bg-[#0a0c12] border-b border-gray-800 px-6 py-2">
        <div className="max-w-6xl mx-auto flex items-center gap-2 overflow-x-auto text-[10px] font-mono text-gray-600">
          {["Mellin-L²", "→", "Zero-Density Simplex α_j", "→", "SZD + Ω6", "→", "Coeff Cage", "→", "‖R_N^ζ‖<0.20", "→", "RH"].map((s, i) => (
            <span key={i} className={`whitespace-nowrap ${s === "RH" ? "text-violet-400 font-bold" : s.startsWith("→") ? "text-gray-700" : ""}`}>{s}</span>
          ))}
        </div>
      </div>

      {/* Tab Bar */}
      <nav className="border-b border-gray-800 bg-[#10131a] px-6">
        <div className="max-w-6xl mx-auto flex gap-0 overflow-x-auto">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 text-xs tracking-wider uppercase border-b-2 transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? "border-violet-400 text-violet-400"
                  : "border-transparent text-gray-500 hover:text-gray-300"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {activeTab === "operators" && <OmegaPanel />}
        {activeTab === "zeros"     && <ZeroShellViz />}
        {activeTab === "hierarchy" && <SpectralShellHierarchy />}
        {activeTab === "route"     && <RHRouteMap />}
        {activeTab === "theorems"  && <RHTheoremBlock />}
        {activeTab === "summary"   && <RHSummaryCard />}
        {activeTab === "shells"    && <ShellTopologyMap />}
        {activeTab === "h3rh"     && <H3ZeroCorrelation />}
      </main>
    </div>
  );
}