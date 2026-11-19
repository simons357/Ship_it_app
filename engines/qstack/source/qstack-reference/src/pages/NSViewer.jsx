import { useState } from "react";
import Sidebar from "../components/ns/Sidebar";
import SectionViewer from "../components/ns/SectionViewer";
import { sections } from "../components/ns/data";

export default function NSViewer() {
  const [activeSection, setActiveSection] = useState(0);
  const [activeStep, setActiveStep] = useState(0);

  const section = sections[activeSection];
  const steps = section.steps;

  const goNext = () => {
    if (activeStep < steps.length - 1) {
      setActiveStep(activeStep + 1);
    } else if (activeSection < sections.length - 1) {
      setActiveSection(activeSection + 1);
      setActiveStep(0);
    }
  };

  const goPrev = () => {
    if (activeStep > 0) {
      setActiveStep(activeStep - 1);
    } else if (activeSection > 0) {
      const prevSection = sections[activeSection - 1];
      setActiveSection(activeSection - 1);
      setActiveStep(prevSection.steps.length - 1);
    }
  };

  const handleSectionClick = (sIdx) => {
    setActiveSection(sIdx);
    setActiveStep(0);
  };

  const totalSteps = sections.reduce((acc, s) => acc + s.steps.length, 0);
  const completedSteps = sections.slice(0, activeSection).reduce((acc, s) => acc + s.steps.length, 0) + activeStep;

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-mono">
      <Sidebar
        sections={sections}
        activeSection={activeSection}
        activeStep={activeStep}
        onSectionClick={handleSectionClick}
      />
      <SectionViewer
        section={section}
        step={steps[activeStep]}
        stepIndex={activeStep}
        totalSteps={steps.length}
        globalStep={completedSteps}
        globalTotal={totalSteps}
        onNext={goNext}
        onPrev={goPrev}
        canNext={activeSection < sections.length - 1 || activeStep < steps.length - 1}
        canPrev={activeSection > 0 || activeStep > 0}
      />
    </div>
  );
}