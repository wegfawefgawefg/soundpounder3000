#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Literal


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def _ffprobe_duration_seconds(path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-of",
        "json",
        "-show_entries",
        "format=duration",
        str(path),
    ]
    out = subprocess.check_output(cmd)
    data = json.loads(out.decode("utf-8", errors="replace"))
    dur = data.get("format", {}).get("duration")
    try:
        return float(dur)
    except Exception:
        return 0.0


Color = Literal["default", "comment", "command", "note", "number", "bracket", "modifier"]


def _ass_escape(s: str) -> str:
    # ASS uses braces for override tags and backslash for control sequences.
    return (
        s.replace("\\", r"\\")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("\n", r"\N")
    )


def _classify_token(tok: str) -> Color:
    if tok in ("[", "]", "{", "}"):
        return "bracket"
    if tok.startswith("t") and len(tok) > 1:
        return "command"
    if tok.startswith("i") and len(tok) > 1:
        return "command"
    if tok.startswith("f") and len(tok) > 1:
        return "command"
    if tok[:1] in ("s", "d", "o", "v", "b", "r") and len(tok) > 1:
        return "command"
    if tok.startswith("_") and len(tok) > 2 and tok[1] in ("d", "o", "v"):
        return "modifier"
    # Notes like C, C#, Db.
    if tok[:1] in "ABCDEFG" and (len(tok) == 1 or tok[1:2] in ("#", "b")):
        return "note"
    # Numbers (int/float/fraction), including negative.
    if tok.replace("-", "", 1).replace(".", "", 1).isdigit():
        return "number"
    if "/" in tok:
        a, b = tok.split("/", 1)
        if a.replace("-", "", 1).isdigit() and b.isdigit():
            return "number"
    return "default"


def _sp_to_ass_text(sp_text: str) -> str:
    out_lines: list[str] = []

    # ASS colors are BGR: &HBBGGRR&
    colors: dict[Color, str] = {
        "default": "&HFFFFFF&",
        "comment": "&H7A7A7A&",
        "command": "&HFFD700&",   # cyan-ish
        "note": "&H00FC7C&",      # green
        "number": "&H00A5FF&",    # orange-ish
        "bracket": "&HC086C5&",   # purple-ish
        "modifier": "&H9CDCFE&",  # light blue
    }

    for raw in sp_text.splitlines():
        line = raw.rstrip("\n")
        stripped = line.lstrip()

        # Full-line comments.
        if stripped.startswith("#"):
            out_lines.append("{\\c" + colors["comment"] + "}" + _ass_escape(line))
            continue

        # Inline comments: `;` or `//`.
        comment_idx = None
        for delim in ("//", ";"):
            idx = line.find(delim)
            if idx != -1 and (comment_idx is None or idx < comment_idx):
                comment_idx = idx

        code = line if comment_idx is None else line[:comment_idx]
        comment = "" if comment_idx is None else line[comment_idx:]

        # Tokenize code but preserve whitespace.
        parts: list[tuple[bool, str]] = []
        cur = ""
        is_ws: bool | None = None
        for ch in code:
            ch_ws = ch.isspace()
            if is_ws is None:
                is_ws = ch_ws
                cur = ch
            elif ch_ws == is_ws:
                cur += ch
            else:
                parts.append((bool(is_ws), cur))
                is_ws = ch_ws
                cur = ch
        if is_ws is not None:
            parts.append((bool(is_ws), cur))

        out: list[str] = []
        cur_color: Color = "default"

        def set_color(c: Color) -> None:
            nonlocal cur_color
            if c != cur_color:
                out.append("{\\c" + colors[c] + "}")
                cur_color = c

        for ws, txt in parts:
            if ws:
                set_color("default")
                out.append(_ass_escape(txt))
                continue

            # Color modifiers separately: `C_o4_d1/16`.
            if "_" in txt:
                segs = txt.split("_")
                head = segs[0]
                if head:
                    set_color(_classify_token(head))
                    out.append(_ass_escape(head))
                for seg in segs[1:]:
                    set_color("modifier")
                    out.append(_ass_escape("_" + seg))
            else:
                set_color(_classify_token(txt))
                out.append(_ass_escape(txt))

        if comment:
            set_color("comment")
            out.append(_ass_escape(comment))

        out_lines.append("".join(out))

    return r"\N".join(out_lines)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Make an mp4 from a SoundPounder .sp file + a .wav file (scrolling, colored text + title).",
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
    # Keep visual stable.
    text = "\n".join(line.expandtabs(2).rstrip() for line in text.splitlines()) + "\n"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    dur_s = _ffprobe_duration_seconds(wav_path)
    if dur_s <= 0:
        dur_s = 10.0

    ass_text = _sp_to_ass_text(text)

    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", prefix="soundpounder_", suffix=".ass") as tf:
        ass_path = Path(tf.name)

        pad = 24
        title_h = 64
        font_size = 26
        y1 = args.height + pad
        y2 = y1 - (args.scroll_speed * dur_s)

        tf.write(
            "\n".join(
                [
                    "[Script Info]",
                    "ScriptType: v4.00+",
                    f"PlayResX: {args.width}",
                    f"PlayResY: {args.height}",
                    "WrapStyle: 0",
                    "",
                    "[V4+ Styles]",
                    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
                    f"Style: Default,{args.font},{font_size},&H00FFFFFF&,&H000000FF&,&H66000000&,&H00000000&,0,0,0,0,100,100,0,0,1,2,1,7,0,0,0,1",
                    "",
                    "[Events]",
                    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
                    (
                        "Dialogue: 0,0:00:00.00,"
                        f"0:00:{dur_s:05.2f},Default,,0,0,0,,"
                        f"{{\\an7\\move(24,{y1:.2f},24,{y2:.2f})}}{ass_text}"
                    ),
                    "",
                ]
            )
        )

    try:
        vf = ",".join(
            [
                "format=yuv420p",
                f"subtitles={shlex.quote(str(ass_path))}",
                (
                    "drawtext="
                    f"font={shlex.quote(args.font)}:"
                    f"text={shlex.quote(title)}:"
                    "x=24:y=18:"
                    "fontsize=42:fontcolor=white:"
                    "shadowcolor=black@0.6:shadowx=2:shadowy=2"
                ),
                f"drawbox=x=0:y=64:w=iw:h=2:color=white@0.25:t=fill",
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
            os.unlink(ass_path)
        except OSError:
            pass

    print(out_path)


if __name__ == "__main__":
    main()

