import React from "react";
import { motion } from "framer-motion";
import { Check, Sparkles } from "lucide-react";

const theorems = [
  { id: "A", title: "Q1 Global Regularity", desc: "The augmented system is globally C∞ for every ε > 0.", isNew: false },
  { id: "B", title: "Φ‑Renormalization", desc: "The 1/r⁴ axis singularity cancels exactly and algebraically — no Hardy inequality needed.", isNew: true },
  { id: "C", title: "Uniform Convergence", desc: "u^ε → u at rate ε^{4/(β+2)}, uniformly in time, without Grönwall amplification.", isNew: false },
  { id: "D", title: "Clay ⟺ [SND]", desc: "The Clay Prize is exactly equivalent to [SND]. Two‑way proof.", isNew: false },
  { id: "E", title: "[SND] on T³ finite time", desc: "For smooth solutions on any finite interval of T³, J/X ≥ c* > 0.", isNew: false },
  { id: "F", title: "Shell‑Spread Poincaré", desc: "Spreading enstrophy across N shells forces dissipation to grow as 4^N.", isNew: true },
  { id: "G", title: "(SND‑C) ⟹ [SND]", desc: "If the flux estimate holds, [SND] follows.", isNew: false },
  { id: "H", title: "(SND‑C) itself", desc: "|Π_{j*}| ≤ C*(ν·4^{j*}·X_{j*} + X^½·𝒟^½).", isNew: false, today: true },
];

export default function TheoremTable() {
  return (
    <div className="space-y-px bg-border rounded-lg overflow-hidden border border-border">
      {theorems.map((t, i) => (
        <motion.div
          key={t.id}
          initial={{ opacity: 0, x: -10 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-50px" }}
          transition={{ duration: 0.4, delay: i * 0.04 }}
          className="bg-card grid grid-cols-[auto_1fr_auto] md:grid-cols-[auto_1fr_1.5fr_auto] gap-4 md:gap-8 px-5 md:px-8 py-5 md:py-6 hover:bg-muted/50 transition-colors"
        >
          <div className="font-serif text-3xl md:text-4xl text-accent leading-none w-10">
            {t.id}
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="font-serif text-lg md:text-xl leading-tight">{t.title}</h3>
              {t.isNew && (
                <span className="inline-flex items-center gap-1 text-[10px] uppercase tracking-wider bg-accent/10 text-accent px-2 py-0.5 rounded-full border border-accent/20">
                  <Sparkles className="w-2.5 h-2.5" /> New
                </span>
              )}
              {t.today && (
                <span className="text-[10px] uppercase tracking-wider bg-primary text-primary-foreground px-2 py-0.5 rounded-full">
                  Closed today
                </span>
              )}
            </div>
            <p className="md:hidden text-sm text-muted-foreground mt-1.5 leading-relaxed">
              {t.desc}
            </p>
          </div>
          <p className="hidden md:block text-sm text-muted-foreground leading-relaxed self-center">
            {t.desc}
          </p>
          <div className="flex items-center self-start md:self-center">
            <div className="flex items-center gap-1.5 text-xs font-medium text-accent">
              <div className="w-5 h-5 rounded-full bg-accent flex items-center justify-center">
                <Check className="w-3 h-3 text-accent-foreground" strokeWidth={3} />
              </div>
              <span className="hidden md:inline uppercase tracking-wider">Proved</span>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
