import whisper
import os
import json
import warnings
import numpy as np
from embedchain import App
warnings.filterwarnings('ignore')
        

def convert_audio_to_text(audio_file):
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file, temperature=0., fp16=False)
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
    
    instruction = """
        Task: Analyze the input text and identify different topics being discussed. For each topic generate a summary. Generate the summaries as bullet points for each topic. 
        Generate atleast 5 bullet points and atmax 20 bullet points for each topic summary. 
        Provide the result in the following format: Topic\n - bullet point1\n -bullet point2\n"""
    prompt = f'{instruction}\n + Text: {text}'
    answer= app.chat(prompt)
    bullet_points = answer.split('Answer')[-1]
    app.delete_session_chat_history()
    return bullet_points