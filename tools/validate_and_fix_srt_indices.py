#!/usr/bin/env python3
"""Validate and (optionally) fix SRT sequence indices for all .srt files
under a directory (default: drama-cd-transcript).

Behavior:
- Scans every line that is exactly a number (pure digits) — these are treated as
  subtitle sequence indices.
- Verifies the indices are consecutive starting at 1.
- If mismatches are found the script reports them and (optionally) reparents
  sequence numbers so they become 1..N in order of appearance.
- A backup (``<filename>.srt.bak``) is created before writing changes.

Usage:
  python3 scripts/validate_and_fix_srt_indices.py        # interactive (prompts)
  python3 scripts/validate_and_fix_srt_indices.py --no  # check-only (default behavior)
  python3 scripts/validate_and_fix_srt_indices.py --fix # auto-fix without prompting

The interactive prompt defaults to NO (press Enter or any non-yes answer => no fix).
This tool is careful and intended to be safe for general .srt files.
"""
from pathlib import Path
import argparse
import sys
import time


def analyze_srt(lines):
    """Return list of (line_index, int_value) for lines that are pure digits."""
    nums = []
    for idx, ln in enumerate(lines):
        s = ln.strip()
        if s.isdigit():
            nums.append((idx, int(s)))
    return nums


def summarize_mismatches(nums):
    """Given numeric entries [(line_idx, value)...], produce mismatches vs expected 1..N."""
    expected = list(range(1, len(nums) + 1))
    mismatches = []
    for ((line_idx, value), exp) in zip(nums, expected):
        if value != exp:
            mismatches.append((line_idx + 1, value, exp))  # return 1-based file line no
    return mismatches


def make_backup(path, contents):
    bak = path.with_suffix(path.suffix + '.bak')
    if bak.exists():
        bak = path.with_suffix(path.suffix + f'.bak.{int(time.time())}')
    bak.write_text(contents, encoding='utf-8')
    return bak


def fix_indices(lines, nums):
    """Return new lines with the numeric sequence lines renumbered 1..N."""
    new_lines = list(lines)
    for target, ((line_idx, _), new_val) in enumerate(zip(nums, range(1, len(nums) + 1)), start=1):
        i = nums[target - 1][0]
        new_lines[i] = str(new_val)
    return new_lines


def process_file(path: Path, auto_fix: bool | None):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    nums = analyze_srt(lines)

    if not nums:
        return {'path': path, 'status': 'no_indices'}

    mismatches = summarize_mismatches(nums)
    if not mismatches:
        return {'path': path, 'status': 'ok'}

    result = {'path': path, 'status': 'mismatch', 'mismatches': mismatches}

    # Decide whether to fix
    if auto_fix is None:
        # interactive prompt; default is NO
        if not sys.stdin.isatty():
            result['fix_taken'] = False
            return result
        ans = input(f"Fix indices in '{path.name}'? [y/N]: ").strip().lower()
        fix = ans in ('y', 'yes')
    else:
        fix = bool(auto_fix)

    if not fix:
        result['fix_taken'] = False
        return result

    # create backup and write fixed file
    bak = make_backup(path, text)
    new_lines = fix_indices(lines, nums)
    path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
    result['fix_taken'] = True
    result['backup'] = str(bak)
    result['changed'] = len(mismatches)
    return result


def main():
    p = argparse.ArgumentParser(description='Validate and optionally fix .srt sequence indices.')
    p.add_argument('paths', nargs='*', help='Optional file paths or globs to check (overrides --dir)')
    p.add_argument('--dir', default='drama-cd-transcript', help='Directory containing .srt files (default: drama-cd-transcript)')
    g = p.add_mutually_exclusive_group()
    g.add_argument('--fix', action='store_true', help='Automatically fix all detected index errors (assume YES)')
    g.add_argument('--no', action='store_true', help='Do not fix anything; only check (assume NO)')
    args = p.parse_args()

    # If positional paths are provided, expand them (accept single file, multiple files, or globs).
    files = []
    if args.paths:
        for pth in args.paths:
            ppath = Path(pth)
            if ppath.is_file():
                files.append(ppath)
            else:
                # treat as glob pattern relative to workspace
                files.extend(sorted(Path('.').glob(pth)))
        # remove duplicates while preserving order
        seen = set()
        unique_files = []
        for f in files:
            if f not in seen:
                seen.add(f)
                unique_files.append(f)
        files = unique_files
    else:
        dd = Path(args.dir)
        if not dd.exists() or not dd.is_dir():
            print(f"Directory not found: {dd}")
            sys.exit(2)
        files = sorted(dd.glob('*.srt'))
    if not files:
        print(f"No .srt files found in: {dd}")
        sys.exit(0)

    auto_fix = True if args.fix else (False if args.no else None)

    total = len(files)
    ok = 0
    fixed = 0
    problems = 0

    for f in files:
        res = process_file(f, auto_fix)
        if res['status'] == 'ok':
            print(f"OK:     {f.name}")
            ok += 1
        elif res['status'] == 'no_indices':
            print(f"SKIP:   {f.name} (no numeric index lines found)")
        elif res['status'] == 'mismatch':
            problems += 1
            print(f"ERROR:  {f.name} — {len(res['mismatches'])} mismatched index line(s)")
            # show up to 6 mismatches as sample
            for ln, cur, exp in res['mismatches'][:6]:
                print(f"         line {ln}: {cur}  ->  {exp}")
            if res.get('fix_taken'):
                fixed += 1
                print(f"FIXED:  {f.name} (backup: {res.get('backup')})")
            else:
                print(f"NOTICE: not fixed. Run with --fix to apply fixes, or rerun interactively and answer 'y'.")

    print('\nSummary:')
    print(f"  files checked: {total}")
    print(f"  OK:            {ok}")
    print(f"  fixed:         {fixed}")
    print(f"  problems:      {problems - fixed}")

    # exit code: 0 if no un-fixed problems; 1 if there are any problems left
    remaining = (problems - fixed)
    sys.exit(0 if remaining == 0 else 1)


if __name__ == '__main__':
    main()
