import React, { useState, useEffect, useRef } from "react";
import { MB, ML } from "../qstack/MathBlock";

// ── NS Shell config ──────────────────────────────────────────────
const N_NS = 12;
const NS_CRIT = 1 / N_NS;

function initNS() {
  return Array.from({ length: N_NS }, (_, j) => {
    const ref = Math.exp(-0.35 * j) * (0.6 + 0.2 * Math.sin(j * 1.1));
    return {
      j,
      energy: ref * (1 + (Math.random() - 0.5) * 0.2),
      ref,
      delta: 0,
      stable: true,
    };
  });
}

// ── RH Zero-Shell config ─────────────────────────────────────────
const KNOWN_ZEROS = [
  14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774,
  52.970, 56.446, 59.347, 60.832, 65.113, 67.080, 69.546, 72.067, 75.705, 77.145,
];
const N_RH = 12;
const BAND_W = 6.0;

function initRH() {
  return Array.from({ length: N_RH }, (_, j) => {
    const Tj = 14.0 + j * BAND_W;
    const zeros = KNOWN_ZEROS.filter(z => z >= Tj && z < Tj + BAND_W);
    const deviation = zeros.length > 0 ? 0.008 + Math.random() * 0.02 : Math.random() * 0.07;
    return {
      j,
      Tj,
      bandEnd: Tj + BAND_W,
      zeros,
      deviation,
      gap: Math.max(0, 0.5 - deviation),
      stable: deviation < 0.04,
    };
  });
}

// ── Correlation engine ───────────────────────────────────────────
// Hypothesis: NS shell j stable ↔ RH shell j has small deviation
// Both normalized on [0,1]; Pearson-style comparison
function computeCorrelation(nsShells, rhShells) {
  const n = Math.min(nsShells.length, rhShells.length);
  const nsStab = nsShells.slice(0, n).map(s => s.stable ? 1 : 0);
  const rhStab = rhShells.slice(0, n).map(s => s.stable ? 1 : 0);
  const both = nsStab.reduce((acc, v, i) => acc + (v === 1 && rhStab[i] === 1 ? 1 : 0), 0);
  const nsOnly = nsStab.reduce((acc, v, i) => acc + (v === 1 && rhStab[i] === 0 ? 1 : 0), 0);
  const rhOnly = nsStab.reduce((acc, v, i) => acc + (v === 0 && rhStab[i] === 1 ? 1 : 0), 0);
  const neither = n - both - nsOnly - rhOnly;
  const corr = both / n; // fraction of jointly stable shells
  return { both, nsOnly, rhOnly, neither, n, corr };
}

// ── Color helpers ────────────────────────────────────────────────
const nsColor  = (stable, energy, ref) => {
  if (!stable) return "#ef4444";
  const ratio = energy / ref;
  if (ratio > 1.15) return "#f59e0b";
  return "#22d3ee";
};
const rhColor = (stable, dev) => {
  if (!stable) return "#ef4444";
  if (dev > 0.025) return "#f59e0b";
  return "#a78bfa";
};

// ── Spark line ───────────────────────────────────────────────────
function SparkLine({ history, color, height = 36 }) {
  if (history.length < 2) return null;
  const max = Math.max(...history, 0.001);
  const W = 200, H = height;
  const pts = history.map((v, i) => `${(i / (history.length - 1)) * W},${H - (v / max) * (H - 4)}`).join(" ");
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ height }}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth={1.5} opacity={0.8} />
    </svg>
  );
}

