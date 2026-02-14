#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
from bisect import bisect_right
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from soundpounder3000.parse import NoteEvent, parse_song_with_events


@dataclass(frozen=True)
class PaneRow:
    token: str
    start_s: float
    end_s: float


@dataclass
class Lane:
    name: str
    rows: list[PaneRow]
    starts: list[float]
    windows: list[tuple[float, float]]


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


def _merge_windows(events: list[NoteEvent], idle_hold_s: float) -> list[tuple[float, float]]:
    if not events:
        return []
    expanded = [(max(0.0, e.start_s - idle_hold_s), e.end_s + idle_hold_s) for e in events]
    expanded.sort(key=lambda x: x[0])

    out: list[tuple[float, float]] = []
    cur_start, cur_end = expanded[0]
    for start, end in expanded[1:]:
        if start <= cur_end:
            cur_end = max(cur_end, end)
        else:
            out.append((cur_start, cur_end))
            cur_start, cur_end = start, end
    out.append((cur_start, cur_end))
    return out


def _build_lanes(events: list[NoteEvent], idle_hold_s: float) -> list[Lane]:
    grouped: dict[str, list[NoteEvent]] = defaultdict(list)
    for e in events:
        grouped[e.instrument_name].append(e)

    def first_start(name: str) -> float:
        xs = grouped[name]
        return min(e.start_s for e in xs)

    lanes: list[Lane] = []
    for name in sorted(grouped.keys(), key=first_start):
        evs = sorted(grouped[name], key=lambda e: (e.start_s, e.line, e.column))
        rows = [PaneRow(token=e.token, start_s=e.start_s, end_s=e.end_s) for e in evs]
        starts = [r.start_s for r in rows]
        windows = _merge_windows(evs, idle_hold_s=idle_hold_s)
        lanes.append(Lane(name=name, rows=rows, starts=starts, windows=windows))
    return lanes


def _is_lane_active(lane: Lane, t: float) -> bool:
    windows = lane.windows
    lo = 0
    hi = len(windows)
    while lo < hi:
        mid = (lo + hi) // 2
        if windows[mid][0] <= t:
            lo = mid + 1
        else:
            hi = mid
    idx = lo - 1
    if idx < 0:
        return False
    start, end = windows[idx]
    return start <= t <= end


