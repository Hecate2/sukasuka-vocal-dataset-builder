ffmpeg -y \
  -loop 1 -framerate 1 -i cover.png \
  -i "../[MH&Airota&FZSD&VCB-Studio]/.../CDs/[171129] SPCD 06 (flac)/KAXA-7506CD.flac" \
  -i drama-cd-transcript/KAXA-7506CD_bilingual.ja.srt \
  -i drama-cd-transcript/KAXA-7506CD_bilingual.zh.srt \
  -i drama-cd-transcript/KAXA-7506CD_bilingual.en.srt \
  -i drama-cd-transcript/KAXA-7506CD_bilingual.srt \
  -map 0:v:0 -map 1:a:0 -map 2 -map 3 -map 4 -map 5 \
  -c:v libx264 -preset slow -tune stillimage -crf 26 -pix_fmt yuv420p \
  -c:a aac -q:a 4 \
  -c:s srt \
  -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" \
  -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" \
  -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" \
  -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" \
  -shortest \
  output-KAXA-7506CD.mkv