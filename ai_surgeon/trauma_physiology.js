/* ==========================================================================
   AI SURGEON — Module 02 trauma physiology
   Tube thoracostomy: tension pneumothorax with haemothorax.

   Extracted so the live monitor and the headless playtest share one loop.
   Numbers match the uploaded trauma module: needle is temporising, a tube
   holds, and staying critical for 40 seconds voids the case.
   ========================================================================== */

(function (global) {
'use strict';

const TraumaPhys = {
  NEEDLE_RELIEF: 0.55,
  TUBE_RELIEF: 1.0,
  /* Per second, multiplied by the coherence clock rate.
     Needle buys ~67–110s depending on band; doing nothing arrests ~56–78s. */
  RELIEF_DECAY: 0.013,
  VITAL_BLEND: 0.040,
  CRITICAL_SBP: 58,
  CRITICAL_SPO2: 79,
  ARREST_AFTER: 40,
  CRITICAL_RECOVER: 2,

  seed(){
    return {
      hr: 128, sbp: 84, dbp: 52, spo2: 88,
      relief: 0, live: false, arrested: false, timeCritical: 0
    };
  },

  resetForDoOne(){
    return {
      hr: 132, sbp: 80, dbp: 48, spo2: 87,
      relief: 0, live: true, arrested: false, timeCritical: 0
    };
  },

  targets(relief){
    const r = relief;
    return {
      hr:   150 - 58 * r,
      sbp:   52 + 62 * r,
      dbp:   30 + 44 * r,
      spo2:  74 + 24 * r
    };
  },

  /* 0 = decompressed and holding, 1 = full tension / crashing.
     Feeds AISS.Handover.assess — envelope opens above 0.7. */
  severity(state){
    const r = Math.max(0, Math.min(1, Number(state.relief) || 0));
    const sbp = Number(state.sbp) || 0;
    if (state.arrested) return 1;
    if (sbp < 58) return 1;
    if (r >= 0.95) return 0.15;
    return Math.max(1 - r, sbp < 84 ? 0.75 : 0);
  },

  give(relief, amount){
    let next = Math.max(Number(relief) || 0, amount);
    if (amount >= 0.95) next = 1;
    return next;
  },

  step(state, dt, clockRate){
    const rate = clockRate == null ? 1 : clockRate;
    const out = {
      hr: state.hr,
      sbp: state.sbp,
      dbp: state.dbp,
      spo2: state.spo2,
      relief: state.relief,
      live: state.live,
      arrested: state.arrested,
      timeCritical: state.timeCritical || 0,
      critical: false,
      arrest: false
    };
    if (!out.live || out.arrested) return out;

    if (out.relief > 0 && out.relief < 0.95) {
      out.relief = Math.max(0, out.relief - dt * this.RELIEF_DECAY * rate);
    }
    const T = this.targets(out.relief);
    const k = dt * this.VITAL_BLEND * rate;
    out.hr   += (T.hr   - out.hr)   * k;
    out.sbp  += (T.sbp  - out.sbp)  * k;
    out.dbp  += (T.dbp  - out.dbp)  * k;
    out.spo2 += (T.spo2 - out.spo2) * k;

    out.critical = out.sbp < this.CRITICAL_SBP || out.spo2 < this.CRITICAL_SPO2;
    if (out.critical) out.timeCritical += dt;
    else out.timeCritical = Math.max(0, out.timeCritical - dt * this.CRITICAL_RECOVER);
    out.arrest = out.timeCritical > this.ARREST_AFTER;
    return out;
  }
};

global.TraumaPhys = TraumaPhys;
if (typeof module !== 'undefined' && module.exports) module.exports = TraumaPhys;
})(typeof window !== 'undefined' ? window : globalThis);
