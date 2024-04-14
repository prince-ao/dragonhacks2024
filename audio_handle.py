from flask import request
from flask_restx import Namespace, Resource
from scripts.nlp import convert_audio_to_text, Hear2Learn

audio_handle_ns = Namespace('handle-audio', description='audio handling module')

h = Hear2Learn()
user_text = ""

@audio_handle_ns.route('/stream')
class AudioHandler(Resource):
    def post(self):
        global user_text

        body = request.get_json()

        body_convert = convert_audio_to_text(body['data'])

        user_text = user_text + body_convert

        return body_convert



@audio_handle_ns.route('/stop')
class AudioHandler(Resource):
    def get(self):
        global usr_text

        summery = h.summarize_text(user_text)

        return summery



