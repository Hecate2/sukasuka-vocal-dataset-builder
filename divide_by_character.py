import os

OUTPUT_PATH = "raw-vocal-output"
METADATA_CSV_FILE = "meta.csv"
AUDIO_FORMAT = '.ogg'

csv_file = open(os.path.join(OUTPUT_PATH, METADATA_CSV_FILE), 'r', encoding='utf_8_sig')
for line in csv_file:
    if line == "filename,character,content\n":
        continue
    if line.count(',') != 2:
        continue
    filename, character, content = line[:-1].split(',')  # [:-1] removes \n at the end of line
    character_path = os.path.join(OUTPUT_PATH, character)
    if not os.path.exists(character_path):
        os.mkdir(character_path)
    original_voice_file_path = os.path.join(OUTPUT_PATH, filename)
    if os.path.exists(original_voice_file_path):
        os.rename(original_voice_file_path, os.path.join(character_path, filename))
character_directories = [i for i in os.listdir(OUTPUT_PATH) if os.path.isdir(os.path.join(OUTPUT_PATH, i))]
for i in character_directories:
    character_voice_files = os.listdir(os.path.join(OUTPUT_PATH, i))
    for file in character_voice_files:
        assert file.endswith(AUDIO_FORMAT)
    print(i, len(character_voice_files))