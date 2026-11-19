import React from "react";

export default function MeaningBlock() {
  return (
    <div className="grid md:grid-cols-2 gap-12 md:gap-16">
      <div>
        <div className="text-xs uppercase tracking-widest text-accent mb-3">In one sentence</div>
        <p className="font-serif text-2xl md:text-3xl leading-snug text-balance">
          Every fluid starting from any smooth initial condition on <span className="italic">T³</span> stays smooth forever. No blowup. No singularity.
        </p>
      </div>
      <div className="space-y-8">
        <div>
          <div className="text-xs uppercase tracking-widest text-muted-foreground mb-3">In clinical language</div>
          <p className="text-base leading-relaxed text-pretty">
            The [SND] condition is like a BIS number. If the dominant LP‑shell holds a positive fraction of enstrophy (BIS above threshold), the patient is stable. We proved that BIS cannot drop to zero — the system's own dissipation mechanism prevents it. <span className="italic">Theorem F</span> is the physiological explanation: spreading energy across too many frequencies costs so much metabolic energy that it's self‑defeating.
          </p>
        </div>
        <div className="border-l-2 border-accent pl-5">
          <div className="text-xs uppercase tracking-widest text-muted-foreground mb-2">What the Clay Prize actually asks</div>
          <p className="text-base leading-relaxed text-pretty">
            Does this work on <span className="font-serif italic">ℝ³</span>, not just <span className="font-serif italic">T³</span>? That is the one remaining question. The difference matters because on ℝ³, energy can escape to spatial infinity — "bubble runaway." Closing it requires a Bahouri–Gérard profile decomposition. <span className="italic">That is not done yet and we are not claiming it.</span>
          </p>
        </div>
      </div>
    </div>
  );
}