export default function H3ZeroCorrelation() {
  const [nsShells, setNsShells] = useState(initNS);
  const [rhShells, setRhShells] = useState(initRH);
  const [running, setRunning]   = useState(false);
  const [q6On, setQ6On]         = useState(true);
  const [omega6On, setOmega6On] = useState(true);
  const [selected, setSelected] = useState(null); // index 0..N_NS-1
  const [corrHistory, setCorrHistory] = useState([]);
  const [nsEnergyH, setNsEnergyH] = useState([]);   // dominant shell energy history
  const [rhDevH, setRhDevH]       = useState([]);   // dominant shell deviation history
  const [events, setEvents]       = useState([]);
  const tick = useRef(0);

  // ── Simulation tick ──────────────────────────────────────────
  useEffect(() => {
    if (!running) return;
    const id = setInterval(() => {
      tick.current += 1;

      setNsShells(prev => {
        const next = prev.map(s => {
          let e = Math.max(0.005, s.energy + (Math.random() - 0.49) * 0.018);
          // Energy cascade: flow toward dominant shell
          const js = prev.indexOf(prev.reduce((a, b) => b.energy > a.energy ? b : a));
          if (s.j !== js) e += 0.003 * (prev[js].energy - s.energy) * 0.15;
          // Q6: damp if dominant shell exceeds 2× critical
          if (q6On && s.j === js && e / (prev.reduce((a, b) => a + b.energy, 0) / N_NS) > 2.2) {
            e *= 0.93;
          }
          const total = prev.reduce((a, b) => a + b.energy, 0);
          const a_j = s.energy / total;
          const delta = Math.abs(a_j - NS_CRIT);
          return { ...s, energy: e, delta, stable: delta < 0.20 };
        });
        return next;
      });

      setRhShells(prev => prev.map(s => {
        let dev = Math.max(0, s.deviation + (Math.random() - 0.49) * 0.006);
        if (omega6On && dev > 0.03) dev *= (1 - 0.07);
        dev = Math.min(0.15, dev);
        return { ...s, deviation: dev, gap: Math.max(0, 0.5 - dev), stable: dev < 0.04 };
      }));

    }, 300);
    return () => clearInterval(id);
  }, [running, q6On, omega6On]);

  // ── Track correlation history ────────────────────────────────
  useEffect(() => {
    const c = computeCorrelation(nsShells, rhShells);
    setCorrHistory(h => [...h.slice(-60), c.corr]);

    const domNS = nsShells.reduce((a, b) => b.energy > a.energy ? b : a);
    const domRH = rhShells.reduce((a, b) => b.deviation > a.deviation ? b : a);
    setNsEnergyH(h => [...h.slice(-60), domNS.energy]);
    setRhDevH(h => [...h.slice(-60), domRH.deviation]);

    // Events
    if (running && tick.current % 4 === 0) {
      const bothUnstable = nsShells.filter(s => !s.stable).length > 2 && rhShells.filter(s => !s.stable).length > 2;
      if (bothUnstable) {
        setEvents(ev => [`t=${tick.current} · Both domains destabilizing — Q6↔Ω6 link stressed`, ...ev].slice(0, 6));
      }
      const jointStable = nsShells.every(s => s.stable) && rhShells.every(s => s.stable);
      if (jointStable && tick.current > 5) {
        setEvents(ev => [`t=${tick.current} · Full joint stability — H3 ∩ RH condition met`, ...ev].slice(0, 6));
      }
    }
  }, [nsShells, rhShells]);

  const corr = computeCorrelation(nsShells, rhShells);
  const nsUnstable = nsShells.filter(s => !s.stable).length;
  const rhUnstable = rhShells.filter(s => !s.stable).length;
  const jointHealth = corr.corr;
  const selNS = selected !== null ? nsShells[selected] : null;
  const selRH = selected !== null ? rhShells[Math.min(selected, N_RH - 1)] : null;

  return (
    <div className="space-y-5 max-w-5xl mx-auto">

      {/* ── Header ── */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className={`w-2 h-2 rounded-full ${jointHealth > 0.8 ? "bg-emerald-400" : jointHealth > 0.5 ? "bg-amber-400" : "bg-rose-500"} animate-pulse`} />
            <span className={`text-xs font-mono uppercase tracking-widest ${jointHealth > 0.8 ? "text-emerald-400" : jointHealth > 0.5 ? "text-amber-400" : "text-rose-400"}`}>
              Joint Stability: {(jointHealth * 100).toFixed(0)}%
            </span>
          </div>
          <h2 className="text-lg font-bold text-white">H3 ↔ Zero-Shell Correlation</h2>
          <p className="text-xs text-gray-400 mt-1">
            NS energy shells (Q6) linked live to RH zero-density shells (Ω6). Click any row to inspect the coupled pair.
          </p>
        </div>

        <div className="flex gap-3 flex-wrap">
          {[
            { label: "Joint stable", value: corr.both, color: "#22d3ee" },
            { label: "NS only", value: corr.nsOnly, color: "#f59e0b" },
            { label: "RH only", value: corr.rhOnly, color: "#a78bfa" },
            { label: "Neither", value: corr.neither, color: "#ef4444" },
          ].map(m => (
            <div key={m.label} className="bg-[#0a0c12] border border-gray-800 rounded px-3 py-2 text-center min-w-[66px]">
              <div className="text-[9px] text-gray-600 uppercase tracking-widest">{m.label}</div>
              <div className="text-lg font-bold font-mono mt-0.5" style={{ color: m.color }}>{m.value}</div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Controls ── */}
      <div className="flex flex-wrap gap-2 items-center">
        <button onClick={() => setRunning(r => !r)}
          className={`px-3 py-1.5 text-xs font-mono border rounded transition-colors ${running ? "border-cyan-600 bg-cyan-900/20 text-cyan-300" : "border-gray-700 text-gray-400 hover:border-gray-500"}`}>
          {running ? "⏸ Pause" : "▶ Simulate"}
        </button>
        <button onClick={() => { setNsShells(initNS()); setRhShells(initRH()); setCorrHistory([]); setEvents([]); tick.current = 0; }}
          className="px-3 py-1.5 text-xs font-mono border border-gray-700 text-gray-400 hover:text-gray-200 rounded transition-colors">
          ↺ Reset
        </button>

        <label className="flex items-center gap-1.5 text-xs text-gray-400 cursor-pointer ml-2">
          <div onClick={() => setQ6On(v => !v)}
            className={`w-8 h-4 rounded-full relative transition-colors ${q6On ? "bg-cyan-700" : "bg-gray-700"}`}>
            <div className={`absolute top-0.5 w-3 h-3 rounded-full bg-white transition-all ${q6On ? "left-4" : "left-0.5"}`} />
          </div>
          <span className="text-cyan-500">Q6</span>
        </label>

        <label className="flex items-center gap-1.5 text-xs text-gray-400 cursor-pointer">
          <div onClick={() => setOmega6On(v => !v)}
            className={`w-8 h-4 rounded-full relative transition-colors ${omega6On ? "bg-violet-700" : "bg-gray-700"}`}>
            <div className={`absolute top-0.5 w-3 h-3 rounded-full bg-white transition-all ${omega6On ? "left-4" : "left-0.5"}`} />
          </div>
          <span className="text-violet-500">Ω6</span>
        </label>
      </div>

      {/* ── Correlation history sparkline ── */}
      <div className="bg-[#080a10] border border-gray-800 rounded-lg px-4 pt-3 pb-2">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] text-gray-600 uppercase tracking-widest">Joint stability over time</span>
          <span className={`text-xs font-mono font-bold ${jointHealth > 0.8 ? "text-emerald-400" : jointHealth > 0.5 ? "text-amber-400" : "text-rose-400"}`}>
            {(jointHealth * 100).toFixed(0)}%
          </span>
        </div>
        <SparkLine history={corrHistory} color={jointHealth > 0.8 ? "#22d3ee" : jointHealth > 0.5 ? "#f59e0b" : "#ef4444"} height={40} />
        <div className="flex justify-between text-[8px] text-gray-800 mt-0.5 font-mono">
          <span>t-60</span><span>now</span>
        </div>
      </div>

      {/* ── Main linked grid ── */}
      <div className="bg-[#080a10] border border-gray-800 rounded-lg overflow-hidden">
        {/* Column headers */}
        <div className="grid grid-cols-11 border-b border-gray-800 text-[9px] uppercase tracking-widest text-gray-600">
          <div className="col-span-1 px-3 py-2 border-r border-gray-800">j</div>
          <div className="col-span-4 px-3 py-2 text-cyan-700 border-r border-gray-800">QStack NS Shell — H3 Energy</div>
          <div className="col-span-1 px-3 py-2 text-center border-r border-gray-800">link</div>
          <div className="col-span-5 px-3 py-2 text-violet-700">ΩStack RH Shell — Zero Deviation</div>
        </div>

        {Array.from({ length: Math.min(N_NS, N_RH) }, (_, i) => {
          const ns = nsShells[i];
          const rh = rhShells[i];
          const isSel = selected === i;
          const jointStable = ns.stable && rh.stable;
          const nsE = ns.energy;
          const refE = ns.ref;
          const energyPct = Math.min(100, (nsE / (refE * 1.8)) * 100);
          const devPct = Math.min(100, (rh.deviation / 0.12) * 100);
          const nc = nsColor(ns.stable, nsE, refE);
          const rc = rhColor(rh.stable, rh.deviation);

          return (
            <div key={i}
              onClick={() => setSelected(isSel ? null : i)}
              className={`grid grid-cols-11 items-center border-b border-gray-800/40 cursor-pointer transition-all ${isSel ? "bg-white/5 ring-inset ring-1 ring-white/10" : "hover:bg-white/2"}`}
            >
              {/* Index */}
              <div className="col-span-1 px-3 py-2.5 text-xs font-mono text-gray-600 border-r border-gray-800/40">{i + 1}</div>

              {/* NS panel */}
              <div className="col-span-4 px-3 py-2.5 border-r border-gray-800/40">
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: nc, boxShadow: `0 0 4px ${nc}` }} />
                  <span className="text-[10px] font-mono" style={{ color: nc }}>P_{i + 1}</span>
                  <span className="text-[9px] text-gray-700 font-mono ml-auto">{(nsE).toFixed(3)}</span>
                </div>
                <div className="h-2 bg-gray-900 rounded relative">
                  <div className="h-full rounded transition-all duration-300" style={{ width: `${energyPct}%`, backgroundColor: nc, opacity: 0.8 }} />
                  {/* Ref marker */}
                  <div className="absolute top-0 bottom-0 w-px bg-white/20" style={{ left: `${(refE / (refE * 1.8)) * 100}%` }} />
                </div>
                <div className="flex justify-between mt-0.5">
                  <span className="text-[8px] text-gray-700 font-mono">δ={ns.delta.toFixed(3)}</span>
                  <span className="text-[8px] font-mono" style={{ color: nc }}>{ns.stable ? "stable" : "WARN"}</span>
                </div>
              </div>

              {/* Link column */}
              <div className="col-span-1 flex items-center justify-center border-r border-gray-800/40 py-2.5">
                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${jointStable ? "border-emerald-600 bg-emerald-900/30" : "border-rose-700 bg-rose-900/20"}`}>
                  <span className="text-[8px]">{jointStable ? "✓" : "✗"}</span>
                </div>
              </div>

              {/* RH panel */}
              <div className="col-span-5 px-3 py-2.5">
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: rc, boxShadow: `0 0 4px ${rc}` }} />
                  <span className="text-[10px] font-mono" style={{ color: rc }}>Π{i + 1}^ζ</span>
                  <span className="text-[9px] text-gray-700 font-mono">Im∈[{rh.Tj.toFixed(0)},{rh.bandEnd.toFixed(0)})</span>
                  <span className="text-[9px] text-violet-700 font-mono ml-auto">{rh.zeros.length} zero{rh.zeros.length !== 1 ? "s" : ""}</span>
                </div>
                <div className="h-2 bg-gray-900 rounded relative">
                  <div className="h-full rounded transition-all duration-300" style={{ width: `${devPct}%`, backgroundColor: rc, opacity: 0.8 }} />
                  {/* Threshold marker at 0.04 */}
                  <div className="absolute top-0 bottom-0 w-px bg-white/20" style={{ left: `${(0.04 / 0.12) * 100}%` }} />
                </div>
                <div className="flex justify-between mt-0.5">
                  <span className="text-[8px] text-gray-700 font-mono">dev={rh.deviation.toFixed(4)}</span>
                  <span className="text-[8px] font-mono" style={{ color: rc }}>gap={rh.gap.toFixed(3)}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* ── Detail panel for selected shell pair ── */}
      {selNS && selRH && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* NS detail */}
          <div className="bg-[#080a10] border border-cyan-900/40 rounded-lg p-4 space-y-3">
            <div className="text-xs text-cyan-600 uppercase tracking-widest">NS Shell {selected + 1} — H3 State</div>
            <MB>{`\\|P_{${selected+1}} u(t)\\|^2_{L^2} = ${selNS.energy.toFixed(4)}`}</MB>
            <div className="space-y-1 text-xs">
              {[
                ["Energy", selNS.energy.toFixed(5)],
                ["Reference γ_j", selNS.ref.toFixed(5)],
                ["Δγ_j", selNS.delta.toFixed(5)],
                ["Stable (δ<0.20)?", selNS.stable ? "✓ Yes" : "✗ No"],
                ["H3 contribution", selNS.stable ? "CLEAR" : "AT RISK"],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between border-b border-gray-800/40 pb-1">
                  <span className="text-gray-600 font-mono">{k}</span>
                  <span className="font-mono text-cyan-300">{v}</span>
                </div>
              ))}
            </div>
            <div>
              <div className="text-[9px] text-gray-600 mb-1">Energy history</div>
              <SparkLine history={nsEnergyH} color="#22d3ee" height={32} />
            </div>
          </div>

          {/* RH detail */}
          <div className="bg-[#080a10] border border-violet-900/40 rounded-lg p-4 space-y-3">
            <div className="text-xs text-violet-600 uppercase tracking-widest">RH Shell {selected + 1} — Zero State</div>
            <MB>{`\\Pi_{${selected+1}}^\\zeta:\\;\\mathrm{Im}\\in[${selRH.Tj.toFixed(1)},${selRH.bandEnd.toFixed(1)})`}</MB>
            <div className="space-y-1 text-xs">
              {[
                ["Zeros in band", selRH.zeros.length],
                ["Deviation σ_j", selRH.deviation.toFixed(5)],
                ["Spectral gap λ", selRH.gap.toFixed(5)],
                ["Stable (σ<0.04)?", selRH.stable ? "✓ Yes" : "✗ No"],
                ["RH contribution", selRH.stable ? "CERTIFIED" : "UNCERTAIN"],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between border-b border-gray-800/40 pb-1">
                  <span className="text-gray-600 font-mono">{k}</span>
                  <span className="font-mono text-violet-300">{v}</span>
                </div>
              ))}
            </div>
            {selRH.zeros.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {selRH.zeros.map((z, i) => (
                  <span key={i} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-violet-900/30 text-violet-400 border border-violet-800/40">
                    ρ={z.toFixed(3)}
                  </span>
                ))}
              </div>
            )}
            <div>
              <div className="text-[9px] text-gray-600 mb-1">Deviation history</div>
              <SparkLine history={rhDevH} color="#a78bfa" height={32} />
            </div>
          </div>

          {/* Cross-domain insight */}
          <div className="md:col-span-2 bg-[#080a10] border border-gray-700 rounded-lg p-4">
            <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Cross-Domain Insight — Shell {selected + 1}</div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div>
                <div className="text-gray-600 mb-1">Joint status</div>
                <div className={`text-base font-bold font-mono ${selNS.stable && selRH.stable ? "text-emerald-400" : "text-rose-400"}`}>
                  {selNS.stable && selRH.stable ? "✓ JOINTLY STABLE" : "✗ DECOUPLED"}
                </div>
              </div>
              <div>
                <div className="text-gray-600 mb-1">Hypothesis</div>
                <div className="text-gray-400 text-[10px] leading-relaxed">
                  {selNS.stable && selRH.stable
                    ? "NS shell is energetically bounded AND corresponding RH zeros stay on Re=½. Supports the spectral-gap analogy."
                    : selNS.stable && !selRH.stable
                    ? "NS is stable but RH zero drifts — gap in spectral analogy at this index."
                    : !selNS.stable && selRH.stable
                    ? "NS energy concentrates while RH holds. Analogy breaks in this direction."
                    : "Both unstable — cascade + zero-drift co-occurring. Q6 and Ω6 both stressed."}
                </div>
              </div>
              <div>
                <div className="text-gray-600 mb-2">Formal bridge</div>
                <MB>{"a_j[u]\\leftrightarrow\\alpha_j(T)\\in\\Delta_N"}</MB>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Correlation SVG scatter plot ── */}
      <div className="bg-[#080a10] border border-gray-800 rounded-lg p-4">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">NS Δγ_j vs RH deviation σ_j — scatter (all shells)</div>
        <div className="relative" style={{ height: 200 }}>
          <svg viewBox="0 0 600 200" className="w-full h-full">
            {/* Grid */}
            {[0.25, 0.5, 0.75].map(v => (
              <g key={v}>
                <line x1={40} y1={v * 180 + 10} x2={580} y2={v * 180 + 10} stroke="#111827" strokeWidth={0.5} />
                <line x1={40 + v * 540} y1={10} x2={40 + v * 540} y2={190} stroke="#111827" strokeWidth={0.5} />
              </g>
            ))}
            {/* Axes */}
            <line x1={40} y1={190} x2={580} y2={190} stroke="#1e293b" strokeWidth={1} />
            <line x1={40} y1={10} x2={40} y2={190} stroke="#1e293b" strokeWidth={1} />
            <text x={310} y={200} textAnchor="middle" fill="#374151" fontSize={8}>NS Δγ_j (shell deviation)</text>
            <text x={10} y={100} fill="#374151" fontSize={8} transform="rotate(-90,10,100)">RH σ_j</text>

            {/* Stability threshold lines */}
            <line x1={40 + (0.20 / 0.5) * 540} y1={10} x2={40 + (0.20 / 0.5) * 540} y2={190}
              stroke="#22d3ee" strokeWidth={0.8} strokeDasharray="4,3" opacity={0.4} />
            <line x1={40} y1={190 - (0.04 / 0.15) * 180} x2={580} y2={190 - (0.04 / 0.15) * 180}
              stroke="#a78bfa" strokeWidth={0.8} strokeDasharray="4,3" opacity={0.4} />

            {/* Data points */}
            {nsShells.slice(0, N_RH).map((ns, i) => {
              const rh = rhShells[i];
              const x = 40 + (Math.min(ns.delta, 0.5) / 0.5) * 540;
              const y = 190 - (Math.min(rh.deviation, 0.15) / 0.15) * 180;
              const c = ns.stable && rh.stable ? "#22d3ee" : ns.stable ? "#f59e0b" : rh.stable ? "#a78bfa" : "#ef4444";
              const isSel = selected === i;
              return (
                <g key={i} onClick={() => setSelected(isSel ? null : i)} style={{ cursor: "pointer" }}>
                  <circle cx={x} cy={y} r={isSel ? 7 : 5} fill={c} opacity={0.9}
                    style={{ filter: `drop-shadow(0 0 ${isSel ? 6 : 3}px ${c})` }} />
                  <text x={x + 6} y={y - 3} fill={c} fontSize={7} fontFamily="monospace" opacity={0.7}>{i + 1}</text>
                </g>
              );
            })}

            {/* Quadrant labels */}
            <text x={80} y={25} fill="#22d3ee" fontSize={7} opacity={0.4}>jointly stable</text>
            <text x={400} y={25} fill="#f59e0b" fontSize={7} opacity={0.4}>NS warn / RH ok</text>
            <text x={80} y={185} fill="#a78bfa" fontSize={7} opacity={0.4}>NS ok / RH drift</text>
            <text x={390} y={185} fill="#ef4444" fontSize={7} opacity={0.4}>both unstable</text>
          </svg>
        </div>
        <div className="flex gap-4 mt-1 text-[9px] text-gray-600">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-cyan-400 inline-block" /> Jointly stable</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-400 inline-block" /> NS warn</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-violet-400 inline-block" /> RH drift</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-500 inline-block" /> Both unstable</span>
          <span className="ml-auto flex items-center gap-1 text-cyan-800">— NS threshold (Δγ&lt;0.20)</span>
          <span className="flex items-center gap-1 text-violet-800">— RH threshold (σ&lt;0.04)</span>
        </div>
      </div>

      {/* ── Formal bridge ── */}
      <div className="bg-[#080a10] border border-gray-700 rounded-lg p-5 space-y-3">
        <div className="text-xs text-gray-500 uppercase tracking-widest">H3 ↔ RH Formal Bridge</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <div className="text-[10px] text-cyan-600 mb-2">H3 condition (NS)</div>
            <MB>{"\\sup_{t\\ge0}\\|R_N(t)\\|_{\\mathrm{op}} < 0.20 \\iff \\max_j|\\Delta\\gamma_j(t)| < 0.20"}</MB>
          </div>
          <div>
            <div className="text-[10px] text-violet-600 mb-2">RH condition (ΩStack)</div>
            <MB>{"\\sup_T\\|R_N^\\zeta(T)\\|_{\\mathrm{op}} < 0.20 \\iff \\max_j\\sigma_j(T) < 0.04"}</MB>
          </div>
        </div>
        <div className="border-t border-gray-800 pt-3">
          <MB>{"a_j[u(t)] \\longleftrightarrow \\alpha_j(T),\\quad \\Delta\\gamma_j \\longleftrightarrow \\sigma_j,\\quad Q_6 \\longleftrightarrow \\Omega_6"}</MB>
          <div className="text-[10px] text-gray-600 mt-2">
            The simplex coordinates a_j (NS energy fractions) and α_j (zero-density fractions) play identical structural roles. Stability of both requires their ℓ¹ deviation from μ to remain bounded — different physics, identical cage geometry.
          </div>
        </div>
      </div>

      {/* ── Event log ── */}
      {events.length > 0 && (
        <div className="bg-[#080a10] border border-gray-800 rounded-lg p-3 space-y-1">
          <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-2">Cross-Domain Event Log</div>
          {events.map((e, i) => (
            <div key={i} className="text-[10px] font-mono text-emerald-700">{e}</div>
          ))}
        </div>
      )}
    </div>
  );
}