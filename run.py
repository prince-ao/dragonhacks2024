from flask import Flask, render_template
from taipy import Gui
from taipy.gui import Html

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template("main.j2")  # Template for the main Taipy application page

@app.route('/record')
def record():
    return render_template("index.j2")

@app.route('/login')
def login():
    return render_template('login.j2')

@app.route('/signup')
def signup():
    return render_template('signup.j2')

with app.app_context():
        html_page = Html(render_template('login.j2'))
        gui = Gui(page=html_page,flask=app)

if __name__ == '__main__':
    gui.run()
