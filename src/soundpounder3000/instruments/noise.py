from __future__ import annotations

import numpy as np

from ..dsp import amplitude, timebase


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    # freq unused; kept for uniform signature.
    _ = freq
    amp = amplitude(volume)
    t = timebase(sample_rate, duration_s)
    wave = amp * np.random.normal(0.0, 1.0, t.shape[0])
    return wave
