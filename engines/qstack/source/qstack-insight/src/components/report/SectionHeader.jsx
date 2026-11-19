import React from "react";

export default function SectionHeader({ number, eyebrow, title, subtitle }) {
  return (
    <div className="mb-12 md:mb-16">
      <div className="flex items-baseline gap-4 mb-4">
        <span className="font-mono text-xs text-accent tracking-widest">{number}</span>
        <span className="h-px flex-1 bg-border" />
        <span className="font-mono text-xs text-muted-foreground uppercase tracking-widest">{eyebrow}</span>
      </div>
      <h2 className="font-serif text-3xl md:text-5xl leading-tight tracking-tight text-balance">
        {title}
      </h2>
      {subtitle && (
        <p className="mt-4 font-serif text-lg md:text-xl text-muted-foreground max-w-2xl italic text-pretty">
          {subtitle}
        </p>
      )}
    </div>
  );
}
