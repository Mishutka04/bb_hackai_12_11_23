from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import os
from pydub.playback import play
import json


SetLogLevel(0)

# Проверяем наличие модели
if not os.path.exists("model"):
    print("Please download the model from \
        https://alphacephei.com/vosk/models\
            and unpack as 'model' in the current folder.")
    exit(1)

# Устанавливаем Frame Rate
FRAME_RATE = 44100
CHANNELS = 1

model = Model("model")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)

# Используя библиотеку pydub делаем предобработку аудио
audio = AudioSegment.from_wav('files/Song_2.wav')
audio = audio.set_channels(CHANNELS)
audio = audio.set_frame_rate(FRAME_RATE)

# Воспроизводим аудио
play(audio)

# Преобразуем аудио в бинарный формат
audio_binary = audio.raw_data

max_frames = len(audio_binary)


# Проход по аудиофайлу и распознавание
rec.AcceptWaveform(audio_binary)
result = rec.FinalResult()
text = json.loads(result)["text"]
print(text)

# TODO
# Добавляем пунктуацию (работает через стороннее API, найти другой вариант )
# try:
#     cased = subprocess.check_output('python3 recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)
#     raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

# Записываем результат в файл "data.txt"
with open('files/data.txt', 'w') as f:
    json.dump(text, f, ensure_ascii=False, indent=4)
