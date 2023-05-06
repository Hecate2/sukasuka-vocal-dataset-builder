import datetime
import json
import os

CD_PATH = r"../[MH&Airota&FZSD&VCB-Studio] Shuumatsu Nani Shitemasuka？ Isogashii Desuka？ Sukutte Moratte Ii Desuka？ [Ma10p_1080p]/CDs/"
OUTPUT_PATH = "drama-cd-transcript"
CSV_AI_PATH = "drama-cd-AI-transcript.csv"
CSV_PATH = "drama-cd-transcript.csv"
AUDIO_FORMAT = ".ogg"
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

cd_subdirectories = sorted([d for d in os.listdir(CD_PATH) if "SPCD" in d])
assert len(cd_subdirectories) == 6
cd_paths = [os.path.join(CD_PATH, d, f"KAXA-75{str(i+1).zfill(2)}CD.flac") for i, d in enumerate(cd_subdirectories)]
csv_ai_path = os.path.join(OUTPUT_PATH, CSV_AI_PATH)
with open(csv_ai_path, 'w', encoding='utf-8-sig') as csv_file:
    csv_file.write("filename,character,content\n")
    for i, cd in enumerate(cd_paths):
        result_path = os.path.join(OUTPUT_PATH, f"cd{str(i+1).zfill(2)}.json")
        imported = False
        if not os.path.exists(result_path):
            if not imported:
                imported = True
                import whisper  # pip install -U openai-whisper
                model = whisper.load_model("medium")
            # fp32 runs faster than fp16 at less power consumption on many gaming GPUs?
            result = model.transcribe(cd, language='ja', verbose=True, fp16=False)
            with open(result_path, 'w', encoding='utf-8-sig') as f:
                json.dump(result['segments'], f, ensure_ascii=False, indent=2)
        print(f"Finished {result_path}")
        def split_min_sec_decisec(float_sec: float):
            """
            :param float_sec: 123.1214232
            :return: 02.03.12
            """
            _, start_min, start_sec = str(datetime.timedelta(seconds=float_sec)).split(':')
            start_sec_split = start_sec.split('.')
            start_decisec = '00' if len(start_sec_split) == 1 else start_sec_split[1][:2]
            start_sec = start_sec_split[0]
            return f'{start_min}.{start_sec}.{start_decisec}'
        with open(result_path, encoding='utf-8-sig') as f:
            result = json.load(f)
            for transcript_count, transcript in enumerate(result):
                filename, content = f"[cd{str(i+1).zfill(2)}-{str(transcript_count).zfill(4)}][{split_min_sec_decisec(transcript['start'])}-{split_min_sec_decisec(transcript['end'])}]{AUDIO_FORMAT}", transcript['text']
                csv_file.write(f"{filename},,{content}\n")
if not os.path.exists(os.path.join(OUTPUT_PATH, CSV_PATH)):
    os.rename(os.path.join(OUTPUT_PATH, CSV_AI_PATH), os.path.join(OUTPUT_PATH, CSV_PATH))