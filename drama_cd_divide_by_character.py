"""Generate .ogg vocal segments from drama CD audio using timestamps in `drama-cd-transcript.csv`.

This script:
- Reads `drama-cd-transcript.csv` (expects rows: filename,character,content)
- Locates source CD audio files in a configurable directory
- Extracts segments and writes them to `drama-cd-raw-vocal-output/` using the original CSV filename
- Does NOT create or modify `meta.csv` in the output directory

IMPORTANT: Use `--dry-run` to perform a dry-run (no extraction). Without `--dry-run` the script will perform extraction when possible.
Requires `ffmpeg` on PATH to actually perform extraction. Does not use Whisper.
"""

import argparse
import csv
import os
import re
import concurrent.futures
from moviepy.editor import AudioFileClip
from typing import Optional

# Config
TRANSCRIPT_CSV = "drama-cd-transcript.csv"
OUTPUT_DIR = "drama-cd-raw-vocal-output"
# Directory containing full CD audio files (user should set to the folder where source audio sits)
CD_AUDIO_DIR = r"../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/"  # original path; can be overridden with --cd-dir
AUDIO_EXTENSIONS = {'.flac'}  # only process .flac source audio files
AUDIO_FORMAT = '.ogg'
META_CSV = 'meta.csv'

os.makedirs(OUTPUT_DIR, exist_ok=True)

FILENAME_RE = re.compile(r"\[cd(?P<cd_idx>\d{2})-(?P<track_idx>\d{4})\]\[(?P<start>[^-\]]+)-(?P<end>[^\]]+)\].ogg")
TIME_RE = re.compile(r"(?P<min>\d{2})\.(?P<sec>\d{2})\.(?P<dec>\d{2})")


def parse_time_to_seconds(t: str) -> float:
    m = TIME_RE.match(t)
    if not m:
        raise ValueError(f"Invalid time format: {t}")
    minutes = int(m.group('min'))
    seconds = int(m.group('sec'))
    deci = int(m.group('dec'))
    return minutes * 60 + seconds + deci / 100.0


def find_cd_audio(cd_idx: str, cd_dir: str) -> Optional[str]:
    """Try to locate the source audio file for a given cd index (e.g., '01').

    Heuristics:
    - Look for files whose basename contains 'cd01' (case-insensitive)
    - Otherwise, if there are exactly N audio files and max cd index equals N, map by sorted order
    """
    cd_search = f"cd{cd_idx}"
    candidates = []
    for root, _, files in os.walk(cd_dir):
        for f in files:
            if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS:
                candidates.append(os.path.join(root, f))
    # prefer filename containment
    for c in candidates:
        if cd_search.lower() in os.path.basename(c).lower():
            return c
    # try to map by sorted order
    if candidates:
        # sort deterministic
        candidates = sorted(candidates)
        max_cd = None
        # Map by index safely without try/except
        idx = int(cd_idx) - 1
        if 0 <= idx < len(candidates):
            return candidates[idx]
        return None
    return None


def extract_segment(source: str, start: float, end: float, dest: str, run: bool = False):
    """Extract an audio segment using MoviePy into .ogg (mono, 44.1kHz).

    If run is False, performs a dry-run and prints the intended operation. MoviePy will call ffmpeg internally when writing files, but we do not invoke ffmpeg directly.
    """
    duration = end - start
    if duration <= 0:
        raise ValueError(f"Non-positive duration for {source}: {start} -> {end}")

    action = (
        f"Extract {duration:.3f}s from {source} ({start:.3f}->{end:.3f}) -> {dest} "
        "(mono, 44.1kHz, .ogg libvorbis)"
    )
    if not run:
        print("DRY RUN:", action)
        return

    # Use MoviePy to load, subclip and write audio. Let errors propagate (no try/except).
    with AudioFileClip(source) as clip:
        sub = clip.subclip(start, end)
        # ensure 44.1 kHz and force mono at write time (MoviePy AudioClip doesn't expose set_channels)
        sub = sub.set_fps(44100)
        sub.write_audiofile(dest, codec='libvorbis', fps=44100, ffmpeg_params=["-ac", "1"], verbose=False, logger=None)
        sub.close()
    print(f"Extracted: {dest}")


