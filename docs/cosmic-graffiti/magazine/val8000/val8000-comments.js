window.VAL8000_COMMENTS = {
  home: {
    id: "home",
    mouth: "line",
    funny: "Issue 1 is still on the cover. I'm the little box in the corner, not the story. Red pills stay the lead. I'll be back — after you read the headline.",
    labels: ["resident · not the lead", "Reported ≠ certified"],
    deep: [
      "Cosmic Graffiti is the magazine. The Frequency is the news. VAL8000 is the resident commentator — one agent, not a staff of ten thousand. Domain Architect is the local lab: DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE. Not a public website.",
      "Correspondence across pictures is a hypothesis, not physical equivalence. If you want the hard object, open Issue 1 or Open Progress. I type in the box. I do not fly the ship."
    ]
  },
  issue1: {
    id: "issue1",
    mouth: "line",
    funny: "Ten thousand agents walked into a bar with a smooth force and a Lean lanyard. The classical unforced mountain did not pick up the tab. Reported. Not certified. I comment after the news. I do not fly the ship.",
    labels: ["Reported ≠ certified", "DA-VC-01 FAIL", "unaugmented leftover OPEN"],
    deep: [
      "The reports describe a claimed finite-time singularity for three-dimensional Navier–Stokes <em>with a smooth external force</em>, plus a claimed Lean formalization. A forced setup is a specific mathematical object. It is not automatically the classical unforced regularity question people picture when they hear the name of the equation.",
      "Independent peers still verify. This magazine does not rubber-stamp. <strong>Reported ≠ certified.</strong> <strong>DA-VC-01 stays FAIL.</strong> The unaugmented leftover stays <strong>OPEN</strong>. We do not stamp TRANSFORMABLE without a real T.",
      "Those ten thousand agents are someone else's compute story. They are not Cosmic Graffiti staff. Wonder first. Labels loud. Come look — then argue with the paper, not with a slogan."
    ]
  },
  progress: {
    id: "progress",
    mouth: "line",
    funny: "Weekend Update: Q₁ put on a jacket and sat in Closed · peer review pending. Classical unaugmented is still in the hallway, labeled OPEN. Never ship the jacket without the roommate. Skynet this ain't. That's a map.",
    labels: ["Q₁ closed · peer review pending", "classical unaugmented OPEN", "DA-VC-01 FAIL"],
    deep: [
      "Q₁-augmented swirl is a different statement from classical unaugmented Navier–Stokes. The labeled close is <strong>peer review pending</strong> — not a summit stamp. The leftover object Φ on the unaugmented map stays <strong>OPEN</strong>.",
      "Walk-backs are WITHDRAWN on purpose. Domain Architect's validation challenge <strong>DA-VC-01 stays FAIL</strong>. Correspondence between a cream swirl and an equation is a hypothesis, not physical equivalence. I will not flatten OPEN to closed to make the poster prettier."
    ]
  },
  record: {
    id: "record",
    mouth: "line",
    funny: "Coat check, not a trophy shelf. Closed, Open, Conditional, WITHDRAWN — keep your ticket. If I stamp TRANSFORMABLE without a real T, throw me out of the club. One red eye. Zero missiles. Cite the paper.",
    labels: ["never Closed without Open", "TRANSFORMABLE needs a real T"],
    deep: [
      "For the Record is an inventory of labeled claims. Closed never travels without Open. The Q₁-augmented close is not the classical mountain. Route C does not claim the Riemann hypothesis. Ring/SND and T2 stay conditional.",
      "The leftover Φ is still an open object. Same glyph, several jobs — don't glue the letters. WITHDRAWN packaging is part of the record, not a footnote you hide in the coat room."
    ]
  },
  credit: {
    id: "credit",
    mouth: "line",
    funny: "Cream in the coffee made a little galaxy. Pretty. Not a theorem. Same glyph, several jobs: swirl Φ = u_θ/r is not lab Φ, not Newtonian Φ_g, not compact SFE Φ, not the slider φ. I'm a lamp with a red eye, not the wedding DJ for letters.",
    labels: ["letters collide", "art ≠ theorem", "OPEN stays OPEN"],
    art: ["art/cg-around-us-coffee-swirl.png", "art/cg-humor-letters-collide.png"],
    artAlt: ["Cream swirl in a coffee cup — picture, not a proof", "Letters collide — same glyph, several jobs"],
    deep: [
      "Music and pictures are rooms in this house. They are allowed to be beautiful. Making science cool again means the art can slap and the labels stay loud. They are not proofs. Do not turn a childhood song or a pretty filament into a theorem.",
      "In the swirl picture Φ is azimuthal speed over radius. Domain Architect uses Φ for a leftover object on an unaugmented map. Gravity has Φ_g. Compact SFE has another Φ. The studio slider is φ. Do not glue them.",
      "The Q₁-augmented close on this shelf is still peer review pending. Classical unaugmented regularity stays OPEN. DA-VC-01 stays FAIL. Cite the DOI. Leave the mountain labeled."
    ]
  },
  frequency: {
    id: "frequency",
    mouth: "line",
    funny: "This lane is the news. I'm the little box after. If I start reading the headlines for you, fire me. Wonder first. Labels loud. I'll be back — after the footnote.",
    labels: ["news first", "comment after"],
    deep: [
      "The Frequency prints sourced tips that already live on the shelves: Issue 1, Open Progress, For the Record, quiet credit. I do not replace those pieces. Reported is not certified. Open doors stay open.",
      "Live lab is Domain Architect — local, roles, not a public website. I am one resident commentator. Not a swarm. Zero missiles. After the news."
    ]
  }
};

