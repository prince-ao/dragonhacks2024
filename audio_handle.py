from flask import request
from flask_restx import Namespace, Resource

audio_handle_ns = Namespace('handle-audio', description='audio handling module')

@audio_handle_ns.route('/')
class AudioHandler(Resource):
    def post(self):
        print(request.get_data())