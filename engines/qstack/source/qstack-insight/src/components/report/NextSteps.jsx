import React from "react";
import { motion } from "framer-motion";

const steps = [
  { n: "01", when: "Today · 30 min", title: "Compile the paper", body: "Open Overleaf. Paste Simons_NS_QStack_arXiv.tex. Insert the (SND‑C) proof from SNDC_proof.tex into Section 7 (replace the \"Open Problem\" block). Check LaTeX compiles cleanly." },
  { n: "02", when: "Today · 20 min", title: "Write the endorser email", body: "One email to George Seregin (Oxford). Three paragraphs: what the paper claims (scoped to T³) · the new result, Theorem B · request for arXiv endorsement in math.AP." },
  { n: "03", when: "After endorsement", title: "Submit to arXiv", body: "Category: math.AP (Analysis of PDEs). MSC: 35Q30, 76D05, 35B65, 42B25." },
  { n: "04", when: "This week", title: "Begin SFE standalone paper", body: "Write the 15‑page irrotational sector paper. Use the MasterMap descent diagram as Figure 1. Clean, honest, publishable." },
  { n: "05", when: "Ongoing · months", title: "ℝ³ extension program", body: "Study Bahouri–Gérard profiles for NS. This is the path from \"resolved on T³\" to the Clay Prize." },
];

export default function NextSteps() {
  return (
    <ol className="relative space-y-12 md:space-y-16 pl-0">
      <div className="absolute left-[11px] md:left-[15px] top-2 bottom-8 w-px bg-border" aria-hidden="true" />
      {steps.map((s, i) => (
        <motion.li
          key={s.n}
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, delay: i * 0.08 }}
          className="relative grid grid-cols-[auto_1fr] gap-6 md:gap-10"
        >
          <div className="relative">
            <div className="w-6 h-6 md:w-8 md:h-8 rounded-full bg-background border-2 border-accent flex items-center justify-center font-mono text-[9px] md:text-[10px] text-accent font-medium">
              {s.n}
            </div>
          </div>
          <div className="pb-2">
            <div className="text-[11px] uppercase tracking-widest text-accent mb-2">{s.when}</div>
            <h3 className="font-serif text-2xl md:text-3xl leading-tight mb-3 text-balance">{s.title}</h3>
            <p className="text-base leading-relaxed text-muted-foreground max-w-2xl text-pretty">{s.body}</p>
          </div>
        </motion.li>
      ))}
    </ol>
  );
}
