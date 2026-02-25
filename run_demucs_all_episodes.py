from __future__ import annotations

import argparse

from run_demucs_batch import run_demucs_batch


INPUT_FILES = [
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [01][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [02][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [03][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [04][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [05][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [06][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [07][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [08][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [09][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [10][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [11][Ma10p_1080p][x265_flac_aac].mkv",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [12][Ma10p_1080p][x265_flac_aac].mkv",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Demucs for all episodes with multiprocessing and skip existing outputs.")
    parser.add_argument("--jobs", "-j", type=int, default=None, help="Worker process count (default: (cpu_count / 3) or 1)")
    parser.add_argument("--out", default="separated", help="Output root directory (default: separated)")
    parser.add_argument("--model", default="htdemucs", help="Demucs model name (default: htdemucs)")
    parser.add_argument("--device", default=None, help="Demucs device, e.g. cpu/cuda (optional)")
    args = parser.parse_args()

    return run_demucs_batch(
        INPUT_FILES,
        jobs=args.jobs,
        out_root=args.out,
        model_name=args.model,
        two_stems="vocals",
        device=args.device,
    )


if __name__ == "__main__":
    raise SystemExit(main())
