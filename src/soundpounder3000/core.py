import math
import os
import wave
from pathlib import Path

import numpy as np

from .parse import parse_song
from .settings import SAMPLE_RATE


def _write_wav_pcm16_mono(path: str, sample_rate: int, data: np.ndarray) -> None:
    data_i16 = np.asarray(data, dtype=np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(data_i16.tobytes())

def apply_ramp(waveform, duration=20):
    ramp_duration = int(waveform.shape[0] / duration)

    ramp_up = np.linspace(0, 1.0, ramp_duration)
    ramp_down = np.linspace(1.0, 0, ramp_duration)
    
    ramp_up_indices = np.arange(ramp_duration, dtype=np.int64)
    waveform[ramp_up_indices] *= ramp_up[ramp_up_indices]

    ramp_down_indices = np.arange(ramp_duration, dtype=np.int64) - ramp_duration
    waveform[ramp_down_indices] *= ramp_down[ramp_up_indices]

    return waveform

def gen_waveform(freq, duration, volume, instrument='sine'):
    if instrument == 'sine':
        return gen_soft_sinwave(freq, duration, volume)
    elif instrument == 'square':
        return gen_squarewave(freq, duration, volume)
    elif instrument == 'noise':
        return gen_noise(freq, duration, volume)
    elif instrument == 'string':
        return gen_string(freq, duration, volume)
    else:
        return gen_soft_sinwave(freq, duration, volume)

def gen_soft_sinwave(freq, duration, volume, ramp=True):
    amplitude = 4096 * volume
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    if ramp:
        apply_ramp(wave)
    return wave

def gen_squarewave(freq, duration, volume, ramp=True):
    amplitude = 4096 * volume
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples)
    wave = np.sin(2 * np.pi * freq * t)
    #   convert to square wave
    wave = np.ceil(wave)    # ceil the wave to get half duty cycle
    wave -= 0.5             # you lost the lower half of the wave, so shift it down
    wave *= 2.0             # double the wave to get full envelope
    wave *= amplitude

    if ramp:
        apply_ramp(wave, duration=10)

    return wave

def gen_noise(freq, duration, volume, ramp=True):
    amplitude = 4096 * volume
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples)
    wave = amplitude * np.random.normal(0, 1, num_samples)
    if ramp:
        apply_ramp(wave)
    return wave

def gen_string(freq, duration, volume, ramp=True):
    amplitude = 4096 * volume
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples)
    # account for harmonics
    harmonics = []
    wave = np.zeros(num_samples)
    num_harmonics = 8
    for i in range(1, num_harmonics + 1):
        di = 8.0
        frequency = freq * (float(i + di) / (di + 1))
        amp = amplitude * (1.0 / i)
        offset = 0
        wave += amp * np.sin(2 * np.pi * frequency * t + offset)
        harmonics.append((frequency, amp))
    
    # # plot the harmonics
    # # make a plot
    # xs = []
    # ys = []
    # for harmonic in harmonics:
    #     xs.append(harmonic[0])
    #     ys.append(harmonic[1])
    # plt.bar(xs, ys)
    # # make the lines thicker
    # plt.rcParams['lines.linewidth'] = 20
    # plt.show()

    wave *= np.exp(-t * 10) # attenuate the wave exponentially
    if ramp:
        apply_ramp(wave)

    # plt.plot(wave)
    # plt.show()
    return wave

def fiddle_to_wav(
    fiddle: str,
    *,
    outdir: str = "waves",
    outfile: str | None = None,
    default_title: str = "Untitled",
) -> str:
    title, tones = parse_song(fiddle, default_title=default_title)

    # tones.sort(key=lambda tone: tone.time, reverse=False)
    last_tone = tones[-1]
    song_length_seconds = int(math.ceil(last_tone.time + last_tone.duration)) 
    song_length_samples = (song_length_seconds + 1) * SAMPLE_RATE
    base = np.zeros(song_length_samples)

    for tone in tones:
        waveform = gen_waveform(tone.note.get_freq(), tone.duration, tone.volume, 
            tone.instrument
            # "string"
        )
        # plt.plot(waveform)
        # plt.show()

        time_seconds = tone.time
        time_samples = int(time_seconds * SAMPLE_RATE)

        # duration_time = tone.duration
        # duration_samples = int(tone.duration * settings.SAMPLE_RATE)

        waveform_indices = np.arange(waveform.shape[0], dtype=np.int64)
        base_indices = waveform_indices + time_samples
        base[base_indices] += waveform[waveform_indices]

    if outfile is None:
        out_path = Path(outdir) / f"{title}.wav"
    else:
        p = Path(outfile)
        # If given a directory (or a path with no suffix), write `<title>.wav` inside it.
        if (p.exists() and p.is_dir()) or (p.suffix == "" and str(outfile).endswith(os.sep)):
            out_path = p / f"{title}.wav"
        elif p.suffix == "":
            out_path = p / f"{title}.wav"
        else:
            out_path = p

    out_path.parent.mkdir(parents=True, exist_ok=True)
    _write_wav_pcm16_mono(str(out_path), SAMPLE_RATE, base)
    return title
