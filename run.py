from flask import Flask, render_template
from taipy import Gui

app = Flask(__name__)

@app.route('/record')
def hello_world():
    return render_template("index.j2")

gui = Gui(page="# Taipy application", flask=app)

if __name__ == '__main__':
    gui.run()