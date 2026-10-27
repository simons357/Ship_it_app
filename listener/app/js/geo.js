export function gpsQuality(accuracy) {
  if (!Number.isFinite(accuracy)) return "unknown";
  if (accuracy <= 15) return "good";
  if (accuracy <= 40) return "fair";
  return "fading";
}

export function bearingDeg(from, to) {
  if (!from || !to) return null;
  const φ1 = (from.lat * Math.PI) / 180;
  const φ2 = (to.lat * Math.PI) / 180;
  const Δλ = ((to.lon - from.lon) * Math.PI) / 180;
  const y = Math.sin(Δλ) * Math.cos(φ2);
  const x = Math.cos(φ1) * Math.sin(φ2) - Math.sin(φ1) * Math.cos(φ2) * Math.cos(Δλ);
  return (Math.atan2(y, x) * 180) / Math.PI;
}

export function distanceM(from, to) {
  if (!from || !to) return null;
  const R = 6371000;
  const φ1 = (from.lat * Math.PI) / 180;
  const φ2 = (to.lat * Math.PI) / 180;
  const Δφ = ((to.lat - from.lat) * Math.PI) / 180;
  const Δλ = ((to.lon - from.lon) * Math.PI) / 180;
  const a = Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2;
  return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export function projectRelative(start, point, spanM = 120) {
  if (!start || !point || start.lat == null || point.lat == null) return null;
  const dx = distanceM(start, { lat: start.lat, lon: point.lon }) || 0;
  const dy = distanceM(start, { lat: point.lat, lon: start.lon }) || 0;
  const sx = point.lon >= start.lon ? 1 : -1;
  const sy = point.lat >= start.lat ? -1 : 1;
  const x = 50 + ((sx * dx) / spanM) * 38;
  const y = 58 + ((sy * dy) / spanM) * 38;
  return {
    left: Math.min(92, Math.max(8, x)),
    top: Math.min(88, Math.max(16, y)),
  };
}

export function watchPosition(onFix, onFail) {
  if (!navigator.geolocation) {
    onFail?.(new Error("Location is not available on this device."));
    return () => {};
  }
  const id = navigator.geolocation.watchPosition(
    (pos) => {
      onFix({
        lat: pos.coords.latitude,
        lon: pos.coords.longitude,
        accuracy: pos.coords.accuracy,
        heading: Number.isFinite(pos.coords.heading) ? pos.coords.heading : null,
        t: pos.timestamp || Date.now(),
        quality: gpsQuality(pos.coords.accuracy),
      });
    },
    (err) => onFail?.(err),
    { enableHighAccuracy: true, maximumAge: 2000, timeout: 12000 }
  );
  return () => navigator.geolocation.clearWatch(id);
}
