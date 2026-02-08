from __future__ import annotations

import numpy as np

from ..dsp import amplitude, timebase


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    amp = amplitude(volume)
    t = timebase(sample_rate, duration_s)
    wave = np.sin(2.0 * np.pi * freq * t)

    # Original behavior: ceil-based shaping (harsh pulse-ish square).
    wave = np.ceil(wave)
    wave -= 0.5
    wave *= 2.0
    wave *= amp

    return wave