def _load_font(size: int, font_path: str | None = None) -> ImageFont.ImageFont:
    candidates: list[str] = []
    if font_path:
        candidates.append(font_path)
    candidates.extend(
        [
            "DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/local/share/fonts/DejaVuSansMono.ttf",
        ]
    )
    for cand in candidates:
        try:
            return ImageFont.truetype(cand, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def _layout(count: int, width: int, height: int, top_y: int, gap: int) -> list[tuple[int, int, int, int]]:
    if count <= 0:
        return []

    body_h = max(1, height - top_y)
    cols = max(1, math.ceil(math.sqrt(count * (width / max(1, body_h)))))
    rows = math.ceil(count / cols)

    pane_w = (width - gap * (cols + 1)) // cols
    pane_h = (body_h - gap * (rows + 1)) // rows

    rects: list[tuple[int, int, int, int]] = []
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= count:
                break
            x = gap + c * (pane_w + gap)
            y = top_y + gap + r * (pane_h + gap)
            rects.append((x, y, pane_w, pane_h))
            idx += 1
    return rects


def _draw_pane(
    draw: ImageDraw.ImageDraw,
    lane: Lane,
    rect: tuple[int, int, int, int],
    t: float,
    font_title: ImageFont.ImageFont,
    font_body: ImageFont.ImageFont,
) -> None:
    x, y, w, h = rect

    bg = (16, 20, 24)
    border = (72, 84, 96)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=12, fill=bg, outline=border, width=2)

    header_h = 34
    draw.rectangle((x, y, x + w, y + header_h), fill=(34, 43, 53))
    draw.text((x + 10, y + 8), lane.name, font=font_title, fill=(240, 245, 250))

    body_x = x + 10
    body_y = y + header_h + 8
    body_w = max(1, w - 20)
    body_h = max(1, h - header_h - 16)

    line_h = 20
    max_rows = max(1, body_h // line_h)

    if not lane.rows:
        draw.text((body_x, body_y), "(no notes)", font=font_body, fill=(130, 140, 150))
        return

    active_idxs = [i for i, row in enumerate(lane.rows) if row.start_s <= t < row.end_s]
    if active_idxs:
        center_idx = active_idxs[0]
    else:
        center_idx = max(0, bisect_right(lane.starts, t) - 1)

    start_idx = max(0, center_idx - max_rows // 2)
    end_idx = min(len(lane.rows), start_idx + max_rows)
    start_idx = max(0, end_idx - max_rows)

    max_chars = max(6, int(body_w / 8))

    for row_idx in range(start_idx, end_idx):
        row = lane.rows[row_idx]
        yy = body_y + (row_idx - start_idx) * line_h

        is_active = row.start_s <= t < row.end_s
        is_past = row.end_s <= t

        if is_active:
            draw.rounded_rectangle(
                (body_x - 4, yy - 1, body_x + body_w - 4, yy + line_h - 2),
                radius=5,
                fill=(35, 88, 60),
                outline=(73, 173, 106),
                width=1,
            )

        if is_active:
            color = (232, 255, 240)
        elif is_past:
            color = (128, 138, 146)
        else:
            color = (200, 210, 218)

        text = row.token
        if len(text) > max_chars:
            text = text[: max_chars - 1] + "…"
        draw.text((body_x, yy), text, font=font_body, fill=color)


def _render_frame(
    *,
    width: int,
    height: int,
    title: str,
    t: float,
    lanes: list[Lane],
    font_title: ImageFont.ImageFont,
    font_pane_title: ImageFont.ImageFont,
    font_body: ImageFont.ImageFont,
) -> Image.Image:
    img = Image.new("RGB", (width, height), (7, 10, 14))
    draw = ImageDraw.Draw(img)

    top_h = 72
    draw.rectangle((0, 0, width, top_h), fill=(14, 18, 24))
    draw.text((20, 18), title, font=font_title, fill=(248, 252, 255))
    draw.line((0, top_h, width, top_h), fill=(84, 95, 108), width=2)

    active_lanes = [lane for lane in lanes if _is_lane_active(lane, t)]
    if not active_lanes:
        draw.text((20, top_h + 20), "(no active instruments)", font=font_body, fill=(150, 160, 170))
        return img

    rects = _layout(len(active_lanes), width, height, top_y=top_h, gap=10)
    for lane, rect in zip(active_lanes, rects):
        _draw_pane(draw, lane, rect, t, font_pane_title, font_body)

    return img


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Make an advanced mp4 from a SoundPounder .sp file + .wav with adaptive "
            "instrument panes and note highlighting."
        ),
    )
    ap.add_argument("sp", help="Input .sp song file.")
    ap.add_argument("wav", help="Input .wav audio file.")
    ap.add_argument(
        "-o",
        "--out",
        help="Output .mp4 path. Default: <sp_basename>.advanced.mp4 in current directory.",
    )
    ap.add_argument("--title", help="Override displayed title. Default: stem of the .sp filename.")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument(
        "--idle-hold",
        type=float,
        default=0.40,
        help="Seconds to keep an instrument pane visible before/after nearby notes.",
    )
    ap.add_argument("--font-path", help="Path to a .ttf font file.")
    args = ap.parse_args()

    sp_path = Path(args.sp)
    wav_path = Path(args.wav)
    out_path = Path(args.out) if args.out else Path.cwd() / f"{sp_path.stem}.advanced.mp4"

    text = sp_path.read_text(encoding="utf-8")
    parsed_title, _tones, note_events = parse_song_with_events(text, default_title=sp_path.stem)
    title = args.title or parsed_title or sp_path.stem

    lanes = _build_lanes(note_events, idle_hold_s=max(0.0, args.idle_hold))

    dur_audio = _ffprobe_duration_seconds(wav_path)
    dur_notes = max((e.end_s for e in note_events), default=0.0)
    dur_s = max(dur_audio, dur_notes, 0.1)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    font_title = _load_font(38, args.font_path)
    font_pane_title = _load_font(21, args.font_path)
    font_body = _load_font(18, args.font_path)

    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{args.width}x{args.height}",
        "-r",
        str(args.fps),
        "-i",
        "-",
        "-i",
        str(wav_path),
        "-shortest",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(out_path),
    ]

    total_frames = max(1, int(math.ceil(dur_s * args.fps)))

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        assert proc.stdin is not None
        for frame_idx in range(total_frames):
            t = frame_idx / args.fps
            img = _render_frame(
                width=args.width,
                height=args.height,
                title=title,
                t=t,
                lanes=lanes,
                font_title=font_title,
                font_pane_title=font_pane_title,
                font_body=font_body,
            )
            proc.stdin.write(img.tobytes())

        proc.stdin.close()
        ret = proc.wait()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)
    finally:
        if proc.stdin is not None and not proc.stdin.closed:
            proc.stdin.close()

    print(out_path)


if __name__ == "__main__":
    main()
