from flask import Flask, render_template
from taipy import Gui
from audio_handle import audio_handle_ns
from config import DevConfig
from flask_restx import Api

app = Flask(__name__)

app.config.from_object(DevConfig)

@app.route('/record')
def hello_world():
    return render_template("index.j2")

api = Api(app, version='1.0', title='HearToLearn.tech', description='API for HearToLearn.tech', prefix='/api/v1', doc='/docs')
api.add_namespace(audio_handle_ns)

gui = Gui(page="# Taipy application", flask=app)

"""
asd
"""

if __name__ == '__main__':
    gui.run()