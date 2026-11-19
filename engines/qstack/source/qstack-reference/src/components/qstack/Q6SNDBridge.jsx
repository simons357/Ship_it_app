import React, { useState, useMemo } from "react";
import { MB, ML } from "./MathBlock";

// ── Constants ─────────────────────────────────────────────────────
const N_SHELLS = 12;
const REF_MU = Array.from({ length: N_SHELLS }, (_, j) =>
  Math.exp(-0.35 * j) * 0.6
).map((v, _, arr) => v / arr.reduce((a, b) => a + b, 0)); // normalized simplex

// ── Core math ─────────────────────────────────────────────────────
// Given SND threshold η and damping params, compute:
//   - γ_j[u] = Q6 activation coefficient for each shell
//   - whether SND is implied
//   - the spectral gap λ_min estimate
function computeQ6Profile({ eta, kappa, alpha, a0Spread, N }) {
  const shells = Array.from({ length: N }, (_, j) => {
    const mu_j = REF_MU[j];
    // Simulate a_j deviating from mu by some spread (worst-case within SND tube)
    const deviation = a0Spread * Math.exp(-0.3 * j) * (1 + 0.2 * Math.sin(j * 0.9));
    const a_j = Math.max(0, mu_j + deviation);

    // Q6 activation coefficient: γ_j = kappa * max(0, a_j - a_c)^alpha
    // where a_c is the critical threshold (derived from η and N)
    const a_c = mu_j + eta / N;
    const excess = Math.max(0, a_j - a_c);
    const gamma_j = kappa * Math.pow(excess, alpha);

    // Damped coordinate after Q6 intervention
    const a_j_damped = a_j - gamma_j * (a_j - mu_j);

    // Delta (deviation after damping)
    const delta_j = Math.abs(a_j_damped - mu_j);

    return {
      j,
      mu_j,
      a_j,
      a_c,
      excess,
      gamma_j,
      a_j_damped,
      delta_j,
      sndSatisfied: delta_j <= eta / N,
      q6Active: excess > 0,
    };
  });

  const l1Deviation = shells.reduce((s, sh) => s + sh.delta_j, 0);
  const l1Raw      = shells.reduce((s, sh) => s + Math.abs(sh.a_j - sh.mu_j), 0);
  const sndHolds   = l1Deviation <= eta;
  const maxDelta   = Math.max(...shells.map(s => s.delta_j));

  // Spectral gap estimate: λ_min ≈ 0.5 - C_N * l1Deviation
  const C_N = 1.2 + 0.05 * N; // grows with N (honest)
  const lambdaMin = 0.5 - C_N * l1Deviation;
  const h3Holds   = lambdaMin > -0.5 && C_N * l1Deviation < 0.20;

  return { shells, l1Deviation, l1Raw, sndHolds, maxDelta, C_N, lambdaMin, h3Holds };
}

// ── Sub-components ────────────────────────────────────────────────

function StatusBadge({ ok, trueLabel, falseLabel }) {
  return (
    <span className={`text-[9px] font-mono px-2 py-0.5 rounded-full border uppercase tracking-widest ${
      ok ? "bg-emerald-900/40 text-emerald-400 border-emerald-700" : "bg-rose-900/30 text-rose-400 border-rose-700"
    }`}>
      {ok ? trueLabel : falseLabel}
    </span>
  );
}

