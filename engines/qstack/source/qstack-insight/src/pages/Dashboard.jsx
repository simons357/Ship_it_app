import React from "react";
import SectionHeader from "../components/report/SectionHeader";
import ProjectGantt from "../components/dashboard/ProjectGantt";
import LaTeXPreviewer from "../components/dashboard/LaTeXPreviewer";
import EndorsementTracker from "../components/dashboard/EndorsementTracker";
import VersionHistory from "../components/dashboard/VersionHistory";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border">
        <div className="max-w-6xl mx-auto px-6 md:px-12 py-12 md:py-16">
          <div className="flex items-baseline gap-3 mb-4">
            <span className="font-mono text-xs text-accent tracking-widest">DASHBOARD</span>
            <span className="h-px flex-1 bg-border" />
          </div>
          <h1 className="font-serif text-4xl md:text-5xl leading-tight">
            Research Program Dashboard
          </h1>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl">
            Track five interconnected research projects, manage arXiv endorsement outreach, and access proofs.
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 md:px-12 py-20 md:py-28 space-y-28 md:space-y-36">
        <section>
          <SectionHeader
            number="01"
            eyebrow="Projects & Milestones"
            title="Interactive Gantt chart."
            subtitle="Five concurrent research programs with live progress tracking."
          />
          <ProjectGantt />
        </section>

        <section>
          <SectionHeader
            number="02"
            eyebrow="Theorem H"
            title="LaTeX proof viewer."
            subtitle="Complete proof ready to compile. Copy, download, or view formatted."
          />
          <LaTeXPreviewer />
        </section>

        <section>
          <SectionHeader
            number="03"
            eyebrow="Version Control"
            title="Document history."
            subtitle="Upload .tex or .pdf iterations, tag by status, and compare changes between versions."
          />
          <VersionHistory />
        </section>

        <section>
          <SectionHeader
            number="04"
            eyebrow="arXiv Endorsement"
            title="CRM & outreach tracker."
            subtitle="Manage contact with potential math.AP endorsers. Track status from pending to endorsed."
          />
          <EndorsementTracker />
        </section>

        <section className="p-8 md:p-12 bg-muted/40 border border-border rounded-lg">
          <h2 className="font-serif text-2xl mb-4">Next Immediate Action</h2>
          <ol className="space-y-3 text-base leading-relaxed">
            <li>
              <span className="font-medium">1. Compile the paper.</span>{" "}
              <span className="text-muted-foreground">
                Open Overleaf. Paste Simons_NS_QStack_arXiv.tex. Insert the Theorem H proof (above) into Section 7. Verify LaTeX compiles.
              </span>
            </li>
            <li>
              <span className="font-medium">2. Update endorsement tracker.</span>{" "}
              <span className="text-muted-foreground">
                Mark status as "Contacted" once you've sent emails. Track responses.
              </span>
            </li>
            <li>
              <span className="font-medium">3. Submit to arXiv.</span>{" "}
              <span className="text-muted-foreground">
                Once you have an endorsement, upload PDF to math.AP. MSC: 35Q30, 76D05, 35B65, 42B25.
              </span>
            </li>
          </ol>
        </section>
      </main>

      <footer className="border-t border-border">
        <div className="max-w-6xl mx-auto px-6 md:px-12 py-10 text-xs text-muted-foreground">
          <div className="font-mono uppercase tracking-widest">
            Dashboard · April 18, 2026
          </div>
        </div>
      </footer>
    </div>
  );
}
