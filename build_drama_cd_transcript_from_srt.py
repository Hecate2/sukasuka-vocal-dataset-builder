"""Build `drama-cd-transcript.csv` from bilingual SRT files.

- Scans `drama-cd-transcript/` for files matching `KAXA-75**CD_bilingual.srt` (ignores `*.ja.srt`).
- Extracts: filename (`[cd##-####][mm.ss.dd-mm.ss.dd].ogg`), character (mapped from Chinese speaker name via `characters.csv`), content (Japanese subtitle line).
- If Chinese speaker name is empty (line starts with `：`) the character column is written as empty string.
- If Chinese speaker name is present but not found in `characters.csv`, a message is printed and the character column is left empty.
- If the Chinese subtitle line does NOT contain the expected `角色名：` (or `：`), an Exception is raised and the offending file+line is reported.

Usage: python build_drama_cd_transcript_from_srt.py
"""

from __future__ import annotations
import argparse
import csv
import os
import re
from typing import Dict, List, Tuple

SRT_DIR_DEFAULT = "drama-cd-transcript"
CHAR_CSV_DEFAULT = "characters.csv"
OUT_CSV_DEFAULT = "drama-cd-transcript.csv"
SRT_BASENAME_RE = re.compile(r"^KAXA-75(?P<cd_idx>\d{2})CD_bilingual\.srt$")
CHINESE_SPEAKER_RE = re.compile(r"^(?P<name>[^：:]*)[：:](?P<rest>.*)$")  # accept fullwidth or ascii colon
SRT_TIMESTAMP_RE = re.compile(r"(?P<hh>\d+):(?P<mm>\d{2}):(?P<ss>\d{2}),(?P<ms>\d{3})\s*-->\s*(?P<hh2>\d+):(?P<mm2>\d{2}):(?P<ss2>\d{2}),(?P<ms2>\d{3})")


