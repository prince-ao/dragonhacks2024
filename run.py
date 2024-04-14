from flask import Flask, render_template, request, redirect, make_response
from taipy import Gui
from audio_handle import audio_handle_ns
from config import DevConfig
from flask_restx import Api
from taipy.gui import Html, navigate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

app = Flask(__name__)

@app.route('/index')
def main_page():
    return render_template("index.j2")

app.config.from_object(DevConfig)

db = SQLAlchemy(app)

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    length = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo('UTC')))


@app.route('/lecture', methods=['POST', 'GET'])
def lecture():
    if request.method == 'POST':
        body = request.get_json()

        lecture = Lecture.query.get(int(body['id']))

        return { "title": lecture.title }
    else:
        return "Not implemented"

@app.get('/end-lecture')
def end_lecture():
    user_id = request.cookies.get('ml')

    lecture = Lecture.query.get(int(user_id))

    print(lecture.datetime)

    datetime1 = lecture.datetime.replace(tzinfo=timezone.utc).timestamp()
    datetime2 = datetime.now(timezone.utc).timestamp()

    time_difference = datetime2 - datetime1

    elapsed_minutes = time_difference / 60

    lecture.length = elapsed_minutes

    resp = redirect('/create-lecture')

    resp.delete_cookie('ml')

    return resp


@app.route('/create-lecture', methods=['POST', 'GET'])
def create_lecture():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        new_lecture = Lecture(
            title=name,
            description=description
        )

        db.session.add(new_lecture)
        db.session.commit()

        resp = redirect('/start-lecture')

        resp.set_cookie('ml', str(new_lecture.id))

        return resp
    else:
        return render_template("create_lecture.j2")

@app.get('/start-lecture')
def start_lecture():
    return render_template("start_lecture.j2")

@app.get('/login')
def login():
    return render_template('login.j2')

@app.get('/signup')
def signup():
    return render_template('signup.j2')

@app.get('/lectures')
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

<div style="display: flex; justify-content: center; align-items: center; height: 100vh">
    <div style="display: flex; justify-content: center; align-items: center; width: 1100px; padding: 20px; gap: 50px;">
        <p>An accessible auditory AI companion that transforms the way you engage with lectures. Hear2Learn not only records lectures in their entirety but also employs Natural Language Processing to condense content and craft questions and flashcards tailored to your learning needs. Embrace a revolutionized learning experience with Hear2Learn — where efficiency meets efficacy.</p>
        <img src="http://127.0.0.1:5000/static/images/ai-speech.webp" width="500px"/>
    </div>
</div>

<div style="display: flex; justify-content: center; align-items: center; height: 100vh">
    <div style="display: flex; justify-content: center; align-items: center; width: 1100px; padding: 20px; gap: 50px;">
        <p>Powered by Google Cloud API, Hear2Learn offers real-time listening and recording, complemented by an audio file backup. Questions are generated through two innovative methods: NLP analysis for core topics combined with web scraping for problem-solving, and AI integration with ChatGPT for quick, efficient question generation — with safeguards against inaccuracies.</p>
        <img src="http://127.0.0.1:5000/static/images/google-cloud.png" width="400px"/>
    </div>
</div>

<div style="display: flex; justify-content: center; align-items: center; height: 100vh">
    <div style="display: flex; justify-content: center; align-items: center; width: 1100px; padding: 20px; gap: 50px;">
        <p>Flashcards are effortlessly formatted in JSON for simplicity and effectiveness, akin to popular study tools like Quizlet. Lectures are automatically sectioned by date and time, with customization options available for personal titles.</p>
    </div>
</div>

<div style="display: flex; justify-content: center; align-items: center; height: 100vh">
    <div style="display: flex; justify-content: center; align-items: center; width: 1100px; padding: 20px; gap: 50px;">
        <p>Discover the collaborative edge with account linking for classroom environments, paving the way for potential professor supervision. Plus, with translation features, Hear2Learn is an ally for non-native speakers seeking comprehensive learning support.</p>
        <img src="http://127.0.0.1:5000/static/images/teacher.jpg" width="400px"/>
    </div>
</div>

<|Begin|button|on_action=button_pressed|class_name=plain|>
"""

gui = Gui(page=page , flask=app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    gui.run()
