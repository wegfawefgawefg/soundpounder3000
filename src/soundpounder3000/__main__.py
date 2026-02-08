from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import fiddle_to_wav


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="main",
        description="Render a SoundPounder .sp song file to a .wav file.",
    )
    parser.add_argument("input", help="Path to input .sp file.")
    parser.add_argument(
        "-o",
        "--out",
        help="Output path (.wav file or directory). Default: write <title>.wav to the current working directory.",
    )
    args = parser.parse_args(argv)

    in_path = Path(args.input)
    text = in_path.read_text(encoding="utf-8")
    title = fiddle_to_wav(text, outdir=".", outfile=args.out, default_title=in_path.stem)
    out = args.out
    if out is None:
        print(str(Path.cwd() / f"{title}.wav"))
    else:
        p = Path(out)
        if p.suffix == "" or (p.exists() and p.is_dir()):
            print(str(p / f"{title}.wav"))
        else:
            print(str(p))


if __name__ == "__main__":
    main(sys.argv[1:])
