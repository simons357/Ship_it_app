import React, { useState } from "react";
import { Link } from "react-router-dom";
import OperatorPanel from "../components/qstack/OperatorPanel";
import ShellEnergyViz from "../components/qstack/ShellEnergyViz";
import TheoremBlock from "../components/qstack/TheoremBlock";
import Q6Detail from "../components/qstack/Q6Detail";
import H3RouteMap from "../components/qstack/H3RouteMap";
import RHPanel from "../components/qstack/RHPanel";
import H3SummaryCard from "../components/qstack/H3SummaryCard";
import Q6DampingViz from "../components/qstack/Q6DampingViz";
import Q6SND from "../components/qstack/Q6SNDBridge";
import SpectralIntersectionGraph from "../components/qstack/SpectralIntersectionGraph";
import ShellTopologyMap from "../components/shared/ShellTopologyMap";
import H3ZeroCorrelation from "../components/shared/H3ZeroCorrelation";
import FormulaReference from "../components/shared/FormulaReference";

const TABS = [
  { id: "overview", label: "Operator Stack" },
  { id: "q6", label: "Q6 Definition" },
  { id: "shell", label: "Shell Visualizer" },
  { id: "h3", label: "H3 Route" },
  { id: "theorem", label: "Theorems" },
  { id: "h3card", label: "H3 Card" },
  { id: "q6damp", label: "Q6 Damping" },
  { id: "snd",    label: "Q6↔SND" },
  { id: "intersect", label: "Boundary Map" },
  { id: "shells", label: "Shell Map" },
  { id: "h3rh", label: "H3↔RH" },
  { id: "rh", label: "RH" },
];

export default function QStackDashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="min-h-screen bg-[#0d0f14] text-gray-100 font-mono">
      <FormulaReference />
      {/* Header */}
      <header className="border-b border-gray-800 bg-[#10131a] px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
              <span className="text-xs text-cyan-400 tracking-widest uppercase">QStack Language</span>
            </div>
            <h1 className="text-xl font-bold text-white mt-1">
              Adaptive Spectral Stabilizer — <span className="text-cyan-400">Q6</span>
            </h1>
          </div>
          <div className="hidden md:flex gap-2">
            <Link to="/explorer" className="text-xs px-3 py-1.5 rounded border border-cyan-800 text-cyan-400 hover:bg-cyan-900/20 transition-colors tracking-wider uppercase font-mono">
              3D →
            </Link>
            <Link to="/gallery" className="text-xs px-3 py-1.5 rounded border border-pink-800 text-pink-400 hover:bg-pink-900/20 transition-colors tracking-wider uppercase font-mono">
              Gallery →
            </Link>
            <Link to="/rh" className="text-xs px-3 py-1.5 rounded border border-violet-700 text-violet-400 hover:bg-violet-900/20 transition-colors tracking-wider uppercase font-mono">
              ΩStack →
            </Link>
          </div>
          <div className="text-right hidden md:block">
            <div className="text-xs text-gray-500">H3 Energy-Observable Route</div>
            <div className="text-xs text-gray-600 mt-1">δ₀ = 0.20 · ‖R_N(t)‖_op target</div>
          </div>
        </div>
      </header>

      {/* Tab Bar */}
      <nav className="border-b border-gray-800 bg-[#10131a] px-6">
        <div className="max-w-6xl mx-auto flex gap-0 overflow-x-auto">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 text-xs tracking-wider uppercase border-b-2 transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? "border-cyan-400 text-cyan-400"
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
        {activeTab === "overview" && <OperatorPanel />}
        {activeTab === "q6" && <Q6Detail />}
        {activeTab === "shell" && <ShellEnergyViz />}
        {activeTab === "h3" && <H3RouteMap />}
        {activeTab === "theorem" && <TheoremBlock />}
        {activeTab === "h3card" && <H3SummaryCard />}
        {activeTab === "q6damp" && <Q6DampingViz />}
        {activeTab === "snd"    && <Q6SND />}
        {activeTab === "intersect" && <SpectralIntersectionGraph />}
        {activeTab === "shells" && <ShellTopologyMap />}
        {activeTab === "h3rh"  && <H3ZeroCorrelation />}
        {activeTab === "rh" && <RHPanel />}
      </main>
    </div>
  );
}
