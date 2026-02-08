from __future__ import annotations

import numpy as np

from ..dsp import amplitude, timebase


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    amp = amplitude(volume)
    t = timebase(sample_rate, duration_s)

    # Triangle from phase: 1 - 4*abs(frac - 0.5)
    phase = (freq * t) % 1.0
    tri = 1.0 - 4.0 * np.abs(phase - 0.5)
    wave = amp * tri
    return wave
