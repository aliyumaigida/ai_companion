import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import pyttsx3

model = whisper.load_model("base")

engine = pyttsx3.init()


def record_audio(filename="input.wav", duration=5, fs=44100):

    print("Recording...")

    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    sd.wait()

    wav.write(filename, fs, audio)

    return filename


def transcribe_audio(file):

    result = model.transcribe(file)

    return result["text"]


def speak(text):

    engine.say(text)

    engine.runAndWait()
