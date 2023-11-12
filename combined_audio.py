from pydub import AudioSegment
import os

def main(voice_path):
    main_dir = "/media/robot/Seagate/hak"
    
    dir_file_name = f'{voice_path.split("/")[-3]}'

    try:
        os.mkdir(f"{main_dir}/files/{dir_file_name}/voice/")
    except FileExistsError:
        pass

    # Создайте пустой объект AudioSegment для объединения аудио
    combined_audio = AudioSegment.silent(duration=0)

    # Пройдите циклом по файлам в папке
    for filename in os.listdir(voice_path):
        if filename.startswith("combined"):
            pass
        elif filename.endswith(".wav"):  # Убедитесь, что файлы – это WAV-файлы (может потребоваться изменение расширения)
            file_path = os.path.join(voice_path, filename)
            audio_segment = AudioSegment.from_wav(file_path)
            combined_audio += audio_segment
        

    # Сохраните объединенное аудио в новый файл
    combined_audio.export(f"{main_dir}/files/{dir_file_name}/voice/combined_{dir_file_name}.wav", format="wav")



if __name__ == "__main__":
    for i in range(100):
        voice_path = f"/media/robot/Seagate/hak/files/{i}/voice/"
        # print(voice_path)
        if os.path.exists(voice_path):
            print(voice_path)
            main(voice_path)
        # if os.path.isdir(voice_path):
        #     print(voice_path)
    # voice_path = "files/0/voice/"
    # main(voice_path=voice_path)