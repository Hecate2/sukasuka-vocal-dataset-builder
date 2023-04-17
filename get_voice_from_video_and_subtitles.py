from collections import namedtuple
import csv
import os
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import ass
from moviepy.editor import VideoFileClip

pool = ThreadPoolExecutor(os.cpu_count())
metadata_lock = threading.Lock()

SUBTITLE_PATH = "../[XKsub] 終末なにしてますか [简日·繁日双语字幕]/[XKsub] 終末なにしてますか chs_jap"
VIDEO_PATH = "../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]"
OUTPUT_PATH = "raw-vocal-output"
METADATA_CSV_FILE = "meta.csv"
AUDIO_FORMAT = '.ogg'


def main():
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    if os.listdir(OUTPUT_PATH):
        print(f"WARNING: OUTPUT_PATH {OUTPUT_PATH} not empty", file=sys.stderr)
        # input('Press ENTER to continue. This will overwrite everything including the metadata csv file!')
    
    all_subtitles_path = [s for s in os.listdir(SUBTITLE_PATH) if s.endswith(".ass")]
    print(all_subtitles_path)
    assert len(all_subtitles_path) == 12
    for s in all_subtitles_path:
        assert re.search(r"Shuumatsu Nani Shitemasuka \d{2}\.chs_jap\.ass", s)
    all_subtitles_path = [os.path.join(SUBTITLE_PATH, s) for s in all_subtitles_path]
    
    all_videos_path = [s for s in os.listdir(VIDEO_PATH) if s.endswith(".mkv")]
    print(all_videos_path)
    assert len(all_videos_path) == 12
    for s in all_videos_path:
        assert re.search(r"\[MH&Airota&FZSD&VCB-Studio] sukasuka \[\d{2}]\[Ma10p_1080p]\[x265_flac_aac]\.mkv", s)
    all_videos_path = [os.path.join(VIDEO_PATH, s) for s in all_videos_path]
    
    SubtitleItem = namedtuple('SubtitleItem', ('start', 'end', 'text'))
    metadata_file_path = os.path.join(OUTPUT_PATH, METADATA_CSV_FILE)
    completed_filenames = set()
    csv_file = open(metadata_file_path, 'a', encoding='utf_8_sig')
    csv_file.close()
    if os.path.getsize(metadata_file_path) == 0:
        csv_file = open(metadata_file_path, 'w', encoding='utf_8_sig')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(("filename", "character", "content"))  # we are not going to write the character column in this phase
    else:
        with open(metadata_file_path, 'r', encoding='utf_8_sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line:
                    completed_filenames.add(line[0])

    for i, (video_path, subtitle_path) in enumerate(zip(all_videos_path, all_subtitles_path)):
        print(i, video_path, subtitle_path)
        with open(subtitle_path, 'r', encoding='utf_8_sig') as f:
            subtitle_doc = ass.parse_file(f)
        subtitles = [SubtitleItem(s.start, s.end, re.sub(r"{.*}", "", s.text)) for s in subtitle_doc.events if s.TYPE == 'Dialogue' and "jap" in s.style]
        print(f'{len(subtitles)} subtitles')

        clip = VideoFileClip(video_path)
        for sub_index, s in enumerate(subtitles):
            start_time_str = str(s.start).replace(':', '.')
            if len(start_time_str) == len('0:01:22'):
                start_time_str = start_time_str[2:] + '.00'
            else:
                start_time_str = start_time_str[2:-4]
            end_time_str = str(s.end).replace(':', '.')
            if len(end_time_str) == len('0:01:22'):
                end_time_str = end_time_str[2:] + '.00'
            else:
                end_time_str = end_time_str[2:-4]
            output_filename = f"[{str(i + 1).zfill(2)}-{str(sub_index + 1).zfill(4)}][{start_time_str}-{end_time_str}]{AUDIO_FORMAT}"
            assert len(output_filename) == len(f'[01-0001][00.04.75-00.07.46]{AUDIO_FORMAT}')
            if output_filename not in completed_filenames:
                output_filename_and_path = os.path.join(OUTPUT_PATH, output_filename)

                def thread_task():
                    print(f"starting {output_filename}")
                    clip.subclip(str(s.start), str(s.end)).audio.write_audiofile(output_filename_and_path, verbose=False, logger=None)
                    with metadata_lock:
                        with open(metadata_file_path, 'a', encoding='utf_8_sig') as csv_file:
                            csv_file.write(f"{output_filename},{s.text}\n")
                    print(f"finished {output_filename}")
                # pool.submit(thread_task)
                thread_task()
    

if __name__ == '__main__':
    main()
    pool.shutdown(wait=True)
