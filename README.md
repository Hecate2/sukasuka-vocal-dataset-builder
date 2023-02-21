My Python codes in this repo are licensed in MIT. Be aware that the anime & subtitles may have other licenses. 

Salute to all the contributors!

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

#### Data sources

**subtititles**: https://bbs.acgrip.com/thread-6124-1-1.html (with **AGPLv3** & **CC BY-NC-SA 4.0** licenses)

**anime videos**: magnet:?xt=urn:btih:a05ba5cf6182e0757288c377fe8c06606a0f6428&dn=%5bMH%26Airota%26FZSD%26VCB-Studio%5d%20Shuumatsu%20Nani%20Shitemasuka%ef%bc%9f%20Isogashii%20Desuka%ef%bc%9f%20Sukutte%20Moratte%20Ii%20Desuka%ef%bc%9f%20%5bMa10p_1080p%5d&tr=udp%3a%2f%2ftracker.publicbt.com%3a80%2fannounce&tr=http%3a%2f%2ftr.bangumi.moe%3a6969%2fannounce&tr=http%3a%2f%2ft.nyaatracker.com%2fannounce&tr=http%3a%2f%2fopen.acgtracker.com%3a1096%2fannounce&tr=http%3a%2f%2fopen.nyaatorrents.info%3a6544%2fannounce&tr=http%3a%2f%2ft2.popgo.org%3a7456%2fannonce&tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce&tr=http%3a%2f%2fopentracker.acgnx.se%2fannounce&tr=http%3a%2f%2ftracker.acgnx.se%2fannounce&tr=http%3a%2f%2fnyaa.tracker.wf%3a7777%2fannounce&tr=udp%3a%2f%2ftracker.openbittorrent.com%3a80%2fannounce&tr=http%3a%2f%2ft.acg.rip%3a6699%2fannounce&tr=udp%3a%2f%2ftracker.prq.to%3a80%2fannounce&tr=http%3a%2f%2fshare.dmhy.org%2fannonuce&tr=http%3a%2f%2ftracker.btcake.com%2fannounce&tr=http%3a%2f%2ftracker.ktxp.com%3a6868%2fannounce&tr=http%3a%2f%2ftracker.ktxp.com%3a7070%2fannounce&tr=udp%3a%2f%2fbt.sc-ol.com%3a2710%2fannounce&tr=http%3a%2f%2fbtfile.sdo.com%3a6961%2fannounce&tr=https%3a%2f%2ft-115.rhcloud.com%2fonly_for_ylbud&tr=http%3a%2f%2fexodus.desync.com%3a6969%2fannounce&tr=udp%3a%2f%2fcoppersurfer.tk%3a6969%2fannounce&tr=http%3a%2f%2ftracker3.torrentino.com%2fannounce&tr=http%3a%2f%2ftracker2.torrentino.com%2fannounce&tr=udp%3a%2f%2fopen.demonii.com%3a1337%2fannounce&tr=udp%3a%2f%2ftracker.ex.ua%3a80%2fannounce&tr=http%3a%2f%2fpubt.net%3a2710%2fannounce&tr=http%3a%2f%2ftracker.tfile.me%2fannounce&tr=http%3a%2f%2fbigfoot1942.sektori.org%3a6969%2fannounce&tr=http%3a%2f%2fbt.sc-ol.com%3a2710%2fannounce

