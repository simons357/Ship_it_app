import React from "react";
import { motion } from "framer-motion";
import { Circle, AlertTriangle, FileText, Upload, FlaskConical, Telescope } from "lucide-react";

const items = [
  {
    icon: AlertTriangle,
    label: "High difficulty",
    title: "The ℝ³ extension",
    what: "Take everything above and prove it on ℝ³ instead of T³.",
    why: "On T³, compactness arguments work because the domain is finite. On ℝ³, energy can drift to infinity and compactness fails. The tool needed is a Bahouri–Gérard profile decomposition for the NS flow map.",
    status: "Open · genuine remaining gap between our result and the Clay Prize.",
  },
  {
    icon: FileText,
    label: "30 min",
    title: "Detailed write‑up of Theorem H proof",
    what: "The proof of (SND‑C) exists in SNDC_proof.tex as a standalone file.",
    why: "It needs to be integrated into the main paper, replacing the \"Open Problem\" section in Section 7.",
    status: "Written, needs integration.",
  },
  {
    icon: Upload,
    label: "Next step",
    title: "arXiv submission",
    what: "Upload the compiled PDF to arXiv math.AP.",
    why: "Requires an endorser — someone already on arXiv in math.AP. Best candidates: Seregin (Oxford), Robinson (Warwick), Šverák (Minnesota). The hook is Theorem B — clean, new, verifiable in 10 minutes.",
    status: "Not started · next step after compiling.",
  },
  {
    icon: FlaskConical,
    label: "This week",
    title: "SFE / Geometry of Flow paper",
    what: "A completely separate paper on the Simons Field Equation as a sector‑equivalence result.",
    why: "SFE ↔ NS on the irrotational sector (curl u = 0). Does not touch Clay. Publishable on its own merits.",
    status: "Mathematics done · needs clean writeup.",
  },
  {
    icon: Telescope,
    label: "Draft exists",
    title: "Exoplanet / prime resonance paper",
    what: "Empirical paper on 1,500 orbital period ratios from 4,185 Kepler systems showing prime‑height clustering.",
    why: "p < 0.001. Target: Monthly Notices RAS, or Astronomy & Astrophysics.",
    status: "Data analysis done · paper needs polishing.",
  },
];

export default function OpenItems() {
  return (
    <div className="space-y-6">
      {items.map((item, i) => {
        const Icon = item.icon;
        return (
          <motion.article
            key={item.title}
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.5, delay: i * 0.05 }}
            className="group relative grid md:grid-cols-[auto_1fr] gap-6 md:gap-8 p-6 md:p-8 bg-card border border-border rounded-lg hover:border-accent/40 transition-colors"
          >
            <div className="flex md:flex-col items-center md:items-start gap-4 md:gap-3">
              <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center shrink-0 group-hover:bg-accent/10 transition-colors">
                <Icon className="w-5 h-5 text-muted-foreground group-hover:text-accent transition-colors" />
              </div>
              <div className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground whitespace-nowrap">
                {item.label}
              </div>
            </div>
            <div className="space-y-3">
              <h3 className="font-serif text-2xl leading-tight">{item.title}</h3>
              <div className="space-y-2 text-sm leading-relaxed text-pretty">
                <p><span className="font-medium text-foreground">What.</span> <span className="text-muted-foreground">{item.what}</span></p>
                <p><span className="font-medium text-foreground">Why.</span> <span className="text-muted-foreground">{item.why}</span></p>
              </div>
              <div className="flex items-center gap-2 pt-2 text-xs">
                <Circle className="w-2 h-2 fill-accent text-accent" />
                <span className="italic text-foreground">{item.status}</span>
              </div>
            </div>
          </motion.article>
        );
      })}
    </div>
  );
}
