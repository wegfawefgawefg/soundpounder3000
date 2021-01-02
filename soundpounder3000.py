import math
import os

import numpy as np
from pprint import pprint
from scipy.io.wavfile import write

from parse import parse_song
from settings import SAMPLE_RATE
import settings

def gen_waveform(freq, duration=0.5, volume=1.0, ramp=True):
    amplitude = 4096 * volume
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, num_samples)
    wave = amplitude * np.sin(2 * np.pi * freq * t)

    if ramp:
        ramp_duration = num_samples / 20

        ramp_up = np.linspace(0, 1, ramp_duration)
        ramp_down = np.linspace(1, 0, ramp_duration)

        ramp_up_indices = np.arange(ramp_duration - 1, dtype=np.int64)
        wave[ramp_up_indices] *= ramp_up[ramp_up_indices]

        ramp_down_indices = np.arange(ramp_duration - 1, dtype=np.int64) + int(0.95 * num_samples) + 1
        wave[ramp_down_indices] *= ramp_down[ramp_up_indices]

    return wave

def fiddle_to_wav(fiddle):
    title, tones = parse_song(fiddle)
    pprint(tones)

    last_tone = tones[-1]
    song_length_seconds = int(math.ceil(last_tone.time + last_tone.duration)) 
    song_length_samples = (song_length_seconds + 1) * settings.SAMPLE_RATE 
    base = np.zeros(song_length_samples)

    for tone in tones:
        waveform = gen_waveform(tone.note.get_freq(), tone.duration, tone.volume)

        time_seconds = tone.time
        time_samples = int(time_seconds * settings.SAMPLE_RATE)

        # duration_time = tone.duration
        # duration_samples = int(tone.duration * settings.SAMPLE_RATE)

        waveform_indices = np.arange(waveform.shape[0], dtype=np.int64)
        base_indices = waveform_indices + time_samples
        base[base_indices] += waveform[waveform_indices]

    write(os.path.join("waves/", title + '.wav'), SAMPLE_RATE, base.astype(np.int16))