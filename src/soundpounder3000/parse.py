import math
import re
from dataclasses import dataclass

from .token_params import TokenParams
from .utils import parse_num_or_frac
from .tone import Tone
from .note import Note


@dataclass(frozen=True)
class TokenLocation:
    token: str
    index: int
    line: int
    column: int


@dataclass
class NoteEvent:
    token: str
    token_index: int
    line: int
    column: int
    start_s: float
    duration_s: float
    end_s: float
    note: str
    octave: float
    instrument_name: str
    instrument_params: dict[str, object]
    inline_comment: str


def _comment_cut_index(line: str) -> int:
    if line.lstrip().startswith("#"):
        return 0

    cut = len(line)
    for delim in ("//", ";"):
        idx = line.find(delim)
        if idx != -1:
            cut = min(cut, idx)
    idx = line.find(" #")
    if idx != -1:
        cut = min(cut, idx)
    return cut


def _strip_comments(line: str) -> str:
    # Notes use sharps like `C#`, so avoid treating `#` as an inline comment
    # delimiter. We support:
    # - `; ...` end-of-line comments
    # - `// ...` end-of-line comments
    # - `# ...` only as a full-line comment (or after whitespace as ` # ...`)
    if line.lstrip().startswith("#"):
        return ""

    s = line[:_comment_cut_index(line)]
    return s.strip()


def extract_inline_comment(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("#"):
        return stripped[1:].strip()

    idxs: list[int] = []
    for delim in ("//", ";", " #"):
        idx = line.find(delim)
        if idx != -1:
            idxs.append(idx)
    if not idxs:
        return ""

    idx = min(idxs)
    comment = line[idx:]
    if comment.startswith(" #"):
        comment = comment[1:]
    if comment.startswith("//"):
        comment = comment[2:]
    elif comment.startswith(";"):
        comment = comment[1:]
    elif comment.startswith("#"):
        comment = comment[1:]
    return comment.strip()


def tokenize_song(song_string: str) -> list[str]:
    return [t.token for t in tokenize_song_with_locations(song_string)]


def tokenize_song_with_locations(song_string: str) -> list[TokenLocation]:
    tokens: list[TokenLocation] = []
    index = 0
    for line_no, raw in enumerate(song_string.splitlines(), start=1):
        if raw.lstrip().startswith("#"):
            continue
        code = raw[:_comment_cut_index(raw)]
        for m in re.finditer(r"\S+", code):
            tokens.append(
                TokenLocation(
                    token=m.group(0),
                    index=index,
                    line=line_no,
                    column=m.start() + 1,
                )
            )
            index += 1
    return tokens


def beats_to_time(bpm, step_size):
    bps = 60 / bpm
    time_to_step = bps * step_size

    return time_to_step

def parse_instrument_token(token: str) -> tuple[str, dict[str, object]]:
    # Format: i<name>[:k=v,k=v]
    spec = token[1:]
    if ":" in spec:
        name, rest = spec.split(":", 1)
    else:
        name, rest = spec, ""
    name = name.strip() or "sine"

    params: dict[str, object] = {}
    rest = rest.strip()
    if rest:
        for part in rest.split(","):
            part = part.strip()
            if not part:
                continue
            if "=" not in part:
                # Allow bare flags: `ifoo:bar` => {"bar": True}
                params[part] = True
                continue
            k, v = part.split("=", 1)
            k = k.strip()
            v = v.strip()
            if not k:
                continue
            # Parse numeric values when possible (float or fraction).
            try:
                params[k] = parse_num_or_frac(v)
            except Exception:
                params[k] = v

    return name, params

def _parse_song_tokens(
    tokens: list[str],
    *,
    default_title: str,
    token_locations: dict[int, TokenLocation] | None = None,
    line_comments: dict[int, str] | None = None,
) -> tuple[str, list[Tone], list[NoteEvent]]:
    title = default_title
    bpm = 60
    base_octave = 4
    base_duration = 1
    base_volume = 1
    time_stack = []
    auto_step = True
    cursor = 0
    instrument_name = "sine"
    instrument_params: dict[str, object] = {}
    tones: list[Tone] = []
    note_events: list[NoteEvent] = []
    for token_index, token in enumerate(tokens):
        head = token[0]
        tail = token[1:]
        token_params = TokenParams(token)
        if head == 't':     #   title
            title = tail
        elif head == 's':   #   speed
            bpm = int(tail)
        elif head == 'd':   #   set duration
            base_duration = parse_num_or_frac(tail)
        elif head == 'b':   #   go to next beat
            cursor = math.ceil(cursor)
        elif head == 'o':   #   set octave
            base_octave = parse_num_or_frac(tail)
        elif head == 'r':   #   rest
            cursor += beats_to_time(bpm, base_duration)
        elif head == 'v':   #   volume
            base_volume = parse_num_or_frac(tail)
        elif head == '[':   #   disable auto step
            auto_step = False
        elif head == ']':   #   enable auto step
            auto_step = True
            cursor += beats_to_time(bpm, base_duration)
        elif head == '{':   #   push cursor
            time_stack.append(cursor)
        elif head == '}':   #   pop cursor
            cursor = time_stack.pop()
        elif head == 'i':   #   set instrument
            instrument_name, instrument_params = parse_instrument_token(token)
        elif head == 'f':   #   move cursor
            if tail == '':  #   no explicit duration given, use base duration
                cursor += beats_to_time(bpm, base_duration)
            else:
                duration = parse_num_or_frac(tail)
                cursor += beats_to_time(bpm, duration)
        elif head in Note.all_notes():
            note_string = token.split('_')[0]
            octave = token_params.octave if token_params.octave else base_octave
            if token_params.relative_octave:
                octave += token_params.relative_octave
            note = Note(note_string, octave)

            relative_duration = token_params.duration if token_params.duration else base_duration
            duration = beats_to_time(bpm, relative_duration)
            volume = token_params.volume if token_params.volume else base_volume

            # print(note)

            # Copy params so later `i...` tokens don't mutate previously-emitted tones.
            tone = Tone(cursor, note, duration, volume, instrument_name, dict(instrument_params))
            tones.append(tone)
            if token_locations is not None and token_index in token_locations:
                loc = token_locations[token_index]
                note_events.append(
                    NoteEvent(
                        token=token,
                        token_index=token_index,
                        line=loc.line,
                        column=loc.column,
                        start_s=cursor,
                        duration_s=duration,
                        end_s=cursor + duration,
                        note=note_string,
                        octave=float(octave),
                        instrument_name=instrument_name,
                        instrument_params=dict(instrument_params),
                        inline_comment=(line_comments or {}).get(loc.line, ""),
                    )
                )

            if auto_step:
                cursor += duration

    return title, tones, note_events


def parse_song(song_string: str, *, default_title: str = "Untitled"):
    tokens = tokenize_song(song_string)
    title, tones, _ = _parse_song_tokens(tokens, default_title=default_title)
    return title, tones


def parse_song_with_events(song_string: str, *, default_title: str = "Untitled") -> tuple[str, list[Tone], list[NoteEvent]]:
    token_locs = tokenize_song_with_locations(song_string)
    tokens = [x.token for x in token_locs]
    loc_by_index = {x.index: x for x in token_locs}
    comments: dict[int, str] = {}
    for line_no, raw in enumerate(song_string.splitlines(), start=1):
        c = extract_inline_comment(raw)
        if c:
            comments[line_no] = c
    return _parse_song_tokens(
        tokens,
        default_title=default_title,
        token_locations=loc_by_index,
        line_comments=comments,
    )
