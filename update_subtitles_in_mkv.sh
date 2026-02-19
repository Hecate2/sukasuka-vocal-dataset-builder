#!/usr/bin/env bash
set -euo pipefail

python3 tools/split_bilingual_srt.py drama-cd-transcript/KAXA-7501CD_bilingual.srt
python3 tools/split_bilingual_srt.py drama-cd-transcript/KAXA-7502CD_bilingual.srt
python3 tools/split_bilingual_srt.py drama-cd-transcript/KAXA-7503CD_bilingual.srt
python3 tools/split_bilingual_srt.py drama-cd-transcript/KAXA-7504CD_bilingual.srt
python3 tools/split_bilingual_srt.py drama-cd-transcript/KAXA-7505CD_bilingual.srt
python3 tools/split_bilingual_srt.py drama-cd-transcript/KAXA-7506CD_bilingual.srt

ffmpeg -y -i output-KAXA-7501CD.mkv -i drama-cd-transcript/KAXA-7501CD_bilingual.ja.srt -i drama-cd-transcript/KAXA-7501CD_bilingual.zh.srt -i drama-cd-transcript/KAXA-7501CD_bilingual.en.srt -i drama-cd-transcript/KAXA-7501CD_bilingual.srt -map 0:v:0 -map 0:a:0 -map 1:0 -map 2:0 -map 3:0 -map 4:0 -c:v copy -c:a copy -c:s srt -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" output-KAXA-7501CD.tmp.mkv &
ffmpeg -y -i output-KAXA-7502CD.mkv -i drama-cd-transcript/KAXA-7502CD_bilingual.ja.srt -i drama-cd-transcript/KAXA-7502CD_bilingual.zh.srt -i drama-cd-transcript/KAXA-7502CD_bilingual.en.srt -i drama-cd-transcript/KAXA-7502CD_bilingual.srt -map 0:v:0 -map 0:a:0 -map 1:0 -map 2:0 -map 3:0 -map 4:0 -c:v copy -c:a copy -c:s srt -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" output-KAXA-7502CD.tmp.mkv &
ffmpeg -y -i output-KAXA-7503CD.mkv -i drama-cd-transcript/KAXA-7503CD_bilingual.ja.srt -i drama-cd-transcript/KAXA-7503CD_bilingual.zh.srt -i drama-cd-transcript/KAXA-7503CD_bilingual.en.srt -i drama-cd-transcript/KAXA-7503CD_bilingual.srt -map 0:v:0 -map 0:a:0 -map 1:0 -map 2:0 -map 3:0 -map 4:0 -c:v copy -c:a copy -c:s srt -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" output-KAXA-7503CD.tmp.mkv &
ffmpeg -y -i output-KAXA-7504CD.mkv -i drama-cd-transcript/KAXA-7504CD_bilingual.ja.srt -i drama-cd-transcript/KAXA-7504CD_bilingual.zh.srt -i drama-cd-transcript/KAXA-7504CD_bilingual.en.srt -i drama-cd-transcript/KAXA-7504CD_bilingual.srt -map 0:v:0 -map 0:a:0 -map 1:0 -map 2:0 -map 3:0 -map 4:0 -c:v copy -c:a copy -c:s srt -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" output-KAXA-7504CD.tmp.mkv &
ffmpeg -y -i output-KAXA-7505CD.mkv -i drama-cd-transcript/KAXA-7505CD_bilingual.ja.srt -i drama-cd-transcript/KAXA-7505CD_bilingual.zh.srt -i drama-cd-transcript/KAXA-7505CD_bilingual.en.srt -i drama-cd-transcript/KAXA-7505CD_bilingual.srt -map 0:v:0 -map 0:a:0 -map 1:0 -map 2:0 -map 3:0 -map 4:0 -c:v copy -c:a copy -c:s srt -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" output-KAXA-7505CD.tmp.mkv &
ffmpeg -y -i output-KAXA-7506CD.mkv -i drama-cd-transcript/KAXA-7506CD_bilingual.ja.srt -i drama-cd-transcript/KAXA-7506CD_bilingual.zh.srt -i drama-cd-transcript/KAXA-7506CD_bilingual.en.srt -i drama-cd-transcript/KAXA-7506CD_bilingual.srt -map 0:v:0 -map 0:a:0 -map 1:0 -map 2:0 -map 3:0 -map 4:0 -c:v copy -c:a copy -c:s srt -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" output-KAXA-7506CD.tmp.mkv &

wait

mv -f output-KAXA-7501CD.tmp.mkv output-KAXA-7501CD.mkv
mv -f output-KAXA-7502CD.tmp.mkv output-KAXA-7502CD.mkv
mv -f output-KAXA-7503CD.tmp.mkv output-KAXA-7503CD.mkv
mv -f output-KAXA-7504CD.tmp.mkv output-KAXA-7504CD.mkv
mv -f output-KAXA-7505CD.tmp.mkv output-KAXA-7505CD.mkv
mv -f output-KAXA-7506CD.tmp.mkv output-KAXA-7506CD.mkv
