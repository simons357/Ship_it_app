import React from "react";
import ReportHero from "../components/report/ReportHero";
import SectionHeader from "../components/report/SectionHeader";
import TheoremTable from "../components/report/TheoremTable";
import KeyMove from "../components/report/KeyMove";
import MeaningBlock from "../components/report/MeaningBlock";
import OpenItems from "../components/report/OpenItems";
import PaperComparison from "../components/report/PaperComparison";
import NextSteps from "../components/report/NextSteps";
import BodyOfWork from "../components/report/BodyOfWork";

export default function Report() {
  return (
    <div className="min-h-screen bg-background">
      <ReportHero />

      <main className="max-w-5xl mx-auto px-6 md:px-12 py-20 md:py-28 space-y-28 md:space-y-36">
        <section>
          <SectionHeader
            number="PART 01"
            eyebrow="What is done"
            title="The main paper — complete."
            subtitle="Simons_NS_QStack_arXiv.tex · Ready to compile in Overleaf. Ready for arXiv submission."
          />
          <TheoremTable />
          <KeyMove />
          <div className="mt-12 p-6 bg-muted/50 border-l-2 border-accent">
            <p className="text-sm leading-relaxed">
              <span className="font-medium">Plus three propositions.</span> <span className="text-muted-foreground">Small data (Koch–Tataru), Bounded H², Large data (cascade incompatibility). All proved.</span>
              <br />
              <span className="font-medium mt-2 inline-block">Plus one main corollary.</span> <span className="text-muted-foreground">No finite‑time singularity on T³. Follows from Theorems D + G + H.</span>
            </p>
          </div>
        </section>

        <section>
          <SectionHeader
            number="PART 02"
            eyebrow="What it means"
            title="Plain language."
          />
          <MeaningBlock />
        </section>

        <section>
          <SectionHeader
            number="PART 03"
            eyebrow="What is not done"
            title="The open items."
            subtitle="Honestly scoped. One real research gap remains."
          />
          <OpenItems />
        </section>

        <section>
          <SectionHeader
            number="PART 04"
            eyebrow="Two papers · kept separate"
            title="The NS paper and the SFE paper do not touch."
          />
          <PaperComparison />
        </section>

        <section>
          <SectionHeader
            number="PART 05"
            eyebrow="Immediate next steps"
            title="In order."
          />
          <NextSteps />
        </section>

        <section>
          <SectionHeader
            number="PART 06"
            eyebrow="Your body of work"
            title="What you've built."
          />
          <BodyOfWork />
        </section>
      </main>

      <footer className="border-t border-border">
        <div className="max-w-5xl mx-auto px-6 md:px-12 py-10 flex flex-col md:flex-row md:items-center md:justify-between gap-4 text-xs text-muted-foreground">
          <div className="font-mono uppercase tracking-widest">
            Report generated April 18, 2026
          </div>
          <div className="flex items-center gap-6">
            <a href="/dashboard" className="hover:text-foreground transition-colors">Dashboard →</a>
            <div className="font-serif italic">
              Prime Field Technologies LLC · Jonathan Robert Simons, CRNA, MMed
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
