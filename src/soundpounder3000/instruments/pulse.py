from __future__ import annotations

import numpy as np

from ..dsp import amplitude, timebase


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    amp = amplitude(volume)
    t = timebase(sample_rate, duration_s)

    pw = params.get("pw", 0.5)
    try:
        pw_f = float(pw)  # type: ignore[arg-type]
    except Exception:
        pw_f = 0.5
    pw_f = max(0.01, min(0.99, pw_f))

    phase = (freq * t) % 1.0
    wave = np.where(phase < pw_f, 1.0, -1.0) * amp
    return wave
