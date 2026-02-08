import math
import wave
from pathlib import Path

import numpy as np

from .parse import parse_song
from .settings import SAMPLE_RATE
from . import instruments


def _write_wav_pcm16_mono(path: str, sample_rate: int, data: np.ndarray) -> None:
    data_i16 = np.asarray(data, dtype=np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(data_i16.tobytes())

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
        waveform = instruments.render(
            tone.instrument_name,
            tone.note.get_freq(),
            tone.duration,
            tone.volume,
            SAMPLE_RATE,
            tone.instrument_params,
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
