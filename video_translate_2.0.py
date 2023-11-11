import moviepy.editor as mp
import speech_recognition as sr

# Создаем объект Recognizer
recognizer = sr.Recognizer()

# Открываем видеофайл (в формате, поддерживаемом moviepy)
video_file = "your_video.mp4"
clip = mp.VideoFileClip(video_file)

# Извлекаем аудиодорожку из видео
audio_clip = clip.audio
audio_clip.write_audiofile("temp_audio.wav", codec='pcm_s16le')

# Открываем аудиофайл для распознавания
with sr.AudioFile("temp_audio.wav") as source:
    audio = recognizer.record(source)

# Распознаваем речь
try:
    text = recognizer.recognize_google(audio, language="ru-RU")
    print("Распознанный текст: " + text)

    # Разбиваем текст на 3 строки (в этом примере)
    lines = text.split("\n")
    num_lines = 3
    text = "\n".join(lines[:num_lines])

    # Создаем субтитры с контрастными цветами и измененными отступами
    subtitles = mp.TextClip(text, fontsize=18, color="white", bg_color="black")
    subtitles = subtitles.set_duration(clip.duration)
    subtitles = subtitles.set_position(('center', 0.8), relative=True)  # Поднимаем субтитры

    # # Подгоняем ширину субтитров под ширину видео
    subtitles = subtitles.resize(clip.size[0])

    # Синхронизируем субтитры с видео
    video_with_subtitles = mp.CompositeVideoClip([clip, subtitles])

    # Сохраняем видео с субтитрами
    video_with_subtitles.write_videofile("video_with_subtitles.mp4", codec="libx264")

except sr.UnknownValueError:
    print("Извините, не удалось распознать речь.")
except sr.RequestError as e:
    print("Произошла ошибка при запросе к сервису Google; {0}".format(e))
