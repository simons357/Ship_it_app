/*
 * Portable OMEN listener. Same contract as the Python package.
 *
 * A phone, a wearable, or a tree-top box can run this file with no network
 * and no dependencies. It listens for a rotor-like harmonic stack, merges
 * observations it already holds, and opens a shelter clock only when there
 * is a track toward the protected point.
 *
 * Keep the numeric constants aligned with omen_listener/detect.py,
 * omen_listener/picture.py, and omen_listener/geo.py.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  if (root) {
    root.OmenListener = api;
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  const F_MIN_HZ = 80;
  const F_MAX_HZ = 250;
  const F_STEP_HZ = 5;
  const P1_OVER_NOISE = 8;
  const P2_OVER_NOISE = 5;
  const P3_OVER_NOISE = 4;
  const MIN_SCORE = 0.45;
  const SPEED_OF_SOUND_M_S = 343;

  const M_PER_DEG_LAT = 111320;
  const COMPASS_8 = [
    "north",
    "northeast",
    "east",
    "southeast",
    "south",
    "southwest",
    "west",
    "northwest",
  ];

  const BIN_S = 1;
  const MIN_CROSS = 0.2;
  const MIN_SPEED_M_S = 8;
  const MAX_SPEED_M_S = 90;
  const MIN_PATH_M = 40;
  const MIN_SPAN_S = 1.5;
  const MAX_SEGMENT_HEADING_DEG = 40;
  const DEFAULT_LEAD_S = 30;
  const DEFAULT_WATCH_RADIUS_M = 1000;
  const DEFAULT_STALE_AFTER_S = 8;
  const DEFAULT_HOLD_S = 120;
  const DEFAULT_MAX_EXTRAP_S = 45;
  const MAX_RANGE_M = 20000;
  const MAX_OPEN_UNCERTAINTY_M = 800;
  const OVERHEAD_M = 150;
  const EXTRAP_GROWTH_M_PER_S = 5;
  const FUTURE_SKEW_S = 5;
  const MOVE_WITHIN_S = 180;
  const APPROX_WHEN_M = 150;
  const PLATE_RANGE_M = 40;
  const PLATE_RMSE_M = 12;
  const DEFAULT_SIGMA_DEG = { treetop: 3, phone: 8, wearable: 12 };

  function mod(value, cycle) {
    return ((value % cycle) + cycle) % cycle;
  }

  function hann(samples) {
    const n = samples.length;
    if (n <= 1) return samples.slice();
    const scale = (2 * Math.PI) / (n - 1);
    const out = new Array(n);
    for (let i = 0; i < n; i += 1) {
      out[i] = samples[i] * (0.5 - 0.5 * Math.cos(scale * i));
    }
    return out;
  }

  function goertzelPower(samples, sampleRate, freq) {
    const n = samples.length;
    if (n === 0 || freq <= 0 || freq >= sampleRate / 2) return 0;
    const omega = (2 * Math.PI * freq) / sampleRate;
    const coeff = 2 * Math.cos(omega);
    let s1 = 0;
    let s2 = 0;
    for (let i = 0; i < n; i += 1) {
      const s0 = samples[i] + coeff * s1 - s2;
      s2 = s1;
      s1 = s0;
    }
    let power = s1 * s1 + s2 * s2 - coeff * s1 * s2;
    if (power < 0) power = 0;
    return power / (n * n);
  }

  function rotorCue(samples, sampleRate) {
    if (sampleRate < 8000 || samples.length < 1024) {
      return { detected: false, score: 0, fundamentalHz: null, detail: "frame too short" };
    }
    const windowed = hann(samples);
    let bestScore = 0;
    let bestF = null;
    for (let f = F_MIN_HZ; f <= F_MAX_HZ + 1e-9; f += F_STEP_HZ) {
      if (3 * f >= sampleRate * 0.45) break;
      const p1 = goertzelPower(windowed, sampleRate, f);
      const p2 = goertzelPower(windowed, sampleRate, 2 * f);
      const p3 = goertzelPower(windowed, sampleRate, 3 * f);
      const noiseBins = [];
      const fractions = [0.55, 0.72, 1.35, 1.62, 2.28, 2.55];
      for (let i = 0; i < fractions.length; i += 1) {
        const nf = f * fractions[i];
        if (nf < 40 || nf >= sampleRate * 0.45) continue;
        const nearest = Math.min(Math.abs(nf - f), Math.abs(nf - 2 * f), Math.abs(nf - 3 * f));
        if (nearest < 12) continue;
        noiseBins.push(goertzelPower(windowed, sampleRate, nf));
      }
      if (noiseBins.length < 3) continue;
      noiseBins.sort(function (a, b) {
        return a - b;
      });
      const noise = Math.max(noiseBins[Math.floor(noiseBins.length / 2)], 1e-18);
      const ratio2 = p1 > 0 ? p2 / p1 : 0;
      const ratio3 = p1 > 0 ? p3 / p1 : 0;
      const stack =
        p1 > P1_OVER_NOISE * noise &&
        p2 > P2_OVER_NOISE * noise &&
        p3 > P3_OVER_NOISE * noise &&
        ratio2 >= 0.04 &&
        ratio2 <= 2.5 &&
        ratio3 >= 0.01 &&
        ratio3 <= 2.5;
      if (!stack) continue;
      const weakest = Math.min(p1 / P1_OVER_NOISE, p2 / P2_OVER_NOISE, p3 / P3_OVER_NOISE);
      let score = weakest / noise / 4;
      if (score > 1) score = 1;
      if (score > bestScore) {
        bestScore = score;
        bestF = f;
      }
    }
    if (bestF === null || bestScore < MIN_SCORE) {
      return { detected: false, score: bestScore, fundamentalHz: bestF, detail: "no harmonic stack" };
    }
    return { detected: true, score: bestScore, fundamentalHz: bestF, detail: "harmonic stack" };
  }

  function correlation(left, right, lag) {
    const n = Math.min(left.length, right.length);
    let acc = 0;
    let count = 0;
    for (let i = 0; i < n; i += 1) {
      const j = i - lag;
      if (j >= 0 && j < n) {
        acc += left[i] * right[j];
        count += 1;
      }
    }
    if (count === 0) return 0;
    return acc / count;
  }

  function delayRightMinusLeft(left, right, sampleRate, maxDelayS) {
    const n = Math.min(left.length, right.length);
    if (n < 256 || sampleRate <= 0 || maxDelayS <= 0) return null;
    const maxLag = Math.max(1, Math.ceil(maxDelayS * sampleRate));
    let bestLag = 0;
    let best = correlation(left, right, 0);
    for (let lag = -maxLag; lag <= maxLag; lag += 1) {
      if (lag === 0) continue;
      const value = correlation(left, right, lag);
      if (value > best) {
        best = value;
        bestLag = lag;
      }
    }
    if (bestLag <= -maxLag || bestLag >= maxLag) return -bestLag / sampleRate;
    const leftC = correlation(left, right, bestLag - 1);
    const rightC = correlation(left, right, bestLag + 1);
    const denom = leftC - 2 * best + rightC;
    let delta = 0;
    if (denom !== 0) {
      delta = (0.5 * (leftC - rightC)) / denom;
      if (delta > 1) delta = 1;
      else if (delta < -1) delta = -1;
    }
    return -(bestLag + delta) / sampleRate;
  }

  function azimuthFromDelay(delayS, spacingM, arrayHeadingDeg) {
    if (spacingM <= 0) return null;
    let arg = (-SPEED_OF_SOUND_M_S * delayS) / spacingM;
    if (arg > 1) arg = 1;
    else if (arg < -1) arg = -1;
    const phiDeg = (Math.asin(arg) * 180) / Math.PI;
    return mod(arrayHeadingDeg + phiDeg, 360);
  }

  function azimuthFromPair(left, right, sampleRate, spacingM, arrayHeadingDeg) {
    if (spacingM <= 0) return null;
    const delay = delayRightMinusLeft(left, right, sampleRate, spacingM / SPEED_OF_SOUND_M_S);
    if (delay === null) return null;
    return azimuthFromDelay(delay, spacingM, arrayHeadingDeg);
  }

  function metersPerDegLon(latDeg) {
    return M_PER_DEG_LAT * Math.cos((latDeg * Math.PI) / 180);
  }

  function toLocal(lat, lon, originLat, originLon) {
    return [(lon - originLon) * metersPerDegLon(originLat), (lat - originLat) * M_PER_DEG_LAT];
  }

  function toGeo(east, north, originLat, originLon) {
    return [originLat + north / M_PER_DEG_LAT, originLon + east / metersPerDegLon(originLat)];
  }

  function compassDeg(east, north) {
    return mod((Math.atan2(east, north) * 180) / Math.PI, 360);
  }

  function direction(azimuthDeg) {
    const radians = (azimuthDeg * Math.PI) / 180;
    return [Math.sin(radians), Math.cos(radians)];
  }

  function angDiffDeg(a, b) {
    return Math.abs(mod(a - b + 180, 360) - 180);
  }

  function compassName(azimuthDeg) {
    return COMPASS_8[Math.floor((azimuthDeg + 22.5) / 45) % 8];
  }

  function whereText(east, north, approximate) {
    const dist = Math.hypot(east, north);
    let phrase;
    if (dist < 15) {
      phrase = "at the protected point";
    } else {
      const amount = dist >= 1000 ? (dist / 1000).toFixed(1) + " km" : String(Math.round(dist)) + " m";
      phrase = amount + " " + compassName(compassDeg(east, north)) + " of the protected point";
    }
    if (approximate && dist >= 15) return "about " + phrase;
    return phrase;
  }

  function intersectBearings(originA, azimuthA, originB, azimuthB) {
    const dirA = direction(azimuthA);
    const dirB = direction(azimuthB);
    const det = dirA[0] * dirB[1] - dirA[1] * dirB[0];
    const sinCross = Math.abs(det);
    if (sinCross < MIN_CROSS) return null;
    const dx = originB[0] - originA[0];
    const dy = originB[1] - originA[1];
    const rangeA = (dx * dirB[1] - dy * dirB[0]) / det;
    const rangeB = (dx * dirA[1] - dy * dirA[0]) / det;
    if (rangeA < 0 || rangeB < 0) return null;
    if (rangeA > MAX_RANGE_M || rangeB > MAX_RANGE_M) return null;
    return {
      east: originA[0] + rangeA * dirA[0],
      north: originA[1] + rangeA * dirA[1],
      sinCross: sinCross,
      rangeA: rangeA,
      rangeB: rangeB,
    };
  }

  function sigmaDeg(obs) {
    if (obs.azimuth_sigma_deg != null) return Number(obs.azimuth_sigma_deg);
    return DEFAULT_SIGMA_DEG[obs.kind] || 8;
  }

  function recentOf(observations, now, holdS) {
    const kept = [];
    for (let i = 0; i < observations.length; i += 1) {
      const t = Number(observations[i].t);
      if (t >= now - holdS && t <= now + FUTURE_SKEW_S) kept.push(observations[i]);
    }
    kept.sort(function (a, b) {
      if (Number(a.t) !== Number(b.t)) return Number(a.t) - Number(b.t);
      return String(a.node_id).localeCompare(String(b.node_id));
    });
    return kept;
  }

  function fixesFrom(observations, originLat, originLon) {
    const groups = {};
    for (let i = 0; i < observations.length; i += 1) {
      const obs = observations[i];
      if (obs.azimuth_deg == null || Number(obs.score || 0) < MIN_SCORE) continue;
      const key = Math.floor(Number(obs.t) / BIN_S);
      if (!groups[key]) groups[key] = [];
      groups[key].push(obs);
    }
    const fixes = [];
    const keys = Object.keys(groups)
      .map(Number)
      .sort(function (a, b) {
        return a - b;
      });
    for (let k = 0; k < keys.length; k += 1) {
      const latest = {};
      const bucket = groups[keys[k]];
      for (let i = 0; i < bucket.length; i += 1) {
        const obs = bucket[i];
        const prev = latest[obs.node_id];
        if (!prev || Number(obs.t) >= Number(prev.t)) latest[obs.node_id] = obs;
      }
      const nodes = Object.keys(latest)
        .sort()
        .map(function (id) {
          return latest[id];
        });
      if (nodes.length < 2) continue;
      let weightedE = 0;
      let weightedN = 0;
      let weightedU = 0;
      let weightedR = 0;
      let weightSum = 0;
      const times = [];
      const used = {};
      for (let i = 0; i < nodes.length; i += 1) {
        const left = nodes[i];
        const leftXy = toLocal(Number(left.lat), Number(left.lon), originLat, originLon);
        for (let j = i + 1; j < nodes.length; j += 1) {
          const right = nodes[j];
          const rightXy = toLocal(Number(right.lat), Number(right.lon), originLat, originLon);
          const hit = intersectBearings(leftXy, Number(left.azimuth_deg), rightXy, Number(right.azimuth_deg));
          if (!hit) continue;
          const sigma = (Math.max(sigmaDeg(left), sigmaDeg(right)) * Math.PI) / 180;
          const pairRmse = (sigma * Math.max(hit.rangeA, hit.rangeB)) / Math.max(hit.sinCross, MIN_CROSS);
          const uncertainty = Math.max(20, pairRmse);
          weightedE += hit.east * hit.sinCross;
          weightedN += hit.north * hit.sinCross;
          weightedU += uncertainty * hit.sinCross;
          weightedR += pairRmse * hit.sinCross;
          weightSum += hit.sinCross;
          times.push(0.5 * (Number(left.t) + Number(right.t)));
          used[String(left.node_id)] = leftXy;
          used[String(right.node_id)] = rightXy;
        }
      }
      if (weightSum <= 0) continue;
      let tSum = 0;
      for (let i = 0; i < times.length; i += 1) tSum += times[i];
      const aimerIds = Object.keys(used).sort();
      fixes.push({
        t: tSum / times.length,
        east_m: weightedE / weightSum,
        north_m: weightedN / weightSum,
        uncertainty_m: weightedU / weightSum,
        rmse_m: weightedR / weightSum,
        aimers: aimerIds.map(function (nodeId) {
          return { node_id: nodeId, east_m: used[nodeId][0], north_m: used[nodeId][1] };
        }),
      });
    }
    return fixes;
  }

  function trajectoryFrom(fixes) {
    const usable = fixes.filter(function (fix) {
      return fix.uncertainty_m <= MAX_OPEN_UNCERTAINTY_M;
    });
    if (usable.length < 2) return null;
    const start = usable[0];
    const end = usable[usable.length - 1];
    const dt = end.t - start.t;
    if (dt < MIN_SPAN_S) return null;
    const de = end.east_m - start.east_m;
    const dn = end.north_m - start.north_m;
    const dist = Math.hypot(de, dn);
    if (dist < MIN_PATH_M) return null;
    const speed = dist / dt;
    if (speed < MIN_SPEED_M_S || speed > MAX_SPEED_M_S) return null;
    const heading = compassDeg(de, dn);
    for (let i = 0; i < usable.length - 1; i += 1) {
      const left = usable[i];
      const right = usable[i + 1];
      const segDt = right.t - left.t;
      if (segDt < 0.4) continue;
      const segDe = right.east_m - left.east_m;
      const segDn = right.north_m - left.north_m;
      if (Math.hypot(segDe, segDn) < 10) continue;
      if (angDiffDeg(compassDeg(segDe, segDn), heading) > MAX_SEGMENT_HEADING_DEG) return null;
    }
    const radians = (heading * Math.PI) / 180;
    return {
      t: end.t,
      east_m: end.east_m,
      north_m: end.north_m,
      vx: speed * Math.sin(radians),
      vy: speed * Math.cos(radians),
      speed_m_s: speed,
      heading_deg: heading,
      uncertainty_m: end.uncertainty_m,
      rmse_m: end.rmse_m,
      aimers: end.aimers,
      fixes: usable,
    };
  }

  function shownM(value) {
    return Math.floor(Number(value) + 0.5);
  }

  function rmseReport(rmseM, east, north, aimers, extrapolatedS) {
    if (rmseM == null || east == null || north == null) {
      return {
        rmse_m: null,
        range_m: null,
        nearest_node_id: null,
        samples: 0,
        close: false,
        try_plate: false,
        label: "No RMSE",
      };
    }
    const grown = Number(rmseM) + EXTRAP_GROWTH_M_PER_S * Number(extrapolatedS);
    let nearestId = null;
    let rangeM = null;
    let best = null;
    const rows = aimers || [];
    for (let i = 0; i < rows.length; i += 1) {
      const dist = Math.hypot(Number(east) - Number(rows[i].east_m), Number(north) - Number(rows[i].north_m));
      if (best === null || dist < best) {
        best = dist;
        nearestId = String(rows[i].node_id);
        rangeM = dist;
      }
    }
    const close = rangeM != null && rangeM <= PLATE_RANGE_M;
    const tryPlate = Boolean(close && grown <= PLATE_RMSE_M && rows.length >= 2);
    const shown = shownM(grown);
    let label = "RMSE " + shown + " m";
    if (tryPlate && rangeM != null) label = "RMSE " + shown + " m · " + shownM(rangeM) + " m out · plate";
    else if (close && rangeM != null) label = "RMSE " + shown + " m · " + shownM(rangeM) + " m out";
    return {
      rmse_m: grown,
      range_m: rangeM,
      nearest_node_id: nearestId,
      samples: rows.length,
      close: close,
      try_plate: tryPlate,
      label: label,
    };
  }

  function guidance(reason, urgency, decisionSeconds, where) {
    let text;
    if (reason === "trajectory" && urgency === "watch" && decisionSeconds != null) {
      text =
        "You have " +
        decisionSeconds +
        "s to decide. The contact is " +
        where +
        ". Stay ready to go inside, away from windows.";
    } else if (reason === "trajectory" && urgency === "move" && decisionSeconds != null) {
      text =
        "You have " +
        decisionSeconds +
        "s to decide. The contact is " +
        where +
        ". Move inside, away from windows.";
    } else if (reason === "trajectory" && urgency === "shelter_now") {
      text = "Decision time is up. The contact is " + where + ". Shelter in place, away from windows.";
    } else if (reason === "receding") {
      text = "The contact is moving away. The decision window is closed. Keep listening.";
    } else if (reason === "wide_miss") {
      text = "A track is passing wide of this point. The decision window stays closed. You can still see it.";
    } else if (reason === "weak_geometry") {
      if (where.indexOf("heard") === 0) {
        text =
          "Listeners hear a rotor-like sound, but the lines do not place it well enough to time a decision. You can see who heard it.";
      } else {
        text = "The contact is " + where + ", but the circle is too large to time a decision. The window stays closed.";
      }
    } else if (reason === "no_bearing") {
      text =
        "Rotor-like sound on a listener, with no direction yet. You can see which listener heard it. The decision window stays closed.";
    } else if (reason === "no_trajectory") {
      text =
        "Rotor-like sound, no track yet. You can see the cue. The decision window stays closed until the contact is clearly moving.";
    } else if (reason === "no_contact") {
      text = "Listening. No rotor cue yet.";
    } else if (reason === "not_listening") {
      text = "Listener is idle. A wearable listen message opens it.";
    } else {
      text = "Listening.";
    }
    return text;
  }

  function point(east, north, originLat, originLon) {
    const geo = toGeo(east, north, originLat, originLon);
    return { lat: geo[0], lon: geo[1], east_m: east, north_m: north };
  }

  function buildPicture(state) {
    if (!state || !state.protected || state.now == null) {
      throw new Error("state needs protected and now");
    }
    const originLat = Number(state.protected.lat);
    const originLon = Number(state.protected.lon);
    const now = Number(state.now);
    const leadS = state.lead_s == null ? DEFAULT_LEAD_S : Number(state.lead_s);
    const watchRadiusM = state.watch_radius_m == null ? DEFAULT_WATCH_RADIUS_M : Number(state.watch_radius_m);
    const holdS = state.hold_s == null ? DEFAULT_HOLD_S : Number(state.hold_s);
    const staleAfterS = state.stale_after_s == null ? DEFAULT_STALE_AFTER_S : Number(state.stale_after_s);
    const maxExtrapS = state.max_extrap_s == null ? DEFAULT_MAX_EXTRAP_S : Number(state.max_extrap_s);
    const listening = Boolean(state.listening);
    const observations = state.observations || [];
    const recent = recentOf(observations, now, holdS);

    const latestByNode = {};
    for (let i = 0; i < recent.length; i += 1) {
      const obs = recent[i];
      const prev = latestByNode[obs.node_id];
      if (!prev || Number(obs.t) >= Number(prev.t)) latestByNode[obs.node_id] = obs;
    }
    const listeners = Object.keys(latestByNode)
      .sort()
      .map(function (nodeId) {
        const obs = latestByNode[nodeId];
        const local = toLocal(Number(obs.lat), Number(obs.lon), originLat, originLon);
        const entry = {
          node_id: nodeId,
          kind: obs.kind || "phone",
          lat: Number(obs.lat),
          lon: Number(obs.lon),
          east_m: local[0],
          north_m: local[1],
          last_score: Number(obs.score || 0),
          last_t: Number(obs.t),
        };
        if (obs.alt_m != null) entry.alt_m = Number(obs.alt_m);
        if (obs.azimuth_deg != null) entry.azimuth_deg = Number(obs.azimuth_deg);
        return entry;
      });

    const systems = [];
    listeners.forEach(function (item) {
      const kind = String(item.kind);
      if (systems.indexOf(kind) === -1) systems.push(kind);
    });
    systems.sort();
    const heardBy = listeners
      .filter(function (item) {
        return item.last_score >= MIN_SCORE;
      })
      .map(function (item) {
        return item.node_id;
      });

    let newestT = null;
    for (let i = 0; i < recent.length; i += 1) {
      const t = Number(recent[i].t);
      if (newestT === null || t > newestT) newestT = t;
    }
    const age = newestT === null ? null : Math.max(0, now - newestT);
    let comms;
    let stale;
    if (newestT === null) {
      comms = listening ? "local" : "idle";
      stale = false;
    } else if (age > staleAfterS) {
      comms = "down";
      stale = true;
    } else {
      comms = "local";
      stale = false;
    }

    const fixes = fixesFrom(recent, originLat, originLon);
    const track = trajectoryFrom(fixes);
    const placed = fixes.length ? fixes[fixes.length - 1] : null;
    let reason = listening ? "no_contact" : "not_listening";
    let openWindow = false;
    let urgency = "none";
    let decisionSeconds = null;
    let timeToClosest = null;
    let timeUncertainty = null;
    let where = "no contact";
    let threat = null;
    let heading = null;
    let speed = null;
    let extrapolatedS = 0;
    let clockEstimated = false;
    const trackPoints = [];

    let azimuthCount = 0;
    for (let i = 0; i < recent.length; i += 1) {
      if (recent[i].azimuth_deg != null && Number(recent[i].score || 0) >= MIN_SCORE) azimuthCount += 1;
    }
    if (recent.length && !placed && azimuthCount >= 2) reason = "weak_geometry";
    else if (recent.length && !placed && azimuthCount === 1) reason = "no_trajectory";
    else if (recent.length && !placed && azimuthCount === 0) reason = "no_bearing";
    else if (placed && !track) {
      reason = placed.uncertainty_m <= MAX_OPEN_UNCERTAINTY_M ? "no_trajectory" : "weak_geometry";
    }

    let east = null;
    let north = null;
    let uncertaintyM = null;
    if (track) {
      const dt = Math.max(0, now - track.t);
      extrapolatedS = Math.min(dt, maxExtrapS);
      clockEstimated = extrapolatedS > 1;
      east = track.east_m + track.vx * extrapolatedS;
      north = track.north_m + track.vy * extrapolatedS;
      uncertaintyM = track.uncertainty_m + EXTRAP_GROWTH_M_PER_S * extrapolatedS;
      heading = track.heading_deg;
      speed = track.speed_m_s;
      const rx = -east;
      const ry = -north;
      const vv = track.vx * track.vx + track.vy * track.vy;
      const tCpa = (rx * track.vx + ry * track.vy) / vv;
      let miss;
      let eta;
      let approaching;
      if (tCpa > 0.5) {
        miss = Math.hypot(east + track.vx * tCpa, north + track.vy * tCpa);
        eta = tCpa;
        approaching = true;
      } else {
        miss = Math.hypot(east, north);
        eta = 0;
        approaching = false;
      }
      timeToClosest = eta;
      timeUncertainty = speed ? uncertaintyM / speed : null;
      where = whereText(east, north, uncertaintyM > APPROX_WHEN_M);
      threat = point(east, north, originLat, originLon);
      threat.uncertainty_m = uncertaintyM;
      const outward = east * track.vx + north * track.vy;
      if (uncertaintyM > MAX_OPEN_UNCERTAINTY_M) {
        reason = "weak_geometry";
      } else if (approaching && miss <= watchRadiusM) {
        reason = "trajectory";
        openWindow = true;
        const conservative = Math.max(0, eta - (timeUncertainty || 0));
        if (conservative <= leadS) {
          urgency = "shelter_now";
          decisionSeconds = 0;
        } else if (conservative <= MOVE_WITHIN_S) {
          urgency = "move";
          decisionSeconds = Math.floor(conservative - leadS);
        } else {
          urgency = "watch";
          decisionSeconds = Math.floor(conservative - leadS);
        }
      } else if (!approaching && miss <= OVERHEAD_M) {
        reason = "trajectory";
        openWindow = true;
        urgency = "shelter_now";
        decisionSeconds = 0;
        timeToClosest = 0;
      } else if (!approaching && outward > 0) {
        reason = "receding";
      } else {
        reason = "wide_miss";
      }
      for (let i = 0; i < track.fixes.length; i += 1) {
        const fix = track.fixes[i];
        const plotted = point(fix.east_m, fix.north_m, originLat, originLon);
        plotted.t = fix.t;
        plotted.estimated = false;
        trackPoints.push(plotted);
      }
      if (clockEstimated) {
        const tip = point(east, north, originLat, originLon);
        tip.t = track.t + extrapolatedS;
        tip.estimated = true;
        trackPoints.push(tip);
      }
    } else if (placed) {
      east = placed.east_m;
      north = placed.north_m;
      uncertaintyM = placed.uncertainty_m;
      where = whereText(east, north, uncertaintyM > APPROX_WHEN_M);
      threat = point(east, north, originLat, originLon);
      threat.uncertainty_m = uncertaintyM;
    }

    if (!threat && recent.length) where = "heard, not placed yet";
    let rmse;
    if (track) rmse = rmseReport(track.rmse_m, east, north, track.aimers, extrapolatedS);
    else if (placed) rmse = rmseReport(placed.rmse_m, east, north, placed.aimers, 0);
    else rmse = rmseReport(null, null, null, [], 0);
    const guidanceText = guidance(reason, urgency, decisionSeconds, where);
    let commsNote;
    if (comms === "down" && (threat || recent.length)) {
      commsNote = "No new cue. Showing the last listeners on hand. No server required.";
    } else if (comms === "local" && recent.length) {
      commsNote = "Built from listeners on hand. No server required.";
    } else {
      commsNote = "No server required.";
    }

    let lockT = null;
    let sharedFix = false;
    if (track) {
      lockT = track.t;
      sharedFix = true;
    } else if (placed) {
      lockT = placed.t;
      sharedFix = true;
    } else if (heardBy.length && newestT != null) {
      lockT = newestT;
    }
    const lit = [];
    for (let i = 0; i < listeners.length; i += 1) {
      const item = listeners[i];
      const coherent =
        lockT != null && item.last_score >= MIN_SCORE && Math.abs(item.last_t - lockT) <= BIN_S;
      item.coherent = coherent;
      if (coherent) lit.push(item.node_id);
    }
    let coherenceState = "quiet";
    let coherenceLabel = "Field quiet";
    if (sharedFix && lit.length >= 2) {
      coherenceState = "locked";
      coherenceLabel = "Field locked";
    } else if (lit.length) {
      coherenceState = "partial";
      coherenceLabel = "Field partial";
    }
    const coherence = {
      state: coherenceState,
      value: listeners.length ? lit.length / listeners.length : 0,
      lit: lit,
      label: coherenceLabel,
    };

    const label = (state.protected && state.protected.label) || "protected point";
    const layers = [
      {
        type: "protected",
        lat: originLat,
        lon: originLon,
        east_m: 0,
        north_m: 0,
        label: label,
      },
    ];
    for (let i = 0; i < listeners.length; i += 1) {
      const item = listeners[i];
      if (item.azimuth_deg != null && !threat) {
        layers.push({
          type: "bearing",
          node_id: item.node_id,
          east_m: item.east_m,
          north_m: item.north_m,
          azimuth_deg: item.azimuth_deg,
          length_m: 1500,
        });
      }
      const layer = {
        type: "listener",
        node_id: item.node_id,
        kind: item.kind,
        lat: item.lat,
        lon: item.lon,
        east_m: item.east_m,
        north_m: item.north_m,
        coherent: Boolean(item.coherent),
      };
      layers.push(layer);
    }
    if (trackPoints.length) layers.push({ type: "track", points: trackPoints });
    if (threat) {
      layers.push({
        type: "threat",
        lat: threat.lat,
        lon: threat.lon,
        east_m: threat.east_m,
        north_m: threat.north_m,
        uncertainty_m: threat.uncertainty_m,
      });
    }
    if (openWindow) layers.push({ type: "decision", seconds: decisionSeconds, urgency: urgency });

    let contact = null;
    if (recent.length) {
      contact = { visible: true, placed: Boolean(threat), heard_by: heardBy, where: where };
      if (threat) {
        contact.lat = threat.lat;
        contact.lon = threat.lon;
        contact.east_m = threat.east_m;
        contact.north_m = threat.north_m;
        contact.uncertainty_m = threat.uncertainty_m;
      }
    }

    return {
      system: "omen-decision-window",
      version: 1,
      community_id: state.community_id || "",
      alert_id: state.alert_id || "",
      listening: listening,
      opened_by: state.opened_by == null ? null : state.opened_by,
      comms: comms,
      stale: stale,
      comms_note: commsNote,
      generated_at: now,
      protected: { lat: originLat, lon: originLon, label: label },
      omen: {
        open: openWindow,
        reason: reason,
        urgency: urgency,
        time_to_closest_s: timeToClosest,
        time_uncertainty_s: timeUncertainty,
        decision_seconds: decisionSeconds,
        lead_s: leadS,
        where: where,
        threat: threat,
        track: trackPoints,
        heading_deg: heading,
        speed_m_s: speed,
        extrapolated_s: extrapolatedS,
        clock_estimated: clockEstimated,
        guidance: guidanceText,
      },
      coherence: coherence,
      rmse: rmse,
      contact: contact,
      listeners: listeners,
      systems: systems,
      layers: layers,
    };
  }

  const PRESETS = {
    inside: "Inside",
    hear: "I hear it",
    quiet: "I don't hear it",
    clear: "Clear here",
  };

  function smartText(picture) {
    const omen = (picture && picture.omen) || {};
    const field = (picture && picture.coherence && picture.coherence.state) || "quiet";
    const rmse = (picture && picture.rmse) || {};
    let text;
    if (omen.open && omen.decision_seconds != null) {
      text = omen.decision_seconds + "s · " + (omen.where || "unplaced") + " · field " + field;
    } else if (omen.where && omen.where !== "no contact") {
      text = omen.where + " · field " + field;
    } else {
      text = "field " + field;
    }
    if (rmse.try_plate && rmse.label) return text + " · " + rmse.label;
    return text;
  }

  function makeFieldNote(nodeId, t, text, preset, noteId) {
    let compact = String(text).replace(/\s+/g, " ").trim();
    if (compact.length > 160) compact = compact.slice(0, 157) + "...";
    return {
      type: "omen.field_note",
      id: noteId || preset + ":" + nodeId + ":" + Number(t).toFixed(3),
      node_id: String(nodeId),
      t: Number(t),
      text: compact,
      preset: preset,
      status: "sent",
    };
  }

  function smartFieldNote(picture, nodeId, t, noteId) {
    return makeFieldNote(nodeId, t, smartText(picture), "smart", noteId);
  }

  function presetFieldNote(preset, nodeId, t, noteId) {
    if (!Object.prototype.hasOwnProperty.call(PRESETS, preset)) {
      throw new Error("unknown field note preset: " + preset);
    }
    return makeFieldNote(nodeId, t, PRESETS[preset], preset, noteId);
  }

  function observationKey(obs) {
    const azimuth = obs.azimuth_deg == null ? "" : Number(obs.azimuth_deg).toFixed(2);
    return [obs.node_id || "", Number(obs.t).toFixed(3), azimuth, Number(obs.score || 0).toFixed(3)].join("|");
  }

  function normalizeObservation(raw) {
    const lat = Number(raw.lat);
    const lon = Number(raw.lon);
    if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
      throw new Error("observation lat/lon out of range");
    }
    let score = Number(raw.score);
    if (score < 0) score = 0;
    else if (score > 1) score = 1;
    const normalized = {
      node_id: String(raw.node_id),
      kind: String(raw.kind || "phone"),
      t: Number(raw.t),
      lat: lat,
      lon: lon,
      score: score,
      azimuth_deg: raw.azimuth_deg == null ? null : mod(Number(raw.azimuth_deg), 360),
      alert_id: String(raw.alert_id || ""),
      community_id: String(raw.community_id || ""),
    };
    if (raw.alt_m != null) normalized.alt_m = Number(raw.alt_m);
    if (raw.azimuth_sigma_deg != null) normalized.azimuth_sigma_deg = Number(raw.azimuth_sigma_deg);
    if (raw.fundamental_hz != null) normalized.fundamental_hz = Number(raw.fundamental_hz);
    return normalized;
  }

  function mergeBundles(bundles, options) {
    const communityId = options.communityId;
    const alertId = options.alertId || "";
    const token = options.communityToken;
    const merged = {};
    for (let b = 0; b < bundles.length; b += 1) {
      const bundle = bundles[b];
      if (!bundle || typeof bundle !== "object") continue;
      if (bundle.type != null && bundle.type !== "omen.bundle") continue;
      if (bundle.community_id && bundle.community_id !== communityId) continue;
      const bundleAlert = String(bundle.alert_id || "");
      if (alertId && bundleAlert && bundleAlert !== alertId) continue;
      if (token != null && bundle.community_token !== token) continue;
      const observations = bundle.observations || [];
      for (let i = 0; i < observations.length; i += 1) {
        let obs;
        try {
          obs = normalizeObservation(observations[i]);
        } catch (err) {
          continue;
        }
        if (obs.community_id && obs.community_id !== communityId) continue;
        if (alertId && obs.alert_id && obs.alert_id !== alertId) continue;
        obs.community_id = communityId;
        if (alertId) obs.alert_id = alertId;
        merged[observationKey(obs)] = obs;
      }
    }
    return Object.keys(merged)
      .sort()
      .map(function (key) {
        return merged[key];
      });
  }

  return {
    rotorCue: rotorCue,
    azimuthFromPair: azimuthFromPair,
    buildPicture: buildPicture,
    mergeBundles: mergeBundles,
    smartFieldNote: smartFieldNote,
    presetFieldNote: presetFieldNote,
    PRESETS: PRESETS,
    MIN_SCORE: MIN_SCORE,
    OVERHEAD_M: OVERHEAD_M,
  };
});
