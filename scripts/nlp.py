import whisper
import os
import json
import warnings
import numpy as np
from embedchain import App
from ast import literal_eval
warnings.filterwarnings('ignore')
        

def convert_audio_to_text(audio_file):
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file, temperature=0., fp16=False)
    return result['text']


class Hear2Learn:
    
    def __init__(self) -> None:
        
        with open('../creds.json') as f:
            creds = json.load(f)
            os.environ["HUGGINGFACE_ACCESS_TOKEN"] = creds['HFTOKEN']
        
        self.app = App.from_config(config=self.generate_app_config())
        
        self.summary_instruction = """Task: Analyze the input text and identify different topics being discussed. For each topic generate a summary. Generate the summaries as bullet points for each topic. 
        Generate atleast 5 bullet points and atmax 20 bullet points for each topic summary. Provide the result in the following format: Topic\n - bullet point1\n -bullet point2\n
        """
        
        self.quiz_instruction = """Task: Generate a quiz with 10 to 15 questions on the topics provided. Generate the response in json format with {"question": quesiton1, "options": [option1, option2, option3, option4], "answer": "anser1"}"""
        
    def generate_app_config(self, temperature=0.):
        config={
            "llm": {
                "provider": "huggingface",
                "config": {
                    "model": 'mistralai/Mixtral-8x7B-Instruct-v0.1',
                    'top_p': 0.95,
                    'temperature': temperature,
                }
            },
            "embedder": {
                "provider": "huggingface",
                "config": {
                    "model": 'sentence-transformers/all-mpnet-base-v2'
                }
            }
        }
        return config
        
    def summarize_text(self, text):
        prompt = f'{self.summary_instruction}\n + Text: {text}'
        answer= self.app.chat(prompt)
        summaries = answer.split('Answer')[-1]
        self.app.delete_session_chat_history()
        summaries = self.format_summaries(summaries)
        
        return summaries
    
    def generate_quiz(self, context):
        self.app.add(context)
        answer = self.app.chat(self.quiz_instruction)
        quiz = answer.split('Answer')[-1]
        self.app.delete_session_chat_history()
        quiz = self.format_quiz(quiz)
        return quiz
    
    def chat(self, prompt):
        answer = self.app.chat(prompt)
        response = answer.split('Answer')[-1]
        self.app.delete_session_chat_history()
        return response
        
    def format_summaries(self, summaries):
        summaries = summaries.strip(':\n')
        summaries_list = []
        for s in summaries.split('Topic: ')[1:]:
            topic_summs = s.split('\n')
            topic = topic_summs[0]
            points = topic_summs[1:]
            summaries_list.append({
                "topic": topic,
                "points": [point.strip('-').strip() for point in points if len(point) > 1]
            })
            
        return summaries_list
    
    def format_quiz(self, quiz):
        return literal_eval(quiz.strip(":\n").replace("\n", ""))