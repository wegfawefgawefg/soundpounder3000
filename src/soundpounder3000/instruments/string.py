from __future__ import annotations

import numpy as np

from ..dsp import amplitude, timebase


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    amp = amplitude(volume)
    t = timebase(sample_rate, duration_s)

    wave = np.zeros(t.shape[0], dtype=np.float64)
    num_harmonics = int(params.get("harmonics", 8) or 8)

    # Original behavior: slightly detuned harmonic series (via `di`) + exp decay.
    di = float(params.get("detune", 8.0) or 8.0)
    for i in range(1, num_harmonics + 1):
        frequency = freq * (float(i + di) / (di + 1.0))
        wave += (amp * (1.0 / i)) * np.sin(2.0 * np.pi * frequency * t)

    decay = float(params.get("decay", 10.0) or 10.0)
    wave *= np.exp(-t * decay)
    return wave