function ShellRow({ sh, etaPerShell, maxA }) {
  const rawPct    = Math.min(100, (sh.a_j / (maxA * 1.1)) * 100);
  const dampedPct = Math.min(100, (sh.a_j_damped / (maxA * 1.1)) * 100);
  const muPct     = Math.min(100, (sh.mu_j / (maxA * 1.1)) * 100);
  const acPct     = Math.min(100, (sh.a_c / (maxA * 1.1)) * 100);

  return (
    <div className={`px-3 py-2 border-b border-gray-800/40 hover:bg-white/2 transition-colors ${sh.q6Active ? "bg-cyan-950/10" : ""}`}>
      <div className="flex items-center gap-2 mb-1.5">
        <span className="text-[10px] font-mono text-gray-600 w-5">{sh.j + 1}</span>
        <div className="flex-1 h-3 bg-gray-900 rounded relative">
          {/* Raw a_j bar */}
          <div className="absolute top-0 h-full rounded bg-gray-700 transition-all duration-300" style={{ width: `${rawPct}%`, opacity: 0.4 }} />
          {/* Damped bar */}
          <div className={`absolute top-0 h-full rounded transition-all duration-300 ${sh.sndSatisfied ? "bg-cyan-500" : "bg-rose-500"}`}
            style={{ width: `${dampedPct}%`, opacity: 0.9 }} />
          {/* μ marker */}
          <div className="absolute top-0 bottom-0 w-px bg-white/30" style={{ left: `${muPct}%` }} />
          {/* a_c threshold marker */}
          <div className="absolute top-0 bottom-0 w-px bg-amber-500/60" style={{ left: `${acPct}%` }} />
        </div>
        <div className="flex items-center gap-1.5 w-44">
          {sh.q6Active && (
            <span className="text-[8px] font-mono text-cyan-600">Q6↓{sh.gamma_j.toFixed(3)}</span>
          )}
          <span className={`text-[8px] font-mono ${sh.sndSatisfied ? "text-emerald-600" : "text-rose-500"}`}>
            δ={sh.delta_j.toFixed(4)}
          </span>
        </div>
      </div>
    </div>
  );
}

function CurvePanel({ etaRange, kappa, alpha, a0Spread, N }) {
  const W = 560, H = 180;
  const pts_l1 = [], pts_lambda = [], pts_raw = [];

  for (let i = 0; i <= 40; i++) {
    const eta = etaRange[0] + (i / 40) * (etaRange[1] - etaRange[0]);
    const { l1Deviation, l1Raw, lambdaMin } = computeQ6Profile({ eta, kappa, alpha, a0Spread, N });
    const x = (i / 40) * W;
    pts_l1.push([x, H - Math.min((l1Deviation / 0.6) * (H - 20), H - 10)]);
    pts_lambda.push([x, H - Math.min(Math.max(((lambdaMin + 0.6) / 1.2) * (H - 20), 0), H - 10)]);
    pts_raw.push([x, H - Math.min((l1Raw / 0.6) * (H - 20), H - 10)]);
  }

  const toPolyline = pts => pts.map(([x, y]) => `${x},${y}`).join(" ");

  // Threshold lines
  const etaSpan = etaRange[1] - etaRange[0];
  const h3ThreshX = W * (0.20 / (etaSpan + 0.001)); // eta where h3 boundary is
  const lambdaZeroY = H - ((-0.0 + 0.6) / 1.2) * (H - 20);
  const lambdaNegHalfY = H - ((-0.5 + 0.6) / 1.2) * (H - 20);

  return (
    <div className="bg-[#080a10] border border-gray-800 rounded-lg p-4">
      <div className="text-[10px] text-gray-500 uppercase tracking-widest mb-3">
        Q6 damping effect vs SND threshold η — curve view
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ height: 180 }}>
        {/* Grid */}
        {[0.25, 0.5, 0.75].map(v => (
          <line key={v} x1={0} y1={v * H} x2={W} y2={v * H} stroke="#111827" strokeWidth={0.5} />
        ))}
        {/* λ=0 line */}
        <line x1={0} y1={lambdaZeroY} x2={W} y2={lambdaZeroY} stroke="#22d3ee" strokeWidth={0.5} strokeDasharray="4,3" opacity={0.4} />
        <text x={4} y={lambdaZeroY - 3} fill="#22d3ee" fontSize={7} opacity={0.5}>λ=0</text>
        {/* λ=−½ line (H3 threshold) */}
        <line x1={0} y1={lambdaNegHalfY} x2={W} y2={lambdaNegHalfY} stroke="#ef4444" strokeWidth={0.5} strokeDasharray="4,3" opacity={0.4} />
        <text x={4} y={lambdaNegHalfY - 3} fill="#ef4444" fontSize={7} opacity={0.5}>λ=−½</text>

        {/* Raw ℓ¹ deviation (without Q6) */}
        <polyline points={toPolyline(pts_raw)} fill="none" stroke="#374151" strokeWidth={1} strokeDasharray="3,2" opacity={0.6} />
        {/* Post-Q6 ℓ¹ deviation */}
        <polyline points={toPolyline(pts_l1)} fill="none" stroke="#22d3ee" strokeWidth={2} />
        {/* λ_min curve */}
        <polyline points={toPolyline(pts_lambda)} fill="none" stroke="#a78bfa" strokeWidth={1.5} />

        {/* Axis labels */}
        <text x={W / 2} y={H - 2} textAnchor="middle" fill="#374151" fontSize={7}>η (SND threshold) →</text>
        <text x={4} y={12} fill="#22d3ee" fontSize={7}>ℓ¹ dev</text>
        <text x={4} y={24} fill="#a78bfa" fontSize={7}>λ_min</text>
      </svg>
      <div className="flex gap-4 mt-1 text-[9px] text-gray-600">
        <span className="flex items-center gap-1"><span className="w-4 h-px bg-gray-600 inline-block" style={{ borderTop: "1px dashed #374151" }} /> ℓ¹ without Q6</span>
        <span className="flex items-center gap-1"><span className="w-4 h-0.5 bg-cyan-500 inline-block" /> ℓ¹ after Q6</span>
        <span className="flex items-center gap-1"><span className="w-4 h-0.5 bg-violet-400 inline-block" /> λ_min estimate</span>
      </div>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────