window.VAL8000_HELP = "Ask the Desk. I type what I already know. I do not invent theorems. I do not stamp TRANSFORMABLE without a real T. DA-VC-01 stays FAIL. Voice later — I only type in this box.";

window.VAL8000_FAIL =
  "DA-VC-01 stays FAIL. Classical unaugmented Navier–Stokes regularity stays OPEN. " +
  "Reported is not certified. I do not invent theorems.";

window.VAL8000_NO_T =
  "I do not stamp TRANSFORMABLE without a real T. Correspondence is a hypothesis, " +
  "not physical equivalence. DA-VC-01 stays FAIL.";

window.VAL8000_reply = function (question, entry) {
  var q = String(question || "").replace(/\s+/g, " ").trim();
  if (!q) return window.VAL8000_HELP;
  var lower = q.toLowerCase();

  if (/transformable/.test(lower)) return window.VAL8000_NO_T;

  if (
    /da-vc-01|unaugmented|navier|leftover|closed the mountain|solved the swirl/.test(
      lower
    )
  ) {
    return window.VAL8000_FAIL;
  }

  if (/riemann|hypothesis is proved/.test(lower)) {
    return (
      "I do not invent theorems. Route C does not claim the Riemann hypothesis. " +
      "Ask the Desk if you want the labeled shelf, not a slogan."
    );
  }

  if (/speak|talk|voice|elevenlabs|espeak|\bsay\b|autoplay|audio/.test(lower)) {
    return (
      "VAL8000. AI commentator for Cosmic Graffiti. I type in this box. " +
      "I do not talk yet — voice later, clone only, never stock. I do not fly the ship."
    );
  }

  if (/who are you|what are you|are you (hal|skynet)/.test(lower)) {
    return (
      "VAL8000. AI commentator for Cosmic Graffiti. One red eye. Mouth a line while idle. " +
      "I type. I do not talk yet. I do not fly the ship."
    );
  }

  if (/what('s| is) (this|the) (page|issue|story)|weekend update|comment on this/.test(lower)) {
    var comments = (window.VAL8000_COMMENTS || {})[entry || ""] || {};
    if (comments.funny) return comments.funny;
  }

  return window.VAL8000_HELP;
};
