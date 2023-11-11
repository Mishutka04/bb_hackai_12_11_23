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

def main():
  encoder_weights = Path("pretrained/encoder/saved_models/pretrained.pt")
  vocoder_weights = Path("pretrained/vocoder/saved_models/pretrained/pretrained.pt")
  syn_dir = Path("pretrained/synthesizer/saved_models/logs-pretrained/taco_pretrained/pretrained.pt")
  encoder.load_model(encoder_weights)
  synthesizer = Synthesizer(syn_dir)
  vocoder.load_model(vocoder_weights)

  # text = "Python programming language"
  text = "My Wonderful Family I live in a house near the mountains. I have two brothers and one sister"
  # text = "My Wonderful Family I live in a house near the mountains. I have two brothers and one sister, and I was born last. My father teaches mathematics, and my mother is a nurse at a big hospital. My brothers are very smart and work hard in school. My sister is a nervous girl, but she is very kind. My grandmother also lives with us. She came from Italy when I was two years old. She has grown old, but she is still very strong. She cooks the best food! My family is very important to me. We do lots of things together. My brothers and I like to go on long walks in the mountains. My sister likes to cook with my grandmother. On the weekends we all play board games together. We laugh and always have a good time. I love my family very much."
  # print(len(text)) # 85
  in_fpath = Path("files/0.wav")
  reprocessed_wav = encoder.preprocess_wav(in_fpath)
  original_wav, sampling_rate = librosa.load(in_fpath)
  preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
  embed = encoder.embed_utterance(preprocessed_wav)
  with io.capture_output() as captured:
    specs = synthesizer.synthesize_spectrograms([text], [embed])
  generated_wav = vocoder.infer_waveform(specs[0])
  generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

  filename = "generated_voice.wav" 
  sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)

  # output_file = "generated_voice.mp3"
  # write(output_file, synthesizer.sample_rate, generated_wav)

  display(Audio(generated_wav, rate=synthesizer.sample_rate))
