# soundpounder3000

Generate `.wav` files from small "fiddle string" song descriptions.

## Quickstart (uv)

1) Install `uv` (one option):

```bash
pipx install uv
pipx ensurepath
```

2) Create the project env + install deps:

```bash
uv venv
uv sync
```

3) Render a demo song:

```bash
uv run main songs/computer_polka.sp
```

This prints the output path and writes a `.wav` into the current working directory.

## Songs

Song files live in `songs/*.sp`.

```bash
uv run main songs/interesting.sp
uv run main songs/interesting.sp -o out.wav
uv run main songs/interesting.sp -o ./out_dir/
```

Instrument selection is done with tokens like `isine`, `isquare`, etc. Instruments can also take parameters:

```text
ipulse:pw=0.2
istring:harmonics=12,decay=6
isaw:atk=0.005,rel=0.08,cut=1200,fenv=4200,fatk=0.01,fdec=0.20,fsus=0.0,frel=0.10
```

## Video (mp4)

Given a `.sp` file and a rendered `.wav`, you can make a simple `.mp4` that shows the title and scrolls through the `.sp` source:

```bash
uv run python scripts/sp_wav_to_mp4.py songs/interesting.sp waves/interesting.wav -o interesting.mp4

# Advanced pane-based renderer (adaptive instrument panes + note highlights)
uv run python scripts/sp_wav_to_mp4_advanced.py songs/interesting.sp waves/interesting.wav -o interesting.advanced.mp4
```

## Old scripts

These still exist:

```bash
uv run python compose.py
uv run python test.py
```

## Notes / TODOs (old)

- time savepoints so it can go back to the last `{` at an `}`
- more instruments
- normalize volumes / may no longer be necessary
- fix bug where the last note doesnt represent the needed music duration
- fix double nesting of cursor jumps
- clean up the location of the output existing in two places for no good reason
