from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os


def main(subtitles):
    
    dir_file_name = f'{subtitles.split("/")[-2]}'

    try:
        os.mkdir(f"files/{dir_file_name}")
    except FileExistsError:
        pass
    
    with open(subtitles, 'r', encoding='utf-8') as file:
        # Читаем содержимое файла
        input_text = file.read()

    # Загрузка токенизатора и модели для перевода с русского на ...
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
    # tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-fr")
    # model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-fr")
    # tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-ar")
    # model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-ar")

    # Пример текста на русском для перевода
    # input_text = "Привет, как дела?"
    
    # Токенизация входного текста
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Получение выходных токенов от модели
    output_ids = model.generate(input_ids)

    # Декодирование выходных токенов в текст
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Вывод результата
    print("Исходный текст:", input_text)
    print("Переведенный текст:", output_text)
    
    with open(f'files/{dir_file_name}/transcription_{dir_file_name}.txt', 'w') as f:
        f.write(output_text)

if __name__ == "__main__":
    subtitles = "files/0/subtitles_0.srt"
    main(subtitles=subtitles)