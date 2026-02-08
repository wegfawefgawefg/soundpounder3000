from __future__ import annotations

import numpy as np

from ..dsp import amplitude, apply_ramp, timebase


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    amp = amplitude(volume)
    t = timebase(sample_rate, duration_s)

    # Naive saw: 2 * frac(f*t) - 1
    phase = (freq * t) % 1.0
    wave = amp * (2.0 * phase - 1.0)
    return apply_ramp(wave, parts=int(params.get("ramp", 20) or 20))
