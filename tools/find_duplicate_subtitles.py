#!/usr/bin/env python3
"""Find identical subtitle text appearing in multiple subtitle blocks (single .srt file).

Usage:
  python tools/find_duplicate_subtitles.py path/to/file.srt
  python tools/find_duplicate_subtitles.py path/to/file.srt -i

By default the comparison collapses whitespace; use -i/--ignore-case to ignore case.
This script only reports duplicates — it does not modify files.
"""

from __future__ import annotations
import argparse
import os
import re
import sys
import textwrap
from typing import List, Dict, Optional

TIMESTAMP_RE = re.compile(r"(\d{1,2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}[,\.]\d{3})")


def parse_timestamp(ts: str) -> float:
    m = re.match(r"^(\d+):(\d{2}):(\d{2})[,\.](\d{3})$", ts.strip())
    if not m:
        raise ValueError(f"Invalid timestamp: {ts!r}")
    h, mm, ss, ms = m.groups()
    return int(h) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0


def parse_srt(path: str) -> List[Dict]:
    raw = open(path, "r", encoding="utf-8-sig").read()
    chunks = re.split(r"\n\s*\n", raw.strip())
    blocks: List[Dict] = []

    for chunk in chunks:
        lines = [ln.rstrip() for ln in chunk.splitlines() if ln.strip() != ""]
        if not lines:
            continue
        ts_line_idx = None
        for i, ln in enumerate(lines[:3]):
            if "-->" in ln:
                ts_line_idx = i
                break
        if ts_line_idx is None:
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


def normalize_text(text: str, ignore_case: bool = False) -> str:
    # collapse whitespace and strip; keep line-breaks collapsed to single spaces
    t = text.strip()
    t = re.sub(r"\s+", " ", t)
    if ignore_case:
        t = t.lower()
    return t


def find_duplicates(blocks: List[Dict], ignore_case: bool = False) -> Dict[str, List[Dict]]:
    mapping: Dict[str, List[Dict]] = {}
    for b in blocks:
        key = normalize_text(b["text"], ignore_case=ignore_case)
        mapping.setdefault(key, []).append(b)
    return {k: v for k, v in mapping.items() if k != "" and len(v) > 1}


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Find identical subtitle text appearing in multiple blocks in a single .srt file.")
    p.add_argument("file", help="Path to a .srt file to check")
    p.add_argument("-i", "--ignore-case", action="store_true", help="Ignore case when comparing subtitle text")
    args = p.parse_args(argv)

    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        return 2

    blocks = parse_srt(args.file)
    if not blocks:
        print("No subtitle blocks parsed.")
        return 0

    duplicates = find_duplicates(blocks, ignore_case=args.ignore_case)
    if not duplicates:
        print("✅ No duplicate subtitle texts found.")
        return 0

    print(f"Found {len(duplicates)} duplicate text group(s) in {args.file}:\n")
    for i, (text_key, items) in enumerate(sorted(duplicates.items(), key=lambda kv: -len(kv[1])), start=1):
        print(f"Group {i} — {len(items)} occurrences:")
        for b in items:
            print(f"  [{b.get('index') if b.get('index') is not None else '?'}] {b['start_ts']} --> {b['end_ts']}")
        print("  Text:")
        print(textwrap.indent(items[0]['text'], '    '))
        print("-" * 60)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
