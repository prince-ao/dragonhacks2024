from flask import Flask, render_template
from taipy import Gui
from audio_handle import audio_handle_ns
from config import DevConfig
from flask_restx import Api
from taipy.gui import Html, navigate

app = Flask(__name__)

@app.route('/index')
def main_page():
    return render_template("index.j2")

app.config.from_object(DevConfig)



@app.route('/start-lecture')
def start_lecture():
    return render_template("start_lecture.j2")

@app.route('/login')
def login():
    return render_template('login.j2')

@app.route('/signup')
def signup():
    return render_template('signup.j2')

@app.route('/lectures')
def lectures():
    return render_template('lectures.j2')

api = Api(app, version='1.0', title='HearToLearn.tech', description='API for HearToLearn.tech', prefix='/api/v1', doc='/docs')
api.add_namespace(audio_handle_ns)

logo_url = 'http://127.0.0.1:5000/static/images/logo.webp'

def button_pressed(state):
  # React to the button press action
  navigate(state, "/login", tab="_self")

page = """
<|{logo_url}|image|>

<div style="display: flex; justify-content: center; align-items: center;">
    <div style="display: flex; justify-content: center; align-items: center; width: 1100px; padding: 20px; gap: 50px;">
        <p>An accessible auditory AI companion that transforms the way you engage with lectures. Hear2Learn not only records lectures in their entirety but also employs Natural Language Processing to condense content and craft questions and flashcards tailored to your learning needs. Embrace a revolutionized learning experience with Hear2Learn — where efficiency meets efficacy.</p>
        <img src="http://127.0.0.1:5000/static/images/ai-speech.webp" width="500px"/>
    </div>
</div>

<div style="display: flex; justify-content: center; align-items: center;">
    <div style="display: flex; justify-content: center; align-items: center; width: 1100px; padding: 20px; gap: 50px;">
        <p>Powered by Google Cloud API, Hear2Learn offers real-time listening and recording, complemented by an audio file backup. Questions are generated through two innovative methods: NLP analysis for core topics combined with web scraping for problem-solving, and AI integration with ChatGPT for quick, efficient question generation — with safeguards against inaccuracies.</p>
    </div>
</div>

<div style="display: flex; justify-content: center; align-items: center;">
    <div style="display: flex; justify-content: center; align-items: center; width: 1100px; padding: 20px; gap: 50px;">
        <p>Flashcards are effortlessly formatted in JSON for simplicity and effectiveness, akin to popular study tools like Quizlet. Lectures are automatically sectioned by date and time, with customization options available for personal titles.</p>
    </div>
</div>

<div style="display: flex; justify-content: center; align-items: center;">
    <div style="display: flex; justify-content: center; align-items: center; width: 1100px; padding: 20px; gap: 50px;">
        <p>Discover the collaborative edge with account linking for classroom environments, paving the way for potential professor supervision. Plus, with translation features, Hear2Learn is an ally for non-native speakers seeking comprehensive learning support.</p>
    </div>
</div>

<|Begin|button|on_action=button_pressed|class_name=plain|>
"""

gui = Gui(page=page , flask=app)

if __name__ == '__main__':
    gui.run()