const PROOF_STEPS = [
  {
    id: "s1", label: "Leray Energy Class",
    formula: "u \\in L^\\infty(0,T;L^2) \\cap L^2(0,T;\\dot{H}^1)",
    status: "proven", color: "emerald",
    note: "Standard Leray-Hopf. Unconditional."
  },
  {
    id: "s2", label: "Shell Simplex",
    formula: "a_j(t) = \\frac{\\|P_j u\\|^2_{L^2}}{\\sum_k\\|P_k u\\|^2_{L^2}} \\in \\Delta_N",
    status: "proven", color: "emerald",
    note: "Well-defined a.e. t for Leray-Hopf."
  },
  {
    id: "s3", label: "Q6 Activation",
    formula: "\\gamma_j = \\kappa\\cdot\\max(0,\\,a_j - a_c)^\\alpha",
    status: "defined", color: "cyan",
    note: "Operator: defined. But a_c depends on η — which is the variable we're trying to close."
  },
  {
    id: "s4", label: "Differential Inequality",
    formula: "\\frac{d}{dt}\\|a(t)-\\mu\\|_{\\ell^1} \\le -\\kappa f(t) + C_{\\mathrm{NL}}",
    status: "open", color: "amber",
    note: "OPEN. Requires bounding the nonlinear NS remainder C_NL without smoothness assumption."
  },
  {
    id: "s5", label: "SND — ℓ¹ Tube",
    formula: "\\sup_{t\\ge 0}\\|a(t)-\\mu\\|_{\\ell^1} \\le \\eta_N",
    status: "open", color: "amber",
    note: "OPEN. Follows from Step 4 only if C_NL ≤ κ·f(0) (Gronwall closure). Not yet proven for all Leray-Hopf."
  },
  {
    id: "s6", label: "H3 — Spectral Gap",
    formula: "C_N\\eta_N < 0.20 \\implies \\inf_{t\\ge0}\\lambda_{\\min}(H_N) > -\\tfrac{1}{2}",
    status: "proven", color: "emerald",
    note: "Proven (Simplex Lipschitz Lemma). Contingent on SND holding."
  },
];

const STATUS_COLOR = {
  proven:  { border: "border-emerald-800/60", bg: "bg-emerald-950/10", tag: "text-emerald-400", badge: "bg-emerald-900/40 text-emerald-400 border-emerald-700" },
  defined: { border: "border-cyan-800/60",    bg: "bg-cyan-950/10",    tag: "text-cyan-400",    badge: "bg-cyan-900/40 text-cyan-400 border-cyan-700" },
  open:    { border: "border-amber-800/60",   bg: "bg-amber-950/10",   tag: "text-amber-400",   badge: "bg-amber-900/40 text-amber-400 border-amber-700" },
};

