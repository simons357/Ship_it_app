#!/usr/bin/env python3
"""
Build data/qnm_events.csv for HB Ringdown Experiment 01.

Rows mix:
  1) published agnostic/mode-labeled ringdown measurements
  2) Kerr-fit modes from published remnant (M, chi) using Berti et al. fits

This is a starting catalog for the pipeline. Replace with posterior samples
and a GR-informed null before publication-grade claims.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

MSUN_SECONDS = 4.925490947e-6

# Berti, Cardoso, Willard / Berti et al. fitting coefficients for M*omega_R and Q.
# Q = omega_R / (2 omega_I). Source: standard BH spectroscopy fits (l=m fundamentals + 221).
BERTI = {
    "220": dict(f1=1.5251, f2=-1.1568, f3=0.1292, q1=0.7000, q2=1.4187, q3=-0.4990),
    "221": dict(f1=1.3506, f2=-1.2018, f3=0.1840, q1=0.1828, q2=1.1960, q3=-0.4217),
    "330": dict(f1=1.8956, f2=-1.3043, f3=0.0927, q1=0.9000, q2=2.3430, q3=-0.4810),
    "210": dict(f1=0.6000, f2=-0.2339, f3=0.4173, q1=0.1290, q2=0.2840, q3=-0.5170),
    "440": dict(f1=2.3000, f2=-1.5056, f3=0.1144, q1=1.1030, q2=3.1260, q3=-0.4810),
}


def kerr_mode(mode: str, chi: float) -> tuple[float, float]:
    c = BERTI[mode]
    one = max(1.0e-12, 1.0 - chi)
    m_omega_r = c["f1"] + c["f2"] * (one ** c["f3"])
    q = c["q1"] + c["q2"] * (one ** c["q3"])
    m_omega_i = m_omega_r / (2.0 * q)
    return m_omega_r, m_omega_i


def to_f_tau(m_msun: float, m_omega_r: float, m_omega_i: float) -> tuple[float, float]:
    m = m_msun * MSUN_SECONDS
    omega_r = m_omega_r / m
    omega_i = m_omega_i / m
    f_hz = omega_r / (2.0 * math.pi)
    tau_ms = 1000.0 / omega_i
    return f_hz, tau_ms


# Published remnant parameters (detector-frame / redshifted mass where noted).
# Splits frozen before TEST evaluation.
EVENTS = [
    # TRAIN
    dict(
        event_id="GW150914",
        split="train",
        M_msun=68.2,
        chi=0.67,
        modes=("220", "221", "330"),
        provenance="kerr_fit_from_LVC_remnant",
        reference="Abbott+2016 GW150914; remnant approx. from IMR",
    ),
    dict(
        event_id="GW170104",
        split="train",
        M_msun=51.0,
        chi=0.64,
        modes=("220", "221", "330"),
        provenance="kerr_fit_from_LVC_remnant",
        reference="Abbott+2017 GW170104",
    ),
    dict(
        event_id="GW190521",
        split="train",
        M_msun=330.0,
        chi=0.86,
        modes=None,  # measured rows added separately
        provenance="measured_capano2021",
        reference="Capano+2021 arXiv:2105.05238",
    ),
    # TEST
    dict(
        event_id="GW190412",
        split="test",
        M_msun=38.5,
        chi=0.67,
        modes=("220", "221", "330"),
        provenance="kerr_fit_from_LVC_remnant",
        reference="Abbott+2020 GW190412",
    ),
    dict(
        event_id="GW190814",
        split="test",
        M_msun=25.7,
        chi=0.28,
        modes=("220", "221", "330"),
        provenance="kerr_fit_from_LVC_remnant",
        reference="Abbott+2020 GW190814",
    ),
    dict(
        event_id="GW200129",
        split="test",
        M_msun=63.0,
        chi=0.70,
        modes=("220", "221", "330"),
        provenance="kerr_fit_from_LVC_remnant",
        reference="Abbott+2021/2023 GWTC-3 remnant approx.",
    ),
]


def measured_rows() -> list[dict]:
    # Capano et al. agnostic QNM search at t_ref+6ms
    return [
        dict(
            event_id="GW190521",
            mode="220",
            f_Hz=63.0,
            f_Hz_err=2.0,
            tau_ms=26.0,
            tau_ms_err_plus=8.0,
            tau_ms_err_minus=6.0,
            M_msun=330.0,
            chi=0.86,
            split="train",
            provenance="measured_capano2021",
            reference="Capano+2021 arXiv:2105.05238",
        ),
        dict(
            event_id="GW190521",
            mode="330",
            f_Hz=98.0,
            f_Hz_err_plus=89.0,
            f_Hz_err_minus=7.0,
            tau_ms=40.0,
            tau_ms_err_plus=50.0,
            tau_ms_err_minus=30.0,
            M_msun=330.0,
            chi=0.86,
            split="train",
            provenance="measured_capano2021",
            reference="Capano+2021 arXiv:2105.05238",
        ),
    ]


def main() -> None:
    rows: list[dict] = []
    rows.extend(measured_rows())
    for ev in EVENTS:
        if ev["modes"] is None:
            continue
        for mode in ev["modes"]:
            mor, moi = kerr_mode(mode, ev["chi"])
            f_hz, tau_ms = to_f_tau(ev["M_msun"], mor, moi)
            # Fractional uncertainty proxy (~3%) for pipeline exercises only
            rows.append(
                dict(
                    event_id=ev["event_id"],
                    mode=mode,
                    f_Hz=round(f_hz, 6),
                    f_Hz_err=round(0.03 * f_hz, 6),
                    tau_ms=round(tau_ms, 6),
                    tau_ms_err=round(0.05 * tau_ms, 6),
                    M_msun=ev["M_msun"],
                    chi=ev["chi"],
                    M_omega_R=round(mor, 8),
                    M_omega_I=round(moi, 8),
                    split=ev["split"],
                    provenance=ev["provenance"],
                    reference=ev["reference"],
                )
            )

    out = Path(__file__).resolve().parents[1] / "data" / "qnm_events.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "event_id",
        "mode",
        "f_Hz",
        "f_Hz_err",
        "f_Hz_err_plus",
        "f_Hz_err_minus",
        "tau_ms",
        "tau_ms_err",
        "tau_ms_err_plus",
        "tau_ms_err_minus",
        "M_msun",
        "chi",
        "M_omega_R",
        "M_omega_I",
        "split",
        "provenance",
        "reference",
    ]
    with out.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
