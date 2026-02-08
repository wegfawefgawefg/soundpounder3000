from __future__ import annotations

import numpy as np

from ..dsp import amplitude, apply_ramp, timebase


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    amp = amplitude(volume)
    t = timebase(sample_rate, duration_s)
    wave = amp * np.sin(2.0 * np.pi * freq * t)
    return apply_ramp(wave)
