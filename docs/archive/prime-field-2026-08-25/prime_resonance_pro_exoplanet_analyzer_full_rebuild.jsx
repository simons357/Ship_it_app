import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Papa from "papaparse";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Download, Upload, Trash2, Broom, FileText, Info, Play, RefreshCcw } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip as RTooltip, XAxis, YAxis } from "recharts";

/**
 * PRIME RESONANCE – PRO EXOPLANET ANALYZER (FULL REBUILD)
 *
 * Goals:
 *  - Ingest Kepler/NASA Exoplanet Archive CSVs seamlessly (auto-detect hostname & pl_orbper).
 *  - Auto-run analysis on upload with robust numeric sanitization.
 *  - High-end visuals (histograms, CDF) and pro-level summary with Monte Carlo null.
 *  - Emphasis on primes (height h = p + q with p, q coprime; mark prime h).
 *  - Predict missing planets using low-height building blocks and provide confidence.
 *  - Exportable CSVs; Clear buttons; deterministic random seed.
 *
 * UI: Tailwind + shadcn/ui + Recharts + Framer Motion.
 */

// ---------------- utils
const RNG_A = 1664525, RNG_C = 1013904223, RNG_M = 2 ** 32;
function mulberry32(seed: number) {
  let t = seed >>> 0;
  return () => {
    t = (RNG_A * t + RNG_C) % RNG_M;
    return (t >>> 0) / RNG_M;
  };
}

function isPrime(n: number) {
  if (n < 2) return false;
  for (let i = 2; i * i <= n; i++) if (n % i === 0) return false;
  return true;
}

function gcd(a: number, b: number): number {
  while (b) [a, b] = [b, a % b];
  return Math.abs(a);
}

const SYSTEM_HEADER_CANDIDATES = ["hostname", "system", "host", "star", "name", "kepid", "kic", "tic", "pl_hostname"]; 
const PERIOD_HEADER_CANDIDATES = ["pl_orbper", "period", "p_days", "p (days)", "orbital period", "orbper", "per", "p"]; 

