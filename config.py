from decouple import config


class DevConfig:
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = True