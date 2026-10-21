#!/usr/bin/env node
"use strict";

const fs = require("fs");
const api = require("../omen_listener/portable/omen_listener.js");

const raw = fs.readFileSync(0, "utf8");
const msg = JSON.parse(raw);
const out = {
  picture: api.buildPicture(msg.picture),
  later: api.buildPicture(msg.later),
  cue: api.rotorCue(msg.samples, msg.sampleRate),
  merged: api.mergeBundles(msg.bundles, {
    communityId: "north-oak",
    alertId: "alert-1",
    communityToken: "oak",
  }).length,
};
process.stdout.write(JSON.stringify(out));
