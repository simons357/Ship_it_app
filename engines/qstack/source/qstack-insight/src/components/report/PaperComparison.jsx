import React from "react";

const rows = [
  { label: "File", ns: "Simons_NS_QStack_arXiv.tex", sfe: "To be written" },
  { label: "Core result", ns: "Global regularity on T³", sfe: "NS isomorphism on irrotational sector" },
  { label: "Key new result", ns: "Theorem B (Φ‑renorm) + Theorem F (Shell‑Spread Poincaré) + Theorem H (SND‑C)", sfe: "Madelung decomposition → NS form" },
  { label: "Vorticity", ns: "Full arbitrary vorticity", sfe: "Zero vorticity (u_C = ∇Φ, curl = 0)" },
  { label: "Target journal", ns: "Annals of Math, Inventiones, JAMS", sfe: "Foundations of Physics, Entropy" },
  { label: "Status", ns: "Complete, ready to submit", sfe: "Not yet written as standalone" },
  { label: "Connection to Clay", ns: "Direct", sfe: "None — sequestered" },
];

export default function PaperComparison() {
  return (
    <div className="space-y-8">
      <div className="grid md:grid-cols-2 gap-px bg-border border border-border rounded-lg overflow-hidden">
        <div className="bg-card p-6 md:p-8">
          <div className="font-mono text-xs text-accent tracking-widest mb-2">PAPER I</div>
          <h3 className="font-serif text-2xl md:text-3xl leading-tight">NS / Clay Paper</h3>
        </div>
        <div className="bg-card p-6 md:p-8">
          <div className="font-mono text-xs text-muted-foreground tracking-widest mb-2">PAPER II</div>
          <h3 className="font-serif text-2xl md:text-3xl leading-tight">SFE / Geometry of Flow</h3>
        </div>

        {rows.map((row) => (
          <React.Fragment key={row.label}>
            <div className="bg-card px-6 md:px-8 py-4 border-t border-border">
              <div className="text-xs uppercase tracking-widest text-muted-foreground mb-1">{row.label}</div>
              <div className="text-sm leading-relaxed">{row.ns}</div>
            </div>
            <div className="bg-card px-6 md:px-8 py-4 border-t border-border">
              <div className="text-xs uppercase tracking-widest text-muted-foreground mb-1 md:opacity-0">{row.label}</div>
              <div className="text-sm leading-relaxed text-muted-foreground">{row.sfe}</div>
            </div>
          </React.Fragment>
        ))}
      </div>

      <div className="flex items-start gap-3 p-5 bg-muted/60 rounded-lg border border-border">
        <div className="font-serif text-2xl text-accent leading-none mt-1">§</div>
        <p className="text-sm leading-relaxed italic">
          <span className="font-medium not-italic">Rule.</span> These papers do not reference each other. The NS paper contains no SFE. The SFE paper makes no Clay claims. This separation makes both papers stronger.
        </p>
      </div>
    </div>
  );
}
