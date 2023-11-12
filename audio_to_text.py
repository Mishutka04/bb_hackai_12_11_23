from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import os
from pydub.playback import play
import json


SetLogLevel(0)


def voice_to_text(audio_file: str):
    
    main_dir = "/media/robot/Seagate/hak"
    
    dir_file_name = f'{audio_file.split("/")[-1].split(".")[-2]}'

    try:
        os.mkdir(f"{main_dir}/files/{dir_file_name}")
    except FileExistsError:
        pass
    
    file = f'{main_dir}/files/{dir_file_name}/subtitles_{dir_file_name}.srt'
    if os.path.exists(file):
        print(f"Файл был распознан ранее {file}")
        return

    # Проверяем наличие модели
    if not os.path.exists("/media/robot/Seagate/hak/model"):
        print("Please download the model from \
            https://alphacephei.com/vosk/models\
                and unpack as 'model' in the current folder.")
        exit(1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 44100
    CHANNELS = 1

    model = Model("/media/robot/Seagate/hak/model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)

    # Используя библиотеку pydub делаем предобработку аудио
    audio = AudioSegment.from_wav(audio_file)
    audio = audio.set_channels(CHANNELS)
    audio = audio.set_frame_rate(FRAME_RATE)

    # Воспроизводим аудио
    # play(audio)

    # Преобразуем аудио в бинарный формат
    audio_binary = audio.raw_data
    # Проход по аудиофайлу и распознавание
    rec.AcceptWaveform(audio_binary)
    result = rec.FinalResult()
    text = json.loads(result)["text"]
    print("Распознано: ", text)

    # TODO
    # Добавляем пунктуацию (работает через стороннее API, найти другой вариант)
    # cased = subprocess.check_output(
    #     'python3 recasepunc/recasepunc.py predict recasepunc/checkpoint',
    #     shell=True,
    #     text=True,
    #     input=text
    #     )
    # Записываем результат в файл "data.txt"
    with open(file, 'w') as f:
        json.dump(text, f, ensure_ascii=False, indent=4)

    return text


if __name__ == "__main__":
    videos = "/media/robot/Seagate/hak/files"
    for root, dirs, files in os.walk(videos):
        for file in files:
            if file.endswith('.wav'):
                print(os.path.join(root, file))
                voice_to_text(os.path.join(root, file))
        # if v.is_file() and v.name.endswith('.wav'):
        #     print(v.path)
            # voice_to_text(audio_file==v.path)
    # audio_file = "files/0/0.wav"
    # voice_to_text(audio_file=audio_file)
