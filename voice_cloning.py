from IPython.display import Audio, display
from IPython.utils import io
from synthesizer.inference import Synthesizer
from real.encoder import inference as encoder
from real.vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import librosa
from scipy.io.wavfile import write
import soundfile as sf
import os

def main(in_fpath, transcription):
  
  main_dir = "/media/robot/Seagate/hak"
  
  dir_file_name = f'{in_fpath.split("/")[-1].split(".")[-2]}'
  try:
      os.mkdir(f"{main_dir}/files/{dir_file_name}/voice/")
  except FileExistsError:
      pass
  except FileNotFoundError:
    return
      
  encoder_weights = Path("pretrained/encoder/saved_models/pretrained.pt")
  vocoder_weights = Path("pretrained/vocoder/saved_models/pretrained/pretrained.pt")
  syn_dir = Path("pretrained/synthesizer/saved_models/logs-pretrained/taco_pretrained/pretrained.pt")
  encoder.load_model(encoder_weights)
  synthesizer = Synthesizer(syn_dir)
  vocoder.load_model(vocoder_weights)
  
  with open(transcription, 'r', encoding='utf-8') as file:
        # Читаем содержимое файла
        text = file.read()

  # text = "Python programming language"
  # text = "My Wonderful Family I live in a house near the mountains. I have two brothers and one sister"
  # text = "My Wonderful Family I live in a house near the mountains. I have two brothers and one sister, and I was born last. My father teaches mathematics, and my mother is a nurse at a big hospital. My brothers are very smart and work hard in school. My sister is a nervous girl, but she is very kind. My grandmother also lives with us. She came from Italy when I was two years old. She has grown old, but she is still very strong. She cooks the best food! My family is very important to me. We do lots of things together. My brothers and I like to go on long walks in the mountains. My sister likes to cook with my grandmother. On the weekends we all play board games together. We laugh and always have a good time. I love my family very much."
  words = text.split(" ")
  print(words)
  words_list = list()
  index=0
  for i in range(len(words)):
    if i % 20 == 0:
      words_list.append(" ".join(words[index:i]))
      index=i
    elif i==len(words)-1:
      # print(words[index:i+1])
      words_list.append(" ".join(words[index:i+1]))
  print(words_list)

  in_fpath = Path(in_fpath)
  preprocessed_wav = encoder.preprocess_wav(in_fpath)
  original_wav, sampling_rate = librosa.load(in_fpath)
  preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
  embed = encoder.embed_utterance(preprocessed_wav)
  count=0
  for text in words_list:
    
    with io.capture_output() as captured:
      specs = synthesizer.synthesize_spectrograms([text], [embed])
      
    
    count+=1
    filename = f"{main_dir}/files/{dir_file_name}/voice/voice_{count}.wav"
    if os.path.exists(filename):
        print(f"Уже обработан {filename}")
        return
    try:
      generated_wav = vocoder.infer_waveform(specs[0])
    except ValueError:
      return
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

    # filename = "generated_voice.wav"
    sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)

  # output_file = "generated_voice.mp3"
  # write(output_file, synthesizer.sample_rate, generated_wav)

  # display(Audio(generated_wav, rate=synthesizer.sample_rate))


if __name__ == "__main__":
  videos = "/media/robot/Seagate/hak/files"
  fi_list=[]
  
  for root, dirs, files in os.walk(videos):
      for file in files:
        print(root)
        fi=list()
        for f in os.scandir(root):
          if f.is_file() and f.name.endswith('.wav'):
            # print(os.path.join(root, f))
            fi.append(os.path.join(root, f))
          elif f.is_file() and f.name.endswith('.txt'):
            # print(os.path.join(root, f))
            fi.append(os.path.join(root, f))

          if len(fi)<=1:
            pass
          else:
            fi_list.append(fi)
  print(fi_list)
  for i in fi_list:
    print(i[0], i[1])
    main(i[0], i[1])
        # print(root)
          # if file.endswith('.wav'):# and file.endswith('.txt'):
          #   print(os.path.join(root, file))
          # if file.endswith('.txt'):
          #   print(os.path.join(root, file))
              # main(os.path.join(root, file))
    # in_fpath = "files/0/0.wav"
    # transcription = "files/0/transcription_0.txt"
    # main(in_fpath=in_fpath, transcription=transcription)
