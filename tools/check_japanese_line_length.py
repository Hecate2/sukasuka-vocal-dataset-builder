#!/usr/bin/env python3
"""
Check first (Japanese) subtitle lines in .srt files for length > N characters.

Assumption: the first text line of each subtitle block is Japanese.

Usage:
  python tools/check_japanese_line_length.py                      # scan drama-cd-transcript, max 30
  python tools/check_japanese_line_length.py --path path/to/dir --max 40 --fail-on-violation

Exit code: 0 when no violations (or --fail-on-violation not used), 1 if --fail-on-violation and violations found.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import sys


def iter_srt_files(root: Path):
    if not root.exists():
        return
    # if a single file was supplied, yield it (only .srt files)
    if root.is_file():
        if root.suffix.lower() == ".srt":
            yield root
        return
    for p in sorted(root.rglob("*.srt")):
        yield p


def parse_srt_blocks(text: str):
    """Yield (index, timecode, text_lines) for each subtitle block.

    This is a forgiving parser that handles common small SRT variations.
    """
    # split on blank lines (one or more)
    blocks = re.split(r"\n\s*\n", text.strip(), flags=re.M)
    for block in blocks:
        if not block.strip():
            continue
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        idx = None
        timecode = ""
        text_lines = []
        # common: index, timecode, text...
        if re.fullmatch(r"\d+", lines[0]):
            idx = int(lines[0])
            if len(lines) >= 2 and "-->" in lines[1]:
                timecode = lines[1].strip()
                text_lines = lines[2:]
            else:
                # missing/odd timecode line
                text_lines = lines[1:]
        elif "-->" in lines[0]:
            # index omitted
            timecode = lines[0].strip()
            text_lines = lines[1:]
        else:
            # fallback: treat everything after first line as text
            text_lines = lines[1:] or lines
        yield idx, timecode, text_lines


def check_file(path: Path, max_len: int):
    violations = []
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        raw = path.read_text(encoding="utf-8", errors="replace")
    for idx, timecode, text_lines in parse_srt_blocks(raw):
        if not text_lines:
            continue
        first = text_lines[0].strip()
        # count characters (unicode code points)
        length = len(first)
        if length > max_len:
            violations.append({
                "index": idx,
                "timecode": timecode,
                "length": length,
                "line": first,
            })
    return violations


def main(argv=None):
    p = argparse.ArgumentParser(description="Check Japanese (first) subtitle lines in .srt files for length > N characters")
    p.add_argument("target", nargs="?", default=None, help="file or directory to scan (positional, default: drama-cd-transcript)")
    p.add_argument("--path", "-p", default="drama-cd-transcript", help="directory to scan (default: drama-cd-transcript)")
    p.add_argument("--max", "-m", type=int, default=30, help="maximum allowed characters for the first subtitle line (default: 30)")
    p.add_argument("--json", action="store_true", help="print results as JSON")
    p.add_argument("--fail-on-violation", action="store_true", help="exit with code 1 if any violations are found")
    args = p.parse_args(argv)

    # prefer positional target if provided (file or directory), otherwise use --path
    target = args.target if args.target is not None else args.path
    root = Path(target)
    files_checked = 0
    total_violations = 0
    report = {}

    for srt in iter_srt_files(root):
        files_checked += 1
        v = check_file(srt, args.max)
        if v:
            report[str(srt)] = v
            total_violations += len(v)

    if args.json:
        print(json.dumps({
            "scanned_path": str(root),
            "files_checked": files_checked,
            "max_length": args.max,
            "violations_count": total_violations,
            "violations": report,
        }, ensure_ascii=False, indent=2))
    else:
        if total_violations == 0:
            print(f"✅ OK — scanned {files_checked} .srt file(s); no first-line > {args.max} chars found.")
        else:
            print(f"⚠️  Found {total_violations} first-line(s) longer than {args.max} chars in {len(report)} file(s):\n")
            for fp, vs in report.items():
                print(f"{fp}")
                for item in vs:
                    idx = item["index"] if item["index"] is not None else "-"
                    tc = f" [{item['timecode']} ]" if item["timecode"] else ""
                    line = item["line"]
                    print(f"  #{idx}{tc}  len={item['length']}: {line}")
                print()

    if args.fail_on_violation and total_violations > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
