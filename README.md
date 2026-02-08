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