def main(dry_run: bool = False, cd_dir: str = CD_AUDIO_DIR, jobs: int | None = None):
    if not os.path.exists(TRANSCRIPT_CSV):
        raise FileNotFoundError(f"Transcript CSV not found at {TRANSCRIPT_CSV}")

    rows = []
    max_cdseen = 0
    with open(TRANSCRIPT_CSV, newline='', encoding='utf_8_sig') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 1:
                continue
            # allow empty character/content fields
            filename = row[0]
            character = row[1] if len(row) > 1 else ''
            content = row[2] if len(row) > 2 else ''
            m = FILENAME_RE.match(filename)
            if not m:
                print(f"Skipping unrecognized filename format: {filename}")
                continue
            cd_idx = m.group('cd_idx')
            start_s = parse_time_to_seconds(m.group('start'))
            end_s = parse_time_to_seconds(m.group('end'))
            max_cdseen = max(max_cdseen, int(cd_idx))
            rows.append((filename, character, content, cd_idx, start_s, end_s))

    # Try to automatically locate CD audio files for missing ones
    cd_cache = {}
    for _, _, _, cd_idx, _, _ in rows:
        if cd_idx in cd_cache:
            continue
        src = find_cd_audio(cd_idx, cd_dir)
        cd_cache[cd_idx] = src
        if src is None:
            print(f"WARNING: no source audio found for cd{cd_idx} in {cd_dir} (will skip segments for this CD)")

    # If --dry-run was specified, only validate presence of source audio files and report summary
    if dry_run:
        print("\nDRY RUN: checking source audio files (no extraction will be performed)")
        unique_cd_idxs = sorted({cd_idx for (_, _, _, cd_idx, _, _) in rows})
        for cd_idx in unique_cd_idxs:
            src = cd_cache.get(cd_idx)
            if src:
                print(f"cd{cd_idx}: FOUND -> {src}")
            else:
                print(f"cd{cd_idx}: MISSING")
        print(f"Planned segments: {len(rows)}")
        print("No files were created (dry-run).\n")
        return

    # Process each row (no meta.csv operations) — build task list first
    processed = 0
    skipped_missing = 0
    tasks: list[tuple[str, float, float, str]] = []

    for filename, character, content, cd_idx, start_s, end_s in rows:
        src = cd_cache.get(cd_idx)
        out_path = os.path.join(OUTPUT_DIR, filename)
        if character:
            char_dir = os.path.join(OUTPUT_DIR, character)
            os.makedirs(char_dir, exist_ok=True)
            out_path = os.path.join(char_dir, filename)
        # Ensure parent dir exists
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        if src is None:
            print(f"Skipping {filename}: no source audio for cd{cd_idx}")
            skipped_missing += 1
            continue

        if os.path.exists(out_path):
            print(f"Skipping {filename}: output already exists at {out_path}")
            continue

        tasks.append((src, start_s, end_s, out_path))

    if not tasks:
        print('\nNo extraction tasks to run.')
        print('\nFinished. Output dir:', OUTPUT_DIR)
        print(f'Processed: {processed}, Skipped (missing source): {skipped_missing}')
        return

    # dry-run: show sample tasks
    if dry_run:
        print(f"\nDRY RUN: {len(tasks)} extraction tasks would be executed (no files will be written).")
        for src, s, e, out in tasks[:10]:
            print(f"  {os.path.basename(out)}: {s:.2f}->{e:.2f} from {src} -> {out}")
        if len(tasks) > 10:
            print(f"  ... ({len(tasks)-10} more)")
        return

    # Run extractions in parallel using ProcessPoolExecutor
    max_workers = jobs if (jobs and jobs > 0) else (os.cpu_count() or 1)
    print(f"Running {len(tasks)} extraction tasks with {max_workers} worker(s)...")

    failures = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {executor.submit(extract_segment, src, s, e, out, True): (src, s, e, out)
                          for (src, s, e, out) in tasks}
        try:
            for fut in concurrent.futures.as_completed(future_to_task):
                src, s, e, out = future_to_task[fut]
                try:
                    fut.result()
                except Exception as exc:
                    failures += 1
                    print(f"ERROR extracting {os.path.basename(out)} from {src}: {exc}")
                else:
                    processed += 1
        except KeyboardInterrupt:
            print("Interrupted by user — cancelling remaining tasks...")
            for f in future_to_task:
                f.cancel()
            raise

    print('\nFinished. Output dir:', OUTPUT_DIR)
    print(f'Processed: {processed}, Failed: {failures}, Skipped (missing source): {skipped_missing}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Slice drama CD audio into .ogg segments according to drama-cd-transcript.csv')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry-run only: check source audio and report (no extraction)')
    parser.add_argument('--cd-dir', default=CD_AUDIO_DIR, help='Directory containing source CD audio files')
    parser.add_argument('--jobs', '-j', type=int, default=None, help='Number of worker processes to use (default: cpu_count())')
    args = parser.parse_args()
    main(dry_run=args.dry_run, cd_dir=args.cd_dir, jobs=args.jobs)
