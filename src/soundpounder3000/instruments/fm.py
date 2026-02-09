from __future__ import annotations

import numpy as np

from ..dsp import amplitude, timebase


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    amp = amplitude(volume)
    t = timebase(sample_rate, duration_s)

    # Simple 2-op FM.
    # car/mod are frequency ratios; idx controls modulation index.
    car = params.get("car", 1.0)
    mod = params.get("mod", 2.0)
    idx = params.get("idx", 2.0)

    try:
        car_f = float(car)  # type: ignore[arg-type]
    except Exception:
        car_f = 1.0
    try:
        mod_f = float(mod)  # type: ignore[arg-type]
    except Exception:
        mod_f = 2.0
    try:
        idx_f = float(idx)  # type: ignore[arg-type]
    except Exception:
        idx_f = 2.0

    # Modulator
    mod_wave = np.sin(2.0 * np.pi * (freq * mod_f) * t)
    wave = np.sin(2.0 * np.pi * (freq * car_f) * t + idx_f * mod_wave)
    return amp * wave
