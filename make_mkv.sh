#!/usr/bin/env bash
set -euo pipefail

ffmpeg -y \
  -loop 1 -framerate 1 -i 1.jpg \
  -i "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170628] SPCD 01 (flac)/KAXA-7501CD.flac" \
  -i drama-cd-transcript/KAXA-7501CD_bilingual.ja.srt \
  -i drama-cd-transcript/KAXA-7501CD_bilingual.zh.srt \
  -i drama-cd-transcript/KAXA-7501CD_bilingual.en.srt \
  -i drama-cd-transcript/KAXA-7501CD_bilingual.srt \
  -map 0:v:0 -map 1:a:0 -map 2 -map 3 -map 4 -map 5 \
  -c:v libx264 -preset slow -tune stillimage -crf 26 -pix_fmt yuv420p \
  -c:a aac -q:a 4 \
  -c:s srt \
  -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" \
  -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" \
  -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" \
  -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" \
  -t 960.773333 \
  output-KAXA-7501CD.mkv

ffmpeg -y \
  -loop 1 -framerate 1 -i 2.jpg \
  -i "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170726] SPCD 02 (flac)/KAXA-7502CD.flac" \
  -i drama-cd-transcript/KAXA-7502CD_bilingual.ja.srt \
  -i drama-cd-transcript/KAXA-7502CD_bilingual.zh.srt \
  -i drama-cd-transcript/KAXA-7502CD_bilingual.en.srt \
  -i drama-cd-transcript/KAXA-7502CD_bilingual.srt \
  -map 0:v:0 -map 1:a:0 -map 2 -map 3 -map 4 -map 5 \
  -c:v libx264 -preset slow -tune stillimage -crf 26 -pix_fmt yuv420p \
  -c:a aac -q:a 4 \
  -c:s srt \
  -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" \
  -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" \
  -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" \
  -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" \
  -t 1022.306667 \
  output-KAXA-7502CD.mkv

ffmpeg -y \
  -loop 1 -framerate 1 -i 3.jpg \
  -i "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170823] SPCD 03 (flac)/KAXA-7503CD.flac" \
  -i drama-cd-transcript/KAXA-7503CD_bilingual.ja.srt \
  -i drama-cd-transcript/KAXA-7503CD_bilingual.zh.srt \
  -i drama-cd-transcript/KAXA-7503CD_bilingual.en.srt \
  -i drama-cd-transcript/KAXA-7503CD_bilingual.srt \
  -map 0:v:0 -map 1:a:0 -map 2 -map 3 -map 4 -map 5 \
  -c:v libx264 -preset slow -tune stillimage -crf 26 -pix_fmt yuv420p \
  -c:a aac -q:a 4 \
  -c:s srt \
  -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" \
  -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" \
  -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" \
  -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" \
  -t 983.786667 \
  output-KAXA-7503CD.mkv

ffmpeg -y \
  -loop 1 -framerate 1 -i 4.jpg \
  -i "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170927] SPCD 04 (flac)/KAXA-7504CD.flac" \
  -i drama-cd-transcript/KAXA-7504CD_bilingual.ja.srt \
  -i drama-cd-transcript/KAXA-7504CD_bilingual.zh.srt \
  -i drama-cd-transcript/KAXA-7504CD_bilingual.en.srt \
  -i drama-cd-transcript/KAXA-7504CD_bilingual.srt \
  -map 0:v:0 -map 1:a:0 -map 2 -map 3 -map 4 -map 5 \
  -c:v libx264 -preset slow -tune stillimage -crf 26 -pix_fmt yuv420p \
  -c:a aac -q:a 4 \
  -c:s srt \
  -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" \
  -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" \
  -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" \
  -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" \
  -t 968.706667 \
  output-KAXA-7504CD.mkv

ffmpeg -y \
  -loop 1 -framerate 1 -i 5.png \
  -i "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[171025] SPCD 05 (flac)/KAXA-7505CD.flac" \
  -i drama-cd-transcript/KAXA-7505CD_bilingual.ja.srt \
  -i drama-cd-transcript/KAXA-7505CD_bilingual.zh.srt \
  -i drama-cd-transcript/KAXA-7505CD_bilingual.en.srt \
  -i drama-cd-transcript/KAXA-7505CD_bilingual.srt \
  -map 0:v:0 -map 1:a:0 -map 2 -map 3 -map 4 -map 5 \
  -c:v libx264 -preset slow -tune stillimage -crf 26 -pix_fmt yuv420p \
  -c:a aac -q:a 4 \
  -c:s srt \
  -metadata:s:s:0 language=jpn -metadata:s:s:0 title="Japanese (原文)" \
  -metadata:s:s:1 language=chi -metadata:s:s:1 title="Chinese (翻訳)" \
  -metadata:s:s:2 language=eng -metadata:s:s:2 title="English (translation)" \
  -metadata:s:s:3 language=mul -metadata:s:s:3 title="Original (JP/ZH/EN)" \
  -t 1172.813333 \
  output-KAXA-7505CD.mkv

ffmpeg -y \
  -loop 1 -framerate 1 -i 6.png \
  -i "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[171129] SPCD 06 (flac)/KAXA-7506CD.flac" \
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
  -t 1020.666667 \
  output-KAXA-7506CD.mkv

wait

FD1=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170628] SPCD 01 (flac)/KAXA-7501CD.flac")
MD1=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 output-KAXA-7501CD.mkv)
OK1=$(awk -v a="$MD1" -v b="$FD1" 'BEGIN{print (a>=b?"YES":"NO")}')
echo "KAXA-7501CD|$FD1|$MD1|$OK1"

FD2=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170726] SPCD 02 (flac)/KAXA-7502CD.flac")
MD2=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 output-KAXA-7502CD.mkv)
OK2=$(awk -v a="$MD2" -v b="$FD2" 'BEGIN{print (a>=b?"YES":"NO")}')
echo "KAXA-7502CD|$FD2|$MD2|$OK2"

FD3=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170823] SPCD 03 (flac)/KAXA-7503CD.flac")
MD3=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 output-KAXA-7503CD.mkv)
OK3=$(awk -v a="$MD3" -v b="$FD3" 'BEGIN{print (a>=b?"YES":"NO")}')
echo "KAXA-7503CD|$FD3|$MD3|$OK3"

FD4=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[170927] SPCD 04 (flac)/KAXA-7504CD.flac")
MD4=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 output-KAXA-7504CD.mkv)
OK4=$(awk -v a="$MD4" -v b="$FD4" 'BEGIN{print (a>=b?"YES":"NO")}')
echo "KAXA-7504CD|$FD4|$MD4|$OK4"

FD5=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[171025] SPCD 05 (flac)/KAXA-7505CD.flac")
MD5=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 output-KAXA-7505CD.mkv)
OK5=$(awk -v a="$MD5" -v b="$FD5" 'BEGIN{print (a>=b?"YES":"NO")}')
echo "KAXA-7505CD|$FD5|$MD5|$OK5"

FD6=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/[171129] SPCD 06 (flac)/KAXA-7506CD.flac")
MD6=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 output-KAXA-7506CD.mkv)
OK6=$(awk -v a="$MD6" -v b="$FD6" 'BEGIN{print (a>=b?"YES":"NO")}')
echo "KAXA-7506CD|$FD6|$MD6|$OK6"

[ "$OK1" = "YES" ] && [ "$OK2" = "YES" ] && [ "$OK3" = "YES" ] && [ "$OK4" = "YES" ] && [ "$OK5" = "YES" ] && [ "$OK6" = "YES" ]
