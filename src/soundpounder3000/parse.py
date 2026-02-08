import math

from .token_params import TokenParams
from .utils import parse_num_or_frac
from .tone import Tone
from .note import Note


def _strip_comments(line: str) -> str:
    # Notes use sharps like `C#`, so avoid treating `#` as an inline comment
    # delimiter. We support:
    # - `; ...` end-of-line comments
    # - `// ...` end-of-line comments
    # - `# ...` only as a full-line comment (or after whitespace as ` # ...`)
    s = line

    # Full-line '#' comments.
    if s.lstrip().startswith("#"):
        return ""

    # Inline comments.
    for delim in ("//", ";"):
        idx = s.find(delim)
        if idx != -1:
            s = s[:idx]
    idx = s.find(" #")
    if idx != -1:
        s = s[:idx]
    return s.strip()


def tokenize_song(song_string: str) -> list[str]:
    tokens: list[str] = []
    for line in song_string.splitlines():
        line = _strip_comments(line)
        if not line:
            continue
        tokens.extend(line.split())
    return tokens


def beats_to_time(bpm, step_size):
    bps = 60 / bpm
    time_to_step = bps * step_size

    return time_to_step

def parse_song(song_string: str, *, default_title: str = "Untitled"):
    tokens = tokenize_song(song_string)

    title = default_title
    bpm = 60
    base_octave = 4
    base_duration = 1
    base_volume = 1
    time_stack = []
    auto_step = True
    cursor = 0
    instrument = "sine"
    tones = []
    for token in tokens:
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
            instrument = tail
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

            tone = Tone(cursor, note, duration, volume, instrument)
            tones.append(tone)

            if auto_step:
                cursor += duration

    return title, tones
            
