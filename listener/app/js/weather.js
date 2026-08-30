/** Field sky from this clock. Weather from YOUR app — not a stranger's. */

import { fetchOwnerWeather, ownerEndpoints } from "./plugins.js";

export function skyPeriod(date = new Date()) {
  const h = date.getHours() + date.getMinutes() / 60;
  if (h < 5 || h >= 21) return "night";
  if (h < 7) return "dawn";
  if (h < 18) return "day";
  return "dusk";
}

export function clockLabel(date = new Date()) {
  return date.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}

export function isWetLabel(label) {
  return /rain|drizzle|thunder|storm/i.test(String(label || ""));
}

/** Only your weather. If it is not plugged in, we say so. */
export async function fetchFieldWeather(lat, lon) {
  if (!ownerEndpoints().weather) return null;
  return fetchOwnerWeather(lat, lon);
}

export function weatherLine(wx, when = new Date()) {
  const sky = skyPeriod(when);
  const clock = clockLabel(when);
  if (!ownerEndpoints().weather) {
    return `${clock} · ${sky} · your weather not connected`;
  }
  if (!wx) return `${clock} · ${sky} · waiting on your weather`;
  const temp = wx.tempC == null ? "" : ` · ${Math.round(wx.tempC)}°`;
  return `${clock} · ${sky} · ${wx.label}${temp}`;
}
