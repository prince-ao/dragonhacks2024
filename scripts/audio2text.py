import whisper
        

def convert_audio_to_text(model, filepath):
    result = model.transcribe(filepath, temperature=0., fp16=False)
    return result['text']



if __name__ == '__main__':
    model = whisper.load_model("tiny")
    text = convert_audio_to_text(model, 'harvard.wav')
    print(text)