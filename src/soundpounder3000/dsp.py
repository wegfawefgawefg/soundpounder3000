from __future__ import annotations

import numpy as np


def apply_ramp(waveform: np.ndarray, *, parts: int = 20) -> np.ndarray:
    # Basic fade-in/out to avoid clicks. `parts` is roughly "how much of the note is ramp".
    ramp_len = int(waveform.shape[0] / parts)
    if ramp_len <= 0:
        return waveform

    ramp_up = np.linspace(0.0, 1.0, ramp_len, dtype=np.float64)
    ramp_down = np.linspace(1.0, 0.0, ramp_len, dtype=np.float64)

    idx = np.arange(ramp_len, dtype=np.int64)
    waveform[idx] *= ramp_up[idx]
    waveform[idx - ramp_len] *= ramp_down[idx]
    return waveform


def timebase(sample_rate: int, duration_s: float) -> np.ndarray:
    n = int(sample_rate * duration_s)
    return np.linspace(0.0, duration_s, n, dtype=np.float64)


def amplitude(volume: float) -> float:
    # Historic choice from the original script.
    return 4096.0 * float(volume)

