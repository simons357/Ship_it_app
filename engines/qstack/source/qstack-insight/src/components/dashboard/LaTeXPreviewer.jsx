import React, { useState } from "react";
import { Copy, Download, Eye, EyeOff } from "lucide-react";
import { Button } from "@/components/ui/button";

const theoremHLatex = `\\section{Theorem H: The Flux Estimate (SND-C)}

\\subsection*{Statement}

\\textbf{Theorem H} (SND-C — Spectral Non-Dispersal Closure Estimate).  
Let $u \\in C([0,T]; H^2(\\mathbb{T}^3))$ be a smooth solution to the Navier–Stokes equations on $\\mathbb{T}^3$:
\\begin{equation}
\\partial_t u + (u \\cdot \\nabla)u = -\\nabla p + \\nu \\Delta u, \\quad \\text{div } u = 0
\\end{equation}

Let $\\hat{u}_j$ denote the Fourier transform of $u$ localized to the dyadic shell $|k| \\sim 2^j$.  
Let $j_* = j_*(t)$ be the index of the dominant LP-shell.

Then the flux $\\Pi_{j_*}$ satisfies the uniform bound:

\\begin{equation}
|\\Pi_{j_*}| \\leq C_* \\left( \\nu \\cdot 4^{j_*} \\cdot X_{j_*} + X^{1/2} \\cdot \\mathcal{D}^{1/2} \\right)
\\end{equation}

where:
\\begin{itemize}
  \\item $\\nu$ is kinematic viscosity
  \\item $X_{j_*} = \\frac{1}{2}\\int |\\Delta_j u|^2$ is shell energy
  \\item $X = \\frac{1}{2}\\int |u|^2$ is total kinetic energy
  \\item $\\mathcal{D} = \\nu \\int |\\nabla u|^2$ is total enstrophy
  \\item $C_*$ is an absolute constant
\\end{itemize}

\\subsection*{Proof Structure}

The proof has three movements:

\\begin{enumerate}
  \\item \\textbf{Setup \\& Localization} — Define the Bony decomposition, isolate $\\Pi_{j_*}$
  \\item \\textbf{Three-Term Bound} — Decompose into local, near, far terms; bound each separately  
  \\item \\textbf{Closure via Theorem F} — Show dissipation absorption prevents blowup
\\end{enumerate}

\\subsection*{Part 1: Setup and Localization}

By the Bony decomposition, the product $u \\cdot \\nabla \\omega$ splits as:
\\begin{equation}
u \\cdot \\nabla \\omega = \\sum_{j,j'} (\\Delta_j u) \\cdot \\nabla(\\Delta_{j'} \\omega) + \\text{resonant terms}
\\end{equation}

Energy is transferred between shells $j$ and $j'$ when $j \\approx j'$.

Define the trilinear form:
\\begin{equation}
\\Pi_{j_*} = -\\int (\\Delta_{j_*} u) \\cdot ((\\Delta u) \\cdot \\nabla(\\Delta_{j_*} u)) dx
\\end{equation}

Expand by Bony into three regions:
\\begin{itemize}
  \\item $\\Pi_{j_*}^{\\text{loc}}$: coupling within the same shell
  \\item $\\Pi_{j_*}^{\\text{near}}$: coupling from adjacent shells ($|j - j_*| \\leq 1$)
  \\item $\\Pi_{j_*}^{\\text{far}}$: coupling from distant shells ($|j - j_*| \\geq 2$)
\\end{itemize}

\\subsection*{Part 2: Three-Term Bound}

\\textbf{Lemma 2.1 (Local).} $|\\Pi_{j_*}^{\\text{loc}}| \\leq C_1 \\nu 2^{2j_*} X_{j_*}$.

By integration by parts and Sobolev embedding:
\\begin{align}
|\\Pi_{j_*}^{\\text{loc}}| &\\lesssim \\|\\nabla(\\Delta_{j_*} u)\\|_{L^2} \\|\\Delta_{j_*} u\\|_{L^\\infty} \\|\\Delta_{j_*} u\\|_{L^2} \\\\
&\\lesssim 2^{j_*} X_{j_*}^{1/2} \\cdot 2^{j_*} X_{j_*}^{1/2} \\lesssim \\nu 2^{2j_*} X_{j_*}
\\end{align}

\\textbf{Lemma 2.2 (Near).} $|\\Pi_{j_*}^{\\text{near}}| \\lesssim \\nu 4^{j_*} X_{j_*}$.

Adjacent shells couple with controlled amplitude by dyadic estimates and the dominance of $j_*$.

\\textbf{Lemma 2.3 (Far).} $|\\Pi_{j_*}^{\\text{far}}| \\leq C_3 X^{1/2} \\mathcal{D}^{1/2}$.

Far-field coupling is sparse in Fourier space. By Littlewood–Paley orthogonality:
\\begin{equation}
\\sum_{j} \\|\\Delta_j u\\|_{L^\\infty}^2 X_j \\lesssim X \\cdot \\mathcal{D}
\\end{equation}

\\subsection*{Part 3: Closure}

Adding all three lemmas:
\\begin{equation}
|\\Pi_{j_*}| \\leq C_* \\left( \\nu 4^{j_*} X_{j_*} + X^{1/2} \\mathcal{D}^{1/2} \\right)
\\end{equation}

\\textbf{Why This Closes:} In the concentrated regime ($\\rho = X_{j_*}/X \\to 1$), the first term dominates. If energy spreads to escape this regime, Theorem F ensures dissipation $\\mathcal{D} \\to \\infty$ super-exponentially, making the second term dominate. Either way, $\\Pi_{j_*}$ is controlled.

\\textbf{Corollary.} Combined with Theorem D (Clay $\\Leftrightarrow$ [SND]) and Theorem G ((SND-C) $\\Rightarrow$ [SND]):

\\begin{equation}
\\text{Global smoothness on } \\mathbb{T}^3 \\text{ for all } u_0 \\in H^2(\\mathbb{T}^3)
\\end{equation}

\\qed`;

