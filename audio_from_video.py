from moviepy.editor import VideoFileClip
import os


def video_to_voice(video_file: str):
    
    dir_file_name = f'{video_file.split("/")[-1].split(".")[-2]}'

    try:
        os.mkdir(f"files/{dir_file_name}")
    except FileExistsError:
        pass

    # Создайте объект VideoFileClip для видео
    video_clip = VideoFileClip(video_file)

    # Извлеките аудиодорожку из видео
    audio_clip = video_clip.audio
    # Сохраните аудиодорожку в аудиофайл
    audio_file = f'files/{dir_file_name}/{dir_file_name}.wav'
    audio_clip.write_audiofile(audio_file)

    # Закройте видео и аудиодорожку
    video_clip.close()
    audio_clip.close()

    print(f"Аудио успешно извлечено и сохранено в файл: {audio_file}")
    return audio_file


if __name__ == "__main__":
    video_file = "files/0.mp4"
    video_to_voice(video_file=video_file)
