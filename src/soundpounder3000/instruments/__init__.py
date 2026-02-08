from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from . import noise, pulse, saw, sine, square, string, triangle


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
}


def get(name: str) -> Instrument:
    return _REGISTRY.get(name, _REGISTRY["sine"])


def render(name: str, freq: float, duration_s: float, volume: float, sample_rate: int, params: dict[str, object] | None = None) -> np.ndarray:
    inst = get(name)
    return inst.render(freq, duration_s, volume, sample_rate, params or {})

