import React from "react";
import { motion } from "framer-motion";

export default function ReportHero() {
  return (
    <header className="relative border-b border-border">
      <div className="max-w-5xl mx-auto px-6 md:px-12 pt-16 pb-20 md:pt-24 md:pb-28">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          className="space-y-10"
        >
          <div className="flex items-center gap-3 text-xs uppercase tracking-[0.2em] text-muted-foreground">
            <span className="h-px w-8 bg-accent" />
            <span>Project Report</span>
            <span className="text-border">·</span>
            <span>April 18, 2026</span>
          </div>

          <div className="space-y-6">
            <h1 className="font-serif text-5xl md:text-7xl leading-[0.95] tracking-tight text-balance">
              Spectral Non‑Dispersal &amp; the Reduction of the{" "}
              <em className="italic text-accent font-light">Clay Navier–Stokes</em> Problem
            </h1>
            <p className="font-serif text-xl md:text-2xl text-muted-foreground max-w-3xl leading-snug text-pretty">
              A complete proof program on <span className="italic">T³</span>, reducing global regularity to a single flux inequality.
            </p>
          </div>

          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 pt-6">
            <div className="space-y-1">
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Prepared by</div>
              <div className="font-serif text-lg">Jonathan Robert Simons <span className="text-muted-foreground font-sans text-sm">· CRNA, MMed</span></div>
              <div className="text-sm text-muted-foreground">Prime Field Technologies LLC · QStack NS Program</div>
            </div>
            <div className="flex items-center gap-3">
              <div className="px-3 py-1.5 rounded-full bg-accent/10 border border-accent/30 text-accent text-xs font-medium uppercase tracking-wider">
                Ready for arXiv
              </div>
              <div className="px-3 py-1.5 rounded-full bg-primary text-primary-foreground text-xs font-medium uppercase tracking-wider">
                8 / 8 Theorems Proved
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </header>
  );
}
