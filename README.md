My Python codes in this repo are licensed in MIT. Be aware that the anime & subtitles & Python packages (e.g. ffmpeg) may have other licenses. 

#### Salute to all the contributors!

Episodes 09 & 10 labeled by 亡絮开始·祖安钢琴师

Episodes 11 & 12 labeled by 喵る桑

Drama CD 01 subtitled & labeled by [camimo](https://github.com/camimoser1)

[Experimental synthesis (see the .mp3 & .flac files in the release)](https://github.com/Hecate2/sukasuka-vocal-dataset-builder/releases/tag/0.0.anime) and **[model](https://note.ay1.us/#/chtholly-sovits)** training performed by [Aya](https://github.com/Brx86).

[TTS model](https://huggingface.co/mio/chtholly) using ESPnet by [mio](https://huggingface.co/mio).

Dataset of Chtholly checked by mio; Ithea checked by camimo.

If you are going to train your own model, **pay attention that the dataset is further cleaned and [released](https://huggingface.co/datasets/mio/sukasuka-anime-vocal-dataset) by [mio](https://huggingface.co/mio) at huggingface.co to remove non-vocal sounds, using [demucs](https://github.com/facebookresearch/demucs). My releases here STILL INCLUDES NON-VOCAL SOUNDS.** 

![contributions-banner](contributions-banner.png)

(Image created by [Carzit](https://github.com/Carzit/) using AI)

#### Contribution guides for potential Chthollists: Following Tasks!

**All kinds of contributions from anyone are welcomed**, while a perfectly ideal contributor needs to:

- **[THIS IS THE MOST IMPORTANT!]** be familiar with SukaSuka characters, especially the sounds and personalities! **At least you need to know their names...** (head to `releases` to check the English names)
- understand how AI models are trained, and why and how we are building datasets
- know something about `.csv`, or other text-only formats like `.json` that are designed for both humans and machines
- know about github, huggingface, civitai, etc.
- be able to read or write basic programs
- be familiar with AI-ops

**Please always fire an issue mentioning what you are going to do before contributing, in case others may repeat (or have already repeated) your work for many times, wasting labor forces.**

- Verify `meta.csv`. Surely there are mistakes.
- Filter out non-vocal sounds in the dataset
- Mark vocal sounds that are not suitable for training, in `meta.csv`. This requires some training experience. For example, short and meaningless `ああああ~` running away from the character's normal pitch may pollute the model. 

#### How to build your dataset

Place your files like this

```
sukasuka-vocal-dataset-builder:
  get_voice_from_video_and_subtitles.py
  divide_by_character.py
  (Others...)
[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]:
  [MH&Airota&FZSD&VCB-Studio] sukasuka [01][Ma10p_1080p][x265_flac_aac].mkv
  (Others...)
[XKsub] 終末なにしてますか [简日·繁日双语字幕]:
  [XKsub] 終末なにしてますか chs_jap:
    Shuumatsu Nani Shitemasuka 01.chs_jap.ass
    (Others...)
```

Run `get_voice_from_video_and_subtitles.py`, and then **MANUALLY** label all the characters in `sukasuka-vocal-dataset-builder/meta.csv` (format: filename,character,content; check if your csv file has the exact first line `filename,character,content`). Finally run `divide_by_character.py`.

Optional — extract vocals with demucs (htdemucs)

- You can optionally separate vocal stems with `demucs` (htdemucs) and place results under `separated/htdemucs/<album>/vocals.wav`.
- `drama_cd_divide_by_character.py` now supports using those `vocals.wav` files as input and will prefer them over CD `.flac` when available. Use `--separated-dir` to override the default separated directory.
- Example Demucs command (creates `separated/htdemucs/<track>/vocals.wav`):

  pip install demucs
  demucs --two-stems=vocals "../[MH&Airota&FZSD&VCB-Studio] ... /KAXA-7502CD.flac"

  (example full path used in this repo)

- After producing separated vocals you can run:

  python drama_cd_divide_by_character.py --separated-dir separated/htdemucs --jobs 4

  This will read `vocals.wav` under `separated/htdemucs/*` where available and extract segments into `drama-cd-raw-vocal-output/`.

#### Drama CD dataset...

WIP. It is almost done. Just need more checks. If you are interested, manually edit srt files in `drama-cd-transcript`, and run `build_drama_cd_transcript_from_srt.py` and `drama_cd_divide_by_character.py`.

#### Data sources

**subtititles**: https://bbs.acgrip.com/thread-6124-1-1.html (with **AGPLv3** & **CC BY-NC-SA 4.0** licenses)

**anime videos**: magnet:?xt=urn:btih:a05ba5cf6182e0757288c377fe8c06606a0f6428&dn=%5bMH%26Airota%26FZSD%26VCB-Studio%5d%20Shuumatsu%20Nani%20Shitemasuka%ef%bc%9f%20Isogashii%20Desuka%ef%bc%9f%20Sukutte%20Moratte%20Ii%20Desuka%ef%bc%9f%20%5bMa10p_1080p%5d&tr=udp%3a%2f%2ftracker.publicbt.com%3a80%2fannounce&tr=http%3a%2f%2ftr.bangumi.moe%3a6969%2fannounce&tr=http%3a%2f%2ft.nyaatracker.com%2fannounce&tr=http%3a%2f%2fopen.acgtracker.com%3a1096%2fannounce&tr=http%3a%2f%2fopen.nyaatorrents.info%3a6544%2fannounce&tr=http%3a%2f%2ft2.popgo.org%3a7456%2fannonce&tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce&tr=http%3a%2f%2fopentracker.acgnx.se%2fannounce&tr=http%3a%2f%2ftracker.acgnx.se%2fannounce&tr=http%3a%2f%2fnyaa.tracker.wf%3a7777%2fannounce&tr=udp%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce&tr=http%3a%2f%2ft.acg.rip%3a6699%2fannounce&tr=udp%3a%2f%2ftracker.prq.to%3a80%2fannounce&tr=http%3a%2f%2fshare.dmhy.org%2fannonuce&tr=http%3a%2f%2ftracker.btcake.com%2fannounce&tr=http%3a%2f%2ftracker.ktxp.com%3a6868%2fannounce&tr=http%3a%2f%2ftracker.ktxp.com%3a7070%2fannounce&tr=udp%3a%2f%2fbt.sc-ol.com%3a2710%2fannounce&tr=http%3a%2f%2fbtfile.sdo.com%3a6961%2fannounce&tr=https%3a%2f%2ft-115.rhcloud.com%2fonly_for_ylbud&tr=http%3a%2f%2fexodus.desync.com%3a6969%2fannounce&tr=udp%3a%2f%2fcoppersurfer.tk%3a6969%2fannounce&tr=http%3a%2f%2ftracker3.torrentino.com%2fannounce&tr=http%3a%2f%2ftracker2.torrentino.com%2fannounce&tr=udp%3a%2f%2fopen.demonii.com%3a1337%2fannounce&tr=udp%3a%2f%2ftracker.ex.ua%3a80%2fannounce&tr=http%3a%2f%2fpubt.net%3a2710%2fannounce&tr=http%3a%2f%2ftracker.tfile.me%2fannounce&tr=http%3a%2f%2fbigfoot1942.sektori.org%3a6969%2fannounce&tr=http%3a%2f%2fbt.sc-ol.com%3a2710%2fannounce

