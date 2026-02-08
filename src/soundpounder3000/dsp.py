from __future__ import annotations

import math
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
    # Use endpoint=False to avoid duplicating the final sample at `duration_s`.
    return np.linspace(0.0, duration_s, n, endpoint=False, dtype=np.float64)


def amplitude(volume: float) -> float:
    # Historic choice from the original script.
    return 4096.0 * float(volume)


def adsr_envelope(
    duration_s: float,
    sample_rate: int,
    *,
    atk: float = 0.005,
    dec: float = 0.0,
    sus: float = 1.0,
    rel: float = 0.02,
) -> np.ndarray:
    """
    Simple ADSR envelope.

    Times are in seconds. Sustain is a linear level in [0, 1].
    If atk+dec+rel exceeds duration, the stages are proportionally scaled to fit.
    """
    n = int(sample_rate * duration_s)
    if n <= 0:
        return np.zeros(0, dtype=np.float64)

    atk = max(0.0, float(atk))
    dec = max(0.0, float(dec))
    rel = max(0.0, float(rel))
    sus = float(sus)
    if math.isnan(sus) or math.isinf(sus):
        sus = 1.0
    sus = max(0.0, min(1.0, sus))

    total = atk + dec + rel
    if total > duration_s and total > 0.0:
        scale = duration_s / total
        atk *= scale
        dec *= scale
        rel *= scale

    a_n = int(round(atk * sample_rate))
    d_n = int(round(dec * sample_rate))
    r_n = int(round(rel * sample_rate))
    # Ensure we don't exceed n.
    if a_n + d_n + r_n > n:
        overflow = (a_n + d_n + r_n) - n
        # Trim release first, then decay, then attack.
        trim = min(overflow, r_n)
        r_n -= trim
        overflow -= trim
        trim = min(overflow, d_n)
        d_n -= trim
        overflow -= trim
        trim = min(overflow, a_n)
        a_n -= trim

    s_n = n - (a_n + d_n + r_n)

    env = np.empty(n, dtype=np.float64)
    idx = 0
    if a_n > 0:
        env[idx : idx + a_n] = np.linspace(0.0, 1.0, a_n, endpoint=False, dtype=np.float64)
        idx += a_n
    if d_n > 0:
        env[idx : idx + d_n] = np.linspace(1.0, sus, d_n, endpoint=False, dtype=np.float64)
        idx += d_n
    if s_n > 0:
        env[idx : idx + s_n] = sus
        idx += s_n
    if r_n > 0:
        # Release starts from the current level (sus if we had sustain).
        start = sus if (s_n > 0 or d_n > 0) else 1.0 if a_n > 0 else 0.0
        env[idx : idx + r_n] = np.linspace(start, 0.0, r_n, endpoint=True, dtype=np.float64)
        idx += r_n

    if idx < n:
        env[idx:] = 0.0

    return env


def lowpass_1p(waveform: np.ndarray, cutoff_hz: float | np.ndarray, sample_rate: int) -> np.ndarray:
    """
    One-pole lowpass filter.

    `cutoff_hz` can be a scalar or per-sample array. Returns a new array.
    """
    x = np.asarray(waveform, dtype=np.float64)
    n = x.shape[0]
    if n == 0:
        return x

    if np.isscalar(cutoff_hz):
        fc = float(cutoff_hz)  # type: ignore[arg-type]
        if not (fc > 0.0):
            return x
        a = 1.0 - math.exp(-2.0 * math.pi * fc / float(sample_rate))
        y = np.empty_like(x)
        y0 = 0.0
        for i in range(n):
            y0 = y0 + a * (x[i] - y0)
            y[i] = y0
        return y

    fc_arr = np.asarray(cutoff_hz, dtype=np.float64)
    if fc_arr.shape[0] != n:
        raise ValueError("cutoff_hz array length must match waveform length")
    # Clamp to sane range to avoid NaNs / instability.
    fc_arr = np.clip(fc_arr, 20.0, float(sample_rate) * 0.45)
    a_arr = 1.0 - np.exp(-2.0 * math.pi * fc_arr / float(sample_rate))

    y = np.empty_like(x)
    y0 = 0.0
    for i in range(n):
        a = float(a_arr[i])
        y0 = y0 + a * (x[i] - y0)
        y[i] = y0
    return y
