"""One community's listener.

A wearable sends a listen message. Phones that are awake record rotor cues.
Tree-top boxes and other phones send the same observation JSON. The session
merges whatever bundles are on hand and asks the decision window for a picture.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from omen_listener.detect import azimuth_from_pair, rotor_cue
from omen_listener.mesh import make_bundle, merge_bundles, normalize_observation, observation_key
from omen_listener.picture import build_picture


@dataclass(frozen=True)
class GeoPoint:
    lat: float
    lon: float
    alt_m: float = 0.0


class ListenerSession:
    def __init__(
        self,
        community_id: str,
        protected: GeoPoint,
        *,
        lead_s: float = 30.0,
        watch_radius_m: float = 1000.0,
        community_token: str | None = None,
        label: str = "protected point",
    ) -> None:
        self.community_id = community_id
        self.protected = protected
        self.lead_s = lead_s
        self.watch_radius_m = watch_radius_m
        self.community_token = community_token
        self.label = label
        self.alert_id = ""
        self.opened_by: str | None = None
        self._listen_until: float | None = None
        self._observations: list[dict[str, Any]] = []

    def listening(self, now: float) -> bool:
        return self._listen_until is not None and now <= self._listen_until

    def apply_wake(self, wake: dict[str, Any], now: float) -> bool:
        """Open or close this phone's microphone. Returns whether it is listening."""
        if str(wake.get("community_id") or "") != self.community_id:
            return self.listening(now)
        if self.community_token is not None and wake.get("community_token") != self.community_token:
            return self.listening(now)
        command = wake.get("command")
        if command == "stop":
            self._listen_until = None
            return False
        if command != "listen":
            return self.listening(now)
        alert_id = str(wake.get("alert_id") or "")
        if alert_id and alert_id != self.alert_id:
            self.alert_id = alert_id
            self._observations = []
        issued = float(wake["issued_at"])
        ttl = float(wake.get("ttl_s", 600.0))
        self._listen_until = issued + ttl
        self.opened_by = str(wake.get("source") or "wearable")
        return self.listening(now)

    def ingest_pcm(
        self,
        node: dict[str, Any],
        samples: list[float],
        sample_rate: float,
        t: float,
        *,
        azimuth_deg: float | None = None,
        array: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Score one microphone frame. Ignored unless a listen message is active."""
        if not self.listening(t):
            return None
        cue = rotor_cue(samples, sample_rate)
        if not cue.detected:
            return None
        bearing = azimuth_deg
        if array is not None:
            measured = azimuth_from_pair(
                array["left"],
                array["right"],
                sample_rate,
                float(array["spacing_m"]),
                float(array["heading_deg"]),
            )
            if measured is not None:
                bearing = measured
        raw = {
            "node_id": node["node_id"],
            "kind": node.get("kind", "phone"),
            "t": t,
            "lat": node["lat"],
            "lon": node["lon"],
            "score": cue.score,
            "azimuth_deg": bearing,
            "alert_id": self.alert_id,
            "community_id": self.community_id,
            "fundamental_hz": cue.fundamental_hz,
        }
        if node.get("alt_m") is not None:
            raw["alt_m"] = node["alt_m"]
        if node.get("azimuth_sigma_deg") is not None and "azimuth_sigma_deg" not in raw:
            raw["azimuth_sigma_deg"] = node["azimuth_sigma_deg"]
        if not self.ingest_observation(raw):
            return None
        wanted = observation_key(normalize_observation(raw))
        for obs in self._observations:
            if observation_key(obs) == wanted:
                return obs
        return None

    def ingest_observation(self, raw: dict[str, Any]) -> bool:
        """Accept a cue another system already computed. No microphone required."""
        if str(raw.get("community_id") or self.community_id) != self.community_id:
            return False
        if self.community_token is not None and raw.get("community_token") not in (
            None,
            "",
            self.community_token,
        ):
            return False
        try:
            obs = normalize_observation(raw)
        except (KeyError, TypeError, ValueError):
            return False
        if obs["community_id"] not in ("", self.community_id):
            return False
        incoming_alert = obs["alert_id"]
        if self.alert_id and incoming_alert not in ("", self.alert_id):
            return False
        if not self.alert_id and incoming_alert:
            self.alert_id = incoming_alert
        obs["community_id"] = self.community_id
        if self.alert_id:
            obs["alert_id"] = self.alert_id
        self._observations = merge_bundles(
            [
                self._local_bundle(),
                {"type": "omen.bundle", "community_id": self.community_id, "alert_id": self.alert_id, "observations": [obs]},
            ],
            community_id=self.community_id,
            alert_id=self.alert_id,
            community_token=None,
        )
        return True

    def ingest_bundle(self, bundle: dict[str, Any]) -> int:
        before = len(self._observations)
        if self.community_token is not None and bundle.get("community_token") != self.community_token:
            return 0
        incoming_alert = str(bundle.get("alert_id") or "")
        if not self.alert_id and incoming_alert:
            self.alert_id = incoming_alert
        self._observations = merge_bundles(
            [self._local_bundle(), bundle],
            community_id=self.community_id,
            alert_id=self.alert_id,
            community_token=self.community_token,
        )
        return max(0, len(self._observations) - before)

    def export_bundle(self, origin_id: str, now: float) -> dict[str, Any]:
        return make_bundle(
            community_id=self.community_id,
            alert_id=self.alert_id,
            origin_id=origin_id,
            sent_at=now,
            observations=list(self._observations),
            community_token=self.community_token,
        )

    def state(self, now: float) -> dict[str, Any]:
        return {
            "version": 1,
            "community_id": self.community_id,
            "alert_id": self.alert_id,
            "protected": {
                "lat": self.protected.lat,
                "lon": self.protected.lon,
                "label": self.label,
            },
            "lead_s": self.lead_s,
            "watch_radius_m": self.watch_radius_m,
            "now": now,
            "listening": self.listening(now),
            "opened_by": self.opened_by,
            "observations": list(self._observations),
        }

    def picture(self, now: float) -> dict[str, Any]:
        return build_picture(self.state(now))

    def _local_bundle(self) -> dict[str, Any]:
        return {
            "type": "omen.bundle",
            "community_id": self.community_id,
            "alert_id": self.alert_id,
            "observations": list(self._observations),
            "community_token": self.community_token,
        }
