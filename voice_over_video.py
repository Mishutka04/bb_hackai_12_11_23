from moviepy.editor import VideoFileClip, AudioFileClip
import os

def main(voice_path, video_path):
    
    main_dir = "/media/robot/Seagate/hak"
    dir_file_name = f'{voice_path.split("/")[-3]}'
    print(dir_file_name)

    try:
        os.mkdir(f"{main_dir}/files/{dir_file_name}/out_file/")
    except FileExistsError:
        pass

    # Загрузите видео и аудио
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(voice_path)

    # Наложите аудио на видео
    video_clip = video_clip.set_audio(audio_clip)

    # Сохраните видео с новым аудио
    video_clip.write_videofile(f"{main_dir}/files/{dir_file_name}/out_file/out_file_{dir_file_name}.mp4", codec="libx264", audio_codec="aac")



if __name__ == "__main__":
    for i in range(100):
        voice_path = f"/media/robot/Seagate/hak/files/{i}/voice/combined_{i}.wav"
        video_path = f"/media/robot/Seagate/hak/video/{i}.mp4"
        # print(voice_path)
        if os.path.exists(voice_path) and os.path.exists(video_path):
            print(voice_path, video_path)
            main(voice_path, video_path)
    # voice_path = "files/0/voice/combined_0.wav"
    # video_path = "files/0.mp4"
    # main(voice_path=voice_path, video_path=video_path)