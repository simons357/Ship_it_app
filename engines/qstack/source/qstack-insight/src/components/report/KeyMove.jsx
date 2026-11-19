import React from "react";
import { ArrowRight } from "lucide-react";

export default function KeyMove() {
  return (
    <div className="mt-16 p-8 md:p-12 bg-primary text-primary-foreground rounded-lg relative overflow-hidden">
      <div className="absolute top-0 right-0 w-96 h-96 bg-accent/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3 pointer-events-none" />
      <div className="relative">
        <div className="text-xs uppercase tracking-[0.2em] text-accent mb-4">The single key move</div>
        <h3 className="font-serif text-2xl md:text-3xl leading-snug mb-6 max-w-3xl text-balance">
          Theorems F and H are paired — one creates the conditions that make the other close.
        </h3>
        <div className="grid md:grid-cols-[1fr_auto_1fr] gap-6 items-center text-sm md:text-base leading-relaxed opacity-90">
          <div>
            <div className="font-mono text-xs text-accent mb-2">THEOREM F</div>
            Spreading enstrophy across N LP‑shells forces dissipation <span className="font-serif italic">𝒟</span> to grow as <span className="font-mono">4^N</span>. In the dangerous spread regime, <span className="font-mono">𝒟 → ∞</span> super‑exponentially.
          </div>
          <ArrowRight className="w-6 h-6 text-accent hidden md:block mx-auto" />
          <div>
            <div className="font-mono text-xs text-accent mb-2">THEOREM H</div>
            The dangerous T‑term contains <span className="font-mono">𝒟^(−1/4)</span>. When <span className="font-mono">𝒟 → ∞</span>, the term vanishes. <span className="italic">No finite‑time singularity on T³.</span>
          </div>
        </div>
      </div>
    </div>
  );
}