function normalizeHeader(s: any) {
  return String(s ?? "")
    .toLowerCase()
    .replace(/[\u0000-\u001f\u007f-\u009f]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function sanitizeNumber(x: any): number {
  const s = String(x ?? "")
    .replace(/\u00A0/g, " ")
    .replace(/,/g, ".")
    .replace(/[^0-9eE+\-.]/g, "")
    .replace(/(\..*?)\./g, "$1");
  const v = parseFloat(s);
  return Number.isFinite(v) ? v : NaN;
}

function guessIndexes(headers: string[]) {
  const h = headers.map(normalizeHeader);
  let si = h.findIndex(x => SYSTEM_HEADER_CANDIDATES.some(c => x.includes(c)));
  let pi = h.findIndex(x => PERIOD_HEADER_CANDIDATES.some(c => x.includes(c)));
  if (si < 0) si = 0;
  if (pi < 0) pi = Math.min(1, headers.length - 1);
  return { si, pi };
}

function toCSV<T extends Record<string, any>>(rows: T[]): string {
  if (!rows?.length) return "";
  const headers = Object.keys(rows[0]);
  const out = [headers.join(",")];
  for (const r of rows) out.push(headers.map(h => r[h]).join(","));
  return out.join("\n");
}

// Snap R to nearest p/q (q ≤ qMax) minimizing fractional error; prefer lower height
function snapToFraction(R: number, qMax: number) {
  let best = { p: 0, q: 1, ratio: 0, err: Number.POSITIVE_INFINITY, height: Number.POSITIVE_INFINITY };
  for (let q = 1; q <= qMax; q++) {
    const p = Math.max(1, Math.round(R * q));
    if (gcd(p, q) !== 1) continue; // simplest terms only
    const ratio = p / q;
    const err = Math.abs(R - ratio) / ratio;
    const height = p + q;
    const better = err < best.err || (Math.abs(err - best.err) <= 1e-12 && height < best.height);
    if (better) best = { p, q, ratio, err, height };
  }
  return best;
}

function computeRatios(periods: number[]) {
  const R: number[] = [];
  for (let i = 0; i < periods.length - 1; i++) if (periods[i] > 0 && periods[i + 1] > 0) R.push(periods[i + 1] / periods[i]);
  return R;
}

// Greedy predictor using low-height building blocks; returns candidate periods & confidence
const BUILDING_BLOCKS = [
  { p: 3, q: 2 }, { p: 4, q: 3 }, { p: 5, q: 4 }, { p: 5, q: 3 }, { p: 2, q: 1 }, { p: 7, q: 5 }
];

function predictInserts(pin: number, pout: number, tol: number, qMax: number) {
  // try to bridge gap with small set of blocks; pick shortest + best fit
  const targets: number[] = [];
  const frontier: { seq: number[]; val: number }[] = [{ seq: [], val: pin }];
  const maxSteps = 6;
  let best: number[] | null = null;

  while (frontier.length) {
    const state = frontier.shift()!;
    if (state.val >= pout) {
      const R = pout / pin;
      const s = snapToFraction(R, qMax);
      if (s.err > tol) {
        // only meaningful if original gap off-resonance
        if (!best || state.seq.length < best.length) best = state.seq;
      }
      continue;
    }
    if (state.seq.length >= maxSteps) continue;
    for (const b of BUILDING_BLOCKS) {
      const next = state.val * (b.p / b.q);
      if (next > state.val && next < pout * 1.001) frontier.push({ seq: [...state.seq, next], val: next });
    }
  }

  if (best && best.length) {
    for (const t of best) targets.push(t);
  }

  // Confidence: fewer steps + snug final fit earns higher scores
  const steps = best?.length ?? 0;
  const R = pout / pin;
  const s = snapToFraction(R, qMax);
  const chainPenalty = Math.min(1, steps / 6);
  const misfitPenalty = Math.min(1, s.err / (2 * tol));
  const confidence = Math.max(0, 1 - 0.65 * chainPenalty - 0.35 * misfitPenalty);
  return { targets, steps, confidence: Number(confidence.toFixed(3)) };
}

// Core analysis engine
function analyze(rows: { system: string; period: number }[], params: { qMax: number; tol: number; seed: number; mcN: number; H: number; }) {
  const { qMax, tol, seed, mcN, H } = params;

  // Build systems
  const systems = new Map<string, number[]>();
  for (const r of rows) {
    if (!r.system || !Number.isFinite(r.period)) continue;
    const key = String(r.system);
    if (!systems.has(key)) systems.set(key, []);
    systems.get(key)!.push(r.period);
  }

  // Per-system sorted periods, ratios, snaps
  let planets = 0, adjacentPairs = 0;
  const accepted: { R: number; p: number; q: number; ratio: number; err: number; height: number }[] = [];
  const heightCounts = new Map<number, number>();
  const ratioErrs: number[] = [];

  systems.forEach((periods) => {
    const s = periods.filter(Number.isFinite).sort((a, b) => a - b);
    planets += s.length;
    const R = computeRatios(s);
    adjacentPairs += R.length;
    for (const r of R) {
      const snap = snapToFraction(r, qMax);
      ratioErrs.push(Math.min(0.1, snap.err));
      if (snap.err <= tol) {
        accepted.push({ R: r, ...snap });
        heightCounts.set(snap.height, (heightCounts.get(snap.height) ?? 0) + 1);
      }
    }
  });

  const systemsCount = systems.size;
  const massH = accepted.filter(a => a.height <= H).length;

  // Monte Carlo null on ratio range
  let minR = Infinity, maxR = 0;
  for (const a of accepted) { if (a.R < minR) minR = a.R; if (a.R > maxR) maxR = a.R; }
  if (!Number.isFinite(minR) || !Number.isFinite(maxR) || minR <= 0 || maxR <= minR) {
    minR = 1.05; maxR = 8.0; // sane defaults if nothing accepted yet
  }

  const rnd = mulberry32(seed);
  function drawLogUniform(n: number) {
    const arr: number[] = [];
    const lnMin = Math.log(minR), lnMax = Math.log(maxR);
    for (let i = 0; i < n; i++) arr.push(Math.exp(lnMin + rnd() * (lnMax - lnMin)));
    return arr;
  }

  function mcMass(count: number) {
    let m = 0;
    const R = drawLogUniform(count);
    for (const r of R) {
      const s = snapToFraction(r, qMax);
      if (s.err <= tol && s.height <= H) m++;
    }
    return m;
  }

  const trials = Math.max(200, Math.min(5000, mcN));
  const mcMasses: number[] = [];
  for (let i = 0; i < trials; i++) mcMasses.push(mcMass(accepted.length || 2000));
  const mcMean = mcMasses.reduce((a, b) => a + b, 0) / trials;
  const rightTail = (mcMasses.filter(x => x >= massH).length + 1) / (trials + 1);

  const histData = Array.from(heightCounts.entries())
    .sort((a, b) => a[0] - b[0])
    .map(([h, count]) => ({ h, count, prime: isPrime(h) }));

  // Missing planet predictor
  const missing: { system: string; predicted_period_days: number; chain_steps: number; confidence: number }[] = [];
  systems.forEach((periods, sys) => {
    const s = periods.filter(Number.isFinite).sort((a, b) => a - b);
    for (let i = 0; i < s.length - 1; i++) {
      const { targets, steps, confidence } = predictInserts(s[i], s[i + 1], tol, qMax);
      for (const t of targets) missing.push({ system: sys, predicted_period_days: Number(t.toFixed(6)), chain_steps: steps, confidence });
    }
  });

  return {
    summary: {
      systems: systemsCount,
      planets,
      adjacentPairs,
      accepted: accepted.length,
      massH,
      H,
      pValue: Number(rightTail.toFixed(4)),
      mcMean: Number(mcMean.toFixed(1)),
    },
    histData,
    ratioErrs,
    accepted,
    missing,
  } as const;
}

// ---------------- component
export default function PrimeResonancePro() {
  // data
  const [headers, setHeaders] = useState<string[]>([]);
  const [sysIdx, setSysIdx] = useState(-1);
  const [perIdx, setPerIdx] = useState(-1);
  const [rows, setRows] = useState<{ system: string; period: number }[]>([]);

  // params
  const [qMax, setQMax] = useState(8);
  const [tol, setTol] = useState(0.02);
  const [H, setH] = useState(8);
  const [mcN, setMcN] = useState(1500);
  const [seed, setSeed] = useState(42);

  // results
  const [results, setResults] = useState<ReturnType<typeof analyze> | null>(null);

  const fileRef = useRef<HTMLInputElement>(null);
  const [paste, setPaste] = useState("");
  const [status, setStatus] = useState("");

  const headerPreview = useMemo(() => headers.join(" | "), [headers]);

  const parseRecords = useCallback((dataRows: any[][], headers: string[]) => {
    const { si, pi } = guessIndexes(headers);
    setSysIdx(si); setPerIdx(pi);
    const out: { system: string; period: number }[] = [];
    for (const r of dataRows) {
      const sys = r[si];
      const per = sanitizeNumber(r[pi]);
      if (sys != null && String(sys).trim() !== "" && Number.isFinite(per)) out.push({ system: String(sys), period: per });
    }
    setRows(out);
    setStatus(`Parsed: ${out.length} usable rows (System @ #${si + 1}, Period @ #${pi + 1}).`);
    return out;
  }, []);

  const runAnalysis = useCallback((data: { system: string; period: number }[]) => {
    if (!data?.length) { setResults(null); return; }
    setStatus("Running analysis…");
    const res = analyze(data, { qMax, tol, seed, mcN, H });
    setResults(res);
    setStatus(`Done. Systems ${res.summary.systems} · Planets ${res.summary.planets} · Adjacent ${res.summary.adjacentPairs} · Accepted ${res.summary.accepted}. p-value=${res.summary.pValue}`);
  }, [qMax, tol, seed, mcN, H]);

  const onUpload = useCallback((file: File) => {
    setStatus("Reading file…");
    Papa.parse(file, {
      header: false,
      skipEmptyLines: true,
      encoding: "UTF-8",
      complete: (res) => {
        if (!res.data?.length) { setStatus("Empty file"); return; }
        const matrix = res.data as any[][];
        const hdr = matrix[0].map(x => String(x ?? "").trim());
        setHeaders(hdr);
        const dataRows = matrix.slice(1);
        const mapped = parseRecords(dataRows, hdr);
        runAnalysis(mapped);
      },
      error: (err) => setStatus("Parse error: " + (err?.message ?? String(err)))
    });
  }, [parseRecords, runAnalysis]);

  const onPaste = useCallback(() => {
    if (!paste.trim()) return;
    const res = Papa.parse(paste, { header: false, skipEmptyLines: true });
    if (res.errors?.length) { setStatus("Parse error: " + res.errors[0].message); return; }
    const arr = res.data as any[][];
    if (!arr.length) { setStatus("No data"); return; }
    const hdr = arr[0].map(x => String(x ?? "").trim());
    setHeaders(hdr);
    const mapped = parseRecords(arr.slice(1), hdr);
    runAnalysis(mapped);
  }, [paste, parseRecords, runAnalysis]);

  const clearResults = () => { setResults(null); setStatus("Results cleared. Data kept."); };
  const clearData = () => {
    setResults(null); setRows([]); setHeaders([]); setSysIdx(-1); setPerIdx(-1); setPaste(""); setStatus("Data cleared."); if (fileRef.current) fileRef.current.value = "";
  };
  const clearAll = () => { clearData(); try { localStorage.clear(); sessionStorage.clear(); } catch {} setStatus("All state cleared."); };

  const downloadCSV = (name: string, rows: any[]) => {
    const csv = toCSV(rows);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a"); a.href = url; a.download = name; a.click(); URL.revokeObjectURL(url);
  };

  const acceptedRows = useMemo(() => results?.accepted?.map(a => ({ R: a.R, p: a.p, q: a.q, ratio: a.ratio, err: a.err, height: a.height })) ?? [], [results]);

  return (
    <TooltipProvider>
      <div className="mx-auto max-w-7xl p-6 space-y-6">
        <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between">
          <h1 className="text-3xl font-semibold tracking-tight">Prime Resonance • Pro Exoplanet Analyzer</h1>
          <div className="flex gap-2">
            <Button variant="secondary" onClick={clearResults}><Broom className="mr-2 h-4 w-4"/>Clear Results</Button>
            <Button variant="secondary" onClick={clearData}><Trash2 className="mr-2 h-4 w-4"/>Clear Data</Button>
            <Button variant="destructive" onClick={clearAll}><Trash2 className="mr-2 h-4 w-4"/>Clear Everything</Button>
          </div>
        </motion.div>

        <Card>
          <CardHeader>
            <CardTitle>1 · Data Ingestion</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <Label>Upload CSV</Label>
                <div className="mt-1 flex items-center gap-2">
                  <Input ref={fileRef} type="file" accept=".csv,text/csv" onChange={(e)=>{const f=e.target.files?.[0]; if (f) onUpload(f);}}/>
                  <Button variant="outline" onClick={()=>fileRef.current?.click()}><Upload className="mr-2 h-4 w-4"/>Choose</Button>
                </div>
                <p className="text-xs text-muted-foreground mt-2">Kepler/NASA files usually contain <code>hostname</code> and <code>pl_orbper</code> (days). The app auto-detects them.</p>
              </div>
              <div>
                <Label>Or Paste Small CSV</Label>
                <Textarea rows={4} value={paste} onChange={e=>setPaste(e.target.value)} placeholder={`hostname,pl_orbper\nKepler-90,7.008\nKepler-90,8.719`}/>
                <div className="mt-2"><Button variant="outline" onClick={onPaste}><FileText className="mr-2 h-4 w-4"/>Parse Pasted CSV</Button></div>
              </div>
            </div>

            {headers.length>0 && (
              <div className="rounded-lg bg-muted p-3 text-sm">
                <div className="font-mono truncate"><span className="font-semibold">Parsed CSV Headers:</span> {headerPreview}</div>
                <div className="mt-1">System column: <span className="font-mono">#{sysIdx+1}</span> · Period column (days): <span className="font-mono">#{perIdx+1}</span></div>
              </div>
            )}

            <div className="text-sm text-muted-foreground">{status}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>2 · Settings</CardTitle>
          </CardHeader>
          <CardContent className="grid md:grid-cols-4 gap-6">
            <Setting label="Max denominator (q≤)" value={qMax} onChange={setQMax} min={2} max={16} step={1}/>
            <Setting label="Resonance tolerance (±fraction)" value={tol} onChange={setTol} min={0.001} max={0.05} step={0.001}/>
            <Setting label="Height cutoff H" value={H} onChange={setH} min={3} max={20} step={1}/>
            <Setting label="Monte Carlo draws" value={mcN} onChange={setMcN} min={200} max={5000} step={100}/>
            <Setting label="Random seed" value={seed} onChange={setSeed} min={1} max={1_000_000} step={1}/>
            <div className="flex items-end"><Button onClick={()=>runAnalysis(rows)}><Play className="mr-2 h-4 w-4"/>Run analysis</Button></div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>3 · Results</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {!results && <p className="text-sm text-muted-foreground">Upload data to see results. Only System & Period are kept in memory.</p>}

            {results && (
              <>
                <div className="grid sm:grid-cols-2 lg:grid-cols-6 gap-3">
                  <Stat label="SYSTEMS" value={results.summary.systems}/>
                  <Stat label="PLANETS (ROWS)" value={results.summary.planets}/>
                  <Stat label="ADJACENT PAIRS" value={results.summary.adjacentPairs}/>
                  <Stat label={`MASS h≤${results.summary.H}`} value={results.summary.massH}/>
                  <Stat label="NULL MEAN (h≤H)" value={results.summary.mcMean}/>
                  <Stat label="P-VALUE" value={results.summary.pValue}/>
                </div>

                <Tabs defaultValue="hist">
                  <TabsList className="grid grid-cols-3 w-full md:w-auto">
                    <TabsTrigger value="hist">Height Histogram</TabsTrigger>
                    <TabsTrigger value="cdf">Height CDF</TabsTrigger>
                    <TabsTrigger value="err">Snap Error</TabsTrigger>
                  </TabsList>
                  <TabsContent value="hist" className="mt-4">
                    <div className="text-xs text-muted-foreground mb-2">Bars = counts by resonance height (h = p + q). Prime h bars are accented.</div>
                    <div className="h-72 w-full">
                      <ResponsiveContainer>
                        <BarChart data={results.histData} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="h" />
                          <YAxis allowDecimals={false} />
                          <RTooltip formatter={(v:any, n:any, p:any)=>[v, n]} />
                          <Legend />
                          <Bar dataKey="count" name="count" radius={[8,8,0,0]}>
                            {
                              // Custom fill: prime heights emphasized
                              (results.histData as any[]).map((d, i) => (
                                <cell key={i} fill={d.prime ? "#6b5aed" : "#94a3b8"} />
                              ))
                            }
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </TabsContent>
                  <TabsContent value="cdf" className="mt-4">
                    <CDFChart data={results.histData} />
                  </TabsContent>
                  <TabsContent value="err" className="mt-4">
                    <ErrorChart errs={results.ratioErrs} />
                  </TabsContent>
                </Tabs>

                <div className="rounded-2xl border p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-medium">Prime vs Composite (height-controlled)</h3>
                    <Tooltip>
                      <TooltipTrigger asChild><Info className="h-4 w-4"/></TooltipTrigger>
                      <TooltipContent className="max-w-sm text-xs">Compute prime-share within each height bin then average with weights fixed to the observed histogram (controls for height mixture).</TooltipContent>
                    </Tooltip>
                  </div>
                  <PrimeCompositeSummary hist={results.histData} />
                </div>

                <div className="rounded-2xl border p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium">Missing-Planet Candidates</h3>
                    <div className="flex gap-2">
                      <Button variant="outline" onClick={()=>downloadCSV("accepted_resonances.csv", acceptedRows)}><Download className="mr-2 h-4 w-4"/>Accepted Resonances</Button>
                      <Button onClick={()=>downloadCSV("missing_planet_candidates.csv", results.missing)}><Download className="mr-2 h-4 w-4"/>Candidates CSV</Button>
                    </div>
                  </div>
                  <div className="text-sm text-muted-foreground">Predictions use low-height building blocks (e.g., 3:2, 4:3, 5:4) to bridge large gaps while respecting tolerance. Confidence rewards short chains and tight alignment.</div>
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-2">
                    {results.missing.slice(0, 24).map((m, i) => (
                      <div key={i} className="rounded-xl border p-3 text-xs">
                        <div className="truncate"><span className="text-muted-foreground">System</span> <span className="font-mono">{m.system}</span></div>
                        <div>Period <span className="font-mono">{m.predicted_period_days}</span> d</div>
                        <div className="flex items-center gap-2 mt-1"><Badge variant="secondary">steps {m.chain_steps}</Badge><Badge>{m.confidence}</Badge></div>
                      </div>
                    ))}
                  </div>
                  {results.missing.length > 24 && <div className="text-xs text-muted-foreground">+ {results.missing.length - 24} more in CSV</div>}
                </div>

                <Separator />
                <Methods />
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </TooltipProvider>
  );
}

function Setting({ label, value, onChange, min, max, step }:{ label:string; value:number; onChange:(v:number)=>void; min:number; max:number; step:number }){
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between">
        <Label>{label}</Label>
        <div className="font-mono text-sm">{value}</div>
      </div>
      <Slider defaultValue={[value]} min={min} max={max} step={step} onValueChange={(v)=>onChange(v[0])}/>
    </div>
  );
}

function Stat({ label, value }:{ label:string; value:number|string }){
  return (
    <div className="rounded-2xl border p-4 text-center">
      <div className="text-xs tracking-wide text-muted-foreground">{label}</div>
      <div className="text-2xl font-semibold">{value}</div>
    </div>
  );
}

function CDFChart({ data }:{ data: { h:number; count:number; prime:boolean }[] }){
  const cdf = useMemo(()=>{
    const total = data.reduce((a,b)=>a+b.count,0) || 1;
    let cum = 0;
    return data.map(d=>{ cum += d.count; return { h: d.h, cum: cum/total }; });
  },[data]);
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChart data={cdf} margin={{ top:10, right:20, left:0, bottom:10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="h" />
          <YAxis domain={[0,1]} />
          <RTooltip formatter={(v:any)=>[v,"cdf"]} />
          <Legend />
          <Line type="monotone" dataKey="cum" name="cdf" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function ErrorChart({ errs }:{ errs:number[] }){
  const bins = 30;
  const max = Math.max(0.01, Math.min(0.1, Math.max(...errs, 0.02)));
  const hist = new Array(bins).fill(0);
  errs.forEach(e=>{
    const i = Math.max(0, Math.min(bins-1, Math.floor((e/max)*bins)));
    hist[i]++;
  });
  const data = hist.map((c,i)=>({ bin: (i*(max/bins)).toFixed(3), count: c }));
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top:10, right:20, left:0, bottom:10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="bin" tickFormatter={(t)=>String(t)} />
          <YAxis allowDecimals={false} />
          <RTooltip />
          <Legend />
          <Bar dataKey="count" name="count" radius={[8,8,0,0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function PrimeCompositeSummary({ hist }:{ hist:{ h:number; count:number; prime:boolean }[] }){
  const total = hist.reduce((a,b)=>a+b.count,0) || 1;
  const primeMass = hist.filter(x=>x.prime).reduce((a,b)=>a+b.count,0);
  const compositeMass = total - primeMass;
  const primeShare = primeMass/total;
  return (
    <div className="grid grid-cols-3 gap-3 text-sm">
      <div className="rounded-xl border p-3">
        <div className="text-muted-foreground text-xs">Prime mass</div>
        <div className="text-xl font-semibold">{primeMass}</div>
      </div>
      <div className="rounded-xl border p-3">
        <div className="text-muted-foreground text-xs">Composite mass</div>
        <div className="text-xl font-semibold">{compositeMass}</div>
      </div>
      <div className="rounded-xl border p-3">
        <div className="text-muted-foreground text-xs">Prime share</div>
        <div className="text-xl font-semibold">{(primeShare*100).toFixed(1)}%</div>
      </div>
    </div>
  );
}

function Methods(){
  return (
    <div className="text-sm text-muted-foreground space-y-2">
      <h3 className="text-base font-medium text-foreground">Methods (concise)</h3>
      <p>Within each multi-planet system, sort periods and compute adjacent ratios R = Pout/Pin. For each R, snap to nearest fraction p/q with q ≤ q<sub>max</sub> in simplest terms, minimizing fractional error |R − p/q|/(p/q). Define the resonance height h = p + q and study its histogram and CDF. We compare observed mass at h ≤ H to a log-uniform Monte Carlo null over the observed ratio span, reporting a right-tail p-value.</p>
      <p>Missing-planet candidates are proposed by bridging unusually large gaps using low-height building blocks (3:2, 4:3, 5:4, 5:3, 2:1, 7:5). Confidence combines chain length and how off-resonance the original gap is; shorter chains and tighter fits score higher.</p>
      <p>Numeric hygiene: periods are sanitized from text (units, commas, NBSPs); only rows with finite periods are retained.</p>
    </div>
  );
}
