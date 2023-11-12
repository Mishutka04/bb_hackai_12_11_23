from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os


def main(subtitles):
    main_dir = "/media/robot/Seagate/hak"
    
    dir_file_name = f'{subtitles.split("/")[-2]}'

    try:
        os.mkdir(f"{main_dir}/files/{dir_file_name}")
    except FileExistsError:
        pass
    
    file_path = f'{main_dir}/files/{dir_file_name}/transcription_{dir_file_name}_fr.txt'
    if os.path.exists(file_path):
        print(f"Файл был переведён ранее {file_path}")
        return
    
    with open(subtitles, 'r', encoding='utf-8') as file:
        # Читаем содержимое файла
        input_text = file.read()

    """
    Модели кторые могуьт быть использованы для перевода текста,
    
    Helsinki-NLP/opus-mt-ru-en
    Helsinki-NLP/opus-mt-ru-fr
    Helsinki-NLP/opus-mt-ru-es
    Helsinki-NLP/opus-mt-ru-da
    Helsinki-NLP/opus-mt-ru-de
    Helsinki-NLP/opus-mt-ru-it
    Helsinki-NLP/opus-mt-ru-cs
    Helsinki-NLP/opus-mt-ru-pt
    Helsinki-NLP/opus-mt-ru-trk
    Helsinki-NLP/opus-mt-ru-ya
    Helsinki-NLP/opus-mt-ru-pl
    Helsinki-NLP/opus-mt-ru-ch
    """

    
    # Загрузка токенизатора и модели для перевода с русского на ...
    # tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
    # model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-fr")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-fr")
    # tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-ar")
    # model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-ar")

    # Пример текста на русском для перевода
    # input_text = "Привет, как дела?"
    
    # Токенизация входного текста
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # TODO Исправить (Разбить входной текст на более короткие отрезки)
    try:
        # Получение выходных токенов от модели
        output_ids = model.generate(input_ids)
    except IndexError as e:
        print("Превышена длина входных данных", e)
        return

    # Декодирование выходных токенов в текст
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Вывод результата
    print("Исходный текст:", input_text)
    print("Переведенный текст:", output_text)
    
    with open(file_path, 'w') as f:
        f.write(output_text)

if __name__ == "__main__":
    # 
    dict_name_video = dict()
    dataset = pd.read_csv("dataset.csv")
    target_language = list(dataset["target_language"])
    video_name = list(dataset["video_name"])
    dict_name_video = {}
    abbr_dict = {"Немецкий": "de", "Русский":"ru", "Английский": "en", "Французский":"fr", "Итальянский":"it", "Испанский":"es", "Японский":"ja", "Китайский":"cn", "Португальский":"pt", "Чешский":"cs", "Датский":"da", "Польский":"pl","Турецкий":"trk"}
    for i in range(100):
        dict_name_video[video_name[i]] = target_language[i]

    videos = "/media/robot/Seagate/hak/files"
    for root, dirs, files in os.walk(videos):
        for file in files:
            if file.endswith('.srt'):
                print(os.path.join(root, file))
                main(os.path.join(root, file))

    # subtitles = "files/0/subtitles_0.srt"
    # main(subtitles=subtitles)