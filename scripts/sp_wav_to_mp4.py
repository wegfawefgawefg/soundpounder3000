#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import tempfile
from pathlib import Path


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Make an mp4 from a SoundPounder .sp file + a .wav file (scrolling text + title).",
    )
    ap.add_argument("sp", help="Input .sp song file.")
    ap.add_argument("wav", help="Input .wav audio file.")
    ap.add_argument(
        "-o",
        "--out",
        help="Output .mp4 path. Default: <sp_basename>.mp4 in current directory.",
    )
    ap.add_argument("--title", help="Override the displayed title. Default: stem of the .sp filename.")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument(
        "--scroll-speed",
        type=float,
        default=45.0,
        help="Scroll speed in pixels/sec.",
    )
    ap.add_argument(
        "--font",
        default="DejaVuSansMono",
        help="Font name (fontconfig), e.g. DejaVuSansMono.",
    )
    args = ap.parse_args()

    sp_path = Path(args.sp)
    wav_path = Path(args.wav)
    out_path = Path(args.out) if args.out else Path.cwd() / f"{sp_path.stem}.mp4"
    title = args.title or sp_path.stem

    text = sp_path.read_text(encoding="utf-8").rstrip() + "\n"
    # Keep the visual stable: expand tabs and strip trailing whitespace.
    text = "\n".join(line.expandtabs(2).rstrip() for line in text.splitlines()) + "\n"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # `drawtext=textfile=...` reads the file at render time. Use a stable temp file.
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", prefix="soundpounder_", suffix=".txt") as tf:
        tf.write(text)
        tf_path = Path(tf.name)

    try:
        # Scroll from below the screen upward over time.
        # Start position: just below the bottom, with padding.
        # y(t) = h - t*speed + pad
        # Note: doesn't clamp at the end; it will keep moving (fine for typical songs).
        pad = 24
        title_h = 64
        font_size = 26
        y_expr = f"(h+{pad})-t*{args.scroll_speed}"

        vf = ",".join(
            [
                # Background
                "format=yuv420p",
                # Title bar
                (
                    "drawtext="
                    f"font={shlex.quote(args.font)}:"
                    f"text={shlex.quote(title)}:"
                    "x=24:y=18:"
                    "fontsize=42:fontcolor=white:"
                    "shadowcolor=black@0.6:shadowx=2:shadowy=2"
                ),
                # Scrolling body (monospace recommended)
                (
                    "drawtext="
                    f"font={shlex.quote(args.font)}:"
                    f"textfile={shlex.quote(str(tf_path))}:"
                    "reload=1:"
                    f"x=24:y={y_expr}:"
                    f"fontsize={font_size}:line_spacing=6:"
                    "fontcolor=white@0.95:"
                    "shadowcolor=black@0.6:shadowx=2:shadowy=2"
                ),
                # Subtle separator line under title
                f"drawbox=x=0:y={title_h}:w=iw:h=2:color=white@0.25:t=fill",
            ]
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"color=c=black:s={args.width}x{args.height}:r={args.fps}",
            "-i",
            str(wav_path),
            "-shortest",
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(out_path),
        ]
        _run(cmd)
    finally:
        try:
            os.unlink(tf_path)
        except OSError:
            pass

    print(out_path)


if __name__ == "__main__":
    main()

