from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Sequence
try:
    import torchaudio as _
except:
    print("WARNING: torchaudio not found; demucs may fail on output.")


def expected_vocals_path(input_path: str, out_root: str, model_name: str) -> Path:
    return Path(out_root) / model_name / Path(input_path).stem / "vocals.flac"


def _run_one(input_path: str, out_root: str, model_name: str, two_stems: str, device: str | None) -> tuple[str, bool, str]:
    output_file = expected_vocals_path(input_path, out_root, model_name)
    if output_file.exists():
        return input_path, False, f"SKIP: {output_file} already exists"

    if not Path(input_path).is_file():
        return input_path, False, f"ERROR: input not found: {input_path}"

    try:
        from demucs.separate import main as demucs_main

        args = [
            "--two-stems",
            two_stems,
            "--flac",
            "--name",
            model_name,
            "--out",
            out_root,
        ]
        if device:
            args.extend(["--device", device])
        args.append(input_path)

        demucs_main(args)

        if output_file.exists():
            return input_path, True, f"DONE: {output_file}"
        return input_path, False, f"ERROR: demucs finished but output missing: {output_file}"
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
        return input_path, False, f"ERROR: demucs exited with code {code} for {input_path}"
    except Exception as exc:
        return input_path, False, f"ERROR: {input_path}: {exc}"


def run_demucs_batch(
    input_files: Sequence[str],
    jobs: int | None = None,
    out_root: str = "separated",
    model_name: str = "htdemucs",
    two_stems: str = "vocals",
    device: str | None = None,
) -> int:
    if not input_files:
        print("No input files configured.")
        return 0

    unique_inputs = list(dict.fromkeys(input_files))
    workers = jobs if jobs and jobs > 0 else ((os.cpu_count() or 1) // 3 or 1)

    skip_count = 0
    fail_count = 0
    done_count = 0

    print(f"Using {workers} process(es)")
    print(f"Model: {model_name}, out: {out_root}, stem: {two_stems}, format: flac")

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_run_one, path, out_root, model_name, two_stems, device): path
            for path in unique_inputs
        }

        for future in as_completed(futures):
            _, created, message = future.result()
            print(message)
            if message.startswith("SKIP:"):
                skip_count += 1
            elif message.startswith("DONE:") and created:
                done_count += 1
            else:
                fail_count += 1

    print(f"\nSummary: done={done_count}, skipped={skip_count}, failed={fail_count}")
    return 0 if fail_count == 0 else 1
