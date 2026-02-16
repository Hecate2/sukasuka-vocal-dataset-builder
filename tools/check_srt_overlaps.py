#!/usr/bin/env python3
"""Check adjacent SRT subtitle blocks for overlapping timestamps.

Usage:
  python tools/check_srt_overlaps.py path/to/file.srt
  python tools/check_srt_overlaps.py path/to/directory [-r|--recursive]

This script only *reports* overlaps — it does not modify files.
"""

from __future__ import annotations
import argparse
import glob
import os
import re
import sys
import textwrap
from typing import List, Dict, Optional

TIMESTAMP_RE = re.compile(r"(\d{1,2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}[,\.]\d{3})")


def parse_timestamp(ts: str) -> float:
    """Return seconds (float) for an SRT timestamp like 00:01:23,456 or 0:01:23.456."""
    m = re.match(r"^(\d+):(\d{2}):(\d{2})[,\.](\d{3})$", ts.strip())
    if not m:
        raise ValueError(f"Invalid timestamp: {ts!r}")
    h, mm, ss, ms = m.groups()
    return int(h) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0


def parse_srt(path: str) -> List[Dict]:
    """Parse an .srt file into a list of blocks.

    Each block is a dict: {index, start (s), end (s), start_ts, end_ts, text}
    Blocks with unparsable timestamps are skipped.
    """
    raw = open(path, "r", encoding="utf-8-sig").read()
    # split on blank lines (one or more)
    chunks = re.split(r"\n\s*\n", raw.strip())
    blocks: List[Dict] = []

    for chunk in chunks:
        lines = [ln.rstrip() for ln in chunk.splitlines() if ln.strip() != ""]
        if not lines:
            continue
        # detect timestamp line (usually second line)
        ts_line_idx = None
        for i, ln in enumerate(lines[:3]):
            if "-->" in ln:
                ts_line_idx = i
                break
        if ts_line_idx is None:
            # skip malformed block
            continue

        index = None
        if ts_line_idx >= 1 and re.match(r"^\d+\s*$", lines[0]):
            try:
                index = int(lines[0].strip())
            except Exception:
                index = None

        ts_line = lines[ts_line_idx]
        m = TIMESTAMP_RE.search(ts_line)
        if not m:
            continue
        start_ts, end_ts = m.group(1), m.group(2)
        try:
            start = parse_timestamp(start_ts)
            end = parse_timestamp(end_ts)
        except Exception:
            continue

        # text is what's after the timestamp line
        text_lines = lines[ts_line_idx + 1 :]
        text = "\n".join(text_lines).strip()
        blocks.append({
            "index": index,
            "start": start,
            "end": end,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "text": text,
        })

    return blocks


def find_overlaps(blocks: List[Dict]) -> List[Dict]:
    """Return list of overlapping adjacent block-pairs (as tuples in dict form).

    We consider "adjacent" by index when all blocks have indexes; otherwise by start time.
    Overlap condition: next.start < current.end
    """
    if not blocks:
        return []
    if all(b.get("index") is not None for b in blocks):
        ordered = sorted(blocks, key=lambda b: b["index"])  # adjacent by index
    else:
        ordered = sorted(blocks, key=lambda b: b["start"])  # adjacent by time

    overlaps = []
    for a, b in zip(ordered, ordered[1:]):
        if b["start"] < a["end"]:
            overlaps.append({"a": a, "b": b})
    return overlaps


def scan_path(path: str, recursive: bool = False) -> List[str]:
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        if recursive:
            pattern = os.path.join(path, "**", "*.srt")
            return sorted(glob.glob(pattern, recursive=True))
        else:
            pattern = os.path.join(path, "*.srt")
            return sorted(glob.glob(pattern))
    raise FileNotFoundError(path)


def print_overlap(file: str, pair: Dict) -> None:
    a = pair["a"]
    b = pair["b"]
    idx_a = a.get("index")
    idx_b = b.get("index")
    print(f"File: {file}")
    print(f"Overlap between blocks {idx_a if idx_a is not None else '?'} and {idx_b if idx_b is not None else '?'}:")
    print(f"  [{idx_a if idx_a is not None else '?'}] {a['start_ts']} --> {a['end_ts']}")
    print(textwrap.indent(a['text'] or '<no text>', '    '))
    print(f"  [{idx_b if idx_b is not None else '?'}] {b['start_ts']} --> {b['end_ts']}")
    print(textwrap.indent(b['text'] or '<no text>', '    '))
    print("-" * 60)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Report overlapping adjacent subtitle blocks in .srt files.")
    p.add_argument("path", help="Path to a .srt file or a directory containing .srt files")
    p.add_argument("-r", "--recursive", action="store_true", help="Recurse into subdirectories when path is a directory")
    args = p.parse_args(argv)

    try:
        files = scan_path(args.path, recursive=args.recursive)
    except FileNotFoundError:
        print(f"Path not found: {args.path}", file=sys.stderr)
        return 2

    if not files:
        print("No .srt files found.")
        return 0

    total_overlaps = 0
    for f in files:
        try:
            blocks = parse_srt(f)
        except Exception as ex:
            print(f"Failed to parse {f}: {ex}", file=sys.stderr)
            continue
        overlaps = find_overlaps(blocks)
        if overlaps:
            for pair in overlaps:
                print_overlap(f, pair)
            total_overlaps += len(overlaps)

    if total_overlaps:
        print(f"\n✅ Found {total_overlaps} overlapping adjacent subtitle pair(s) across {len(files)} scanned file(s).")
        return 1
    else:
        print("✅ No overlapping adjacent subtitle blocks found.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
