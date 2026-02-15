#!/usr/bin/env python3
"""Scan .srt files and report subtitle lines that start with a speaker label
of the form `Name：` where `Name` is NOT found in the Chinese names column
of `characters.csv`.

Usage examples:
  python3 tools/check_chinese_speaker_labels.py drama-cd-transcript/*.srt
  python3 tools/check_chinese_speaker_labels.py --dir drama-cd-transcript

By default the script reads `characters.csv` from the repository root.
"""
from pathlib import Path
import argparse
import re
import csv
import sys

SPEAKER_RE = re.compile(r"^\s*(?P<name>[^：\n]+)：")


def load_chinese_names(csv_path: Path):
    if not csv_path.exists():
        raise FileNotFoundError(f"characters.csv not found at: {csv_path}")
    names = set()
    with csv_path.open(encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        # Accept header names 'chinese' or third column fallback
        for row in reader:
            ch = row.get('chinese') if 'chinese' in row else None
            if ch is None:
                # fallback to third column if CSV has no header
                vals = list(row.values())
                if len(vals) >= 3:
                    ch = vals[2]
            if ch:
                names.add(ch.strip())
    return names


def parse_srt_blocks(lines):
    """Yield subtitle blocks as (index, timecode, text_lines, start_line_no)."""
    i = 0
    n = len(lines)
    while i < n:
        # skip empty lines
        if lines[i].strip() == '':
            i += 1
            continue
        # expect numeric index
        idx_line_no = i + 1
        idx_line = lines[i].strip()
        if not idx_line.isdigit():
            # skip until next blank or digit to be permissive
            i += 1
            continue
        idx = int(idx_line)
        # timecode should follow
        tline = lines[i + 1].rstrip() if i + 1 < n else ''
        # gather text lines until a blank line or EOF
        j = i + 2
        text_lines = []
        while j < n and lines[j].strip() != '':
            text_lines.append(lines[j].rstrip())
            j += 1
        yield idx, tline, text_lines, idx_line_no
        i = j + 1


def check_file(path: Path, chinese_names: set):
    problems = []
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    for idx, times, text_lines, start_line_no in parse_srt_blocks(lines):
        for offset, tl in enumerate(text_lines, start=0):
            m = SPEAKER_RE.match(tl)
            if not m:
                continue
            speaker = m.group('name').strip()
            if speaker not in chinese_names:
                problems.append({
                    'file': str(path),
                    'block_index': idx,
                    'time': times,
                    'line_no': start_line_no + 2 + offset,  # approximate file line number
                    'text': tl,
                    'speaker': speaker,
                })
    return problems


def main():
    p = argparse.ArgumentParser(description='Find speaker labels in Chinese SRT lines that are not in characters.csv')
    p.add_argument('paths', nargs='*', help='Files or glob (default: drama-cd-transcript/*.srt)')
    p.add_argument('--dir', default=None, help='Directory to scan for .srt files (overrides positional globs)')
    p.add_argument('--csv', default='characters.csv', help='Path to characters.csv (default: characters.csv)')
    p.add_argument('--show-unique', action='store_true', help='Also print a unique list of unknown speaker names')
    args = p.parse_args()

    csv_path = Path(args.csv)
    try:
        chinese_names = load_chinese_names(csv_path)
    except Exception as e:
        print('ERROR loading characters.csv:', e, file=sys.stderr)
        sys.exit(2)

    if args.dir:
        base = Path(args.dir)
        files = sorted(base.glob('*.srt'))
    elif args.paths:
        # expand given paths
        files = []
        for pth in args.paths:
            files.extend(sorted(Path().glob(pth)))
    else:
        files = sorted(Path('drama-cd-transcript').glob('*.srt'))

    if not files:
        print('No .srt files found to scan.')
        sys.exit(0)

    total_problems = 0
    unknown_names = set()

    for f in files:
        probs = check_file(f, chinese_names)
        if not probs:
            continue
        total_problems += len(probs)
        print(f"\nFile: {f} — {len(probs)} unknown speaker label(s) found:")
        for p in probs:
            print(f"  [block #{p['block_index']} | {p['time']} | line {p['line_no']}] {p['text']}  -> speaker='{p['speaker']}' (NOT in characters.csv)")
            unknown_names.add(p['speaker'])

    if total_problems == 0:
        print('No unknown Chinese speaker labels found.')
        sys.exit(0)

    print('\nSummary:')
    print(f'  total files scanned: {len(files)}')
    print(f'  total unknown speaker labels: {total_problems}')
    if args.show_unique:
        print('\nUnknown speaker names:')
        for name in sorted(unknown_names):
            print(' ', name)
    sys.exit(1)


if __name__ == '__main__':
    main()
