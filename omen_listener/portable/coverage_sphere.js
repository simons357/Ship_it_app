/*
 * Play model for a body-worn listener sphere.
 *
 * AirPods are a voice mic at the ear: one room, 3 m.
 * A phone on listen is open to the air: 6 m.
 * The bundle handoff is a separate 10 m phone-to-phone step.
 * These are not a measurement, and they are not the tree-line kilometer.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.OmenCoverage = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  const COVERAGE = {
    earM: 1.6,
    pocketM: 1.0,
    airpodsRadiusM: 3,
    phoneRadiusM: 6,
    bundleM: 10,
    ceilingM: 2.7,
  };

  function round1(value) {
    return Math.round(value * 10) / 10;
  }

  function mic(kind, headM) {
    if (kind === "airpods") {
      return { name: "AirPods", y: headM, r: COVERAGE.airpodsRadiusM };
    }
    return { name: "phone", y: Math.max(0.4, headM - 0.6), r: COVERAGE.phoneRadiusM };
  }

  function assess(input) {
    const youHead = COVERAGE.earM;
    const you = mic(input.you, youHead);
    const them = mic(input.them, Number(input.theirHeadM));
    const distance = Number(input.distanceM);
    const gap = Math.hypot(distance, them.y - you.y);
    const indoors = input.place === "indoors";
    const rawTop = you.y + you.r;
    const usableTop = indoors ? Math.min(rawTop, COVERAGE.ceilingM) : rawTop;
    const theirPhoneY = Math.max(0.4, Number(input.theirHeadM) - 0.6);
    const bundleGap = Math.hypot(distance, theirPhoneY - COVERAGE.pocketM);
    const insideYours = gap <= you.r + 1e-9;
    const youInsideTheirs = gap <= them.r + 1e-9;
    const overlap = gap <= you.r + them.r + 1e-9;
    const bundle = bundleGap <= COVERAGE.bundleM + 1e-9;
    const ceilingCuts = indoors && rawTop > COVERAGE.ceilingM;
    const lines = [
      ceilingCuts
        ? "How high: the sphere wants " + round1(rawTop) + " m. The ceiling stops it at " + COVERAGE.ceilingM + " m."
        : "How high: " + round1(usableTop) + " m above the floor.",
      "They are " + round1(distance) + " m away, head at " + round1(Number(input.theirHeadM)) + " m. The gap between mics is " + round1(gap) + " m.",
      insideYours
        ? "They are inside your " + you.name + " sphere (" + you.r + " m)."
        : "They are outside your " + you.name + " sphere (" + you.r + " m).",
      youInsideTheirs
        ? "You are inside their " + them.name + " sphere (" + them.r + " m)."
        : "You are outside their " + them.name + " sphere (" + them.r + " m).",
      overlap ? "The two spheres overlap." : "The two spheres do not overlap.",
      bundle ? "Their phone can hand you the bundle." : "Their phone is too far to hand you the bundle.",
    ];
    return {
      gapM: gap,
      rawTopM: rawTop,
      usableTopM: usableTop,
      insideYours: insideYours,
      youInsideTheirs: youInsideTheirs,
      overlap: overlap,
      bundle: bundle,
      ceilingCuts: ceilingCuts,
      yourY: you.y,
      yourR: you.r,
      theirY: them.y,
      theirR: them.r,
      lines: lines,
    };
  }

  return { COVERAGE: COVERAGE, assess: assess, round1: round1 };
});
