from moviepy.editor import VideoFileClip, AudioFileClip
import os

def main(voice_path, video_path):
    
    dir_file_name = f'{voice_path.split("/")[-3]}'
    print(dir_file_name)

    try:
        os.mkdir(f"files/{dir_file_name}/out_file/")
    except FileExistsError:
        pass

    # Загрузите видео и аудио
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(voice_path)

    # Наложите аудио на видео
    video_clip = video_clip.set_audio(audio_clip)

    # Сохраните видео с новым аудио
    video_clip.write_videofile(f"files/{dir_file_name}/out_file/out_file_{dir_file_name}.mp4", codec="libx264", audio_codec="aac")



if __name__ == "__main__":
    voice_path = "files/0/voice/combined_0.wav"
    video_path = "files/0.mp4"
    main(voice_path=voice_path, video_path=video_path)