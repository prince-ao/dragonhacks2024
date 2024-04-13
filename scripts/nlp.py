import base64
import io
from pydub import AudioSegment
import speech_recognition as sr

r = sr.Recognizer()

def convert_webm_to_wav(webm_data):
    audio = AudioSegment.from_file(io.BytesIO(webm_data), format="webm")
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    return wav_io

def convert_ogg_to_wav(ogg_data):
    audio = AudioSegment.from_file(io.BytesIO(ogg_data), format="ogg")
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    return wav_io

def process_audio(data):
    text = ""
    try:
        wav_audio = convert_webm_to_wav(data)

        with sr.AudioFile(wav_audio) as source:
            audio = r.record(source)

            try:
                text = r.recognize_google(audio)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

    return text

def convert_audio_to_text(base64_audio):
    binary_data = base64.b64decode(base64_audio)
    result = process_audio(binary_data)

    return result