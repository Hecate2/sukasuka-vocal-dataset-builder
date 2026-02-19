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

demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170628] SPCD 01 (flac)/KAXA-7501CD.flac"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170726] SPCD 02 (flac)/KAXA-7502CD.flac"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170823] SPCD 03 (flac)/KAXA-7503CD.flac"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170927] SPCD 04 (flac)/KAXA-7504CD.flac"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[171025] SPCD 05 (flac)/KAXA-7505CD.flac"
demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[171129] SPCD 06 (flac)/KAXA-7506CD.flac"