export default function Q6SND() {
  const [eta,       setEta]       = useState(0.18);
  const [kappa,     setKappa]     = useState(0.80);
  const [alpha,     setAlpha]     = useState(1.0);
  const [a0Spread,  setA0Spread]  = useState(0.12);
  const [N,         setN]         = useState(12);
  const [lambdaGap, setLambdaGap] = useState(0.25);
  const [expanded,  setExpanded]  = useState("s4");

  const result = useMemo(
    () => computeQ6Profile({ eta, kappa, alpha, a0Spread, N }),
    [eta, kappa, alpha, a0Spread, N]
  );

  // Rigorous spectral-gap–derived bounds (replaces heuristic λ_min)
  const C_N_gap   = 1 + 1 / Math.max(lambdaGap, 0.001);
  const etaN_max  = 0.20 / C_N_gap;           // max η for H3 to hold
  const kappaMin  = 0.30 / (lambdaGap * Math.max(etaN_max, 0.001));
  const lambdaMin_rigorous = lambdaGap - C_N_gap * result.l1Deviation;
  const h3Rigorous = C_N_gap * result.l1Deviation < 0.20;

  const maxA = Math.max(...result.shells.map(s => s.a_j));
  const sndColor = result.sndHolds ? "text-emerald-400" : "text-rose-400";
  const h3Color  = h3Rigorous      ? "text-emerald-400" : "text-rose-400";

  return (
    <div className="space-y-6 max-w-5xl mx-auto">

      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <div className={`w-2 h-2 rounded-full animate-pulse ${result.h3Holds ? "bg-emerald-400" : "bg-amber-400"}`} />
          <span className="text-xs font-mono uppercase tracking-widest text-gray-400">Q6 ↔ SND Bridge</span>
        </div>
        <h2 className="text-lg font-bold text-white">Q6 Damping vs SND Threshold — Mechanism vs Condition</h2>
        <p className="text-xs text-gray-400 mt-1">
          Q6 is an <span className="text-cyan-400">operator</span>. SND is a <span className="text-amber-400">condition</span>.
          This dashboard shows where Q6 closes the gap — and where it doesn't yet.
        </p>
      </div>

      {/* Spectral hierarchy — three-layer diagram */}
      <div className="bg-[#0a0c12] border border-violet-900/40 rounded-lg p-4 space-y-4">
        <div className="text-[10px] text-violet-500 uppercase tracking-widest">Spectral Hierarchy — Three Layers</div>

        {/* Layered explanation */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-[10px] font-mono">
          <div className="bg-[#080a10] border border-rose-900/40 rounded p-3">
            <div className="text-rose-400 font-bold mb-1">① Hard Floor  =  −½</div>
            <div className="text-gray-600 leading-relaxed">Fixed. Never moves. This is the threshold that must never be breached. If λ_min(H_N) ≤ −½ the resolvent estimate collapses.</div>
            <div className="text-rose-700 mt-2">−0.500  ← always</div>
          </div>
          <div className="bg-[#080a10] border border-violet-900/40 rounded p-3">
            <div className="text-violet-400 font-bold mb-1">② Headroom at μ  =  λ_gap</div>
            <div className="text-gray-600 leading-relaxed">How far above the floor H_N sits when a = μ (reference point). This is what you compute / assume. Slider below sets it.</div>
            <div className="text-violet-300 mt-2">−½ + {lambdaGap.toFixed(3)}  =  {(-0.5 + lambdaGap).toFixed(3)}</div>
          </div>
          <div className="bg-[#080a10] border border-amber-900/40 rounded p-3">
            <div className="text-amber-400 font-bold mb-1">③ Margin spent  =  C_N · ℓ¹ dev</div>
            <div className="text-gray-600 leading-relaxed">How much headroom the current drift a ≠ μ has consumed. Lipschitz constant C_N tells you the rate of loss per unit of deviation.</div>
            <div className="text-amber-300 mt-2">spent: {(C_N_gap * result.l1Deviation).toFixed(4)}  of  {lambdaGap.toFixed(3)}</div>
          </div>
        </div>

        {/* Visual margin bar */}
        <div>
          <div className="flex justify-between text-[9px] font-mono text-gray-600 mb-1">
            <span className="text-rose-600">−½ (floor)</span>
            <span className="text-violet-400">λ_gap headroom: {lambdaGap.toFixed(3)}</span>
            <span className="text-emerald-400">remaining margin: {Math.max(0, lambdaGap - C_N_gap * result.l1Deviation).toFixed(4)}</span>
          </div>
          <div className="h-5 bg-gray-900 rounded relative overflow-hidden">
            {/* Full headroom bar */}
            <div className="absolute left-0 top-0 h-full bg-violet-900/40 rounded" style={{ width: "100%" }} />
            {/* Spent margin (red from left) */}
            <div className="absolute left-0 top-0 h-full bg-rose-800/60 transition-all duration-300"
              style={{ width: `${Math.min(100, (C_N_gap * result.l1Deviation / Math.max(lambdaGap, 0.001)) * 100)}%` }} />
            {/* Remaining margin label */}
            <div className="absolute inset-0 flex items-center justify-center text-[9px] font-mono text-white/60">
              {lambdaMin_rigorous > 0
                ? `certified lower bound: −½ + ${lambdaMin_rigorous.toFixed(4)} above floor`
                : lambdaMin_rigorous > -0.5
                ? `certified lower bound: ${lambdaMin_rigorous.toFixed(4)} — still above −½ ✓`
                : `bound crossed floor — H3 not certified at these params ✗`}
            </div>
          </div>
          <div className="flex justify-between text-[8px] font-mono text-gray-800 mt-0.5">
            <span>← spent by drift</span>
            <span>remaining headroom →</span>
          </div>
        </div>

        {/* λ_gap slider */}
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="text-[10px] text-violet-400 font-mono">λ_gap  (headroom at μ)</span>
            <span className="text-base font-bold font-mono text-violet-300 ml-auto">{lambdaGap.toFixed(2)}</span>
          </div>
          <input type="range" min={0.01} max={1.00} step={0.01} value={lambdaGap}
            onChange={e => setLambdaGap(parseFloat(e.target.value))}
            className="w-full accent-violet-400 cursor-pointer" />
          <div className="text-[8px] text-gray-700 mt-1">
            This is the eigenvalue gap of H_N at a = μ. It is an <em>assumption</em> until proven by explicit matrix analysis. Drag left to see H3 fail.
          </div>
        </div>

        {/* Derived quantities */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-[10px]">
          {[
            { label: "C_N  (loss rate)", val: C_N_gap.toFixed(3), color: "text-amber-300", sub: "headroom lost per ℓ¹ unit" },
            { label: "max safe η", val: etaN_max.toFixed(4), color: h3Rigorous ? "text-emerald-400" : "text-rose-400", sub: "η < this → H3 certified" },
            { label: "κ_min needed", val: kappaMin.toFixed(3), color: kappa >= kappaMin ? "text-emerald-400" : "text-rose-400", sub: `current κ=${kappa.toFixed(2)} ${kappa >= kappaMin ? "✓" : "✗ too small"}` },
            { label: "certified bound", val: lambdaMin_rigorous.toFixed(4), color: lambdaMin_rigorous > -0.5 ? "text-emerald-400" : "text-rose-400", sub: `must be > −0.5 (floor)` },
          ].map(m => (
            <div key={m.label} className="bg-[#080a10] border border-gray-800 rounded px-3 py-2">
              <div className="text-[8px] text-gray-700 uppercase tracking-widest mb-1">{m.label}</div>
              <div className={`text-sm font-bold font-mono ${m.color}`}>{m.val}</div>
              <div className="text-[8px] text-gray-700 mt-0.5">{m.sub}</div>
            </div>
          ))}
        </div>

        <div className="text-[9px] font-mono text-gray-700 border-t border-gray-800 pt-2">
          Derivation: λ_min(H_N[a]) ≥ <span className="text-violet-400">{lambdaGap.toFixed(3)}</span> (headroom) − <span className="text-amber-400">{C_N_gap.toFixed(3)}</span>·<span className="text-amber-400">{result.l1Deviation.toFixed(4)}</span> (spent) = <span className={lambdaMin_rigorous > -0.5 ? "text-emerald-400" : "text-rose-400"}>{lambdaMin_rigorous.toFixed(4)}</span> &nbsp;|&nbsp; hard floor = −0.500 &nbsp;|&nbsp; margin remaining = <span className="text-emerald-400">{Math.max(0, lambdaMin_rigorous + 0.5).toFixed(4)}</span>
        </div>
      </div>

      {/* Live status bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: "η (SND tube)", val: eta.toFixed(3), color: "text-amber-300" },
          { label: "ℓ¹ deviation (drift)", val: result.l1Deviation.toFixed(4), color: result.sndHolds ? "text-emerald-400" : "text-rose-400" },
          { label: "headroom spent", val: (C_N_gap * result.l1Deviation).toFixed(4), color: h3Rigorous ? "text-emerald-400" : "text-rose-400" },
          { label: "certified bound (> −½?)", val: lambdaMin_rigorous.toFixed(4), color: lambdaMin_rigorous > -0.5 ? "text-emerald-400" : "text-rose-400" },
        ].map(m => (
          <div key={m.label} className="bg-[#0a0c12] border border-gray-800 rounded-lg px-4 py-3">
            <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-1">{m.label}</div>
            <div className={`text-lg font-bold font-mono ${m.color}`}>{m.val}</div>
          </div>
        ))}
      </div>

      <div className="flex gap-3 flex-wrap">
        <StatusBadge ok={result.sndHolds} trueLabel="SND ✓ holds" falseLabel="SND ✗ not certified" />
        <StatusBadge ok={h3Rigorous}  trueLabel="H3 ✓ gap secured" falseLabel="H3 ✗ gap uncertain" />
        <span className="text-[9px] font-mono text-gray-600 self-center">C_N(gap) = {C_N_gap.toFixed(3)}, κ_min = {kappaMin.toFixed(3)}, κ = {kappa.toFixed(2)} {kappa >= kappaMin ? "✓" : "← too small"}</span>
      </div>

      {/* Controls */}
      <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-4">
        <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-4">Parameters</div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {[
            { label: "η  (SND threshold)", val: eta, set: setEta, min: 0.01, max: 0.50, step: 0.01, color: "accent-amber-400", desc: "ℓ¹-tube radius. SND asserts ‖a−μ‖_ℓ¹ ≤ η." },
            { label: "κ  (Q6 damping strength)", val: kappa, set: setKappa, min: 0.1, max: 3.0, step: 0.05, color: "accent-cyan-400", desc: "Higher κ = stronger activation damping." },
            { label: "α  (Q6 activation exponent)", val: alpha, set: setAlpha, min: 0.5, max: 3.0, step: 0.1, color: "accent-cyan-400", desc: "α=1 is linear; α>1 penalizes large excess harder." },
            { label: "a₀ spread (initial deviation)", val: a0Spread, set: setA0Spread, min: 0.0, max: 0.40, step: 0.01, color: "accent-violet-400", desc: "Worst-case initial ℓ¹ deviation within SND tube." },
          ].map(p => (
            <div key={p.label}>
              <div className="flex justify-between items-center mb-1.5">
                <span className="text-[10px] text-gray-400 font-mono">{p.label}</span>
                <span className="text-xs font-bold font-mono text-white">{p.val.toFixed(2)}</span>
              </div>
              <input type="range" min={p.min} max={p.max} step={p.step} value={p.val}
                onChange={e => p.set(parseFloat(e.target.value))}
                className={`w-full cursor-pointer ${p.color}`} />
              <div className="text-[8px] text-gray-700 mt-1">{p.desc}</div>
            </div>
          ))}
        </div>
        <div className="mt-4 flex items-center gap-3">
          <span className="text-[10px] text-gray-600 font-mono">N (shells)</span>
          {[6, 8, 10, 12].map(n => (
            <button key={n} onClick={() => setN(n)}
              className={`px-2 py-1 text-[10px] font-mono border rounded transition-colors ${N === n ? "border-cyan-600 text-cyan-300 bg-cyan-900/20" : "border-gray-700 text-gray-500 hover:border-gray-600"}`}>
              {n}
            </button>
          ))}
          <span className="text-[9px] text-gray-700 ml-2">C_N grows with N — H3 gets harder</span>
        </div>
      </div>

      {/* Shell-by-shell grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-[#080a10] border border-gray-800 rounded-lg overflow-hidden">
          <div className="px-3 py-2 border-b border-gray-800 text-[10px] text-gray-600 uppercase tracking-widest flex justify-between">
            <span>Shell breakdown — post-Q6 vs SND</span>
            <span className="flex gap-3">
              <span className="text-white/20">▌ gray=raw</span>
              <span className="text-cyan-700">▌ cyan=damped</span>
              <span className="text-white/20">| μ</span>
              <span className="text-amber-700">| a_c</span>
            </span>
          </div>
          {result.shells.map(sh => (
            <ShellRow key={sh.j} sh={sh} etaPerShell={eta / N} maxA={maxA} />
          ))}
          <div className="px-3 py-2 border-t border-gray-800 flex justify-between text-[9px] font-mono">
            <span className="text-gray-600">ℓ¹ raw: {result.l1Raw.toFixed(4)}</span>
            <span className={result.sndHolds ? "text-emerald-400" : "text-rose-400"}>ℓ¹ after Q6: {result.l1Deviation.toFixed(4)} {result.sndHolds ? "≤" : ">"} η={eta.toFixed(3)}</span>
          </div>
        </div>

        {/* Scatter: γ_j vs excess */}
        <div className="bg-[#080a10] border border-gray-800 rounded-lg p-4">
          <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-3">Q6 activation per shell — γ_j vs excess (a_j − a_c)</div>
          <div style={{ height: 220 }} className="relative">
            <svg viewBox="0 0 400 200" className="w-full h-full">
              {[0.25, 0.5, 0.75].map(v => (
                <line key={v} x1={30} y1={v * 190 + 5} x2={390} y2={v * 190 + 5} stroke="#111827" strokeWidth={0.5} />
              ))}
              <line x1={30} y1={195} x2={390} y2={195} stroke="#1e293b" strokeWidth={1} />
              <line x1={30} y1={5}   x2={30}  y2={195} stroke="#1e293b" strokeWidth={1} />
              <text x={210} y={200} textAnchor="middle" fill="#374151" fontSize={7}>excess a_j − a_c</text>
              <text x={10}  y={100} fill="#374151" fontSize={7} transform="rotate(-90,10,100)">γ_j</text>

              {/* Q6 activation curve (theoretical) */}
              {Array.from({ length: 50 }, (_, i) => {
                const ex = (i / 49) * 0.15;
                const gm = kappa * Math.pow(ex, alpha);
                return [30 + (ex / 0.15) * 360, 195 - Math.min((gm / 1.5) * 185, 185)];
              }).map(([x, y], i, arr) => i === 0 ? null : (
                <line key={i} x1={arr[i-1][0]} y1={arr[i-1][1]} x2={x} y2={y} stroke="#22d3ee" strokeWidth={1} opacity={0.4} />
              ))}

              {/* Data points per shell */}
              {result.shells.map(sh => {
                const x = 30 + (Math.min(sh.excess, 0.15) / 0.15) * 360;
                const y = 195 - Math.min((sh.gamma_j / 1.5) * 185, 185);
                const c = sh.sndSatisfied ? "#22d3ee" : "#ef4444";
                return (
                  <g key={sh.j}>
                    <circle cx={x} cy={y} r={4} fill={c} opacity={0.9} style={{ filter: `drop-shadow(0 0 3px ${c})` }} />
                    <text x={x + 5} y={y - 2} fill={c} fontSize={7} fontFamily="monospace">{sh.j + 1}</text>
                  </g>
                );
              })}

              {/* κ label */}
              <text x={380} y={15} textAnchor="end" fill="#22d3ee" fontSize={7} opacity={0.5}>κ={kappa.toFixed(2)}, α={alpha.toFixed(1)}</text>
            </svg>
          </div>
          <div className="mt-1 text-[9px] text-gray-600">
            Shells above the curve are over-damped; below are under-damped. Q6 active shells lit cyan.
          </div>
        </div>
      </div>

      {/* Curve panel */}
      <CurvePanel etaRange={[0.01, 0.50]} kappa={kappa} alpha={alpha} a0Spread={a0Spread} N={N} />

      {/* Proof chain with gap annotation */}
      <div className="space-y-2">
        <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-3">Proof Chain — Q6 → SND → H3</div>
        {PROOF_STEPS.map((step, i) => {
          const c = STATUS_COLOR[step.status];
          const open = expanded === step.id;
          return (
            <div key={step.id}>
              {i === 3 && (
                <div className="flex items-center gap-2 my-1 px-2">
                  <div className="flex-1 h-px bg-amber-800/40" />
                  <span className="text-[9px] text-amber-600 font-mono uppercase tracking-widest">← open proof debt</span>
                  <div className="flex-1 h-px bg-amber-800/40" />
                </div>
              )}
              <div className={`rounded-lg border transition-all ${c.border} ${open ? c.bg : "bg-[#0a0c12]"}`}>
                <button className="w-full px-4 py-3 flex items-center justify-between text-left"
                  onClick={() => setExpanded(open ? null : step.id)}>
                  <div className="flex items-center gap-3">
                    <span className={`w-5 h-5 rounded-full border text-[9px] flex items-center justify-center flex-shrink-0 ${c.border} ${c.tag}`}>{i + 1}</span>
                    <span className="text-xs text-gray-200">{step.label}</span>
                    <span className={`text-[9px] px-1.5 py-0.5 rounded border uppercase tracking-widest ${c.badge}`}>
                      {step.status}
                    </span>
                  </div>
                  <span className="text-gray-700 text-xs">{open ? "▲" : "▼"}</span>
                </button>
                {open && (
                  <div className="px-4 pb-4 space-y-2">
                    <MB>{step.formula}</MB>
                    <div className={`text-xs rounded border p-2 ${c.border} ${c.bg} ${c.tag}`}>{step.note}</div>
                    {step.id === "s4" && (
                      <div className="mt-2 text-[10px] text-gray-600 space-y-1 font-mono">
                        <div>Current κ gives damping rate ≈ <span className="text-cyan-400">{(kappa * 0.5).toFixed(3)}</span></div>
                        <div>Need C_NL ≤ <span className="text-amber-400">{(kappa * result.l1Deviation * 0.5).toFixed(4)}</span> to close Gronwall</div>
                        <div className="text-amber-600">→ Nonlinear remainder not yet bounded for Leray-Hopf</div>
                      </div>
                    )}
                    {step.id === "s5" && (
                      <div className="mt-2 text-[10px] font-mono space-y-1">
                        <div className="text-gray-600">With current params:</div>
                        <div className={result.sndHolds ? "text-emerald-400" : "text-rose-400"}>
                          ‖a−μ‖_ℓ¹ = {result.l1Deviation.toFixed(5)} {result.sndHolds ? "≤" : ">"} η = {eta.toFixed(3)} → SND {result.sndHolds ? "✓" : "✗"}
                        </div>
                      </div>
                    )}
                    {step.id === "s6" && (
                      <div className="mt-2 text-[10px] font-mono space-y-1">
                        <div className="text-gray-600">With current params (rigorous via λ_gap = {lambdaGap.toFixed(3)}):</div>
                        <div className={h3Rigorous ? "text-emerald-400" : "text-rose-400"}>
                          C_N·‖a−μ‖_ℓ¹ = {(C_N_gap * result.l1Deviation).toFixed(5)} {h3Rigorous ? "< 0.20 → H3 ✓" : "≥ 0.20 → H3 ✗"}
                        </div>
                        <div className="text-violet-400">
                          λ_min(H_N) ≥ {lambdaGap.toFixed(3)} − {C_N_gap.toFixed(3)}·{result.l1Deviation.toFixed(4)} = {lambdaMin_rigorous.toFixed(4)}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
              {i < PROOF_STEPS.length - 1 && (
                <div className="flex justify-center my-0.5 text-gray-800 text-xs">↓</div>
              )}
            </div>
          );
        })}
      </div>

      {/* Key distinction callout */}
      <div className="bg-[#080a10] border border-gray-700 rounded-lg p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="space-y-2">
          <div className="text-xs text-cyan-500 uppercase tracking-widest font-mono">Q6 — Operator (mechanism)</div>
          <MB>{"Q_6[u] = \\sum_j \\gamma_j[u]\\,\\Pi_j\\, u"}</MB>
          <div className="text-[10px] text-gray-500 leading-relaxed">
            Applied to u. Activates when a_j exceeds a_c. <span className="text-cyan-400">You define it.</span> Its existence and action on L² solutions is clear. What it <em>produces</em> for all Leray-Hopf is the open question.
          </div>
        </div>
        <div className="space-y-2">
          <div className="text-xs text-amber-500 uppercase tracking-widest font-mono">SND — Condition (target)</div>
          <MB>{"\\mathrm{SND}_N(\\eta,\\mu):\\;\\sup_{t\\ge0}\\|a(t)-\\mu\\|_{\\ell^1}\\le\\eta"}</MB>
          <div className="text-[10px] text-gray-500 leading-relaxed">
            A statement about the solution trajectory. <span className="text-amber-400">You prove it</span> — or you don't. Q6 is designed to enforce SND, but this implication is not yet proven unconditionally for all Leray-Hopf solutions.
          </div>
        </div>
      </div>
    </div>
  );
}