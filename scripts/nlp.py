import whisper
import os
import json
import warnings
import numpy as np
from embedchain import App
warnings.filterwarnings('ignore')
        

def convert_audio_to_text(model, filepath):
    result = model.transcribe(filepath, temperature=0., fp16=False)
    return result['text']

def summarize_text(text):
    with open('../creds.json') as f:
        creds = json.load(f)
        
    os.environ["HUGGINGFACE_ACCESS_TOKEN"] = creds['HFTOKEN'] #put your access token here

    app = App.from_config(config={
        "llm": {
            "provider": "huggingface",
            "config": {
                "model": 'mistralai/Mixtral-8x7B-Instruct-v0.1',
                'top_p': 0.95,
                'temperature': 0.,
            }
        },
        "embedder": {
            "provider": "huggingface",
            "config": {
                "model": 'sentence-transformers/all-mpnet-base-v2'
            }
        }
    })
    
    instruction = """Task: Analyze the input text and idnetify different topics being discussed. For each topic generate a summary. Generate the summaries as bullet points. Generate atleast 5 bullet points and atmax 20 bullet points for each summary."""
    prompt = f'{instruction}\n + Text: {text}'
    answer= app.chat(prompt)
    bullet_points = answer.split('Answer')[-1].split('\n')
    return bullet_points



if __name__ == '__main__':
    model = whisper.load_model("tiny")
    text = convert_audio_to_text(model, 'harvard.wav')
    print(text)