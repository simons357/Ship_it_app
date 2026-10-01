# Pictures

Four objects. Each is shown two ways: a drawing, then a labeled plot. The drawings are for the gut. The plots are for the habit of reading axes.

Same files: [`figures/`](figures/).

---

## 1. Laminar vs turbulent

**Look at:** a pipe. Left, the dye would stay a thread. Right, the dye is mixed by eddies of several sizes.

<img src="/opt/cursor/artifacts/ns_laminar_vs_turbulent.png" alt="Laminar pipe flow with parallel streamlines next to turbulent pipe flow with mixed eddies" />

**Then the profiles.** Across a pipe, laminar speed is a **parabola** (Poiseuille). Turbulent mean speed is **flatter in the core** and drops near the wall; a snapshot jitters around that mean.

<img src="/opt/cursor/artifacts/ns_laminar_vs_turbulent_plot.png" alt="Poiseuille parabola versus a flatter turbulent mean profile with fluctuations" />

**Takeaway.** Laminar is not “simple because we like it.” It is the viscous corner of Navier–Stokes. Turbulence is the same law when the nonlinear term has enough room to breed scales. Blood in a capillary is usually laminar. Blood in the aorta is not a capillary.

---

## 2. A control volume

**Look at:** a dashed box. Fluid in, fluid out, pressure on the skin, gravity, an object inside.

<img src="/opt/cursor/artifacts/ns_control_volume.png" alt="Control volume V with surface S, inlet and outlet arrows, pressure, gravity, and an object inside" />

<img src="/opt/cursor/artifacts/ns_control_volume_plot.png" alt="Labeled schematic of a dashed control volume with inlet, outlet, and gravity" />

**Takeaway.** Before there is a PDE, there is accounting. Navier–Stokes is that accounting written at every point. If you can keep mass and momentum honest on \(S\), you already understand the skeleton of the equation. Lift on a wing is a control-volume statement. So is “what did this stenosis do to the pressure drop.”

---

## 3. A vortex

**Look at:** a spinning tube. Fast core, slower wrap, a hint of stretch along the axis.

<img src="/opt/cursor/artifacts/ns_vortex.png" alt="A spinning vortex tube with a bright core and wrapping streamlines" />

**Then the plane cut.** A Rankine sketch: inside the dashed core the fluid rotates almost as a rigid body; outside, swirl falls like \(1/r\).

<img src="/opt/cursor/artifacts/ns_vortex_plot.png" alt="Rankine vortex: solid-body core and 1/r swirl outside, shown as streamlines" />

**Takeaway.** A vortex is not a separate religion. It is velocity going around. In three dimensions you can **stretch** the tube; stretching intensifies spin. That is the shape OpenAI used in the 8 September write-up (inward spiral, spaghetti elongation). It is also the shape of wingtip vortices, bathtub drains, and a lot of cardiac flow. The news construction is a designed example. The object is real.

Book B talks about swirl with \(\Phi = u_\theta/r\). That letter is **not** Domain Architect’s \(\Phi\). Do not glue them. Leftover \(T_{j\leftarrow j}\) (radial stretching \(u^r/r\)) is still **OPEN**.

---

## 4. Energy cascade

**Look at:** a large eddy breaking into smaller ones until viscosity can finish the job.

<img src="/opt/cursor/artifacts/ns_energy_cascade.png" alt="Energy cascade: a large eddy breaking into smaller eddies and then dissipating" />

**Then the spectrum sketch.** Horizontal: wavenumber \(k\) (big \(k\) means small eddies). Vertical: energy at that size. The dashed slope is the Kolmogorov \(k^{-5/3}\) cartoon of the in-between range. The red band is where viscosity wins. This is a **sketch**, not a measurement from a tunnel.

<img src="/opt/cursor/artifacts/ns_energy_spectrum_plot.png" alt="Sketch of a Kolmogorov energy spectrum with a k to the minus five thirds inertial range" />

**Takeaway.** This is why the equations feel beastly. You do not get to pick “the” eddy. Energy is a chain. Paper2’s SND story is a **conditional** attempt to talk about shells of that chain on a torus. It is not this picture, and it is not Book B.

---

## How to look at a fluids figure for the rest of your life

1. Is the flow **laminar or turbulent**? (One scale vs many.)
2. What **box** are they balancing? (Control volume.)
3. Is spin being **stretched**? (Vortex.)
4. Where is the energy going? (Cascade.)

If a headline skips those four, it is not teaching you the law.

Back to [why the equations](02-why-these-equations.md) or the [start page](README.md).
