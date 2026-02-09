from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from . import fm, noise, pluck, pulse, saw, sine, square, string, triangle
from ..dsp import adsr_envelope, lowpass_1p


RenderFn = Callable[[float, float, float, int, dict[str, object]], np.ndarray]


@dataclass(frozen=True)
class Instrument:
    name: str
    render: RenderFn


_REGISTRY: dict[str, Instrument] = {
    "sine": Instrument("sine", sine.render),
    "square": Instrument("square", square.render),
    "noise": Instrument("noise", noise.render),
    "string": Instrument("string", string.render),
    "saw": Instrument("saw", saw.render),
    "triangle": Instrument("triangle", triangle.render),
    "pulse": Instrument("pulse", pulse.render),
    "pluck": Instrument("pluck", pluck.render),
    "fm": Instrument("fm", fm.render),
}


def get(name: str) -> Instrument:
    return _REGISTRY.get(name, _REGISTRY["sine"])


def _f(params: dict[str, object], key: str, default: float) -> float:
    v = params.get(key, default)
    try:
        return float(v)  # type: ignore[arg-type]
    except Exception:
        return default


def render(name: str, freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object] | None = None) -> np.ndarray:
    inst = get(name)
    p = params or {}

    wave = inst.render(freq, duration_s, volume, sample_rate, p)

    # Amp envelope (ADSR). Defaults are chosen to behave like the old click-prevention ramp.
    atk = _f(p, "atk", 0.005)
    dec = _f(p, "dec", 0.0)
    sus = _f(p, "sus", 1.0)
    rel = _f(p, "rel", 0.02)
    env = adsr_envelope(duration_s, sample_rate, atk=atk, dec=dec, sus=sus, rel=rel)
    if env.shape[0] == wave.shape[0]:
        wave = wave * env

    # Optional 1-pole lowpass. Params:
    # - cut (Hz): base cutoff
    # - fenv (Hz): envelope amount (added to base cutoff)
    # - fatk/fdec/fsus/frel: filter ADSR (defaults to amp ADSR)
    cut = p.get("cut", p.get("cutoff", p.get("fcut")))
    if cut is not None:
        base = _f(p, "cut", _f(p, "cutoff", _f(p, "fcut", 0.0)))
        fenv_amt = _f(p, "fenv", 0.0)
        if fenv_amt != 0.0:
            fatk = _f(p, "fatk", atk)
            fdec = _f(p, "fdec", dec)
            fsus = _f(p, "fsus", 0.0)
            frel = _f(p, "frel", rel)
            fenv = adsr_envelope(duration_s, sample_rate, atk=fatk, dec=fdec, sus=fsus, rel=frel)
            cutoff = base + (fenv_amt * fenv)
            wave = lowpass_1p(wave, cutoff, sample_rate)
        else:
            if base > 0.0:
                wave = lowpass_1p(wave, base, sample_rate)

    return wave
