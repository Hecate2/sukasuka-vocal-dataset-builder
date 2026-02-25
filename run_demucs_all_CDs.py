from __future__ import annotations

import argparse

from run_demucs_batch import run_demucs_batch


INPUT_FILES = [
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170628] SPCD 01 (flac)/KAXA-7501CD.flac",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170726] SPCD 02 (flac)/KAXA-7502CD.flac",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170823] SPCD 03 (flac)/KAXA-7503CD.flac",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170927] SPCD 04 (flac)/KAXA-7504CD.flac",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[171025] SPCD 05 (flac)/KAXA-7505CD.flac",
    "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[171129] SPCD 06 (flac)/KAXA-7506CD.flac",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Demucs for all drama CDs with multiprocessing and skip existing outputs.")
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
