from __future__ import annotations

import numpy as np

from ..dsp import amplitude


def render(freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object]) -> np.ndarray:
    amp = amplitude(volume)
    n = int(sample_rate * duration_s)
    if n <= 0 or freq <= 0:
        return np.zeros(0, dtype=np.float64)

    # Karplus-Strong.
    # - decay: feedback amount per cycle (0..1). Closer to 1 rings longer.
    # - bright: mix of raw noise into the feedback path (0..1). Higher is brighter/noisier.
    # - damp: lowpass in the feedback path (0..1). Higher is darker/more damped.
    decay = params.get("decay", 0.985)
    bright = params.get("bright", 0.2)
    damp = params.get("damp", 0.2)

    try:
        decay_f = float(decay)  # type: ignore[arg-type]
    except Exception:
        decay_f = 0.985
    try:
        bright_f = float(bright)  # type: ignore[arg-type]
    except Exception:
        bright_f = 0.2
    try:
        damp_f = float(damp)  # type: ignore[arg-type]
    except Exception:
        damp_f = 0.2

    decay_f = max(0.0, min(0.9999, decay_f))
    bright_f = max(0.0, min(1.0, bright_f))
    damp_f = max(0.0, min(1.0, damp_f))

    period = max(2, int(round(sample_rate / freq)))

    # Seed buffer with noise.
    buf = np.random.uniform(-1.0, 1.0, period).astype(np.float64)
    out = np.empty(n, dtype=np.float64)

    # Simple 1-pole lowpass in feedback path.
    # a ~ 1 means follow input quickly (brighter); a small means smoother (darker).
    a = 1.0 - damp_f
    lp = 0.0

    for i in range(n):
        x = buf[i % period]
        # feedback: average adjacent samples (string dispersion-ish)
        nxt = buf[(i + 1) % period]
        fb = 0.5 * (x + nxt)
        # brightness: inject a bit of fresh noise
        fb = (1.0 - bright_f) * fb + bright_f * np.random.uniform(-1.0, 1.0)
        # damping filter
        lp = lp + a * (fb - lp)
        buf[i % period] = decay_f * lp
        out[i] = x

    return amp * out