def read_characters(char_csv_path: str) -> Dict[str, str]:
    """Return mapping chinese_name -> english_name from `characters.csv`."""
    mapping: Dict[str, str] = {}
    with open(char_csv_path, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            chinese = (row.get("chinese") or "").strip()
            english = (row.get("english") or "").strip()
            if chinese:
                mapping[chinese] = english
    return mapping


def srt_time_to_mm_ss_dd(srt_ts: str) -> str:
    """Convert SRT timestamp (HH:MM:SS,mmm) to MM.SS.DD (minutes, seconds, centiseconds).

    - minutes is total minutes (hours * 60 + minutes) and zero-padded to 2 digits.
    - centiseconds are computed by integer-division ms//10 (no rounding) and zero-padded.
    """
    m = re.match(r"(?P<hh>\d+):(?P<mm>\d{2}):(?P<ss>\d{2}),(?P<ms>\d{3})", srt_ts.strip())
    if not m:
        raise ValueError(f"Invalid SRT timestamp: {srt_ts!r}")
    hh = int(m.group("hh"))
    mm = int(m.group("mm"))
    ss = int(m.group("ss"))
    ms = int(m.group("ms"))
    total_min = hh * 60 + mm
    centisec = ms // 10
    return f"{total_min:02d}.{ss:02d}.{centisec:02d}"


def parse_srt_blocks(lines: List[str]) -> List[Tuple[int, str, List[str], int]]:
    """Parse SRT file lines into blocks.

    Returns list of tuples: (block_index, time_line, content_lines, chinese_line_number_in_file)
    chinese_line_number_in_file is 1-based file line number for the Chinese subtitle line (for error messages).
    """
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        # skip leading blank lines
        while i < n and lines[i].strip() == "":
            i += 1
        if i >= n:
            break
        # expect index line
        idx_line = lines[i].strip()
        # If idx is not numeric, still try to proceed (some SRTs omit numeric index)
        try:
            block_index = int(idx_line)
            i += 1
        except Exception:
            # treat current line as index-less; do not consume it as content if it's a time line
            # if it's a time line, set block_index = -1 and continue
            block_index = -1
        if i >= n:
            break
        time_line = lines[i].strip()
        i += 1
        # collect content lines until blank line or EOF
        content_start_idx = i
        content_lines: List[str] = []
        while i < n and lines[i].strip() != "":
            content_lines.append(lines[i].rstrip("\n"))
            i += 1
        if not content_lines:
            # malformed block
            raise Exception(f"Malformed SRT block starting near line {max(1, i-2)}: no content lines found")
        # Chinese subtitle is expected to be the second content line -> compute its file line number
        chinese_line_number = content_start_idx + 2  # 1-based: content_start_idx is 0-based index of first content line
        blocks.append((block_index, time_line, content_lines, chinese_line_number))
        # i currently at blank line or EOF; loop will skip blanks
    return blocks


def process_srt_file(srt_path: str, char_map: Dict[str, str]) -> List[Tuple[str, str, str]]:
    """Process one bilingual SRT file and return list of CSV rows (filename, character, content)."""
    basename = os.path.basename(srt_path)
    m = SRT_BASENAME_RE.match(basename)
    if not m:
        raise ValueError(f"SRT filename doesn't match expected pattern: {basename}")
    cd_idx = m.group("cd_idx")

    with open(srt_path, encoding="utf-8-sig") as f:
        all_lines = f.read().splitlines()

    blocks = parse_srt_blocks(all_lines)
    rows: List[Tuple[str, str, str]] = []
    count = 0
    for block_index, time_line, content_lines, chinese_line_no in blocks:
        # content_lines: [Japanese (0), Chinese (1), English (2), ...]
        if len(content_lines) < 2:
            raise Exception(f"{srt_path}:{chinese_line_no}: expected Chinese subtitle on the 2nd content line, but block has {len(content_lines)} content lines")
        japanese = content_lines[0].strip()
        chinese = content_lines[1].strip()

        # validate chinese subtitle begins with {角色名}： or ：
        cm = CHINESE_SPEAKER_RE.match(chinese)
        if not cm:
            raise Exception(f"{srt_path}:{chinese_line_no}: Chinese subtitle does not start with '{{角色名}}：' (found: {chinese!r})")
        speaker_name = cm.group("name").strip()
        if speaker_name == "":
            # explicitly empty speaker (starts with '：')
            print(f"{srt_path}:{chinese_line_no}: empty Chinese speaker — leaving character column blank")
            character = ""
        else:
            character = char_map.get(speaker_name, "")
            if not character:
                print(f"{srt_path}:{chinese_line_no}: Chinese name {speaker_name!r} not found in characters.csv — leaving character blank")
        if character == "Suowong":
            character = "SuowongYoung"

        # parse time range
        ts_match = SRT_TIMESTAMP_RE.match(time_line)
        if not ts_match:
            raise Exception(f"{srt_path}: invalid SRT time-range line near {chinese_line_no - 1}: {time_line!r}")
        start_srt = f"{ts_match.group('hh')}:{ts_match.group('mm')}:{ts_match.group('ss')},{ts_match.group('ms')}"
        end_srt = f"{ts_match.group('hh2')}:{ts_match.group('mm2')}:{ts_match.group('ss2')},{ts_match.group('ms2')}"
        start_fmt = srt_time_to_mm_ss_dd(start_srt)
        end_fmt = srt_time_to_mm_ss_dd(end_srt)

        filename = f"[cd{cd_idx}-{str(count).zfill(4)}][{start_fmt}-{end_fmt}].ogg"
        rows.append((filename, character, japanese))
        count += 1
    return rows


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build drama-cd-transcript.csv from bilingual SRT files")
    p.add_argument("--srt-dir", default=SRT_DIR_DEFAULT, help="Directory containing bilingual .srt files")
    p.add_argument("--chars", default=CHAR_CSV_DEFAULT, help="characters.csv path")
    p.add_argument("--out", default=OUT_CSV_DEFAULT, help="Output CSV path (will be overwritten)")
    p.add_argument("--dry-run", action="store_true", help="Do not write CSV; just print counts and warnings")
    args = p.parse_args(argv)

    if not os.path.isdir(args.srt_dir):
        raise SystemExit(f"SRT directory not found: {args.srt_dir}")
    if not os.path.exists(args.chars):
        raise SystemExit(f"characters.csv not found: {args.chars}")

    char_map = read_characters(args.chars)

    srt_files = sorted([os.path.join(args.srt_dir, f)
                        for f in os.listdir(args.srt_dir)
                        if SRT_BASENAME_RE.match(f)])
    if not srt_files:
        raise SystemExit(f"No bilingual SRT files found in {args.srt_dir} matching KAXA-75**CD_bilingual.srt")

    all_rows: List[Tuple[str, str, str]] = []
    for srt in srt_files:
        print(f"Processing {srt}")
        rows = process_srt_file(srt, char_map)
        all_rows.extend(rows)

    print(f"Total subtitle rows parsed: {len(all_rows)}")
    if args.dry_run:
        print("Dry-run: not writing CSV.")
        return 0

    # write CSV (overwrite)
    with open(args.out, 'w', encoding='utf-8-sig', newline='') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(["filename", "character", "content"])
        for fn, ch, cont in all_rows:
            writer.writerow([fn, ch, cont])

    print(f"Wrote {len(all_rows)} rows to {args.out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
