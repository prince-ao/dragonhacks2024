from flask import request
from flask_restx import Namespace, Resource
from scripts.nlp import convert_audio_to_text

audio_handle_ns = Namespace('handle-audio', description='audio handling module')

@audio_handle_ns.route('/')
class AudioHandler(Resource):
    def post(self):
        body = request.get_json()

        print(body['data'])
        print(convert_audio_to_text(body['data']))