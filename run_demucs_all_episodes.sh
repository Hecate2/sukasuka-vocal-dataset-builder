command -v demucs >/dev/null 2>&1 || { echo "ERROR: demucs not found (pip install demucs)" >&2; exit 1; }
# check torchaudio in the active Python environment and warn if missing
PYTHON_CMD=$(command -v python3 || command -v python || true)
if [ -n "$PYTHON_CMD" ]; then
  if ! "$PYTHON_CMD" -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('torchaudio') else 1)" 2>/dev/null; then
    echo "WARNING: Python package 'torchaudio' not found in $PYTHON_CMD environment. Demucs may fail. Install with: $PYTHON_CMD -m pip install torchaudio" >&2
  fi
else
  echo "WARNING: no python executable found to check for 'torchaudio' (skipping check)" >&2
fi

demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [01][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [02][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [03][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [04][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [05][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [06][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [07][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [08][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [09][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [10][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [11][Ma10p_1080p][x265_flac_aac].mkv"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/[MH&Airota&FZSD&VCB-Studio] sukasuka [12][Ma10p_1080p][x265_flac_aac].mkv"
