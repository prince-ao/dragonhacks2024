from flask import request, make_response
from flask_restx import Namespace, Resource
from scripts.nlp import convert_audio_to_text, Hear2Learn
from db import db, Lecture

audio_handle_ns = Namespace('handle-audio', description='audio handling module')

hear = Hear2Learn()
user_text = ""

@audio_handle_ns.route('/stream')
class AudioHandler(Resource):
    def post(self):
        global user_text

        body = request.get_json()


        body_convert = convert_audio_to_text(body['data'])

        user_text = user_text + body_convert

        resp = make_response(body_convert)

        resp.content_type = 'text/plain'

        return resp