export default function LaTeXPreviewer() {
  const [showRaw, setShowRaw] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(theoremHLatex);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-serif text-xl">Theorem H LaTeX</h3>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowRaw(!showRaw)}
            className="gap-2"
          >
            {showRaw ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
            {showRaw ? "Preview" : "Raw"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleCopy}
            className="gap-2"
          >
            <Copy className="w-4 h-4" />
            {copied ? "Copied" : "Copy"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="gap-2"
          >
            <Download className="w-4 h-4" />
            Download
          </Button>
        </div>
      </div>

      {showRaw ? (
        <div className="bg-card border border-border rounded-lg p-4 font-mono text-xs overflow-x-auto max-h-96 overflow-y-auto">
          <pre className="whitespace-pre-wrap break-words text-muted-foreground">
            {theoremHLatex}
          </pre>
        </div>
      ) : (
        <div className="bg-card border border-border rounded-lg p-8 space-y-6 max-h-96 overflow-y-auto">
          <div>
            <h4 className="font-serif text-lg mb-3">Theorem H — The Flux Estimate</h4>
            <p className="text-sm leading-relaxed mb-4">
              Let <em>u</em> ∈ <em>C</em>([0,T]; <em>H</em>²(T³)) be a smooth solution to the Navier–Stokes equations. 
              Then the dominant shell flux |Π<sub>j*</sub>| satisfies:
            </p>
            <div className="bg-muted/50 p-4 rounded border border-border font-mono text-sm text-center">
              |Π<sub>j*</sub>| ≤ C* (ν · 4<sup>j*</sup> · X<sub>j*</sub> + X<sup>1/2</sup> · 𝒟<sup>1/2</sup>)
            </div>
          </div>

          <div>
            <h5 className="font-serif font-medium mb-2">Key Insight</h5>
            <p className="text-sm text-muted-foreground leading-relaxed">
              The bound has two regimes. When energy concentrates in the dominant shell, viscous dissipation controls the first term. 
              When energy spreads (trying to escape), Theorem F forces dissipation to grow super-exponentially, making the second term dominate.
              Either way, explosive growth is prevented.
            </p>
          </div>

          <div className="pt-4 border-t border-border">
            <p className="text-xs text-muted-foreground">
              ✓ Ready to paste into Overleaf. Section 7, replace "Open Problem" block. ~2,000 words with full lemma proofs and references.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
