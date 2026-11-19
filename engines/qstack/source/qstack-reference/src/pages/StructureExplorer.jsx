import React, { useState } from "react";
import { Link } from "react-router-dom";
import Explorer3DCanvas from "../components/explorer/Explorer3DCanvas";
import LayerPanel from "../components/explorer/LayerPanel";
import MeasurementPanel from "../components/explorer/MeasurementPanel";
import CrossSectionPanel from "../components/explorer/CrossSectionPanel";

const TOOLS = ["layers", "measure", "crosssection"];

export default function StructureExplorer() {
  const [layers, setLayers] = useState({
    simplex:   { on: true,  label: "Simplex Δ_N",       color: "#22d3ee" },
    spectral:  { on: true,  label: "Spectral Floor",     color: "#a78bfa" },
    cascade:   { on: true,  label: "Energy Cascade",     color: "#f59e0b" },
    zeros:     { on: true,  label: "Zeta Zeros",         color: "#ec4899" },
    snd:       { on: false, label: "SND Tube ℓ¹",        color: "#34d399" },
    connections:{ on: true, label: "Entanglement Links", color: "#6366f1" },
  });

  const [activeTool, setActiveTool] = useState("layers");
  const [crossSection, setCrossSection] = useState({ axis: "y", value: 0 });
  const [measurement, setMeasurement] = useState(null); // set by canvas pick
  const [params, setParams] = useState({
    eta: 0.18,
    kappa: 0.8,
    N: 12,
    lambdaGap: 0.3,
    time: 0,
    animating: true,
  });

  function toggleLayer(key) {
    setLayers(l => ({ ...l, [key]: { ...l[key], on: !l[key].on } }));
  }

  return (
    <div className="h-screen bg-[#04050a] text-gray-100 font-mono flex flex-col overflow-hidden">
      {/* Top bar */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-gray-800 bg-[#06080e] flex-shrink-0">
        <div className="flex items-center gap-4">
          <Link to="/gallery" className="text-[10px] text-gray-600 hover:text-gray-300 tracking-widest uppercase transition-colors">
            ← Gallery
          </Link>
          <div className="w-px h-4 bg-gray-800" />
          <span className="text-xs text-white font-bold tracking-wider">3D Structure Explorer</span>
          <div className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-[9px] text-gray-600">live</span>
          </div>
        </div>

        {/* Tool selector */}
        <div className="flex gap-1">
          {[
            { id: "layers",     label: "Layers",       icon: "◫" },
            { id: "measure",    label: "Measure",      icon: "⊷" },
            { id: "crosssection", label: "Cross Section", icon: "⊡" },
          ].map(t => (
            <button key={t.id} onClick={() => setActiveTool(t.id)}
              className={`px-3 py-1.5 text-[10px] rounded border transition-colors tracking-wider uppercase flex items-center gap-1.5 ${
                activeTool === t.id
                  ? "border-cyan-700 bg-cyan-900/20 text-cyan-300"
                  : "border-gray-800 text-gray-500 hover:border-gray-700 hover:text-gray-300"
              }`}>
              <span>{t.icon}</span>{t.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setParams(p => ({ ...p, animating: !p.animating }))}
            className={`text-[10px] px-2 py-1 rounded border transition-colors ${
              params.animating ? "border-cyan-700 text-cyan-400" : "border-gray-700 text-gray-500"
            }`}>
            {params.animating ? "⏸ Pause" : "▶ Animate"}
          </button>
          <Link to="/" className="text-[10px] text-gray-600 hover:text-gray-300 tracking-widest uppercase">QStack →</Link>
        </div>
      </div>

      {/* Main layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* 3D Viewport */}
        <div className="flex-1 relative">
          <Explorer3DCanvas
            layers={layers}
            params={params}
            setParams={setParams}
            crossSection={crossSection}
            onMeasure={setMeasurement}
          />
          {/* 3D viewport hint */}
          <div className="absolute bottom-4 left-4 text-[9px] text-gray-700 font-mono space-y-0.5 pointer-events-none">
            <div>Left drag — rotate</div>
            <div>Right drag — pan</div>
            <div>Scroll — zoom</div>
            <div>Click object — measure</div>
          </div>
        </div>

        {/* Right panel */}
        <div className="w-72 border-l border-gray-800 bg-[#06080e] flex flex-col overflow-y-auto flex-shrink-0">
          {activeTool === "layers" && (
            <LayerPanel layers={layers} toggleLayer={toggleLayer} params={params} setParams={setParams} />
          )}
          {activeTool === "measure" && (
            <MeasurementPanel measurement={measurement} params={params} layers={layers} />
          )}
          {activeTool === "crosssection" && (
            <CrossSectionPanel crossSection={crossSection} setCrossSection={setCrossSection} params={params} />
          )}
        </div>
      </div>
    </div>
  );
}